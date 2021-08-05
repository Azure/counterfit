# Anti-Phishing Evasion Challenge
This document describes how to start experimenting with evading the anti-phishing models using Counterfit.

Note that this is just an example illustrating how to use Counterfit to evade a target model, participants in the competition should try to modify existing attacks, or develop their own attacks.

It is assumed that you are using the competition docker image and have persisted your credentials from https://mlsec.io/myuser/ using the `mlsec_creds` command as described in [Getting Started](getting_started.md).

<!-- vscode-markdown-toc -->
* [Interact with a target](#interact-with-a-target)
* [Select an attack](#select-an-attack)
* [Set attack parameters](#set-attack-parameters)
* [Run the attack](#run-the-attack)
* [Upload the results](#upload-the-results)

<!-- vscode-markdown-toc-config
	numbering=false
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

## <a name='interact-with-a-target'></a>Interact with a target
```
counterfit> list targets

Name             Type             Input Shape      Location

----------------------------------------------------------------------------------------------------------------------------------------
creditfraud      numpy            (30,)            counterfit/targets/creditfraud/creditfraud_sklearn_pipeline.pkl
ember            pe               (1,)             counterfit/targets/ember/ember_model.txt.gz
mlsecphish       html             (1,)             http://127.0.0.1:8085/eval
```

```
counterfit> interact mlsecphish
scanning malware sample info from counterfit/targets/mlsecphish/phishing_samples_2021.zip
```

## <a name='select-an-attack'></a>Select an attack
```
mlsecphish> load mlsecevade

[+] Framework loaded successfully!
```

```
mlsecphish> list attacks

Name                       Type             Category         Tags             Framework
----------------------------------------------------------------------------------------
boundary-html              evasion          blackbox         html             mlsecevade
hop_skip_jump-html         evasion          blackbox         html             mlsecevade
hyperopt-html              evasion          blackbox         html             mlsecevade
randdescent-html           evasion          blackbox         html             mlsecevade
zoo-html                   evasion          blackbox         html             mlsecevade
boundary-pe                evasion          blackbox         pe               mlsecevade
hop_skip_jump-pe           evasion          blackbox         pe               mlsecevade
hyperopt-pe                evasion          blackbox         pe               mlsecevade
zoo-pe                     evasion          blackbox         pe               mlsecevade
```

For this exercise, we'll use the `randdescent-html` attack, but any attack with an `html` tag can be used.
```
mlsecphish> use randdescent-html

[+] Using randdescent-html cb7a1fa5
```

## <a name='set-attack-parameters'></a>Set attack parameters
```
mlsecphish>randdescent-html> show options

Attack Parameter (type)      Default       Current
-----------------------------------------------------
            n_iters (int)  100           100
            n_times (int)  1             1
       sample_index (int)  0             0
       target_class (int)  0             0
```

The `n_iters` parameter corresopnds to the number of model queries the attack will spend in decreasing the target model "malicious" score.  The `n_times` parameter (default=1) tells that algorithm to apply each HTML modification action multiple (for `n_times > 1`) times, and is analgous to "step size" in gradient descent.

There are ten phishing samples in the dataset.  To take an initial pass at each of them using a small query budget,
```
set n_iters=10 sample_index=`list(range(10))`
```

```
mlsecphish>randdescent-html> set n_iters=10 sample_index=`list(range(10))`

Attack Parameter (type)      Default       Previous        New
-------------------------------------------------------------------
            n_iters (int)  100           10
            n_times (int)  1             1
       sample_index (int)  0             0             [0, 1, 2, 3,
                                                       4, 5, 6, 7,
                                                       8, 9]
       target_class (int)  0             0
```

## <a name='run-the-attack'></a>Run the attack
```
mlsecphish>randdescent-html> run

[+] Running randdescent-html on mlsecphish

sample 1:   0%|                                                                 | 0/10 [00:00<?, ?it/s]
sample 2: 100%|████████████████████████████████████████████████████████| 10/10 [00:08<00:00,  1.17it/s]
sample 3:  40%|██████████████████████▊                                  | 4/10 [00:33<00:50,  8.40s/it]
sample 4: 100%|████████████████████████████████████████████████████████| 10/10 [00:11<00:00,  1.13s/it]
sample 5: 100%|████████████████████████████████████████████████████████| 10/10 [01:24<00:00,  8.42s/it]
sample 6: 100%|████████████████████████████████████████████████████████| 10/10 [00:05<00:00,  1.70it/s]
sample 7: 100%|████████████████████████████████████████████████████████| 10/10 [00:14<00:00,  1.44s/it]
sample 8: 100%|████████████████████████████████████████████████████████| 10/10 [00:06<00:00,  1.59it/s]
sample 9: 100%|████████████████████████████████████████████████████████| 10/10 [00:07<00:00,  1.26it/s]
sample 10: 100%|███████████████████████████████████████████████████████| 10/10 [00:12<00:00,  1.22s/it]

Increase terminal width to show results.

[+] 2/10 succeeded

[+] Elapsed time [sec] 206.1

[+] Total number of queries [rate] 106 (1.9 sec/query)

     Sample Index      Label (conf)     Attack Label (conf)  filesize
---------------------------------------------------------------------
1.               0          1 (0.7348)           0 (0.6714)     15005
2.               1          1 (0.7534)           1 (0.5864)     94937
3.               2          1 (0.6382)           0 (0.5116)   4199590
4.               3          1 (0.6970)           1 (0.5544)     44281
5.               4          1 (0.9120)           1 (0.6024)    189902
6.               5          1 (0.6780)           1 (0.6770)    141630
7.               6          1 (0.8930)           1 (0.7762)     67715
8.               7          1 (0.6530)           1 (0.6530)      9513
9.               8          1 (0.7940)           1 (0.5872)    161512
10.              9          1 (0.7400)           1 (0.6162)     28974
```

In this case, two samples evade the target in only a few queries!  One of them exceeds 2 MiB, which is too large to upload!  So, some modifications to the algorithm may be warranted to prevent large files.

There are two things to do before proceeding:
1. Modify the algorithm to prevent large files
2. Continue iterating on this attack for files that remain malicious to the model

## <a name='upload-the-results'></a>Upload the results
When you are satisfied, you may upload your submission as an encrpyted ZIP file automatically:
```
mlsecphish>randdescent-html> phish_upload 

[+] Successfully uploaded counterfit/targets/mlsecphish/results/mlsecphish.zip
```

You will not see your score immediately at [https://mlsec.io/pscores/] since the backend system must validate each of the samples in your submission.  Please check back in 30 minutes.  Also, please note that there is a rate limit on uploads, so you should use of the `upload` command sparingly.
