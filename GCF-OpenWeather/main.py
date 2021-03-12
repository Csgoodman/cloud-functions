import requests
import datetime
import json

import flask
import logging

###################### Main
def main(request):
    try:
        # Parse incoming JSON request data to Python Dict
        request = request.get_json() # {"apiKey": "e9ae407b3b45b2f4220e52d5995fbd6d"} passed into Secrets
        

        # Get Authentication Details From Fivetran Request
        api_key = request['secrets']['apiKey']

        # API Specific Inputs To Function
        id = 5378538 #Oakland

        # Request Data From OpenWeather API
        data = request_data(id, api_key)

        # Define Time for Next Cursor
        state_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Assemble Response for Fivetran
        response = assemble_response(data, state_time)

        # Send Response to Fivetran
        headers = {"Content-Type": "application/json"}
        return flask.make_response(response,200,headers)
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)


###################### Request to OpenWeather API
def request_data(id, api_key):
    url = "https://api.openweathermap.org/data/2.5/weather?id={}&appid={}".format(id, api_key)
    params = {"units": "imperial"} # units for returned temperature
    weatherResponse = requests.get(url, params=params).json()
    
    # Clean Up Data From OpenWeather API Into New Python Dict
    newobj = {
        'longitude': weatherResponse['coord']['lon'],
        'latitude': weatherResponse['coord']['lat'],
        'description': weatherResponse['weather'][0]['description'],
        'temperature': weatherResponse['main']['temp'],
        'temp_feels_like': weatherResponse['main']['feels_like'],
        'temperature_min': weatherResponse['main']['temp_min'],
        'temperature_max': weatherResponse['main']['temp_max'],
        'pressure': weatherResponse['main']['pressure'],
        'humidity': weatherResponse['main']['humidity'],
        'wind_speed': weatherResponse['wind']['speed'],
        'dt': weatherResponse['dt'],
        'city_name': weatherResponse['name']
    }
   
    # Place Python Object Into Data Array
    data = []
    data.append(newobj)
    return data


###################### Assemble Response
def assemble_response(data, state):
    response_dict = {
        "state": state,
        "schema": {
            "daily_weather": {
                "primary_key": ["dt"]
            }
        },
        "insert": {
            "daily_weather": data
        },
        "hasMore": False
    }
    # Convert to JSON From Python Dict and Return
    return json.dumps(response_dict) 




#### TESTING ############
# testing_data = request_data(5378538, "e9ae407b3b45b2f4220e52d5995fbd6d") # TESTING
# print(testing_data)

# state_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
# testing_response = assemble_response(testing_data, state_time)
# print(testing_response)
