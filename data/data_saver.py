# ==========================================
# Data Export Module - Flight Intelligence System
# ==========================================
# This module provides utilities to export flight data 
# in multiple formats (CSV, Excel) with timestamped filenames
# ==========================================

import os
from datetime import datetime

def save_to_csv(df):
    """
    Save a pandas DataFrame to CSV format with timestamp.
    
    Args:
        df (pandas.DataFrame): The flight data to save
        
    Returns:
        None: Prints confirmation message with filename
        
    Note:
        - Creates 'data' directory if it doesn't exist
        - Filename format: flight_data_YYYYMMDD_HHMMSS.csv
        - This avoids file overwrites and maintains data history
    """
    # Create directory recursively if it doesn't exist (using makedirs instead of mkdir)
    # os.makedirs supports exist_ok parameter unlike os.mkdir()
    os.makedirs("data", exist_ok=True)
    
    # Generate timestamp for unique filename (prevents overwriting previous data)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Construct file path with timestamp
    filename = f"data/flight_data_{timestamp}.csv"
    
    # Export DataFrame to CSV (index=False removes row numbers from output)
    df.to_csv(filename, index=False)
    
    # Confirm successful save with full filepath
    print(f"\nData saved to csv file: {filename}")


def save_to_excel(df):
    """
    Save a pandas DataFrame to Excel format with timestamp.
    
    Args:
        df (pandas.DataFrame): The flight data to save
        
    Returns:
        None: Prints confirmation message with filename
        
    Note:
        - Creates 'data' directory if it doesn't exist
        - Filename format: flight_data_YYYYMMDD_HHMMSS.xlsx
        - Excel format useful for non-technical stakeholders
    """
    # Create directory recursively if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Generate timestamp for unique filename (maintains data history)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Construct file path with timestamp
    filename = f"data/flight_data_{timestamp}.xlsx"
    
    # Export DataFrame to Excel (index=False removes row numbers from output)
    df.to_excel(filename, index=False)
    
    # Confirm successful save with full filepath (f-string prefix required for variable interpolation)
    print(f"\nData saved to excel file: {filename}")
