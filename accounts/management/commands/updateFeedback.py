from django.core.management.base import BaseCommand
from feedback.models import Reviews

class Command(BaseCommand):

    help = 'Updates the Patron Names of Review Objects.'


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
        print(f'Number of Reviews Updated: {report["num_updated_reviews"]}')
        self.stdout.write(self.style.SUCCESS(f'This command successfully completed'))

