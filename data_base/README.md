# Sistema de Alocação de Materiais

Modelagem de domínio + camada de persistência SQLite. Os testes unitários ficam
na pasta `testes/` (a implementar).

## Estrutura

```
sistema_alocacao_materiais/
├── sistema_alocacao/
│   ├── database.py              # conexão, schema, conversores de data
│   ├── modelos/                 # entidades com atributos privados
│   │   ├── tipo_material.py
│   │   ├── material.py
│   │   ├── cliente.py
│   │   ├── locacao.py
│   │   └── item_da_alocacao.py
│   └── dao/                     # CRUD de cada unidade persistente
│       ├── base_dao.py
│       ├── tipo_material_dao.py
│       ├── material_dao.py
│       ├── cliente_dao.py
│       ├── locacao_dao.py
│       └── item_da_alocacao_dao.py
├── testes/                      # seus módulos unittest
├── exemplo_uso.py
└── README.md
```

Sem dependências externas — só a biblioteca padrão do Python 3.

## Como rodar

```bash
python exemplo_uso.py                       # demonstração ponta a ponta
python -m unittest discover -s testes -t .  # seus testes
```

## O gancho para o `setUp()` / `tearDown()`

`Database` recebe o caminho do banco por parâmetro e os DAOs recebem o
`Database` por injeção. É esse ponto que permite trocar o arquivo real por um
banco `:memory:` novo a cada teste:

```python
import unittest
from sistema_alocacao import Database, MaterialDAO

class TestMaterialDAO(unittest.TestCase):

    def setUp(self):
        self.db = Database(":memory:")   # já cria as tabelas
        self.dao = MaterialDAO(self.db)
        # ... insira aqui as massas de dados de que o teste precisa

    def tearDown(self):
        self.db.apagar_tabelas()
        self.db.fechar()
```

Cada `Database(":memory:")` é um banco independente que morre junto com a
conexão, então nenhum teste enxerga o estado do outro. Se preferir preservar o
schema entre testes, use `self.db.limpar_dados()` no lugar de
`apagar_tabelas()` (ele também zera o `AUTOINCREMENT`).

## Convenções da API

**Modelos** — todos os atributos são privados (`__nome`, name mangling) e
expostos por `@property` / `@setter`. Todos têm `validar()`, que levanta
`ValueError` com mensagem específica no primeiro campo obrigatório inválido, e
`para_dicionario()`, útil para `assertEqual` em cima de dicionários.

**DAOs** — assinatura uniforme:

| Método | Retorno |
| --- | --- |
| `inserir(objeto)` | id gerado (também atribuído a `objeto.id`); chama `validar()` antes |
| `buscar_por_id(id)` | objeto ou `None` |
| `listar_todos()` | lista (vazia se não houver registros) |
| `atualizar(objeto)` | `True` se alguma linha mudou |
| `remover(id)` | `True` se alguma linha foi removida |
| `contar()` | inteiro |

`PRAGMA foreign_keys` está ligado, então inserir com FK inexistente levanta
`sqlite3.IntegrityError` — dá um bom teste negativo.

## Regras de negócio implementadas

**Material** — `status` só aceita `Disponível` ou `Alocado`; `condicao` só
aceita `Novo`, `Bom`, `Ruim` ou `Inutilizado` (validado no objeto **e** por
`CHECK` no schema). `atualizar_status()` / `atualizar_condicao()` levantam
`ValueError` em valor fora do domínio. `esta_disponivel()` exige status
`Disponível` **e** condição diferente de `Inutilizado`.

**Cliente** — `validar()` exige nome, endereço e telefone, e o telefone precisa
ter pelo menos 10 dígitos após remover a máscara.

**Locacao** — `previsao_devolucao` não pode ser anterior a `data`.
`finalizar_locacao(itens)` levanta `ValueError` se algum item ainda estiver sem
devolução; caso contrário devolve o total pago.

**ItensDaAlocacao** — `valor` é a diária do material congelada no momento da
locação. `data_devolucao` e `valor_pago` nascem `NULL` e só são preenchidos por
`registrar_devolucao()`. Chamar duas vezes levanta `ValueError`.

### Métodos de cálculo (os que os testes precisam cobrir)

| Classe | Método | Regra |
| --- | --- | --- |
| `Material` | `calcular_valor_alocacao(dias)` | diária × dias; `dias <= 0` levanta `ValueError` |
| `Material` | `calcular_dias_para_retorno()` | `ceil(valor_compra / diária)` |
| `Locacao` | `calcular_dias_previstos()` | `previsao - data`, mínimo 1 |
| `Locacao` | `calcular_valor_previsto(itens)` | soma das diárias × dias previstos |
| `ItemDaAlocacao` | `calcular_dias_utilizados(...)` | `devolucao - locacao`, mínimo 1 (devolver no mesmo dia custa 1 diária) |
| `ItemDaAlocacao` | `calcular_dias_atraso(...)` | `devolucao - previsao`, nunca negativo |
| `ItemDaAlocacao` | `calcular_multa(...)` | dias de atraso × diária × 20% (`PERCENTUAL_MULTA_ATRASO`) |
| `ItemDaAlocacao` | `calcular_valor_devido(...)` | diárias utilizadas + multa |

Todos os retornos monetários vêm com `round(..., 2)`.

Exemplo fechado para conferir na mão: diária R$ 45, locação em 31/08,
previsão 05/09, devolução em 07/09 → 7 diárias = R$ 315, atraso de 2 dias =
R$ 18 de multa, total **R$ 333,00**.

## Observação sobre o schema

`itens_da_alocacao` ganhou um `id` próprio (além de `locacao_id` e
`material_id`), porque o enunciado pede teste de *Read* por ID. Há também um
`UNIQUE (locacao_id, material_id)` impedindo o mesmo material duas vezes na
mesma locação, e `ON DELETE CASCADE` na FK de `locacao`.
