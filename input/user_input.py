# Import the required libraries for date validation
from datetime import datetime


# Function to get user input
def get_user_input():
    """
    Collects user input for flight search with date validation.
    
    Returns:
        dict: A dictionary containing source, destination, and valid travel date
    """
    # Display header for better user experience
    print("=== Flight Search System ===")
    
    # Collect departure city from user
    # strip() removes any leading/trailing whitespace for data validation
    source = input("Enter Departure City:").strip()
    
    # Collect destination city from user
    destination = input("Enter Destination City:").strip()
    
    # Validate travel date with loop to ensure correct format
    # This demonstrates error handling and user input validation
    while True:
        travel_date = input("Enter Travel Date (YYYY-MM-DD):").strip()
        try:
            # Attempt to parse the date string in YYYY-MM-DD format
            datetime.strptime(travel_date, "%Y-%m-%d")
            # Exit loop if date is valid
            break
        except ValueError:
            # Notify user of invalid format and prompt again
            print("Invalid date format. Please enter date in YYYY-MM-DD format.")
    
    # Package collected data into a dictionary for easy access and passing
    user_data = {
        "source": source,
        "destination": destination,
        "date": travel_date
    }
    
    # Return the user data to be used by other functions
    return user_data
