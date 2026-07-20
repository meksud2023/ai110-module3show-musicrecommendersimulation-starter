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

Running `python -m src.main` with the default profile (genre=pop, mood=happy, energy=0.8) produces the following:

```
Loaded songs: 18

====================================================
  Top Recommendations
  Profile: genre=pop, mood=happy, energy=0.8
====================================================

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

The top result, Sunrise City, is the only song that matches the profile on genre, mood, and energy at once, so it correctly earns the highest score.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

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



