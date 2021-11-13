import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key, **kwargs):
    print("GET from {}".format(url))
    print(kwargs)
    try:
        if api_key is not None:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        print("Error")
    status_code = response.status_code
    print("With status code {}".format(status_code))
    json_data = json.loads(response.text)
    return json_data, status_code

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    # print("Post to url: {} ".format(url))
    # print(kwargs)
    # print(json_payload)
    response = requests.post(url, headers={'Content-Type': 'application/json'}, params=kwargs, json=json_payload)
    status_code = response.status_code
    # print("With status code {}".format(status_code))
    json_data = json.loads(response.text)
    return json_data, status_code


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



