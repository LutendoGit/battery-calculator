import requests
import json
url = "http://ip-api.com/json/"
url = "http://api.weatherstack.com/current"
url = http://api.weatherstack.com/current
?access_key=af68d305bf256d427a5dabff76e8e12d

responds = requests.get(url).json()

print(responds)

#print(responds['country'])
#print(responds['city'])
#print(responds['isp'])


#for key, value in responds.items():
    #print(f"{key} = {value}")

#print(json.dumps(responds, indent=2))


