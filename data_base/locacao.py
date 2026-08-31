"""Entidade Locacao: cabeçalho do empréstimo realizado pelo cliente."""

from datetime import date, datetime


class Locacao:

    def __init__(self, cliente_id=None, data=None, previsao_devolucao=None, id=None):
        self.__id = id
        self.__cliente_id = cliente_id
        self.__data = self.__data_valida(data)
        self.__previsao_devolucao = self.__data_valida(previsao_devolucao)

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
    def cliente_id(self):
        return self.__cliente_id

    @cliente_id.setter
    def cliente_id(self, valor):
        self.__cliente_id = valor

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, valor):
        self.__data = self.__data_valida(valor)

    @property
    def previsao_devolucao(self):
        return self.__previsao_devolucao

    @previsao_devolucao.setter
    def previsao_devolucao(self, valor):
        self.__previsao_devolucao = self.__data_valida(valor)

    # ------------------------------------------------------------------
    # Conversores auxiliares
    # ------------------------------------------------------------------
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
        if self.__cliente_id is None:
            raise ValueError("A locação precisa estar vinculada a um cliente.")
        if self.__data is None:
            raise ValueError("A data da locação é obrigatória.")
        if self.__previsao_devolucao is None:
            raise ValueError("A previsão de devolução é obrigatória.")
        if self.__previsao_devolucao < self.__data:
            raise ValueError(
                "A previsão de devolução não pode ser anterior à data da locação."
            )
        return True

    def finalizar_locacao(self, itens):
        """Encerra a locação somando o valor pago de todos os itens.

        Levanta ValueError se algum item ainda não tiver sido devolvido.
        Retorna o total efetivamente pago pelo cliente.
        """
        if not itens:
            raise ValueError("Não é possível finalizar uma locação sem itens.")
        pendentes = [item for item in itens if not item.foi_devolvido()]
        if pendentes:
            raise ValueError(
                "Existem {} item(ns) sem devolução registrada.".format(len(pendentes))
            )
        return round(sum(item.valor_pago for item in itens), 2)

    # ------------------------------------------------------------------
    # Métodos de cálculo
    # ------------------------------------------------------------------
    def calcular_dias_previstos(self):
        """Quantidade de dias previstos entre a locação e a devolução."""
        if self.__data is None or self.__previsao_devolucao is None:
            raise ValueError(
                "Data da locação e previsão de devolução são necessárias para o cálculo."
            )
        dias = (self.__previsao_devolucao - self.__data).days
        return max(dias, 1)

    def calcular_valor_previsto(self, itens):
        """Valor estimado da locação: soma das diárias dos itens x dias previstos."""
        dias = self.calcular_dias_previstos()
        return round(sum(item.valor for item in itens) * dias, 2)

    def esta_atrasada(self, data_referencia=None):
        if self.__previsao_devolucao is None:
            raise ValueError("A previsão de devolução não foi informada.")
        referencia = self.__data_valida(data_referencia) or date.today()
        return referencia > self.__previsao_devolucao

    def para_dicionario(self):
        return {
            "id": self.__id,
            "cliente_id": self.__cliente_id,
            "data": self.__data,
            "previsao_devolucao": self.__previsao_devolucao,
        }

    def __repr__(self):
        return "Locacao(id={!r}, cliente_id={!r}, data={!r})".format(
            self.__id, self.__cliente_id, self.__data
        )
