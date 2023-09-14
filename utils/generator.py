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
    