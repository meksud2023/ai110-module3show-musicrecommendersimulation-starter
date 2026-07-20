# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

It matches songs to a listener's vibe. The name is meant to be simple and fun.

---

## 2. Intended Use  

VibeMatch tries to suggest songs a listener will like. It takes a short taste profile and returns a ranked list of songs that fit it. It also gives a short reason for each pick, so the choice is easy to understand.

It assumes the user can name a favorite genre, a favorite mood, and an energy level. It works on a tiny catalog of 18 songs.

**Intended use:** this is a classroom project. It is for learning how a simple recommender turns data into ranked suggestions.

**Not intended use:** it is not for real music apps or real users. It should not be used to make important choices about people or to judge music quality. The catalog is too small and the rules are too simple for that.

---

## 3. How the Model Works  

The model gives each song a score, then sorts the songs from highest to lowest. The top few become the recommendations.

To score a song, it compares the song to the user's profile and adds points for good matches.

- Same genre as the user likes, add 2 points.
- Same mood as the user likes, add 1 point.
- Energy close to the user's target, add up to 1.5 points. Closer means more points.
- Matches the acoustic preference, add half a point.

The energy rule is the important idea. It does not reward loud songs or quiet songs. It rewards songs that are close to the energy the user asked for. So being close is what earns points, not being high or low.

Every point comes with a short reason, like "genre match" or "energy close to target". That way the user can see why a song was picked. The main change from the starter code was writing the scoring and ranking rules, which were empty at the start.

---

## 4. Data  

The catalog is a small CSV file with 18 songs. I started with 10 songs and added 8 more to get more variety.

Each song has these features: id, title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. The model only uses genre, mood, energy, and acousticness for now.

There are 15 genres and 14 moods. But most of them appear only once. Only lofi (3 songs) and pop (2 songs) show up more than once.

A lot of real musical taste is missing. The catalog is tiny, it leans toward calm and electronic styles, and it has no lyrics, no language, and no info about song quality or popularity.

---

## 5. Strengths  

The system works well when the user's profile is clear and consistent. A chill lofi fan gets calm lofi songs. A rock fan gets loud rock songs. The top pick usually feels right.

It captures the energy idea well. It matches songs to the energy the user wants, instead of just picking the loudest song.

It is easy to understand. Every pick comes with a reason, so you can always see why a song was chosen. It also fails safely. Even with a weird or empty profile, it still returns a ranked list instead of crashing.

---

## 6. Limitations and Bias 

The clearest weakness I found is a representation bias baked into the catalog that the scoring logic then amplifies. Of the 15 genres in the 18 song dataset, only lofi (3 songs) and pop (2 songs) appear more than once, while the other 13 genres each have a single song. Because the genre rule in `score_song` only awards its +2.0 for an exact match, a lofi or pop fan can collect that top bonus on several songs, but a metal, jazz, or country fan can earn it on exactly one, so the rest of their top 5 is padded with energy only matches that ignore their actual taste. This is a filter bubble driven by data composition: users whose taste happens to be well represented get rich, genre aligned recommendations, while niche genre users quietly get a weaker, less personalized list even though the code treats everyone with the same rules. Two further limitations make this worse: the exact match rule gives zero credit for closely related styles, for example metal for a rock fan, and the profile only uses four features, so it never considers valence, tempo, or danceability, which means two very different songs at the same energy can look identical to the system.

---

## 7. Evaluation  

I tested the recommender with six user profiles and read the top 5 songs it returned for each. Three were normal listeners: High-Energy Pop (upbeat pop fan), Chill Lofi (calm study music fan), and Deep Intense Rock (loud rock fan). Three were tricky edge cases: Contradictory (asks for calm ambient but also very high energy), Unknown Genre (likes a genre that is not in the catalog at all), and Sparse (only says how much energy they want, nothing else). For each one I looked at whether the top songs actually fit the request and whether the reasons the system printed made sense.

What surprised me most was how often a song rode in on energy and genre even when its mood was wrong. The best example is the High-Energy Pop profile, where the person asked for happy pop, but the song Gym Hero keeps showing up near the top. In plain terms, the system gives points for three things here: the song being pop, the song being close to the requested energy level, and the mood matching. Gym Hero is pop and it is very high energy, so it collects most of the available points, and it only misses out on the happy mood bonus. Missing one small bonus is not enough to push it down, so a loud workout song lands right next to the genuinely happy pop songs, even though a person expecting cheerful music might find it too aggressive.

Comparisons between pairs of profiles:

- High-Energy Pop vs Chill Lofi: These are near opposites and the outputs cleanly separate. The pop fan gets fast, upbeat, non acoustic songs like Sunrise City and Gym Hero, while the lofi fan gets slow, quiet, acoustic songs like Library Rain and Midnight Coding. This makes sense because their energy targets sit at opposite ends and they prefer opposite acoustic settings, so almost no song scores well for both.

- High-Energy Pop vs Deep Intense Rock: Both want high energy, and you can see that overlap because Gym Hero and Storm Runner appear in both lists. The difference is the genre and mood anchor, so the pop fan is led by Sunrise City (pop and happy) while the rock fan is led by Storm Runner (rock and intense). This shows energy pulls in similar loud songs for both, and genre plus mood is what finally separates them.

- Deep Intense Rock vs Contradictory: The rock fan gets a clear, satisfying top pick in Storm Runner because genre, mood, and energy all agree. The Contradictory profile instead gets Spacewalk Thoughts first, a calm ambient song, even though the user also asked for high energy. This happens because the genre bonus for ambient is large enough to beat the energy mismatch, which is exactly the kind of confusing result that appears when a user gives conflicting signals.

- Chill Lofi vs Contradictory: Both profiles say they like acoustic music, so calm acoustic songs show up in both, but the lofi fan gets a tightly focused list of actual lofi tracks while the Contradictory fan gets a scattered list. The reason is that the lofi profile is internally consistent, so its preferences all point at the same handful of songs, while the contradictory profile pulls in different directions and ends up with weaker, lower scoring matches.

- Unknown Genre vs Sparse: Neither profile can earn the genre bonus, the first because kpop is not in the catalog and the second because no genre was given, so both fall back to mood and energy. The Unknown Genre fan still does a little better because the happy mood bonus can fire, so happy songs like Rooftop Lights rise up, while the Sparse profile ranks purely on energy and returns a random looking mix of styles that simply sit near the requested energy level.

- High-Energy Pop vs Unknown Genre: Both ask for happy, non acoustic music, but the pop fan names a genre that exists and the kpop fan does not. The result is that the pop fan gets a stronger, higher scoring list led by a true genre match, while the kpop fan gets a reasonable but weaker list where the top songs win only on mood and energy. This shows the system fails safely, it still returns sensible happy songs, but naming a real genre clearly produces better, more confident recommendations.

Overall the tests told me the top pick is usually valid when a profile is consistent, the middle of the list is where questionable songs sneak in on energy alone, and conflicting or unknown inputs are handled without crashing but with visibly weaker results.

---

## 8. Future Work  

- Give partial credit for similar styles. Right now metal earns nothing for a rock fan. It should earn some points because the styles are close.
- Use more features. The songs already have tempo, valence, and danceability, but the profile ignores them. Adding them would tell similar songs apart.
- Grow and balance the catalog. More songs per genre would give every user more real matches, not just lofi and pop fans.

---

## 9. Personal Reflection  

My biggest learning moment was seeing that a recommender is just a scoring rule and a sort, and that the weights quietly decide everything.

The AI tools helped me write and explain the code fast, but I had to double-check the math and the rankings myself, since I could not trust the output until I ran it.

What surprised me was how simple points and sorting can still feel like real recommendations, even with only a few rules.

If I kept going, I would add more features like tempo and valence, give partial credit for similar genres, and grow the catalog so every user gets fair matches.
