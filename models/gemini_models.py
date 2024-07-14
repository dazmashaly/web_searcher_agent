import requests
import json
import os
from utils.helper_functions import load_config
from langchain_core.messages.human import HumanMessage
import time
class GeminiJSONModel:
    def __init__(self, temperature=0, model=None):
        config_path = os.path.join(r"D:\Data\agents\my_own_custom\config.yaml")
        load_config(config_path)
        self.api_key = os.environ.get("GOOGLE_API_KEY")
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.model_endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
        self.temperature = temperature
        self.model = model

    def invoke(self, messages):
        system = messages[0]["content"]
        user = messages[1]["content"]

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"system:{system}. Your output must be JSON formatted. Just return the specified JSON format, do not prepend your response with anything.\n\nuser:{user}"
                        }
                    ]
                }
            ],
            "generationConfig": {
                "response_mime_type": "application/json",
                "temperature": self.temperature
            },
        }

        try:
            if self.model.endswith("pro"):
                time.sleep(20)
                # print("waited 20 seconds to not get error 429")
            request_response = requests.post(
                self.model_endpoint, 
                headers=self.headers, 
                data=json.dumps(payload)
            )
            
            print("REQUEST RESPONSE", request_response.status_code)
            
            
            request_response_json = request_response.json()

            if 'candidates' not in request_response_json or not request_response_json['candidates']:
                raise ValueError("No content in response")

            response_content = request_response_json['candidates'][0]['content']['parts'][0]['text']
            
            response = json.loads(response_content)
            response = json.dumps(response)

            response_formatted = HumanMessage(content=response)

            return response_formatted
        except (requests.RequestException, ValueError, KeyError, json.JSONDecodeError) as e:
            error_message = f"Error in invoking model! {str(e)}"
            print("ERROR", error_message)
            response = {"error": error_message}
            response_formatted = HumanMessage(content=json.dumps(response))
            return response_formatted

class GeminiModel:
    def __init__(self, temperature=0, model=None):
        config_path = os.path.join(r"D:\Data\agents\my_own_custom\config.yaml")
        load_config(config_path)
        self.api_key = os.environ.get("GOOGLE_API_KEY")
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.model_endpoint = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={self.api_key}"
        self.temperature = temperature
        self.model = model

    def invoke(self, messages):
        system = messages[0]["content"]
        user = messages[1]["content"]

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"system:{system}\n\nuser:{user}"
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": self.temperature
            },
        }

        try:
            if self.model.endswith("pro"):
                time.sleep(20)
                # print("waited 20 seconds to not get error 429")
            request_response = requests.post(
                self.model_endpoint, 
                headers=self.headers, 
                data=json.dumps(payload)
            )
            
            print("REQUEST RESPONSE", request_response.status_code)
            
            request_response_json = request_response.json()

            if 'candidates' not in request_response_json or not request_response_json['candidates']:
                raise ValueError("No content in response")

            response_content = request_response_json['candidates'][0]['content']['parts'][0]['text']
            

            return response_content
        except (requests.RequestException, ValueError, KeyError, json.JSONDecodeError) as e:
            error_message = f"Error in invoking model! {str(e)}"
            print("ERROR", error_message)
            response = {"error": error_message}
            return response
