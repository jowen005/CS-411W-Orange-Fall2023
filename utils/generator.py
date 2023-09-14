import json
import faker as Faker

def generateAccounts(modeltype, count):
    #load the definition file for model fields
    BASE_DIR = Path(__file__).resolve().parent
    try:
        with open(BASE_DIR/'models.json') as handle:
            MODELS = json.load(handle)
    except IOError:
        MODELS = {}
    #todo faker integration
    #basic logic is as follows
    # load models file
    # find model from modeltype
    # iterate over each defined field
    # if faker has a util for a given field have faker generate it
    #   ex: the name field is a faker function so anything of type name will be filled from that function
    # package into one json file named "Fake[modeltype].json"
    