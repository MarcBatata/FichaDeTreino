import json
import os
from tabulate import tabulate  # Importando tabulate para exibição formatada

# Banco de dados de exercícios por grupo muscular
exercicios = {
    "Quadríceps": ["Agachamento Livre", "Leg Press", "Afundo", "Cadeira Extensora", "Agachamento Búlgaro"],
    "Glúteos": ["Elevação Pélvica", "Glúteo na Polia", "Stiff", "Passada", "Abdução no Aparelho"],
    "Posterior De Coxa": ["Stiff", "Mesa Flexora", "Cadeira Flexora", "Levantamento Terra"],
    "Panturrilha": ["Panturrilha no Smith", "Panturrilha no Leg Press", "Panturrilha Sentado", "Saltos"],
    "Peito": ["Supino Reto", "Supino Inclinado", "Crucifixo", "Crossover", "Flexões"],
    "Costas": ["Puxador Frontal", "Remada Curvada", "Barra Fixa", "Pulldown", "Remada Unilateral"],
    "Bíceps": ["Rosca Direta", "Rosca Martelo", "Rosca Alternada", "Rosca Concentrada", "Rosca Scott"],
    "Tríceps": ["Tríceps Testa", "Tríceps Corda", "Paralelas", "Supino Fechado", "Tríceps Francês"],
    "Ombro Anterior": ["Desenvolvimento com Halteres", "Desenvolvimento no Smith", "Elevação Frontal"],
    "Ombro Lateral": ["Elevação Lateral", "Desenvolvimento Arnold", "Remada Alta"],
    "Ombro Posterior": ["Face Pull", "Crucifixo Inverso", "Remada Alta Aberta"],
    "Abdômen": ["Abdominal Infra", "Prancha", "Crunch", "Elevação de Pernas"]
}

# Treino do usuário (inicialmente vazio)
treino_usuario = {}

def aplicar_drop_set():
    escolha = input("Deseja aplicar a técnica de drop set? (s/n): ").strip().lower()
    return "10/8/6 reps (Drop Set)" if escolha == "s" else "Série Normal"

def sugerir_tempo_descanso():
    print("\nObjetivo do treino:")
    print("1. Hipertrofia (60-90 segundos de descanso)")
    print("2. Ganho de Força (2-3 minutos de descanso)")
    escolha = input("Escolha o objetivo: ")
    return "Hipertrofia (90s descanso)" if escolha == "1" else "Força (2-3min descanso)"

def adicionar_exercicio():
    dia = input("Digite o dia da semana: ").capitalize()

    while True:
        grupo = input(f"Escolha um grupo muscular {list(exercicios.keys())}: ").title()

        if grupo not in exercicios:
            print("Grupo muscular inválido.")
            continue

        print("Exercícios disponíveis:", ", ".join(exercicios[grupo]))
        ex = input("Escolha um exercício: ").title()

        if ex not in exercicios[grupo]:
            print("Exercício inválido.")
            continue

        drop_set = aplicar_drop_set()
        descanso = sugerir_tempo_descanso()

        treino_usuario.setdefault(dia, {}).setdefault(grupo, []).append(f"{ex} ({drop_set}, {descanso})")
        print(f"{ex} adicionado ao treino de {dia} com configuração: {drop_set} e objetivo: {descanso}.")

        mais_exercicios = input(f"Deseja adicionar mais exercícios de {grupo} ao treino de {dia}? (s/n): ").strip().lower()
        if mais_exercicios != "s":
            break  # Sai do loop e volta ao menu principal

def remover_exercicio():
    dia = input("Digite o dia da semana: ").capitalize()

    if dia not in treino_usuario:
        print("Não há treino nesse dia.")
        return

    print("Treino atual:", treino_usuario[dia])
    grupo = input("De qual grupo muscular deseja remover um exercício? ").title()

    if grupo not in treino_usuario[dia]:
        print("Grupo muscular não encontrado.")
        return

    print("Exercícios no treino:")
    for i, ex in enumerate(treino_usuario[dia][grupo], start=1):
        print(f"{i}. {ex}")

    escolha = input("Escolha um exercício para remover (digite o nome ou número): ").strip()

    # Permitir remoção por número
    if escolha.isdigit():
        escolha_index = int(escolha) - 1
        if 0 <= escolha_index < len(treino_usuario[dia][grupo]):
            removido = treino_usuario[dia][grupo].pop(escolha_index)
            print(f"✅ {removido} removido do treino de {dia}.")
        else:
            print("Número inválido.")
            return
    else:
        # Permitir remoção por nome do exercício
        for ex in treino_usuario[dia][grupo]:
            if escolha.lower() in ex.lower():  # Verifica se o nome está dentro da string completa
                treino_usuario[dia][grupo].remove(ex)
                print(f"✅ {ex} removido do treino de {dia}.")
                break
        else:
            print("Exercício não encontrado.")
            return

    # 🚀 **Se o grupo muscular ficar vazio, remove ele**
    if not treino_usuario[dia][grupo]:
        del treino_usuario[dia][grupo]
        print(f"⚠️ Grupo muscular '{grupo}' removido de {dia}, pois não tem mais exercícios.")

    # 🚀 **Se o dia ficar vazio, remove ele**
    if not treino_usuario[dia]:
        del treino_usuario[dia]
        print(f"⚠️ Treino de {dia} removido completamente, pois não há mais exercícios.")



def mostrar_treino():
    if not treino_usuario:
        print("Nenhum exercício adicionado ao treino.")
        return

    data = []
    for dia, grupos in treino_usuario.items():
        for grupo, exercicios_lista in grupos.items():
            exercicios_formatados = "\n".join(exercicios_lista)  # Quebra de linha para melhor visualização
            data.append([dia, grupo, exercicios_formatados])

    headers = ["Dia", "Grupo Muscular", "Exercícios"]
    tabela = tabulate(data, headers=headers, tablefmt="fancy_grid", stralign="center")

    print("\n📋 Treino da Semana:\n")
    print(tabela)

def sugerir_exercicios():
    grupo = input(f"Escolha um grupo muscular para sugestões {list(exercicios.keys())}: ").capitalize()

    if grupo in exercicios:
        print("Sugestões:", ", ".join(exercicios[grupo]))
    else:
        print("Grupo muscular inválido.")

# Função para salvar o treino em um arquivo JSON
def salvar_treino():
    # Obtenha o caminho correto para a pasta "Documentos" do usuário
    caminho = os.path.join(os.path.expanduser("~"), "Documents", "treino.json")
    
    # Verifique se a pasta Documentos existe
    if not os.path.exists(os.path.dirname(caminho)):
        print("⚠️ A pasta 'Documents' não foi encontrada.")
        return
    
    # Salve o arquivo JSON
    with open(caminho, "w") as arquivo:
        json.dump(treino_usuario, arquivo, indent=4)
    print(f"\n✅ Treino salvo com sucesso em: {caminho}")

# Função para carregar o treino salvo
def carregar_treino():
    global treino_usuario
    # Caminho para o arquivo treino.json na pasta Documentos
    caminho = os.path.join(os.path.expanduser("~"), "Documents", "treino.json")
    
    try:
        with open(caminho, "r") as arquivo:
            treino_usuario = json.load(arquivo)
        print("\n📂 Treino carregado com sucesso!")
    except FileNotFoundError:
        print("\n⚠️ Nenhum treino salvo encontrado.")

def mostrar_menu():
    print("\n1. Adicionar exercício ao treino")
    print("2. Remover exercício do treino")
    print("3. Mostrar treino")
    print("4. Sugerir exercícios")
    print("5. Salvar treino")
    print("6. Carregar treino")
    print("7. Sair")

# Loop do menu
while True:
    mostrar_menu()
    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        adicionar_exercicio()
    elif escolha == "2":
        remover_exercicio()
    elif escolha == "3":
        mostrar_treino()
    elif escolha == "4":
        sugerir_exercicios()
    elif escolha == "5":
        salvar_treino()
    elif escolha == "6":
        carregar_treino()
    elif escolha == "7":
        print("Saindo...")
        break
    else:
        print("Opção inválida. Tente novamente.")

