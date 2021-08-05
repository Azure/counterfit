from collections import OrderedDict
import inspect
import numpy as np

class VectorModifier:
    def __init__(self, actions: OrderedDict, baseclass: object, default_args = 0):
        # actions contains {function_name, list_of_arguments} pairs
        # baseclass contains methods for each function_name, and has a "content" property

        # lookup table for number of options for each action
        self.action_size = OrderedDict([ (k, len(v)) for k, v in actions.items() ])

        # store the base class
        self.baseclass = baseclass  # a PEFileModifier or HTMLModifier object

        # create a list that maps vector index to a discrete action that is a ('function', arguments) pair
        self.lookup = []
        self.action_offset = {}  # self.action_offset[function] = offset into vector
        for function, arglist in actions.items():
            self.action_offset[function] = len(self.lookup)
            for arguments in arglist:
                self.lookup.append((function, arguments))

        # expose size of action vector
        self.input_size = len(self.lookup)

        # how many default arguments in the function calls
        self.default_args = default_args

    def create_vector(self, aiv_pairs):
        # aiv_pairs is a list of (action_name, content_index, value) triplets
        vector = np.zeros((self.input_size, ), dtype=np.float32)

        for action, index, value in aiv_pairs:
            vector[self.action_offset[action]+index] = value

        return vector

    def __call__(self, action_vector, input_bytes):
        # takes a single vector and a single binary file as input
        #modpe = PEFileModifier(input_bytes, verbose=False)
        modifier = self.baseclass(input_bytes)

        for i, v in enumerate(action_vector):
            pct = action_vector[i]
            if pct > 0:
                funcname, content = self.lookup[i]
                func = getattr(modifier, funcname)
                sig = inspect.signature(func)
                # modify the sample
                if len(sig.parameters) == 0:
                    func()  # no arguments
                elif len(sig.parameters) > 1 + self.default_args:
                    func(*content)  # multiple arguments
                else:
                    func(content)  # default: single argument

        return modifier.content