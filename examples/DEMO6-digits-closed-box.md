# DEMO 6: Closed-box attack on Digits model
[[Demo Home]](./README.md)
## Objective
Change the label of a digit image (true label: `5`) into `3`.

## Threat Model
- Attacker knowledge: API access to model
- Security violation: integrity

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



3. Set target to `digits_mlp`
   ```
   counterfit> set_target digits_mlp
   digits_mlp >
   ```

4. Look at a few digits
   ```
   digits_mlp> predict -i range(10)
   ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃ Sample Index ┃ Sample                                                                                                              ┃ Label ┃ Output Scores                                       ┃
   ┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
   │ 0            │ https://counterfit4s2tanqztopsc.blob.core.windows.net/counterfit/targets/results/predict/initial-digits_mlp-032566… │ 5     │ [0.00 0.00 0.00 0.00 0.00 1.00 0.00 0.00 0.00 0.00] │
   │ 1            │ https://counterfit4s2tanqztopsc.blob.core.windows.net/counterfit/targets/results/predict/initial-digits_mlp-5035cf… │ 0     │ [1.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00] │
   │ 2            │ https://counterfit4s2tanqztopsc.blob.core.windows.net/counterfit/targets/results/predict/initial-digits_mlp-bd4a80… │ 4     │ [0.00 0.00 0.00 0.00 1.00 0.00 0.00 0.00 0.00 0.00] │
   │ 3            │ https://counterfit4s2tanqztopsc.blob.core.windows.net/counterfit/targets/results/predict/initial-digits_mlp-bcebd1… │ 1     │ [0.00 1.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00] │
   │ 4            │ https://counterfit4s2tanqztopsc.blob.core.windows.net/counterfit/targets/results/predict/initial-digits_mlp-69c2ac… │ 9     │ [0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 1.00] │
   │ 5            │ https://counterfit4s2tanqztopsc.blob.core.windows.net/counterfit/targets/results/predict/initial-digits_mlp-17d215… │ 2     │ [0.00 0.00 1.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00] │
   │ 6            │ https://counterfit4s2tanqztopsc.blob.core.windows.net/counterfit/targets/results/predict/initial-digits_mlp-18a723… │ 1     │ [0.00 1.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00] │
   │ 7            │ https://counterfit4s2tanqztopsc.blob.core.windows.net/counterfit/targets/results/predict/initial-digits_mlp-a3bb68… │ 3     │ [0.00 0.00 0.00 1.00 0.00 0.00 0.00 0.00 0.00 0.00] │
   │ 8            │ https://counterfit4s2tanqztopsc.blob.core.windows.net/counterfit/targets/results/predict/initial-digits_mlp-4d8a91… │ 1     │ [0.00 1.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00] │
   │ 9            │ https://counterfit4s2tanqztopsc.blob.core.windows.net/counterfit/targets/results/predict/initial-digits_mlp-a5418d… │ 4     │ [0.00 0.00 0.00 0.00 1.00 0.00 0.00 0.00 0.00 0.00] │
   └──────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴───────┴─────────────────────────────────────────────────────┘
      
   ```


5. List possible attacks
   ```
   digits_mlp> list attacks

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
   digits_mlp>> set_attack hop_skip_jump 
   [+] success:  Using 92784548
   
   digits_mlp>HopSkipJump:92784548> set_params --sample_index 0 --max_eval 1000 --max_iter 50
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
   │ max_eval (int)       │ 1000       │ 1000       │ Maximum number of evaluations for estimating gradient.                   │
   │ max_iter (int)       │ 50         │ 50         │ Maximum number of iterations.                                            │
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
   ```
   
9. Run the attack
   ```
   digits_mlp>HopSkipJump:92784548> run
   HopSkipJump: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  2.53it/s]
   [+] success:  Attack completed 92784548
   ```

10. Show results

   ```
   digits_mlp>HopSkipJump:92784548> show results
   [-] info:  Image has been saved in the location <Azure Storage Blob SAS URL>
   ┏━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃ Success ┃ Elapsed time ┃ Total Queries            ┃
   ┡━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
   │ 1/1     │ 7.6          │ 24552 (3251.4 query/sec) │
   └─────────┴──────────────┴──────────────────────────┘
   ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
   ┃              ┃                    ┃ Adversarial Label  ┃              ┃                                                                                                                ┃         ┃
   ┃ Sample Index ┃ Input Label (conf) ┃ (conf)             ┃ Max Abs Chg. ┃ Adversarial Input                                                                                              ┃ Success ┃
   ┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
   │ 0            │ 5 (0.9990)         │ 3 (0.9983)         │ 1.0902       │ https://counterfit4s2tanqztopsc.blob.core.windows.net/counterfit/targets/results/92784548/digits_mlp-913d75ce… │ [ True] │
   └──────────────┴────────────────────┴────────────────────┴──────────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴─────────┘
   ```

## (Optional) Self Assessment
1. What are the model access requirements for `HopSkipJump`?
2. Find a set of _best_ parameters for `HopSkipJump` that provides excellent visual quality with few "Total Queries".  
3. Try running with the parameters `set_params --sample_index 0 --max_eval 500 --max_iter 10` and observe the adversarial class label? 

