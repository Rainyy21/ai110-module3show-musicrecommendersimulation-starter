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
        """Initializes the recommender with a list of songs."""
        self.songs = songs

    def calculate_score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Calculates a numeric score and point-based reasoning for a single song."""
        score = 0.0
        reasons = []
        
        # 1. Genre Match (+2.0 points)
        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0
            reasons.append(f"genre match (+2.0)")
            
        # 2. Mood Match (+1.0 point)
        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.0
            reasons.append(f"mood match (+1.0)")
        
        # 3. Energy Proximity (Up to 1.0 point)
        energy_diff = abs(song.energy - user.target_energy)
        proximity_score = (1.0 - energy_diff)
        score += proximity_score
        reasons.append(f"energy proximity (+{proximity_score:.2f})")

        # 4. Acousticness Preference (+0.5 point)
        if user.likes_acoustic:
            if song.acousticness > 0.5:
                score += 0.5
                reasons.append(f"acoustic preference (+0.5)")
        else:
            if song.acousticness <= 0.5:
                score += 0.5
                reasons.append(f"non-acoustic preference (+0.5)")
        
        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Tuple[Song, float, List[str]]]:
        """Ranks all catalog songs and returns the top k results sorted by score."""
        scored_songs = []
        for song in self.songs:
            score, reasons = self.calculate_score(user, song)
            scored_songs.append((song, score, reasons))
            
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        return scored_songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Provides a human-readable explanation of why a song was recommended."""
        # This method is now a wrapper for the new point-based system
        _, reasons = self.calculate_score(user, song)
        return "Reasoning: " + ", ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file and returns them as a list of dictionaries.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs = []
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields
                row['id'] = int(row['id'])
                row['energy'] = float(row['energy'])
                row['tempo_bpm'] = float(row['tempo_bpm'])
                row['valence'] = float(row['valence'])
                row['danceability'] = float(row['danceability'])
                row['acousticness'] = float(row['acousticness'])
                songs.append(row)
    except FileNotFoundError:
        print(f"Error: {csv_path} not found.")
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # Map Dict to objects for Recommender class
    song_objects = []
    for s in songs:
        song_objects.append(Song(
            id=s['id'],
            title=s['title'],
            artist=s['artist'],
            genre=s['genre'],
            mood=s['mood'],
            energy=s['energy'],
            tempo_bpm=s['tempo_bpm'],
            valence=s['valence'],
            danceability=s['danceability'],
            acousticness=s['acousticness']
        ))
    
    user_profile = UserProfile(
        favorite_genre=user_prefs.get('genre', ''),
        favorite_mood=user_prefs.get('mood', ''),
        target_energy=user_prefs.get('energy', 0.5),
        likes_acoustic=user_prefs.get('likes_acoustic', False)
    )
    
    recommender = Recommender(song_objects)
    recommended_with_scores = recommender.recommend(user_profile, k)
    
    results = []
    for song_obj, score, reasons in recommended_with_scores:
        # Find the original dict for this song
        original_dict = next(s for s in songs if s['id'] == song_obj.id)
        explanation = "Reasoning: " + ", ".join(reasons)
        results.append((original_dict, score, explanation))
        
    return results
