# ===============================================
# Excel Data Verification Diagnostic
# ===============================================
# This script reads and validates the Excel file contents

import pandas as pd
import os
from pathlib import Path

print("=" * 70)
print("EXCEL FILE DATA VERIFICATION")
print("=" * 70)

excel_file = "data/flight_data_20260426_224648.xlsx"

# Check if file exists
if not os.path.exists(excel_file):
    print(f"❌ File not found: {excel_file}")
else:
    print(f"✓ File found: {excel_file}")
    print(f"  File size: {os.path.getsize(excel_file)} bytes")
    
    try:
        # Read the Excel file
        print("\n" + "-" * 70)
        print("Reading Excel file...")
        print("-" * 70)
        
        df = pd.read_excel(excel_file)
        
        # Display basic information
        print(f"\n📊 BASIC INFO:")
        print(f"   - Number of rows: {len(df)}")
        print(f"   - Number of columns: {len(df.columns)}")
        print(f"   - Data shape: {df.shape}")
        
        # Display column information
        print(f"\n📋 COLUMNS:")
        for i, col in enumerate(df.columns, 1):
            dtype = str(df[col].dtype)
            print(f"   {i}. {col:20s} (Type: {dtype})")
        
        # Display data types summary
        print(f"\n🔍 DATA TYPES:")
        print(df.dtypes)
        
        # Display first few rows
        print(f"\n📝 FIRST 5 ROWS:")
        print("-" * 70)
        print(df.head())
        
        # Display statistical summary
        print(f"\n📈 STATISTICAL SUMMARY:")
        print("-" * 70)
        print(df.describe())
        
        # Check for missing values
        print(f"\n⚠️  MISSING VALUES:")
        missing = df.isnull().sum()
        if missing.sum() == 0:
            print("   ✓ No missing values found")
        else:
            print(missing[missing > 0])
        
        # Data quality checks
        print(f"\n✅ DATA QUALITY CHECKS:")
        print("-" * 70)
        
        # Check for duplicate rows
        duplicates = df.duplicated().sum()
        print(f"   • Duplicate rows: {duplicates}")
        
        # Check for negative values in numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            if (df[col] < 0).any():
                print(f"   ⚠️  Column '{col}' has negative values")
            else:
                print(f"   ✓ Column '{col}' - all values >= 0")
        
        # Expected columns for flight data
        expected_cols = ['airline', 'price', 'duration_hours', 'ai_score']
        print(f"\n🎯 EXPECTED vs ACTUAL COLUMNS:")
        for col in expected_cols:
            if col in df.columns:
                print(f"   ✓ {col:20s} - FOUND")
            else:
                print(f"   ❌ {col:20s} - MISSING")
        
        # Full data display
        print(f"\n📄 COMPLETE DATA:")
        print("-" * 70)
        print(df.to_string(index=False))
        
        # Validation results
        print(f"\n{'=' * 70}")
        print("VALIDATION SUMMARY:")
        print(f"{'=' * 70}")
        
        validation_passed = True
        
        if len(df) > 0:
            print("✓ Data exists in Excel file")
        else:
            print("❌ No data found in Excel file")
            validation_passed = False
        
        if all(col in df.columns for col in expected_cols):
            print("✓ All expected columns present")
        else:
            print("⚠️  Some expected columns missing")
            validation_passed = False
        
        if df.isnull().sum().sum() == 0:
            print("✓ No missing/null values")
        else:
            print("⚠️  Some missing values found")
        
        if duplicates == 0:
            print("✓ No duplicate rows")
        else:
            print(f"⚠️  {duplicates} duplicate rows found")
        
        print(f"\n{'=' * 70}")
        if validation_passed:
            print("✅ DATA VALIDATION: PASSED")
        else:
            print("⚠️  DATA VALIDATION: NEEDS REVIEW")
        print(f"{'=' * 70}\n")
        
    except Exception as e:
        print(f"\n❌ Error reading Excel file: {str(e)}")
        import traceback
        traceback.print_exc()
