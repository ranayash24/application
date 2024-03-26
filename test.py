import requests

API_URL = "http://localhost:3000/api/v1/prediction/b9b3b48c-b185-4429-8975-6a12533f38a9"

def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()
    
output = query({
    "question": "what is estimated budget of America?",
})
print(output)