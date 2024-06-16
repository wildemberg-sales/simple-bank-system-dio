import random
import textwrap
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

ROOT_PATH = Path(__file__).parent

clientes = []
contas = []


class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
            """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0

    def realizar_trasacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("\n@@@ Você execedeu o limite de transações diárias @@@\n")
            return

        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.conta.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, endereco, cpf):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, numero, cliente):
        self._numero = numero
        self._cliente = cliente
        self._saldo = 0
        self._agencia = "0001"
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self._saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação Falhou: Saldo Insuficiente @@@\n")
        elif valor > 0:
            self._saldo -= valor
            print("\n@@@ Operação Realizada com Sucesso @@@\n")
            return True
        else:
            print("\n@@@ Operação Falhou: Valor Inválido @@@\n")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n@@@ Operação Realizada com Sucesso @@@\n")
            return True
        else:
            print("\n@@@ Operação Falhou: Valor Inválido @@@\n")

        return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saque=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saque = limite_saque

    def sacar(self, valor):
        numero_saque = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        execedeu_saques = numero_saque >= self._limite_saque

        if excedeu_limite:
            print("\n@@@ Operação Falhou: Limite de Saque Excedido @@@\n")
        elif execedeu_saques:
            print("\n@@@ Operação Falhou: Limite de Saque Excedido @@@\n")
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""
        Agência: \t{self.agencia}
        C/C:     \t{self.numero}
        Titular: \t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.now().date()
        transacoes = []

        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d/%m/%Y %H:%M:%S").date()
            if data_atual == data_transacao:
                transacoes.append(transacao)

        return transacoes


class Transacao(ABC):
    @property
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        data_hora = datetime.utcnow().strftime("%y-%m-%d %H:%M:%S")

        with open(ROOT_PATH / "log.txt", "a") as arquivo:
            arquivo.write(
                f"[{data_hora}] Função '{func.__name__.upper()}' executada com argumentos {args} e {kwargs}. Retornou {resultado}\n"
            )

        print(f"{data_hora}: {func.__name__.upper()}")
        return resultado

    return envelope


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta cadastrada. @@@")
        return

    return cliente.contas[0]


@log_transacao
def deposito(clientes):

    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado. @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_trasacao(conta, transacao)


@log_transacao
def saque(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado. @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_trasacao(conta, transacao)


def extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado. @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n@@@ Extrato @@@")
    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():  # pode ser passado o tipo de transação
        tem_transacao = True
        extrato += f"\n{transacao['tipo']}: \n \t R$ {transacao['valor']:.2f}"

    if not tem_transacao:
        extrato = "Não foram realizadas movimentações nesta conta"

    print(extrato)
    print(f"\nSaldo:\n \tR$ {conta.saldo:.2f}\n")
    print("@" * 30)


@log_transacao
def criar_conta(clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado. @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=random.randint(1000, 9999))
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n@@@ Conta criada com sucesso. @@@\n")


def listar_contas(contas):
    for conta in ContasIterador(contas):
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Cliente já cadastrado. @@@")
        return

    nome = input("Informe o nome do cliente: ")
    data_nascimento = input("Informe a data de nascimento do cliente (dd-mm-aaaa): ")
    endereco = input("Informe o endereço do cliente (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=nome, endereco=endereco, cpf=cpf)

    clientes.append(cliente)

    print("\n@@@ Cliente cadastrado com sucesso. @@@\n")


menu = """
    [d] - Depositar
    [s] - Sacar
    [e] - Extrato
    [cu] - Cadastrar Usuário
    [cc] - Cadastrar Conta
    [lc] - Listar Contas
    [q] - Sair
"""

while True:
    opcao = input(menu)

    if opcao == "d":
        deposito(clientes)
    elif opcao == "s":
        saque(clientes)
    elif opcao == "e":
        extrato(clientes)
    elif opcao == "cu":
        criar_cliente(clientes)
    elif opcao == "cc":
        criar_conta(clientes, contas)
    elif opcao == "lc":
        listar_contas(contas)
    elif opcao == "q":
        print("\n@@@ Sistema Encerrado @@@\n")
        break
    else:
        print("\n@@@ Opção Inválida @@@\n")
