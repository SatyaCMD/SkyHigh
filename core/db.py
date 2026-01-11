import os
import certifi
from pymongo import MongoClient

class MongoDB:
    _client = None
    _db = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            mongo_uri = os.getenv("MONGO_URI")

            if not mongo_uri:
                raise RuntimeError("MONGO_URI environment variable not set")

            cls._client = MongoClient(
                mongo_uri,
                tls=True,
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=30000,
            )

            cls._client.admin.command("ping")
            print("MongoDB connected successfully")

        return cls._client

    @classmethod
    def get_db(cls):
        if cls._db is None:
            client = cls.get_client()
            db_name = os.getenv("MONGO_DB_NAME", "flight_simulator")
            cls._db = client[db_name]

        return cls._db

def get_flights_collection():
    return MongoDB.get_db()["flights"]

def get_airports_collection():
    return MongoDB.get_db()["airports"]

def get_airlines_collection():
    return MongoDB.get_db()["airlines"]

def get_users_collection():
    return MongoDB.get_db()["users"]

def get_bookings_collection():
    return MongoDB.get_db()["bookings"]

def get_captchas_collection():
    return MongoDB.get_db()["captchas"]
