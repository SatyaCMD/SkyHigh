from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import random
import uuid

from flights.models import Flight
from flights.repositories import FlightRepository

class Command(BaseCommand):
    help = "Seed the database with simulated flight data (Render-safe)"

    def handle(self, *args, **options):
        repo = FlightRepository()

        if repo.count() > 0:
            self.stdout.write(
                self.style.WARNING("Flights already exist. Skipping seeding.")
            )
            return

        airlines = [
            'AA', 'DL', 'UA', 'BA', 'LH', 'EK', 'SQ',
            'QF', 'NH', 'AF', 'TK', 'QR', 'CX', 'VS'
        ]

        airports = [
            'JFK', 'LHR', 'LAX', 'DXB', 'SIN', 'HND',
            'CDG', 'AMS', 'SYD', 'FRA', 'IST', 'ORD',
            'ATL', 'PEK', 'CAN', 'SFO', 'MIA', 'YYZ',
            'BOM', 'DEL'
        ]

        flights = []
        batch_size = 2000

        base_date = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        self.stdout.write("🚀 Seeding flights (safe mode)...")

        for day_offset in range(0, 14):
            current_date = base_date + timedelta(days=day_offset)

            for origin in airports:
                for destination in airports:
                    if origin == destination:
                        continue

                    num_flights_today = random.randint(4, 6)
                    hours = random.sample(range(0, 23), num_flights_today)

                    for hour in hours:
                        minute = random.randint(0, 59)
                        departure = current_date.replace(hour=hour, minute=minute)

                        route_hash = abs(sum(ord(c) for c in origin + destination))
                        base_duration_hours = (route_hash % 10) + 2
                        duration_minutes = (base_duration_hours * 60) + random.randint(-20, 30)

                        arrival = departure + timedelta(minutes=duration_minutes)

                        airline = random.choice(airlines)
                        base_price = 100 + (base_duration_hours * 50)
                        price = base_price + random.randint(-30, 150)

                        total_seats = random.choice([180, 200, 220])
                        available_seats = random.randint(20, total_seats)

                        seat_map = []
                        seats_per_row = 6
                        rows = total_seats 

                        for _ in range(rows):
                            row = "A" * seats_per_row
                            row = row[:3] + "X" + row[3:]
                            seat_map.append(row)

                        flight = Flight(
                            flight_id=str(uuid.uuid4()),
                            flight_number=f"{airline}{random.randint(1000, 9999)}",
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
