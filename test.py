import requests

url = "http://127.0.0.1:5000/ask"  
question = "what is the scope of a data scientist?"
data = {'question': question}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response Text:", response.text) 
