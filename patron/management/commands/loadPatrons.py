from patron.models import Patron
from lcc_project.commands.load import LoadCommand, add_file_path
from restaurants.models import RestrictionTag, AllergyTag, TasteTag


@add_file_path
class Command(LoadCommand):
    DEFAULT_JSON_PATH = 'json_files/patronBuffer.json'


    def load(self, data_list):
        for obj in data_list:
            
            #Create the patron account
            email = obj.pop('email')
            username = obj.pop('username')
            password = obj.pop('password')

            #Check to see if account exists
            try:
                user = self.User.objects.get(email=email)
            except self.User.DoesNotExist:
                user = self.User.objects.create_user(email=email, username=username, password=password, user_type="patron")

            #All PK Field Attributes must be popped off
            restriction_tag_ids = obj.pop('patron_restriction_tag')
            allergy_tag_ids = obj.pop('patron_allergy_tag')
            taste_tag_ids = obj.pop('patron_taste_tag')
            
            #Retrieve objects references by PKFields
            restriction_tags = [RestrictionTag.objects.get(pk=tag_id) for tag_id in restriction_tag_ids]
            allergy_tags = [AllergyTag.objects.get(pk=tag_id) for tag_id in allergy_tag_ids]
            taste_tags = [TasteTag.objects.get(pk=tag_id) for tag_id in taste_tag_ids]

            #Check to see if profile exists
            try:
                patron = Patron.objects.get(user=user)
                #Update patron
                for attr, value in obj.items():
                    setattr(patron, attr, value)

            except Patron.DoesNotExist:
                #Create Patron
                patron = Patron.objects.create(user=user, **obj)
            
            patron.patron_restriction_tag.set(restriction_tags)
            patron.patron_allergy_tag.set(allergy_tags)
            patron.patron_taste_tag.set(taste_tags)

            patron.save()


            