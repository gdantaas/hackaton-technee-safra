import requests
import json
import datetime as dt


class WebServiceSafra:

    def __init__(self, client_id='f9d3cd9600874ac2803d03ca709b78eb',
                 client_secret='1a2075e3-b15e-4324-902c-0f12f8f08082', accountID=''):
        self.url = 'https://af3tqle6wgdocsdirzlfrq7w5m.apigateway.sa-saopaulo-1.oci.customer-oci.com/fiap-sandbox'
        self.token = self.getToken(client_id, client_secret)
        self.accountID = accountID
        assert self.verifyUp(), 'Service Unvailable. Try again later.'

    @staticmethod
    def getToken(client_id, client_secret):
        from base64 import b64encode

        urlToken = 'https://idcs-902a944ff6854c5fbe94750e48d66be5.identity.oraclecloud.com/oauth2/v1/token'
        token = b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')
        headers = {
            'authorization': f'Basic {token}',
            'content-type': 'application/x-www-form-urlencoded',
        }
        tokenService = requests.request('POST', urlToken, headers=headers,
                                        data="grant_type=client_credentials&scope=urn:opc:resource:consumer::all")
        return tokenService.json()['access_token']

    def verifyUp(self):
        path = '/health'
        headers = {
            'authorization': f'Bearer {self.token}'
        }
        resp = requests.request('GET', self.url + path, headers=headers)
        return resp.status_code == 200

    def getAccountData(self):
        path = f'/open-banking/v1/accounts/{self.accountID}'
        headers = {
            'authorization': f'Bearer {self.token}'
        }
        resp = requests.request('GET', self.url + path, headers=headers)
        return resp.json()

    def getBalances(self):
        path = f'/open-banking/v1/accounts/{self.accountID}/balances'
        headers = {
            'authorization': f'Bearer {self.token}'
        }
        resp = requests.request('GET', self.url + path, headers=headers)
        return resp.json()

    def getTransactions(self):
        path = f'/open-banking/v1/accounts/{self.accountID}/transactions'
        headers = {
            'authorization': f'Bearer {self.token}'
        }
        resp = requests.request('GET', self.url + path, headers=headers)
        return resp.json()

    def transfer(self, type, transInfo, destinyAcc, amount, currency):
        path = f'/accounts/v1/accounts/{self.accountID}/transfers'
        headers = {
            'Content-Type': 'application/json',
            'authorization': f'Bearer {self.token}'
        }
        data = {
            "Type": type,
            "TransactionInformation": transInfo,
            "DestinyAccount": destinyAcc,
            "Amount": {
                "Amount": "250.00",
                "Currency": currency
            }
        }
        data = json.dumps(data)

        resp = requests.request('POST', self.url + path, headers=headers, data=data)

        return resp.json()

    def contactOpenAcc(self, name, email, phone):
        path = '/accounts/v1/optin'
        headers = {
            'Content-Type': 'application/json',
            'authorization': f'Bearer {self.token}'
        }
        data = {
            "Name": name,
            "Email": email,
            "Phone": phone,
        }
        data = json.dumps(data)

        resp = requests.request('POST', self.url + path, headers=headers, data=data)

        return resp.status_code

    def listMorningCalls(self, fromDate=(dt.datetime.today() - dt.timedelta(days=7)).strftime('%Y-%m-%d'),
                         toDate=dt.datetime.today().strftime('%Y-%m-%d')):
        path = f'/media/v1/youtube?fromData={fromDate}&toData={toDate}&playlist=morningCalls&channel=safra'
        headers = {
            'authorization': f'Bearer {self.token}'
        }
        resp = requests.request('GET', self.url + path, headers=headers)
        return resp.json()

