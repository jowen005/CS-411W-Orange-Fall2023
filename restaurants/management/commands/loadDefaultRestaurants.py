from lcc_project.commands.load import LoadCommand, add_file_path
from restaurants.models import Restaurant, RestTag


@add_file_path
class Command(LoadCommand):
    DEFAULT_JSON_PATH = 'json_files/restaurantSetup.json'


    def load(self, data_list):
        skipped_emails = []
        updated_restaurants = []
        created_restaurants = []
    
        for obj in data_list:

            #Create the patron account
            email = obj.pop('owner_email')

            #Check to see if account exists (dont add if account does not exist)
            try:
                owner = self.User.objects.filter(user_type='restaurant').get(email=email)
            except self.User.DoesNotExist:
                skipped_emails.append(email)
                continue

            #All PK Field Attributes must be popped off
            rest_tag_names = obj.pop('tags')
            
            #Retrieve objects references by PKFields
            rest_tags = [RestTag.objects.get(title=name) for name in rest_tag_names]

            #Check to see if profile exists
            try:
                restaurant = Restaurant.objects.get(owner=owner, street_name=obj['street_name'])
                updated_restaurants.append(email+" -- "+obj['name']+" -- "+obj['street_name'])
                #Update patron
                for attr, value in obj.items():
                    setattr(restaurant, attr, value)

            except Restaurant.DoesNotExist:
                #Create Patron
                restaurant = Restaurant.objects.create(owner=owner, **obj)
                created_restaurants.append(email+" -> "+obj['street_name'])
            
            restaurant.tags.set(rest_tags)
            
            restaurant.save()

        print("-"*50)
        print("loadDefaultRestaurants Report")
        print("-"*50)

        if skipped_emails:
            print("SKIPPED | These owner emails were not registered so restaurant not created:")
            for email in skipped_emails:
                print(f" - {email}")
        
        if updated_restaurants:
            print("UPDATED | These owner emails and addresses were registered with a restaurant:")
            for email in updated_restaurants:
                print(f" - {email}")

        if created_restaurants:
            print("CREATED | These owner emails were registered but the address was not associated with a restaurant:")
            for email in created_restaurants:
                print(f" - {email}")