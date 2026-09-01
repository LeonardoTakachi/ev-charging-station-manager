"""
EV Charging Station Manager

Sistema em Python para gerenciamento de sessões de recarga de veículos elétricos.
Inclui Smart Charging, simulação de mensagens OCPP, Busca Sequencial, Bubble Sort,
estatísticas e relatório de sessões.
"""

import datetime
import json
import random

# Configuração do sistema
POTENCIA_MAXIMA_ESTACAO = 50.0  # Limite de potência em kW
PRECO_BASE_KWH = 1.50


class SessaoRecarga:
    def __init__(self, id_sessao, id_veiculo, capacidade_bateria):
        self.id_sessao = id_sessao
        self.id_veiculo = id_veiculo
        self.capacidade_bateria = capacidade_bateria
        self.soc_atual = random.randint(10, 40)
        self.potencia_alocada = 0.0
        self.energia_consumida = 0.0
        self.inicio = datetime.datetime.now()
        self.fim = None
        self.custo_final = None
        self.status = "Carregando"

    def calcular_tarifa_atual(self):
        hora_atual = datetime.datetime.now().hour

        if 18 <= hora_atual <= 21:
            fator_horario = 1.4
        elif 0 <= hora_atual <= 6:
            fator_horario = 0.8
        else:
            fator_horario = 1.0

        return PRECO_BASE_KWH * fator_horario

    def calcular_custo_atual(self):
        if self.custo_final is not None:
            return self.custo_final
        return self.energia_consumida * self.calcular_tarifa_atual()

    def calcular_tempo_recarga(self):
        momento_final = self.fim if self.fim is not None else datetime.datetime.now()
        return (momento_final - self.inicio).total_seconds()

    def atualizar_progresso(self):
        if self.status != "Carregando":
            return

        energia_injetada = self.potencia_alocada * (1 / 60)
        self.energia_consumida += energia_injetada

        incremento_soc = (energia_injetada / self.capacidade_bateria) * 100
        self.soc_atual = min(100.0, self.soc_atual + incremento_soc)

        if self.soc_atual >= 100.0:
            self.status = "Concluído"
            self.potencia_alocada = 0.0
            self.fim = datetime.datetime.now()
            self.custo_final = (
                self.energia_consumida * self.calcular_tarifa_atual()
            )


class GerenciadorRecarga:
    def __init__(self):
        self.sessoes = []
        self.contador_sessoes = 1

    # ------------------------------------------------------------------
    # OCPP
    # ------------------------------------------------------------------
    def simular_envio_ocpp(self, tipo_mensagem, dados):
        mensagem_ocpp = {
            "ocpp_version": "2.0.1",
            "message_id": random.randint(100000, 999999),
            "timestamp": datetime.datetime.now().isoformat(),
            "action": tipo_mensagem,
            "payload": dados
        }

        print(f"\n[OCPP >> TRANSMISSÃO]: {json.dumps(mensagem_ocpp, indent=2)}")
        print(
            f"[OCPP << CONFIRMAÇÃO]: Mensagem "
            f"{mensagem_ocpp['message_id']} processada com sucesso pelo backend."
        )

    # ------------------------------------------------------------------
    # BUSCA SEQUENCIAL
    # ------------------------------------------------------------------
    def busca_sequencial(self, id_sessao):
        # Complexidade no pior caso: O(n)
        for sessao in self.sessoes:
            if sessao.id_sessao == id_sessao:
                return sessao
        return None

    # ------------------------------------------------------------------
    # VALIDAÇÕES E IDENTIFICAÇÃO
    # ------------------------------------------------------------------
    def _id_veiculo_valido(self, id_veiculo):
        return isinstance(id_veiculo, str) and id_veiculo.strip() != ""

    def _capacidade_valida(self, capacidade_bateria):
        try:
            valor = float(capacidade_bateria)
        except (TypeError, ValueError):
            return False

        return valor > 0

    def _id_sessao_ja_existe(self, id_sessao):
        return self.busca_sequencial(id_sessao) is not None

    def _gerar_id_automatico(self):
        while True:
            id_sessao = f"SES-{self.contador_sessoes:03d}"
            self.contador_sessoes += 1

            if not self._id_sessao_ja_existe(id_sessao):
                return id_sessao

    # ------------------------------------------------------------------
    # CADASTRO
    # ------------------------------------------------------------------
    def cadastrar_sessao(self, id_veiculo, capacidade_bateria, id_sessao=""):
        if not self._id_veiculo_valido(id_veiculo):
            print("\n[ERRO] Placa/ID do veículo inválido.")
            return False

        if not self._capacidade_valida(capacidade_bateria):
            print(
                "\n[ERRO] Capacidade da bateria inválida. "
                "Informe um número maior que zero."
            )
            return False

        if not isinstance(id_sessao, str):
            print("\n[ERRO] ID da sessão inválido.")
            return False

        id_sessao = id_sessao.strip().upper()

        # Se o usuário deixar em branco, o sistema gera SES-XXX.
        if id_sessao == "":
            id_sessao = self._gerar_id_automatico()
        elif self._id_sessao_ja_existe(id_sessao):
            print(f"\n[ERRO] ID de sessão {id_sessao} já existe.")
            return False

        nova_sessao = SessaoRecarga(
            id_sessao,
            id_veiculo.strip().upper(),
            float(capacidade_bateria)
        )

        self.sessoes.append(nova_sessao)

        print(
            f"\n[SISTEMA] Veículo {nova_sessao.id_veiculo} conectado "
            f"com sucesso na sessão {id_sessao}!"
        )

        self.simular_envio_ocpp(
            "AuthorizeRequest",
            {"idToken": nova_sessao.id_veiculo}
        )

        self.simular_envio_ocpp(
            "TransactionEventStarted",
            {
                "transactionId": id_sessao,
                "soc": nova_sessao.soc_atual
            }
        )

        self.balancear_potencia()
        return True

    # ------------------------------------------------------------------
    # SMART CHARGING
    # ------------------------------------------------------------------
    def balancear_potencia(self):
        sessoes_ativas = [
            sessao
            for sessao in self.sessoes
            if sessao.status == "Carregando"
        ]

        num_ativas = len(sessoes_ativas)

        if num_ativas == 0:
            return

        print(
            f"\n[SMART CHARGING] Balanceando carga para "
            f"{num_ativas} veículo(s) ativo(s)..."
        )
        print(
            f"Capacidade Total da Estação: "
            f"{POTENCIA_MAXIMA_ESTACAO} kW"
        )

        potencia_nominal_por_veiculo = 22.0
        demanda_total_teorica = (
            num_ativas * potencia_nominal_por_veiculo
        )

        if demanda_total_teorica <= POTENCIA_MAXIMA_ESTACAO:
            for sessao in sessoes_ativas:
                sessao.potencia_alocada = potencia_nominal_por_veiculo
        else:
            potencia_reduzida = POTENCIA_MAXIMA_ESTACAO / num_ativas

            for sessao in sessoes_ativas:
                sessao.potencia_alocada = potencia_reduzida

            print(
                f">>> ALERTA: Limite da estação atingido! "
                f"Potência limitada a {potencia_reduzida:.2f} kW por veículo."
            )

    # ------------------------------------------------------------------
    # ATUALIZAÇÃO DA SIMULAÇÃO
    # ------------------------------------------------------------------
    def atualizar_sistema(self):
        if not self.sessoes:
            print("\n[ERRO] Nenhuma sessão cadastrada.")
            return

        encontrou_ativa = False

        for sessao in self.sessoes:
            if sessao.status == "Carregando":
                encontrou_ativa = True
                sessao.atualizar_progresso()

                self.simular_envio_ocpp(
                    "MeterValuesRequest",
                    {
                        "transactionId": sessao.id_sessao,
                        "soc": round(sessao.soc_atual, 1),
                        "energyDelivered": round(sessao.energia_consumida, 2),
                        "powerAllocated": round(sessao.potencia_alocada, 2)
                    }
                )

        if not encontrou_ativa:
            print("\n[SISTEMA] Não há sessões ativas para atualizar.")

        self.balancear_potencia()

    # ------------------------------------------------------------------
    # ENCERRAMENTO
    # ------------------------------------------------------------------
    def encerrar_sessao(self, id_sessao):
        id_sessao = (
            id_sessao.strip().upper()
            if isinstance(id_sessao, str)
            else ""
        )

        if id_sessao == "":
            print("\n[ERRO] Informe um ID de sessão para encerrar.")
            return False

        sessao = self.busca_sequencial(id_sessao)

        if sessao is None:
            print("\n[ERRO] Sessão não encontrada.")
            return False

        if sessao.status != "Carregando":
            print(
                f"\n[SISTEMA] A sessão {id_sessao} já está "
                f"com status '{sessao.status}'."
            )
            return False

        sessao.status = "Encerrada pelo Usuário"
        sessao.potencia_alocada = 0.0
        sessao.fim = datetime.datetime.now()
        sessao.custo_final = (
            sessao.energia_consumida * sessao.calcular_tarifa_atual()
        )

        print(f"\n[SISTEMA] Sessão {id_sessao} finalizada.")

        self.simular_envio_ocpp(
            "TransactionEventEnded",
            {
                "transactionId": id_sessao,
                "totalEnergy": round(sessao.energia_consumida, 2),
                "totalCost": round(sessao.calcular_custo_atual(), 2)
            }
        )

        self.balancear_potencia()
        return True

    # ------------------------------------------------------------------
    # EXIBIÇÃO DE UMA SESSÃO
    # ------------------------------------------------------------------
    def exibir_dados_sessao(self, sessao, indice=None):
        tempo_minutos = sessao.calcular_tempo_recarga() / 60

        if indice is not None:
            print(f"\n[{indice}] ID: {sessao.id_sessao}")
        else:
            print(f"ID:                 {sessao.id_sessao}")

        prefixo = "    " if indice is not None else ""

        print(f"{prefixo}Veículo:            {sessao.id_veiculo}")
        print(f"{prefixo}Status:             {sessao.status}")
        print(f"{prefixo}SOC atual:          {sessao.soc_atual:.1f}%")
        print(f"{prefixo}Potência alocada:   {sessao.potencia_alocada:.1f} kW")
        print(f"{prefixo}Energia consumida:  {sessao.energia_consumida:.2f} kWh")
        print(f"{prefixo}Custo atual:        R$ {sessao.calcular_custo_atual():.2f}")
        print(f"{prefixo}Tempo de recarga:   {tempo_minutos:.2f} min")
        print(f"{prefixo}Capacidade bateria: {sessao.capacidade_bateria:.2f} kWh")
        print(
            f"{prefixo}Início:             "
            f"{sessao.inicio.strftime('%d/%m/%Y %H:%M:%S')}"
        )

    # ------------------------------------------------------------------
    # LISTAGEM
    # ------------------------------------------------------------------
    def listar_sessoes(self):
        print("\n" + "=" * 70)
        print("                    LISTAGEM DE SESSÕES")
        print("=" * 70)

        if not self.sessoes:
            print("Nenhuma sessão registrada.")
            print("=" * 70)
            return

        for indice, sessao in enumerate(self.sessoes, start=1):
            self.exibir_dados_sessao(sessao, indice)

        print("\n" + "=" * 70)
        print(f"Total de sessões cadastradas: {len(self.sessoes)}")
        print("=" * 70)

    # ------------------------------------------------------------------
    # BUSCA - INTERAÇÃO COM O USUÁRIO
    # ------------------------------------------------------------------
    def buscar_sessao(self, id_sessao):
        id_sessao = (
            id_sessao.strip().upper()
            if isinstance(id_sessao, str)
            else ""
        )

        if id_sessao == "":
            print("\n[ERRO] Informe um ID de sessão para buscar.")
            return None

        sessao = self.busca_sequencial(id_sessao)

        print("\n" + "=" * 70)
        print("                         RESULTADO DA BUSCA")
        print("=" * 70)

        if sessao is None:
            print("Sessão não encontrada.")
            print("=" * 70)
            return None

        self.exibir_dados_sessao(sessao)
        print("=" * 70)
        return sessao

    # ------------------------------------------------------------------
    # BUBBLE SORT
    # ------------------------------------------------------------------
    def _valor_ordenacao(self, sessao, criterio):
        if criterio == "1":
            return sessao.id_sessao
        if criterio == "2":
            return sessao.energia_consumida
        if criterio == "3":
            return sessao.calcular_custo_atual()
        if criterio == "4":
            return sessao.calcular_tempo_recarga()

        return None

    def bubble_sort(self, criterio):
        # Complexidade no pior caso: O(n²)
        n = len(self.sessoes)

        for i in range(n - 1):
            houve_troca = False

            for j in range(n - 1 - i):
                valor_atual = self._valor_ordenacao(
                    self.sessoes[j], criterio
                )
                valor_proximo = self._valor_ordenacao(
                    self.sessoes[j + 1], criterio
                )

                if valor_atual > valor_proximo:
                    self.sessoes[j], self.sessoes[j + 1] = (
                        self.sessoes[j + 1],
                        self.sessoes[j]
                    )
                    houve_troca = True

            if not houve_troca:
                break

    def ordenar_sessoes(self, criterio):
        if len(self.sessoes) == 0:
            print("\n[ERRO] Nenhuma sessão cadastrada para ordenar.")
            return False

        if len(self.sessoes) == 1:
            print(
                "\n[SISTEMA] Existe apenas uma sessão. "
                "Não é necessário ordenar."
            )
            self.listar_sessoes()
            return True

        criterios = {
            "1": "ID da sessão",
            "2": "energia consumida",
            "3": "custo atual",
            "4": "tempo de recarga"
        }

        if criterio not in criterios:
            print("\n[ERRO] Critério de ordenação inválido.")
            return False

        self.bubble_sort(criterio)

        print(
            f"\n[SISTEMA] Sessões ordenadas por "
            f"{criterios[criterio]} usando Bubble Sort."
        )

        self.listar_sessoes()
        return True

    # ------------------------------------------------------------------
    # ESTATÍSTICAS
    # ------------------------------------------------------------------
    def mostrar_estatisticas(self):
        print("\n" + "=" * 70)
        print("                    ESTATÍSTICAS DAS SESSÕES")
        print("=" * 70)

        if not self.sessoes:
            print("Nenhuma sessão registrada para calcular estatísticas.")
            print("=" * 70)
            return

        total_sessoes = len(self.sessoes)
        energia_total = 0.0
        receita_total = 0.0

        sessao_maior_consumo = self.sessoes[0]
        sessao_menor_consumo = self.sessoes[0]

        # Complexidade: O(n)
        for sessao in self.sessoes:
            energia_total += sessao.energia_consumida
            receita_total += sessao.calcular_custo_atual()

            if (
                sessao.energia_consumida
                > sessao_maior_consumo.energia_consumida
            ):
                sessao_maior_consumo = sessao

            if (
                sessao.energia_consumida
                < sessao_menor_consumo.energia_consumida
            ):
                sessao_menor_consumo = sessao

        custo_medio = receita_total / total_sessoes

        print(f"Total de sessões:       {total_sessoes}")
        print(f"Energia total:          {energia_total:.2f} kWh")
        print(f"Receita total:          R$ {receita_total:.2f}")
        print(f"Custo médio por sessão: R$ {custo_medio:.2f}")
        print(
            f"Maior consumo:          "
            f"{sessao_maior_consumo.id_sessao} - "
            f"{sessao_maior_consumo.energia_consumida:.2f} kWh"
        )
        print(
            f"Menor consumo:          "
            f"{sessao_menor_consumo.id_sessao} - "
            f"{sessao_menor_consumo.energia_consumida:.2f} kWh"
        )
        print("=" * 70)

    # ------------------------------------------------------------------
    # RELATÓRIO GERAL
    # ------------------------------------------------------------------
    def gerar_relatorio(self):
        print("\n" + "=" * 78)
        print("               RELATÓRIO GERAL DE GERENCIAMENTO DE RECARGA")
        print("=" * 78)

        if not self.sessoes:
            print("Nenhuma sessão registrada até o momento.")
            print("=" * 78)
            return

        print(
            f"{'ID':<12}"
            f"{'Veículo':<14}"
            f"{'Status':<24}"
            f"{'Energia (kWh)':<16}"
            f"{'Custo (R$)':<14}"
            f"{'Tempo (min)':<12}"
        )
        print("-" * 78)

        energia_total = 0.0
        receita_total = 0.0

        for sessao in self.sessoes:
            custo = sessao.calcular_custo_atual()
            tempo_minutos = sessao.calcular_tempo_recarga() / 60

            energia_total += sessao.energia_consumida
            receita_total += custo

            print(
                f"{sessao.id_sessao:<12}"
                f"{sessao.id_veiculo:<14}"
                f"{sessao.status:<24}"
                f"{sessao.energia_consumida:<16.2f}"
                f"{custo:<14.2f}"
                f"{tempo_minutos:<12.2f}"
            )

        print("-" * 78)
        print(f"Total de sessões: {len(self.sessoes)}")
        print(f"Energia total consumida: {energia_total:.2f} kWh")
        print(f"Receita total estimada: R$ {receita_total:.2f}")
        print("=" * 78)


def menu():
    gerenciador = GerenciadorRecarga()

    while True:
        print("\n" + "=" * 60)
        print("        SISTEMA DE GERENCIAMENTO DE ESTAÇÃO DE RECARGA")
        print("=" * 60)
        print("1. Nova Sessão de Recarga")
        print("2. Listar Sessões")
        print("3. Buscar Sessão")
        print("4. Ordenar Sessões")
        print("5. Estatísticas")
        print("6. Avançar Tempo / Simular Progresso")
        print("7. Encerrar uma Sessão")
        print("8. Gerar Relatório")
        print("9. Sair")
        print("=" * 60)

        opcao = input("Escolha uma opção (1-9): ").strip()

        if opcao == "1":
            print("\n--- NOVA SESSÃO ---")
            id_sessao = input(
                "ID da sessão (Enter para gerar automaticamente): "
            )
            placa = input("Digite a placa/ID do veículo: ")
            bateria = input(
                "Capacidade da bateria em kWh (ex: 50): "
            )

            gerenciador.cadastrar_sessao(
                placa,
                bateria,
                id_sessao
            )

        elif opcao == "2":
            gerenciador.listar_sessoes()

        elif opcao == "3":
            id_busca = input(
                "Digite o ID da sessão a buscar (ex: SES-001): "
            )
            gerenciador.buscar_sessao(id_busca)

        elif opcao == "4":
            print("\nORDENAR SESSÕES POR:")
            print("1. ID da sessão")
            print("2. Energia consumida")
            print("3. Custo atual")
            print("4. Tempo de recarga")

            criterio = input(
                "Escolha o critério (1-4): "
            ).strip()

            gerenciador.ordenar_sessoes(criterio)

        elif opcao == "5":
            gerenciador.mostrar_estatisticas()

        elif opcao == "6":
            print(
                "\n[SIMULAÇÃO] Passando o tempo "
                "(1 ciclo de carga)..."
            )
            gerenciador.atualizar_sistema()

        elif opcao == "7":
            id_sessao = input(
                "Digite o ID da sessão para encerrar: "
            )
            gerenciador.encerrar_sessao(id_sessao)

        elif opcao == "8":
            gerenciador.gerar_relatorio()

        elif opcao == "9":
            print(
                "\nEncerrando o Sistema de Gerenciamento. Até logo!"
            )
            break

        else:
            print("\n[ERRO] Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()
