import textwrap
from datetime import datetime, date, timezone, timedelta

mascara_ptbr = '%d/%m/%Y %H:%M'

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))
 
 
def depositar(saldo: int, valor: int, extrato : list):
    if valor < 0:
        print("Não é possível depositar valor negativo, por favor tente novamente")
        return
    data_hora_atu = datetime.now().strftime(mascara_ptbr)
    saldo += valor
    extrato.append(f"R${valor} operação de Depósito,  Data:{data_hora_atu}") 
    print(f"O valor de R${valor} foi depositado na conta, operação de Depósito")
    return saldo

def sacar(saldo: float, valor: float, extrato : list, quantidade_saque):
    if saldo < valor:
        print(f"Não foi possível realizar a operação, saldo insuficiente")
        return 
    if quantidade_saque > 3:
        print(f"O limite diário de saque foi atingido, tente novamente mais tarde")
        return
    if valor > 500:
        print(f"O saque máximo permitido é de R$500 reais, insira um valor menor")
        return
    data_hora_atu = datetime.now().strftime(mascara_ptbr)
    
    saldo -= valor
    extrato.append(f"R${valor} operação Saque, Data:{data_hora_atu}")
    print(f"O valor de R${valor} foi sacado da conta, operação de saque")
    return saldo

    
def mostrar_extrato(extratos: list, saldo):
    print("=============== EXTRATO ===============")
    for extrato in extratos:
        print(extrato) 
    print("===============   FIM   ===============")
        
def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    LIMITE_TRANSACOES = 10
    
    contador_transacoes = 0
    saldo = 0
    limite = 500
    extrato = []
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao != None:
            if opcao == "d":
                contador_transacoes +=1
                data_amanha = datetime.today() + timedelta(days=1)
                if contador_transacoes > LIMITE_TRANSACOES:
                    print(f"Você chegou no limite de transções diárias tente novamente no dia {data_amanha.strftime(mascara_ptbr)}")
                else:
                    valor = int(input("Insira o valor a ser depositado:"))
                    depositado = depositar(saldo, valor, extrato)
                    saldo += depositado
    
            if opcao == "s":
                contador_transacoes +=1
                data_amanha = datetime.today() + timedelta(days=1)
                if contador_transacoes > LIMITE_TRANSACOES:
                    print(f"Você chegou no limite de transções diárias tente novamente no dia {data_amanha.strftime(mascara_ptbr)}")
                else:
                    valor = int(input("Insira o valor a ser sacado:"))
                    sacado = sacar(saldo, valor, extrato, numero_saques)
                    saldo = sacado
                    numero_saques += 1

            if opcao == "e":
                mostrar_extrato(extrato, saldo)
                print(f" SALDO ATUAL:      R${saldo}")  
                

            if opcao == "q":
                break
        else:
            print("Operação Inválida, por favor selecione novamente a operação desejada")

main()