#########################
###     LIBRARIES     ###
#########################

import random as rd
import numpy as np
import requests  # HTTP Management
import shutil  # Files operations
import logging
import ast # for Abstract Syntax Trees
import os
# Create the logs directory if it doesn't exist
os.makedirs("static/logs", exist_ok = True)
os.makedirs("static/user_content", exist_ok = True)

from flask import Flask, render_template, request #, jsonify, url_for, flash, redirect
from keras.models import load_model
from keras.preprocessing import image
from keras import backend, layers
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from urllib.parse import urlparse
from datetime import datetime

from config import ProductionConfig, DevelopmentConfig, TestingConfig

from colorama import init, Fore, Back #BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE
init(autoreset = True)



#########################
###       FLASK       ###
#########################

app = Flask(__name__, template_folder = "templates")


# Get the environment from environment variable
ENV = os.getenv("FLASK_ENV", "development")

# If FLASK_ENV is not set, default to "testing"
if ENV is None:
    ENV = "testing"

# Load the config according to the detected environment.
if ENV == "production":
    app.config.from_object(ProductionConfig)
    print(Fore.RED + "##### PRODUCTION ENVIRONMENT : Specific configuration for production deployment loaded ! #####")
elif ENV == "development":
    app.config.from_object(DevelopmentConfig)
    print(Back.BLUE + "##### DEVELOPMENT ENVIRONMENT : Specific configuration for development deployment loaded ! #####")
elif ENV == "testing":
    app.config.from_object(TestingConfig)
    print(Fore.YELLOW + "##### TESTING ENVIRONMENT : Specific configuration for testing deployment loaded ! #####")
else:
    raise ValueError(Back.RED + "##### Invalid environment name ! #####")



#########################
###    USER INPUT     ###
#########################

confidence_limit = 0.95

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
log_filename = f"static/logs/session_{timestamp}.txt"

success_img_upload = "Image envoyée avec succès: "
error_not_img = "Le fichier sélectionné n'est pas une image ! "
error_img_nofile = "Vous n'avez pas sélectionné d'image ! "
error_link_field_empty = "Vous n'avez pas inséré d'URL ! "
error_link_field_image = "L'URL ne doit pas rediriger vers une image ! "



#########################
###      LOGGER       ###
#########################

logger = logging.getLogger("LAIFE_ID_logger")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(log_filename, encoding = "utf-8")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(lineno)d - %(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)



#########################
###    LOAD MODEL     ###
#########################

class FixedDropout(layers.Dropout):
    def _get_noise_shape(self, inputs):
        if self.noise_shape is None:
            return self.noise_shape
        symbolic_shape = backend.shape(inputs)
        noise_shape = [symbolic_shape[axis] if shape is None else shape for axis,
                       shape in enumerate(self.noise_shape)]
        return tuple(noise_shape)

model = load_model("model.h5", custom_objects = {"FixedDropout": FixedDropout(rate = 0.4)})

model.make_predict_function()

# Read data from file
with open("dictionary.txt") as f:
    data = f.read()

# Reconstruct data (string) as dictionary
d = ast.literal_eval(data)



#########################
###     FUNCTIONS     ###
#########################

def predict_label(img_path):
    i = image.load_img(img_path, target_size = (240, 240))
    i = image.img_to_array(i)/255.0
    i = i.reshape(1, 240, 240, 3)
    p = model.predict(i)

    predicted_class_index = np.argmax(p)
    confidence_cal = p[0][predicted_class_index]
    predicted_class = d[predicted_class_index]

    # If confidence calculate < confidence limit, special value
    if confidence_cal < confidence_limit:
        return "low_confidence", confidence_cal
    return predicted_class, confidence_cal


def get_random_anecdote(prediction):
    animal = prediction.replace("une ", "").replace("un ", "")  # delete un/une from prediction sentence
    with open(f"static/anecdotes/{animal}_anecdotes.txt", "r", encoding = "utf-8") as f:
        anecdotes = f.readlines()
    return rd.choice(anecdotes)

app.jinja_env.globals.update(get_random_anecdote = get_random_anecdote)



#########################
###      ROUTES       ###
#########################

@app.route("/", methods=["GET", "POST"])
def main():
    return render_template("index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return app.send_static_file(filename)

@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/predictions.html")
def predictions():
    return render_template("predictions.html")

@app.route("/gestion.html")
def gestion():
    return render_template("gestion.html")

@app.route("/linkimg", methods = ("GET", "POST"))
def linkimg():
    error = None
    if request.method == "POST":

        # IMAGE parameters
        if request.form["action"] == "Envoyer image":
            img = request.files["my_image"]

            # Check if no file was selected
            if not img:
                error = error_img_nofile
                logger.error(error)

            else:
                # Check if the file is an image
                try:
                    Image.open(BytesIO(img.read()))
                    img.seek(0)  # Rewind the file to play it again
                except UnidentifiedImageError:
                    error = error_not_img
                    logger.error(error)

                else:
                    img_path = "static/user_content/" + img.filename
                    img.save(img_path)
                    a = img.filename
                    m, confidence = predict_label(img_path)

                    logger.info(f"{success_img_upload} {img_path}")
                    logger.info(f"{m} {confidence}")

                    confidence = "{:.3f} %".format(confidence * 100)
                    return render_template("predictions.html", prediction = m, confidence = confidence, a = a)

    return render_template("predictions.html", error = error)


@app.route("/linkurl", methods = ("GET", "POST"))
def linkurl():
    error = None
    if request.method == "POST":
        # URL parameters
        link_url = request.form["linkurl"]

        # Check if the link field is empty
        if not link_url:
            error = error_link_field_empty
            logger.error(error)
        else:
            parsed_url = urlparse(link_url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                error = error_link_field_image
                logger.error(error)
            else:
                filename = os.path.basename(parsed_url.path)  # Use only URL path for the file name

                try:
                    r = requests.get(link_url, stream = True)
                except requests.exceptions.RequestException:
                    error = error_link_field_image
                    logger.error(error)
                    return render_template("predictions.html", error = error)

                # Check if the content is an image
                if "image" in r.headers["Content-Type"]:

                    if r.status_code == 200:
                        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                        r.raw.decode_content = True

                        # Open a local file with wb (write binary) permission.
                        with open("static/user_content/" + filename, "wb") as f:
                            shutil.copyfileobj(r.raw, f)

                        img_path = "static/user_content/" + filename
                        a = filename
                        m, confidence = predict_label(img_path)

                        logger.info(f"{success_img_upload} {img_path}")
                        logger.info(f"{m} {confidence}")

                        confidence = "{:.3f} %".format(confidence * 100)
                        return render_template("predictions.html", prediction = m, confidence = confidence, a = a)

                    else:
                        error = error_link_field_image
                        logger.error(error)

                else:
                    error = error_link_field_image
                    logger.error(error)

    return render_template("predictions.html", error = error)



#########################
###        RUN        ###
#########################

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = "2024")