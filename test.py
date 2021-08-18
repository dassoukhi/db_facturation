import os
from dotenv import load_dotenv
load_dotenv()
print('postgres://postgres:admin@localhost/facturation'.replace("://", "ql://", 1))
