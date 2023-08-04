#########################
###    REQUIREMENTS   ###
#########################
'''
pip install selenium
pip install selenium-stealth
pip install python-dateutil
'''



#########################
###     LIBRARIES     ###
#########################

# System & Files
import os
# Absolute path to the folder where is the executed file
main_dir_path = os.path.dirname(os.path.abspath(__file__))
import csv
import sys
import random as rd

# Time
import time
from  datetime import datetime
from dateutil.parser import parse

# Webscraping
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Custom
from tqdm import tqdm



#########################
###      WEBSITE      ###
#########################

# Initalize URL
obs_base_url = "https://www.inaturalist.org/observations/"

# Define page range
start_page = 29995
end_page = 29999



#########################
###       XPATH       ###
#########################

xpath_error = '//*[@id="message"]'   # Error page
xpath_common_name = '//*[@id="ObservationShow"]/div[1]/div/div[1]/div[1]/div/span[1]/a[1]'
xpath_sci_name = '//*[@id="ObservationShow"]/div[1]/div/div[1]/div[1]/div/span[1]/a[2]'
xpath_picture = '/html/body/div[1]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/div/div/div/div/div/div/img'
xpath_date_obs = '//*[@id="ObservationShow"]/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div[1]/span[2]'
xpath_details_button = '/html/body/div[1]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div[2]/div[2]/div/button'
xpath_lat = '//*[@id="ObservationShow"]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div[2]/div[2]/div/ul/li/div/div[1]/div[1]/span[2]'
xpath_long = '//*[@id="ObservationShow"]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div[2]/div[2]/div/ul/li/div/div[1]/div[2]/span[2]'
xpath_precision = '//*[@id="ObservationShow"]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div[2]/div[2]/div/ul/li/div/div[1]/div[3]/span[2]'
xpath_continent = '//*[@id="ObservationShow"]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div[2]/div[2]/div/ul/li/div/div[2]/div[1]/span[2]/a'
xpath_country = '//*[@id="ObservationShow"]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div[2]/div[2]/div/ul/li/div/div[2]/div[1]/span[3]/a'
xpath_state_region = '//*[@id="ObservationShow"]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div[2]/div[2]/div/ul/li/div/div[2]/div[1]/span[4]/a'



#########################
###      CUSTOM       ###
#########################

# Bar progression format
bar_format = "{l_bar}{bar}| {n_fmt}/{total_fmt}"

# Bar progression size
bar_ncols = 90

# Bar progression colour
bar_colour = "#ff9900" #valid choices: [#ff9900, BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]



#########################
###    LOGS PARAMS    ###
#########################

# Create a "LOGS" folder in the current folder if it doesn't exist
log_dir = os.path.join(main_dir_path, "LOGS")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# LOG File name
log_file_name = f"log_{start_page}-{end_page-1}.txt"

# Full path to LOG file
log_file_path = os.path.join(log_dir, log_file_name)



#########################
###    CSV PARAMS     ###
#########################

# DB Directory Name
db_dir_name = "DB"

# Create a "DB" folder in the current folder if it doesn't exist
db_dir_path = os.path.join(main_dir_path, db_dir_name)
if not os.path.exists(db_dir_path):
    os.makedirs(db_dir_path)
    print(f"The directory '{db_dir_name}' created successfully in '{main_dir_path}' !\n'{db_dir_path}'")
else:
    print(f"The directory '{db_dir_path}' already exists.")

# CSV full file name
csv_file_name = f"inat_db_{start_page}-{end_page-1}.csv"

# Full path to CSV file
csv_file_path = os.path.join(db_dir_path, csv_file_name)

# Open CSV file in write mode
csv_file_open = open(csv_file_path, "w", newline = "", encoding = "utf-8")

# Create a CSV writer object
csv_writer = csv.writer(csv_file_open)

# Define column_names for CSV file
column_names = ["id", "common_name", "sci_name", "pict_url", "date_obs", "latitude", "longitude", "precision", "continent", "country", "state_region", "code_country", "url"]
"""
id = Page number 'n'
common_name = Common name
sci_name = Scientific name
pict_url = Full url to the image
date_obs = Date of observation
latitude
longitude
precision = Precision of lat/long
continent = In letters
country = Country in letters
state_region = State or region depending country
code_country = Country code alpha 2
url = Full url of observation
"""

# Define data structure when save to CSV file
"""
    See 'csv_struct' @line 292 (Main Code)
"""

# Write header row in CSV file
csv_writer.writerow(column_names)



#########################
###  SCRAP SETTINGS   ###
#########################

# WebDriver settings
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-setuid-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')
driver = webdriver.Chrome(options = chrome_options)

# Stealth settings
stealth(
    driver,
    languages = ["en-US", "en"],   #["fr-FR", "fr"],
    vendor = "Google Inc.",
    platform = "Win32",
    webgl_vendor = "Intel Inc.",
    renderer = "Intel Iris OpenGL Engine",
    fix_hairline = True,
)



#>>>>>>>>>>>>>>>>>>>>>>>#
#>>    START LOGS     >>#
#>>>>>>>>>>>>>>>>>>>>>>>#

# Open the file in write mode
log_f = open(log_file_path, 'w')

# Redirect standard output to the log file
sys.stdout = log_f # log_f.close() is after the Main Code.



#>>>>>>>>>>>>>>>>>>>>>>>#
#>>       MAIN        >>#
#>>>>>>>>>>>>>>>>>>>>>>>#

# Start time
start_time = datetime.now()
print("****************************************")
print(f"Webscraping started @ : {start_time}")
print(csv_file_path, "created successfully !")
print(log_file_path, "created successfully !")
print("****************************************")

# Random pages without repetition
#page_list = rd.sample(range(start_page, end_page), end_page - start_page)

# Loop
for n in tqdm(range(start_page, end_page), bar_format = bar_format, ncols = bar_ncols, colour = bar_colour):
    url = obs_base_url + str(n)
    driver.get(url)

    # Pause while the web page is loading
    time.sleep(3)   #rd.randint(2, 5)

    # Test if the page exists or not
    elements = driver.find_elements(By.XPATH, xpath_error)

    # Page doesn't exists
    if len(elements) > 0:
        print(f"\nLa page {n} n'existe pas ({url}).")

    # Page exists
    else:
        print(f"\n>>> La page {n} EXISTE ({url}) !")

        # Scrap info
        try:
            common_name = driver.find_element(By.XPATH, xpath_common_name).text
        except NoSuchElementException:
            print(f"Unable to find common name on page {n}.")
            common_name = ""

        try:
            sci_name = driver.find_element(By.XPATH, xpath_sci_name).text
        except NoSuchElementException:
            print(f"Unable to find scientific name on page {n}.")
            sci_name = ""

        try:
            pict_url = driver.find_element(By.XPATH, xpath_picture).get_attribute('src')
        except NoSuchElementException:
            print(f"Unable to find picture url on page {n}.")
            pict_url = ""

        try:
            date_obs = driver.find_element(By.XPATH, xpath_date_obs).text

            # Convert the string to a datetime object
            date_obj = parse(date_obs, fuzzy = True)
            date_parse = date_obj.date()

            # Convert the date to the desired French format
            date_fr = date_parse.strftime("%d/%m/%Y")

        except (NoSuchElementException, ValueError):
            print(f"Unable to find date or format incorrect on page {n}.")
            date_fr = ""

        try:
            # Click to show Details
            details_button = driver.find_element(By.XPATH, xpath_details_button)
            details_button.click()
            time.sleep(1)
            lat = driver.find_element(By.XPATH, xpath_lat).text
            lat = float(lat)
        except (NoSuchElementException, ValueError):
            print(f"Unable to find or parse latitude on page {n}.")
            lat = 0.0

        try:
            long = driver.find_element(By.XPATH, xpath_long).text
            long = float(long)
        except (NoSuchElementException, ValueError):
            print(f"Unable to find or parse longitude on page {n}.")
            long = 0.0

        try:
            precision = driver.find_element(By.XPATH, xpath_precision).text
        except (NoSuchElementException, ValueError):
            print(f"Unable to find precision on page {n}.")
            precision = ""

        try:
            continent = driver.find_element(By.XPATH, xpath_continent).text
        except NoSuchElementException:
            print(f"Unable to find continent on page {n}.")
            continent = ""

        try:
            country = driver.find_element(By.XPATH, xpath_country).text
        except NoSuchElementException:
            print(f"Unable to find country on page {n}.")
            country = ""

        try:
            state_region = driver.find_element(By.XPATH, xpath_state_region).text
            
            # Split state_region value
            try:
                state_region_parts = state_region.split(", ")
                state_region = state_region_parts[0]
                code_country = state_region_parts[1]
            except IndexError:
                state_region = ""
                code_country = ""
                
        except NoSuchElementException:
            print(f"Unable to find state/region on page {n}.")
            state_region = ""
            code_country = ""

        # Define data structure for CSV file
        csv_struct = [n, common_name, sci_name, pict_url, date_fr, lat, long, precision, continent, country, state_region, code_country, url]

        # Write in CSV File
        csv_writer.writerow(csv_struct)

# Close CSV writer object
csv_file_open.close()

# Close WebDriver
driver.quit()

#<<<<<<<<<<<<<<<<<<<<<<<#
#<<     END MAIN      <<#
#<<<<<<<<<<<<<<<<<<<<<<<#



#########################
###     RUN TIME      ###
#########################

# After the loop, record the end time
end_time = datetime.now()

# Calculate the total_time and total_pages
total_time = (end_time - start_time)
total_pages = (end_page - start_page)

# Calculate the total time in days, hours, minutes, and seconds
total_seconds = total_time.total_seconds()
days, remainder = divmod(total_seconds, 86400)
hours, remainder = divmod(remainder, 3600)
minutes, seconds = divmod(remainder, 60)
statistics = (total_pages / (total_seconds / 60))

# Print the time
print("\n\n\n****************************************")
print("Webscraping started @ :", start_time)
print("Webscraping finished @ :", end_time)
print(total_pages, "webscraped page(s).")
print("\nThe execution took :", int(days), "days,", int(hours), "hours,", int(minutes), "minutes and", int(seconds), "seconds.")
print(f"Statistics : {statistics:.2f} pages/min.")
print("****************************************")



#<<<<<<<<<<<<<<<<<<<<<<<#
#<<<     END LOGS    <<<#
#<<<<<<<<<<<<<<<<<<<<<<<#

# Restore standard output
sys.stdout = sys.__stdout__

# Close log file
log_f.close()
