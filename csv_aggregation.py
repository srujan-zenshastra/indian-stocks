import pandas as pd
import os

# Define the expected headers for both weekly and monthly files
WEEKLY_HEADERS = ["Symbol  ", "Series  ", "Date  ", "Prev Close  ", "Open Price  ", 
                 "High Price  ", "Low Price  ", "Last Price  ", "Close Price  ", 
                 "Average Price ", "Total Traded Quantity  ", "Turnover ₹  ", 
                 "No. of Trades  ", "Deliverable Qty  ", "% Dly Qt to Traded Qty  "]

MONTHLY_HEADERS = ["Symbol  ", "Series  ", "Date  ", "Prev Close  ", "Open Price  ", 
                  "High Price  ", "Low Price  ", "Last Price  ", "Close Price  ", 
                  "Average Price ", "Total Traded Quantity  ", "Turnover ₹  ", 
                  "No. of Trades  ", "Deliverable Qty  ", "% Dly Qt to Traded Qty  "]

def check_headers(input_df, expected_headers):
    """Check if input CSV headers match expected headers"""
    input_headers = list(input_df.columns)
    return input_headers == expected_headers

def process_csv(input_filename, target_filename, expected_headers):
    """Process the CSV file and append data if headers match and data is not duplicate"""
    try:
        # Get the directory of the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        input_file = os.path.join(script_dir, input_filename)
        target_file = os.path.join(script_dir, target_filename)
        
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"Error: File '{input_filename}' not found in the script directory")
            return False
        
        # Read the input CSV file
        input_df = pd.read_csv(input_file)
        print(f"Input file rows: {len(input_df)}")
        
        # Check if headers match
        if not check_headers(input_df, expected_headers):
            print("Error: CSV headers do not match the expected format")
            print("Expected headers:", expected_headers)
            print("Found headers:", list(input_df.columns))
            return False
        
        # Handle the target file
        if os.path.exists(target_file):
            # Read existing data
            existing_df = pd.read_csv(target_file)
            print(f"Existing file rows before append: {len(existing_df)}")
            
            # Check for duplicates based on Date column
            existing_dates = set(existing_df["Date  "].astype(str))
            new_data = input_df[~input_df["Date  "].astype(str).isin(existing_dates)]
            
            if len(new_data) == 0:
                print("No new data to append - all dates already exist in target file")
                return True
            
            print(f"New unique rows to append: {len(new_data)}")
            
            # Append new data
            updated_df = pd.concat([existing_df, new_data], ignore_index=True)
            print(f"Total rows after append: {len(updated_df)}")
            
            # Write back to file
            updated_df.to_csv(target_file, mode='w', index=False)
        else:
            # If file doesn't exist, create it with the input data
            input_df.to_csv(target_file, mode='w', index=False)
            print(f"New file created with rows: {len(input_df)}")
            new_data = input_df  # For consistency in verification
        
        # Verify the result
        result_df = pd.read_csv(target_file)
        print(f"Final file rows: {len(result_df)}")
        print(f"Successfully processed and appended data to {target_filename}")
        return True
    
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return False

def main():
    print("CSV Data Processing System")
    print("1. Process Weekly Data")
    print("2. Process Monthly Data")
    
    while True:
        choice = input("Enter your choice (1 or 2): ")
        
        if choice in ['1', '2']:
            break
        print("Invalid choice. Please enter 1 or 2.")
    
    # Get input filename
    input_filename = input("Enter the CSV filename (must be in same directory as script): ")
    
    # Add .csv extension if not provided
    if not input_filename.lower().endswith('.csv'):
        input_filename += '.csv'
    
    # Process based on user choice
    if choice == '1':
        target_filename = "etf_week.csv"
        success = process_csv(input_filename, target_filename, WEEKLY_HEADERS)
    else:
        target_filename = "etf_month.csv"
        success = process_csv(input_filename, target_filename, MONTHLY_HEADERS)
    
    if success:
        print("Processing completed successfully")
    else:
        print("Processing failed")

if __name__ == "__main__":
    main()