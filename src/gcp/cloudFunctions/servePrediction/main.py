#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
import os
import datetime
import pytz
import joblib
from flask import abort
from google.cloud import storage

#define:
def servePrediction(request):
    """Responds to a POST request from any CORS origin.
    Args:
        request: HTTP request object.
    Returns:
        The response text
    """
    print(f"local log: request.method was {request.method}\n")
    #Set CORS headers for preflight request:
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 202, headers)
    
    now = datetime.datetime.now()
    #always wait until display before time zone convert:
    co = now.astimezone(pytz.timezone("America/Denver"))
    print(f'main request at {co.strftime("%m/%d/%Y %H:%M:%S")} MT')
    # Set CORS headers for main request:
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    requestJson = request.get_json()
    if requestJson:
        sortingHat = cocktailClassifier(requestJson)
        return (sortingHat.awaken(), 201)
    elif request.method in ['DELETE', 'PUT']:
        return abort(403)
    else:
        print(f'local log: Else unexpectedly reached\n')
        return abort(417)

class cocktailClassifier(object):
    def __init__(self, json):
        self.json = json

    def awaken(self):
        stored = self.getFromGcs('trained.joblib')
        model, extractor = joblib.load(stored)
        x = extractor.transform((self.json['ingredients'],))
        probabilities = model.predict_proba(x)
        os.remove(stored)
        return {f: f'{p*100:0.2f}%' for f, p in zip(model.classes_,
                                                    probabilities[0])}

    def getFromGcs(self, filePath):
        client = storage.Client()
        bucket = client.get_bucket('wstoffers-galvanize-codex-data-lake')
        storagePath = os.path.join('/tmp',filePath)
        bucket.get_blob(filePath).download_to_filename(storagePath)
        return storagePath

#run:
if __name__ == '__main__':
    pass
