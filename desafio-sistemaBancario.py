# Variáveis globais para rastrear informações bancárias
saldo = 0
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

# Lista para armazenar informações dos usuários
usuarios = []

class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

class ContaCorrente:
    def __init__(self, agencia, numero_conta, usuario):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.saldo = 0
        self.extrato = []

def cadastrar_usuario():
    nome = input("Nome do cliente: ")
    data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    cpf = input("CPF do cliente: ")
    endereco = input("Endereço (logradouro, bairro-cidade/sigla estado): ")

    for usuario_existente in usuarios:
        if usuario_existente.cpf == cpf:
            print("Já existe um usuário com esse CPF.")
            return

    usuario = Usuario(nome, data_nascimento, cpf, endereco)
    usuarios.append(usuario)
    print("Usuário cadastrado com sucesso.")

def criar_conta_corrente():
    agencia = input("Número da agência: ")
    numero_conta = input("Número da conta: ")
    cpf_usuario = input("CPF do usuário associado à conta: ")

    for usuario in usuarios:
        if usuario.cpf == cpf_usuario:
            conta_corrente = ContaCorrente(agencia, numero_conta, usuario)
            usuario.conta_corrente = conta_corrente
            print("Conta corrente criada e associada ao usuário com sucesso.")
            return

    print("Usuário com o CPF especificado não encontrado.")

def deposito(valor):
    global saldo, extrato
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
        return True
    else:
        print("Operação falhou! O valor informado é inválido.")
        return False

def sacar(*, valor):
    global saldo, extrato, numero_saques
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato.append(f"Saque: R$ {valor:.2f}")
        numero_saques += 1
    else:
        print("Operação falhou! O valor informado é inválido.")

def extrato(*, nome=None):
    global saldo, extrato
    print("\n================ EXTRATO ================")
    if nome:
        print(f"Extrato de {nome}:")
    print("Não foram realizadas movimentações." if not extrato else "\n".join(extrato))
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

while True:
    menu = """
    [1] Cadastrar Usuário
    [2] Criar Conta Corrente
    [3] Depositar
    [4] Sacar
    [5] Extrato
    [6] Sair

    => """
    opcao = input(menu)

    if opcao == "1":
        cadastrar_usuario()
    elif opcao == "2":
        criar_conta_corrente()
    elif opcao == "3":
        valor = float(input("Informe o valor do depósito: "))
        deposito(valor)
    elif opcao == "4":
        valor = float(input("Informe o valor do saque: "))
        sacar(valor=valor)
    elif opcao == "5":
        cpf = input("Informe o CPF do usuário para exibir o extrato (ou deixe em branco para o seu próprio extrato): ")
        if not cpf:
            extrato()
        else:
            for usuario in usuarios:
                if usuario.cpf == cpf:
                    extrato(nome=usuario.nome)
                    break
            else:
                print("Usuário com o CPF especificado não encontrado.")
    elif opcao == "6":
        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
