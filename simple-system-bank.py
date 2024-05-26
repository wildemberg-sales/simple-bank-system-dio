menu = """
    [d] - Depositar
    [s] - Sacar
    [e] - Extrato
    [cu] - Cadastrar Usuário
    [cc] - Cadastrar Conta
    [lc] - Listar Contas
    [q] - Sair
"""

clientes = []
contas = []
num_contas = 1
saldo = 0
limite = 500
extrato = ""
numero_saque = 0
LIMITE_SAQUE = 3
AGENCIA = "0001"

def deposito(valor):
    global saldo
    global extrato

    if valor > 0:
        saldo += valor
        print("=" * 30)
        print("===========Depósito Realizado===========")
        print(f"Seu saldo atual: {saldo:.2f}")
        print("=" * 30)
        extrato += f" Ação: Depósito - Valor: R$ {valor:.2f}\n"
    else:
        print("=" * 30)
        print("Coloque um valor maior que zero!")
        print("=" * 30)

def saque(*,valor):
    global saldo
    global extrato
    global numero_saque
    global LIMITE_SAQUE
    global limite

    if saldo > 0 and numero_saque < LIMITE_SAQUE and valor <= limite and valor > 0:
        saldo -= valor
        numero_saque += 1
        print("=" * 30)
        print("===========Saque Realizado===========")
        print(f"Seu saldo atual: {saldo:.2f}")
        print("=" * 30)
        extrato += f" Ação: Saque - Valor: R$ {valor:.2f}\n"
    else:
        if saldo < 0:
            print("=" * 30)
            print("\nSaldo insuficiente\n")
            print("=" * 30)
        elif numero_saque >= LIMITE_SAQUE:
            print("=" * 30)
            print("\nLimite de Saques atingido\n")
            print("=" * 30)
        else:
            print("=" * 30)
            print("\nLimite de valor de saque maior do que permitido\n")
            print("=" * 30)

def imprimi_extrato(saldo, /, extrato):
    print("========================EXTRATO========================\n")
    print(extrato)
    print(f"\nSeu saldo atual é de R$ {saldo:.2f}")
    print("=" * 30)

def criar_usuario(*, nome, data_nascimento, cpf, estado):
    global clientes

    cliente = {
        "CPF":cpf,
        "dados":{
            "nome":nome,
            "data_nascimento":data_nascimento,
            "estado":{
                "logradouro":estado['logradouro'],
                "nro":estado['nro'],
                "bairro":estado['bairro'],
                "cidade_estado":estado['cidade_estado']
            }
        }
    }

    if any(c["CPF"] == cpf for c in clientes):
        print()
        print("=" * 30)
        print("Usuário já existente, operação cancelada!")
        print("=" * 30)
        return

    try:
        clientes.append(cliente)
        print("=" * 30)
        print(clientes)
        print("Cliente cadastrado com sucesso!")
        print("=" * 30)
    except:
        print("=" * 30)
        print(clientes)
        print("Cliente não cadastrado, repita a operação")
        print("=" * 30)

def criar_conta(*, cpf):
    global AGENCIA
    global contas
    global clientes
    global num_contas
    
    if any(c["CPF"] == cpf for c in clientes):
        conta = {
        "CPF":cpf,
        "conta":num_contas,
        "agencia":AGENCIA
        }

        contas.append(conta)
        num_contas += 1
        print("=" * 30)
        print(f"Conta cadastrada com sucesso:\n{conta}")
        print("=" * 30)
    else:
        print("=" * 30)
        print("Usuário não encontrado no sistema!")
        print("=" * 30)
    
def listar_contas():
    if len(contas) > 0:
        for c in contas:
            print(f"""
                \n
                CPF Cliente - {c['CPF']}
                Número Conta - {c['conta']}
                Agência Conta - {c['agencia']}
            """)
    else:
        print("=" * 30)
        print("Não há contas cadastradas")
        print("=" * 30)

while True:
    print(menu)
    opcao = input("Escolha uma opção: ")

    if opcao == "q":
        print("\nSaindo do sistema...\n")
        break

    elif opcao == "d":
        print("=" * 30)
        valor = float(input("Digite o valor a ser depositado: "))
        deposito(valor)

    elif opcao == "s":
        print("=" * 30)
        valor = float(input("Digite o valor a ser sacado: "))
        saque(valor = valor)

    elif opcao == "e":
        imprimi_extrato(saldo, extrato = extrato)

    elif opcao == "cu":
        print("=" * 30)
        nome = input("Qual o nome do cliente: ")
        data_nascimento = input("Qual a data de nascimento do cliente (dd-mm-yyyy): ")
        cpf = input("Qual o CPF do cliente: ")
        print("\nAgora vamos cadastrar o endereço\n")
        logradouro = input("Qual o logradouro: ")
        num = int(input("Qual o numero: "))
        bairro = input("Qual o bairro: ")
        cidade_estado = input("Qual a cidade/estado: ")

        criar_usuario(
            nome=nome, 
            data_nascimento=data_nascimento, 
            cpf=cpf, 
            estado={
                "logradouro":logradouro, 
                "nro":num, 
                "bairro":bairro, 
                "cidade_estado":cidade_estado
            }
        )
    
    elif opcao == "cc":
        cpf = input("Qual o CPF do usuário que deseja cadastrar: ")
        criar_conta(cpf=cpf)

    elif opcao == "lc":
        listar_contas()

    else:
        print("Opção inválida")