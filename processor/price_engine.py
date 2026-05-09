# Import required libraries for numerical operations and datetime handling
import numpy as np
from datetime import datetime
import pandas as pd

# ============================================================================
# FLIGHT PRICING ENGINE
# ============================================================================
# This module implements a dynamic pricing system for flights based on:
# - Flight duration (base cost factor)
# - Airline brand value (premium vs budget)
# - Peak hour demand multiplier
# - Random market fluctuations
#
# Use Cases:
# 1. simulate_price(): Calculate realistic flight prices
# 2. normalize_price(): Scale prices for ML models and comparisons
# ============================================================================

# Dictionary mapping airline names to their pricing multipliers
# Premium airlines (Qatar, Singapore) have higher multipliers, budget airlines (AirAsia) have lower
airline_factor = {
    "Qatar Airways": 1.8,
    "Singapore Airlines": 1.7,
    "Air India": 1.3,
    "Indigo": 1.1,
    "AirAsia": 1.0,
    "Qantas": 1.6,
    "default": 1.2  # Fallback multiplier for airlines not in the dictionary
}

# Function to get peak hour multiplier based on departure time
# Peak hours are defined as morning (6-10 AM) and evening (5-9 PM) when demand is highest
def get_peak_multiplier(departure_time):
    """
    Calculates a multiplier for flights departing during peak hours.
    
    Args:
        departure_time (str): ISO format datetime string
        
    Returns:
        float: 1.5 for peak hours, 1.0 for off-peak hours
    """
    try:
        # Parse ISO format datetime and handle timezone indicator (Z)
        departure_time = datetime.fromisoformat(departure_time.replace("Z", "+00:00"))
        hour = departure_time.hour
        
        # Peak hours: Morning (6-10 AM) + Evening (5-9 PM)
        # During these times, airline prices are typically higher due to demand
        if 6 <= hour < 10 or 17 <= hour < 21:
            return 1.5
        else:
            return 1.0
    except (ValueError, AttributeError, TypeError):
        # If time parsing fails, return default multiplier of 1.0
        return 1.0

# Function to simulate and calculate flight prices based on multiple factors
def simulate_price(df):
    """
    Calculates flight prices for all rows in the dataframe based on:
    1. Base price: Duration × 4000 (price per hour)
    2. Airline factor: Each airline has a different pricing strategy
    3. Peak hour multiplier: Flights during peak hours cost more
    4. Random fluctuation: ±1500 to simulate real-world market variations
    
    Args:
        df (pandas.DataFrame): DataFrame with columns: duration_hours, airline, departure_time
        
    Returns:
        pandas.DataFrame: Original dataframe with new 'price' column added
        
    Note:
        PERFORMANCE: Currently uses iterrows() which is slower than vectorized operations.
        For production with large datasets (>100K rows), consider refactoring to use:
        - apply() with lambda functions
        - numpy vectorization for batch operations
        - or pandas.apply() with axis parameter
        This demonstrates O(n) complexity but with Python loop overhead.
    """
    prices = []
    
    # Iterate through each flight record in the dataframe
    # TODO: Optimize with vectorized operations for large datasets
    for index, row in df.iterrows():
        duration = row["duration_hours"]
        airline = row["airline"]
        departure_time = row["departure_time"]
        
        # Handle missing duration values
        # Note: Invalid data handling - skip calculation if core data missing
        if duration is None:
            prices.append(None)
            continue
        
        # Step 1: Base Price Calculation (price per hour)
        # Standard rate: ₹4000 per flight hour
        # This represents the base cost structure of the airline
        base_price = duration * 4000
        
        # Step 2: Airline Factor - premium airlines charge more
        # Get airline-specific multiplier or use default if airline not found
        # Demonstrates dictionary lookup with fallback pattern
        factor = airline_factor.get(airline, airline_factor["default"])
        
        # Step 3: Peak Hour Multiplier - demand-based pricing
        # Morning and evening flights have higher multipliers
        # Implements time-based dynamic pricing strategy
        peak_multiplier = get_peak_multiplier(departure_time)
        
        # Step 4: Random Fluctuation - simulate market variations
        # Adds randomness within ±1500 range to simulate real pricing
        # Represents market volatility and supply-demand fluctuations
        fluctuation = np.random.randint(-1500, 1500)
        
        # Final Price Calculation
        # All factors are multiplicative for compound effect on base price
        # Formula: (Base × Airline Factor × Peak Multiplier) + Random Fluctuation
        final_price = (base_price * factor * peak_multiplier) + fluctuation
        
        # Round to 2 decimal places for currency representation
        # Ensures prices are realistic (no fractional paise in final quotes)
        prices.append(round(final_price, 2))
    
    # Assign all calculated prices to the dataframe
    # Modifies dataframe in-place by adding new column
    df["price"] = prices
    
    # Return the enhanced dataframe with price column
    return df


# Function to normalize flight prices to a 0-1 scale for fair comparison
def normalize_price(df):
    """
    Normalizes prices using Min-Max normalization technique.
    Scales all prices to a [0, 1] range for fair comparison and visualization.
    
    Formula: normalized_price = (price - min_price) / (max_price - min_price)
    
    Use Cases:
    - Preparing data for machine learning models (they prefer normalized inputs)
    - Creating fair comparison visualizations
    - Feature scaling for neural networks
    
    Args:
        df (pandas.DataFrame): DataFrame with 'price' column to normalize
        
    Returns:
        pandas.DataFrame: DataFrame with new 'normalized_prices' column added
        
    Time Complexity: O(n) - single pass through data
    Space Complexity: O(n) - stores normalized values
    
    Edge Cases Handled:
    - Missing values (NaN/None) are preserved
    - All identical prices (avoided with epsilon smoothing)
    """
    # Extract valid (non-null) prices from the dataframe
    # dropna() removes None/NaN values for statistical calculations
    valid_prices = df["price"].dropna()
    
    # Handle edge case: if all prices are None, return dataframe with None values
    # This prevents division by zero and invalid normalization
    if valid_prices.empty:
        df["normalized_prices"] = None
        return df
    
    # Get minimum and maximum prices for scaling
    # These form the bounds of the normalization range
    min_price = valid_prices.min()
    max_price = valid_prices.max()
    
    # Initialize list to store normalized values
    # Using list instead of direct assignment for data integrity during iteration
    normalized = []
    
    # Iterate through all prices and normalize each one
    for price in df["price"]:
        if price is None:
            # Preserve None values for missing data
            # Maintains data alignment across columns
            normalized.append(None)
        else:
            # Apply Min-Max normalization formula
            # Small epsilon (1e-6) prevents division by zero if all prices are identical
            # This is a numerical stability technique commonly used in ML
            norm = (price - min_price) / (max_price - min_price + 1e-6)
            normalized.append(round(norm, 3))
    
    # Assign normalized values to the dataframe as new column
    # Creates new column without modifying existing data
    df["normalized_prices"] = normalized
    
    # Return the enhanced dataframe with normalized prices column
    return df
if __name__ == "__main__":
    """
    Main entry point demonstrating the flight pricing and normalization workflow.
    This section showcases:
    1. Creating sample flight data
    2. Calculating prices using simulate_price()
    3. Normalizing prices using normalize_price()
    """
    
    # Sample test data representing different flight scenarios
    flight_data = {
        "duration_hours": [2.5, 4.0, 1.5, 3.0, 2.0],
        "airline": ["Qatar Airways", "Air India", "AirAsia", "Singapore Airlines", None],
        "departure_time": ["2024-04-23T08:00:00Z", "2024-04-23T14:30:00Z", 
                          "2024-04-23T18:45:00Z", "2024-04-23T22:00:00Z", "2024-04-23T09:15:00Z"]
    }
    
    # Create DataFrame from sample data
    df = pd.DataFrame(flight_data)
    print("=" * 60)
    print("ORIGINAL FLIGHT DATA:")
    print("=" * 60)
    print(df)
    print("\n")
    
    # Step 1: Calculate flight prices based on multiple factors
    print("=" * 60)
    print("STEP 1: SIMULATING PRICES...")
    print("=" * 60)
    df_with_prices = simulate_price(df)
    print(df_with_prices[["airline", "duration_hours", "departure_time", "price"]])
    print("\n")
    
    # Step 2: Normalize prices to [0, 1] range for fair comparison
    print("=" * 60)
    print("STEP 2: NORMALIZING PRICES...")
    print("=" * 60)
    df_normalized = normalize_price(df_with_prices)
    print(df_normalized[["price", "normalized_prices"]])
    print("=" * 60)
