from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")

# Client for the database
db_client = MongoClient(config["DB_HOST"], 27017)

# Available databases
db_test = db_client["test-database"]
db_prod = db_client["quantum-proxy-db"]

# Collections
users = db_test.users

providers = db_prod.providers
backends = db_prod.backends