import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file into a list of dictionaries.

    Numeric columns are converted from strings to numbers so they can be
    used in scoring math later: id and tempo_bpm become ints, and the
    audio features (energy, valence, danceability, acousticness) become floats.

    Required by src/main.py
    """
    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song: Dict = {}
            for key, value in row.items():
                if key in int_fields:
                    song[key] = int(value)
                elif key in float_fields:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against the user's preferences.

    Algorithm Recipe (see README, How The System Works):
      - Genre match     +2.0   (exact match, strongest signal)
      - Mood match      +1.0   (exact match, softer signal)
      - Energy closeness up to +1.5, rewards being CLOSE to the target,
                                 not simply having high energy
      - Acoustic pref   +0.5   (optional, light tie breaker)

    Returns a tuple of (score, reasons), where reasons is a list of short
    strings such as "genre match (+2.0)" so the recommendation can be explained.
    Maximum possible score is 5.0.
    """
    score = 0.0
    reasons: List[str] = []

    # Rule 1 - Genre match (weight 2.0)
    if user_prefs.get("genre") is not None and song.get("genre") == user_prefs["genre"]:
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Rule 2 - Mood match (weight 1.0)
    if user_prefs.get("mood") is not None and song.get("mood") == user_prefs["mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Rule 3 - Energy closeness (up to 1.5): closer to target = more points
    target_energy = user_prefs.get("energy")
    if target_energy is not None:
        distance = abs(song["energy"] - target_energy)      # both on a 0..1 scale
        energy_points = (1 - distance) * 1.5
        score += energy_points
        reasons.append(f"energy close to target (+{energy_points:.2f})")

    # Rule 4 - Acoustic preference (weight 0.5), only if the profile expresses one
    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is True and song["acousticness"] >= 0.6:
        score += 0.5
        reasons.append("acoustic, as preferred (+0.5)")
    elif likes_acoustic is False and song["acousticness"] < 0.4:
        score += 0.5
        reasons.append("not acoustic, as preferred (+0.5)")

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Ranks the whole catalog and returns the top k recommendations.

    Steps:
      1. Judge every song with score_song (the scoring loop).
      2. Sort all scored songs from highest to lowest score.
      3. Keep the top k and turn each song's reasons into an explanation.

    Returns a list of (song_dict, score, explanation) tuples.
    Required by src/main.py
    """
    # 1. Score every song. Build (song, score, explanation) up front so the
    #    reasons collected during scoring travel with the result.
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "no strong matches"
        scored.append((song, score, explanation))

    # 2. Sort by score, highest first. item[1] is the score in each tuple.
    scored.sort(key=lambda item: item[1], reverse=True)

    # 3. Return only the top k.
    return scored[:k]
