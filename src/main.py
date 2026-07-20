"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


# Profiles used to stress test the recommender.
# The first three are "normal" listener archetypes. The last three are
# adversarial / edge cases designed to try to trick the scoring logic.
PROFILES = [
    # --- Normal archetypes ---
    ("High-Energy Pop",
     {"genre": "pop", "mood": "happy", "energy": 0.9, "likes_acoustic": False}),
    ("Chill Lofi",
     {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True}),
    ("Deep Intense Rock",
     {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False}),

    # --- Adversarial / edge cases ---
    # Conflicting signals: wants high energy but a low-energy "sad" mood that
    # does not exist in the catalog, so mood can never match.
    ("Contradictory (energetic but sad)",
     {"genre": "ambient", "mood": "sad", "energy": 0.9, "likes_acoustic": True}),
    # Genre that is not in the catalog at all: the genre rule can never fire,
    # so ranking must fall back entirely to mood and energy.
    ("Unknown Genre (kpop)",
     {"genre": "kpop", "mood": "happy", "energy": 0.6, "likes_acoustic": False}),
    # Sparse profile: only an energy target, no genre or mood preference.
    ("Sparse (energy only)",
     {"energy": 0.5}),
]


def print_recommendations(name: str, user_prefs: dict, songs: list) -> None:
    """Print the top 5 recommendations for one named profile."""
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print()
    print("=" * 60)
    print(f"  Profile: {name}")
    print(f"  Prefs: {user_prefs}")
    print("=" * 60)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  {rank}. {song['title']}  by {song['artist']}")
        print(f"     Score: {score:.2f}")
        print(f"     Reasons: {explanation}")

    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES:
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
