from dotenv import load_dotenv
import os

load_dotenv()

# Debug: Print all environment variables
print("Loaded environment variables:")
print(f"DB_HOST: {os.getenv('DB_HOST')}")
print(f"DB_USER: {os.getenv('DB_USER')}")
print(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")
print(f"DB_NAME: {os.getenv('DB_NAME')}")
print(f"SECRET_KEY: {os.getenv('SECRET_KEY')}")
print(f"FLASK_RUN_PORT: {os.getenv('FLASK_RUN_PORT')}")

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'amanbangetgess')
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:{os.getenv('DB_PASSWORD', '')}@{os.getenv('DB_HOST', 'localhost')}/{os.getenv('DB_NAME', 'mydatabase')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT = int(os.getenv('FLASK_RUN_PORT', 1337))