"""
Simple test script to debug visualization issues.
Run this separately to verify if charts work without running the entire application.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

print("=" * 60)
print("VISUALIZATION TEST SCRIPT")
print("=" * 60)

# Step 1: Check matplotlib backend
print("\n1. Checking Matplotlib Backend...")
print(f"   Current backend: {plt.get_backend()}")
try:
    # Try to use TkAgg backend (interactive)
    plt.switch_backend('TkAgg')
    print("   ✓ Switched to TkAgg backend (interactive)")
except:
    print("   ⚠ Could not switch to TkAgg, using default")

# Step 2: Create sample flight data
print("\n2. Creating sample flight data...")
sample_data = {
    'airline': ['IndiGo', 'Air India', 'SpiceJet', 'IndiGo', 'Air India', 'SpiceJet'],
    'price': [3500, 4200, 3800, 3900, 4500, 3600],
    'duration_hours': [2.5, 2.0, 2.3, 2.4, 2.1, 2.2]
}

df = pd.DataFrame(sample_data)
print(f"   Created {len(df)} test flights")
print(f"   Columns: {list(df.columns)}")
print(f"   Data:\n{df}")

# Step 3: Test Chart 1 - Price Distribution
print("\n3. Testing Price Distribution Chart...")
try:
    plt.figure(figsize=(10, 6))
    plt.hist(df["price"], bins=10, color='skyblue', edgecolor='black')
    plt.title("Test: Flight Price Distribution", fontsize=14, fontweight='bold')
    plt.xlabel("Price (Rupees)", fontsize=12)
    plt.ylabel("Number of Flights", fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    print("   ✓ Chart created successfully!")
    plt.show()
    plt.close()
    print("   ✓ Chart displayed successfully!")
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

# Step 4: Test Chart 2 - Airline Prices
print("\n4. Testing Airline Prices Chart...")
try:
    plt.figure(figsize=(12, 6))
    airline_avg = df.groupby("airline")["price"].mean().sort_values(ascending=False)
    airline_avg.plot(kind="bar", color='coral', edgecolor='black')
    plt.title("Test: Average Flight Price by Airline", fontsize=14, fontweight='bold')
    plt.xlabel("Airline", fontsize=12)
    plt.ylabel("Average Price (Rupees)", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    print("   ✓ Chart created successfully!")
    plt.show()
    plt.close()
    print("   ✓ Chart displayed successfully!")
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

# Step 5: Test Chart 3 - Duration vs Price
print("\n5. Testing Duration vs Price Chart...")
try:
    plt.figure(figsize=(10, 6))
    plt.scatter(df["duration_hours"], df["price"], color='green', alpha=0.6, s=100, edgecolor='black')
    plt.title("Test: Flight Duration vs Price", fontsize=14, fontweight='bold')
    plt.xlabel("Duration (Hours)", fontsize=12)
    plt.ylabel("Price (Rupees)", fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Add trend line
    z = np.polyfit(df["duration_hours"], df["price"], 1)
    p = np.poly1d(z)
    plt.plot(df["duration_hours"], p(df["duration_hours"]), "r--", alpha=0.8, linewidth=2, label='Trend Line')
    plt.legend()
    
    print("   ✓ Chart created successfully!")
    plt.show()
    plt.close()
    print("   ✓ Chart displayed successfully!")
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

print("\n" + "=" * 60)
print("✓ VISUALIZATION TEST COMPLETED!")
print("=" * 60)
print("\nIf all charts appeared, your system can display visualizations.")
print("If not, check the error messages above.\n")
