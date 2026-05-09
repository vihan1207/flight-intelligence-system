# ============================================
# Flight Data Processing Module
# ============================================
# This module handles data extraction, transformation, and filtering
# of flight information from raw API responses into usable formats.
# It uses pandas for efficient data manipulation and analysis.

import pandas as pd

# Dictionary to map city names to airport IATA codes
# IATA codes are standardized 3-letter airport identifiers used worldwide
# This can be expanded or loaded from a database for scalability in production
city_to_airport = {
    "new york": "JFK",           # John F. Kennedy International Airport
    "los angeles": "LAX",        # Los Angeles International Airport
    "delhi": "DEL",              # Indira Gandhi International Airport
    "mumbai": "BOM",             # Bombay (Mumbai) Maharishi Dadasaheb Airoport
    "tokyo": "NRT",              # Narita International Airport
    "Bangalore": "BLR",          # Kempegowda International Airport
    # Add more cities as needed for expansion
}


def process_flight_data(flights):
    """
    Process raw flight data from the API into a structured pandas DataFrame.
    
    This function performs data extraction and transformation:
    - Extracts essential fields from each flight record
    - Handles missing or incomplete data gracefully
    - Converts raw data into a structured tabular format
    
    Args:
        flights (list): A list of flight data dictionaries from the AviationStack API.
                       Each dictionary contains nested information about departure,
                       arrival, airline, and timing details.
        
    Returns:
        pd.DataFrame: A cleaned DataFrame containing only essential flight information:
                     - departure_airport: IATA code of departure airport
                     - arrival_airport: IATA code of arrival airport
                     - airline: Airline operator name
                     - departure_time: Scheduled departure time
                     - arrival_time: Scheduled arrival time
                     Returns an empty DataFrame if no valid flights are found.
    """
    processed = []
    
    # Step 1: Log the total number of flights received from the API
    # Useful for debugging and understanding data flow
    print(f"[DEBUG] Total flights received from API: {len(flights)}")
    
    # Step 2: Iterate through each flight record and extract relevant information
    # This is a common pattern in data processing: Extract → Transform → Load (ETL)
    for flight in flights:
        try:
            # Extract departure airport IATA code from nested dictionary structure
            # Example: flight["departure"]["iata"] = "JFK"
            departure_airport = flight["departure"]["iata"]
            
            # Extract arrival airport IATA code
            # Example: flight["arrival"]["iata"] = "LAX"
            arrival_airport = flight["arrival"]["iata"]
            
            # Extract airline operator name
            # Example: flight["airline"]["name"] = "United Airlines"
            airline = flight["airline"]["name"]
            
            # Extract scheduled departure time (ISO 8601 format typically)
            # Example: "2026-04-22T10:30:00+00:00"
            departure_time = flight["departure"]["scheduled"]
            
            # Extract scheduled arrival time
            # Example: "2026-04-22T13:45:00+00:00"
            arrival_time = flight["arrival"]["scheduled"]
            
            # Step 3: Create a dictionary with only the essential fields
            # This reduces data size and focuses on relevant information
            processed.append({
                "departure_airport": departure_airport,
                "arrival_airport": arrival_airport,
                "airline": airline,
                "departure_time": departure_time,
                "arrival_time": arrival_time
            })
        except KeyError:
            # Handle missing keys gracefully - some API responses may have incomplete data
            # Rather than crashing, we skip that flight and continue processing
            continue
    
    # Step 4: Convert the list of dictionaries into a pandas DataFrame
    # DataFrames are efficient for filtering, sorting, and aggregation operations
    df = pd.DataFrame(processed)
    
    # Step 5: Log processing results for debugging and monitoring
    print(f"[DEBUG] Flights successfully processed: {len(df)}")
    if df.empty:
        print("[WARNING] No valid flight data found. Check API response structure.")
    
    return df


def filter_flights(df, user_data):
    """
    Filter flight data based on user-specified source and destination cities.
    
    Implements a multi-level matching strategy:
    - Level 1: Exact match (both departure and arrival airports match)
    - Level 2: Partial match (only departure airport matches)
    - Level 3: Fallback (show sample of available flights)
    
    Args:
        df (pd.DataFrame): DataFrame containing processed flight data
        user_data (dict): Dictionary containing user search preferences with keys:
                         'source' (departure city) and 'destination' (arrival city)
                         
    Returns:
        pd.DataFrame: Filtered DataFrame with matching flights, or sample data if no match found
    """
    
    # Step 1: Extract and normalize the source city to lowercase for case-insensitive matching
    source = user_data["source"].lower()
    
    # Step 2: Extract and normalize the destination city to lowercase for case-insensitive matching
    destination = user_data["destination"].lower()
    
    # Debug: Show what user entered
    print(f"\n[DEBUG] User search: {source} → {destination}")
    
    # Step 3: Look up the IATA airport code for the source city from the mapping dictionary
    source_code = city_to_airport.get(source)
    
    # Step 4: Look up the IATA airport code for the destination city from the mapping dictionary
    destination_code = city_to_airport.get(destination)
    
    # Debug: Show airport codes found
    print(f"[DEBUG] Airport codes - Source: {source_code}, Destination: {destination_code}")
    
    # Step 5: Validate that both cities are supported (have corresponding airport codes)
    if not source_code or not destination_code:
        print(f"\n❌ City not supported yet. Please try another city.")
        print(f"   Supported cities: {', '.join(city_to_airport.keys())}")
        # Fallback: Return a sample of available flights to show what's possible
        print("\n   Showing 10 sample flights from the database:\n")
        return df.head(10)
    
    # Debug: Show DataFrame info before filtering
    print(f"[DEBUG] Total flights in DataFrame: {len(df)}")
    if not df.empty:
        print(f"[DEBUG] Available departure airports: {df['departure_airport'].unique().tolist()}")
        print(f"[DEBUG] Available arrival airports: {df['arrival_airport'].unique().tolist()}")
    
    # ============================================
    # MATCHING STRATEGY: Multi-level approach
    # ============================================
    
    # LEVEL 1: Try to find an exact match (both departure and arrival airports match)
    # This is the most specific and preferred result
    exact_match = df[(df["departure_airport"] == source_code) & 
                     (df["arrival_airport"] == destination_code)]
    
    if not exact_match.empty:
        print(f"\n✓ [EXACT MATCH] Found {len(exact_match)} flight(s) on the exact route")
        print(f"[DEBUG] Flights found after filtering: {len(exact_match)}")
        return exact_match
    
    # LEVEL 2: If no exact match, look for partial match (same departure airport)
    # This helps users find alternative destinations from their chosen departure city
    partial_match = df[df["departure_airport"] == source_code]
    
    if not partial_match.empty:
        print(f"\n⚠ [PARTIAL MATCH] No exact route found.")
        print(f"   Showing {len(partial_match)} flight(s) from your departure city ({source} - {source_code})")
        print(f"[DEBUG] Flights found after filtering: {len(partial_match)}")
        return partial_match
    
    # LEVEL 3: Fallback - Show sample of all available flights
    # This demonstrates what flights are available in the system
    print(f"\n⚠ [FALLBACK] No matching routes found from {source}.")
    print("   Showing 10 sample flights available in the system:\n")
    print(f"[DEBUG] Flights found after filtering: 10 (sample)")
    return df.head(10)
