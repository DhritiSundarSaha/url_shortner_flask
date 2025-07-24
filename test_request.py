# test_request.py
import requests
import json

url = "http://localhost:8080/api/shorten"
payload = {"url": "https://www.google.com"}
headers = {"Content-Type": "application/json"}

print("Sending POST request to the server...")

try:
    # Make the POST request with a 10-second timeout
    response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=10)

    # Print the results
    print(f"Status Code: {response.status_code}")
    print("Response from server:")
    print(response.json())

except requests.exceptions.RequestException as e:
    # This will catch any connection errors or timeouts
    print(f"An error occurred: {e}")