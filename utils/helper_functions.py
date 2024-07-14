import os
import yaml
import json
from datetime import datetime, timezone
import ast

def parse_json(response):
    try:
        # Assuming the model response is stored in a variable called 'model_output'
        try:
            response_json = json.loads(response)
            response = response_json['response']
            return response
        except json.JSONDecodeError:
            response_json = ast.literal_eval(response)
            response = response_json['response']
            return response
        
    except :
        try:
            response_json = json.loads(response[8:-4])
            response = response_json['response']
            return response
        except json.JSONDecodeError:
            response_json = ast.literal_eval(response[8:-4])
            response = response_json['response']
            return response
        

def load_config(file_path="config.yaml"):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
        for key, value in config.items():
            os.environ[key] = value

def get_current_utc_datetime():
    now_utc = datetime.now(timezone.utc)
    current_time_utc = now_utc.strftime("%Y-%m-%d %H:%M:%S %Z")
    return current_time_utc

def save_feedback(response, json_filename="memory.json"):
    # Create a dictionary with the response
    feedback_entry = {"feedback": response}
    
    # Load existing data from the JSON file if it exists
    if os.path.exists(json_filename):
        with open(json_filename, "r") as json_file:
            data = json.load(json_file)
    else:
        data = []
    
    # Append the new feedback entry to the data
    data.append(feedback_entry)
    
    # Write the updated data back to the JSON file
    with open(json_filename, "w") as json_file:
        json.dump(data, json_file, indent=4)

def read_feedback(json_filename="memory.json"):
    if os.path.exists(json_filename):
        with open(json_filename, "r") as json_file:
            data = json.load(json_file)
            # Convert the JSON data to a pretty-printed string
            json_string = json.dumps(data, indent=4)
            # json_string = str(data)
            return json_string
    else:
        return ""
    
def clear_json_file(json_filename="memory.json"):
    # Open the file in write mode to clear its contents
    with open(json_filename, "w") as json_file:
        json.dump([], json_file)

def initialize_json_file(json_filename="memory.json"):
    if not os.path.exists(json_filename) or os.path.getsize(json_filename) == 0:
        with open(json_filename, "w") as json_file:
            json.dump([], json_file)



# for checking if an attribute of the state dict has content.
def check_for_content(var):
    if var:
        try:
            var = var.content
            return var.content
        except:
            return var
    else:
        var = ""