from django.core.management.base import BaseCommand
from faker import Faker
from fire.models import Locations, Incident, FireStation, FireTruck

class Command(BaseCommand):
    help = 'Create Initial data for the application'

    def handle(self, *args, **kwargs):
        self.create_locations(10)
        self.create_incidents(50)
        self.create_fire_stations(10)
        self.create_fire_trucks(10)

    def create_locations(self, count):
        fake = Faker()
        for _ in range(count):
            latitude = fake.latitude()
            longitude = fake.longitude()
            Locations.objects.create(
                name=fake.street_name(),
                address=fake.address(),
                city=fake.city(),
                country=fake.country(),
                latitude=latitude,
                longitude=longitude
            )

        self.stdout.write(self.style.SUCCESS(
            'Initial data for locations created successfully.'))

    def create_incidents(self, count):
        fake = Faker()
        for _ in range(count):
            Incident.objects.create(
                location=Locations.objects.order_by('?').first(),
                description=fake.sentence(),
                severity_level=fake.random_element(elements=('Low', 'Medium', 'High'))
            )

        self.stdout.write(self.style.SUCCESS(
            'Initial data for incidents created successfully.'))

    def create_fire_stations(self, count):
        fake = Faker()
        for _ in range(count):
            latitude = fake.latitude()
            longitude = fake.longitude()
            FireStation.objects.create(
                name=fake.company(),
                address=fake.address(),
                city=fake.city(),
                country=fake.country(),
                latitude=latitude,
                longitude=longitude
            )

        self.stdout.write(self.style.SUCCESS(
            'Initial data for fire stations created successfully.'))

    def create_fire_trucks(self, count):
        fake = Faker()
        for _ in range(count):
            FireTruck.objects.create(
                truck_number=fake.random_number(digits=4),
                model=fake.word(),
                capacity=fake.random_element(elements=('1000L', '2000L', '3000L')),
                station=FireStation.objects.order_by('?').first()
            )

        self.stdout.write(self.style.SUCCESS(
            'Initial data for fire trucks created successfully.'))
