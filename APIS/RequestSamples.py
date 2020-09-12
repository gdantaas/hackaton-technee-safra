from APIS import APIRequest

newAccount = APIRequest.WebServiceSafra(accountid='00711234511')

'''--------------------------------------------------- EXEMPLOS DE CHAMADA DAS APIS ---------------------------------------------------'''
'''print(f'Dados da conta {newAccount.getAccountData()}')
print(f'Saldos {newAccount.getBalances()}')
print(f'Extrato {newAccount.getTransactions()}')
print('Transferencia:', end= ' ')
print(newAccount.transfer(type="TEF",
                          transInfo="Mensalidade Academia",
                          destinyAcc={
                              "Bank": "422",
                              "Agency": "0071",
                              "Id": "1234533",
                              "Cpf": "12345678933",
                              "Name": "Mark Zuckerberg da Silva",
                              "Goal": "Credit"
                          },
                          amount="250.00",
                          currency="BRL"))
print(f'Lista morning Call {newAccount.listMorningCalls("2020-07-09", "2020-07-14")}')'''
#print(f'Contato de abertura de conta {newAccount.contactOpenAcc(name="Eric Evans Silva", email="eric.evans@ddd.com", phone="+5511911111111")}')