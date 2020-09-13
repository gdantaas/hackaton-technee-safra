from flask import Flask, request
from flask_cors import CORS
from APIS import APIRequest
import os
import getDbData
import json

from APIS import APIRequest

app = Flask(__name__)
app._static_folder = os.path.abspath('APIS/')
CORS(app)


@app.route('/', methods=['GET'])
def isUp():
    """localhost:8080/"""
    session = APIRequest.WebServiceSafra()
    return session.verifyUp()


@app.route('/token', methods=['POST'])
def token():
    """localhost:8080/token"""
    session = APIRequest.WebServiceSafra()
    return session.getToken()


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


'''------------------------------------------------ DATABASE ROUTES ------------------------------------------------'''


@app.route('/validlogin', methods=['POST'])
def validLogin():
    """
    localhost:8080/validlogin
    body = {
            "id": "1",
            "pwd":"hsasyagsyag"
            }
    """
    token = APIRequest.WebServiceSafra().getToken()
    profile = list()

    data = request.json
    base = getDbData.dbData()
    # User Data
    ret = base.selectData('AppAccount', f"customer_id = {data['id']} and customer_password_hash = '{data['pwd']}'")
    if len(ret) == 0:
        return 'Unauthorized'
    else:
        profile.append({'customer_id': ret[0][0], 'customer_name': ret[0][3], 'customer_email': ret[0][1], 'token': token,'banks': []})
        # Bank Accounts
        ret = base.selectData('Bank', f"customer_id = {data['id']}", columns='Bank.bank_id, Bank.bank_name, acc.Account_id',
                              join='INNER JOIN '
                                   'BankAccount acc '
                                   'on Bank.bank_id '
                                   '= '
                                   'acc.Account_bank_id')
        profile[0]['banks'] = [{'bank_id': x[0], 'bank_name': x[1], 'bank_account': x[2]} for x in ret]

        return json.dumps(profile[0])


@app.route('/transactionsdb/<account_id>', methods=['GET'])
def transactionDB(account_id):
    """
    localhost:8080/transactionsDB/1
    """
    profile = list()
    base = getDbData.dbData()
    # User Data
    ret = base.selectData('Transactions', f"account_id = {account_id}")
    if len(ret) == 0:
        return 'None'
    else:
        transactions = [{
            'transaction_id': x[0],
            'account_id': x[1],
            'transaction_booking_date': x[2],
            'transaction_date': x[3],
            'transaction_recipient_account': x[4],
            'transaction_receipt': x[5],
            'transaction_credit_debit_indicator': x[6],
            'transaction_currency': x[7],
            'transaction_amount': int(x[8]),
            'transaction_description': x[9],
            'transaction_status': x[10]
        } for x in ret]

        return json.dumps(transactions[0])


if __name__ == '__main__':
    # Router(app)
    app.run(port='8080')
    print('Server started!')
