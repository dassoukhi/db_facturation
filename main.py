organisation =  {
        "adresse": "12 Avenue de charles de Gaule",
        "created": "Tue, 13 Jul 2021 12:42:03 GMT",
        "email": "client1@gmail.com",
        "password": "123456",
        "iban": "FA2315643456345",
        "id": 1,
        "nom": "clien1",
        "nom_banque": "BAC",
        "num_registre": "126985837",
        "site_internet": "test.td",
        "telephone": "6612443344",
        "tva": 20.0
    }

clients = [
    {
        "adresse": "12 Avenue de charles de Gaule",
        "created": "Tue, 13 Jul 2021 12:44:07 GMT",
        "email": "client1@gmail.com",
        "id": 1,
        "nom": "clien1",
        "site_internet": "test.td",
        "telephone": "6612443344",
        "organisation_id": 1
    },
    {
        "adresse": "12 Avenue de charles de Gaule",
        "created": "Tue, 13 Jul 2021 12:45:28 GMT",
        "email": "client2@gmail.com",
        "id": 2,
        "nom": "clien2",
        "site_internet": "client1.td",
        "telephone": "6612443344",
        "organisation_id": 1
    },
    {
        "adresse": "12 Avenue de charles de Gaule",
        "created": "Tue, 13 Jul 2021 12:45:44 GMT",
        "email": "client3@gmail.com",
        "id": 3,
        "nom": "clien3",
        "site_internet": "client3.td",
        "telephone": "6612443344",
        "organisation_id": 1
    }
]

factures = [
    {
        "created": "Tue, 13 Jul 2021 13:38:53 GMT",
        "date_debut": "Tue, 13 Jul 2021 12:44:07 GMT",
        "date_echeance": "Sat, 17 Jul 2021 12:44:07 GMT",
        "description": "",
        "devise": "DOLLAR",
        "id": 4,
        "num_facture": "Fact_12435412"
    },
    {
        "created": "Tue, 13 Jul 2021 13:31:37 GMT",
        "date_debut": "Tue, 13 Jul 2021 12:44:07 GMT",
        "date_echeance": "Sat, 17 Jul 2021 12:44:07 GMT",
        "description": "",
        "devise": "Franc CFA",
        "id": 2,
        "num_facture": "Fact_12435412"
    },
    {
        "created": "Tue, 13 Jul 2021 13:38:47 GMT",
        "date_debut": "Tue, 13 Jul 2021 12:44:07 GMT",
        "date_echeance": "Sat, 17 Jul 2021 12:44:07 GMT",
        "description": "",
        "devise": "EURO",
        "id": 3,
        "num_facture": "Fact_12435412"
    }
]

articles = [
    {
        "created": "Tue, 13 Jul 2021 14:01:02 GMT",
        "description": "Matelas",
        "id": 1,
        "prix": 12000.0,
        "quantite": 2,
        "taxe": None,
        "total": 24000.0
    },
    {
        "created": "Tue, 13 Jul 2021 14:05:25 GMT",
        "description": "Lit",
        "id": 3,
        "prix": 13000.0,
        "quantite": 1,
        "taxe": 10.0,
        "total": 13000.0
    },
    {
        "created": "Tue, 13 Jul 2021 14:05:52 GMT",
        "description": "Ordi",
        "id": 4,
        "prix": 4000000.0,
        "quantite": 1,
        "taxe": 40.0,
        "total": 4000000.0
    },
    {
        "created": "Tue, 13 Jul 2021 14:02:04 GMT",
        "description": "Chaussures",
        "id": 2,
        "prix": 10000.0,
        "quantite": 3,
        "taxe": None,
        "total": 30000.0
    }
]