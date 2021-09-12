import os
from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import click
from flask.cli import with_appcontext
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace("://", "ql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['DEBUG'] = True
app.secret_key = os.environ['SECRET_KEY']
app.config["CORS_HEADERS"] = "Content-Type"
db = SQLAlchemy(app)

CORS(app)


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
    print("create")


app.cli.add_command(create_tables)

migrate = Migrate(app, db)
from ressources.modules.models import *


@app.teardown_request
def checkin_db(exc):
    try:
        print("Removing db session.")
        db.session.remove()
    except AttributeError:
        pass


@app.route("/")
@cross_origin()
def index():
    return jsonify()


@app.route("/organisations", methods=['GET', 'POST'])
def getOrganisations():  # sourcery no-metrics
    if request.method == "GET":
        organs = Organisation.query.all()
        print("count:", len(organs))
        return jsonify([c.serialize() for c in organs])
    if request.method == "POST":
        request_data = request.get_json()
        nom, adresse, email, password, telephone, num_registre, nom_banque, iban, tva, site_internet = None, None, None, None, None, None, None, None, None, None
        print(nom, adresse, email, password, telephone, num_registre, nom_banque, iban, tva, site_internet)
        print(request_data)
        if request_data:
            if 'nom' in request_data:
                nom = request_data['nom']
            else:
                make_response(jsonify({"error": "Attribut nom required"}), 404)

            if 'adresse' in request_data:
                adresse = request_data['adresse']

            if 'email' in request_data:
                email = request_data['email']

            if 'password' in request_data:
                password = request_data['password']
            else:
                make_response(jsonify({"error": "Attribut nom required"}), 404)

            if 'telephone' in request_data:
                telephone = request_data['telephone']

            if 'num_registre' in request_data:
                num_registre = request_data['num_registre']

            if 'nom_banque' in request_data:
                nom_banque = request_data['nom_banque']

            if 'iban' in request_data:
                iban = request_data['iban']

            if 'tva' in request_data:
                tva = request_data['tva']

            if 'site_internet' in request_data:
                site_internet = request_data['site_internet']
            organ = Organisation(nom, adresse, email, password, telephone, num_registre, nom_banque, iban, tva,
                                 site_internet)
            try:
                db.session.add(organ)
                db.session.commit()
                return jsonify(organ.serialize())
            except AssertionError as e:
                print(str(e))
                return make_response(jsonify({"error": "insertion failed"}), 404)
        return make_response(jsonify({"error": "Data not found"}), 404)


@app.route("/organisations/<int:organisation_id>", methods=['GET', 'PUT', 'DELETE'])
def organisation(organisation_id):
    if request.method == "GET":
        organ = Organisation.query.get_or_404(organisation_id)
        return jsonify(organ.serialize())

    if request.method == "PUT":
        organ = Organisation.query.get_or_404(organisation_id)
        request_data = request.get_json()
        if request_data:
            if 'nom' in request_data:
                nom = request_data['nom']
            else:
                make_response(jsonify({"error": "Attribut nom required"}), 404)

            if 'adresse' in request_data:
                adresse = request_data['adresse']

            if 'email' in request_data:
                email = request_data['email']

            if 'password' in request_data:
                password = request_data['password']
            else:
                make_response(jsonify({"error": "Attribut nom required"}), 404)

            if 'telephone' in request_data:
                telephone = request_data['telephone']

            if 'num_registre' in request_data:
                num_registre = request_data['num_registre']

            if 'nom_banque' in request_data:
                nom_banque = request_data['nom_banque']

            if 'iban' in request_data:
                iban = request_data['iban']

            if 'tva' in request_data:
                tva = request_data['tva']

            if 'site_internet' in request_data:
                site_internet = request_data['site_internet']
            organ.nom, organ.adresse, organ.email, organ.telephone, organ.num_registre, organ.nom_banque, organ.iban, organ.tva, organ.site_internet, organ.password = nom, adresse, email, telephone, num_registre, nom_banque, iban, tva, site_internet, password
            try:
                db.session.commit()
                return jsonify(organ.serialize())
            except AssertionError as e:
                print(str(e))
                return make_response(jsonify({"error": "modification failed"}), 404)
        return make_response(jsonify({"error": "Data not found"}), 404)

    if request.method == "DELETE":
        organ = Organisation.query.get_or_404(organisation_id)
        db.session.delete(organ)
        db.session.commit()
        return make_response(jsonify({"status": "success"}), 204)


@app.route("/organisations/login", methods=['POST'])
def login():  # sourcery no-metrics

    request_data = request.get_json()
    if request_data:
        email = ''
        password = ''
        if 'email' in request_data:
            email = request_data['email']
        else:
            return make_response(jsonify({"error": "Attribut email required"}), 404)

        if 'password' in request_data:
            password = request_data['password']
        else:
            return make_response(jsonify({"error": "Attribut password required"}), 404)

        try:
            organ = Organisation.query.filter_by(email=email).first()
            if not organ or not check_password_hash(organ.password, password):
                return make_response(jsonify({"error": "Email et/ou mot de passe incorrect(s)"}), 400)
            return jsonify(organ.serialize())
        except AssertionError as e:
            print(str(e))
            return make_response(jsonify({"error": "Authentification failed"}), 404)
    return make_response(jsonify({"error": "Data not found"}), 404)


@app.route("/organisations/register", methods=['POST'])
def register():  # sourcery no-metrics

    request_data = request.get_json()
    if request_data:
        email = ''
        password = ''
        nom = ''
        if 'nom' in request_data:
            nom = request_data['nom']
        else:
            return make_response(jsonify({"error": "Attribut name required"}), 404)

        if 'email' in request_data:
            email = request_data['email']
        else:
            return make_response(jsonify({"error": "Attribut email required"}), 404)

        if 'password' in request_data:
            password = request_data['password']
        else:
            return make_response(jsonify({"error": "Attribut password required"}), 404)


        try:
            organ = Organisation.query.filter_by(email=email).first()
            if organ:
                return make_response(jsonify({"error": "Email existe déjà"}), 302)
            new_organ = Organisation(nom=nom, email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_organ)
            db.session.commit()
            return jsonify(new_organ.serialize())
        except AssertionError as e:
            print(str(e))
            return make_response(jsonify({"error": "Authentification failed"}), 404)
    return make_response(jsonify({"error": "Data not found"}), 404)


@app.route("/clients", methods=['GET', 'POST'])
@cross_origin()
def getClients():
    if request.method == "GET":
        clients = Client.query.all()
        print("count:", len(clients))
        return jsonify([c.serialize() for c in clients])
    if request.method == "POST":
        request_data = request.get_json()
        nom, adresse, email, telephone, site_internet, organisation_id = None, None, None, None, None, None
        print(nom, adresse, email, telephone, site_internet, 1)
        print(request_data)
        if request_data:
            if 'nom' in request_data:
                nom = request_data['nom']
            else:
                return make_response(jsonify({"error": "Attribut nom required"}), 404)

            if 'adresse' in request_data:
                adresse = request_data['adresse']

            if 'email' in request_data:
                email = request_data['email']

            if 'telephone' in request_data:
                telephone = request_data['telephone']

            if 'site_internet' in request_data:
                site_internet = request_data['site_internet']
            if 'organisation_id' in request_data:
                organisation_id = request_data['organisation_id']
            else:
                return make_response(jsonify({"error": "Attribut organisation_id required"}), 404)
            client = Client(nom, adresse, email, telephone, site_internet)
            client.organisation_id = int(organisation_id)
            try:
                db.session.add(client)
                db.session.commit()
                return jsonify(client.serialize())
            except AssertionError as e:
                print(str(e))
                return make_response(jsonify({"error": "insertion failed"}), 404)
        return make_response(jsonify({"error": "Data not found"}), 404)


@app.route("/clients/<int:client_id>", methods=['GET', 'PUT', 'DELETE'])
def client(client_id):
    if request.method == "GET":
        client = Client.query.get_or_404(client_id)
        return jsonify(client.serialize())

    if request.method == "PUT":
        client = Client.query.get_or_404(client_id)
        request_data = request.get_json()
        if request_data:
            if 'nom' in request_data:
                nom = request_data['nom']
            else:
                return make_response(jsonify({"error": "Attribut nom required"}), 404)

            if 'adresse' in request_data:
                adresse = request_data['adresse']

            if 'email' in request_data:
                email = request_data['email']

            if 'telephone' in request_data:
                telephone = request_data['telephone']

            if 'site_internet' in request_data:
                site_internet = request_data['site_internet']
            client.nom, client.adresse, client.email, client.telephone, client.site_internet = nom, adresse, email, telephone, site_internet
            try:
                db.session.commit()
                return jsonify(client.serialize())
            except AssertionError as e:
                print(str(e))
                return make_response(jsonify({"error": "modification failed"}), 404)
        return make_response(jsonify({"error": "Data not found"}), 404)

    if request.method == "DELETE":
        client = Client.query.get_or_404(client_id)
        try:
            db.session.delete(client)
            db.session.commit()
        except AssertionError as e:
            print(str(e))
            return make_response(jsonify({"error": "DELETE failed"}), 404)
        return make_response(jsonify({"status": "success"}), 204)


@app.route("/factures", methods=['GET', 'POST'])
def getFactures():
    if request.method == "GET":
        factures = Facture.query.all()
        print("count:", len(factures))
        return jsonify([c.serialize() for c in factures])
    if request.method == "POST":
        request_data = request.get_json()
        num_facture, devise, date_echeance, date_debut, description, client_id, organisation_id = None, None, None, None, None, None, None
        print(num_facture, devise, date_echeance, date_debut, description, 1)
        print(request_data)
        if request_data:
            if 'num_facture' in request_data:
                num_facture = request_data['num_facture']
            else:
                return make_response(jsonify({"error": "Attribut nom required"}), 404)

            if 'devise' in request_data:
                devise = request_data['devise']

            if 'date_echeance' in request_data:
                date_echeance = request_data['date_echeance']

            if 'date_debut' in request_data:
                date_debut = request_data['date_debut']

            if 'description' in request_data:
                description = request_data['description']

            if 'client_id' in request_data:
                client_id = request_data['client_id']
            else:
                return make_response(jsonify({"error": "Attribut client_id required"}), 404)

            if 'organisation_id' in request_data:
                organisation_id = request_data['organisation_id']
            else:
                return make_response(jsonify({"error": "Attribut organisation_id required"}), 404)

            facture = Facture(num_facture, devise, date_echeance, date_debut, description, client_id, organisation_id)

            try:
                db.session.add(facture)
                db.session.commit()
                return jsonify(facture.serialize())
            except AssertionError as e:
                print(str(e))
                return make_response(jsonify({"error": "insertion failed"}), 404)
        return make_response(jsonify({"error": "Data not found"}), 404)


@app.route("/factures/<int:facture_id>", methods=['GET', 'PUT', 'DELETE'])
def facture(facture_id):
    if request.method == "GET":
        facture = Facture.query.get_or_404(facture_id)
        return jsonify(facture.serialize())

    if request.method == "PUT":
        facture = Facture.query.get_or_404(facture_id)
        request_data = request.get_json()
        if request_data:
            if 'num_facture' in request_data:
                num_facture = request_data['num_facture']
            else:
                return make_response(jsonify({"error": "Attribut nom required"}), 404)

            if 'devise' in request_data:
                devise = request_data['devise']

            if 'date_echeance' in request_data:
                date_echeance = request_data['date_echeance']

            if 'date_debut' in request_data:
                date_debut = request_data['date_debut']

            if 'description' in request_data:
                description = request_data['description']
            facture.num_facture, facture.devise, facture.date_echeance, facture.date_debut, facture.description = num_facture, devise, date_echeance, date_debut, description
            try:
                db.session.commit()
                return jsonify(facture.serialize())
            except AssertionError as e:
                print(str(e))
                return make_response(jsonify(facture.serialize()), 200)
        return make_response(jsonify({"error": "Data not found"}), 404)

    if request.method == "DELETE":
        facture = Facture.query.get_or_404(facture_id)
        try:
            db.session.delete(facture)
            db.session.commit()
        except AssertionError as e:
            print(str(e))
            return make_response(jsonify({"error": "DELETE failed"}), 404)
        return make_response(jsonify({"status": "success"}), 204)


@app.route("/articles", methods=['GET', 'POST'])
def getArticles():
    if request.method == "GET":
        articles = Article.query.all()
        print("count:", len(articles))
        return jsonify([c.serialize() for c in articles])
    if request.method == "POST":
        request_data = request.get_json()
        description, quantite, prix, total, taxe, facture_id = None, None, None, None, None
        print(description, quantite, prix, total, taxe)
        print(request_data)
        if request_data:
            if 'description' in request_data:
                description = request_data['description']
            else:
                return make_response(jsonify({"error": "Attribut nom required"}), 404)

            if 'quantite' in request_data:
                quantite = request_data['quantite']
            else:
                return make_response(jsonify({"error": "Attribut quantité required"}), 404)

            if 'prix' in request_data:
                prix = request_data['prix']
            else:
                return make_response(jsonify({"error": "Attribut prix required"}), 404)

            if 'total' in request_data:
                total = request_data['total']
            else:
                return make_response(jsonify({"error": "Attribut total prix required"}), 404)

            if 'taxe' in request_data:
                taxe = request_data['taxe']

            if 'facture_id' in request_data:
                facture_id = request_data['facture_id']
            else:
                return make_response(jsonify({"error": "Attribut facture_id required"}), 404)
            article = Article(description, quantite, prix, total, taxe)
            article.facture_id = facture_id

            try:
                db.session.add(article)
                db.session.commit()
                return jsonify(article.serialize())
            except AssertionError as e:
                print(str(e))
                return make_response(jsonify({"error": "insertion failed"}), 404)
        return make_response(jsonify({"error": "Data not found"}), 404)


@app.route("/articles/<int:facture_id>", methods=['GET', 'PUT', 'DELETE'])
def articles(article_id):
    if request.method == "GET":
        article = Article.query.get_or_404(article_id)
        return jsonify(article.serialize())

    if request.method == "PUT":
        article = Article.query.get_or_404(article_id)
        request_data = request.get_json()
        if request_data:
            if 'description' in request_data:
                description = request_data['description']
            else:
                return make_response(jsonify({"error": "Attribut description required"}), 404)

            if 'quantite' in request_data:
                quantite = request_data['quantite']

            if 'prix' in request_data:
                prix = request_data['prix']

            if 'total' in request_data:
                total = request_data['total']

            if 'taxe' in request_data:
                taxe = request_data['taxe']
            article.description, article.quantite, article.prix, article.total, article.taxe = description, quantite, prix, total, taxe
            try:
                db.session.commit()
                return jsonify(article.serialize())
            except AssertionError as e:
                print(str(e))
                return make_response(jsonify({"error": "modification failed"}), 404)
        return make_response(jsonify({"error": "Data not found"}), 404)

    if request.method == "DELETE":
        article = Article.query.get_or_404(article_id)
        try:
            db.session.delete(article)
            db.session.commit()
        except AssertionError as e:
            print(str(e))
            return make_response(jsonify({"error": "DELETE failed"}), 404)
        return make_response(jsonify({"status": "success"}), 204)


if __name__ == '__main__':
    # db.create_all()
    # print("create")
    app.run()
