# Algoritmos e complexidade

Este documento resume os algoritmos implementados no projeto e a relação entre o tamanho da entrada e o custo computacional.

## Estrutura de dados

As sessões são armazenadas em uma lista:

```python
self.sessoes = []
```

Cada item é uma instância de `SessaoRecarga`.

A lista é adequada para este projeto porque permite:

- adicionar novas sessões com `append()`;
- percorrer todos os registros;
- aplicar busca sequencial;
- aplicar ordenação manual;
- calcular estatísticas.

## Busca Sequencial

A Busca Sequencial percorre a lista elemento por elemento:

```python
def busca_sequencial(self, id_sessao):
    for sessao in self.sessoes:
        if sessao.id_sessao == id_sessao:
            return sessao
    return None
```

### Melhor caso — O(1)

Ocorre quando a sessão procurada está na primeira posição.

Apenas uma comparação é necessária.

### Pior caso — O(n)

Ocorre quando:

- a sessão está na última posição; ou
- a sessão não existe.

Nesse cenário, todos os `n` elementos podem ser verificados.

Se o número de sessões aproximadamente dobrar, o número máximo de comparações também pode aproximadamente dobrar.

## Bubble Sort

O Bubble Sort compara elementos vizinhos e troca suas posições quando necessário.

```python
for i in range(n - 1):
    for j in range(n - 1 - i):
        if valor_atual > valor_proximo:
            self.sessoes[j], self.sessoes[j + 1] = (
                self.sessoes[j + 1], self.sessoes[j]
            )
```

O projeto utiliza um único Bubble Sort e altera apenas o critério de comparação.

Critérios disponíveis:

- ID da sessão;
- energia consumida;
- custo atual;
- tempo de recarga.

### Pior caso — O(n²)

Existem dois laços aninhados.

A quantidade de comparações no pior caso é aproximadamente:

```text
n(n - 1) / 2
```

Na análise assintótica, constantes e termos menores são desconsiderados, resultando em:

```text
O(n²)
```

Isso significa que, se a quantidade de dados crescer 10 vezes, a quantidade de operações pode crescer aproximadamente 100 vezes no pior caso.

## Otimização aplicada

O Bubble Sort utiliza uma variável que identifica se houve troca durante uma passagem:

```python
houve_troca = False
```

Se nenhuma troca for realizada, a lista já está ordenada e o algoritmo pode ser encerrado antecipadamente.

Essa otimização melhora alguns casos, embora a complexidade no pior caso continue sendo `O(n²)`.

## Comparação

| Algoritmo | Uso no projeto | Melhor caso | Pior caso |
|---|---|---:|---:|
| Busca Sequencial | Localizar sessão por ID | O(1) | O(n) |
| Bubble Sort | Ordenar sessões | O(n) com encerramento antecipado | O(n²) |

Para volumes pequenos, ambos cumprem bem o objetivo educacional do projeto. Para sistemas reais com grandes volumes de dados, outras estruturas e algoritmos seriam mais adequados.
