import numpy as np
from sklearn.metrics import r2_score
import csv
import pandas as pd

def read_mycsv(file_path):
    data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            data.append([float(val) if val != 'nan' else np.nan for val in row])
    return data

def compute_r2(monthly_avg_gt_file, monthly_avg_est_file):
    monthly_avg_gt = read_mycsv(monthly_avg_gt_file)
    monthly_avg_est = read_mycsv(monthly_avg_est_file)
    
    num_locations = len(monthly_avg_gt) // 12  # Calculate the number of locations 
    r2_values = []

    for i in range(num_locations):
        start_index = i * 12
        end_index = (i + 1) * 12
        
        gt_avg = monthly_avg_gt[start_index:end_index]
        est_avg = monthly_avg_est[start_index:end_index]
        nan_fields_indices = []  # List to store field indices with all NaN values
        
        # Iterate over each field
        for j in range(2, len(gt_avg[0])):
            field_gt_avg = [row[j] for row in gt_avg]
            field_est_avg = [row[j] for row in est_avg]  
            # Check if all values in the field are NaN
            if all(np.isnan(val) for val in field_gt_avg) and all(np.isnan(val) for val in field_est_avg):
                nan_fields_indices.append(j)

        r2_location = []
        
        # Iterate over each field
        for j in range(2, len(gt_avg[0])):
            if j not in nan_fields_indices:
                field_gt_avg = [row[j] for row in gt_avg]
                field_est_avg = [row[j] for row in est_avg]
                
                # Find indices where both corresponding values are not NaN
                valid_indices = [idx for idx, (x, y) in enumerate(zip(field_gt_avg, field_est_avg)) if not (np.isnan(x) or np.isnan(y))]
                valid_gt_avg = [field_gt_avg[idx] for idx in valid_indices]
                valid_est_avg = [field_est_avg[idx] for idx in valid_indices]

                if len(valid_gt_avg) == 0 or len(valid_est_avg) == 0:
                    r2 = np.nan
                else:
                    r2 = r2_score(valid_gt_avg, valid_est_avg)
            else:
                r2 = np.nan
            r2_location.append(r2)
        
        r2_values.append(r2_location)
    
    return r2_values

def get_field_names(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Get the header row
    return headers[2:] # first column is Location, second column is Month

def get_locations(file_path):
    df = pd.read_csv(file_path)
    unique_locations = df['Location'].unique()
    return unique_locations

def convert_to_csv(output_file, r2_values, field_names,locations):
    # Create headers for the CSV file
    headers = ['Location'] + field_names
    
    # Prepare data for CSV
    data = []
    for i, r2_location in enumerate(r2_values):
        location_row = [locations[i]]  # Location identifier
        location_row.extend(r2_location)  # Append R-squared values for each field
        data.append(location_row)

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write headers
        writer.writerow(headers)
        
        # Write data rows
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    monthly_avg_gt_file = 'outputs/prepare_output.csv'
    monthly_avg_est_file = 'outputs/process_output.csv'
    locations = get_locations(monthly_avg_est_file)
    r2_values = compute_r2(monthly_avg_gt_file, monthly_avg_est_file)
    convert_to_csv('outputs/evaluate_output.csv',r2_values,get_field_names(monthly_avg_gt_file),locations)
