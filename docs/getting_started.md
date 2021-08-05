# Getting Started
This document briefly describes how to get started in using Counterfit in the [Machine Learning Security Evasion Competition](https://mlsec.io/).

<!-- vscode-markdown-toc -->
* [Setting up Counterfit](#setting-up-counterfit)
    * [Run the JupyterLab environment via Docker](#run-the-jupyterlab-environment-via-docker)
    * [Launch Counterfit](#launch-counterfit)
    * [Set your username and API Token](#set-your-username-and-api-token)
* [Competing with Counterfit](#competing-with-counterfit)
    * [Try the basic solution included in Counterfit](#try-the-basic-solution-included-in-counterfit)
    * [Extend Counterfit](#extend-counterfit)
    * [Automate a solution](#automate-a-solution)
    * [Submit a PR when the competition concludes](#submit-a-pr-when-the-competition-concludes)

<!-- vscode-markdown-toc-config
	numbering=false
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->
## <a name='setting-up-counterfit'></a>Setting up Counterfit
These instructions require [Docker](https://docs.docker.com/get-docker/) so that malicious samples are contained inside a Linux docker container.  Alternatively, you may clone and install in a _Linux environment_ the `mlsecevasion/2021` [branch of Counterfit](https://github.com/Azure/counterfit/tree/mlsecevasion/2021) via `git clone --single-branch --branch mlsecevasion/2021 https://github.com/Azure/counterfit.git`.

### <a name='run-the-jupyterlab-environment-via-docker'></a>Run the JupyterLab environment via Docker
User `docker` to launch a JupterLab environment
```
$ docker run -p8888:8888 azuretrustworthyml/counterfit-mlsecevasion:latest

    To access the server, open this file in a browser:
        file:///home/jovyan/.local/share/jupyter/runtime/jpserver-10-open.html
    Or copy and paste one of these URLs:
        http://127.0.0.1:8888/lab?token=85bd9186f156334478c0881356acdbfc3396f39a0aad5a0f
```
Then, navigate a web browser to the `http://127.0.0.1:8888/lab?token=...` link shown.

### <a name='launch-counterfit'></a>Launch Counterfit
Launch Counterfit insider the JupterLab environment by clicking the `Terminal` icon.  If at anytime you `exit` Counterfit within the terminal, you can start again by typing

```
python counterfit.py


---------------------------------------------------
Microsoft
                          __            _____ __
  _________  __  ______  / /____  _____/ __(_) /_
 / ___/ __ \/ / / / __ \/ __/ _ \/ ___/ /_/ / __/
/ /__/ /_/ / /_/ / / / / /_/  __/ /  / __/ / /
\___/\____/\__,_/_/ /_/\__/\___/_/  /_/ /_/\__/

                                        #ATML

---------------------------------------------------


        [+] 28 attacks
        [+] 7 targets

counterfit>
```

### <a name='set-your-username-and-api-token'></a>Set your username and API Token
Use the `mlsec_creds` command to set your username and API Token.  You can find this by logging into https://mlsec.io/myuser/ and copying the `Username` and `API Token` fields shown in the table.

```
counterfit> mlsec_creds
Login to        https://mlsec.io/myuser/
and enter the following information
Nickname: asdfasdf
API Token: 0123456789abcdef0123456789abcdef
```

Your credentials will be persisted as a new command in the `.counterfit` startup script via `mlsec_creds -u username -k "API_KEY_IN_QUOTES"`.

## <a name='competing-with-counterfit'></a>Competing with Counterfit
To be eligible for a bonus prize, your solution must 
1. extend Counterfit
2. automate a solution using Counterfit scripts, and 
3. submit a GitHub pull request with the improvements after the competition concludes

### <a name='try-the-basic-solution-included-in-counterfit'></a>Try the basic solution included in Counterfit
A basic solution is provided for each track in the Attacker Challenge. For a quick demo, visit the following:
* [Anti-Phishing Challenge](antiphishing.md)
* [Anti-Malware Challenge](antimalware.md)

### <a name='extend-counterfit'></a>Extend Counterfit
There are several ways to improve the basic solutions. Some examples include the following:
* Algorithmic improvements
   1. Some algorithms result in files that are too large for upload.  You may consider modifications that regularize the solution to be small, or constrains the solution to be small (e.g., under 2 MiB for the anti-malware evasion challenge).
   2. You may hack algorithms from other sources.  For example, there is no version of `randdescent-html` for `pe` files. 
   3. You may create your own algorithmic solution.
* Process improvements
   1. Extend counterfit workflow so that in a single working session, algorithmic modifications to your solution may be applied iteratively.
* Bugfixes
   1. Surely there are no bugs in counterfit!  But finding and fixing one would count.

### <a name='automate-a-solution'></a>Automate a solution
Counterfit can be automated with scripts!  And you must do this to qualify for the bonus prize.

A script consists of a text file with one command per line.  For example, an anti-phishing evasion demo script `antiphishing_evasion_demo` would contain the lines (having already issued `mlsec_creds` once)

```
!echo BEGIN DEMO
interact mlsecphish
load mlsecevade
use randdescent-html
set n_iters=10 sample_index=`list(range(10))`
run
phish_upload
!echo DONE DEMO
```

Note that `!{command}` executes `{command}` in the `/bin/bash` interpreter.

The script can be executed via

```
counterfit> run_script antiphishing_evasion_demo
```

or from the shell as

```
python counterfit.py "run_script antiphishing_evasion_demo
```

### <a name='submit-a-pr-when-the-competition-concludes'></a>Submit a PR when the competition concludes
Should your automated Counterfit script be the highest-ranking solution, you must submit your Counterfit improvements to be eligible for the [bonus prize](https://mlsec.io/tos). The PR should be submitted against the [mlsecevasion/2021](https://github.com/Azure/counterfit/tree/mlsecevasion/2021) branch of the Counterfit GitHub repo.