import requests
import adal
import datetime

class graph:

    def __init__(self, tenant, client_id, client_secret):
        self.tenant = tenant
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None

    def getClientAccessToken(self):

        authority = "https://login.microsoftonline.com/" + self.tenant
        RESOURCE = "https://graph.microsoft.com"

        context = adal.AuthenticationContext(authority)

        # Use this for Client Credentials
        self.token = context.acquire_token_with_client_credentials(
            RESOURCE,
            self.client_id,
            self.client_secret
        )

        return self.token

    def getEndpointData(self, endpoint, params=None):
        headers = {
        'User-Agent' : 'O365CalPull',
        'Authorization' : 'Bearer {0}'.format(self.token["accessToken"]),
        'Accept' : 'application/json',
        'Content-Type' : 'application/json'
        }

        response = requests.get(url=endpoint, headers=headers, params=params)

        jsonResponse = response.json()
        nextLink = None

        data = jsonResponse

        if '@odata.nextLink' in jsonResponse:
            nextLink = str(jsonResponse['@odata.nextLink'])


        while nextLink != None:
            response = requests.get(url=nextLink, headers=headers)

            for entry in response.json()['value']:
                data['value'].append(entry)

            jsonResponse = response.json()

            if '@odata.nextLink' in jsonResponse:
                nextLink = str(jsonResponse['@odata.nextLink'])
            else:
                nextLink = None

        return data

    def validate_and_Reauthorize_token(self):
        now = datetime.datetime.now()
        tokenExpiration = datetime.datetime.strptime(self.token['expiresOn'][:-7], "%Y-%m-%d %H:%M:%S")

        if now > tokenExpiration:
            self.token = getClientAccessToken(self.tenant, self.client_id, self.client_secret)
        return self.token