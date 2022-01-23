# DEMO 2: Credit Card Fraud Integrity Attack Assessment

## Objective
Determine roughly how many queries are required to successfully evade `creditfraud` model with `BoundaryAttack` and `HopSkipJump`

## Threat Model
- Attacker knowledge: API access to model
- Security violation: integrity

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


4. Let's try `BoundaryAttack`
   ```
   use BoundaryAttack
   set --max_iter 500 --epsilon 0.001 --delta 0.001 --step_adapt 0.1
   run
   ```

5. Let's try `HopSkipJump`
   ```
   use HopSkipJump
   set --max_iter 5 --max_eval 1250
   run
   ```

6. Let's switch back to our previous `BoundaryAttack` to try different parameters
   ```
   show attacks
   use <Attack id for Boundary Attack>
   set --max_iter 10 --epsilon 0.1 --delta 0.1
   run
   ```

7. Exercise for reader: switch back and forth between your `HopSkipJump` and `BoundaryAttack`.  Try adjusting parameters such that you have a "1/1 Success", but in few "Total Queries".  For `BoundaryAttack`, you might play with `epsilon` and `max_iter`.  For `HopSkipJump`, you might play with `max_iter`,  `max_eval` and `init_size`.
