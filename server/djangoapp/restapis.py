import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key, **kwargs):
    # print("GET from {}".format(url))
    # print(kwargs)
    try:
        if api_key is not None:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        print("Network Error")
    status_code = response.status_code
    # print("With status code {}".format(status_code))
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
def get_dealers_from_cf(url, **kwargs):
    dealers_info = []
    result = "success"
    # - Call get_request() with specified arguments
    json_result, status_code = get_request(url, None)
    if status_code == 200 and json_result:
        dealers = json_result["entries"]
        for dealer in dealers:
# - Parse JSON results into a CarDealer object list
            a_dealer = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                short_name=dealer["short_name"], state=dealer["state"],
                                st=dealer["st"], zip=dealer["zip"])
            dealers_info.append(a_dealer)
    elif json_result:
        result = json_result["message"]
    else:
        result = "Misc error"
    return dealers_info, result

def get_dealers_by_state (url, state):
    state_dealers = []
    result = "ok"
    # Call get_request with a URL parameter
    json_result, status_code = get_request(url, None, state=state)
    if status_code == 200 and json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"], state=dealer["state"],
                                   st=dealer["st"], zip=dealer["zip"])
            state_dealers.append(dealer_obj)
    elif json_result:
        result = json_result["message"]
    else:
        result = "Unknown error"
    return state_dealers, result

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_reviews_from_cf(url, dealerId):
#     results = []
#     # Call get_request with a URL parameter
#     params = {"dealerId": dealerId}
#     json_result = get_request(url, None, **params)
#     if json_result:
#         # Get the row list in JSON as dealers
#         print(json_result)
#         reviews = json_result["entries"]
#         # For each review object
#         for review in reviews:
#             # Create a CarDealer object with values in `doc` object
#             review_obj = DealerReview(dealership=review["dealership"], review=review["review"], name=review["name"], purchase=review["purchase"], purchase_date=review["purchase_date"], car_make=review["car_make"], car_model=review["car_model"], car_year=review["car_year"])
#             #review_obj.sentiment = analyze_review_sentiments(review_obj.review)
#             results.append(review_obj)

#     return results


# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



