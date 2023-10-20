#########################
###    REQUIREMENTS   ###
#########################
'''
pip install -r requirements.txt
'''



#########################
###     LIBRARIES     ###
#########################

import json
import bson
import time
import os
import string
import random as rd
import numpy as np
from colorama import init, Fore, Back
init(autoreset = True)




# Function to generate random string
rd.seed(42)
def random_string(length):
    letters = string.ascii_lowercase
    return "".join(rd.choice(letters) for i in range(length))

# Generate data
data = {random_string(10): random_string(100) for _ in range(100000)}

# Initialize lists
json_write_times = []
json_read_times = []
bson_write_times = []
bson_read_times = []

# Loop Function
for _ in range(20):
    # JSON Write Speed Test
    start_time = time.time()
    with open("test.json", "w") as f:
        json.dump(data, f)
    json_write_times.append(time.time() - start_time)

    # JSON Read Speed Test
    start_time = time.time()
    with open("test.json", "r") as f:
        data = json.load(f)
    json_read_times.append(time.time() - start_time)

    # BSON Write Speed Test
    start_time = time.time()
    with open("test.bson", "wb") as f:
        f.write(bson.BSON.encode(data))
    bson_write_times.append(time.time() - start_time)

    # BSON Read Speed Test
    start_time = time.time()
    with open("test.bson", "rb") as f:
        data = bson.BSON(f.read()).decode()
    bson_read_times.append(time.time() - start_time)

# Clean up
os.remove("test.json")
os.remove("test.bson")

# Print Stats
print(Back.LIGHTGREEN_EX + f"JSON : Mean WRITE time: {np.mean(json_write_times)} seconds")
print(Back.LIGHTGREEN_EX + f"JSON : Mean Read time: {np.mean(json_read_times)} seconds")
print(Back.LIGHTMAGENTA_EX + f"BSON : Mean WRITE time: {np.mean(bson_write_times)} seconds")
print(Back.LIGHTMAGENTA_EX + f"BSON : Mean Read time: {np.mean(bson_read_times)} seconds")
