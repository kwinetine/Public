#########################
###     LIBRARIES     ###
#########################

import json

# Web App
from flask import Flask, request, Blueprint, jsonify, render_template
# render_template pour générer une réponse HTML en utilisant un modèle pré-défini et des données dynamiques

# Spark
import findspark
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from engine import RecommendationEngine


# Créez un Blueprint Flask
main = Blueprint('main', __name__)


# Initialisez Spark
findspark.init()

# Définissez la route principale ("/")
@main.route("/", methods=["GET", "POST", "PUT"])

def home():
    return render_template("index.html")


# Définissez la route pour récupérer les détails d'un film
@main.route("/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    # Code pour récupérer les détails du film avec l'id spécifié
    movie = RecommendationEngine.get_movie_details(movie_id)
    
    # et renvoyer les données au format JSON
    return jsonify(movie)


# Définissez la route pour ajouter de nouvelles évaluations pour les films
@main.route("/newratings/<int:user_id>", methods=["POST"])
def new_ratings(user_id):
    # Code pour vérifier si l'utilisateur existe déjà
    if engine.is_user_known(user_id):
        # Récupérez les évaluations depuis la requête et ajoutez-les au moteur de recommandation
        ratings = request.get_json()  # Supposons que les évaluations sont envoyées en tant que JSON dans la requête
        engine.add_ratings(user_id, ratings)

    else:
        # Si l'utilisateur n'existe pas, créez-le
        user_id = engine.create_user()

        # Récupérez les évaluations depuis la requête et ajoutez-les au moteur de recommandation
        ratings = request.get_json()  # Supposons que les évaluations sont envoyées en tant que JSON dans la requête
        engine.add_ratings(user_id, ratings)

    # Renvoyez l'identifiant de l'utilisateur si c'est un nouvel utilisateur, sinon renvoyez une chaîne vide
    if not engine.is_user_known(user_id):
        return str(user_id)
    else:
        return ""


# Définissez la route pour ajouter des évaluations à partir d'un fichier
@main.route("/<int:user_id>/ratings", methods=["POST"])
def add_ratings(user_id):
    # Code pour récupérer le fichier téléchargé depuis la requête
    file = request.files['ratings_file']

    # Lisez les données du fichier et ajoutez-les au moteur de recommandation

    # Renvoyez un message indiquant que le modèle de prédiction a été recalculé
    return "Le modèle de prédiction a été recalculé avec succès."

    # Code pour récupérer le fichier téléchargé depuis la requête


# Définissez la route pour obtenir la note prédite d'un utilisateur pour un film
@main.route("/<int:user_id>/ratings/<int:movie_id>", methods=["GET"])
def movie_ratings(user_id, movie_id):
    # Code pour prédire la note de l'utilisateur pour le film spécifié
    # Renvoyez la note prédite au format texte


# Définissez la route pour obtenir les meilleures évaluations recommandées pour un utilisateur
@main.route("/<int:user_id>/ratings/<int:movie_id>", methods=["GET"])
def movie_ratings(user_id, movie_id):
    # Code pour prédire la note de l'utilisateur pour le film spécifié
    # Renvoyez la note prédite au format texte


# Définissez la route pour obtenir les évaluations d'un utilisateur
@main.route("/ratings/<int:user_id>", methods=["GET"])
def get_ratings_for_user(user_id):
    # Code pour récupérer les évaluations de l'utilisateur spécifié
    ratings = engine.get_ratings_for_user(user_id)

    # Renvoyez les évaluations au format JSON
    return jsonify(ratings)


# Créer l'application Flask
def create_app(spark_context, movies_set_path, ratings_set_path):
    # Initialisez le moteur de recommandation avec le contexte Spark et les jeux de données
    recommendation_engine = RecommendationEngine(spark_context, movies_set_path, ratings_set_path)

    # Créez une instance de l'application Flask
    app = Flask(__name__)

    # Enregistrez le Blueprint "main" dans l'application
    app.register_blueprint(main)

    # Configurez les options de l'application Flask
    

    # Renvoyez l'application Flask créée
    return app