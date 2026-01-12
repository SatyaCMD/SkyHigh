from django.apps import AppConfig
import threading

class FlightsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "flights"

    def ready(self):
        threading.Thread(target=self.auto_seed_flights, daemon=True).start()

    def auto_seed_flights(self):
        try:
            from flights.repositories import FlightRepository
            from flights.management.commands.seed_flights import Command
            from core.db import MongoDB

            db = MongoDB.get_db()
            lock = db["seed_lock"]

            if lock.find_one({"name": "flights_seeded"}):
                print("Flights already seeded (lock found)")
                return

            repo = FlightRepository()
            if repo.count() > 0:
                lock.insert_one({"name": "flights_seeded"})
                print("Flights already exist, skipping auto-seed")
                return

            print("Auto-seeding flights (Render Free)...")
            Command().handle()

            lock.insert_one({"name": "flights_seeded"})
            print("Flight seeding completed successfully")

        except Exception as e:
            print("Flight auto-seeding failed:", e)
