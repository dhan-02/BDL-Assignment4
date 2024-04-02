import os
import csv
import pandas as pd
import numpy as np

def extract_monthly_averages(folder_path, monthly_avg_fields):
    monthly_averages_list = []  # List to store monthly averages for each CSV file
    
    locations = []
    # Iterate through each CSV file in the folder
    for file_name in sorted(os.listdir(folder_path)):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            locations.append(file_name[:-4])
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path,low_memory=False)

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
    
    return monthly_averages_list,locations

def create_csv_from_dict(data_list,locations):
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
                row_data = {'Location':location,'Month': month}  # Add 'Month' value to the row data
                for field, monthly_avg_list in data_dict.items():
                    if(len(monthly_avg_list)==0):
                        row_data[field] = np.nan
                    else:
                        row_data[field] = monthly_avg_list[month - 1]  # Month is 0-indexed
                # Write row to CSV
                writer.writerow(row_data)


if __name__ == "__main__":

    folder_path = 'data'

    all_daily_avg_fields = ['DailyAverageRelativeHumidity', 
                        'DailyAverageDewPointTemperature', 
                        'DailyAverageDryBulbTemperature', 
                        'DailyAverageSeaLevelPressure',
                        'DailyAverageStationPressure', 
                        'DailyMaximumDryBulbTemperature', 
                        'DailyMinimumDryBulbTemperature', 
                        'DailyAverageWetBulbTemperature']


    all_monthly_avg_fields = ['MonthlyAverageRH', 
                          'MonthlyDewpointTemperature',
                          'MonthlyMeanTemperature', 
                          'MonthlySeaLevelPressure', 
                          'MonthlyStationPressure', 
                          'MonthlyMaximumTemperature', 
                          'MonthlyMinimumTemperature', 
                          'MonthlyWetBulb']

    text_file_path = 'outputs/daily_fields_list.txt'

    # Write the list to a text file
    with open(text_file_path, 'w') as text_file:
        for field in all_daily_avg_fields:
            text_file.write(field + '\n')    
    
    # valid_daily_avg_fields,valid_monthly_avg_fields = get_valid_fields(all_daily_avg_fields,all_monthly_avg_fields)
    monthly_averages,locations = extract_monthly_averages(folder_path, all_monthly_avg_fields)
    create_csv_from_dict(monthly_averages,locations)
