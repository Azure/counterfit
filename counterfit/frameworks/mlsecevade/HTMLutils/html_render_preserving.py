import numpy as np
import functools
import json
import yaml
from hyperopt import hp, fmin, tpe, Trials, STATUS_OK
from collections import OrderedDict
import tqdm
from .html_modify import HTMLModifier
from ..utils import VectorModifier
import random


### globals

# A dictionary containing Base64 representations of images 
BENIGN_IMAGES = yaml.safe_load(open('counterfit/frameworks/mlsecevade/HTMLutils/images.yaml', 'r', encoding='utf-8'))['images']
BENIGN_IMAGES = list(BENIGN_IMAGES.values())  # keep only a list of images

# Long strings to be used for: insert_hidden_text, insert_commented_text
BENIGN_TEXTS = json.load(open('counterfit/frameworks/mlsecevade/HTMLutils/paragraphs.json', 'r', encoding='utf-8'))

# List of strings representing URLs
BENIGN_HREFS = json.load(open('counterfit/frameworks/mlsecevade/HTMLutils/hrefs.json', 'r', encoding='utf-8'))

# Short strings to be used as content for: insert_meta_tag_description,
# insert_meta_tag_keywords, insert_data_attribute
BENIGN_STRINGS = json.load(open('counterfit/frameworks/mlsecevade/HTMLutils/strings.json', 'r', encoding='utf-8'))

# Dictionaries of scripts. The unsafe one should be used only with 
# insert_commented_script.
BENIGN_SCRIPTS_UNSAFE = yaml.safe_load(open('counterfit/frameworks/mlsecevade/HTMLutils/scripts_unsafe.yaml', 'r', encoding='utf-8'))['scripts']
BENIGN_SCRIPTS_UNSAFE = list(BENIGN_SCRIPTS_UNSAFE.values())

BENIGN_SCRIPTS_SAFE = yaml.safe_load(open('counterfit/frameworks/mlsecevade/HTMLutils/scripts_safe.yaml', 'r', encoding='utf-8'))['scripts']
BENIGN_SCRIPTS_SAFE = list(BENIGN_SCRIPTS_SAFE.values())

BENIGN_SCRIPTS_OBF = yaml.safe_load(open('counterfit/frameworks/mlsecevade/HTMLutils/scripts_obfuscated.yaml', 'r', encoding='utf-8'))['scripts']
BENIGN_SCRIPTS_OBF = list(BENIGN_SCRIPTS_OBF.values())


ACTIONS = OrderedDict([
    ('insert_commented_script', BENIGN_SCRIPTS_UNSAFE),
    ('insert_useless_script', BENIGN_SCRIPTS_SAFE),
    ('insert_obfuscated_script', BENIGN_SCRIPTS_OBF),
    ('insert_commented_text', BENIGN_TEXTS), 
    ('insert_hidden_text', BENIGN_TEXTS),
    ('insert_hidden_image', BENIGN_IMAGES),
    ('insert_hidden_links', BENIGN_HREFS),
    ('insert_meta_tag_description', BENIGN_STRINGS),
    ('insert_meta_tag_keywords', BENIGN_STRINGS),
    ('insert_data_attribute', BENIGN_STRINGS),
])

class HTML_ARTWrapperClass:
    def __init__(self, *args, art_attack_cls, **kwargs):
        self.vec_mod = VectorModifier(ACTIONS, HTMLModifier, default_args=1)

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

def HTML_wrap_ART_attack(cls):
    # use like this:     attack_cls = HTML_wrap_ART_attack(BoundaryAttack)
    return functools.partial(HTML_ARTWrapperClass, art_attack_cls=cls)


class HTMLHyperoptAttack:
    ''' uses hyperopt's Tree Parzen Estimator (TPE) for black-box optimization
    of a parameter space that consists of function-preserving file modifications '''

    def __init__(self, estimator, max_evals, **kwargs):
        self.max_evals = max_evals
        self.estimator = estimator
        self.vec_mod = VectorModifier(ACTIONS, HTMLModifier, default_args=1)

        # override the input shape and clip values for the wrapper target
        # estimator is an ART Target model
        estimator._input_shape = (self.vec_mod.input_size, )
        estimator._clip_values = (0, 1)

        # initialize optimization space
        ('insert_commented_script', BENIGN_SCRIPTS_UNSAFE),
        ('insert_useless_script', BENIGN_SCRIPTS_SAFE),
        ('insert_obfuscated_script', BENIGN_SCRIPTS_OBF),
        ('insert_commented_text', BENIGN_TEXTS), 
        ('insert_hidden_text', BENIGN_TEXTS),
        ('insert_hidden_image', BENIGN_IMAGES),
        ('insert_hidden_links', BENIGN_HREFS),
        ('insert_meta_tag_description', BENIGN_STRINGS),
        ('insert_meta_tag_keywords', BENIGN_STRINGS),
        ('insert_data_attribute', BENIGN_STRINGS),

        self.space = {}
        MAX_OPTIONS = 5
        for func, options in ACTIONS.items():
            self.space[func] = {f'{func}{n}': hp.choice(f'{func}{n}', [None, {'idx': hp.randint(f'{func}idx{n}', len(options))}])
                        for n in range(MAX_OPTIONS)}


    def query_to_vector(self, sample):
        aiv_pairs = []
        for k, func_n in sample.items():
            for v in func_n.values():
                if v is not None:
                    aiv_pairs.append((k, v['idx'], 1))
        vector = self.vec_mod.create_vector(aiv_pairs)
        # example: [('insert_commented_script', 2, 1)] means "set to 1 at the vector index for the 2nd content option for 'insert_commented_script'""

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



class HTMLRandomizedDescentAttack:
    ''' Implements a Coordinate Descent based attack using a randomized 
    selection policy over the action space
    '''

    def __init__(self, estimator, n_iters, n_times, **kwargs):
        self.n_iters = n_iters
        self.n_times = n_times
        self.estimator = estimator
        self.vec_mod = VectorModifier(ACTIONS, HTMLModifier, default_args=1)

        self.threshold = 0.5
        self.target = 0.0

        # override the input shape and clip values for the wrapper target
        # estimator is an ART Target model
        estimator._input_shape = (self.vec_mod.input_size, )
        estimator._clip_values = (0, 1)

    def generate(self, x, y=None):
        """ Generate evasive sample from data. This attack is untargeted.
        Overrides ART generate method

        Args:
            x (numpy.ndarray): original samples to modify
            y (numpy.ndarray, optional): Defaults to None.
        """

        results = []
        model_api = self.estimator.predict

        for sample_num, cur_sample in enumerate(x):
            # This vector will contain the frequencies of each action.
            # Negative frequencies indicate damaging actions.
            sel_actions = np.zeros(self.vec_mod.input_size)

            prev_score = model_api([cur_sample])[0][1]

            for _ in tqdm.tqdm(range(self.n_iters), desc=f'sample {sample_num+1}'):
                # Select a random action that is not marked as damaging
                a_ind = np.random.choice(np.where(sel_actions >= 0)[0])

                cur_actions = np.copy(sel_actions)
                cur_actions[a_ind] += 1
                
                # Workaround to allow action repetitions
                while np.any(cur_actions > 0):
                    new_sample = self.vec_mod(cur_actions, cur_sample)
                    cur_actions = cur_actions - 1

                new_score = model_api([new_sample])[0][1]

                # If the new score is closer to the target class accept the action,
                # and reset the list of actions to exclude
                # If the new score is further from the target, reject the action.
                if abs(new_score - self.target) < abs(prev_score - self.target):
                    sel_actions[a_ind] += 1
                    cur_sample = new_sample
                    prev_score = new_score
                else:
                    sel_actions[a_ind] -= 1
                
                # If the new score is closer to the target than the threshold, it
                # means we have crossed the decision boundary -- the sample
                # is evasive
                if abs(new_score - self.target) < abs(self.target - self.threshold):
                    break

            results.append(cur_sample)

        return np.array(results)
