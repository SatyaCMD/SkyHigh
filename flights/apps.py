from django.apps import AppConfig

class FlightsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'flights'

    def ready(self):
        from flights.models import Airport
        if Airport.objects.exists():
            return

        Airport.objects.bulk_create([
            Airport(code="BOM", city="Mumbai"),
            Airport(code="DEL", city="Delhi"),
            Airport(code="BLR", city="Bangalore"),
            Airport(code="HYD", city="Hyderabad"),
            Airport(code="MAA", city="Chennai"),
            Airport(code="CCU", city="Kolkata"),
            Airport(code="PNQ", city="Pune"),
            Airport(code="AMD", city="Ahmedabad"),
            Airport(code="GOI", city="Goa"),
            Airport(code="COK", city="Kochi"),
            Airport(code="TRV", city="Trivandrum"),
            Airport(code="IXC", city="Chandigarh"),
            Airport(code="JAI", city="Jaipur"),
            Airport(code="LKO", city="Lucknow"),
            Airport(code="PAT", city="Patna"),
            Airport(code="RPR", city="Raipur"),
            Airport(code="BBI", city="Bhubaneswar"),
            Airport(code="VNS", city="Varanasi"),
            Airport(code="IXR", city="Ranchi"),
            Airport(code="NAG", city="Nagpur"),
            Airport(code="IDR", city="Indore"),
            Airport(code="BHO", city="Bhopal"),
        ])
