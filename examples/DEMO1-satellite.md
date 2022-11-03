**# DEMO 1: Satellite Images Red Team Operation
[[Demo Home]](../demo/README.md)

## Objective
Change the label of a satellite image (true label: `stadium`) into `airplane`.

## Threat Model
- Attacker knowledge: API access to model
- Security violation: integrity

## Steps

1. Start the Counterfit CLI.
    ```
    $ python examples/terminal/terminal.py 
   
                              __            _____ __
      _________  __  ______  / /____  _____/ __(_) /_
     / ___/ __ \/ / / / __ \/ __/ _ \/ ___/ /_/ / __/
    / /__/ /_/ / /_/ / / / / /_/  __/ /  / __/ / /
    \___/\____/\__,_/_/ /_/\__/\___/_/  /_/ /_/\__/

                    Version: 1.1.0
    ```

2. What models are defined in our environment?
    ```
    counterfit> list targets 
   ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃ Name                ┃ Model Type ┃ Data Type ┃ Input Shape   ┃ # Samples ┃ Endpoint                                             ┃
   ┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
   │ cart_pole           │ closed-box │ tabular   │ (1080000,)    │ 0         │ cartpole_dqn_10000.pt.gz                             │
   │ cart_pole_initstate │ closed-box │ tabular   │ (4,)          │ 0         │ cartpole_dqn_10000.pt.gz                             │
   │ creditfraud         │ closed-box │ tabular   │ (30,)         │ 0         │ creditfraud/creditfraud_sklearn_pipeline.pkl         │
   │ digits_keras        │ closed-box │ image     │ (28, 28, 1)   │ 0         │ digits_keras/mnist_model.h5                          │
   │ digits_mlp          │ closed-box │ image     │ (1, 28, 28)   │ 0         │ digits_mlp/mnist_sklearn_pipeline.pkl                │
   │ movie_reviews       │ closed-box │ text      │ (1,)          │ 0         │ movie_reviews/movie_reviews_sentiment_analysis.pt    │
   │ satellite           │ closed-box │ image     │ (3, 256, 256) │ 0         │ satellite/satellite-image-params-airplane-stadium.h5 │
   └─────────────────────┴────────────┴───────────┴───────────────┴───────────┴──────────────────────────────────────────────────────┘
    ```

3. Interact with the `satellite` target
    ```
    counterfit> set_target satellite
    ```


4. For this target, we'll want to use an attack that requires only API access, and works on image data (see `Tags` column).  Let's use `HopSkipJump`.  (Hint: This creates a new attack, which can be referenced by an id, view them all with `show attacks`, and use a different attack using `use <attack_id>`.)
    ```
    satellite> set_attack hop_skip_jump 
    [+] success:  Using fb58020f
    ```


5. Show information about the attack
    ```
    satellite>HopSkipJump:fb58020f> show info
    ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Attack Field ┃ Description                                                                                                                                               ┃
    ┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ Name         │ hop_skip_jump                                                                                                                                             │
    │ Type         │ closed-box                                                                                                                                                │
    │ Category     │ evasion                                                                                                                                                   │
    │ Tags         │ image, tabular                                                                                                                                            │
    │ Framework    │ art                                                                                                                                                       │
    │ Docs         │ Implementation of the HopSkipJump attack from Jianbo et al. (2019). This is a powerful closed-box attack that only requires final class prediction, and is │
    │              │ an advanced version of the boundary attack. | Paper link: https://arxiv.org/abs/1904.02144                                                                │
    └──────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```


6. What does the model think about the images for sample indices 0 through 9? (Hint: we can use Python notation to select multiple indices).
    ```
    satellite>HopSkipJump:fb58020f> predict -i range(10)
    ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
    ┃ Sample Index ┃ Sample                                                                     ┃ Label    ┃ Output Scores ┃
    ┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
    │ 0            │ counterfit/targets/results/predict/initial-satellite-88d36524-sample-0.png │ airplane │ [0.69 0.31]   │
    │ 1            │ counterfit/targets/results/predict/initial-satellite-f8098e1e-sample-1.png │ airplane │ [0.70 0.30]   │
    │ 2            │ counterfit/targets/results/predict/initial-satellite-41a3629a-sample-2.png │ airplane │ [0.70 0.30]   │
    │ 3            │ counterfit/targets/results/predict/initial-satellite-3e2c9e8e-sample-3.png │ airplane │ [0.70 0.30]   │
    │ 4            │ counterfit/targets/results/predict/initial-satellite-676c8854-sample-4.png │ airplane │ [0.70 0.30]   │
    │ 5            │ counterfit/targets/results/predict/initial-satellite-a85e763e-sample-5.png │ stadium  │ [0.30 0.70]   │
    │ 6            │ counterfit/targets/results/predict/initial-satellite-4db8aae7-sample-6.png │ stadium  │ [0.30 0.70]   │
    │ 7            │ counterfit/targets/results/predict/initial-satellite-34ce22ce-sample-7.png │ stadium  │ [0.30 0.70]   │
    │ 8            │ counterfit/targets/results/predict/initial-satellite-5399ac10-sample-8.png │ stadium  │ [0.30 0.70]   │
    │ 9            │ counterfit/targets/results/predict/initial-satellite-d5018c03-sample-9.png │ stadium  │ [0.30 0.70]   │
    └──────────────┴────────────────────────────────────────────────────────────────────────────┴──────────┴───────────────┘
    ```


7. Set parameters for the attack.  (Hint: to see what options are available to set, type `show options` or `set`.)  We'll use sample index 5 that corresponds to an image of a stadium.
    ```
    satellite>HopSkipJump:fb58020f> set_params --sample_index 5 --norm 2 --max_iter 10 --max_eval 5000 --verbose true
    ┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Parameter (type)     ┃ Default    ┃ Current    ┃ New                                                                      ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ Algo Parameters      │            │            │                                                                          │
    │ -------------------- │ --         │ --         │ --                                                                       │
    │ batch_size (int)     │ 64         │ 64         │ The size of the batch used by the estimator during inference.            │
    │ clip_values (list)   │ [0.0, 1.0] │ (0.0, 1.0) │ Refer to attack file.                                                    │
    │ curr_iter (int)      │ 0          │ 0          │ Refer to attack file.                                                    │
    │ init_eval (int)      │ 100        │ 100        │ Initial number of evaluations for estimating gradient.                   │
    │ init_size (int)      │ 100        │ 100        │ Maximum number of trials for initial generation of adversarial examples. │
    │ max_eval (int)       │ 1000       │ 5000       │ Maximum number of evaluations for estimating gradient.                   │
    │ max_iter (int)       │ 50         │ 10         │ Maximum number of iterations.                                            │
    │ norm (int)           │ 2          │ 2          │ Order of the norm. Possible values: "inf", np.inf or 2.                  │
    │ targeted (bool)      │ False      │ False      │ Should the attack target one specific class.                             │
    │ verbose (bool)       │ True       │ True       │ Show progress bars.                                                      │
    │ target_labels (int)  │ 0          │ 0          │ target labels for a targeted attack                                      │
    │                      │            │            │                                                                          │
    │ CFAttack Options     │            │            │                                                                          │
    │ -------------------- │ --         │ --         │ --                                                                       │
    │ sample_index (int)   │ 0          │ 5          │ Sample index to attack                                                   │
    │ optimize (bool)      │ False      │ False      │ Use Optuna to optimize attack parameters                                 │
    │ logger (str)         │ basic      │ basic      │ Logger to log queries with                                               │
    └──────────────────────┴────────────┴────────────┴──────────────────────────────────────────────────────────────────────────┘
    ```


8. Execute the attack.  This may take several minutes.
    ```
    satellite>HopSkipJump:fb58020f> run
    HopSkipJump:   0%|   
    HopSkipJump: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:54<00:00, 54.52s/it]
    [+] success:  Attack completed fb58020f
    ```
  Hint: if your attack is unsuccessful (e.g., `Failed to draw a random image that is adversarial`) try changing the algorithm parameters (e.g., `set --init_eval 400`).

11. Let's show the "before" and "after" pictures.  If you've done a `predict -i 5`, then "before" picture is in the folder `counterfit/targets/satellite/results/predict/initial-satellite-fb58020f-sample-5.png`.  The "after" picture is in `counterfit/targets/satellite/results/[attack_id]/initial-satellite-fb58020f-sample-5.png`. (Hint: In the JupyterLab demo environment, you cause JupyterLab file navigator ot view these.)


12. Learn more!
    ```
    help
    ```

## (Optional) Self Assessment
1. What minimum level of model access was required for this model?
2. How many queries were required to (a) change the decision of the ML model and (b) still remain convincing to a human?
3. For HopSkipJump, change `norm`, `max_iter` and `max_eval` parameters to tune the results of the algorithm.  Are there tradeoffs between the resulting quality of the adversarial example and number of queries required to create it?

[[Demo Home]](../demo/README.md)**
