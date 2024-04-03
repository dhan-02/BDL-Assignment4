import os
import csv
import pandas as pd
import numpy as np

def extract_monthly_averages(folder_path, monthly_avg_fields):
    """
    Extracts monthly averages for specified fields from CSV files in the given folder path.

    Args:
    - folder_path (str): Path to the folder containing CSV files.
    - monthly_avg_fields (list of str): List of field names for which monthly averages are to be extracted.

    Returns:
    - monthly_averages_list (list of dict): List of dictionaries containing monthly averages for each field.
    - locations (list of str): List of location names extracted from file names.
    """
    monthly_averages_list = []  # List to store monthly averages for each CSV file
    locations = []  # List to store location names extracted from file names
    
    # Iterate through each CSV file in the folder
    for file_name in sorted(os.listdir(folder_path)):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            locations.append(file_name[:-4])  # Extract location name from file name
            
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path, low_memory=False)

            # Define the regex pattern to match any number followed by 's'
            pattern = r'(\d+)s'

            # Apply regex substitution to all columns in the DataFrame
            df = df.replace(regex={pattern: r'\1'})
            
            # Extract month from date column
            df['MONTH'] = df['DATE'].apply(lambda date: int(date.split('-')[1]))
            
            # Initialize a dictionary to store monthly averages for the current CSV file
            monthly_averages = {field: [] for field in monthly_avg_fields}
            
            # Iterate through each field in monthly_avg_fields
            for field in monthly_avg_fields:
                # Check if the field exists and contains at least one non-empty value
                if not df[field].isnull().all():
                    # Extract the monthly average for each month
                    for month in range(1, 13):
                        # Check if data exists for the current month
                        if any(df['MONTH'] == month):
                            # Extract the last value for the current month
                            monthly_data = df[df['MONTH'] == month][field].dropna().astype('float')
                            if not monthly_data.empty:
                                monthly_avg = monthly_data.iloc[-1]  # Extract last non-NaN value
                            else:
                                monthly_avg = np.nan  # All values are NaN for this month
                        else:
                            # No data exists for the current month, append NaN
                            monthly_avg = np.nan
                        # Append the monthly average to the corresponding field in monthly_averages dictionary
                        monthly_averages[field].append(monthly_avg)
                        
            # Append the dictionary containing monthly averages for the current CSV file to the list
            monthly_averages_list.append(monthly_averages)
    
    return monthly_averages_list, locations

def create_csv_from_dict(data_list, locations):
    """
    Creates a CSV file from a list of dictionaries containing monthly averages.

    Args:
    - data_list (list of dict): List of dictionaries containing monthly averages for each field.
    - locations (list of str): List of location names corresponding to the data.

    Returns:
    - None
    """
    # Get the field names from the keys of the dictionary
    field_names = ['Location'] + ['Month'] + list(data_list[0].keys())  # Include 'Location' and 'Month' as the first and second field
    
    # Define the output file path
    output_file = os.path.join('outputs', 'prepare_output.csv')
    
    # Write data to CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        
        # Write header
        writer.writeheader()
        
        # Write monthly averages for each field from each CSV file
        for location, data_dict in zip(locations, data_list):
            for month in range(1, 13):
                row_data = {'Location': location, 'Month': month}  # Add 'Month' value to the row data
                for field, monthly_avg_list in data_dict.items():
                    if len(monthly_avg_list) == 0:
                        row_data[field] = np.nan
                    else:
                        row_data[field] = monthly_avg_list[month - 1]  # Month is 0-indexed
                # Write row to CSV
                writer.writerow(row_data)

if __name__ == "__main__":
    # Define input parameters
    folder_path = 'data'
    all_daily_avg_fields = ['DailyAverageDryBulbTemperature', 
                            'DailyMaximumDryBulbTemperature', 
                            'DailyMinimumDryBulbTemperature',
                            'DailyAverageSeaLevelPressure',
                            'DailyAverageStationPressure']
    all_monthly_avg_fields = ['MonthlyMeanTemperature', 
                              'MonthlyMaximumTemperature', 
                              'MonthlyMinimumTemperature',
                              'MonthlySeaLevelPressure', 
                              'MonthlyStationPressure',]
    text_file_path = 'outputs/daily_fields_list.txt'

    # Write the list to a text file
    with open(text_file_path, 'w') as text_file:
        for field in all_daily_avg_fields:
            text_file.write(field + '\n')    
    
    # Extract monthly averages and location names
    monthly_averages, locations = extract_monthly_averages(folder_path, all_monthly_avg_fields)
    
    # Create CSV from the extracted data
    create_csv_from_dict(monthly_averages, locations)
