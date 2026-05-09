# ============================================================================
# FLIGHT INTELLIGENCE SYSTEM - MAIN ORCHESTRATION MODULE
# ============================================================================
# 
# PURPOSE: Central coordinator for the flight search and recommendation system
# 
# ARCHITECTURE PATTERN: Pipeline Architecture with Error Handling
# - Implements modular data pipeline (fetch → process → filter → rank → export)
# - Each stage is independent and testable
# - Robust error handling at critical points
# 
# KEY FEATURES FOR INTERVIEWS:
# 1. Clean separation of concerns (api/, processor/, intelligence/, visualization/)
# 2. Defensive programming practices (early validation, informative error messages)
# 3. Weighted scoring algorithm for intelligent recommendations
# 4. Comprehensive data validation between pipeline stages
# 5. Graceful error handling (continues execution where possible)
# 6. Well-documented decisions and trade-offs
# 
# ============================================================================

# Import the required libraries and modules
from input.user_input import get_user_input
from api.flight_api import fetch_flight_data
from processor.data_processor import process_flight_data, filter_flights
from processor.duration_calculator import calculate_duration
from intelligence.recommendation_engine import recommend_flights
from visualization.output_formater import display_flights, get_top_flights, rank_flights
from visualization.flight_visualizer import plot_price_distribution, plot_airline_prices, plot_duration_vs_price, generate_insights, display_insights
from data.data_saver import save_to_csv, save_to_excel


def main():
    """
    Main function to orchestrate the flight search system.
    
    ARCHITECTURAL PATTERN: Pipeline Architecture
    - Implements a data pipeline with clear separation of concerns
    - Each step (fetch → process → filter → calculate → recommend → visualize) is independent
    - This design allows easy testing, debugging, and adding new features
    
    WORKFLOW STEPS:
    1. Collect user input (source and destination cities)
    2. Fetch flight data from AviationStack API (external data source)
    3. Process and clean raw flight data into structured DataFrame
    4. Filter flights based on user's route preferences
    5. Calculate flight duration metrics from timestamps
    6. Apply AI recommendation engine (weighted scoring algorithm)
    7. Generate visualizations and market insights
    8. Export results to CSV/Excel for user records
    
    ERROR HANDLING STRATEGY:
    - Validates API response before processing (defensive programming)
    - Checks for empty results at each stage to catch data issues early
    - Wraps complex operations in try-catch blocks for graceful failure
    - Continues execution where possible to provide partial results
    - Uses informative error messages to help users troubleshoot issues
    
    DESIGN PATTERNS USED:
    - Pipeline Pattern: Sequential data transformation stages
    - Defensive Programming: Validate assumptions at each step
    - Fail-Fast Pattern: Check for errors early and stop gracefully
    - Separation of Concerns: Business logic in separate modules (api/, processor/, intelligence/)
    """
    
    # ===== STEP 1: Collect User Input =====
    # Defensive Programming: Get user preferences as the first step
    # This ensures we know WHAT to search for before making expensive API calls
    # Early validation prevents wasted API quota on invalid search parameters
    print("Starting Flight Intelligence System...\n")
    user_data = get_user_input()
    
    # Step 2: Display the collected user preferences for confirmation
    # IMPORTANT: Echo back user input to catch mistakes early
    # Users can verify their selections are correct before we proceed with expensive API calls
    print("\n" + "="*50)
    print("User Search Preferences:")
    print("="*50)
    print(f"Source: {user_data.get('source', 'N/A')}")
    print(f"Destination: {user_data.get('destination', 'N/A')}")
    if 'preferences' in user_data:
        print(f"Additional Preferences: {user_data['preferences']}")
    print("="*50)
    
    # ===== STEP 3: Fetch Flight Data from API =====
    # API Integration Point: Makes actual network request
    # Failure Point 1: This is where external system failures are most likely
    # We validate response immediately before proceeding further
    # BEST PRACTICE: Always validate external API data before processing
    print("\n" + "="*50)
    print("Fetching flight data from the API...")
    print("="*50)
    flights = fetch_flight_data()
    
    # Validate that we received flight data from the API
    if not flights:
        print("\n⚠ No flight data available. Please check your API key and network connection.")
        print("Exiting application.")
        return
    
    # Step 4: Display the number of flights fetched and show sample raw data
    # This helps verify that the API connection is working and data structure is correct
    print(f"\n✓ Total Flights Fetched from API: {len(flights)}")
    print("\nSample Raw Flight Data (First 3 flights):")
    print("-" * 50)
    for i, flight in enumerate(flights[:3], 1):
        print(f"{i}. {flight}")
    
    # Step 5: Process the raw flight data into a structured DataFrame
    # Extracts only essential fields (airline, price, routes, timestamps)
    # Handles missing data and data type conversions for DataFrame operations
    # Returns: pandas DataFrame with cleaned and structured flight data
    print("\n" + "="*50)
    print("Processing flight data...")
    print("="*50)
    df = process_flight_data(flights)
    
    # Verify that essential columns exist after processing
    # This debugging step helps identify missing data early in the pipeline
    print(f"\n✓ Columns after processing: {list(df.columns)}")
    if 'price' not in df.columns:
        print("\n⚠ Warning: 'price' column not found in processed data!")
        print("Available columns:", list(df.columns))
        print("Adding placeholder 'price' column with default values...")
        df['price'] = 0  # Add default price column if missing
    if 'airline' not in df.columns:
        print("\n⚠ Warning: 'airline' column not found in processed data!")
        df['airline'] = 'Unknown'  # Add default airline if missing
    
    # ===== STEP 6: Filter Flights Based on User Preferences =====
    # Data Pipeline Stage: Filter relevant data from the dataset
    # INPUT: df (all processed flights), user_data (source & destination)
    # LOGIC: Matches user-selected cities with airport codes, removes irrelevant flights
    # OUTPUT: Filtered DataFrame with only flights matching user's route
    # PERFORMANCE: Reduces data size for next stages (duration calc, AI ranking)
    print("\nFiltering flights based on user input...")
    filtered_df = filter_flights(df, user_data)
    
    # Verify that price column is preserved after filtering
    if filtered_df is not None and not filtered_df.empty:
        print(f"✓ Columns after filtering: {list(filtered_df.columns)}")
        if 'price' not in filtered_df.columns and 'price' in df.columns:
            print("⚠ Warning: 'price' column lost during filtering - restoring...")
            # Restore price column if it was lost during filtering
            filtered_df['price'] = df.loc[filtered_df.index, 'price']
    
    # Check if the filtering was successful and flights were found
    if filtered_df is None:
        print("\n❌ Filtering failed. Please check your city selection.")
        return
    
    if filtered_df.empty:
        print(f"\n⚠ No flights found between {user_data['source']} and {user_data['destination']}.")
        print("Try different cities or check flight availability.")
        return
    
    # Step 7: Calculate flight duration for each filtered flight
    # Converts departure and arrival ISO format timestamps into duration_hours column
    # This metric is used later in the AI recommendation algorithm (30% weight)
    print("\nCalculating flight durations for all flights...")
    filtered_df = calculate_duration(filtered_df)
    
    # Verify that duration was calculated and price is still available
    print(f"✓ Columns after duration calculation: {list(filtered_df.columns)}")
    if 'price' not in filtered_df.columns:
        print("\n⚠ Warning: 'price' column missing after duration calculation!")
        print("This will affect visualization output.")
    
    # Step 8: Display the final filtered and processed results to the user
    # Shows all matching flights in a formatted table with all relevant information
    # This provides transparency before AI ranking is applied
    print("\n" + "="*50)
    print("Search Results:")
    print("="*50)
    
    # Display the matching flights in a formatted table
    print(f"\n✓ Found {len(filtered_df)} matching flight(s):\n")
    print(filtered_df.to_string(index=False))
    
    # ===== STEP 9: Apply AI-Based Recommendation Engine =====
    # ALGORITHM EXPLANATION (Interview Talking Point):
    # This implements a WEIGHTED SCORING MODEL to rank flights
    # 
    # Scoring Factors:
    #   1. Flight Duration (30% weight): Shorter flights ranked higher for convenience
    #   2. Airline Reputation (20% weight): Better airlines scored higher for reliability
    #   3. Price Normalization: Prevents expensive flights from dominating scoring
    # 
    # Formula: ai_score = (normalized_airline_score × 0.2) + (normalized_duration × 0.3)
    # 
    # WHY THIS APPROACH:
    # - Weighted scoring balances multiple factors vs. single metric
    # - Normalization ensures fair comparison across different price ranges
    # - Extensible: Easy to add new factors or adjust weights
    # 
    # ALTERNATIVE APPROACH: Could use machine learning (clustering/regression)
    # but this rule-based approach is more interpretable for users
    print("\n" + "="*50)
    print("AI-Powered Flight Recommendations:")
    print("="*50)
    
    try:
        # Apply the recommendation engine to score and rank flights
        # Pass a copy to avoid modifying the original filtered_df
        recommended_df = recommend_flights(filtered_df.copy())
        
        # Verify price column is available after recommendation
        print(f"\n✓ Columns after AI recommendation: {list(recommended_df.columns)}")
        if 'price' not in recommended_df.columns and 'price' in filtered_df.columns:
            print("⚠ Note: Restoring 'price' column from original data...")
            recommended_df['price'] = filtered_df.loc[recommended_df.index, 'price']
        
        # Verify that the AI scoring was successful by checking for ai_score column
        if 'ai_score' not in recommended_df.columns:
            print("\n⚠ Warning: AI recommendation scoring failed.")
            print("Using filtered flights without AI ranking.")
            # IMPORTANT: Don't return here - continue with filtered_df for export
            recommended_df = filtered_df
        else:
            # Display top 5 recommended flights with key metrics
            print("\n✓ Top 5 Recommended Flights (Ranked by AI Score):\n")
            
            # Dynamically determine which columns to display based on available columns
            # This makes the code robust to missing data or different data structures
            available_cols = recommended_df.columns.tolist()
            preferred_display_cols = ['airline', 'price', 'duration_hours', 'ai_score']
            
            # Filter to only show columns that actually exist in the DataFrame
            # This prevents KeyError exceptions if some columns are missing
            display_cols = [col for col in preferred_display_cols if col in available_cols]
            
            # Display the available columns with top 5 recommendations
            if display_cols:
                print(recommended_df[display_cols].head(5).to_string(index=False))
            else:
                print("No suitable columns found for display.")
                print("Available columns:", available_cols)
        
    except Exception as e:
        # Handle any errors in the recommendation engine gracefully
        # Catches and displays error message without crashing the application
        print(f"\n⚠ Error during AI recommendation: {str(e)}")
        print("Using filtered flights for export instead.")
        # Don't return - use filtered_df for export
        recommended_df = filtered_df
    
    # Step 10: Apply alternative ranking algorithm for visualization
    # This uses a different weighting scheme (60% price, 40% duration)
    # compared to the AI recommendation (30% duration, 20% airline reputation)
    # Useful for comparing different ranking perspectives
    print("\n" + "="*50)
    print("Alternative Ranking (Price & Duration Focused):")
    print("="*50)
    
    try:
        # Rank flights using the visualization module's scoring algorithm
        # This emphasizes price more heavily (60% vs other factors)
        # Useful for budget-conscious travelers
        ranked_df = rank_flights(recommended_df.copy())
        
        # Extract the top 5 best-ranked flights
        # get_top_flights() filters the DataFrame to return only top N rows
        top_flights = get_top_flights(ranked_df, top_n=5)
        
        # Display flights in a user-friendly formatted output
        # display_flights() formats each flight's details in an attractive tabular format
        # Shows: airline, route, times, duration, price, and ranking score
        display_flights(top_flights)
        
    except Exception as e:
        # Handle errors gracefully in the visualization pipeline
        # Don't return - continue to export step
        print(f"\n⚠ Error during alternative ranking: {str(e)}")
        print("Skipping alternative ranking display - will proceed with export.")
    
    # Step 11: Generate market visualizations and insights from recommended flights
    # These visualizations help users understand pricing trends, airline comparisons,
    # and the relationship between flight duration and price
    # Using recommended_df ensures visualizations reflect the user's search context
    print("\n" + "="*50)
    print("Generating Market Visualizations and Insights...")
    print("="*50)
    
    try:
        # Debug: Show what data we're trying to visualize
        print(f"\n📋 Data Summary for Visualization:")
        print(f"   - Total flights: {len(recommended_df)}")
        print(f"   - Columns: {list(recommended_df.columns)}")
        print(f"   - Data shape: {recommended_df.shape}")
        
        # Generate visualizations based on recommended flight data
        # This provides insights specifically for the user's search route
        # Charts will be DISPLAYED on screen and SAVED to the visualization/charts folder
        print("\n📊 Generating charts...")
        plot_price_distribution(recommended_df)
        plot_airline_prices(recommended_df)
        plot_duration_vs_price(recommended_df)
        print("\n✓ All visualization charts generated and displayed successfully!")
        print("💾 Charts are also saved in: visualization/charts/ directory")
        
        # Generate and display key insights from the flight data
        # Includes: cheapest/most expensive flights, fastest/slowest flights, average price
        print("\n📈 Generating insights...")
        insights = generate_insights(recommended_df)
        if insights:
            display_insights(insights)
        else:
            print("⚠ No insights generated - check the flight data.")
        
    except Exception as e:
        # Handle visualization errors gracefully
        # Continue to export step even if visualization fails
        print(f"\n⚠ Error generating visualizations: {str(e)}")
        print("Continuing to export results...")
    
    # Step 12: Export recommended flight results to CSV and Excel files
    # Saves the final AI-recommended flights (not raw data) for user records and further analysis
    # This allows users to share results with colleagues or import into other tools
    # Files are timestamped to prevent overwriting previous search results
    print("\n" + "="*50)
    print("Exporting Results...")
    print("="*50)
    
    try:
        # Save the final recommended flights (filtered, calculated, and AI-ranked)
        # NOT the raw data - users want to keep the results they found, not all flights
        # recommended_df contains: airline, price, duration_hours, ai_score, and route info
        save_to_csv(recommended_df)
        save_to_excel(recommended_df)
        print("✓ Results successfully exported to CSV and Excel formats")
    except Exception as e:
        # Handle export errors gracefully without crashing the application
        print(f"\n⚠ Warning: Could not export results - {str(e)}")
        print("Search completed but files were not saved.")
    
    # Final completion message
    print("\n" + "="*50)
    print("✓ Flight Intelligence System completed successfully!")
    print("="*50 + "\n")

# Entry point: Check if this script is run directly (not imported as a module)
# This pattern allows this file to be imported as a module without running main() automatically
if __name__ == "__main__":
    # Call the main function to start the application
    main()
