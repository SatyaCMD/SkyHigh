from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import random
import uuid
import json
from pathlib import Path

from flights.models import Flight
from flights.repositories import FlightRepository


class Command(BaseCommand):
    help = "Seed the database with simulated flight data (airport.json based)"

    def handle(self, *args, **options):
        repo = FlightRepository()

        if repo.count() > 0:
            self.stdout.write(
                self.style.WARNING("Flights already exist. Skipping seeding.")
            )
            return

        airports_file = Path(__file__).resolve().parent.parent / "data" / "airports.json"

        with open(airports_file, "r", encoding="utf-8") as f:
            airports_data = json.load(f)

        airports = [a["code"] for a in airports_data]

        airlines = ["AI", "UK", "6E", "SG", "G8", "IX"]

        flights = []
        batch_size = 1000

        base_date = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        self.stdout.write("Seeding flights using airport.json...")

        for day_offset in range(0, 14):
            current_date = base_date + timedelta(days=day_offset)

            for origin in airports:
                for destination in airports:
                    if origin == destination:
                        continue

                    num_flights_today = random.randint(3, 5)
                    hours = random.sample(range(6, 22), num_flights_today)

                    for hour in hours:
                        minute = random.randint(0, 59)
                        departure = current_date.replace(hour=hour, minute=minute)

                        duration_minutes = random.randint(60, 180)
                        arrival = departure + timedelta(minutes=duration_minutes)

                        airline = random.choice(airlines)
                        price = random.randint(2500, 9000)

                        total_seats = random.choice([180, 186])
                        available_seats = random.randint(20, total_seats)

                        seat_map = ["AAAXAA"] * (total_seats // 6)

                        flight = Flight(
                            flight_id=str(uuid.uuid4()),
                            flight_number=f"{airline}{random.randint(100, 999)}",
                            airline_code=airline,
                            origin=origin,
                            destination=destination,
                            departure_time=departure,
                            arrival_time=arrival,
                            base_price=float(price),
                            total_seats=total_seats,
                            available_seats=available_seats,
                            seat_map=seat_map,
                        )

                        flights.append(flight)

                        if len(flights) >= batch_size:
                            repo.insert_many(flights)
                            flights = []
                            self.stdout.write(
                                f"Inserted batch for {current_date.date()}"
                            )

        if flights:
            repo.insert_many(flights)

        self.stdout.write(
            self.style.SUCCESS("Flight seeding completed successfully!")
        )
