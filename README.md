# EV Charging Station Manager

Sistema em Python para gerenciamento de múltiplas sessões de recarga de veículos elétricos.

O projeto simula uma estação de recarga capaz de cadastrar e acompanhar sessões, distribuir a potência disponível entre veículos, calcular custos, pesquisar e ordenar registros e gerar estatísticas. Também aplica algoritmos implementados manualmente, permitindo analisar sua complexidade com Big-O.

## Funcionalidades

- Cadastro de múltiplas sessões de recarga
- ID de sessão manual ou gerado automaticamente
- Validação de entradas e prevenção de IDs duplicados
- Listagem detalhada das sessões
- Busca de sessão por ID
- Ordenação por ID, energia, custo ou tempo
- Atualização simulada do SOC e da energia consumida
- Balanceamento de potência entre veículos ativos
- Simulação de mensagens OCPP 2.0.1
- Tarifação dinâmica por horário
- Encerramento de sessões
- Estatísticas gerais
- Relatório consolidado

## Conceitos aplicados

O projeto foi desenvolvido para praticar fundamentos importantes de Ciência da Computação e desenvolvimento em Python:

- Programação orientada a objetos
- Classes e objetos
- Listas
- Funções e métodos
- Validação de dados
- Estruturas condicionais e laços
- Algoritmos de busca
- Algoritmos de ordenação
- Análise de complexidade Big-O
- Testes automatizados

## Algoritmos

### Busca Sequencial

A busca percorre a lista de sessões do início ao fim até encontrar o ID solicitado.

```python
def busca_sequencial(self, id_sessao):
    for sessao in self.sessoes:
        if sessao.id_sessao == id_sessao:
            return sessao
    return None
```

**Complexidade no pior caso: `O(n)`**

Se a sessão estiver no final da lista ou não existir, todos os elementos podem precisar ser verificados.

### Bubble Sort

A ordenação é implementada manualmente, sem utilizar `list.sort()` ou `sorted()` como substitutos do algoritmo.

```python
for i in range(n - 1):
    for j in range(n - 1 - i):
        if valor_atual > valor_proximo:
            self.sessoes[j], self.sessoes[j + 1] = (
                self.sessoes[j + 1],
                self.sessoes[j]
            )
```

**Complexidade no pior caso: `O(n²)`**

O sistema permite ordenar as sessões por:

1. ID da sessão
2. Energia consumida
3. Custo atual
4. Tempo de recarga

Mais detalhes estão em [`docs/algoritmos.md`](docs/algoritmos.md).

## Smart Charging

A estação possui uma capacidade máxima simulada de **50 kW**.

Cada veículo pode receber até **22 kW**. Quando a demanda total ultrapassa a capacidade da estação, a potência disponível é dividida igualmente entre as sessões ativas.

Exemplo:

```text
3 veículos ativos
Demanda teórica: 66 kW
Limite da estação: 50 kW

Potência por veículo:
50 / 3 = 16,67 kW
```

## Simulação OCPP

O projeto gera mensagens simuladas inspiradas no protocolo OCPP 2.0.1, incluindo eventos como:

- `AuthorizeRequest`
- `TransactionEventStarted`
- `MeterValuesRequest`
- `TransactionEventEnded`

O objetivo é representar de forma simplificada a comunicação entre uma estação de recarga e um backend.

> Observação: esta é uma simulação educacional e não uma implementação completa do protocolo OCPP.

## Estrutura do projeto

```text
ev-charging-station-manager/
├── main.py
├── README.md
├── .gitignore
├── docs/
│   └── algoritmos.md
└── tests/
    └── test_core.py
```

## Como executar

### 1. Clone o repositório

```bash
git clone <URL-DO-SEU-REPOSITORIO>
cd ev-charging-station-manager
```

### 2. Execute o programa

Requer Python 3.

```bash
python main.py
```

No Windows também pode ser necessário usar:

```bash
py main.py
```

Nenhuma biblioteca externa é necessária.

## Menu

```text
1. Nova Sessão de Recarga
2. Listar Sessões
3. Buscar Sessão
4. Ordenar Sessões
5. Estatísticas
6. Avançar Tempo / Simular Progresso
7. Encerrar uma Sessão
8. Gerar Relatório
9. Sair
```

## Executando os testes

Os testes utilizam apenas `unittest`, da biblioteca padrão do Python.

```bash
python -m unittest discover -s tests -v
```

Eles verificam pontos como:

- cadastro válido;
- rejeição de entradas inválidas;
- ID duplicado;
- Busca Sequencial;
- Bubble Sort;
- busca depois da ordenação;
- encerramento de sessão.

## Exemplo de fluxo

1. Cadastre duas ou mais sessões.
2. Avance alguns ciclos da simulação.
3. Liste as sessões e observe SOC, energia, custo e potência.
4. Busque uma sessão pelo ID.
5. Ordene as sessões por energia ou custo.
6. Consulte as estatísticas.
7. Encerre uma sessão.
8. Gere o relatório consolidado.

## Contexto

Projeto acadêmico desenvolvido para aplicar estruturas de dados e algoritmos em um problema relacionado a gerenciamento de recarga de veículos elétricos.

A proposta combina conceitos algorítmicos com uma simulação de domínio real, preservando funcionalidades como Smart Charging e comunicação OCPP simulada.

## Possíveis evoluções

- Persistência das sessões em banco de dados
- API REST com FastAPI
- Interface web
- Autenticação de usuários
- Integração com carregadores reais
- Persistência e consulta de histórico
- Testes unitários mais abrangentes

---

Desenvolvido em **Python** com foco em estruturas de dados, algoritmos e organização de software.
