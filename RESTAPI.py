<<<<<<< HEAD
import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)



def create_connection(user, password, database):
    # Paramètres de connexion à la base de données
    config = {
        'user': user,
        'password': password,
        'host': 'localhost',  # ou '127.0.0.1' si MariaDB est en écoute sur loca                                                                                                                                                             lhost
        'database': database,
        'raise_on_warnings': True
    }

    try:
        # Connexion à la base de données
        cnx = mysql.connector.connect(**config)
        print("Connexion à la base de données réussie.")
        return cnx

    except mysql.connector.Error as err:
        print(f"Erreur de connexion à la base de données : {err}")
        return None


# GET method to retrieve all utilisateurs from the database
@app.route('/utilisateurs', methods=['GET'])
def get_utilisateurs():
    connection = create_connection('root', 'arnaud', 'sondage_database')
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM utilisateurs")
            utilisateurs = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify(utilisateurs)
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return jsonify({"error": "An error occurred while retrieving utilisa                                                                                                                                                             teurs"}), 500
    else:
        return jsonify({"error": "Failed to connect to the database"}), 500

# POST method to add a new utilisateur to the database
@app.route('/utilisateurs', methods=['POST'])
def add_utilisateur():
    new_utilisateur = request.json
    connection = create_connection('root', 'arnaud', 'sondage_database')

    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO utilisateurs (Nom, Prenom, AdresseMail) VALUES (%s, %s, %s)",
                           (new_utilisateur['Nom'], new_utilisateur['Prenom'], new_utilisateur['AdresseMail']))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"success": "User added successfully"}), 201
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return jsonify({"error": "An error occurred while adding the user"}), 500
    else:
        return jsonify({"error": "Failed to connect to the database"}), 500
    
    
# DELETE method to delete an utilisateur from the database
@app.route('/utilisateurs/<int:id>', methods=['DELETE'])
def delete_utilisateur(id):
    connection = create_connection('root', 'arnaud', 'sondage_database')

    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM utilisateurs WHERE id = %s", (id,))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"message": "Utilisateur supprimé avec succès"}), 200
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return jsonify({"error": "An error occurred while deleting utilisate                                                                                                                                                             ur"}), 500
    else:
        return jsonify({"error": "Failed to connect to the database"}), 500

if __name__ == '__main__':
    app.run(host='192.168.0.48',debug=True,port=5000)
=======
import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)



def create_connection(user, password, database):
    # Paramètres de connexion à la base de données
    config = {
        'user': user,
        'password': password,
        'host': 'localhost',  # ou '127.0.0.1' si MariaDB est en écoute sur loca                                                                                                                                                             lhost
        'database': database,
        'raise_on_warnings': True
    }

    try:
        # Connexion à la base de données
        cnx = mysql.connector.connect(**config)
        print("Connexion à la base de données réussie.")
        return cnx

    except mysql.connector.Error as err:
        print(f"Erreur de connexion à la base de données : {err}")
        return None


# GET method to retrieve all utilisateurs from the database
@app.route('/utilisateurs', methods=['GET'])
def get_utilisateurs():
    connection = create_connection('root', 'arnaud', 'sondage_database')
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM utilisateurs")
            utilisateurs = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify(utilisateurs)
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return jsonify({"error": "An error occurred while retrieving utilisa                                                                                                                                                             teurs"}), 500
    else:
        return jsonify({"error": "Failed to connect to the database"}), 500

# POST method to add a new utilisateur to the database
@app.route('/utilisateurs', methods=['POST'])
def add_utilisateur():
    new_utilisateur = request.json
    connection = create_connection('root', 'arnaud', 'sondage_database')

    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO utilisateurs (Nom, Prenom, AdresseMail) VALUES (%s, %s, %s)",
                           (new_utilisateur['Nom'], new_utilisateur['Prenom'], new_utilisateur['AdresseMail']))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"success": "User added successfully"}), 201
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return jsonify({"error": "An error occurred while adding the user"}), 500
    else:
        return jsonify({"error": "Failed to connect to the database"}), 500
    
    
# DELETE method to delete an utilisateur from the database
@app.route('/utilisateurs/<int:id>', methods=['DELETE'])
def delete_utilisateur(id):
    connection = create_connection('root', 'arnaud', 'sondage_database')

    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM utilisateurs WHERE id = %s", (id,))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"message": "Utilisateur supprimé avec succès"}), 200
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return jsonify({"error": "An error occurred while deleting utilisate                                                                                                                                                             ur"}), 500
    else:
        return jsonify({"error": "Failed to connect to the database"}), 500

if __name__ == '__main__':
    app.run(host='192.168.0.48',debug=True,port=5000)
>>>>>>> 1d6dc82 ( Initial)
