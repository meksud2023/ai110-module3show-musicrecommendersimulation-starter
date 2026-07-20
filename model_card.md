# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
