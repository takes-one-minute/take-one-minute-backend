import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env') # Path to .env file
load_dotenv(dotenv_path=dotenv_path, verbose=True) # Load the .env file
# verbose = True: Print out all of errors and informations the loaded .env file

class Settings():
    access_secret_key: str = os.getenv("AccessTokenSecretKey")
    refresh_secret_key: str = os.getenv("RefreshTokenSecretKey")
    algorithm: str = os.getenv("Algorithm")

def get_settings():
    return Settings()
