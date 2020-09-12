import requests
import json
import datetime as dt


class WebServiceSafra:

    def __init__(self, client_id='70a973924bdd4defb211bfd1c0309771',
                 client_secret='51971ed5-9704-4757-924a-d3431a2ae60d', accountid='00711234522'):
        self.url = 'https://af3tqle6wgdocsdirzlfrq7w5m.apigateway.sa-saopaulo-1.oci.customer-oci.com/fiap-sandbox'
        self.token = self.getToken(client_id, client_secret)
        self.accountID = accountid
        assert self.verifyUp(), 'Service Unvailable. Try again later.'

    def getToken(self, client_id, client_secret):
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
        return str(resp.status_code == 200)

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

        return 'Succeed' if resp.status_code else 'Failed'

    def listMorningCalls(self, fromDate='2020-07-09', toDate='2020-07-14'):
        path = f'/media/v1/youtube?fromData={fromDate}&toData={toDate}&playlist=morningCalls&channel=safra'
        headers = {
            'authorization': f'Bearer {self.token}'
        }
        resp = requests.request('GET', self.url + path, headers=headers)
        return resp.json()


newAccount = WebServiceSafra()
print(newAccount.listMorningCalls())

