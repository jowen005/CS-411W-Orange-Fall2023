from patron.models import Patron
from lcc_project.commands.load import LoadCommand, add_file_path
from restaurants.models import RestrictionTag, AllergyTag, TasteTag


@add_file_path
class Command(LoadCommand):
    DEFAULT_JSON_PATH = 'json_files/patronSetup.json'


    def load(self, data_list):
        skipped_emails = []
        updated_profiles = []
        created_profiles = []
    
        for obj in data_list:

            #Create the patron account
            email = obj.pop('email')

            #Check to see if account exists (dont add if account does not exist)
            try:
                user = self.User.objects.filter(user_type='patron').get(email=email)
            except self.User.DoesNotExist:
                skipped_emails.append(email)
                continue

            #All PK Field Attributes must be popped off
            restriction_tag_names = obj.pop('patron_restriction_tag')
            allergy_tag_names = obj.pop('patron_allergy_tag')
            taste_tag_names = obj.pop('patron_taste_tag')
            
            #Retrieve objects references by PKFields
            restriction_tags = [RestrictionTag.objects.get(title=name) for name in restriction_tag_names]
            allergy_tags = [AllergyTag.objects.get(title=name) for name in allergy_tag_names]
            taste_tags = [TasteTag.objects.get(title=name) for name in taste_tag_names]

            #Check to see if profile exists
            try:
                patron = Patron.objects.get(user=user)
                updated_profiles.append(email)
                #Update patron
                for attr, value in obj.items():
                    setattr(patron, attr, value)

            except Patron.DoesNotExist:
                #Create Patron
                patron = Patron.objects.create(user=user, **obj)
                created_profiles.append(email)
            
            patron.patron_restriction_tag.set(restriction_tags)
            patron.patron_allergy_tag.set(allergy_tags)
            patron.patron_taste_tag.set(taste_tags)

            patron.save()

        print("-"*50)
        print("loadDefaultPatrons Report")
        print("-"*50)

        if skipped_emails:
            print("SKIPPED | These emails were not registered so profile not created:")
            for email in skipped_emails:
                print(f" - {email}")
        
        if updated_profiles:
            print("UPDATED | These emails were registered and associated with a profile:")
            for email in updated_profiles:
                print(f" - {email}")

        if created_profiles:
            print("CREATED | These emails were registered and but not associated with a profile:x")
            for email in created_profiles:
                print(f" - {email}")
            
