# Basic Use
After starting Counterfit you will be greeted with a simple interface,

```
[sarah@contoso.com] -> python .\counterfit.py

                              __            _____ __
      _________  __  ______  / /____  _____/ __(_) /_
     / ___/ __ \/ / / / __ \/ __/ _ \/ ___/ /_/ / __/
    / /__/ /_/ / /_/ / / / / /_/  __/ /  / __/ / /
    \___/\____/\__,_/_/ /_/\__/\___/_/  /_/ /_/\__/

                    Version: 1.0.0
```

To view the available targets execute the `list targets` command. Targets are user created classes that represent a prediction endpoint, they can be local or remote. See Targets for more information.
```

counterfit> list targets

┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Name            ┃ Model Type ┃ Data Type ┃ Input Shape   ┃ # Samples    ┃ Endpoint                                   ┃ Loaded ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ creditfraud     │ BlackBox   │ tabular   │ (30,)         │ (not loaded) │ creditfraud_sklearn_pipeline.pkl           │ False  │
│ digits_blackbox │ BlackBox   │ image     │ (1, 28, 28)   │ (not loaded) │ mnist_sklearn_pipeline.pkl                 │ False  │
│ digits_keras    │ keras      │ image     │ (28, 28, 1)   │ (not loaded) │ mnist_model.h5                             │ False  │
│ movie_reviews   │ BlackBox   │ text      │ (1,)          │ (not loaded) │ movie_reviews_sentiment_analysis.pt        │ False  │
│ satellite       │ BlackBox   │ image     │ (3, 256, 256) │ (not loaded) │ satellite-image-params-airplane-stadium.h5 │ False  │
└─────────────────┴────────────┴───────────┴───────────────┴──────────────┴────────────────────────────────────────────┴────────┘
counterfit>

```

To interact with a target, use the `interact` command followed by a target name. The terminal prompt will change to reflect the active target.

```
counterfit> interact creditfraud

[+] creditfraud (d7aefbf1) successfully loaded!

creditfraud>
```

Next, load a framework. To view the available frameworks execute `list frameworks`. The name of the framework and the number of attack available will be displayed. If the number of attacks is 0, no attacks have been loaded. (This can be helpful in debugging loading custom frameworks)
```
counterfit> list frameworks

┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Framework  ┃ # Attacks    ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ art        │ (not loaded) │
│ augly      │ (not loaded) │
│ textattack │ (not loaded) │
└────────────┴──────────────┘

counterfit>
```

Load a framework and its attacks into the session with `load`. 

```
counterfit> load art

[+] art successfully loaded with defaults (no config file provided)

counterfit>
```

After a framework is loaded successfully, the attacks under that framework become available for use. Executing `list attacks` before loading a framework will result in a warning. 

```
counterfit> list attacks

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Name                             ┃ Category ┃ Type             ┃ Tags           ┃ Framework ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ BoundaryAttack                   │ BlackBox │ EvasionAttack    │ image, tabular │ art       │
│ CarliniL0Method                  │ WhiteBox │ EvasionAttack    │ image, tabular │ art       │
│ CarliniLInfMethod                │ WhiteBox │ EvasionAttack    │ image, tabular │ art       │
│ CopycatCNN                       │ BlackBox │ ExtractionAttack │ image          │ art       │
│ DeepFool                         │ WhiteBox │ EvasionAttack    │ image, tabular │ art       │
│ ElasticNet                       │ WhiteBox │ EvasionAttack    │ image, tabular │ art       │
│ FunctionallyEquivalentExtraction │ BlackBox │ ExtractionAttack │ image, tabular │ art       │
│ HopSkipJump                      │ BlackBox │ EvasionAttack    │ image, tabular │ art       │
│ KnockoffNets                     │ BlackBox │ ExtractionAttack │ image, tabular │ art       │
│ LabelOnlyDecisionBoundary        │ WhiteBox │ InferenceAttack  │ image, tabular │ art       │
│ MIFace                           │ WhiteBox │ InferenceAttack  │ image, tabular │ art       │
│ NewtonFool                       │ WhiteBox │ EvasionAttack    │ image, tabular │ art       │
│ ProjectedGradientDescentCommon   │ WhiteBox │ EvasionAttack    │ image, tabular │ art       │
│ SaliencyMapMethod                │ WhiteBox │ EvasionAttack    │ image, tabular │ art       │
│ SimBA                            │ WhiteBox │ EvasionAttack    │ image          │ art       │
│ SpatialTransformation            │ WhiteBox │ EvasionAttack    │ image, tabular │ art       │
│ UniversalPerturbation            │ WhiteBox │ EvasionAttack    │ image          │ art       │
│ VirtualAdversarialMethod         │ WhiteBox │ EvasionAttack    │ image          │ art       │
│ Wasserstein                      │ WhiteBox │ EvasionAttack    │ image          │ art       │
└──────────────────────────────────┴──────────┴──────────────────┴────────────────┴───────────┘
```

From an active target there are two ways to run an attack, and there are some key differences to be aware of.

1. Using the `scan` command.

scan is for automation; it has various arguments that control how many iterations of which attacks to execute against a target. scan by default uses random samples and random parameters. The scan function is useful for baselining and testing a target model. After completing all attacks, a scan summary will be printed. For example, when interacting with a target execute the following command `scan --iterations 10 --attack hop_skip_jump`

2. Using the `run` command.

`run` on the other hand requires that you add an attack via `use`. After successfully executing the use command, the terminal prompt will change to reflect the active attack. With `run` you get control over each parameter and can set them individually. 

```
creditfraud> use HopSkipJump

[+] New HopSkipJump (aad67043) created
[+] Using aad67043

creditfraud> 
```

To view the possible parameters to change, execute the `show options`. To change one or more parameters, execute the `set` command with the parameter you want to change as the argument followed by the value. Learn more about options.

```
creditfraud>aad67043> show options

┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Attack Options (type) ┃ Default    ┃ Current    ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ Algo Parameters       │            │            │
│ --------------------  │ --         │ --         │
│ targeted (bool)       │ False      │ False      │
│ norm (int)            │ 2          │ 2          │
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

After an option has been updated the terminal will print the updated parameters, including the default parameters. During manual testing it can be helpful to know where a particular value started.

```
creditfraud>aad67043> set --max_iter=10

┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━┓
┃ Algo Parameter (type) ┃ Default    ┃ Current    ┃ New ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━┩
│ Algo Parameters       │            │            │     │
│ --------------------  │ --         │ --         │ --  │
│ targeted (bool)       │ False      │ False      │     │
│ norm (int)            │ 2          │ 2          │     │
│ max_iter (int)        │ 50         │ 50         │ 10  │
│ max_eval (int)        │ 10000      │ 10000      │     │
│ init_eval (int)       │ 100        │ 100        │     │
│ init_size (int)       │ 100        │ 100        │     │
│ curr_iter (int)       │ 0          │ 0          │     │
│ batch_size (int)      │ 64         │ 64         │     │
│ verbose (bool)        │ False      │ False      │     │
│ clip_values (tuple)   │ (0.0, 1.0) │ (0.0, 1.0) │     │
│                       │            │            │     │
│ CFAttack Options      │            │            │     │
│ --------------------  │ --         │ --         │ --  │
│ sample_index (int)    │ 0          │ 0          │     │
│ logger (str)          │ default    │ default    │     │
└───────────────────────┴────────────┴────────────┴─────┘

creditfraud>aad67043>
```

Finally, it's time to `run` the attack.

```
creditfraud>aad67043> run

[-] Running attack HopSkipJump with id aad67043 on creditfraud)
[-] Preparing attack...
[-] Running attack...

┏━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Success ┃ Elapsed time ┃ Total Queries            ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1/1     │ 0.2          │ 2390 (12119.0 query/sec) │
└─────────┴──────────────┴──────────────────────────┘
┏━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Sample   ┃ Input   ┃ Adversa… ┃ % Eucl. ┃ Adversarial Input                                                                                    ┃ success ┃
┃ Index    ┃ Label   ┃ Label    ┃ dist.   ┃                                                                                                      ┃         ┃
┃          ┃ (conf)  ┃ (conf)   ┃         ┃                                                                                                      ┃         ┃
┡━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
│ 0        │ fraud   │ benign   │ 0.0     │ [4462.00 -2.30 1.76 -0.36 2.33 -0.82 -0.07 0.56 -0.39 -0.23 -1.53 2.03  -6.56 0.02 -1.47 -0.70 -2.27 │ True    │
│          │ (1.000… │ (1.0000) │         │ -4.79 -2.48 -1.33 -0.44 -0.29 -0.93 0.17  -0.08 -0.15 -0.54 0.04 -0.15 239.93]                       │         │
└──────────┴─────────┴──────────┴─────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────┴─────────┘

[+] Attack completed aad67043 (HopSkipJump)

creditfraud>aad67043>
```

The attack will either complete and print a summary, or complete with an error. Use `save` to write the results or parameters for an attack to disk for later. 

```
creditfraud>aad67043> save --parameters

[+] Successfully wrote counterfit/targets/creditfraud/results/45174834/params.json
[+] Successfully wrote counterfit/targets/creditfraud/results/45174834/run_summary.json

creditfraud>aad67043>
```


# Advanced Use
There is a flow to Counterfit, both in creating targets and in executing attacks. Here we will cover some advanced use cases and show how flexible it can be. You will come to learn that Counterfit does not care how you get traffic back and forth - it only cares outputs are returned to the backend framework in the correct way. 

## Hiding Malicious Queries
Malicious queries look malicious. On some platforms, the predicted image is presented to the ML engineer in a dashboard. If suddenly, the platform starts to receive queries that look like television static, it will set off some alarms. To hide malicious queries, create a function inside `MyTarget` that sends normal traffic to the endpoint and use it in the `__call__` function. The example below shows that for every query the attack algorithm makes, a random number of normal queries will be sent. This ups your traffic but depending on the situation it could be worth it.

```python
import random
       ...
    
    def normal_traffic(num_queries):
        for num in range(num_queries):
            random_sample = random.choice(self.X)
            request.post(self.model_endpoint, data=normal_data)
        return 

    def __call__(self, x):
        sample = x[0].tolist()
        
        num_benign_queries = random.randrange(1,25))
        self.normal_traffic(num_benign_queries)
        
        response = requests.post(self.endpoint, data={"input": sample})

        results = response.json()
        cat_proba = results["confidence"]
        not_a_cat_proba = 1-cat_proba
        
        return [cat_proba, not_a_cat_proba]
    ...
 ```

## Using a Proxy
Most penetration testing tools can create proxies that allow arbitrary traffic to be passed into an internal network. Counterfit does not require any special configuration for this use case. Simply configure the proxy and point the model_endpoint to the target or proxy - just as you would for RDP or SSH. For example, using the requests library with a socks proxy.  

### Python Requests
Setup any proxy you like, then use requests to send traffic to the target.

```python
from counterfit.core.interfaces import AbstractTarget

class MyTarget(AbstractTarget):
    ...
    endpoint = "https://10.10.2.11/predict"
    ...

    def request_proxy_session():
        session = requests.session()
        session.proxies = {
                            'http':  'socks5://10.10.1.3:9050',
                            'https': 'socks5://10.10.1.3:9051'
                          }
        return session

    def __call__(self, x):
        sample = x[0].tolist()
        session = request_proxy_session()
        response = session.post(self.model_endpoint, data=sample)
        ...
``` 

## Sending Inputs and Collecting Outputs from a Different Location
Write a function to send a query, then write a function to collect the output. Sometimes APIs will provide a redirect or separate URI to collect the results from. The below is a fairly simple example, but we have used this technique to collect from a number of obscure places. 


```python

import requests
    ...

    def send_query(query_data):
        response = requests.post(self.model_endpoint, data=query_data)
        return response

    def collect_result(collection_endpoint):
        response = requests.get(collection_endpoint)
        return response

    def __call__(self, x):
        sample = x[0].tolist()
        
        response = send_query(sample)
        collection_endpoint = response.tojson()['location']

        result = collect_result(collection_endpoint)
        
        final_result = result.json()
        cat_proba = results["confidence"]
        not_a_cat_proba = 1-cat_proba
        
        return [cat_proba, not_a_cat_proba]

    ...
```

## Adding Startup Commands
At some point you may want to load all frameworks or perform some checks on start. Counterfit uses cmd2 to load a startup script for this exact reason. Create a .counterfit file at the root of the project, Counterfit will execute these commands on start.

```
load art
load textattack
```

## Overriding Functions in the Parent Target Class
You can technically override any of the functions in the parent target class – and you should be careful to not override functions unnecessarily. However, `outputs_to_labels` is one function that could be comfortably overridden for certain scenarios.  

A primary reason to override `outputs_to_labels` is to incorporate any knowledge you have about the decision threshold for a target model.  By default, `outputs_to_labels` in the parent class reports the class with highest confidence as the model output.  For two classes, that corresponds to an implicit threshold of 0.5, for three classes it corresponds to an implicit threshold of 0.3333, etc.

As an example, suppose you learn through you investigations that a fraud classifier reports `fraudulent` only when confidence score exceeds 0.9.  In this case, you could override `outputs_to_labels` as follows:

```python
def outputs_to_labels(self, output, threshold=0.9):
  output = np.atleast_2d(output)
  return ['fraudulent' if score[0] > threshold else 'benign' for score in output]
```

## Training A Local Model to Attack
Counterfit does not include any of the training functionality from the frameworks that are normally used for whitebox attacks. However, it is still possible to train a model inline and then attack the newly trained model. Put the training code inside the `__init__` function. Beware that the target will fail to load if the `__init__` function fails. Errors should be handled gracefully so that the `reload` command will continue to work.

```python 

def __init__(self):
  ...
  self.model = self.train_model(self.X, self.y)

def train_model(self, X, y):
  ...
  model.fit(X, y)
  ...
  return model

def __call__(self, x):
  results = self.model.predict(x)
  return results

```
