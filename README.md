# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real world recommenders, like the ones behind streaming services, learn from huge amounts of behavior data, such as what millions of people play, skip, save, and replay, and they combine that with audio features and social signals to predict what a specific person will enjoy next. Those systems are powerful, but they are also complex, opaque, and driven by engagement goals that are not always the same as the listener's best interest. My version keeps the same core idea but makes it small and transparent, so I prioritize clarity over scale. Instead of learning from behavior, I represent a user's taste as a simple profile, compare each song to that profile using a scoring rule I can read and explain, and then rank the results so the best matches rise to the top. My goal is a recommender whose reasoning a person can follow line by line, not a black box.

My simulation uses the following features.

**`Song` objects use:**

- `id`, an identifier for the song
- `title`, the song name
- `artist`, who performs it
- `genre`, the style category, for example pop, lofi, rock
- `mood`, the feel of the track, for example happy, chill, intense
- `energy`, a number from 0 to 1 for how energetic it is
- `tempo_bpm`, the speed in beats per minute
- `valence`, a number from 0 to 1 for how positive or upbeat it sounds
- `danceability`, a number from 0 to 1 for how danceable it is
- `acousticness`, a number from 0 to 1 for how acoustic it is

**`UserProfile` objects use:**

- `favorite_genre`, the genre the user prefers
- `favorite_mood`, the mood the user prefers
- `target_energy`, the energy level the user is aiming for, from 0 to 1
- `likes_acoustic`, a true or false flag for whether the user prefers acoustic songs

The `Recommender` scores each song by comparing these song features against the user's profile, rewarding close matches, and then it ranks all the scored songs and returns the top few as recommendations.

### Data Flow

The system moves through three stages.

- Input, the user's taste profile, for example favorite_genre, favorite_mood, target_energy, likes_acoustic.
- Process, the loop, load every song from the CSV and judge each one individually with the scoring logic below, producing a score and a list of reasons for that song.
- Output, the ranking, sort all the scored songs from highest to lowest and return the top K as the recommendations, each with a short explanation.

In short, Input (User Prefs), then Process (score every song in the loop), then Output (rank and return the top K).

### Algorithm Recipe

For each song I start the score at 0, add points for each rule that matches, and record a reason for every point awarded. Higher total means a better match. The maximum possible score is 5.0.

- Genre match, weight 2.0. If the song's genre equals the user's favorite_genre, add 2.0. Genre is the strongest and most stable taste signal, so it carries the most weight.
- Mood match, weight 1.0. If the song's mood equals the user's favorite_mood, add 1.0. Mood is a real but softer signal that partly overlaps with energy, so it is worth half of a genre match.
- Energy closeness, up to 1.5. This rewards closeness, not high values. I take the distance between the song's energy and the user's target_energy, both on a 0 to 1 scale, and add (1 minus distance) times 1.5, so a perfect energy match adds 1.5 and an opposite value adds close to 0.
- Acoustic preference, weight 0.5. If the user likes acoustic and the song's acousticness is 0.6 or higher, add 0.5. If the user does not like acoustic and the song's acousticness is below 0.4, add 0.5. This is a light tie breaker.

Final weights, Genre 2.0, Energy up to 1.5, Mood 1.0, Acoustic 0.5. The genre to mood ratio and the energy maximum are the main knobs I can tune in my experiments.

After every song is scored, the ranking step sorts by score from highest to lowest, breaks ties by preferring the song whose energy is closest to target_energy, keeps the top K, and joins each song's reasons into a short explanation.

### Potential Biases

- Genre over prioritization. Because genre carries the most weight, the system might bury a great song that perfectly matches the user's mood and energy simply because its genre label is different, for example an acoustic jazz track for a lofi fan.
- Exact match blind spots. Genre and mood are matched exactly, so closely related styles, for example lofi and ambient, score a full miss even when they feel similar to a listener.
- Popularity and catalog bias. The recommender can only suggest what is in the tiny CSV, and it has no idea about song quality, lyrics, or language, so it will happily recommend a weak song that matches the profile over a great song that does not.
- Profile narrowness. The user profile only captures four preferences, so features like tempo, valence, and danceability are ignored, and two very different songs can look identical to the system.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

An example run for a single profile (genre=pop, mood=happy, energy=0.8) looks like this:

```
  1. Sunrise City  by Neon Echo
     Score: 4.47
     Reasons: genre match (+2.0), mood match (+1.0), energy close to target (+1.47)

  2. Gym Hero  by Max Pulse
     Score: 3.30
     Reasons: genre match (+2.0), energy close to target (+1.30)

  3. Rooftop Lights  by Indigo Parade
     Score: 2.44
     Reasons: mood match (+1.0), energy close to target (+1.44)

  4. Night Drive Loop  by Neon Echo
     Score: 1.42
     Reasons: energy close to target (+1.42)

  5. Storm Runner  by Voltline
     Score: 1.33
     Reasons: energy close to target (+1.33)
```

The top result, Sunrise City, is the only song that matches the profile on genre, mood, and energy at once, so it correctly earns the highest score. Running `python -m src.main` now prints a full suite of profiles, shown in the next section.

---

## Stress Test: Diverse and Adversarial Profiles

To evaluate the scoring logic, `src/main.py` runs six profiles: three normal listener archetypes and three adversarial edge cases designed to see if the scoring can be tricked. Each block below is real terminal output from `python -m src.main`.

### Normal archetypes

**High-Energy Pop** (genre=pop, mood=happy, energy=0.9, likes_acoustic=False)

```
  1. Sunrise City  by Neon Echo
     Score: 4.88
     Reasons: genre match (+2.0), mood match (+1.0), energy close to target (+1.38), not acoustic, as preferred (+0.5)

  2. Gym Hero  by Max Pulse
     Score: 3.96
     Reasons: genre match (+2.0), energy close to target (+1.46), not acoustic, as preferred (+0.5)

  3. Rooftop Lights  by Indigo Parade
     Score: 2.79
     Reasons: mood match (+1.0), energy close to target (+1.29), not acoustic, as preferred (+0.5)

  4. Storm Runner  by Voltline
     Score: 1.98
     Reasons: energy close to target (+1.48), not acoustic, as preferred (+0.5)

  5. Pulse Reactor  by Kilowatt
     Score: 1.93
     Reasons: energy close to target (+1.43), not acoustic, as preferred (+0.5)
```

**Chill Lofi** (genre=lofi, mood=chill, energy=0.35, likes_acoustic=True)

```
  1. Library Rain  by Paper Lanterns
     Score: 5.00
     Reasons: genre match (+2.0), mood match (+1.0), energy close to target (+1.50), acoustic, as preferred (+0.5)

  2. Midnight Coding  by LoRoom
     Score: 4.89
     Reasons: genre match (+2.0), mood match (+1.0), energy close to target (+1.40), acoustic, as preferred (+0.5)

  3. Focus Flow  by LoRoom
     Score: 3.92
     Reasons: genre match (+2.0), energy close to target (+1.42), acoustic, as preferred (+0.5)

  4. Spacewalk Thoughts  by Orbit Bloom
     Score: 2.90
     Reasons: mood match (+1.0), energy close to target (+1.40), acoustic, as preferred (+0.5)

  5. Coffee Shop Stories  by Slow Stereo
     Score: 1.97
     Reasons: energy close to target (+1.47), acoustic, as preferred (+0.5)
```

**Deep Intense Rock** (genre=rock, mood=intense, energy=0.9, likes_acoustic=False)

```
  1. Storm Runner  by Voltline
     Score: 4.98
     Reasons: genre match (+2.0), mood match (+1.0), energy close to target (+1.48), not acoustic, as preferred (+0.5)

  2. Gym Hero  by Max Pulse
     Score: 2.96
     Reasons: mood match (+1.0), energy close to target (+1.46), not acoustic, as preferred (+0.5)

  3. Pulse Reactor  by Kilowatt
     Score: 1.93
     Reasons: energy close to target (+1.43), not acoustic, as preferred (+0.5)

  4. Iron Verdict  by Bleak Meridian
     Score: 1.90
     Reasons: energy close to target (+1.40), not acoustic, as preferred (+0.5)

  5. Sunrise City  by Neon Echo
     Score: 1.88
     Reasons: energy close to target (+1.38), not acoustic, as preferred (+0.5)
```

### Adversarial / edge cases

**Contradictory, energetic but sad** (genre=ambient, mood=sad, energy=0.9, likes_acoustic=True). The mood "sad" is not in the catalog, so it can never match, and a high energy target fights the calm ambient genre.

```
  1. Spacewalk Thoughts  by Orbit Bloom
     Score: 3.07
     Reasons: genre match (+2.0), energy close to target (+0.57), acoustic, as preferred (+0.5)

  2. Storm Runner  by Voltline
     Score: 1.48
     Reasons: energy close to target (+1.48)

  3. Gym Hero  by Max Pulse
     Score: 1.46
     Reasons: energy close to target (+1.46)

  4. Dust and Diesel  by Old Route 9
     Score: 1.43
     Reasons: energy close to target (+0.93), acoustic, as preferred (+0.5)

  5. Pulse Reactor  by Kilowatt
     Score: 1.43
     Reasons: energy close to target (+1.43)
```

Observation: the genre bonus alone lifts a calm ambient track to the top even though it badly misses the requested energy, while the actually high-energy songs the user asked for rank below it. This shows genre can outweigh a strong numeric mismatch.

**Unknown genre** (genre=kpop, mood=happy, energy=0.6, likes_acoustic=False). No song has genre "kpop", so the genre rule never fires and ranking falls back to mood and energy.

```
  1. Rooftop Lights  by Indigo Parade
     Score: 2.76
     Reasons: mood match (+1.0), energy close to target (+1.26), not acoustic, as preferred (+0.5)

  2. Sunrise City  by Neon Echo
     Score: 2.67
     Reasons: mood match (+1.0), energy close to target (+1.17), not acoustic, as preferred (+0.5)

  3. Island Time  by Sunset Groove
     Score: 1.93
     Reasons: energy close to target (+1.43), not acoustic, as preferred (+0.5)

  4. Concrete Poetry  by Verse Machine
     Score: 1.88
     Reasons: energy close to target (+1.38), not acoustic, as preferred (+0.5)

  5. Night Drive Loop  by Neon Echo
     Score: 1.77
     Reasons: energy close to target (+1.27), not acoustic, as preferred (+0.5)
```

Observation: the system degrades gracefully instead of failing. It still returns sensible results by leaning on mood and energy, though every score is capped lower because the 2.0 genre point is unreachable.

**Sparse profile, energy only** (energy=0.5, no genre or mood).

```
  1. Dust and Diesel  by Old Route 9
     Score: 1.47
     Reasons: energy close to target (+1.47)

  2. Island Time  by Sunset Groove
     Score: 1.42
     Reasons: energy close to target (+1.42)

  3. Letters Unsent  by Ava Hollow
     Score: 1.41
     Reasons: energy close to target (+1.41)

  4. Midnight Coding  by LoRoom
     Score: 1.38
     Reasons: energy close to target (+1.38)

  5. Focus Flow  by LoRoom
     Score: 1.35
     Reasons: energy close to target (+1.35)
```

Observation: with only an energy target, every song is judged on that single axis, so the top results are a genre grab bag that happen to sit near energy 0.5. This confirms the profile needs categorical preferences to produce focused recommendations.

### What the stress test revealed

- Genre weight can dominate. In the contradictory profile, one genre match outranked songs that fit the requested energy far better. If genre feels too strong, lower its weight or add a penalty for large numeric mismatches.
- Exact matching is brittle. A mood or genre value that is not in the catalog silently contributes nothing, with no warning to the user.
- The system fails safe. Unknown or sparse profiles still return ranked results rather than crashing, which is good, but the scores are not comparable across profiles because the reachable maximum changes.

---

## Experiments You Tried

### Experiment 1: Weight shift, double energy and halve genre

I temporarily changed the scoring weights in `score_song` to test how sensitive the rankings are to the balance between a categorical feature and a numeric one.

- Genre match, from +2.0 down to +1.0.
- Energy closeness, from up to +1.5 up to +3.0.

Math check: the new maximum score is 1.0 (genre) + 1.0 (mood) + 3.0 (energy) + 0.5 (acoustic) = 5.5, and energy stays bounded between 0 and 3.0 because the closeness factor (1 minus distance) is always between 0 and 1. The math stayed valid, no negative or runaway scores.

What changed:

- For the three normal profiles, the number 1 pick did not change. High-Energy Pop still led with Sunrise City, Chill Lofi with Library Rain, Deep Intense Rock with Storm Runner. Those profiles are internally consistent, their genre, mood, and energy all point at the same song, so shifting weight between the rules could not dislodge the winner. The scores did compress and a few mid list positions swapped.
- The Contradictory profile (genre=ambient, mood=sad, energy=0.9) flipped completely. Under the original weights the top pick was Spacewalk Thoughts, a calm ambient song that won purely on the genre bonus while ignoring the requested high energy. Under the experiment, the genre bonus was no longer big enough to overcome the energy gap, so Spacewalk Thoughts fell out of the top 5 entirely and the high energy songs the user actually asked for (Storm Runner, Gym Hero, Pulse Reactor) rose to the top.

Was it more accurate or just different? For the everyday profiles it was just different, a reshuffle with the same winners. For the adversarial case it was genuinely more accurate, because it fixed the exact failure the stress test exposed, where a single genre match could outrank a strong numeric preference. The tradeoff is that leaning this hard on energy makes the recommender more of an energy matcher and less of a taste matcher, so two songs of very different styles but similar energy start to look interchangeable.

Decision: I reverted to the finalized weights (genre 2.0, energy up to 1.5) to keep genre as the primary taste signal, but this experiment is good evidence that a middle ground, for example genre 1.5 and energy 2.0, or adding a penalty for large numeric mismatches, would make the system more robust to contradictory profiles.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



