# ===============================================
# Diagnostic Test for CSV/Excel Export
# ===============================================
# This script tests the export functionality independently

import pandas as pd
import os
from datetime import datetime
from data.data_saver import save_to_csv, save_to_excel

# Create sample test data
print("=" * 50)
print("TEST: Export Functionality Diagnostic")
print("=" * 50)

# Create a simple test DataFrame
test_data = {
    'airline': ['Air India', 'SpiceJet', 'IndiGo'],
    'price': [5000, 4500, 5500],
    'duration_hours': [2.5, 2.0, 3.0],
    'ai_score': [0.85, 0.90, 0.80]
}

test_df = pd.DataFrame(test_data)

print("\n1. Test DataFrame Created:")
print(test_df)

print("\n2. Testing CSV Export...")
try:
    save_to_csv(test_df)
    print("✓ CSV Export Successful")
except Exception as e:
    print(f"❌ CSV Export Failed: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n3. Testing Excel Export...")
try:
    save_to_excel(test_df)
    print("✓ Excel Export Successful")
except Exception as e:
    print(f"❌ Excel Export Failed: {str(e)}")
    print("\n⚠ Note: If you see 'No module named openpyxl', run:")
    print("   pip install openpyxl")
    import traceback
    traceback.print_exc()

print("\n4. Checking data/ Directory:")
if os.path.exists("data"):
    print("✓ data/ directory exists")
    files = os.listdir("data")
    print(f"   Files in data/: {files}")
else:
    print("❌ data/ directory not found")

print("\n" + "=" * 50)
print("Diagnostic Test Complete")
print("=" * 50)
