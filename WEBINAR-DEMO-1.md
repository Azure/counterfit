# DEMO 1: Satellite Images Red Team Operation
1. What models are defined in my environment?
  ```
  list targets
  ```


2. Interact with a target
  ```
  interact satelliteimages
  ```


3. What's this model about?
  ```
  show info
  ```


4. What frameworks are there?
  ```
  list frameworks
  ```


5. Load the ART framework
  ```
  load art
  ```


6. List attacks
  ```
  list attacks
  ```


7. Use `hop_skip_jump`
  ```
  use hop_skip_jump
  ```


8. Show more information about the attack
  ```
  show info
  ```


9. Set parameters for the attack
  ```
  set init_size=50 max_iter=20 max_eval=500
  ```


10. What does the model think about the image at `sample_index=0` now?
  ```
  predict
  ```


11. Execute the attack
  ```
  run
  ```


12. View the  "before" (`-initial`) and "after" (`-final`) images in the `satelliteimages` (use JupyterLab file navigator)


13. Learn more!
  ```
  help
  ```
