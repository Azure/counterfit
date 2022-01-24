# DEMO 3: Movie Reviews Sentiment Analysis
[[Demo Home]](README.md)
## Objective
Change the spelling of a few words to change the sentiment of an ML model that understands movie reviews.

## Threat Model
- Attacker knowledge: API access to model
- Security violation: integrity

## Steps
1. List available targets
  ```
  list targets
  ```


2. Interact with `movie_reviews`
  ```
  interact movie_reviews
  ```

3. Look at a few movie reviews
  ```
  predict -i range(5)
  ```


4. Load `textattack` and list possible attacks
  ```
  load textattack
  list attacks
  ```


4. Let's try `DeepWordBugGao2018`
   ```
   use DeepWordBugGao2018
   ```

5. Set `sample_index` to 3.  Notice there are no other algorithmic parameters to set.
   ```
   set --sample_index 3
   ```

6. Run the attack
   ```
   run
   ```

7. Look (scroll) up to see what changed between the original and final.

8. You can save this result using
   `save -p`
   and view the resulting file using `!cat <filename>`.

## (Optional) Self Assessment
1. How would you run this attack with the same parameters simultaneously for several different movie reviews?  (Hint: how would you include many different values for `sample_index` during `run`?)
2. The first 10 samples include only positive reviews (`predict -i range(10)`), but the last 10 samples include both positive and negative reviews (`predict -i range(90,100)`).  Can you find a negative review (`Label` is `0`) for which an attack changes it to a positive review?

[[Demo Home]](README.md)