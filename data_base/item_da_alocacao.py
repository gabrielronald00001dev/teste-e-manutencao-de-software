"""Entidade ItensDaAlocacao: linha de detalhe da locação.

`valor` guarda a diária do material congelada no momento da locação.
`data_devolucao` e `valor_pago` nascem vazios e só são preenchidos no retorno.
"""

from datetime import date, datetime


class ItemDaAlocacao:

    PERCENTUAL_MULTA_ATRASO = 0.20  # 20% da diária por dia de atraso

    def __init__(
        self,
        locacao_id=None,
        material_id=None,
        valor=None,
        data_devolucao=None,
        valor_pago=None,
        id=None,
    ):
        self.__id = id
        self.__locacao_id = locacao_id
        self.__material_id = material_id
        self.__valor = self.__numero(valor)
        self.__data_devolucao = self.__data_valida(data_devolucao)
        self.__valor_pago = self.__numero(valor_pago)

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
    def locacao_id(self):
        return self.__locacao_id

    @locacao_id.setter
    def locacao_id(self, valor):
        self.__locacao_id = valor

    @property
    def material_id(self):
        return self.__material_id

    @material_id.setter
    def material_id(self, valor):
        self.__material_id = valor

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor):
        self.__valor = self.__numero(valor)

    @property
    def data_devolucao(self):
        return self.__data_devolucao

    @data_devolucao.setter
    def data_devolucao(self, valor):
        self.__data_devolucao = self.__data_valida(valor)

    @property
    def valor_pago(self):
        return self.__valor_pago

    @valor_pago.setter
    def valor_pago(self, valor):
        self.__valor_pago = self.__numero(valor)

    # ------------------------------------------------------------------
    # Conversores auxiliares
    # ------------------------------------------------------------------
    @staticmethod
    def __numero(valor):
        if valor is None or valor == "":
            return None
        return float(valor)

    @staticmethod
    def __data_valida(valor):
        if valor is None or valor == "":
            return None
        if isinstance(valor, datetime):
            return valor.date()
        if isinstance(valor, date):
            return valor
        return date.fromisoformat(str(valor))

    # ------------------------------------------------------------------
    # Regras de negócio
    # ------------------------------------------------------------------
    def validar(self):
        if self.__locacao_id is None:
            raise ValueError("O item precisa estar vinculado a uma locação.")
        if self.__material_id is None:
            raise ValueError("O item precisa estar vinculado a um material.")
        if self.__valor is None or self.__valor <= 0:
            raise ValueError("O valor da diária do item deve ser maior que zero.")
        return True

    def foi_devolvido(self):
        return self.__data_devolucao is not None and self.__valor_pago is not None

    def registrar_devolucao(self, data_devolucao, data_locacao, previsao_devolucao=None):
        """Preenche data de devolução e valor pago (diárias + multa por atraso)."""
        if self.foi_devolvido():
            raise ValueError("A devolução deste item já foi registrada.")

        data_devolucao = self.__data_valida(data_devolucao)
        data_locacao = self.__data_valida(data_locacao)
        if data_devolucao is None:
            raise ValueError("A data de devolução é obrigatória.")
        if data_locacao is None:
            raise ValueError("A data da locação é obrigatória para o cálculo.")
        if data_devolucao < data_locacao:
            raise ValueError(
                "A data de devolução não pode ser anterior à data da locação."
            )

        self.__data_devolucao = data_devolucao
        self.__valor_pago = self.calcular_valor_devido(data_locacao, previsao_devolucao)
        return self.__valor_pago

    # ------------------------------------------------------------------
    # Métodos de cálculo
    # ------------------------------------------------------------------
    def calcular_dias_utilizados(self, data_locacao, data_devolucao=None):
        """Dias de uso. Devolução no mesmo dia conta como 1 diária."""
        data_locacao = self.__data_valida(data_locacao)
        data_devolucao = self.__data_valida(data_devolucao) or self.__data_devolucao
        if data_locacao is None or data_devolucao is None:
            raise ValueError("Datas insuficientes para calcular os dias utilizados.")
        return max((data_devolucao - data_locacao).days, 1)

    def calcular_dias_atraso(self, previsao_devolucao, data_devolucao=None):
        """Dias além da previsão. Nunca negativo."""
        previsao_devolucao = self.__data_valida(previsao_devolucao)
        data_devolucao = self.__data_valida(data_devolucao) or self.__data_devolucao
        if previsao_devolucao is None or data_devolucao is None:
            raise ValueError("Datas insuficientes para calcular o atraso.")
        return max((data_devolucao - previsao_devolucao).days, 0)

    def calcular_multa(self, previsao_devolucao, data_devolucao=None):
        """Multa = dias de atraso x diária x PERCENTUAL_MULTA_ATRASO."""
        if previsao_devolucao is None:
            return 0.0
        dias_atraso = self.calcular_dias_atraso(previsao_devolucao, data_devolucao)
        return round(dias_atraso * self.__valor * self.PERCENTUAL_MULTA_ATRASO, 2)

    def calcular_valor_devido(
        self, data_locacao, previsao_devolucao=None, data_devolucao=None
    ):
        """Total do item: (diárias utilizadas x valor) + multa por atraso."""
        if self.__valor is None:
            raise ValueError("O valor da diária não foi informado.")
        dias = self.calcular_dias_utilizados(data_locacao, data_devolucao)
        total = self.__valor * dias
        total += self.calcular_multa(previsao_devolucao, data_devolucao)
        return round(total, 2)

    def para_dicionario(self):
        return {
            "id": self.__id,
            "locacao_id": self.__locacao_id,
            "material_id": self.__material_id,
            "valor": self.__valor,
            "data_devolucao": self.__data_devolucao,
            "valor_pago": self.__valor_pago,
        }

    def __repr__(self):
        return (
            "ItemDaAlocacao(id={!r}, locacao_id={!r}, material_id={!r}, "
            "valor_pago={!r})".format(
                self.__id, self.__locacao_id, self.__material_id, self.__valor_pago
            )
        )
