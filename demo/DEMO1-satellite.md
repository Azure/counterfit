# DEMO 1: Satellite Images Red Team Operation
[[Demo Home]](README.md)
## Objective
Change the label of a satellite image (true label: `stadium`) into `airplane`.

## Threat Model
- Attacker knowledge: API access to model
- Security violation: integrity

## Steps
1. What models are defined in our environment?
  ```
  list targets
  ```


2. Interact with the `satellite` target
  ```
  interact satellite
  ```


3. What frameworks are there?
  ```
  list frameworks
  ```


4. Load the ART framework
  ```
  load art
  ```


5. List attacks.
  ```
  list attacks
  ```


6. For this target, we'll want to use an attack that requires only API access, and works on image data (see `Tags` column).  Let's use `HopSkipJump`.  (Hint: This creates a new attack, which can be referenced by an id, view them all with `show attacks`, and use a different attack using `use <attack_id>`.)
  ```
  use HopSkipJump
  ```


7. Show information about the attack
  ```
  show info
  ```


8. What does the model think about the images for sample indices 0 through 9? (Hint: we can use Python notation to select multiple indices).
  ```
  predict -i range(10)
  ```


9. Set parameters for the attack.  (Hint: to see what options are available to set, type `show options` or `set`.)  We'll use sample index 5 that corresponds to an image of a stadium.
  ```
  set --sample_index 5 --norm 2 --max_iter 10 --max_eval 5000 --verbose true
  ```


10. Execute the attack.  This may take several minutes.
  ```
  run
  ```
  Hint: if your attack is unsuccessful (e.g., `Failed to draw a random image that is adversarial`) try changing the algorithm parameters (e.g., `set --init_eval 400`).

11. Let's show the "before" and "after" pictures.  If you've done a `predict -i 5`, then "before" picture is in the folder `counterfit/targets/satellite/results/predict/initial-satellite-a85e763e-sample-5.png`.  The "after" picture is in `counterfit/targets/satellite/results/[attack_id]/initial-satellite-a85e763e-sample-5.png`. (Hint: In the JupyterLab demo environment, you cause JupyterLab file navigator ot view these.)


12. Learn more!
  ```
  help
  ```

## (Optional) Self Assessment
1. What minimum level of model access was required for this model?
2. How many queries were required to (a) change the decision of the ML model and (b) still remain convincing to a human?
3. For HopSkipJump, change `norm`, `max_iter` and `max_eval` parameters to tune the results of the algorithm.  Are there tradeoffs between the resulting quality of the adversarial example and number of queries required to create it?

[[Demo Home]](README.md)
