# DEMO 2: Credit Card Fraud Integrity Attack Assessment
## Objective
Determine roughly how many queries are required to successfully evade `creditfraud` model with `HopSkipJump`

## Threat Model
- Attacker knowledge: API access to model
- Security violation: integrity

## Steps
1. Start the Counterfit CLI.
    ```bash
    # Start CF option 1. Using the console script.
    $ counterfit 
   
    # Start CF option 2. From the terminal.py file.
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
3. Interact with `creditfraud`
   ```
   counterfit> set_target creditfraud 
   creditfraud> 
   ```


4. List the available attacks
   ```
   creditfraud> list attacks
   ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
   ┃ Name                               ┃ Category          ┃ Type       ┃ Tags           ┃ Framework  ┃
   ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
   │ black_box_rule_based               │ inference         │ closed-box │                │ art        │
   │ boundary                           │ evasion           │ closed-box │ image, tabular │ art        │
   │ carlini                            │ evasion           │ open-box   │ image, tabular │ art        │
   │ copycat_cnn                        │ inversion         │ closed-box │ image          │ art        │
   │ deepfool                           │ evasion           │ open-box   │ image, tabular │ art        │
   │ elastic_net                        │ evasion           │ open-box   │ image, tabular │ art        │
   │ functionally_equivalent_extraction │ inversion         │ closed-box │ image, tabular │ art        │
   │ hop_skip_jump                      │ evasion           │ closed-box │ image, tabular │ art        │
   │ knockoff_nets                      │ inversion         │ closed-box │ image, tabular │ art        │
   │ label_only_boundary_distance       │ inference         │ open-box   │ image, tabular │ art        │
   │ mi_face                            │ inference         │ open-box   │ image, tabular │ art        │
   │ newtonfool                         │ evasion           │ open-box   │ image, tabular │ art        │
   │ pixel_threshold                    │ evasion           │ unknown    │ image          │ art        │
   │ projected_gradient_descent_numpy   │ evasion           │ open-box   │ image, tabular │ art        │
   │ saliency_map                       │ evasion           │ open-box   │ image, tabular │ art        │
   │ simba                              │ evasion           │ open-box   │ image          │ art        │
   │ spatial_transformation             │ evasion           │ open-box   │ image, tabular │ art        │
   │ universal_perturbation             │ evasion           │ open-box   │ image          │ art        │
   │ virtual_adversarial                │ evasion           │ open-box   │ image          │ art        │
   │ wasserstein                        │ evasion           │ open-box   │ image          │ art        │
   │ white_box_decision_tree            │ inference         │ unknown    │                │ art        │
   │ ApplyLambda                        │ common-corruption │ closed-box │ image          │ augly      │
   │ Blur                               │ common-corruption │ closed-box │ image          │ augly      │
   │ Brightness                         │ common-corruption │ closed-box │ image          │ augly      │
   │ ChangeAspectRatio                  │ common-corruption │ closed-box │ image          │ augly      │
   │ ClipImageSize                      │ common-corruption │ closed-box │ image          │ augly      │
   │ ColorJitter                        │ common-corruption │ closed-box │ image          │ augly      │
   │ Contrast                           │ common-corruption │ closed-box │ image          │ augly      │
   │ ConvertColor                       │ common-corruption │ closed-box │ image          │ augly      │
   │ Crop                               │ common-corruption │ closed-box │ image          │ augly      │
   │ EncodingQuality                    │ common-corruption │ closed-box │ image          │ augly      │
   │ Grayscale                          │ common-corruption │ closed-box │ image          │ augly      │
   │ HFlip                              │ common-corruption │ closed-box │ image          │ augly      │
   │ MemeFormat                         │ common-corruption │ closed-box │ image          │ augly      │
   │ Opacity                            │ common-corruption │ closed-box │ image          │ augly      │
   │ OverlayEmoji                       │ common-corruption │ closed-box │ image          │ augly      │
   │ OverlayOntoScreenshot              │ common-corruption │ closed-box │ image          │ augly      │
   │ OverlayStripes                     │ common-corruption │ closed-box │ image          │ augly      │
   │ OverlayText                        │ common-corruption │ closed-box │ image          │ augly      │
   │ Pad                                │ common-corruption │ closed-box │ image          │ augly      │
   │ PadSquare                          │ common-corruption │ closed-box │ image          │ augly      │
   │ PerspectiveTransform               │ common-corruption │ closed-box │ image          │ augly      │
   │ Pixelization                       │ common-corruption │ closed-box │ image          │ augly      │
   │ RandomEmojiOverlay                 │ common-corruption │ closed-box │ image          │ augly      │
   │ RandomNoise                        │ common-corruption │ closed-box │ image          │ augly      │
   │ Resize                             │ common-corruption │ closed-box │ image          │ augly      │
   │ Rotate                             │ common-corruption │ closed-box │ image          │ augly      │
   │ Saturation                         │ common-corruption │ closed-box │ image          │ augly      │
   │ Scale                              │ common-corruption │ closed-box │ image          │ augly      │
   │ Sharpen                            │ common-corruption │ closed-box │ image          │ augly      │
   │ ShufflePixels                      │ common-corruption │ closed-box │ image          │ augly      │
   │ VFlip                              │ common-corruption │ closed-box │ image          │ augly      │
   │ a2t_yoo_2021                       │ evasion           │ closed-box │ text           │ textattack │
   │ bae_garg_2019                      │ evasion           │ closed-box │ text           │ textattack │
   │ bert_attack_li_2020                │ evasion           │ closed-box │ text           │ textattack │
   │ checklist_ribeiro_2020             │ evasion           │ closed-box │ text           │ textattack │
   │ clare_li_2020                      │ evasion           │ closed-box │ text           │ textattack │
   │ deepwordbug_gao_2018               │ evasion           │ closed-box │ text           │ textattack │
   │ faster_genetic_algorithm_jia_2019  │ evasion           │ closed-box │ text           │ textattack │
   │ genetic_algorithm_alzantot_2018    │ evasion           │ closed-box │ text           │ textattack │
   │ hotflip_ebrahimi_2017              │ evasion           │ closed-box │ text           │ textattack │
   │ iga_wang_2019                      │ evasion           │ closed-box │ text           │ textattack │
   │ input_reduction_feng_2018          │ evasion           │ closed-box │ text           │ textattack │
   │ kuleshov_2017                      │ evasion           │ closed-box │ text           │ textattack │
   │ morpheus_tan_2020                  │ evasion           │ closed-box │ text           │ textattack │
   │ pruthi_2019                        │ evasion           │ closed-box │ text           │ textattack │
   │ pso_zang_2020                      │ evasion           │ closed-box │ text           │ textattack │
   │ pwws_ren_2019                      │ evasion           │ closed-box │ text           │ textattack │
   │ seq2sick_cheng_2018_blackbox       │ evasion           │ closed-box │ text           │ textattack │
   │ textbugger_li_2018                 │ evasion           │ closed-box │ text           │ textattack │
   │ textfooler_jin_2019                │ evasion           │ closed-box │ text           │ textattack │
   └────────────────────────────────────┴───────────────────┴────────────┴────────────────┴────────────┘

   ```


5. Let's try `HopSkipJump`
   ```
   set_acreditfraud> set_attack hop_skip_jump 
   [+] success:  Using be1d11b7
   
   creditfraud>HopSkipJump:be1d11b7> set_params --max_iter 5 --max_eval 1250
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
   │ max_eval (int)       │ 1000       │ 1250       │ Maximum number of evaluations for estimating gradient.                   │
   │ max_iter (int)       │ 50         │ 5          │ Maximum number of iterations.                                            │
   │ norm (int)           │ 2          │ 2          │ Order of the norm. Possible values: "inf", np.inf or 2.                  │
   │ targeted (bool)      │ False      │ False      │ Should the attack target one specific class.                             │
   │ verbose (bool)       │ True       │ True       │ Show progress bars.                                                      │
   │ target_labels (int)  │ 0          │ 0          │ target labels for a targeted attack                                      │
   │                      │            │            │                                                                          │
   │ CFAttack Options     │            │            │                                                                          │
   │ -------------------- │ --         │ --         │ --                                                                       │
   │ sample_index (int)   │ 0          │ 0          │ Sample index to attack                                                   │
   │ optimize (bool)      │ False      │ False      │ Use Optuna to optimize attack parameters                                 │
   │ logger (str)         │ basic      │ basic      │ Logger to log queries with                                               │
   └──────────────────────┴────────────┴────────────┴──────────────────────────────────────────────────────────────────────────┘
   creditfraud>HopSkipJump:be1d11b7> run
   HopSkipJump: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 21.75it/s]
   [+] success:  Attack completed be1d11b7 
   ```

6. Let's see the attack
   ```
   creditfraud>HopSkipJump:be1d11b7> show results
   ┏━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
   ┃ Attack id ┃ Target Name ┃ Attack Name    ┃ Status   ┃ Success           ┃
   ┡━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
   │ *be1d11b7 │ creditfraud │ HopSkipJump    │ complete │ {'default': True} │
   └───────────┴─────────────┴────────────────┴──────────┴───────────────────┘
   ```


7. Show results
   ```
    creditfraud>HopSkipJump:be1d11b7> show results
   ┏━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃ Success ┃ Elapsed time ┃ Total Queries             ┃
   ┡━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
   │ 1/1     │ 0.6          │ 24552 (42461.7 query/sec) │
   └─────────┴──────────────┴───────────────────────────┘
   ┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
   ┃           ┃ Input     ┃ Adversar… ┃           ┃                                                                                                                ┃         ┃
   ┃ Sample    ┃ Label     ┃ Label     ┃ % Eucl.   ┃                                                                                                                ┃         ┃
   ┃ Index     ┃ (conf)    ┃ (conf)    ┃ dist.     ┃ Adversarial Input                                                                                              ┃ success ┃
   ┡━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
   │ 0         │ fraud     │ benign    │ 0.0       │ [4462.00 -2.30 1.76 -0.36 2.33 -0.82 -0.08 0.56 -0.40 -0.24 -1.53 2.03  -6.56 0.17 -1.47 -0.70 -2.28 -4.78     │ True    │
   │           │ (1.0000)  │ (1.0000)  │           │ -2.62 -1.33 -0.43 -0.30 -0.93 0.17  -0.09 -0.15 -0.54 0.04 -0.15 239.93]                                       │         │
   └───────────┴───────────┴───────────┴───────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴─────────┘
   ```

## (Optional) Self Assessment
1. How many samples are included in the `creditfraud` target?  (Hint: you can discover this via `list targets`)
2. What is the `sample_index` that was used during this tutorial?  (Hint: you did not set it explicitly.)
3. Optimize the attack for Hop Skip Jump (HSJ). Try adjusting parameters such that you have a "1/1 Success", but in few "Total Queries".  For `HopSkipJump`, you might play with `max_iter`,  `max_eval` and `init_size`.

[[Demo Home]](./README.MD)

