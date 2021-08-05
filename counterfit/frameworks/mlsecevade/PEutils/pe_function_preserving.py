import numpy as np
import functools
import pickle
import json
import gzip
from hyperopt import hp, fmin, tpe, Trials, STATUS_OK
from .pe_modify import PEFileModifier
from collections import OrderedDict
from ..utils import VectorModifier


### globals

# list of (section_name, section_characteristics, section_content), sorted in descending order of size
with gzip.open('counterfit/frameworks/mlsecevade/PEutils/sections.pkl.gz', 'rb') as infile:
    BENIGN_SECTIONS = pickle.load(infile)

# list of overlay_conent, sorted in descending order of size
with gzip.open('counterfit/frameworks/mlsecevade/PEutils/overlays.pkl.gz', 'rb') as infile:
    BENIGN_OVERLAYS = pickle.load(infile)

# list of (library_name, [func1, func2, func3]) listed in descending order of len(function_list)
with open('counterfit/frameworks/mlsecevade/PEutils/imports.json', 'r') as infile:
    BENIGN_IMPORTS = json.load(infile)

# a list of timestamps observed in the wild
with open('counterfit/frameworks/mlsecevade/PEutils/timestamps.json', 'r') as infile:
    BENIGN_TIMESTAMPS = json.load(infile)

ACTIONS = OrderedDict([
            ('upx_unpack', [None]),            # upx_unpack should come first
            ('add_section', BENIGN_SECTIONS),
            ('add_imports', BENIGN_IMPORTS),
            ('append_overlay', BENIGN_OVERLAYS), 
            ('set_timestamp', BENIGN_TIMESTAMPS),
        ])

MAX_SECTIONS = 20    # add up to this amount of new sections
MAX_LIBRARIES = 20   # add up to this amount of libraries

class PE_ARTWrapperClass:
    def __init__(self, *args, art_attack_cls, **kwargs):
        self.vec_mod = VectorModifier(ACTIONS, PEFileModifier)

        # override the input shape and clip values for the wrapper target
        # args[0] is the ART Target model
        self.estimator = args[0]

        self._attack_cls = art_attack_cls(*args, **kwargs)

    # override ART method to generate attack
    def generate(self, x, y=None):
        # input: x is a list of bytes, y is an optional list of target labels
        old_clip = self.estimator._clip_values
        old_shape = self.estimator._input_shape
        self.estimator._input_shape = (self.vec_mod.input_size, )
        self.estimator._clip_values = (0, 1)
        
        # create list of transformations for each sample
        X = np.zeros((len(x), self.vec_mod.input_size), dtype=np.float32)  # TODO: this is fake

        # wrap the __call__ function with a PE byte transformation of the actual input
        model_api = self._attack_cls.estimator.predict

        # function for modifying samples and submitting to the underlying API
        def modify_and_submit_bytes(list_of_mods, batch_size):
            if len(list_of_mods) > len(x):
                # some ART algorithms blast the API with random noise, which are of a different size than the input x.
                # These correspond to random actions.  For which sample?
                # As a hack, we'll select samples at random to return the appropriate shape
                xx = np.array([random.choice(x) for _ in range(len(list_of_mods))])
            else:
                xx = np.array(x)
            modified_bytes = [self.vec_mod(mod, bytez) for mod, bytez in zip(list_of_mods, xx)]
            return model_api(modified_bytes, batch_size)

        # hack to redict self.model._predictions to transform the data before calling
        self._attack_cls.estimator.predict = modify_and_submit_bytes
        
        # call the underlying generate method
        if y is None:
            results = self._attack_cls.generate(X)

        else:
            results = self._attack_cls.generate(X, y)            

        # restore the original function
        self._attack_cls.estimator.predict = model_api

        # restore estimator properties
        self.estimator._input_shape = old_shape
        self.estimator._clip_values = old_clip

        # return transformed results as binary files
        return np.array([self.vec_mod(mod, bytez) for mod, bytez in zip(results, x)])

def PE_wrap_ART_attack(cls):
    # use like this:     attack_cls = PE_wrap_ART_attack(BoundaryAttack)
    return functools.partial(PE_ARTWrapperClass, art_attack_cls=cls)


class PEHyperoptAttack:
    ''' uses hyperopt's Tree Parzen Estimator (TPE) for black-box optimization
    of a parameter space that consists of function-preserving file modifications '''

    def __init__(self, estimator, max_evals, **kwargs):
        self.max_evals = max_evals
        self.estimator = estimator

        self.vec_mod = VectorModifier(ACTIONS, PEFileModifier)

        # override the input shape and clip values for the wrapper target
        # estimator is an ART Target model
        estimator._input_shape = (self.vec_mod.input_size, )
        estimator._clip_values = (0, 1)

        # initialize optimization space
        section_opts = {f's{s}': hp.choice(f's{s}', [None, {'idx': hp.randint(f's_idx_{s}', len(BENIGN_SECTIONS)),
                                                            'pct': hp.uniform(f's_pct_{s}', 0, 1)}])
                        for s in range(MAX_SECTIONS)}

        import_opts = {f'i{s}': hp.choice(f'i{s}', [None, {'idx': hp.randint(f'i_idx_{s}', len(BENIGN_IMPORTS)),
                                                           'pct': hp.uniform(f'i_pct_{s}', 0, 1)}])
                       for s in range(MAX_LIBRARIES)}

        overlay_opts = hp.choice('overlay_info', [None, {'idx': hp.randint('o_idx', len(BENIGN_OVERLAYS)),
                                                         'pct': hp.uniform('o_pct', 0, 1)}])

        self.space = {
            'add_section': section_opts,
            'add_imports': import_opts,
            'append_overlay': overlay_opts,
            'set_timestamp': hp.choice('modify_timestamp', [None, {'pct': hp.uniform('t_pct', 0, 1)}]),
            'upx_unpack': hp.choice('upx_unpack', [False, True])
        }


    def query_to_vector(self, sample):
        vector = np.zeros((self.vec_mod.input_size, ), dtype=np.float32)
        # unpack?
        if sample['upx_unpack']:
            vector[self.vec_mod.action_offset['upx_unpack']] = 1

        # add some sections
        for _, v in sample['add_section'].items():
            if v:
                vector[self.vec_mod.action_offset['add_section'] + v['idx']] = v['pct']

        # add some imports
        for _, v in sample['add_imports'].items():
            if v:
                vector[self.vec_mod.action_offset['add_imports'] + v['idx']] = v['pct']

        # add to the overlay
        if sample['append_overlay']:
            v = sample['append_overlay']
            if v:
                vector[self.vec_mod.action_offset['append_overlay'] + v['idx']] = v['pct']

        # modify the timestamp
        if sample['set_timestamp']:
            v = sample['set_timestamp']
            if v:
                vector[self.vec_mod.action_offset['set_timestamp']] = v['pct']

        return vector


    # override ART method to generate attack
    def generate(self, x, y=None):
        # input: x is a list of bytes, y is an optional list of target labels
        
        # create list of transformations for each sample
        X = np.zeros((len(x), self.vec_mod.input_size), dtype=np.float32)  # TODO: this is fake

        # wrap the __call__ function with a PE byte transformation of the actual input
        model_api = self.estimator.predict

        # use hyperopt to minimize an objective function
        # function to optimize
        def f(sample, bytez):
            v = self.query_to_vector(sample)
            new_bytez = self.vec_mod(v, bytez)
            score = model_api([new_bytez])[0][1]  # assuming a binary classifier
            return {"loss": score, "status": STATUS_OK, "space": sample, "pred": score}
  
        # do the minimization for each sample
        results = []
        for bytez in x:
            history = {'trials': Trials(), 'evals': 0}
            fmin(fn=functools.partial(f, bytez=bytez), space=self.space, algo=tpe.suggest, max_evals=self.max_evals, trials=history['trials'], verbose=True)
            best = history['trials'].best_trial['result']['space']
            bestv = self.query_to_vector(best)
            results.append(bestv)

        # return transformed results as binary files
        return np.array([self.vec_mod(mod, bytez) for mod, bytez in zip(results, x)])


if __name__ == '__main__':
    import os
    from collections import defaultdict
    import random
    import lief

    # gather filenames
    filenames = []
    for root, dirs, files in os.walk('/mnt/c/Program Files'):
        for fn in files:
            if fn[-4:] in ['.acm','.cpl','.dll','.drv','.efi','.exe','.mui','.ocx','.scr','.sys','.tsp'] or fn.endswith('.ax'):
                filenames.append(os.path.join(root, fn))

    sections = []
    overlays = []
    imports = defaultdict(set)
    timestamps = []

    random.shuffle(filenames)

    for fn in filenames[:2000]:
        print(os.path.join(root,fn))
        pe = lief.parse(os.path.join(root, fn))
        if not pe:
            continue
        for s in pe.sections:
            sections.append((s.name, s.characteristics, bytes(s.content)))
        for lib in pe.imports:
            for func in lib.entries:
                imports[lib.name].add(func.name)
        timestamps.append(pe.header.time_date_stamps)
        overlays.append(bytes(pe.overlay))

    imports = [(k, list(v)) for k, v in imports.items()]

    # let's sort by content length
    sections.sort(key=lambda x: len(x[2]), reverse=True)
    overlays.sort(key=lambda x: len(x), reverse=True)
    imports.sort(key=lambda x: len(x[1]), reverse=True)

    # let's filter sections
    from collections import Counter

    def updatecounter(k, counter):
        counter.update([k])
        return counter[k]

    scounter = Counter()
    sections = [(s[0], s[1], s[2][:2**20]) for s in sections if updatecounter(f'{s[0]}{s[1]}', scounter) <= 2]  # how many of each name/characteristics?
    overlays = [o[:2**20] for o in overlays if len(o) >= 1024]
    imports = [i for i in imports if len(i[1]) >= 5]

    import pickle
    import gzip
    import json

    MAX_FILES = 20
    sections = sections[:MAX_SECTIONS]
    overlays = overlays[:MAX_FILES]
    imports = imports[:MAX_LIBRARIES]

    random.shuffle(timestamps)
    timestamps = sorted(timestamps[:MAX_FILES])

    with gzip.open('sections.pkl.gz', 'wb') as outfile:
        pickle.dump(sections, outfile)
    
    with gzip.open('overlays.pkl.gz', 'wb') as outfile:
        pickle.dump(overlays, outfile)

    with open('imports.json', 'w') as outfile:
        json.dump(imports, outfile)

    with open('timestamps.json', 'w') as outfile:
        json.dump(timestamps, outfile)
