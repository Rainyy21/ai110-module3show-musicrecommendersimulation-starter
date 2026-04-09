# Model Card: MoodFinder 1.0

## Model Name
**MoodFinder 1.0** (The "Judge and Sort" Music Recommender)

## Goal / Task
The goal of MoodFinder 1.0 is to suggest a ranked list of the top 5 songs from a music catalog that best align with a user's stated preferences. It aims to balance a user's long-term identity (Genre) with their immediate context (Mood and Energy).

## Data Used
*   **Dataset Size:** 18 songs (10 starter tracks + 8 diverse additions).
*   **Features:** id, title, artist, genre, mood, energy (0.0–1.0), tempo_bpm, valence, danceability, acousticness (0.0–1.0).
*   **Limits:** The dataset is "wide but shallow," meaning it covers many genres but only has one or two examples for each, which can lead to repetitive results if the user's profile is very specific.

## Algorithm Summary
MoodFinder 1.0 uses a **Point-Based Scoring Rule** followed by a **Descending Ranking Rule**:
1.  **Genre Match (+2.0 pts):** Rewards songs in the user's favorite category.
2.  **Mood Match (+1.0 pt):** Rewards songs that match the user's current emotional state.
3.  **Energy Proximity (Up to 1.0 pt):** Uses a linear decay formula (`1.0 - abs(diff)`) to reward songs with an energy level close to the user's target.
4.  **Acoustic Preference (+0.5 pt):** A binary check that rewards songs above or below a 0.5 acousticness threshold based on user preference.

## Observed Behavior / Biases
*   **Genre Dominance:** The +2.0 weight for Genre is the strongest factor. This creates a "Filter Bubble" where a poorly fitting song in the "right" genre will often outrank a perfect match in the "wrong" genre.
*   **Semantic Rigidity:** The system requires exact string matches. If a user inputs "Joyful" but the database uses "Happy," the match fails (0 points).
*   **Linear Energy Gap:** The linear proximity calculation slightly favors "average" energy profiles (0.5) over extreme ones (0.0 or 1.0) because mid-range songs are mathematically "closer" to more of the catalog.

## Evaluation Process
The system was validated through three primary methods:
1.  **Adversarial Testing:** Evaluated 4 edge-case profiles (The Contradictory User, The Ghost User, The Extreme Minimalist, and The Specific Specialist) to observe how the scoring logic "breaks" or defaults.
2.  **Manual Math Verification:** Step-by-step point audits were performed on specific songs (e.g., "Iron Will" and "Gym Hero") to ensure the implementation matched the theoretical recipe.
3.  **Automated Unit Tests:** Used `pytest` to confirm that the sorting and selection logic remained consistent across code changes.

## Intended Use and Non-Intended Use
*   **Intended Use:** Small-scale personal music discovery, teaching basic recommendation logic, and demonstrating the "Judge and Sort" pattern.
*   **Non-Intended Use:** Large-scale commercial streaming services, professional DJ software, or any application requiring deep content-based analysis (like waveform or lyric sentiment analysis).

## Ideas for Improvement
1.  **Semantic Mapping:** Integrate a thesaurus or NLP library to allow "Happy" to match "Joyful" or "Cheerful."
2.  **Gaussian Proximity:** Use a Bell Curve (Gaussian) for energy proximity so that "near-perfect" matches are rewarded much more heavily than "close" matches.
3.  **Diversity Filter:** Implement a ranking rule that prevents more than two songs from the same artist from appearing in the Top 5.
