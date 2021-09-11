import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
load_dotenv()
print('postgres://postgres:admin@localhost/facturation'.replace("://", "ql://", 1))

print(generate_password_hash("123456", method='sha256'))

