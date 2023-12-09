#########################
###    REQUIREMENTS   ###
#########################
'''
pip install -r requirements.txt
'''



#########################
###     LIBRARIES     ###
#########################

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
# import matplotlib.pyplot as plt
import plotly.graph_objects as go
import os
main_dir_path = os.path.dirname(os.path.abspath(__file__))
# os.system("clear" if os.name == "posix" else "cls")
from colorama import init, Fore, Back
init(autoreset = True)




#########################
###       DATA        ###
#########################

# Load
file_name = "iNat_df_croco.parquet"
file_path = os.path.join(main_dir_path, file_name)
df_croco = pd.read_parquet(file_path)


# Prepare
X = df_croco[["latitude", "longitude"]].values
y = df_croco["taxon_id"].values.ravel()

# Split the data into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)




#########################
###        KNN        ###
#########################

# Standardize the feature set
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create a KNN classifier
knn = KNeighborsClassifier(n_neighbors = 5)

# Train the classifier
knn.fit(X_train, y_train)

# Create a dictionary that maps taxon_id to scientific_name
taxon_id_to_name = df_croco.drop_duplicates(subset = "taxon_id").set_index("taxon_id")["scientific_name"].to_dict()



#########################
###     FUNCTIONS     ###
#########################

# Check if float
def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print(Back.RED + "Invalid input. Please enter a number.")


# Prediction
def predict_species():
    # Ask the user for latitude and longitude
    latitude = get_float_input(Back.GREEN + "Please enter latitude (decimal): " + Back.RESET)
    longitude = get_float_input(Back.GREEN + "Please enter longitude (decimal): " + Back.RESET)

    data = np.array([[latitude, longitude]])

    # Standardize the data
    data = scaler.transform(data)

    # Use the KNN model to make a prediction
    prediction = knn.predict(data)

    # Get the scientific_name corresponding to the predicted taxon_id
    scientific_name = taxon_id_to_name[prediction[0]]

    # Print the predicted species
    print("")
    print(Back.MAGENTA + f"The predicted species is: {prediction[0]}, {scientific_name}" + Back.RESET)

    # Create a scatter geo plot
    fig = go.Figure(data = go.Scattergeo(
        lon = df_croco["longitude"],
        lat = df_croco["latitude"],
        mode = "markers",
        marker_color = "blue",
        name = "Model Data"
    ))

    # Add the user's location
    fig.add_trace(go.Scattergeo(
        lon = [longitude],
        lat = [latitude],
        mode = "markers",
        marker_color = "red",
        marker_size = 10,
        name = "User's location"
    ))

    # Update the layout
    fig.update_layout(
        title_text = "User location and Model Data",
        geo = dict(
            scope = "asia",
            showland = True,
            landcolor = 'rgb(243, 243, 243)',
            countrycolor = 'rgb(204, 204, 204)',
            lataxis = dict(range = [5, 40]),
            lonaxis = dict(range = [60, 110])
        ),
    )

    # Show the plot
    fig.show()

# Use the function
predict_species()
