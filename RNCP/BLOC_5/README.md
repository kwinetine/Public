# Sitemap
|_ Life_ID
    |_ static *contains data: images, anecdotes, etc.*
        |_ anecdotes *the DB of anecdotes*
            |_ bee_anecdotes.txt
            |_ ladybug_anecdotes.txt
            |_ butterfly_anecdotes.txt
        |
        |_ assets
            |_ css
            |_ js
            |_ webfonts
        |
        |_ doc_content *downloadable documents*
            |_ impact_mapping_bloc6.drawio.xml
            |_ etc.
        |
        |_ images *folder containing the website's images*
            |_ banner.jpg
            |_ Etc.
        |
        |_ user_content *folder containing user's images sent to the server*
            |_ Etc.
        |
        |_ favicon.ico
    |
    |_ templates *folder with .html templates*
        |_ index.html
        |_ predictions.html
        |_ management.html
    |
    |_ config.py *FLASK configuration file*
    |_ dictionary.txt *file of names for predictions*
    |_ flaskapp.py *FLASK Application*
    |_ model.h5 *file containing the model*
    |_ requirements.txt *libraries*
|
|_ Dockerfile
|_ README.md


# Flask
- Lancer l'exécution du Script flaskapp.py :
python3 flaskapp.py


# Docker
docker build -t life_id .
<!--
"-t" to define the tag / to assign a pseudo-TTY device
-->
docker run -p 2024:2024 -it life_id
<!--
"-p" to define the port
"-it" to get interactive control over the container (not mandatory)
"-i" to get interactive
"-t" to assign a pseudo-TTY device and interact with the terminal
-->