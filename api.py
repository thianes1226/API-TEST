from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

#  BASE DE DONNEES
def get_db_connection():
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    return conn

##  dictionnaires des livres
livres = [
    {"titre": "Learning Python", "auteur": "Mark Lutz", "annee": 2013, "niveau": "Intermédiaire", "id": 1},
    {"titre": "Python Crash Course", "auteur": "Eric Matthes", "annee": 2019, "niveau": "Débutant", "id": 2},
    {"titre": "Fluent Python", "auteur": "Luciano Ramalho", "annee": 2022, "niveau": "Avancé", "id": 3},
    {"titre": "Effective Python", "auteur": "Brett Slatkin", "annee": 2020, "niveau": "Intermédiaire", "id": 4},
    {"titre": "Python Cookbook", "auteur": "David Beazley & Brian K. Jones", "annee": 2013, "niveau": "Avancé", "id": 5}
]

## Tester notre  API 
@app.route('/')
def hello():
    return 'Bienvenue dans notre API!'

##  recuperer tOUS les  dictionnaires des livres LIVRES 
@app.route('/api/v1/resources/books/all')
def get_books():
    return jsonify(livres)

## FILTRAGE des donnes 
@app.route('/api/v1/resources/books')
def get_book_by_id():
    id = request.args.get('id')
    if id:
        id = int(id)
        for livre in livres:
            if livre.get('id') == id:
                return jsonify(livre)

    return jsonify({"message": "Livre non trouvé"})

## se connecter avec SQLITE (CORRIGE) 



if __name__ == '__main__':
    app.run(debug=True, port=5000)