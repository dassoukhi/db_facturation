from app import db, app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

assert isinstance(db.Model, object)


class Organisation(db.Model):
    __tablename__ = 'organisation'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    adresse = db.Column(db.String())
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(), nullable=False)
    telephone = db.Column(db.String())
    num_registre = db.Column(db.String(50))
    nom_banque = db.Column(db.String(100))
    iban = db.Column(db.String())
    tva = db.Column(db.Float(3))
    site_internet = db.Column(db.String(80))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    factures = db.relationship('Facture', backref='organisation', lazy=True)
    clients = db.relationship('Client', backref='organisation', lazy=True)

    def __init__(self, nom, email, password, adresse="", telephone="", site_internet="", num_registre="", nom_banque="",
                 iban="", tva=0.0):
        self.nom = nom
        self.adresse = adresse
        self.email = email
        self.password = password
        self.telephone = telephone
        self.num_registre = num_registre
        self.nom_banque = nom_banque
        self.iban = iban
        self.tva = tva
        self.site_internet = site_internet

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def get_token(self, expires_sec=3600):
        serial = Serializer(app.config['SECRET_KEY'], expires_in=expires_sec)
        return serial.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        serial = Serializer(app.config['SECRET_KEY'])
        try:
            organ_id = serial.loads(token)['id']
        except:
            return None
        return Organisation.query.get(organ_id)

    def serialize(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'adresse': self.adresse,
            'email': self.email,
            'telephone': self.telephone,
            'num_registre': self.num_registre,
            'nom_banque': self.nom_banque,
            'iban': self.iban,
            'tva': self.tva,
            'site_internet': self.site_internet,
            'created': self.created,
            'clients': [c.serialize() for c in self.clients],
            'factures': [f.serialize() for f in self.factures]
        }


class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    adresse = db.Column(db.String())
    email = db.Column(db.String(120), unique=True)
    telephone = db.Column(db.String())
    site_internet = db.Column(db.String(50))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))
    factures = db.relationship('Facture', backref='client', lazy=True)

    def __init__(self, nom, adresse, email, telephone, site_internet):
        self.nom = nom
        self.adresse = adresse
        self.email = email
        self.telephone = telephone
        self.site_internet = site_internet

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'adresse': self.adresse,
            'email': self.email,
            'telephone': self.telephone,
            'site_internet': self.site_internet,
            'created': self.created,
            'organisation_id': self.organisation_id,
            'factures': [f.serialize() for f in self.factures]
        }


class Facture(db.Model):
    __tablename__ = 'facture'

    id = db.Column(db.Integer, primary_key=True)
    num_facture = db.Column(db.String(20), nullable=False)
    devise = db.Column(db.String(10))
    date_echeance = db.Column(db.DateTime, default=datetime.utcnow)
    date_debut = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text())
    total = db.Column(db.String, nullable=False)
    taxe = db.Column(db.String, nullable=False)
    ht = db.Column(db.String, nullable=False)
    etat = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client_name = db.Column(db.String(50), nullable=False)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'), nullable=False)
    articles = db.relationship('Article', backref='facture', lazy=True)

    def __init__(self, num_facture, devise, date_echeance, date_debut, description, total, taxe, ht, etat, client_id,
                 client_name, organisation_id):
        self.num_facture = num_facture
        self.devise = devise
        self.date_echeance = date_echeance
        self.date_debut = date_debut
        self.description = description
        self.client_id = client_id
        self.client_name = client_name
        self.organisation_id = organisation_id
        self.total = total
        self.taxe = taxe
        self.ht = ht
        self.etat = etat

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'num_facture': self.num_facture,
            'devise': self.devise,
            'date_echeance': self.date_echeance,
            'date_debut': self.date_debut,
            'description': self.description,
            'total': self.total,
            'taxe': self.taxe,
            'ht': self.ht,
            'etat': self.etat,
            'created': self.created,
            'client_id': self.client_id,
            'client_name': self.client_name,
            'organisation_id': self.organisation_id,
            'articles': [a.serialize() for a in self.articles]
        }


class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix = db.Column(db.Float(), nullable=False)
    total = db.Column(db.Float(), nullable=False)
    taxe = db.Column(db.Float())
    created = db.Column(db.DateTime, default=datetime.utcnow)
    facture_id = db.Column(db.Integer, db.ForeignKey('facture.id'))

    def __init__(self, description, quantite, prix, total, taxe):
        self.description = description
        self.quantite = quantite
        self.prix = prix
        self.total = total
        self.taxe = taxe

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'prix': self.prix,
            'quantite': self.quantite,
            'total': self.total,
            'taxe': self.taxe,
            'created': self.created
        }
