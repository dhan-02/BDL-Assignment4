import yaml
import os
import pandas as pd
import random

def get_all_file_names(datafile_path):
    """
    Selects a random sample of files from the html file containing the list of files

    Args:
        datafile_path (str): Path to the html file containing the links

    Returns:
        list: A list of sall file names.
    """
    # Validate input arguments
    print(datafile_path)
    if not isinstance(datafile_path, str) or not os.path.isfile(datafile_path):
        raise ValueError("Invalid datafile_path provided.")

    # Read datafile and extract relevant file names
    with open(datafile_path, "r") as page:
        data_links = []
        for line in page:
            # Check whether we are looking at a line of interest
            if "href" in line and ".csv" in line:
                # Extract filename from the link
                filename = line.split("  ")[0].split('"')[1]
                data_links.append(filename)
        # Check if enough files are available for sampling
        return data_links

def download_html(base_url,year):
    current_dir = os.getcwd()
    bash_command = "wget -O {}/data/data_store.html {}access/{}".format(current_dir, base_url, year)
    # Execute the Bash command using os.system
    os.system(bash_command)

# Execute the Bash command using os.system
    
def is_valid_file(file_path,daily_avg_fields,monthly_avg_fields):
    df = pd.read_csv(file_path,low_memory=False)
    for daily_field, monthly_field in zip(daily_avg_fields, monthly_avg_fields):
        if not df[daily_field].dropna().empty and not df[monthly_field].dropna().empty:
            print("Sucess : File Found")
            return True
    print("Fail")
    return False

def download_csv(base_url, year, n_locs):
    download_html(base_url,year)
    list_files = get_all_file_names('data/data_store.html')
    random.shuffle(list_files)  # Shuffle the list of files

    # Multiple tests showed that only for these fields we have both daily and monthly data, that too for very few csv files
    # Almost no csv files contained data for other pairs of daily and monthly fields
    daily_avg_fields = ['DailyAverageDryBulbTemperature', 
                        'DailyMaximumDryBulbTemperature', 
                        'DailyMinimumDryBulbTemperature',
                        'DailyAverageSeaLevelPressure',
                        'DailyAverageStationPressure']


    monthly_avg_fields = ['MonthlyMeanTemperature', 
                          'MonthlyMaximumTemperature', 
                          'MonthlyMinimumTemperature',
                          'MonthlySeaLevelPressure', 
                          'MonthlyStationPressure',]

    valid_file_count = 0
    for file_name in list_files:
        # Download file
        base_url_year = base_url + "access/" + str(year) + "/"
        download_url = f"{base_url_year}{file_name}"
        path = os.path.join(os.getcwd(), 'data')
        fetch_command = f"wget {download_url} -P {path} -q"
        os.system(fetch_command)
        print("Download Done")
        
        file_path = os.path.join(os.path.join(os.getcwd(), 'data'), file_name)
        # Check file validity
        if is_valid_file(file_path, daily_avg_fields, monthly_avg_fields):
            valid_file_count += 1
            if valid_file_count >= n_locs:
                return 1  # Found n_locs valid files, return 1
        else:
            # Delete invalid file
            os.remove(file_path)
    
    # Check conditions and return appropriate value
    if valid_file_count == 0:
        return 0  # No valid files found
    elif valid_file_count < n_locs:
        return 2  # Found at least one file but less than n_locs valid files

if __name__ == "__main__":

    # Define base url
    base_url = 'https://www.ncei.noaa.gov/data/local-climatological-data/'
    # Read YAML file
    with open('params/params.yaml', 'r') as file:
        data = yaml.safe_load(file)

    # Extract variables
    n_locs = data['download']['n_locs']
    year = data['download']['year']

    download_csv(base_url,year,n_locs)