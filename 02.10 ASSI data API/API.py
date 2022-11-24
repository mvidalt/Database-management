import requests
import json
url = "https://data.mongodb-api.com/app/data-cozpc/endpoint/data/v1/action/aggregate"
payload = json.dumps({
    "collection": "bikes",
    "database": "BookingBike",
    "dataSource": "Sandbox",
    "pipeline": [{
    "$group":{"_id":"$Brand"}}]".pretty"
})
headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': "j5MaXkwPuZ4Q0vu7VgCggGolq4Z5CU94lbMfKHFvdPzuMC7AFU2VVLLdKVVlXke0",
}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)