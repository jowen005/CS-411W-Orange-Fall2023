from django.core.management.base import BaseCommand
from restaurants.models import MenuItem

class Command(BaseCommand):

    help = 'Calls the appropriate load functions to initialize the database'


    def handle(self, *args, **options):
        report = self.update_objects()
        self.output_report(report)


    def update_objects(self):
        num_updated_items = 0
        outdated_items = MenuItem.objects.all()

        for item in outdated_items:
            item.save()
            num_updated_items += 1

        report = {
            'num_updated_items': num_updated_items
        }
        return report

    def output_report(self, report):
        print(f'Number of Menu Items Updated: {report["num_updated_items"]}')
        self.stdout.write(self.style.SUCCESS(f'This command successfully completed'))

