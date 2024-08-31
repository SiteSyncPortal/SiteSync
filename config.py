import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


class Config:
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    # MONGO_URI = os.environ.get('MONGO_URI')
    MONGO_URI = "mongodb+srv://sitesyncportal:Sitesync_009@sitesync.n3awe.mongodb.net/?retryWrites=true&w=majority&appName=SiteSync"
    SECRET_KEY = "Sitesync_009"
