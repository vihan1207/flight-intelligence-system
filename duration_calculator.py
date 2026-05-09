# Import required libraries for datetime operations
from datetime import datetime

# Function to calculate flight duration between departure and arrival times
def calculate_duration(df):
    """
    Calculates flight duration in hours for each flight record.
    
    Args:
        df: DataFrame with 'departure_time' and 'arrival_time' columns in ISO format
        
    Returns:
        DataFrame with added 'duration_hours' column containing flight durations
    """
    durations = []
    
    # Iterate through each row in the dataframe
    for index, row in df.iterrows():
        try:
            # Extract departure and arrival times from the current row
            dep_time = row["departure_time"]
            arr_time = row["arrival_time"]
            
            # Skip rows with missing or invalid time values
            if dep_time is None or arr_time is None:
                durations.append(None)
                continue
            
            # Convert ISO format datetime strings to datetime objects
            # Replace 'Z' timezone indicator with '+00:00' for proper parsing
            dep_time = datetime.fromisoformat(dep_time.replace("Z", "+00:00"))
            arr_time = datetime.fromisoformat(arr_time.replace("Z", "+00:00"))
            
            # Calculate the time difference between arrival and departure
            duration_timedelta = arr_time - dep_time
            
            # Convert the duration from seconds to hours (3600 seconds = 1 hour)
            duration_hours = duration_timedelta.total_seconds() / 3600
            
            # Append the rounded duration (2 decimal places) to the list
            durations.append(round(duration_hours, 2))
            
        except Exception as e:
            # Handle any errors during processing and log them for debugging
            print(f"Error calculating duration for row {index}: {e}")
            durations.append(None)
    
    # Add the calculated durations as a new column to the dataframe
    df["duration_hours"] = durations
    return df 

