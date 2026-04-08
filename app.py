from flask import Flask, jsonify, request
import psycopg2


app = Flask(__name__)

## Connexion à la base de données
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="sarr",
        user="postgres",
        password="thiane1226"
    )

## tester mon API
@app.route('/')
def hello():
    return "Hello, thiane ! bienvenue dans mon API Flask"


## récupérer toutes les personnes
@app.route('/people/person')
def get_people():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM person;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "lname": row[1],
            "fname": row[2],
            "timestamp": str(row[3])
        })

    return jsonify(result)

## recupérer une personne par son id
@app.route('/people/person/<int:id>')
def get_person_by_id(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM person WHERE id = %s;", (id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return jsonify({
            "id": row[0],
            "lname": row[1],
            "fname": row[2],
            "timestamp": str(row[3])
        })
    
    else:
        return jsonify({"message": "Person non trouvée"}), 404

## ajouter une personne
@app.route('/people/person/add')
def add_person_get():
    lname = request.args.get('lname')
    fname = request.args.get('fname')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO person (lname, fname, timestamp) VALUES (%s, %s, CURRENT_TIMESTAMP)",
        (lname, fname)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Person ajoutée avec succès"}), 201
  
 ## supprimer une personne par son id
@app.route('/people/person/delete/<int:id>')
def delete_person(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM person WHERE id = %s;", (id,))
    person = cur.fetchone()

    if person is None:
        cur.close()
        conn.close()
        return jsonify({"error": "Personne non trouvée"}), 404

    cur.execute("DELETE FROM person WHERE id = %s;", (id,))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"message": "Person supprimée avec succès"}), 200

if __name__ == '__main__':
    app.run(debug=True)