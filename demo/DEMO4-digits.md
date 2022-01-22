# DEMO 4: White-box attack of an on-disk

## Objective
Compare white-box and API attacks to digits model

## Threat Model
- Attacker knowledge: full access to model
- Security violation: integrity

1. List available targets
  ```
  list targets
  ```


2. Interact with `interact digits_keras`
  ```
  interact digits_blackbox
  ```

3. Look at a few digits
  ```
  predict -i range(5)
  ```


4. Load `art` and list possible attacks
  ```
  load art
  list attacks
  ```


5. Let's first try a whitebox attack `CarliniLInfMethod`
   ```
   use CarliniL0Method
   ```

6. Set some parameters
   ```
   set --eps 0.15 --learning_rate 0.1 --sample_index 3
   ```

7. Run the attack
   ```
   run
   ```

8. Compare this with an API-only attack.  We'll use `HopSkipJump` with default parameters.
   ```
   use HopSkipJump
   set --sample_index 3 --max_eval
   run
   ```

9. Exercise for the reader: compare the visual quality of these two attacks?  Which is better?  Which attack shows lower "Max Absolute Change"?
