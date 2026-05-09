# Function to rank and score flights based on weighted criteria
def rank_flights(df):
    """
    Rank flights based on a weighted combination of price and duration.
    
    Algorithm:
    - Normalizes price and duration to 0-1 range
    - Calculates composite score: 60% price weight + 40% duration weight
    - Lower scores are better (shorter flights + lower prices preferred)
    
    Args:
        df (pandas.DataFrame): DataFrame containing flight data with 'duration_hours' 
                              and 'normalized_price' columns
    
    Returns:
        pandas.DataFrame: DataFrame sorted by score (ascending, lower is better)
    """
    
    # Step 1: Normalize flight duration to 0-1 range for fair comparison
    # Formula: (value - min) / (max - min + epsilon)
    # Epsilon (1e-6) prevents division by zero if all durations are equal
    duration_range = df["duration_hours"].max() - df["duration_hours"].min()
    df["normalized_duration"] = (
        (df["duration_hours"] - df["duration_hours"].min()) / (duration_range + 1e-6)
    )
    # Step 2: Calculate composite score using weighted average
    # Score = (0.6 * normalized_price) + (0.4 * normalized_duration)
    # Weights: 60% for price (price is more important), 40% for duration
    # Lower scores indicate better flights (cheaper and shorter)
    df["score"] = (0.6 * df["normalized_price"] + 0.4 * df["normalized_duration"])
    # Step 3: Sort by score in ascending order (lower scores = better flights)
    # ascending=True ensures best flights (lowest scores) appear first
    ranked_df = df.sort_values(by="score", ascending=True)
    
    return ranked_df


# Function to extract top N flights from the ranking
def get_top_flights(df, top_n=5):
    """
    Extract the top N best-ranked flights from DataFrame.
    
    Args:
        df (pandas.DataFrame): DataFrame sorted by flight ranking/score
        top_n (int): Number of top flights to return (default: 5)
    
    Returns:
        pandas.DataFrame: DataFrame containing only top N flights
    """
    return df.head(top_n)
# Function to display flights in an attractive, user-friendly format
def display_flights(df):
    """
    Format and display flight recommendations in a readable tabular format.
    
    Features:
    - Shows key flight information (airline, route, times, duration, price, score)
    - Rounds numerical values for better readability
    - Displays one flight per numbered entry
    
    Args:
        df (pandas.DataFrame): DataFrame containing flights to display
    """
    print("\n" + "=" * 70)
    print("Top Flight Recommendations - Ranked by Price and Duration")
    print("=" * 70)
    
    # Iterate through each flight in the DataFrame
    for i, row in df.iterrows():
        # Extract and format flight information
        flight_num = i + 1  # User-friendly flight numbering (starts from 1)
        airline = row.get("airline", "N/A")  # Handle missing airline gracefully
        departure_airport = row.get("departure_airport", "N/A")
        arrival_airport = row.get("arrival_airport", "N/A")
        departure_time = row.get("departure_time", "N/A")
        arrival_time = row.get("arrival_time", "N/A")
        duration_hours = round(row.get("duration_hours", 0), 2)  # Round to 2 decimals
        price = int(row.get("price", 0))  # Convert to integer for cleaner display
        score = round(row.get("score", 0), 3)  # Round to 3 decimals
        
        # Display formatted flight details
        print(f"""
Flight {flight_num}
{'-' * 70}
Airline:           {airline}
Route:             {departure_airport} → {arrival_airport}
Departure Time:    {departure_time}
Arrival Time:      {arrival_time}
Duration:          {duration_hours} hours
Price:             ₹{price}
Ranking Score:     {score} (lower is better)
{'-' * 70}""")
        