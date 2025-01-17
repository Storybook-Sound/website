from googleapiclient.discovery import build
import pprint
from . import configs

pprint(configs.googleapikey)

googleapikey = 'AIzaSyBp0UifMv1jfTC4uEHL6wTZrIyQOAuFqlM'
custom_search_engine_id = 'a2cf039c0fade4c2e'

def test():
    print("hello")

test()

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

""" results = google_search(
    '"Storybook Sound"', googleapikey, custom_search_engine_id, num=10)

for result in results:
    pprint.pprint(result)
 """
