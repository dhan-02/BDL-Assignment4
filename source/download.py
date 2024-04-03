import yaml
import os  
import pandas as pd  
import random  

def get_all_file_names(datafile_path):
    """
    Selects a random sample of files from the HTML file containing the list of files

    Args:
        datafile_path (str): Path to the HTML file containing the links

    Returns:
        list: A list of all file names.
    """
    # Validate input arguments
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

def download_html(base_url, year):
    # Validate input arguments
    if not isinstance(base_url, str) or not isinstance(year, int):
        raise ValueError("Invalid input provided for base_url or year.")
    if not base_url or not year:
        raise ValueError("base_url and year cannot be empty.")

    # Create a directory to store downloaded HTML file
    bash_command = "mkdir data/"
    os.system(bash_command)
    
    # Download HTML file containing data links
    current_dir = os.getcwd()
    bash_command = "wget -O {}/data/data_store.html {}access/{}".format(current_dir, base_url, year)
    # Execute the Bash command using os.system
    os.system(bash_command)

def is_valid_file(file_path, daily_avg_fields, monthly_avg_fields):
    """
    Checks if a CSV file contains valid data based on specified daily and monthly fields.

    Args:
        file_path (str): Path to the CSV file.
        daily_avg_fields (list): List of daily average fields to check.
        monthly_avg_fields (list): List of monthly average fields to check.

    Returns:
        bool: True if the file is valid, False otherwise.
    """

    # Validate input arguments
    if not isinstance(file_path, str) or not os.path.isfile(file_path):
        raise ValueError("Invalid file_path provided.")

    # Read the csv file
    df = pd.read_csv(file_path, low_memory=False)
    for daily_field, monthly_field in zip(daily_avg_fields, monthly_avg_fields):
        # Check if at least one pair of required fields is not empty
        if not df[daily_field].dropna().empty and not df[monthly_field].dropna().empty:
            return True
    return False

def download_csv(base_url, year, n_locs):
    """
    Downloads CSV files from a specified URL for a given year and number of locations.

    Args:
        base_url (str): Base URL for downloading files.
        year (str): Year for which data is to be downloaded.
        n_locs (int): Number of locations to download data for.

    Returns:
        int: Status code indicating success or failure of the download process.
            0: No valid files found.
            1: Found n_locs valid files.
            2: Found at least one file but less than n_locs valid files.
    """
    # Validate input arguments
    if not isinstance(base_url, str) or not isinstance(year, int) or not isinstance(n_locs, int):
        raise ValueError("Invalid input provided for base_url, year, or n_locs.")
    if not base_url or not year or n_locs <= 0:
        raise ValueError("base_url, year, and n_locs must be valid.")

    # Download HTML file containing data links
    download_html(base_url, year)
    list_files = get_all_file_names('data/data_store.html')
    random.shuffle(list_files)  # Shuffle the list of files

    # Define daily and monthly average fields
    daily_avg_fields = ['DailyAverageDryBulbTemperature', 
                        'DailyMaximumDryBulbTemperature', 
                        'DailyMinimumDryBulbTemperature',
                        'DailyAverageSeaLevelPressure',
                        'DailyAverageStationPressure']

    monthly_avg_fields = ['MonthlyMeanTemperature', 
                          'MonthlyMaximumTemperature', 
                          'MonthlyMinimumTemperature',
                          'MonthlySeaLevelPressure', 
                          'MonthlyStationPressure']

    valid_file_count = 0
    print("Searching for valid files......")
    for file_name in list_files:
        # Download file
        base_url_year = base_url + "access/" + str(year) + "/"
        download_url = f"{base_url_year}{file_name}"
        path = os.path.join(os.getcwd(), 'data')
        fetch_command = f"wget {download_url} -P {path} -q"
        os.system(fetch_command)        
        file_path = os.path.join(os.path.join(os.getcwd(), 'data'), file_name)
        # Check file validity
        if is_valid_file(file_path, daily_avg_fields, monthly_avg_fields):
            print(valid_file_count + 1, "out of", n_locs, "required files found")
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

    # Call the main function
    download_csv(base_url, year, n_locs)
