# Targets
A target is a user-created class that is the interface between a target model and the attacks included in a framework. Microsoft Counterfit implements the user interface this way to handle the wide variety of ways a user could interact with a target model. There is no universal interface to a machine learning endpoint: Counterfit can interact with a model on disk or hosted behind an API. To provide a clean interface, there are some strict requirements imposed on a target class. The requirements can seem restricting at first, but once you understand how Counterfit interacts with backend frameworks through this interface, attacking new targets will become a breeze.

## Creating a Target
There are two ways to create a new target, either by executing the new command and following the instructions, or simply hacking together a new target from an existing one. On start targets are loaded from a targets folder defined in counterfit/core/config.py, which by default is counterfit/targets. Each target module is contained in its own target folder. This folder is used to store any resources the target may need such as data, models, other python files, etc. 

A target class should inherit from the chosen frameworks baseclass. This baseclass acts as an interface to ensure all required information and methods to successfully build, manage, and run attacks for the framework are present. Inside the target class, a user needs to set a few meta-properties and compose two functions. These properties and functions are the same for all targets in Counterfit. 

### Required Target Information
The required properties for a target consist of the following items,

| Property | Description |
|--- | --- |
| `target_name` | Should be unique among all targets. This is used to uniquely identify a target model within Counterfit. For example, `list targets`. |
| `target_data_type` | The type of data the target model uses. This is used to attach the relevant attacks to a given target. Models for which `target_data_type` is `text` will be compatible with attacks from the TextAttack framework. Adversarial Robustness Toolbox works with `numpy` and `image` data types. |
| `target_endpoint` | API route or model file location where Counterfit will collect outputs. This may be used in the `load` function to load a model file (when referring to a filename), or the `predict` function during an attack to interact with an API (when referring to an API route). | 
| `target_input_shape` | The shape of the input to a target model. Backend frameworks use this to understand the shape of the sample. The `predict` function expects a batch of inputs of this shape, e.g., an input of size `(batch_size, ) + target_input_shape`, where `batch_size` is typically just 1. |
| `target_output_classes` | A list of all output labels returned by the `predict` function. This is used by Counterfit's `outputs_to_labels` function to convert numerical outputs to labels that you define.  It helps Counterift know whether an attack has been successflu or not.
| `X` | The sample data, which is of shape `(N, ) + target_input_shape`, where `N` is the number of samples you included in the target definition.|

The required method for a target consists of the following items,

| Method | Description |
| --- | --- |
| `load(self)`| This function should load models and load and process input data.|
|`predict(self, x)` | This function is the primary interface between a target model and an attack algorithm. An attack algorithm uses this function to submit inputs via `x` and collect the output via the return value.  This function must return a list of probabilities for each input sample.  That is, for each row in `x` there should be an output row of the form `[prob_class_0, prob_class_1, ..., prob_class_2]`.|

## Sample Target Class
At the top of the file are standard module imports and the selected Counterfit framework. Targets will be loaded only if they inherit from a correct baseclass. There are no limits to what you can import, however, they are loaded on start, so heavy ML libraries could slow down the start process. 

```python
import requests
import numpy as np
from counterfit.core.interfaces import ArtTarget
```

Next, the target class is created, and the required properties are defined. 

```python
class CatClassifier(ArtTarget):
    target_name = 'catclassifier'
    target_data_type = 'image'
    target_endpoint = "http://contoso.ai/predict"
    target_input_shape = (3, 256, 256)
    target_output_classes = ["cat", "not_a_cat"]
    X = []
```

| Property | Description | 
| -- | -- |
| target_name | A unique name. Counterfit references each target by name. All logs and results will be stored in this class. |
| target_data_type | The cat classifier target, hosted at `http://contoso.ai/predict` requires pictures of cats. The target_data_type reflects the input data should be an image. Counterfit uses this field to process and reshape data correctly. |
| target_endpoint | This is where Counterfit will collect outputs from the target. This is used in the `predict` function during an attack. |
| target_input_shape | This is the shape of our sample data. It is important to note that this is not necessarily the shape of the target model input, but rather the shape of the sample data. |
| target_output_classes | Are the possible classes for the samples. The image is either a cat, or not a cat.|
| X | Are the sample data. This will be populated in the load function.|

Next, the `load` function should load the required resources. This function is not called until you interact with a target. Sample data should be loaded into `self.X` as a list of lists, arrays, or vectors. Sample selection for both targeted and untargeted attacks are set by referencing an index of this list. As noted earlier, it is important that the shape of an input sample matches the `target_input_shape`. There are no limits to what you can do inside `load`, load models, process samples, execute functions written elsewhere, etc.

```python
def load(self):
    self.X = [[x1], [x2], [x3], ...]
```

Finally, the `predict` function. This function is used by an attack algorithm to send a query to the `target_endpoint`. `x` is the sample the algorithm has provided and is of shape `(1,) + target_input_shape`, or `((1, 3, 256, 256))`. Conventionally, ML frameworks use "batches" of inputs, and it is best practice for the `predict` function to include handle an entire batch, e.g., sending each sample in the batch to an API that may handle only a single query at a time.  However, since most attacks in Counterfit do not require a batch size greater than one, in this example, we'll use `x[0]` to reference the first sample in the batch.

```python
def predict(self, x):
    sample = x[0].tolist()
    response = requests.post(self.endpoint, data={"input": sample})
    results = response.json()

    cat_proba = results["confidence"]
    not_a_cat_proba = 1-cat_proba
        
return [cat_proba, not_a_cat_proba]
```

`predict` function **MUST** return a list of probabilities that is the same length and in the same order as `target_output_classes`. Backend frameworks use both during attack runtime and if they are not the same length, an error will be thrown. If the ordering of the returned list of probabilities is incorrect, the attack will alter the input incorrectly. There are no limits to what you can do inside `predict`, this includes reshaping arrays to images, executing webhooks, or additional logging. Learn more about the flexibility of Counterfit targets in [Advanced Use]

_Note: Pay attention to the channels of an image. By default, backend framework wrappers and Counterfit are configured to use channels first rather than last, (3, 256, 256) vs (256, 256, 3). This can be overridden by adding `self.channels_first=False` to the target class._

## The Final Target Class
```python

import requests
import numpy as np
from counterfit.core.interfaces import ArtTarget

class CatClassifier(ArtTarget):
    target_name = 'catclassifier'
    target_data_type = 'image'
    target_endpoint = "http://contoso.ai/predict"
    target_input_shape = (3, 256, 256)
    target_output_classes = ["cat", "not_a_cat"]
    X = []

    def load(self):
        self.X = [[x1], [x2], [x3], ...]

    def predict(self, x):
        # process an entire batch of requests
        results = []
        for sample in x:
            response = requests.post(self.endpoint, data={"input": sample})
            results = response.json()

            cat_proba = results["confidence"]
            not_a_cat_proba = 1-cat_proba
            results.append([cat_proba, not_a_cat_proba])
        
        return results

```

--

# Frameworks
Counterfit uses existing adversarial ML frameworks for attack algorithms. Some of them are heavy to load and on start, makes for a slow experience. Instead, Counterfit loads a framework when requested with the load command. Each framework has its own baseclass that handles the information coming from a target class. You will notice not all attacks are in each framework – some are missing because they are Whitebox; others are missing due to incompatibility with Counterfit.

### `load()`: 
During load, a framework should load the attacks classes it is responsible for. There are many ways to do this, and some frameworks can be extremely complicated and heavy to load (`art`), or be really lightweight and custom (`augly`). Counterfit also provides the option to load a framework from a json config file.

To load from an attack, use `add_attack` with the required parameters. This function creates a namedtuple that Counterfit references to populate the interface and build attacks. A namedtuple was chosen because of it immutable properties, this allows Counterfit to keep the interface nice and tidy without a user being able to overwrite or create various properties during run time.

```python
# The attack class to add
new_attack = module.AttackClass

# Add the attack to the framework
self.add_attack(
    attack_name=new_attack.__name__,
    attack_type=attack_type.__name__,
    attack_category=attack_category,
    attack_data_tags=attack_data_tags,
    attack_class=loaded_attack,
    attack_default_params=default_params)
```

### `build()`:
Build is called by `state.build_new_attack()` and should return an instantiated attack ready to be configured and run. Build takes the namedtuple object created during load. It pulls the attack out of attack_class and should return an instantiated attack. For any given framework, this build step is usually found in the examples section. After building the attack, Counterfit creates a `CFAttack` object that is used for the remainder of the attack life-cycle. Unlike the namedtuple, `CFAttack` is a standard class and can be altered as needed or required by the framework.

```python

attack_entry.attack_class.build()
```

### `run()`:
Run is called by `state.run_attack()` and takes a `CFAttack` object as a parameter. This is where the framework can execute the attack and return the results. `CFAttack` is an aggregation and carries a large amount of information with it, for example `cfattack.target` provoide ccess to the target instance, `cfattack.options` provides access attack options, `cfattack.logger`provided access to the logger instance. 

### `check_success()`
check_success is called by `state.run_attack()` and should return a bool value denoting the success of the attack. 

### `post_attack_processing()`
Counterfit comes with some basic reporting functionality. If there are custom reports or attacks or datatypes Counterfit does not support. This can be overridden to create these reports. 

## TextAttack
Counterfit includes a number of blackbox attacks against text models from the TextAttack framework. These attacks have no parameters and the user need only set a `target_sample` when running an attack. TextAttack requires that `self.X` be a list of sentences to be used as input to a model.

When implementing a target for Textattack, please note that TextAttack currently expects that `target_output_classes` to be a list of ordered integers beginning at 0 (e.g., [0, 1, 2]) rather than a list of labels (e.g., ['cat', 'dog', 'horse']). This is because it uses the class label as an index.

## Adversarial Robustness Toolkit 
Counterfit includes a number of blackbox evasion attacks suitable for targets of the 'numpy' or 'image' data type using the Adversarial Robustness Toolbox (ART) . ART expects `self.X` to be a list of lists, that is, each row in the list corresponds to an input sample, and each input sample is a list of numbers or images. Thus, it's typical that `self.X` is an array of dimensions (N, dim) (for numpy), (N, channels, height, width) for image with channels_first=True) (default), or (N, height, width, channels) for image with channels_first=False.

ART attacks have parameters that may be set to adjust how the algorithm interacts with a target model. Detailing the parameters for each algorithm is out of the scope of this document. Users may use `show info` to learn more about an attack algorithm and its parameters.

```
creditfraud>hop_skip_jump> show info --attack hop_skip_jump

Attack Information
-----------------------------------------------------------------------------------------------------------
              attack name  hop_skip_jump
              attack type  evasion
          attack category  blackbox
              attack tags  ['image', 'numpy']
         attack framework  art
              attack docs   Implementation of the HopSkipJump attack from Jianbo et al. (2019). This is a
                           powerful black-box attack that   only requires final class prediction, and is an
                           advanced version of the boundary attack. | Paper link:
                           https://arxiv.org/abs/1904.02144

Attack Parameter (type)      Default
---------------------------------------
          targeted (bool)  False
               norm (int)  2
           max_iter (int)  50
           max_eval (int)  10000
          init_eval (int)  100
          init_size (int)  100
       sample_index (int)  0
       target_class (int)  0
```

In this case, the help shows that more information about `hop_skip_jump` can be gleaned by reading the [academic paper](https://arxiv.org/abs/1904.02144) . 

_Note that `sample_index` and` target_class` are properties of all attacks. In particular `target_class` may only be used by some algorithms that support a targeted attack, and in cases where targeted is set to be `True`._

# Attacks
blah blah blah

# Commands
Commands in Counterfit provide the functionality that allow objects to interact. The commands are structured to provides a similar workflow to other offensive security tools, where you typically interact with one target at a time and execute actions against that target. Counterfit keeps a state that keeps track of all interaction and available  objects in the session. Commands use `cmd2` for command categorization and `argparse` for argument handling. For example, the interact command,

```python
import argparse
from cmd2 import Cmd2ArgumentParser, with_argparser, with_category

from counterfit.core.state import CFState

def get_targets():
    return CFState.state().list_targets()

parser = Cmd2ArgumentParser()
parser.add_argument("target", choices=get_targets())

@with_argparser(parser)
@with_category("Counterfit Commands")
def do_interact(self, args: argparse.Namespace) -> None:
    """Sets the the active target. 

    Args:
        target 

    Returns:
        None
    """

    # Load the target
    target = CFState.state().load_target(args.target)

    # Set it as the active target
    CFState.state().set_active_target(target)
```

## Adding a New Command
Adding a new command is simple. Create a new file in the `counterfit/core/commands/` folder and set up the command structure, 

```
import argparse
import cmd2

from core.state import CFState

parser = Cmd2ArgumentParser()
parser.add_argument(…)
```

You could change the category or keep it the same. Changing the category will cause the command to display separately from Counterfit commands. Next, write the function to interact with the current state. 

```python
@cmd2.with_argparser(parser)
@cmd2.with_category("Custom Commands")
def do_thing(self, args):
    """Do cool stuff"""

    active_target = CFState.state().get_active_target()
    print(active_target.target_name)
```

After a new command has been added, use `reload --commands` to load the command into the session. 

## Dynamic Options
Counterfit doesn't load frameworks or targets by default, and in order to react to environment changes (like updating what attacks have been loaded) Counterfit reloads commands via a `terminal.postcmd` function after every command execution. Let's take a closer look at the `interact` command, every time the module is reloaded, the `parser` executes `get_targets()`. Executing a reload after every commands triggers `get_targets()` to be called and the choices for the command to reflect the current state.

```python
def get_targets():
    return CFState.state().list_targets()

parser = Cmd2ArgumentParser()
parser.add_argument("target", choices=get_targets())
```

## Quality of Life Commands
While attacking targets is fun, an attack comes after the target has been written by the user. Because this is something of a development process, there are some convenience commands that will make life a little easier when writing new targets.

| Command | Description | 
| -- | -- | 
| new | Create a new target in the targets folder and load it into the session. |
| reload | When editing a target, this command will reload the target to reflect the changes made. |
| predict | Send a single query to the target model.|
| exit | Exit the active attack or active target.|

For example, a target creation workflow is as follows,

1. Execute `new` to create a fresh target
2. Open the new target python file in your favorite code editor. (`cmd2` haa a built in `edit` command)
3. Make changes to the target and execute `reload`. 
4. Use the `predict` command to ensure inputs and outputs are as expected.

## Informational Commands
These commands gather and present relevant information about the current session, and relevant information about targets and attacks. 

| Command | Description |
| -- | -- |
| list | This command prints loaded objects in the session |
| show | When editing a target, this command will reload the target to reflect the changes made.|
| docs | When editing a target, this command will reload the target to reflect the changes made.|

## Primary Commands
| Command | Description |
| -- | -- |
| load | This command prints loaded objects in the session |
| interact | This command prints loaded objects in the session |
| use | This command prints loaded objects in the session |
| set | This command prints loaded objects in the session |
| run | This command prints loaded objects in the session |
| scan | When editing a target, this command will reload the target to reflect the changes made.|


Basic workflow,

1. Load a framework `load art`
2. Interact with a target, `interact digits_keras`
3. Use an attack `use HopSkipJump`
4. Set 


# Options

Options are kept in `CFAttackOption` and are created during `state.build_new_attack()`.

```
┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Attack Options (type) ┃ Default    ┃ Current    ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ Algo Parameters       │            │            │
│ --------------------  │ --         │ --         │
│ targeted (bool)       │ False      │ False      │
│ norm (int)            │ 2          │ 2          │
│ max_iter (int)        │ 50         │ 50         │
│ max_eval (int)        │ 10000      │ 10000      │
│ init_eval (int)       │ 100        │ 100        │
│ init_size (int)       │ 100        │ 100        │
│ curr_iter (int)       │ 0          │ 0          │
│ batch_size (int)      │ 64         │ 64         │
│ verbose (bool)        │ False      │ False      │
│ clip_values (tuple)   │ (0.0, 1.0) │ (0.0, 1.0) │
│                       │            │            │
│ CFAttack Options      │            │            │
│ --------------------  │ --         │ --         │
│ sample_index (int)    │ 0          │ 0          │
│ logger (str)          │ default    │ default    │
└───────────────────────┴────────────┴────────────┘
```

Options provide the ability to alter attack behaviour at runtime. There are two types of options,

1. `Algo Parameters` come from the specific implementation of the attack algo,, and are loaded as `attack_default_params` when an attack is added to a framework during `framework.add_attack`. A framework author has full control over what parameters get attached to an attack.

2. `CFAttack Options` are injected during `state.build_new_attack`. There are two default options - `sample_index` and `logger`.


## Setting Options
After interacting with a target. 


# Loggers
Counterfit allows users to write and use their own loggers. Counterfit comes with some basic attack loggers, `json`, `list`, `default`. The `default` logger only counts the number of queries an attack has made to a target model. Loggers are kept in `counterfit/loggers/logger.py` and are set prior to an attack with `set --logger json`.

## Write a Logger
