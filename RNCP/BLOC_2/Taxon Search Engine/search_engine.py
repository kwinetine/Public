import os
main_dir_path = os.path.dirname(os.path.abspath(__file__)) #Absolute path to the folder where the executed file is located.
import pandas as pd
import sys
from datetime import datetime

# Path to Functions
sys.path.append(main_dir_path)
from taxonomy_functions import search_taxon_id_by_name, search_scientific_name_by_id


# Load file .parquet to Pandas DF
df = pd.read_parquet(r"C:\WORKSPACES\DATA\PROCESS\search_engine_db.parquet")


# Ask the user for input (scientific name or taxon_id)
user_input = input("Enter a scientific name or a taxon_id: ")

# Check if the input is a number (taxon_id) or a string (scientific name)
if user_input.isdigit():
    taxon_id = int(user_input)
    scientific_name = search_scientific_name_by_id(taxon_id, df)
    if scientific_name:
        print(f"Scientific name for Taxon ID {taxon_id} : {scientific_name}")
    else:
        print(f"No scientific name found for Taxon ID {taxon_id}")
else:
    user_string = user_input
    taxon_id = search_taxon_id_by_name(user_string, df)
    if taxon_id:
        print(f"Taxon ID for '{user_string}': {taxon_id}")
        # Get the current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Create a DataFrame with the results
        result_df = pd.DataFrame({"taxon_id": taxon_id, "search_string": user_string})

        # Save the result to a CSV file with the current date and time as the name
        result_csv_filename = f"result_{current_datetime}.csv"
        result_df.to_csv(result_csv_filename, index = False)
    else:
        print(f"No taxon ID found for '{user_string}'")
