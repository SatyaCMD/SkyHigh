from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import random, uuid, json
from pathlib import Path

from flights.models import Flight

class Command(BaseCommand):
    help = "Seed MongoDB with flights (Render-safe)"

    def handle(self, *args, **options):
        Flight.objects.delete() 

        airports_file = Path("flights/data/airports.json")
        airports = json.loads(airports_file.read_text())
        codes = [a["code"] for a in airports]

        airlines = ["Air India", "Indigo", "Air Asia", "Vistara", "Qatar Arilines"]
        base_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

        flights = []

        for day in range(14):
            date = base_date + timedelta(days=day)

            for origin in codes:
                for destination in codes:
                    if origin == destination:
                        continue

                    for _ in range(3):
                        dep = date + timedelta(hours=random.randint(6, 22))
                        arr = dep + timedelta(minutes=random.randint(60, 180))

                        flights.append(
                            Flight(
                                flight_id=str(uuid.uuid4()),
                                flight_number=f"{random.choice(airlines)}{random.randint(100,999)}",
                                airline_code=random.choice(airlines),
                                origin=origin,
                                destination=destination,
                                departure_time=dep,
                                arrival_time=arr,
                                base_price=random.randint(2500, 9000),
                                total_seats=180,
                                available_seats=random.randint(10, 180),
                                seat_map=["AAAXAA"] * 30,
                            )
                        )

        Flight.objects.insert(flights)
        self.stdout.write(self.style.SUCCESS(f"✅ Seeded {len(flights)} flights"))
