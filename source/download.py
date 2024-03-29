import yaml

# Read YAML file
with open('params/params.yaml', 'r') as file:
    data = yaml.safe_load(file)

# Extract variables
n_locs = data['download']['n_locs']
year = data['download']['year']


# Print variables
print("Number of Locations:", n_locs)
print("Year:", year)