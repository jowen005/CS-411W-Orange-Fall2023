from django.core.management.base import BaseCommand, CommandParser
from django.core.management import call_command
from feedback.models import Reviews
from restaurants.models import MenuItem

class Command(BaseCommand):

    help = 'Updates the Patron Names of Review Objects.'


    # def add_arguments(self, parser: CommandParser):
    #     parser.add_argument('-f', dest='json_path', default=self.DEFAULT_JSON_PATH, 
    #                         help='Specifies a file to load',)


    def handle(self, *args, **options):

        report = self.update_objects()
        self.output_report(report)


    def update_objects(self):
        num_updated_reviews = 0

        outdated_reviews = Reviews.objects.filter(patron_name__isnull=True)
        for review in outdated_reviews:
            review.save()
            num_updated_reviews += 1

        report = {'num_updated_reviews': num_updated_reviews}

        return report

    def output_report(self, report):
        print(f'Number of Reviews Updated: {report["num_updated_reviews"]}\n')
        self.stdout.write(self.style.SUCCESS(f'This command successfully completed'))