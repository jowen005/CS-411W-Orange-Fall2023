from restaurants.models import Restaurant, RestTag
from lcc_project.commands.load import LoadCommand, add_file_path


@add_file_path
class Command(LoadCommand):
    DEFAULT_JSON_PATH = 'json_files/restaurantBuffer.json'


    def load(self, data_list):
        for obj in data_list:
            #All PK Field Attributes must be popped off
            owner_id = obj.pop('owner')
            tag_ids = obj.pop('tags')
            
            #Retrieve objects references by PKFields
            owner = self.User.objects.get(pk=owner_id)   # Format for ForeignKey/OneToOneFields
            tags = [RestTag.objects.get(pk=tag_id) for tag_id in tag_ids]   #Format for ManyToManyFields

            #Create object
            rest = Restaurant.objects.create(owner=owner, **obj)
            rest.tags.set(tags)