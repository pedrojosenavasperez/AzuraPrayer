import requests
import xml.etree.ElementTree as ET
import json

mail = input("Enter email: ")

response = requests.get(f"https://login.microsoftonline.com/getuserrealm.srf?login={mail}&xml=1")
root = ET.fromstring(response.content)

if root.find('NameSpaceType').text == "Managed":
    print("Organization is in Azure under brand name of "+root.find('FederationBrandName').text )
    response = requests.get(f"https://login.microsoftonline.com/" + mail.split('@')[1] + "/.well-known/openid-configuration")
    data = json.loads(response.text)
    token_endpoint = data['token_endpoint']
    print("Tenant ID: " + data['token_endpoint'].split("/")[3])
