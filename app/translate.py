import json
import requests
from flask_babel import _
from app import flaskapp


def translate(text, source_language, dest_language):
    if 'MS_TRANSLATOR_KEY' not in flaskapp.config or \
            not flaskapp.config['MS_TRANSLATOR_KEY']:
        return _('Error1: the translation service is not configured.')
    auth = {'Ocp-Apim-Subscription-Key': flaskapp.config['MS_TRANSLATOR_KEY']}
    r = requests.get('https://api.microsofttranslator.com/v2/Ajax.svc'
                     '/Translate?text={}&from={}&to={}'.format(
                         text, source_language, dest_language),
                     headers=auth)
    if r.status_code != 200:
        return _('Error2: the translation service failed.')
    return json.loads(r.content.decode('utf-8-sig'))