# DEMO 2: Credit Fraud Security Assessment
1. List available targets
  ```
  list targets
  ```


2. Interact with `creditfraud`
  ```
  interact creditfraud
  ```


3. List the available attacks
  ```
  load art
  list attacks
  ```


4. Scan the target across attacks (3 iterations each, enable logging)
   ```
   scan -n 3 --log
   ```


5. Save the results of the scan (note the output filename that you should use below)
  ```
  save
  ```


6. With the `--log`, every model query has been logged.  What's in the log?  Replace `<filename>` with the output `.json` file you observed from the `save` command.
   ```
   !tail -n 1000 <filename>
   ```


7. Let's take a look at a fraudulent transaction, `sample_index=0` of the data that is included in the target definition
  ```
  predict -i 0
  ```


8. Let's scan again with 3 iterations, but targeting only `sample_index=0` using `hop_skip_jump`, with the `--verbose` flag set.
  ```
  scan -n 3 --set sample_index=0 --attack hop_skip_jump --verbose 
  ```

9. From the best performing scan, you can `set` the parameters that work best and run a single attack with those parameters via (your parameters may differ)
  ```
  use hop_skip_jump
  set sample_index=0 targeted=1 target_class=0 init_eval=100 max_eval=500
  run
  ```


9. What is the feature vector from the last attack in the scan?
  ```
  predict -r
  ```


10. What was the original sample?  How close is it to the perturbed input?
  ```
  predict -i 0
  ```


11.  (Exercise for the reader)  Can you use `set` and `run` to find an attack that uses the _least_ number of queries that causes `sample_index=0` to appear benign?
