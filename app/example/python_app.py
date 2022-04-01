import requests as r

# add sample prompt
prompt = "How to draw a circle"

# convert to dictionary
keys = {"user_prompt": prompt}

# send GET request
prediction = r.get("http://127.0.0.1:8000/answers/", params=keys)

# parse results
results = prediction.json()

# print response
print(results["data"])
