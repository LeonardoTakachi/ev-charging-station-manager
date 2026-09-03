# EV Charging Station Manager

Sistema em **Python** para gerenciamento de múltiplas sessões de recarga de veículos elétricos, desenvolvido como projeto acadêmico para aplicar **programação orientada a objetos, estruturas de dados, algoritmos, análise de complexidade, testes automatizados e regras de negócio** em um cenário próximo de um sistema real.

## Visão geral

A aplicação simula uma estação de recarga capaz de cadastrar veículos, distribuir potência entre sessões ativas, acompanhar SOC e energia consumida, calcular custos, pesquisar e ordenar registros e gerar relatórios operacionais.

O projeto também inclui uma simulação educacional de mensagens inspiradas no **OCPP 2.0.1**.

## Principais funcionalidades

- Cadastro de múltiplas sessões de recarga
- ID de sessão manual ou gerado automaticamente
- Validação de dados e prevenção de IDs duplicados
- Busca de sessão por ID
- Ordenação por ID, energia, custo ou tempo
- Atualização simulada do SOC e da energia consumida
- Smart Charging com balanceamento de potência
- Tarifação dinâmica por horário
- Encerramento de sessões
- Estatísticas e relatório consolidado
- Simulação de eventos OCPP
- Testes automatizados com `unittest`

## Conceitos aplicados

- Programação Orientada a Objetos
- Classes e objetos
- Listas e estruturas de dados
- Validação de entradas
- Algoritmos de busca e ordenação
- Análise de complexidade Big-O
- Testes unitários
- Regras de negócio
- Organização e documentação de projeto

## Smart Charging

A estação possui capacidade máxima simulada de **50 kW**.

Cada veículo pode receber até **22 kW**. Quando a demanda total ultrapassa o limite da estação, a potência disponível é dividida entre as sessões ativas.

Exemplo:

```text
3 veículos ativos
Demanda teórica: 66 kW
Limite da estação: 50 kW

Potência aproximada por veículo:
50 / 3 = 16,67 kW
```

## Algoritmos

### Busca Sequencial

A busca percorre a lista de sessões até localizar o ID solicitado.

- Melhor caso: `O(1)`
- Pior caso: `O(n)`

### Bubble Sort

O projeto implementa manualmente Bubble Sort para ordenar as sessões por:

1. ID da sessão
2. Energia consumida
3. Custo atual
4. Tempo de recarga

- Melhor caso com encerramento antecipado: `O(n)`
- Pior caso: `O(n²)`

A explicação completa está em [`docs/algoritmos.md`](docs/algoritmos.md).

## Simulação OCPP

O sistema gera mensagens simuladas inspiradas no OCPP 2.0.1 para representar eventos como:

- `AuthorizeRequest`
- `TransactionEventStarted`
- `MeterValuesRequest`
- `TransactionEventEnded`

> Esta é uma simulação educacional e não uma implementação completa do protocolo OCPP.

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
git clone https://github.com/LeonardoTakachi/ev-charging-station-manager.git
cd ev-charging-station-manager
```

### 2. Execute o programa

Requer Python 3 e não utiliza bibliotecas externas.

```bash
python main.py
```

No Windows, dependendo da instalação:

```bash
py main.py
```

## Menu principal

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

## Testes automatizados

Os testes utilizam `unittest`, da biblioteca padrão do Python.

```bash
python -m unittest discover -s tests -v
```

A suíte cobre cenários como:

- cadastro válido;
- rejeição de capacidade inválida;
- prevenção de ID duplicado;
- busca sequencial;
- Bubble Sort por ID;
- limite total do Smart Charging;
- encerramento de sessão.

## Exemplo de fluxo

1. Cadastre duas ou mais sessões.
2. Avance alguns ciclos da simulação.
3. Observe SOC, energia, custo e potência alocada.
4. Busque uma sessão pelo ID.
5. Ordene as sessões por um dos critérios disponíveis.
6. Consulte as estatísticas.
7. Encerre uma sessão.
8. Gere o relatório consolidado.

## Possíveis evoluções

- Persistência das sessões em banco de dados
- API REST com FastAPI
- Interface web
- Autenticação de usuários
- Histórico persistente de sessões
- Integração com carregadores reais
- CI para execução automática dos testes
- Ampliação da cobertura de testes

## Contexto

Projeto acadêmico desenvolvido para aplicar fundamentos de Ciência da Computação e desenvolvimento em Python em um problema relacionado a infraestrutura de recarga de veículos elétricos.

A proposta combina algoritmos e estruturas de dados com regras de negócio de um domínio real, mantendo o escopo educacional do projeto.

---

Desenvolvido por **Leonardo Takachi** com foco em Python, algoritmos, estruturas de dados e boas práticas de desenvolvimento.
