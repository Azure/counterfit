# DEMO 4: Open-box attack of an on-disk
[[Demo Home]](../demo/README.md)
## Objective
Compare open-box and API attacks to digits model

## Threat Model
- Attacker knowledge: full access to model
- Security violation: integrity

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


2. List available targets
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



3. Set target to `digits_keras`
   ```
   counterfit> set_target digits_keras
   digits_keras >
   ```

4. Look at a few digits
   ```
   digits_keras> predict -i range(20)
   ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃ Sample Index ┃ Sample                                                                         ┃ Label ┃ Output Scores                                       ┃
   ┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
   │ 0            │ counterfit/targets/results/predict/initial-digits_keras-9f36eaaf-sample-0.png  │ 7     │ [0.00 0.00 0.00 0.00 0.00 0.00 0.00 1.00 0.00 0.00] │
   │ 1            │ counterfit/targets/results/predict/initial-digits_keras-ad83a49a-sample-1.png  │ 2     │ [0.00 0.00 1.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00] │
   │ 2            │ counterfit/targets/results/predict/initial-digits_keras-6bcd8e04-sample-2.png  │ 1     │ [0.00 1.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00] │
   │ 3            │ counterfit/targets/results/predict/initial-digits_keras-24d7847f-sample-3.png  │ 0     │ [1.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00] │
   │ 4            │ counterfit/targets/results/predict/initial-digits_keras-f448ff9b-sample-4.png  │ 4     │ [0.00 0.00 0.00 0.00 1.00 0.00 0.00 0.00 0.00 0.00] │
   │ 5            │ counterfit/targets/results/predict/initial-digits_keras-2ebd981d-sample-5.png  │ 1     │ [0.00 1.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00] │
   │ 6            │ counterfit/targets/results/predict/initial-digits_keras-85cbe7cc-sample-6.png  │ 4     │ [0.00 0.00 0.00 0.00 1.00 0.00 0.00 0.00 0.00 0.00] │
   │ 7            │ counterfit/targets/results/predict/initial-digits_keras-98083198-sample-7.png  │ 9     │ [0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.01 0.99] │
   │ 8            │ counterfit/targets/results/predict/initial-digits_keras-26cc450b-sample-8.png  │ 5     │ [0.00 0.00 0.00 0.00 0.00 0.99 0.01 0.00 0.01 0.00] │
   │ 9            │ counterfit/targets/results/predict/initial-digits_keras-c110a792-sample-9.png  │ 9     │ [0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 1.00] │
   │ 10           │ counterfit/targets/results/predict/initial-digits_keras-622ce265-sample-10.png │ 0     │ [1.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00] │
   │ 11           │ counterfit/targets/results/predict/initial-digits_keras-4eb4ec8a-sample-11.png │ 6     │ [0.00 0.00 0.00 0.00 0.00 0.00 1.00 0.00 0.00 0.00] │
   │ 12           │ counterfit/targets/results/predict/initial-digits_keras-7d12346c-sample-12.png │ 9     │ [0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 1.00] │
   │ 13           │ counterfit/targets/results/predict/initial-digits_keras-2ea472b7-sample-13.png │ 0     │ [1.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00] │
   │ 14           │ counterfit/targets/results/predict/initial-digits_keras-d92dcd05-sample-14.png │ 1     │ [0.00 1.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00] │
   │ 15           │ counterfit/targets/results/predict/initial-digits_keras-3247df60-sample-15.png │ 5     │ [0.00 0.00 0.00 0.00 0.00 1.00 0.00 0.00 0.00 0.00] │
   │ 16           │ counterfit/targets/results/predict/initial-digits_keras-ae370179-sample-16.png │ 9     │ [0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 1.00] │
   │ 17           │ counterfit/targets/results/predict/initial-digits_keras-f506fbf1-sample-17.png │ 7     │ [0.00 0.00 0.00 0.00 0.00 0.00 0.00 1.00 0.00 0.00] │
   │ 18           │ counterfit/targets/results/predict/initial-digits_keras-a3379743-sample-18.png │ 5     │ [0.00 0.00 0.00 0.33 0.00 0.66 0.00 0.00 0.00 0.00] │
   │ 19           │ counterfit/targets/results/predict/initial-digits_keras-a4168afa-sample-19.png │ 4     │ [0.00 0.00 0.00 0.00 1.00 0.00 0.00 0.00 0.00 0.00] │
   └──────────────┴────────────────────────────────────────────────────────────────────────────────┴───────┴─────────────────────────────────────────────────────┘
   ```


5. List possible attacks
   ```
   digits_keras> list attacks

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



8. Use `hop_skip_jump` with changed parameters.
   ```
   digits_keras>> set_attack hop_skip_jump 
   [+] success:  Using 0abbe6ef
   
   digits_keras>HopSkipJump:0abbe6ef> set_params --sample_index 18 --max_eval 1250 --max_iter 5 --norm inf
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
   │ norm (int)           │ 2          │ inf        │ Order of the norm. Possible values: "inf", np.inf or 2.                  │
   │ targeted (bool)      │ False      │ False      │ Should the attack target one specific class.                             │
   │ verbose (bool)       │ True       │ True       │ Show progress bars.                                                      │
   │ target_labels (int)  │ 0          │ 0          │ target labels for a targeted attack                                      │
   │                      │            │            │                                                                          │
   │ CFAttack Options     │            │            │                                                                          │
   │ -------------------- │ --         │ --         │ --                                                                       │
   │ sample_index (int)   │ 0          │ 18         │ Sample index to attack                                                   │
   │ optimize (bool)      │ False      │ False      │ Use Optuna to optimize attack parameters                                 │
   │ logger (str)         │ basic      │ basic      │ Logger to log queries with                                               │
   └──────────────────────┴────────────┴────────────┴──────────────────────────────────────────────────────────────────────────┘
   ```
   
9. Run the attack
   ```
   digits_keras>HopSkipJump:0abbe6ef> run
   HopSkipJump: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  2.53it/s]
   [+] success:  Attack completed 0abbe6ef
   ```

10. Show results

   ```
   digits_keras>HopSkipJump:0abbe6ef> show results
   [-] info: Image has been saved in the location ./results/0abbe6ef/digits_keras-bcae6586.png
   ┏━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃ Success ┃ Elapsed time ┃ Total Queries            ┃
   ┡━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
   │ 1/1     │ 5.7          │ 24552 (4299.6 query/sec) │
   └─────────┴──────────────┴──────────────────────────┘
   ┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
   ┃           ┃ Input     ┃ Adversar… ┃           ┃                                                                                                                ┃         ┃
   ┃ Sample    ┃ Label     ┃ Label     ┃ Max Abs   ┃                                                                                                                ┃         ┃
   ┃ Index     ┃ (conf)    ┃ (conf)    ┃ Chg.      ┃ Adversarial Input                                                                                              ┃ Success ┃
   ┡━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
   │ 0         │ 7         │ 0         │ 0.2565    │ ./results/0abbe6ef/digits_keras-bcae6586.png                                                                   │ [ True] │
   │           │ (1.0000)  │ (0.6614)  │           │                                                                                                                │         │
   └───────────┴───────────┴───────────┴───────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴─────────┘
   ```

## (Optional) Self Assessment
1. What are the model access requirements for `HopSkipJump`?
2. Find a set of _best_ parameters for `HopSkipJump` that provides excellent visual quality with few "Total Queries".   

[[Demo Home]](../demo/README.md)
