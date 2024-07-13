import json
import requests

# ===========================GPT-4 API Call===========================

def create_sys_msg(sys_msg, prompt):
    messages = [
        {"role": "system", "content": sys_msg},
        {"role": "user", "content": prompt}
    ]
    return json.dumps(messages)

def generate_response(prompt):
    try:
        url = "<YOUR API URL>"
        headers = {
            "Content-Type": "application/json"
        }
        body = {
            "application_id" : "<YOUR APPLICATION ID>",
            "request_type": "gpt4-completion",
            "prompt": prompt
        }
        response = requests.post(url, headers=headers, json=body)
        response=response.json()[0]['RESPONSE']
    except Exception as e:
        response = "Error: " + str(e)
    return response