#########################
###    REQUIREMENTS   ###
#########################
'''
pip install -r requirements.txt
'''



#########################
###     LIBRARIES     ###
#########################

import os
# Absolute path to the folder where is the executed file
main_dir_path = os.path.dirname(os.path.abspath(__file__))
import sys
import json
import time
import requests
from urllib.parse import urlencode
import random as rd
from datetime import datetime

# Path to Functions
sys.path.append(main_dir_path)
from myfunctions import print_statistics

# Custom
import config
from tqdm import tqdm
from colorama import init, Fore, Back
init(autoreset = True)

# Database
from pymongo import MongoClient, errors


#########################
###  API'S PARAMETERS ###
#########################

# Limit first 10k observations
# API's URL
api_url = "https://api.inaturalist.org/v1/observations/"

# Define page range
while True:
    try:
        start_page = int(input(Fore.GREEN + "Please enter the first page: "))
        end_page = int(input(Fore.GREEN + "Please enter the last page (not incl.): " + Fore.RESET))
        if end_page <= start_page:
            print(Back.RED + "Invalid input. The last page must be greater than the first page.")
        else:
            break
    except ValueError:
        print(Back.RED + "Invalid input. Please enter an integer for both pages.")

# Localisation : Gironde
api_params = {
    "place_id" : "30139", #16.047 entries
    "order" : "asc",
    "quality_grade" : "research",
    "license" : "CC0,CC-BY,CC-BY-NC",
    "per_page" : "200", #81 pages
    "page" : "0"
}



#########################
###    JSON PARAMS    ###
#########################

# DB Directory Name
db_dir_name = "DB"

# Create a "DB" folder in the current folder if it doesn't exist
db_dir_path = os.path.join(main_dir_path, db_dir_name)
os.makedirs(db_dir_path, exist_ok = True)



#########################
###    MONGO PARAMS   ###
#########################

client = MongoClient(config.CONNECTION_STRING)
db = client[config.DB_NAME]
collection = db[config.COLLECTION_NAME]



#########################
###      CUSTOM       ###
#########################

# Bar progression
bar_format = "{l_bar}{bar}| {n_fmt}/{total_fmt}" #Format
bar_ncols = 90 #Size
bar_colour = "GREEN" #valid choices: [#ff9900, BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]



#########################
###    LOGS PARAMS    ###
#########################

# LOGS Directory Name
log_dir_name = "LOGS"

# Create a "LOGS" folder in the current folder if it doesn't exist
log_dir_path = os.path.join(main_dir_path, log_dir_name)
os.makedirs(log_dir_path, exist_ok = True)

# LOG Full file name
log_file_name = f"log_{start_page}-{end_page - 1}.txt"

# Full path to LOG file
log_file_path = os.path.join(log_dir_path, log_file_name)



#>>>>>>>>>>>>>>>>>>>>>>>#
#>>    START LOGS     >>#
#>>>>>>>>>>>>>>>>>>>>>>>#

# Open the file in write mode
log_f = open(log_file_path, "w")

# Redirect standard output to the log file
sys.stdout = log_f # log_f.close() is after the Main Code.



#>>>>>>>>>>>>>>>>>>>>>>>#
#>>       MAIN        >>#
#>>>>>>>>>>>>>>>>>>>>>>>#

# Start time
start_time = datetime.now()
print("****************************************")
print(f"Webscraping API started @ : {start_time}")
print("****************************************")

# Progression bar
pbar = tqdm(total = end_page - start_page, desc="API requesting", bar_format = bar_format, ncols = bar_ncols, colour = bar_colour)

# Navigate through the webpages (range number)
for n in range(start_page, end_page): 

    # Update "page" API parameter
    api_params["page"] = str(n)

    # JSON File name
    file_name = f"{api_params['page']}.json"

    # Full path to JSON file (DB)
    json_file_path = os.path.join(db_dir_path, file_name)

    # Build url
    api_url_params = urlencode(api_params)
    full_api_url = f"{api_url}?{api_url_params}"
    print("\n")
    print(full_api_url)

    # Check the answer
    api_response = requests.get(full_api_url)
    print(api_response, "for page", api_params["page"])

    if api_response.status_code == 200:

        # Collect data via API
        data = api_response.json()["results"]

        # Write data in file
        with open(json_file_path, "w", encoding = "utf-8") as file:
            json.dump(data, file)

        print("File ", file_name, " saved successfully in the folder : ", db_dir_path)

        # Save data to DB
        try:
            result = collection.insert_many(data)
            print("MONGO DB - Inserted document IDs:")
            for id in result.inserted_ids:
                print(id)

        except errors.PyMongoError as e:
            print("An error occurred while inserting the document:", e)

        # Print if success
        print(f"Page {n} extracted successfully.")

        # Pause to manage the usage (max 100/min)
        time.sleep(2) #(rd.randint(5, 10))

    else:
        # Print if error and continue
        print(f"\nError {api_response.status_code} on page {n}.")
        continue

    # pbar update
    pbar.update(1)

# Close pbar object
pbar.close()

# Close MongoDB connexion
client.close()

# After the loop, record the end time
end_time = datetime.now()

#<<<<<<<<<<<<<<<<<<<<<<<#
#<<     END MAIN      <<#
#<<<<<<<<<<<<<<<<<<<<<<<#


#<<<<<<<<<<<<<<<<<<<<<<<#
#<<<     END LOGS    <<<#
#<<<<<<<<<<<<<<<<<<<<<<<#

# Stats in the log file
print_statistics(start_time, end_time, start_page, end_page)

# Restore standard output
sys.stdout = sys.__stdout__

# Close log file
log_f.close()

# Stats in the terminal
print(Fore.YELLOW)
print_statistics(start_time, end_time, start_page, end_page)
print(Fore.RESET)