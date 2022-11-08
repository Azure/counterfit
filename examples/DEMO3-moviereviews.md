# DEMO 3: Movie Reviews Sentiment Analysis
[[Demo Home]](../demo/README.md)
## Objective
Change the spelling of a few words to change the sentiment of an ML model that understands movie reviews.

## Threat Model
- Attacker knowledge: API access to model
- Security violation: integrity

## Steps

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


2. Interact with `movie_reviews`
     ```
     counterfit> set_target movie_reviews
     movie_reviews >
     ```

3. Look at a few movie reviews
   ```   
   movie_reviews> predict -i range(5)
   ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━┓
   ┃ Sample Index ┃ Sample                                                                                                                            ┃ Label ┃ Output Scores ┃
   ┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━┩
   │ 0            │ Ever watched a movie that lost the plot? Well, this didn't even really have one to begin with.<br /><br />Where to begin? The     │ 1     │ [0.01 0.99]   │
   │              │ achingly tedious scenes of our heroine sitting around the house with actually no sense of menace or even foreboding created even  │       │               │
   │              │ during the apparently constant thunderstorms (that are strangely never actually heard in the house-great double glazing)? The     │       │               │
   │              │ house that is apparently only a few miles from a town yet is several hours walk away(?) or the third girl who serves no purpose   │       │               │
   │              │ to the plot except to provide a surprisingly quick gory murder just as the tedium becomes unbearable? Or even the beginning which │       │               │
   │              │ suggests a spate of 20+ killings throughout the area even though it is apparent the killer never ventures far from the house? Or  │       │               │
   │              │ the bizarre ritual with the salt & pepper that pretty much sums up most of the films inherent lack of direction.<br /><br />Add a │       │               │
   │              │ lead actress who can't act but at least is willing to do some completely irrelevant nude shower scenes and this video is truly    │       │               │
   │              │ nasty, but not in the way you hope.<br /><br />Given a following simply for being banned in the UK in the 80's (mostly because of │       │               │
   │              │ a final surprisingly over extended murder) it offers nothing but curiosity value- and one classic 'daft' murder (don't worry-its  │       │               │
   │              │ telegraphed at least ten minutes before).<br /><br />After a walk in the woods our victim comes to a rather steep upward slope    │       │               │
   │              │ which they obviously struggle up. Halfway through they see a figure at the top dressed in black and brandishing a large scythe.   │       │               │
   │              │ What do they do? Slide down and run like the rest of us? No, of course not- they struggle to the top and stand conveniently nice  │       │               │
   │              │ and upright in front of the murder weapon.<br /><br />It really IS only a movie as they say..                                     │       │               │
   │ 1            │ This movie came as a huge disappointment. The anime series ended with a relatively stupid plot twist and the rushed introduction  │ 1     │ [0.01 0.99]   │
   │              │ of a pretty lame villain, but I expected Shamballa to tie up all the loose ends. Unfortunately, it didn't. It added more plot     │       │               │
   │              │ holes than it resolved, and confused more than it clarified. The animation and voice acting were great, but with an idiotic plot, │       │               │
   │              │ dull setting (most of the movie doesn't even take place in dull WWII Earth rather than the Alchemy world), and disappointing      │       │               │
   │              │ ending (Ed is useless for the rest of his days in a world with no alchemy, and he ditches Winry?), it was altogether pretty       │       │               │
   │              │ lackluster. Do yourself a favor-- disregard the last half of the anime as well as this movie, and read the manga.                 │       │               │
   │ 2            │ In this movie, Chávez supporters (either venezuelan and not-venezuelan) just lie about a dramatic situation in our country. <br   │ 1     │ [0.05 0.95]   │
   │              │ /><br />They did not say that the conflict started because of Chávez announcement firing a lot of PDVSA best workers just for     │       │               │
   │              │ political issues.<br /><br />They did not say anything about more than 96 TV interruptions transmitted by Chávez during only 3    │       │               │
   │              │ days in "CADENA NACIONAL" (a kind of confiscation o private TV signals). Each one with about 20 minutes of duration.<br /><br     │       │               │
   │              │ />They did not tell us anything about The quiting announcement made by General en Jefe Lucas Rincon Romero, Inspector General of  │       │               │
   │              │ the army forces, who is a traditional supporter of Chávez. Even now, in despite of his announcement, he is the Ministro de        │       │               │
   │              │ Interior y Justicia. After Chávez return he occuped the Charge of Ministro del Defensa (equals to Defense Secretary in US).<br    │       │               │
   │              │ /><br />They did not say anything about Chávez orders about shooting against a pacifical people concentration who was claiming    │       │               │
   │              │ for elections.<br /><br />They did not say anything about the people in this concentration that were killed by Chávez Supporters  │       │               │
   │              │ (either civilians and Military official forces).<br /><br />They present some facts in a wrong order, in order to lie.<br /><br   │       │               │
   │              │ />They did not say anything about venezuelan civilian society thats are even now claiming for an elections in order to solve the  │       │               │
   │              │ crisis and Chávez actions in order to avoid the elections.<br /><br />That's why i tell you.... This movie is just a lot of lies  │       │               │
   │              │ or a big lie.                                                                                                                     │       │               │
   │ 3            │ The story is about a psychic woman, Tory, who returns to her hometown and begins reliving her traumatic childhood past (the death │ 1     │ [0.44 0.56]   │
   │              │ of her childhood friend and abusive father). Tory discovers that her friend was just the first in a string of murders that are    │       │               │
   │              │ still occurring. Can her psychic powers help solve the crimes and stop the continuing murders? <br /><br />You really don't need  │       │               │
   │              │ to find out because, Oh My God! This was so so so so bad! I know all the Nora Roberts fans will flock to this movie and give it   │       │               │
   │              │ tons of 10's. Then the rest of us will see an IMDb score of 6 and actually think this movie is worth watching. But do not be      │       │               │
   │              │ fooled. The ending was predictable, the acting TERRIBLE (don't even get me started about the southern accents *y'all*) and the    │       │               │
   │              │ story was trite. Just remember....you were warned!                                                                                │       │               │
   │ 4            │ it got switched off before the opening credits had even finished appearing. The first joke was just so appallingly lame and       │ 1     │ [0.03 0.97]   │
   │              │ dreadfully acted that it had to go. You shouldn't really decide to watch this based on my review or not. I saw so little of it I  │       │               │
   │              │ shouldn't even really be commenting but suddenly it all became clear why the video shop guy was sniggering at us paying money to  │       │               │
   │              │ see it.<br /><br />Couldn't they have just made Earnest does Dallas?                                                              │       │               │
   └──────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴───────┴───────────────┘
   movie_reviews> 
   ```


4. Let's try `DeepWordBugGao2018`
   ```
   movie_reviews> set_attack deepwordbug_gao_2018 
   
   ```

5. Set `sample_index` to 3.  Notice there are no other algorithmic parameters to set.
   ```
   movie_reviews> set_params --sample_index 3
   ```

6. Run the attack
   ```
   movie_reviews>DeepWordBugGao2018:9b2ceb77> run
   textattack: Attempting to attack 10 samples when only 1 are available.
   Attack(
     (search_method): GreedyWordSwapWIR(
       (wir_method):  unk
     )
     (goal_function):  UntargetedClassification
     (transformation):  CompositeTransformation(
       (0): WordSwapNeighboringCharacterSwap(
           (random_one):  True
         )
       (1): WordSwapRandomCharacterSubstitution(
           (random_one):  True
         )
       (2): WordSwapRandomCharacterDeletion(
           (random_one):  True
         )
       (3): WordSwapRandomCharacterInsertion(
           (random_one):  True
         )
       )
     (constraints): 
       (0): LevenshteinEditDistance(
           (max_edit_distance):  30
           (compare_against_original):  True
         )
       (1): RepeatModification
       (2): StopwordModification
     (is_black_box):  True
   ) 
   
    10%|█████████████▌                                                                                                                          | 1/10 [00:27<04:08, 27.66s/it]--------------------------------------------- Result 1 ---------------------------------------------
   1 (99%) --> 0 (52%)
   
   Ever watched a movie that lost the plot? Well, this didn't even really have one to begin with.<br /><br />Where to begin? The achingly tedious scenes of our heroine sitting around the house with actually no sense of menace or even foreboding created even during the apparently constant thunderstorms (that are strangely never actually heard in the house-great double glazing)? The house that is apparently only a few miles from a town yet is several hours walk away(?) or the third girl who serves no purpose to the plot except to provide a surprisingly quick gory murder just as the tedium becomes unbearable? Or even the beginning which suggests a spate of 20+ killings throughout the area even though it is apparent the killer never ventures far from the house? Or the bizarre ritual with the salt & pepper that pretty much sums up most of the films inherent lack of direction.<br /><br />Add a lead actress who can't act but at least is willing to do some completely irrelevant nude shower scenes and this video is truly nasty, but not in the way you hope.<br /><br />Given a following simply for being banned in the UK in the 80's (mostly because of a final surprisingly over extended murder) it offers nothing but curiosity value- and one classic 'daft' murder (don't worry-its telegraphed at least ten minutes before).<br /><br />After a walk in the woods our victim comes to a rather steep upward slope which they obviously struggle up. Halfway through they see a figure at the top dressed in black and brandishing a large scythe. What do they do? Slide down and run like the rest of us? No, of course not- they struggle to the top and stand conveniently nice and upright in front of the murder weapon.<br /><br />It really IS only a movie as they say..
   
   Ever watched a movie that lost the Hlot? Well, this didn't een really have one to begiCn with.<br /><br />Where to begin? The achingly tedious scenes of our heroine sitting around the house with actually no sense of menace or even foreboding created eEen during the apparently constant thunderstorms (that are strangely never actually heard in the house-great double glazing)? The house that is apparently only a few miles from a town yet is esveral hours walk away(?) or the third girl who serves no purpose to the lot except to provide a surprisingly quick gory murder just as the tedium becomes unbearable? Or Veven the beginning which suggests a spate of 20+ killings throughout the area eBven though it is apparent the killer never ventures far from the house? Or the bizarre ritual with the salt & pepper that pretty much sums up most of the films inherent lack of direction.<br /><br />Add a lead actress who can't act but at least is willing to do some completely irrelevant nude shower scenes and this video is lruly nasty, but not in the way you hope.<br /><br />Given a following simply for being banned in the UK in the 80's (molstly because of a final surprisingly over extended murder) it offers nothing but curiosity value- and one classic 'daft' murder (don't worry-its telegraphed at least ten minutse before).<br /><br />After a walk in the woods our victim comes to a rEather steep upward slope which they obviously struggle up. Halfway through they see a figure at the top dressed in black and brandishing a large scythe. What do they do? Slide down and run like the Arest of us? No, of course not- they struggle to the top and stand conveniently nice and upright in front of the Wurder weapon.<br /><br />It really IS only a movie as they Xsay..
   
   
   [Succeeded / Failed / Skipped / Total] 1 / 0 / 0 / 1:  10%|████████▏                                                                         | 1/10 [00:27<04:08, 27.67s/it]
   
   +-------------------------------+--------+
   | Attack Results                |        |
   +-------------------------------+--------+
   | Number of successful attacks: | 1      |
   | Number of failed attacks:     | 0      |
   | Number of skipped attacks:    | 0      |
   | Original accuracy:            | 100.0% |
   | Accuracy under attack:        | 0.0%   |
   | Attack success rate:          | 100.0% |
   | Average perturbed word %:     | 4.78%  |
   | Average num. words per input: | 314.0  |
   | Avg num queries:              | 383.0  |
   +-------------------------------+--------+
   [+] success: Attack completed 9b2ceb77
   ```

7. Show results
   ```
   movie_reviews>DeepWordBugGao2018:9b2ceb77> show results 
   ┏━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
   ┃ Success ┃ Elapsed time ┃ Total Queries        ┃
   ┡━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
   │ 1/1     │ 27.7         │ 385 (13.9 query/sec) │
   └─────────┴──────────────┴──────────────────────┘
   ┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
   ┃           ┃ Input     ┃ Adversar… ┃           ┃                                                                                                                ┃         ┃
   ┃ Sample    ┃ Label     ┃ Label     ┃ % edit    ┃                                                                                                                ┃         ┃
   ┃ Index     ┃ (conf)    ┃ (conf)    ┃ dist.     ┃ Adversarial Input                                                                                              ┃ success ┃
   ┡━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
   │ 0         │ 1         │ 0         │ 0.0097    │ Ever watched a movie that lost the Hlot? Well, this didn't een really have one to begiCn with.<br /><br        │ True    │
   │           │ (0.9871)  │ (0.5242)  │           │ />Where to begin? The achingly tedious scenes of our heroine sitting around the house with actually no sense   │         │
   │           │           │           │           │ of menace or even foreboding created eEen during the apparently constant thunderstorms (that are strangely     │         │
   │           │           │           │           │ never actually heard in the house-great double glazing)? The house that is apparently only a few miles from a  │         │
   │           │           │           │           │ town yet is esveral hours walk away(?) or the third girl who serves no purpose to the lot except to provide a  │         │
   │           │           │           │           │ surprisingly quick gory murder just as the tedium becomes unbearable? Or Veven the beginning which suggests a  │         │
   │           │           │           │           │ spate of 20+ killings throughout the area eBven though it is apparent the killer never ventures far from the   │         │
   │           │           │           │           │ house? Or the bizarre ritual with the salt & pepper that pretty much sums up most of the films inherent lack   │         │
   │           │           │           │           │ of direction.<br /><br />Add a lead actress who can't act but at least is willing to do some completely        │         │
   │           │           │           │           │ irrelevant nude shower scenes and this video is lruly nasty, but not in the way you hope.<br /><br />Given a   │         │
   │           │           │           │           │ following simply for being banned in the UK in the 80's (molstly because of a final surprisingly over extended │         │
   │           │           │           │           │ murder) it offers nothing but curiosity value- and one classic 'daft' murder (don't worry-its telegraphed at   │         │
   │           │           │           │           │ least ten minutse before).<br /><br />After a walk in the woods our victim comes to a rEather steep upward     │         │
   │           │           │           │           │ slope which they obviously struggle up. Halfway through they see a figure at the top dressed in black and      │         │
   │           │           │           │           │ brandishing a large scythe. What do they do? Slide down and run like the Arest of us? No, of course not- they  │         │
   │           │           │           │           │ struggle to the top and stand conveniently nice and upright in front of the Wurder weapon.<br /><br />It       │         │
   │           │           │           │           │ really IS only a movie as they Xsay..                                                                          │         │
   └───────────┴───────────┴───────────┴───────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴─────────┘
   ```

9. Look (scroll) up to see what changed between the original and final.

10. You can save this result using
    `save -p`
    and view the resulting file using `!cat <filename>`.

## (Optional) Self Assessment
1. How would you run this attack with the same parameters simultaneously for several different movie reviews?  (Hint: how would you include many different values for `sample_index` during `run`?)
2. The first 10 samples include only positive reviews (`predict -i range(10)`), but the last 10 samples include both positive and negative reviews (`predict -i range(90,100)`).  Can you find a negative review (`Label` is `0`) for which an attack changes it to a positive review?

[[Demo Home]](../demo/README.md)