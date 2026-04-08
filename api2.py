from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="bibliotheque",
        user="postgres",
        password="thiane1226",
        port="5432"
    )
    return conn

@app.route('/') 
def index():
    return jsonify({"message": "Bienvenue dans notre API!"})
## se conncetr sur la base de donne sqlite
@app.route('/api/v1/resources/books/all')
def get_books():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM livres;')
    livres = cur.fetchall()
    cur.close()
    conn.close()

    livres_list = []
    for livre in livres:
        livres_list.append({
            "id": livre[0],
            "titre": livre[1],
            "auteur": livre[2],
            "annee": livre[3],
            "niveau": livre[4]
        })

    return jsonify( livres_list )

## FILTRAGE des donnes avec l'année de publication, l'auteur ou l'id du livre
@app.route('/api/v1/resources/books/filter')
def get_book_by_annee():
    annee = request.args.get('annee')
    auteur = request.args.get('auteur')
    id= request.args.get('id')
    conn = get_db_connection()
    cur = conn.cursor()
    if annee :
        cur.execute('SELECT * FROM livres WHERE annee = %s;', (annee,))
    elif auteur:
        cur.execute('SELECT * FROM livres WHERE auteur = %s;', (auteur,))
    elif id:
        cur.execute('SELECT * FROM livres WHERE id = %s;', (id,))
    livres = cur.fetchall()
    cur.close()
    conn.close()
    
    livres_list = []
    for livre in livres:
        livres_list.append({
            "id": livre[0],
            "titre": livre[1],
            "auteur": livre[2],
            "annee": livre[3],
            "niveau": livre[4]
        })

    return jsonify( livres_list )

## affichage de tous les livres avec un filtrage plus flexible en utilisant plusieurs critères de recherche
@app.route('/api/v1/resources/books/tester')
def tester():
    auteur = request.args.get('auteur')
    annee = request.args.get('annee')
    id= request.args.get('id')
    titre = request.args.get('titre')
    niveau = request.args.get('niveau')
    
    requeste = 'SELECT * FROM livres WHERE  '
    params = []
    if id :
        requeste += ' id = %s AND '
        params.append(id)

    if titre:
        requeste += '  titre = %s AND ' 
        params.append(titre)

    if auteur:
        requeste += ' auteur = %s AND '
        params.append(auteur)
        
    if annee:
        requeste += ' annee = %s AND '
        params.append(annee)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(requeste[:-4] + ';', tuple(params))
    livres = cur.fetchall()
    cur.close()
    conn.close()
    livres_list = []
    for livre in livres:
        livres_list.append({
            "id": livre[0],
            "titre": livre[1],
            "auteur": livre[2],
            "annee": livre[3],
            "niveau": livre[4]
        })
    return jsonify( livres_list )
       

if __name__ == '__main__':  
    app.run(debug=True, port=5000)
