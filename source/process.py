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
                        monthly_avg = df[df['MONTH'] == month][field].astype('float').mean()
                        monthly_averages[field].append(monthly_avg)
            
            # Append the dictionary containing monthly averages for the current CSV file to the list
            monthly_averages_list.append(monthly_averages)
    
    return monthly_averages_list,locations

def create_csv_from_dict(data_list,locations):
    # Get the field names from the keys of the dictionary
    # Include 'Location' and Month' as the first and second field
    field_names = ['Location'] + ['Month'] + list(data_list[0].keys())  
    
    # Define the output file path
    output_file = os.path.join('outputs', 'process_output.csv')
    
    # Write data to CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        
        # Write header
        writer.writeheader()
        
        # Write monthly averages for each field from each CSV file
        for location,data_dict in zip(locations,data_list):
            for month in range(1, 13):
                row_data = {'Location':location, 'Month': month}  # Add 'Month' value to the row data
                for field, monthly_avg_list in data_dict.items():
                    if(len(monthly_avg_list)==0):
                        row_data[field] = np.nan
                    else:
                        row_data[field] = monthly_avg_list[month - 1]  # Month is 0-indexed
                # Write row to CSV
                writer.writerow(row_data)

if __name__ == "__main__":

    folder_path = 'data'
    all_daily_avg_fields_file = 'outputs/daily_fields_list.txt'

    # Read the list from the text file
    with open(all_daily_avg_fields_file, 'r') as text_file:
        all_daily_avg_fields = [line.strip() for line in text_file]
        
    monthly_averages,locations = extract_monthly_averages(folder_path, all_daily_avg_fields)
    create_csv_from_dict(monthly_averages,locations)