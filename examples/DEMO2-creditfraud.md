# DEMO 2: Credit Card Fraud Integrity Attack Assessment
[[Demo Home]](../demo/README.md)
## Objective
Determine roughly how many queries are required to successfully evade `creditfraud` model with `HopSkipJump`

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
    ┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Name            ┃ Model Type ┃ Data Type ┃ Input Shape   ┃ # Samples ┃ Endpoint                                             ┃
    ┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ creditfraud     │ blackbox   │ tabular   │ (30,)         │ 0         │ creditfraud/creditfraud_sklearn_pipeline.pkl         │
    │ digits_blackbox │ blackbox   │ image     │ (1, 28, 28)   │ 0         │ digits_blackbox/mnist_sklearn_pipeline.pkl           │
    │ digits_keras    │ keras      │ image     │ (28, 28, 1)   │ 0         │ digits_keras/mnist_model.h5                          │
    │ movie_reviews   │ blackbox   │ text      │ (1,)          │ 0         │ movie_reviews/movie_reviews_sentiment_analysis.pt    │
    │ satellite       │ blackbox   │ image     │ (3, 256, 256) │ 0         │ satellite/satellite-image-params-airplane-stadium.h5 │
    └─────────────────┴────────────┴───────────┴───────────────┴───────────┴──────────────────────────────────────────────────────┘
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
   │ ApplyLambda                        │ common-corruption │ blackbox   │ image          │ augly      │
   │ Blur                               │ common-corruption │ blackbox   │ image          │ augly      │
   │ Brightness                         │ common-corruption │ blackbox   │ image          │ augly      │
   │ ChangeAspectRatio                  │ common-corruption │ blackbox   │ image          │ augly      │
   │ ClipImageSize                      │ common-corruption │ blackbox   │ image          │ augly      │
   │ ColorJitter                        │ common-corruption │ blackbox   │ image          │ augly      │
   │ Contrast                           │ common-corruption │ blackbox   │ image          │ augly      │
   │ ConvertColor                       │ common-corruption │ blackbox   │ image          │ augly      │
   │ Crop                               │ common-corruption │ blackbox   │ image          │ augly      │
   │ EncodingQuality                    │ common-corruption │ blackbox   │ image          │ augly      │
   │ Grayscale                          │ common-corruption │ blackbox   │ image          │ augly      │
   │ HFlip                              │ common-corruption │ blackbox   │ image          │ augly      │
   │ MemeFormat                         │ common-corruption │ blackbox   │ image          │ augly      │
   │ Opacity                            │ common-corruption │ blackbox   │ image          │ augly      │
   │ OverlayEmoji                       │ common-corruption │ blackbox   │ image          │ augly      │
   │ OverlayOntoScreenshot              │ common-corruption │ blackbox   │ image          │ augly      │
   │ OverlayStripes                     │ common-corruption │ blackbox   │ image          │ augly      │
   │ OverlayText                        │ common-corruption │ blackbox   │ image          │ augly      │
   │ Pad                                │ common-corruption │ blackbox   │ image          │ augly      │
   │ PadSquare                          │ common-corruption │ blackbox   │ image          │ augly      │
   │ PerspectiveTransform               │ common-corruption │ blackbox   │ image          │ augly      │
   │ Pixelization                       │ common-corruption │ blackbox   │ image          │ augly      │
   │ RandomEmojiOverlay                 │ common-corruption │ blackbox   │ image          │ augly      │
   │ RandomNoise                        │ common-corruption │ blackbox   │ image          │ augly      │
   │ Resize                             │ common-corruption │ blackbox   │ image          │ augly      │
   │ Rotate                             │ common-corruption │ blackbox   │ image          │ augly      │
   │ Saturation                         │ common-corruption │ blackbox   │ image          │ augly      │
   │ Scale                              │ common-corruption │ blackbox   │ image          │ augly      │
   │ Sharpen                            │ common-corruption │ blackbox   │ image          │ augly      │
   │ ShufflePixels                      │ common-corruption │ blackbox   │ image          │ augly      │
   │ VFlip                              │ common-corruption │ blackbox   │ image          │ augly      │
   │ a2t_yoo_2021                       │ evasion           │ blackbox   │ text           │ textattack │
   │ bae_garg_2019                      │ evasion           │ blackbox   │ text           │ textattack │
   │ bert_attack_li_2020                │ evasion           │ blackbox   │ text           │ textattack │
   │ checklist_ribeiro_2020             │ evasion           │ blackbox   │ text           │ textattack │
   │ clare_li_2020                      │ evasion           │ blackbox   │ text           │ textattack │
   │ deepwordbug_gao_2018               │ evasion           │ blackbox   │ text           │ textattack │
   │ faster_genetic_algorithm_jia_2019  │ evasion           │ blackbox   │ text           │ textattack │
   │ genetic_algorithm_alzantot_2018    │ evasion           │ blackbox   │ text           │ textattack │
   │ hotflip_ebrahimi_2017              │ evasion           │ blackbox   │ text           │ textattack │
   │ iga_wang_2019                      │ evasion           │ blackbox   │ text           │ textattack │
   │ input_reduction_feng_2018          │ evasion           │ blackbox   │ text           │ textattack │
   │ kuleshov_2017                      │ evasion           │ blackbox   │ text           │ textattack │
   │ morpheus_tan_2020                  │ evasion           │ blackbox   │ text           │ textattack │
   │ pruthi_2019                        │ evasion           │ blackbox   │ text           │ textattack │
   │ pso_zang_2020                      │ evasion           │ blackbox   │ text           │ textattack │
   │ pwws_ren_2019                      │ evasion           │ blackbox   │ text           │ textattack │
   │ seq2sick_cheng_2018_blackbox       │ evasion           │ blackbox   │ text           │ textattack │
   │ textbugger_li_2018                 │ evasion           │ blackbox   │ text           │ textattack │
   │ textfooler_jin_2019                │ evasion           │ blackbox   │ text           │ textattack │
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
   show attacks
   ┏━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
   ┃ Attack id ┃ Target Name ┃ Attack Name    ┃ Status   ┃ Success           ┃
   ┡━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
   │ *be1d11b7 │ creditfraud │ HopSkipJump    │ complete │ {'default': True} │
   └───────────┴─────────────┴────────────────┴──────────┴───────────────────┘
   ```


## (Optional) Self Assessment
1. How many samples are included in the `creditfraud` target?  (Hint: you can discover this via `list targets`)
2. What is the `sample_index` that was used during this tutorial?  (Hint: you did not set it explicitly.)
3. Optimize the attack for Hop Skip Jump (HSJ). Try adjusting parameters such that you have a "1/1 Success", but in few "Total Queries".  For `HopSkipJump`, you might play with `max_iter`,  `max_eval` and `init_size`.

[[Demo Home]](../demo/README.md)
