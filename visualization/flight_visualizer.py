# Import required libraries for visualization
import matplotlib.pyplot as plt
import numpy as np  # For trend line calculation
import os  # For file path operations

# Create visualization directory if it doesn't exist
# This ensures that chart files can be saved without errors
VISUALIZATION_DIR = os.path.join(os.path.dirname(__file__), "charts")
if not os.path.exists(VISUALIZATION_DIR):
    os.makedirs(VISUALIZATION_DIR)

# Function to plot the price distribution of flights using histogram
def plot_price_distribution(df):
    """
    Creates a histogram showing the distribution of flight prices.
    Displays the chart and saves it as a PNG file.
    
    Args:
        df: DataFrame containing flight data with 'price' column
    """
    try:
        # Check if DataFrame is empty
        if df is None or df.empty:
            print("❌ Error: No flight data available to visualize!")
            return
        
        # Check if price column exists
        if 'price' not in df.columns:
            print(f"❌ Error: 'price' column not found! Available columns: {list(df.columns)}")
            return
        
        print(f"📊 Creating price distribution chart with {len(df)} flights...")
        
        plt.figure(figsize=(10, 6))
        plt.hist(df["price"], bins=10, color='skyblue', edgecolor='black')
        plt.title("Flight Price Distribution", fontsize=14, fontweight='bold')
        plt.xlabel("Price (Rupees)", fontsize=12)
        plt.ylabel("Number of Flights", fontsize=12)
        plt.grid(axis='y', alpha=0.3)
        
        # Save chart with absolute path
        chart_path = os.path.join(VISUALIZATION_DIR, "price_distribution.png")
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        print(f"✓ Price distribution chart saved to: {chart_path}")
        
        # Display the chart to user
        plt.show()
        plt.close()
        
    except Exception as e:
        print(f"❌ Error creating price distribution chart: {str(e)}")


# Function to plot average prices by airline
def plot_airline_prices(df):
    """
    Creates a bar chart showing average flight prices for each airline.
    Displays the chart and saves it as a PNG file.
    
    Args:
        df: DataFrame containing flight data with 'airline' and 'price' columns
    """
    try:
        # Check if DataFrame is empty
        if df is None or df.empty:
            print("❌ Error: No flight data available to visualize!")
            return
        
        # Check if required columns exist
        if 'airline' not in df.columns or 'price' not in df.columns:
            print(f"❌ Error: Missing 'airline' or 'price' columns! Available: {list(df.columns)}")
            return
        
        print(f"📊 Creating airline prices chart with {len(df)} flights...")
        
        plt.figure(figsize=(12, 6))
        
        # Group data by airline and calculate mean price for each airline
        airline_avg = df.groupby("airline")["price"].mean().sort_values(ascending=False)
        airline_avg.plot(kind="bar", color='coral', edgecolor='black')
        
        plt.title("Average Flight Price by Airline", fontsize=14, fontweight='bold')
        plt.xlabel("Airline", fontsize=12)
        plt.ylabel("Average Price (Rupees)", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        # Save chart with absolute path
        chart_path = os.path.join(VISUALIZATION_DIR, "airline_prices.png")
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        print(f"✓ Airline prices chart saved to: {chart_path}")
        
        # Display the chart to user
        plt.show()
        plt.close()
        
    except Exception as e:
        print(f"❌ Error creating airline prices chart: {str(e)}")


# Function to plot the relationship between flight duration and price
def plot_duration_vs_price(df):
    """
    Creates a scatter plot showing the correlation between flight duration and price.
    Displays the chart and saves it as a PNG file.
    
    Args:
        df: DataFrame containing flight data with 'duration_hours' and 'price' columns
    """
    try:
        # Check if DataFrame is empty
        if df is None or df.empty:
            print("❌ Error: No flight data available to visualize!")
            return
        
        # Check if required columns exist
        if 'duration_hours' not in df.columns or 'price' not in df.columns:
            print(f"❌ Error: Missing 'duration_hours' or 'price' columns! Available: {list(df.columns)}")
            return
        
        # Check if we have enough data points
        if len(df) < 2:
            print("❌ Error: Need at least 2 data points to create a chart!")
            return
        
        print(f"📊 Creating duration vs price chart with {len(df)} flights...")
        
        plt.figure(figsize=(10, 6))
        plt.scatter(df["duration_hours"], df["price"], color='green', alpha=0.6, s=100, edgecolor='black')
        
        plt.title("Flight Duration vs Price", fontsize=14, fontweight='bold')
        plt.xlabel("Duration (Hours)", fontsize=12)
        plt.ylabel("Price (Rupees)", fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # Add a trend line to show correlation (with error handling)
        try:
            z = np.polyfit(df["duration_hours"], df["price"], 1)
            p = np.poly1d(z)
            plt.plot(df["duration_hours"], p(df["duration_hours"]), "r--", alpha=0.8, linewidth=2, label='Trend Line')
            plt.legend()
        except Exception as trend_error:
            print(f"⚠ Warning: Could not add trend line: {str(trend_error)}")
        
        # Save chart with absolute path
        chart_path = os.path.join(VISUALIZATION_DIR, "duration_vs_price.png")
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        print(f"✓ Duration vs Price chart saved to: {chart_path}")
        
        # Display the chart to user
        plt.show()
        plt.close()
        
    except Exception as e:
        print(f"❌ Error creating duration vs price chart: {str(e)}")


# Function to extract meaningful insights from flight data
def generate_insights(df):
    """
    Analyzes flight data and generates key insights including cheapest/most expensive flights,
    fastest/slowest flights, and average price.
    
    Args:
        df: DataFrame containing flight data
        
    Returns:
        List of insight strings
    """
    try:
        # Check if DataFrame is empty
        if df is None or df.empty:
            print("❌ Error: No flight data to generate insights from!")
            return []
        
        # Check if required columns exist
        if 'price' not in df.columns or 'airline' not in df.columns or 'duration_hours' not in df.columns:
            print(f"❌ Error: Missing required columns! Available: {list(df.columns)}")
            return []
        
        insights = []
        
        # Find cheapest flight
        cheapest = df.loc[df["price"].idxmin()]
        insights.append(f"Cheapest Flight: {cheapest['airline']} at rupees {int(cheapest['price'])}")
        
        # Find most expensive flight
        expensive = df.loc[df["price"].idxmax()]
        insights.append(f"Most Expensive Flight: {expensive['airline']} at rupees {int(expensive['price'])}")
        
        # Find fastest flight
        fastest = df.loc[df["duration_hours"].idxmin()]
        insights.append(f"Fastest Flight: {fastest['airline']} ({round(fastest['duration_hours'], 2)} hours)")
        
        # Find slowest flight
        slowest = df.loc[df["duration_hours"].idxmax()]
        insights.append(f"Slowest Flight: {slowest['airline']} ({round(slowest['duration_hours'], 2)} hours)")
        
        # Calculate average flight price
        avg_price = df["price"].mean()
        insights.append(f"Average Flight Price: rupees {int(avg_price)}")
        
        return insights
        
    except Exception as e:
        print(f"❌ Error generating insights: {str(e)}")
        return []


# Function to display insights in a formatted manner
def display_insights(insights):  # Fixed typo: was "diaplay_insights"
    """
    Prints flight market insights in a formatted way with a decorative border.
    
    Args:
        insights: List of insight strings to display
    """
    print("\n" + "=" * 60)
    print("Market Insights")
    print("=" * 60)
    for insight in insights:
        print(f"- {insight}")
    print("=" * 60)
