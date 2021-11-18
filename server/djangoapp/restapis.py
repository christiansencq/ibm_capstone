import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import logging

logger = logging.getLogger(__name__)

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
        print("Network Error")
    status_code = response.status_code
    print("With status code {}".format(status_code))
    json_data = json.loads(response.text)
    return json_data, status_code

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print("Post to url: {} ".format(url))
    print(kwargs)
    print(json_payload)
    response = requests.post(url, headers={'Content-Type': 'application/json'}, params=kwargs, json=json_payload)
    status_code = response.status_code
    print("With status code {}".format(status_code))
    json_data = json.loads(response.text)
    return json_data, status_code

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    info = []
    result = "ok"
    # - Call get_request() with specified arguments
    logger.info("Get Dealers from CF Called!")
    json_result, status_code = get_request(url, None)
    if status_code == 200 and json_result:
        dealers = json_result['rows']
        logger.info(len(dealers))
        for dealer in dealers:
            dlr_data = dealer['doc']
            #print('ADDRESS', dlr_data["address"])
            if dlr_data.get('address'):
            # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dlr_data.get("address"), city=dlr_data.get("city"), full_name=dlr_data.get("full_name"),
                            id=dlr_data.get("id"), lat=dlr_data.get("lat"), long=dlr_data.get("long"),
                            short_name=dlr_data.get("short_name"), state=dlr_data.get("state"),
                            st=dlr_data.get("st"), zip=dlr_data.get("zip"))
            
            # dealer_obj = CarDealer(address=dealer["doc"]["address"], city=dealer["doc"]["city"], full_name=dealer["doc"]["full_name"],
            #                     id=dealer["doc"]["id"], lat=dealer["doc"]["lat"], long=dealer["doc"]["long"],
            #                     short_name=dealer["doc"]["short_name"], 
            #                     st=dealer["doc"]["st"], state=dealer["doc"]["state"], zip=dealer["doc"]["zip"])
                info.append(dealer_obj)
    elif json_result:
        result = json_result["message"]
    else:
        result = "Unknown error"
    return info, result

def get_dealer_by_id(url, dealerId):
    # Call get_request with a URL parameter
    info = None
    result = "ok"
    json_result, status_code = get_request(url, None, dealerId=dealerId)
#    json_result, status_code = get_request(url, None, dealerId=dealerId)

    if status_code == 200 and json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        for dealer in dealers:
        # Create a CarDealer object with values in `doc` object
            info = CarDealer(address=dealer.get("address"), city=dealer.get("city"), full_name=dealer.get("full_name"),
                                id=dealer.get("id"), lat=dealer.get("lat"), long=dealer.get("long"),
                                short_name=dealer.get("short_name"), 
                                st=dealer.get("st"), state=dealer.get("state"), zip=dealer.get("zip"))
        # info = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
        #                 id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
        #                 short_name=dealer["short_name"], state=dealer["state"],
        #                 st=dealer["st"], zip=dealer["zip"])
    elif json_result:
        result = json_result["message"]
    else:
        result = "Unknown error"
    return info, result

def get_dealers_by_state (url, state):
    info = []
    result = "ok"
    # Call get_request with a URL parameter
    json_result, status_code = get_request(url, None, state=state)
    if status_code == 200 and json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # dlr_data = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer.get("address"), city=dealer.get("city"), full_name=dealer.get("full_name"),
                                   id=dealer.get("id"), lat=dealer.get("lat"), long=dealer.get("long"),
                                   short_name=dealer.get("short_name"), state=dealer.get("state"),
                                   st=dealer.get("st"), zip=dealer.get("zip"))
            # dealer_obj = CarDealer(address=dlr_data.get("address"), city=dlr_data.get("city"), full_name=dlr_data.get("full_name"),
            #                        id=dlr_data.get("id"), lat=dlr_data.get("lat"), long=dlr_data.get("long"),
            #                        short_name=dlr_data.get("short_name"), state=dlr_data.get("state"),
            #                        st=dlr_data.get("st"), zip=dlr_data.get("zip"))
            info.append(dealer_obj)
    elif json_result:
        result = json_result["message"]
    else:
        result = "Unknown error"
    return info, result



def get_dealer_reviews_from_cf (url, dealerId):
    info = []
    result = "ok"
    # Call get_request with a URL parameter
    json_result, status_code = get_request(url, None, dealerId=dealerId)
    if status_code == 200 and json_result:
        # Get the row list in JSON as reviews
        reviews = json_result["body"]["data"]
        # For each review object
        for review in reviews:
            if (dealerId == review.get("dealership")):
            # Create a DealerReview object with values in object
            #sentiment = analyze_review_sentiments(review["review"])
                review_obj = DealerReview( id=review.get("id"), name=review.get("name"), review=review.get("review"),
                                    purchase=review.get("purchase"), car_make=review.get("car_make", None), 
                                    car_model=review.get("car_model", None), car_year=review.get("car_year", None),
                                    purchase_date=review.get("purchase_date", None))
                info.append(review_obj)
    elif json_result:
        result = json_result["message"]
    else:
        result = "Unknown error"
    return info, result






# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



