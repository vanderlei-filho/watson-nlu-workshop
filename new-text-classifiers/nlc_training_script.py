import json, csv
from os.path import join, dirname
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 \
    import ClassificationsOptions, Features, ClassificationsOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


apikey = ""
url = ""


#link util https://csvjson.com/csv2json


authenticator = IAMAuthenticator(apikey)
nlu = NaturalLanguageUnderstandingV1(
    version='2021-03-25',
    authenticator=authenticator
)

nlu.set_service_url(url)
print("Successfully connected with the NLU service")


training_data_filename = 'nlc_training_data.json'
with open(join(dirname(__file__), './.', training_data_filename),'rb') as file:
    
    model = nlu.create_classifications_model(
        language='pt',
        training_data=file, 
        training_data_content_type='application/json', 
        name='Myc', 
        model_version='1.0.1'
    ).get_result()
    
    print("Created a NLU Classifications model: {}".format(model))
    '''
    {
        'name': 'Myc', 
        'user_metadata': None, 
        'language': 'pt', 
        'description': None, 
        'model_version': '1.0.1', 
        'version': '1.0.1', 
        'workspace_id': None, 
        'version_description': None, 
        'status': 'starting', 
        'notices': [], 
        'model_id': 'f3587e4e-9d9d-4dcd-977a-285a9ef91772', 
        'features': ['classifications'], 
        'created': '2021-10-06T19:21:15Z', 
        'last_trained': '2021-10-06T19:21:15Z', 
        'last_deployed': None
    }
    '''
   
models = nlu.list_classifications_models().get_result()
print(models)
'''
{
    'models': [
        {
            'name': 'Myc', 
            'user_metadata': None, 
            'language': 'pt', 
            'description': None, 
            'model_version': '1.0.1', 
            'version': '1.0.1', 
            'workspace_id': None, 
            'version_description': None, 
            'status': 'training', 
            'notices': [], 
            'model_id': 'f3587e4e-9d9d-4dcd-977a-285a9ef91772', 
            'features': ['classifications'], 
            'created': '2021-10-06T19:21:15Z', 
            'last_trained': '2021-10-06T19:21:15Z', 
            'last_deployed': None
        }
    ]
}
'''

response = nlu.analyze(
    text='',
    features=Features(
        #entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
        #keywords=KeywordsOptions(emotion=True, sentiment=True, limit=2)
        classifications=ClassificationsOptions(model='f3587e4e-9d9d-4dcd-977a-285a9ef91772')
    )
).get_result()
print(response)

'''
{
    'usage': {
        'text_units': 1, 
        'text_characters': 207, 
        'features': 1
    }, 
    'language': 'pt', 
    'classifications': [
        {
            'confidence': 0.956859, 
            'class_name': 'Informativo'
        }, 
        {
            'confidence': 0.045921, 
            'class_name': 'Obrigatoriedade'
        }, 
        {
            'confidence': 0.025307, 
            'class_name': 'Sancao'
        }, 
        {
            'confidence': 0.011694, 
            'class_name': 'Sanção'
        }, 
        {
            'confidence': 0.00124, 
            'class_name': 'Ementa'
        }, 
        {
            'confidence': 0.001014, 
            'class_name': 'Norma'
        }
    ]
}
'''