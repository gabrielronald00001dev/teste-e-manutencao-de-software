"""Entidade Cliente: exige validação dos campos obrigatórios antes da inserção."""

import re


class Cliente:

    TAMANHO_MINIMO_TELEFONE = 10  # DDD + número

    def __init__(self, nome=None, endereco=None, telefone=None, id=None):
        self.__id = id
        self.__nome = self.__texto(nome)
        self.__endereco = self.__texto(endereco)
        self.__telefone = self.__texto(telefone)

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
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        self.__nome = self.__texto(valor)

    @property
    def endereco(self):
        return self.__endereco

    @endereco.setter
    def endereco(self, valor):
        self.__endereco = self.__texto(valor)

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, valor):
        self.__telefone = self.__texto(valor)

    # ------------------------------------------------------------------
    # Regras de negócio
    # ------------------------------------------------------------------
    @staticmethod
    def __texto(valor):
        if valor is None:
            return None
        return str(valor).strip()

    def somente_digitos_telefone(self):
        """Telefone sem máscara: (24) 99999-1234 -> 24999991234."""
        if not self.__telefone:
            return ""
        return re.sub(r"\D", "", self.__telefone)

    def validar(self):
        """Levanta ValueError no primeiro campo obrigatório inválido."""
        if not self.__nome:
            raise ValueError("O nome do cliente é obrigatório.")
        if not self.__endereco:
            raise ValueError("O endereço do cliente é obrigatório.")
        if not self.__telefone:
            raise ValueError("O telefone do cliente é obrigatório.")
        if len(self.somente_digitos_telefone()) < self.TAMANHO_MINIMO_TELEFONE:
            raise ValueError(
                "O telefone deve conter ao menos {} dígitos (DDD + número).".format(
                    self.TAMANHO_MINIMO_TELEFONE
                )
            )
        return True

    def para_dicionario(self):
        return {
            "id": self.__id,
            "nome": self.__nome,
            "endereco": self.__endereco,
            "telefone": self.__telefone,
        }

    def __repr__(self):
        return "Cliente(id={!r}, nome={!r})".format(self.__id, self.__nome)
