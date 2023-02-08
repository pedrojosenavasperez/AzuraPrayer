import requests
import subprocess
import json

def getAzureToken():
    proc = subprocess.Popen(["az account get-access-token --resource-type ms-graph"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    out  = (str(out).replace("\\n","").split("'")[1])
    x = json.loads(out)
    return x["accessToken"]

proxies = {
   'http': 'http://localhost:8080',
   'https': 'http://localhost:8080',
}

def AzureADMSInvitation(InvitedUserEmailAddress , InvitedUserDisplayName = "Azura spokesman" , InviteRedirectURL = "https://portal.azure.com", InvitedUserType = "Guest" , SendInvitationMessage = "False" ):
    headers = {
        'Host': 'graph.microsoft.com',
        'User-Agent': 'curl/7.74.0',
        'Authorization': 'Bearer ' + getAzureToken(),
        'Accept-Encoding': 'gzip, deflate' ,
        'Accept': '*/*',
        'Connection': 'close',
        'Content-Type': 'application/json',
    }


    json_data = {
        'invitedUserEmailAddress': InvitedUserEmailAddress,
        'inviteRedirectUrl': InviteRedirectURL,
        'invitedUserDisplayName': InvitedUserDisplayName,
        'invitedUserType': InvitedUserType,
        'sendInvitationMessage': SendInvitationMessage,
    }

    response = requests.post('https://graph.microsoft.com/v1.0/invitations', headers=headers, json=json_data, verify=False ) #, proxies=proxies)
    print(response.json())
    
AzureADMSInvitation(InvitedUserEmailAddress)
