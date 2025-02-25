import textwrap
from datetime import datetime, date, timezone, timedelta

mascara_ptbr = '%d/%m/%Y %H:%M'
mascara_nascimento = '%d/%m/%Y'


class Usuario:
    def __init__(self, nome : str, cpf : str, data_nascimento : date, endereco : str):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco
    
    def __str__(self):
        return f"{self.__class__.__name__}:{', '.join([f'{chave} = {valor}' 
                                                    for chave, valor in self.__dict__.items()])}"  

    def filtrar_usuarios(cpf, usuarios : list):
        usuario_filtrado = [Usuario for usuario in usuarios if Usuario.get_cpf(usuario) == cpf]
        return usuarios[0] if usuario_filtrado else None
    
       
    def get_cpf(self):
        return self.cpf
    
    def criar_usuario(usuarios: list):
        contador_erro = 0
        data_valida = False
        print("Por favor insira seu nome")
        nome = input()
        
        if len(nome) < 3:
            print("O nome deve conter mais de 2 carácteres")
            return
        
        print("Por favor insira seu CPF")
        cpf = input()
        while len(cpf)  != 11:
            contador_erro +=1
            print("CPF Inválido, digite um com 11 digitos")
            cpf = input()
            if contador_erro == 3:
                print("CPF Inválido, tente novamente mais tarde")
                return

        existe_usuario = Usuario.filtrar_usuarios(cpf, usuarios)
        if existe_usuario:
            print("O CPF utilizado já está vínculado a uma conta existente")
            return 
        
        while data_valida == False:
            print("Por favor insira sua data de nascimento")
            print("Digite conforme o padrão: DIA/MÊS/ANO | XX/XX/XXXX")
            data_nascimento = (input())
            try:
                data_nascimento_formatada = datetime.strptime(data_nascimento, mascara_nascimento)
                data_valida = True
            except ValueError:
                print("Data de nascimento inválida, por favor insira no formato DIA/MÊS/ANO | XX/XX/XXXX")
            
        print("Por favor insira seu endereço")
        endereco = input()
        
        usuario = Usuario(nome, cpf, data_nascimento_formatada, endereco)
        usuarios.append(usuario)  
        return usuario  

    
class ContaCorrente:
    num_conta = 0
    def __init__(self, usuario : Usuario, saldo, limite):
        self.num_conta +=1
        self.numero_agencia = "0001"
        self.usuario = usuario
        self.saldo = saldo
        self.limite = limite
        
    def __str__(self):
        return f"{self.__class__.__name__}:{', '.join([f'{chave} = {valor}' 
                                                   for chave, valor in self.__dict__.items()])}"  

    def criar_conta_corrente(saldo, limite, cpf, usuarios: list):
        contador_erro = 0
        usuario = Usuario.filtrar_usuarios(cpf, usuarios)
        while usuario == None:
            print(f"O usuário com o CPF {cpf} não existe, tente novamente")
            contador_erro += 1
            print(f"Digite o seu CPF")
            cpf = input()
            usuario = Usuario.filtrar_usuarios(usuarios)
            if contador_erro == 3:
                print("É nécessário criar uma conta de usuário para este CPF!")
                return
        nova_conta_corrente = ContaCorrente(usuario, saldo, limite)
        return nova_conta_corrente
        

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [q]\tSair
    [c]\tCriar Usuário
    [cc]\tCriar Conta Corrente
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

def sacar(*,saldo: float, valor: float, extrato : list, quantidade_saque):
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
            if opcao == "c":
                usuario = Usuario.criar_usuario(usuarios)
                if usuario:
                    print(f"Conta criada, {usuario}")
            
            if opcao == "cc":
                print("Digite seu CPF")
                cpf = input()
                conta_corrente = ContaCorrente.criar_conta_corrente(saldo, limite, cpf, usuarios)
                if conta_corrente:
                    print(f"Conta corrente criada com sucesso, {conta_corrente}")
                
                
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
                    sacado = sacar(saldo = saldo, valor = valor, extrato=extrato, numero_saques = numero_saques)
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