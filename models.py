from app import db
from datetime import datetime

class Organisation(db.Model):
    __tablename__ = 'organisations'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    adresse = db.Column(db.String())
    email = db.Column(db.String(120))
    telephone = db.Column(db.String())
    num_enregistrement = db.Column(db.String(50))
    nom_banque = db.Column(db.String(100))
    iban = db.Column(db.String())
    tva = db.Column(db.Float(3))
    site_internet = db.Column(db.String(80))
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, nom, adresse, email, telephone, num_enregistrement, nom_banque, iban, tva, site_internet):
        self.nom = nom
        self.adresse = adresse
        self.email = email
        self.telephone = telephone
        self.num_enregistrement = num_enregistrement
        self.nom_banque = nom_banque
        self.iban = iban
        self.tva = tva
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
            'num_enregistrement': self.num_enregistrement,
            'nom_banque': self.nom_banque,
            'iban': self.iban,
            'tva': self.tva,
            'site_internet': self.site_internet,
            'created': self.created
        }

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    adresse = db.Column(db.String())
    email = db.Column(db.String(120))
    telephone = db.Column(db.String())
    tva = db.Column(db.Float())
    site_internet = db.Column(db.String(50))
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, nom, adresse, email, telephone, tva, site_internet):
        self.nom = nom
        self.adresse = adresse
        self.email = email
        self.telephone = telephone
        self.tva = tva
        self.site_internet = site_internet


    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'nom':  self.nom,
            'adresse':  self.adresse,
            'email': self.email,
            'telephone': self.telephone,
            'tva': self.tva,
            'site_internet': self.site_internet,
            'created': self.created
        }