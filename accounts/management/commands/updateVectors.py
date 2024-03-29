from django.core.management.base import BaseCommand, CommandParser
from django.core.management import call_command
from patron.models import Patron, PatronSearchHistory
from restaurants.models import MenuItem

class Command(BaseCommand):

    help = 'Calls the appropriate load functions to initialize the database'


    # def add_arguments(self, parser: CommandParser):
    #     parser.add_argument('-f', dest='json_path', default=self.DEFAULT_JSON_PATH, 
    #                         help='Specifies a file to load',)


    def handle(self, *args, **options):
        report = self.update_objects()
        self.output_report(report)


    def update_objects(self):
        # num_updated_patrons = 0
        num_updated_items = 0

        # outdated_patrons = Patron.objects.filter(profile_updated = True)
        # for patron in outdated_patrons:
        #     patron.save()
        #     num_updated_patrons += 1
        outdated_items = MenuItem.objects.all()
        # outdated_items = MenuItem.objects.filter(suggestion_vector__isnull=True)
        for item in outdated_items:
            item.save()
            num_updated_items += 1

        report = {
            # 'num_updated_patrons': num_updated_patrons,
            'num_updated_items': num_updated_items
        }
        return report

    def output_report(self, report):
        # print(f'Number of Profiles Updated: {report["num_updated_patrons"]}')
        print(f'Number of Menu Items Updated: {report["num_updated_items"]}')
        self.stdout.write(self.style.SUCCESS(f'This command successfully completed'))