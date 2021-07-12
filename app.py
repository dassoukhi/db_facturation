import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/facturation'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.secret_key = 'secret string'
db = SQLAlchemy(app)

migrate = Migrate(app, db)
from models import *



@app.route("/")
def hello():
    #client = Client("dass", "50 rue de l'est", "dass@gmail.com", "0614828800", 30, "dass.com")
    #db.session.add(client)
    #db.session.commit()
    clients = Client.query.all()
    print("count:",len(clients) )
    return jsonify([c.serialize() for c in clients])


if __name__ == '__main__':
    db.create_all()
    print("create")
    app.run()