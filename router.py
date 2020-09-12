from flask import Flask, request
import os

from APIS import APIRequest

app = Flask(__name__)
app._static_folder = os.path.abspath('APIS/')


@app.route('/', methods=['GET'])
def isUp():
    """localhost:8080/"""
    session = APIRequest.WebServiceSafra()
    return session.verifyUp()


@app.route('/accountData/<accountid>', methods=['GET'])
def accountData(accountid):
    """localhost:8080/accountData/00711234511"""
    session = APIRequest.WebServiceSafra(accountid=accountid)
    return session.getAccountData()


@app.route('/balances/<accountid>', methods=['GET'])
def balances(accountid):
    """localhost:8080/balances/00711234511"""
    session = APIRequest.WebServiceSafra(accountid=accountid)
    return session.getBalances()


@app.route('/transactions/<accountid>', methods=['GET'])
def transactions(accountid):
    """localhost:8080/transactions/00711234511"""
    session = APIRequest.WebServiceSafra(accountid=accountid)
    return session.getTransactions()


@app.route('/transfer/<accountid>', methods=['POST'])
def transfer(accountid):
    """
    localhost:8080/transfer/00711234511
    body = {
            "Type": "TEF",
            "TransactionInformation": "Mensalidade Academia",
            "DestinyAccount": {
                "Bank": "422",
                "Agency": "0071",
                "Id": "1234533",
                "Cpf": "12345678933",
                "Name": "Mark Zuckerberg da Silva",
                "Goal":"Credit"
            },
            "Amount": {
                "Amount": "250.00",
                "Currency": "BRL"
            }
    }
    """
    data = request.json
    session = APIRequest.WebServiceSafra(accountid=accountid)
    return session.transfer(data['Type'], data['TransactionInformation'], data['DestinyAccount'],
                            data['Amount']['Amount'], data['Amount']['Currency'])


@app.route('/optin', methods=['POST'])
def optin():
    """
    localhost:8080/optin
    body = {
            "Name": "Eric Evans Silva",
            "Email":"eric.evans@ddd.com",
            "Phone":"+5511911111111"
            }
    """
    data = request.json
    session = APIRequest.WebServiceSafra()
    return session.contactOpenAcc(data['Name'], data['Email'], data['Phone'])


@app.route('/morningcalls', methods=['GET'])
def morningCalls():
    """localhost:8080/morningcalls"""
    session = APIRequest.WebServiceSafra()
    return session.listMorningCalls()


if __name__ == '__main__':
    # Router(app)
    app.run(port='8080')
    print('Server started!')
