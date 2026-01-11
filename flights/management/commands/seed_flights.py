from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import random, uuid, json
from pathlib import Path

from flights.models import Flight
from flights.repositories import FlightRepository

class Command(BaseCommand):
    help = "Seed flights using MongoEngine (FINAL FIX)"

    def handle(self, *args, **kwargs):
        repo = FlightRepository()

        repo.delete_all()  
        self.stdout.write("Cleared existing flights")

        airports_file = Path("flights/data/airports.json")
        airports = json.loads(airports_file.read_text())
        airport_codes = [a["code"] for a in airports]

        airlines = ["AI", "6E", "UK", "SG", "IX"]

        base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        flights = []
        for day in range(14):
            day_date = base_date + timedelta(days=day)

            for origin in airport_codes:
                for destination in airport_codes:
                    if origin == destination:
                        continue

                    for _ in range(3):
                        dep = day_date + timedelta(hours=random.randint(6, 22))
                        arr = dep + timedelta(minutes=random.randint(60, 180))

                        flights.append(Flight(
                            flight_id=str(uuid.uuid4()),
                            flight_number=f"{random.choice(airlines)}{random.randint(100,999)}",
                            airline_code=random.choice(airlines),
                            origin=origin,
                            destination=destination,
                            departure_time=dep,
                            arrival_time=arr,
                            base_price=random.randint(2500, 8000),
                            total_seats=180,
                            available_seats=random.randint(10, 180),
                            seat_map=["AAAXAA"] * 30,
                        ))

        repo.insert_many(flights)
        self.stdout.write(self.style.SUCCESS("✈️ Flights seeded successfully"))
