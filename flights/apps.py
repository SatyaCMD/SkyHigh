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

            repo = FlightRepository()

            if repo.count() > 0:
                print("Flights already exist, skipping auto-seed")
                return

            print("Auto-seeding flights (Render Free)...")
            Command().handle()

        except Exception as e:
            print("Flight auto-seeding failed:", e)
