# Movies Recommandation Motor with SPARK & DOCKER

## Guidelines

### Launch Docker
docker build

## Objectif

## Description
### Database : MovieLens Latest Datasets (recommended for education and development)
These datasets will change over time, and are not appropriate for reporting research results.

Small: 100,000 ratings and 3,600 tag applications applied to 9,000 movies by 600 users. Last updated 9/2018.
File : ml-latest-small.zip (size: 1 MB)

### Usual statistics
Nombre de catégorie
Mieux notés par catégorie / toute catégorie confondue
Etc.

Mettre en parquet => SPARK SQL

## Notes

## Roadmap

## Architecture

## Technos
Collaborative Filtering (CF) is a method of making automatic predictions about the interests of a user by learning its preferences (or taste) based on information of his engagements with a set of available items, along with other users’ engagements with the same set of items. in other words, CF assumes that, if a person A has the same opinion as person B on some set of issues X={x1,x2,…}, then A is more likely to have B‘s opinion on a new issue y than to have the opinion of any other person that doesn’t agree with A on X.


ALS algorythm with SPARK ML
Alternating Least Square (ALS) is also a matrix factorization algorithm and it runs itself in a parallel fashion. ALS is implemented in Apache Spark ML and built for a larges-scale collaborative filtering problems. ALS is doing a pretty good job at solving scalability and sparseness of the Ratings data, and it’s simple and scales well to very large datasets.

ALS est un algorithme itératif qui utilise la décomposition en valeurs singulières pour résoudre les problèmes d'optimisation et minimiser l'erreur de prédiction dans les systèmes de filtrage collaboratif.
