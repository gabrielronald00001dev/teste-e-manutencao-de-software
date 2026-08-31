"""Entidade Material: item alocável, com status e condição controlados."""

import math


class Material:

    STATUS_DISPONIVEL = "Disponível"
    STATUS_ALOCADO = "Alocado"
    STATUS_VALIDOS = (STATUS_DISPONIVEL, STATUS_ALOCADO)

    CONDICAO_NOVO = "Novo"
    CONDICAO_BOM = "Bom"
    CONDICAO_RUIM = "Ruim"
    CONDICAO_INUTILIZADO = "Inutilizado"
    CONDICOES_VALIDAS = (
        CONDICAO_NOVO,
        CONDICAO_BOM,
        CONDICAO_RUIM,
        CONDICAO_INUTILIZADO,
    )

    def __init__(
        self,
        tipo_id=None,
        nome=None,
        valor_compra=0.0,
        valor_alocacao_diaria=0.0,
        status=STATUS_DISPONIVEL,
        condicao=CONDICAO_NOVO,
        id=None,
    ):
        self.__id = id
        self.__tipo_id = tipo_id
        self.__nome = self.__texto(nome)
        self.__valor_compra = self.__numero(valor_compra)
        self.__valor_alocacao_diaria = self.__numero(valor_alocacao_diaria)
        self.__status = self.__texto(status)
        self.__condicao = self.__texto(condicao)

    # ------------------------------------------------------------------
    # Gets e Sets
    # ------------------------------------------------------------------
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, valor):
        self.__id = valor

    @property
    def tipo_id(self):
        return self.__tipo_id

    @tipo_id.setter
    def tipo_id(self, valor):
        self.__tipo_id = valor

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        self.__nome = self.__texto(valor)

    @property
    def valor_compra(self):
        return self.__valor_compra

    @valor_compra.setter
    def valor_compra(self, valor):
        self.__valor_compra = self.__numero(valor)

    @property
    def valor_alocacao_diaria(self):
        return self.__valor_alocacao_diaria

    @valor_alocacao_diaria.setter
    def valor_alocacao_diaria(self, valor):
        self.__valor_alocacao_diaria = self.__numero(valor)

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        self.__status = self.__texto(valor)

    @property
    def condicao(self):
        return self.__condicao

    @condicao.setter
    def condicao(self, valor):
        self.__condicao = self.__texto(valor)

    # ------------------------------------------------------------------
    # Conversores auxiliares
    # ------------------------------------------------------------------
    @staticmethod
    def __texto(valor):
        if valor is None:
            return None
        return str(valor).strip()

    @staticmethod
    def __numero(valor):
        if valor is None or valor == "":
            return None
        return float(valor)

    # ------------------------------------------------------------------
    # Regras de negócio
    # ------------------------------------------------------------------
    def atualizar_status(self, novo_status):
        """Troca o status validando o domínio (Disponível / Alocado)."""
        novo_status = self.__texto(novo_status)
        if novo_status not in self.STATUS_VALIDOS:
            raise ValueError(
                "Status inválido: {!r}. Use um de {}.".format(
                    novo_status, ", ".join(self.STATUS_VALIDOS)
                )
            )
        self.__status = novo_status
        return self.__status

    def atualizar_condicao(self, nova_condicao):
        """Troca a condição validando o domínio (Novo/Bom/Ruim/Inutilizado)."""
        nova_condicao = self.__texto(nova_condicao)
        if nova_condicao not in self.CONDICOES_VALIDAS:
            raise ValueError(
                "Condição inválida: {!r}. Use uma de {}.".format(
                    nova_condicao, ", ".join(self.CONDICOES_VALIDAS)
                )
            )
        self.__condicao = nova_condicao
        return self.__condicao

    def esta_disponivel(self):
        """Só é alocável se estiver Disponível e não estiver Inutilizado."""
        return (
            self.__status == self.STATUS_DISPONIVEL
            and self.__condicao != self.CONDICAO_INUTILIZADO
        )

    def validar(self):
        if not self.__nome:
            raise ValueError("O nome do material é obrigatório.")
        if self.__tipo_id is None:
            raise ValueError("O tipo do material é obrigatório.")
        if self.__valor_compra is None or self.__valor_compra < 0:
            raise ValueError("O valor de compra deve ser maior ou igual a zero.")
        if self.__valor_alocacao_diaria is None or self.__valor_alocacao_diaria <= 0:
            raise ValueError("O valor de alocação diária deve ser maior que zero.")
        if self.__status not in self.STATUS_VALIDOS:
            raise ValueError("Status inválido: {!r}.".format(self.__status))
        if self.__condicao not in self.CONDICOES_VALIDAS:
            raise ValueError("Condição inválida: {!r}.".format(self.__condicao))
        return True

    # ------------------------------------------------------------------
    # Métodos de cálculo
    # ------------------------------------------------------------------
    def calcular_valor_alocacao(self, dias):
        """Valor bruto da alocação para uma quantidade de dias."""
        if dias is None:
            raise ValueError("A quantidade de dias é obrigatória.")
        dias = int(dias)
        if dias <= 0:
            raise ValueError("A quantidade de dias deve ser maior que zero.")
        return round(self.__valor_alocacao_diaria * dias, 2)

    def calcular_dias_para_retorno(self):
        """Dias de alocação necessários para pagar o valor de compra."""
        if not self.__valor_alocacao_diaria:
            raise ValueError(
                "Não é possível calcular o retorno sem valor de alocação diária."
            )
        return math.ceil(self.__valor_compra / self.__valor_alocacao_diaria)

    def para_dicionario(self):
        return {
            "id": self.__id,
            "tipo_id": self.__tipo_id,
            "nome": self.__nome,
            "valor_compra": self.__valor_compra,
            "valor_alocacao_diaria": self.__valor_alocacao_diaria,
            "status": self.__status,
            "condicao": self.__condicao,
        }

    def __repr__(self):
        return "Material(id={!r}, nome={!r}, status={!r}, condicao={!r})".format(
            self.__id, self.__nome, self.__status, self.__condicao
        )
