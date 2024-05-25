#somente deposito positivo, todos os depositos devem ser armazenados no extrato
#3 saques diarios, com limite de 500 por saque, se não puder sacar mostrar mensagem, tem que estar no extrato 
#deve mostrar todos saques e depositos, e no fianl listar o saldo atual com R$ no inicio

menu = """
    [d] - Depositar
    [s] - Sacar
    [e] - Extrato
    [q] - Sair
"""

saldo = 0
limite = 500
extrato = ""
numero_saque = 0
LIMITE_SAQUE = 3

while True:
    print(menu)
    opcao = input("Escolha uma opção: ")

    if opcao == "q":
        print("\nSaindo do sistema...\n")
        break

    elif opcao == "d":
        print("=======================================================")
        valor = float(input("Digite o valor a ser depositado: "))

        if valor > 0:
            saldo += valor
            print("=======================================================")
            print(f"Seu saldo atual: {saldo:.2f}")
            print("=======================================================")
            extrato += f" Ação: Depósito - Valor: R$ {valor:.2f}\n"
        else:
            print("=======================================================")
            print("Coloque um valor maior que zero!")
            print("=======================================================")

    elif opcao == "s":
        print("=======================================================")
        valor = float(input("Digite o valor a ser sacado: "))
        if saldo > 0 and numero_saque < LIMITE_SAQUE and valor < limite and valor > 0:
            saldo -= valor
            numero_saque += 1
            print("=======================================================")
            print(f"Seu saldo atual: {saldo:.2f}")
            print("=======================================================")
            extrato += f" Ação: Saque - Valor: R$ {valor:.2f}\n"
        else:
            if saldo < 0:
                print("=======================================================")
                print("\nSaldo insuficiente\n")
                print("=======================================================")
            elif numero_saque >= LIMITE_SAQUE:
                print("=======================================================")
                print("\nLimite de Saques atingido\n")
                print("=======================================================")
            else:
                print("=======================================================")
                print("\nLimite de valor de saque maior do que permitido\n")
                print("=======================================================")
    

    elif opcao == "e":
        print("========================EXTRATO========================")
        print(extrato)
        print("=======================================================")
    
    else:
        print("Opção inválida")