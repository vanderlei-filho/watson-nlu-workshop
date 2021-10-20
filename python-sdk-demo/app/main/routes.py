import requests
from flask import jsonify, make_response, current_app, request

from app.main import bp

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, EntitiesOptions
from werkzeug.utils import secure_filename


@bp.route('/nlu', methods=['POST'])
def nlu_service():

    try:

        # READ REQUEST PARAMETERS
        model_id = request.json['model_id']
        text = request.json['text']

        # Get NLU credentials from env vars
        nlu_apikey = current_app.config['NLU_APIKEY']
        nlu_url = current_app.config['NLU_URL']

        # Spawn the NLU IAM authenticator
        authenticator = IAMAuthenticator(nlu_apikey)

        # Spawn the NLU client
        nlu = NaturalLanguageUnderstandingV1(
            version="2021-08-01",
            authenticator = authenticator
        )
        nlu.set_service_url(nlu_url)

        # Execute NLU API call to the "analyze" endpoint 
        nlu_response = nlu.analyze(
            text=text,
            features=Features(
                entities=EntitiesOptions(
                    model=model_id
                )
            )
        ).get_result()

    except Exception as err:
        # RETURN SERVICE RESPONSE (IN CASE OF EXCEPTION)
        return make_response(jsonify({"err": True, "msg": "Failure making request to Watson NLU: {}".format(err)}), 500)
    
    else:
        # RETURN SERVICE RESPONSE (IN CASE OF SUCCESS)
        return make_response(jsonify({"err": False, "data": nlu_response}), 200)
