from patron.models import Patron
from lcc_project.commands.load import LoadCommand, add_file_path


@add_file_path
class Command(LoadCommand):
    DEFAULT_JSON_PATH = 'json_files/patronBuffer.json'


    def load(self, data_list):
        for obj in data_list:
            #All PK Field Attributes must be popped off
            user_id = obj.pop('user')
            
            #Retrieve objects references by PKFields
            user_id = self.User.objects.get(pk=user_id)   # Format for ForeignKey/OneToOneFields

            #Create object
            Patron = Patron.objects.create(user=user_id, **obj)
            