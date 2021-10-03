import os
from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import click
from flask.cli import with_appcontext
from werkzeug.security import check_password_hash, generate_password_hash
from mailSender import  emailSender, mailBody


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
                organ.nom = nom

            if 'adresse' in request_data:
                adresse = request_data['adresse']
                organ.adresse = adresse

            if 'email' in request_data:
                email = request_data['email']
                organ.email = email

            if 'password' in request_data:
                return make_response(jsonify({"error": "Access denied, you can request password"}), 404)

            if 'telephone' in request_data:
                telephone = request_data['telephone']
                organ.telephone = telephone
            if 'num_registre' in request_data:
                num_registre = request_data['num_registre']
                organ.num_registre = num_registre

            if 'nom_banque' in request_data:
                nom_banque = request_data['nom_banque']
                organ.nom_banque = nom_banque

            if 'iban' in request_data:
                iban = request_data['iban']
                organ.iban = iban

            if 'tva' in request_data:
                tva = request_data['tva']
                organ.tva = tva

            if 'site_internet' in request_data:
                site_internet = request_data['site_internet']
                organ.site_internet = site_internet
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
            user = {"id": organ.id, "email": organ.email, "name": organ.nom, "siteWeb": organ.site_internet,
                    "phone": organ.telephone, "adress": organ.adresse}
            return jsonify(user)
        except AssertionError as e:
            print(str(e))
            return make_response(jsonify({"error": "Authentification failed"}), 404)
    return make_response(jsonify({"error": "Data not found"}), 404)


@app.route("/organisations/register", methods=['POST'])
def register():
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
            new_organ = Organisation.query.filter_by(email=new_organ.email).first()
            user = {"id": new_organ.id, "email": new_organ.email, "name": new_organ.nom,
                    "siteWeb": new_organ.site_internet,
                    "phone": new_organ.telephone, "adress": new_organ.adresse}
            return jsonify(user)
        except AssertionError as e:
            print(str(e))
            return make_response(jsonify({"error": "Authentification failed"}), 404)
    return make_response(jsonify({"error": "Data not found"}), 404)

@app.route("/organisations/forgot", methods=['POST'])
@cross_origin()
def forgot():
    request_data = request.get_json()
    if request_data:
        email = ''
        if 'email' in request_data:
            email = request_data['email']
        else:
            return make_response(jsonify({"error": "Attribut email required"}), 404)

        try:
            organ = Organisation.query.filter_by(email=email).first()
            if not organ:
                return make_response(jsonify({"error": "Utilisateur non inscrit"}), 400)
            token = organ.get_token()
            print('token: ', token)
            text, html = mailBody(token, organ.nom)
            emailSender(mailReceive=email, text=text, html=html, sujet='Dassolution | Réinitialisation de votre mot de passe')
            return make_response(jsonify({"ok": "Email sended"}), 200)
        except AssertionError as e:
            print(str(e))
            return make_response(jsonify({"error": "Authentification failed"}), 404)
    return make_response(jsonify({"error": "Data not found"}), 404)

@app.route("/organisations/reset/<token>", methods=['GET', 'POST'])
def resetPassword(token):
    if request.method == "GET":
        organ = Organisation.verify_token(token)
        if organ is None:
            return make_response(jsonify({"error": "Token invalide ou déja expiré, Veuillez ressayer s'il vous plaît."}), 404)
        return make_response(jsonify({"success": "OK"}), 200)

    if request.method == "POST":
        organ = Organisation.verify_token(token)
        if organ is None:
            return make_response(
                jsonify({"error": "Token invalide ou déja expiré, Veuillez ressayer s'il vous plaît."}), 404)

        request_data = request.get_json()
        if 'password' in request_data:
            password = request_data['password']
        else:
            return make_response(jsonify({"error": "Attribut password required"}), 404)

        organ.password = generate_password_hash(password, method='sha256')
        try:
            db.session.commit()
            return jsonify(organ.serialize())
        except AssertionError as e:
            print(str(e))
            return make_response(jsonify({"error": "modification failed"}), 404)
    return make_response(jsonify({"error": "Data not found"}), 404)


@app.route("/clients", methods=['POST'])
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

            find = Client.query.filter_by(email=email).first()
            if find:
                return jsonify(find.serialize())

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
                client.nom = nom
            else:
                return make_response(jsonify({"error": "Attribut nom required"}), 404)

            if 'adresse' in request_data:
                adresse = request_data['adresse']
                client.adresse = adresse
            if 'email' in request_data:
                email = request_data['email']
                client.email = email

            if 'telephone' in request_data:
                telephone = request_data['telephone']
                client.telephone = telephone

            if 'site_internet' in request_data:
                site_internet = request_data['site_internet']
                client.site_internet = site_internet
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
        num_facture, devise, date_echeance, date_debut, description, client_id, total, ht, taxe, etat, client_name, organisation_id = None, None, None, None, None, None, None, None, None, None, None, None
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

            if 'total' in request_data:
                total = request_data['total']
            else:
                return make_response(jsonify({"error": "Attribut total required"}), 404)

            if 'taxe' in request_data:
                taxe = request_data['taxe']
            else:
                return make_response(jsonify({"error": "Attribut taxe required"}), 404)

            if 'ht' in request_data:
                ht = request_data['ht']
            else:
                return make_response(jsonify({"error": "Attribut HT required"}), 404)

            if 'etat' in request_data:
                etat = request_data['etat']
            else:
                return make_response(jsonify({"error": "Attribut Etat required"}), 404)

            if 'client_name' in request_data:
                client_name = request_data['client_name']
            else:
                return make_response(jsonify({"error": "Attribut client_name required"}), 404)

            if 'organisation_id' in request_data:
                organisation_id = request_data['organisation_id']
            else:
                return make_response(jsonify({"error": "Attribut organisation_id required"}), 404)

            facture = Facture(num_facture=num_facture, devise=devise, date_echeance=date_echeance,
                              date_debut=date_debut, description=description, total=total, taxe=taxe, ht=ht, etat=etat,
                              client_id=client_id, client_name=client_name, organisation_id=organisation_id)

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
        print('facture find :', facture, "requestData :", request_data)
        if request_data:
            if 'num_facture' in request_data:
                num_facture = request_data['num_facture']
                facture.num_facture = num_facture

            if 'devise' in request_data:
                devise = request_data['devise']
                facture.devise = devise

            if 'date_echeance' in request_data:
                date_echeance = request_data['date_echeance']
                facture.date_echeance = date_echeance

            if 'date_debut' in request_data:
                date_debut = request_data['date_debut']
                facture.date_debut = date_debut

            if 'description' in request_data:
                description = request_data['description']
                facture.description = description

            if 'total' in request_data:
                total = request_data['total']
                facture.total = total

            if 'taxe' in request_data:
                taxe = request_data['taxe']
                facture.taxe = taxe

            if 'ht' in request_data:
                ht = request_data['ht']
                facture.ht = ht

            if 'etat' in request_data:
                etat = request_data['etat']
                facture.etat = etat

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
        description, quantite, prix, total, taxe, facture_id = None, None, None, None, None, None
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
                article.description = description

            if 'quantite' in request_data:
                quantite = request_data['quantite']
                article.quantite = quantite

            if 'prix' in request_data:
                prix = request_data['prix']
                article.prix = prix

            if 'total' in request_data:
                total = request_data['total']
                article.total = total

            if 'taxe' in request_data:
                taxe = request_data['taxe']
                article.taxe = taxe
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
    app.run()
