"""Entidade TipoMaterial: agrupamento lógico dos materiais."""


class TipoMaterial:

    def __init__(self, nome=None, id=None):
        self.__id = id
        self.__nome = self.__normalizar(nome)

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
        self.__nome = self.__normalizar(valor)

    # ------------------------------------------------------------------
    # Regras de negócio
    # ------------------------------------------------------------------
    @staticmethod
    def __normalizar(valor):
        if valor is None:
            return None
        return str(valor).strip()

    def validar(self):
        """Levanta ValueError se algum campo obrigatório estiver ausente."""
        if not self.__nome:
            raise ValueError("O nome do tipo de material é obrigatório.")
        return True

    def para_dicionario(self):
        return {"id": self.__id, "nome": self.__nome}

    def __repr__(self):
        return "TipoMaterial(id={!r}, nome={!r})".format(self.__id, self.__nome)
