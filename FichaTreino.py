import json
import os
import sys
from datetime import datetime
from tabulate import tabulate
from colorama import init, Fore, Style, Back

# Inicializar colorama para funcionar em todos os sistemas operacionais
init(autoreset=True)

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

# Constantes
DIAS_SEMANA = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
ARQUIVO_TREINO = os.path.join(os.path.expanduser("~"), "Documents", "treino.json")
PASTA_BACKUP = os.path.join(os.path.expanduser("~"), "Documents", "Backups_Treino")

# Funções de utilidade
def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    """Pausa para o usuário ler a mensagem"""
    input(f"\n{Fore.CYAN}Pressione ENTER para continuar...{Style.RESET_ALL}")

def imprimir_titulo(titulo):
    """Imprime um título formatado"""
    largura = 60
    print(f"\n{Fore.BLACK}{Back.CYAN}{titulo.center(largura)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'-' * largura}{Style.RESET_ALL}")

def imprimir_sucesso(mensagem):
    """Imprime uma mensagem de sucesso"""
    print(f"{Fore.GREEN}✅ {mensagem}{Style.RESET_ALL}")

def imprimir_erro(mensagem):
    """Imprime uma mensagem de erro"""
    print(f"{Fore.RED}❌ {mensagem}{Style.RESET_ALL}")

def imprimir_aviso(mensagem):
    """Imprime uma mensagem de aviso"""
    print(f"{Fore.YELLOW}⚠️  {mensagem}{Style.RESET_ALL}")

def obter_escolha_menu(opcoes, prompt="Escolha uma opção: "):
    """Obtém a escolha do usuário com validação"""
    while True:
        try:
            escolha = input(f"{Fore.CYAN}{prompt}{Style.RESET_ALL}")
            if escolha.isdigit() and 0 <= int(escolha) <= len(opcoes):
                return int(escolha)
            imprimir_erro(f"Digite um número entre 0 e {len(opcoes)}")
        except ValueError:
            imprimir_erro("Digite um número válido")

def selecionar_da_lista(itens, titulo="Selecione uma opção:"):
    """Apresenta uma lista de itens para seleção"""
    imprimir_titulo(titulo)
    for i, item in enumerate(itens, 1):
        print(f"{Fore.YELLOW}{i}.{Style.RESET_ALL} {item}")
    
    return obter_escolha_menu(itens)

def confirmar_acao(mensagem="Tem certeza?"):
    """Solicita confirmação do usuário"""
    resposta = input(f"{Fore.YELLOW}{mensagem} (s/n): {Style.RESET_ALL}").strip().lower()
    return resposta in ["s", "sim", "y", "yes"]

# Funções de manipulação de treino
def aplicar_drop_set():
    """Define se o exercício terá drop set"""
    limpar_tela()
    imprimir_titulo("Configuração de Séries")
    
    opcoes = [
        "Série Normal (3x10-12 reps)",
        "Drop Set (10/8/6 reps)",
        "Pirâmide (8/10/12 reps)",
        "Bi-set (com próximo exercício)"
    ]
    
    for i, opcao in enumerate(opcoes, 1):
        print(f"{Fore.YELLOW}{i}.{Style.RESET_ALL} {opcao}")
    
    escolha = obter_escolha_menu(opcoes)
    return opcoes[escolha-1]

def sugerir_tempo_descanso():
    """Define o tempo de descanso baseado no objetivo"""
    limpar_tela()
    imprimir_titulo("Objetivo do Treino")
    
    opcoes = [
        "Hipertrofia (60-90 segundos)",
        "Força (2-3 minutos)",
        "Resistência (30-45 segundos)",
        "Definição (45-60 segundos)"
    ]
    
    for i, opcao in enumerate(opcoes, 1):
        print(f"{Fore.YELLOW}{i}.{Style.RESET_ALL} {opcao}")
    
    escolha = obter_escolha_menu(opcoes)
    return opcoes[escolha-1]

def selecionar_dia():
    """Permite selecionar um dia da semana"""
    limpar_tela()
    imprimir_titulo("Selecione o Dia da Semana")
    
    for i, dia in enumerate(DIAS_SEMANA, 1):
        print(f"{Fore.YELLOW}{i}.{Style.RESET_ALL} {dia}")
    
    escolha = obter_escolha_menu(DIAS_SEMANA)
    return DIAS_SEMANA[escolha-1]

def selecionar_grupo_muscular():
    """Permite selecionar um grupo muscular"""
    limpar_tela()
    imprimir_titulo("Selecione o Grupo Muscular")
    
    grupos = list(exercicios.keys())
    for i, grupo in enumerate(grupos, 1):
        print(f"{Fore.YELLOW}{i}.{Style.RESET_ALL} {grupo}")
    
    escolha = obter_escolha_menu(grupos)
    return grupos[escolha-1]

def selecionar_exercicio(grupo):
    """Permite selecionar um exercício do grupo muscular"""
    limpar_tela()
    imprimir_titulo(f"Exercícios para {grupo}")
    
    for i, ex in enumerate(exercicios[grupo], 1):
        print(f"{Fore.YELLOW}{i}.{Style.RESET_ALL} {ex}")
    
    # Opção adicional para inserir exercício personalizado
    print(f"{Fore.YELLOW}{len(exercicios[grupo])+1}.{Style.RESET_ALL} Adicionar exercício personalizado")
    
    escolha = obter_escolha_menu(exercicios[grupo] + ["Personalizado"])
    
    if escolha == len(exercicios[grupo])+1:
        # Exercício personalizado
        novo_exercicio = input(f"\n{Fore.CYAN}Digite o nome do exercício personalizado: {Style.RESET_ALL}").strip().title()
        return novo_exercicio
    else:
        return exercicios[grupo][escolha-1]

def adicionar_exercicio():
    """Adiciona um exercício ao treino"""
    limpar_tela()
    imprimir_titulo("Adicionar Exercício ao Treino")
    
    # Selecionar dia
    dia = selecionar_dia()
    
    # Selecionar grupo muscular
    grupo = selecionar_grupo_muscular()
    
    # Selecionar exercício
    exercicio = selecionar_exercicio(grupo)
    
    # Configurar séries
    serie_config = aplicar_drop_set()
    
    # Definir objetivo/descanso
    descanso = sugerir_tempo_descanso()
    
    # Configurar número de séries e repetições
    series = input(f"\n{Fore.CYAN}Número de séries (padrão: 3): {Style.RESET_ALL}").strip()
    series = series if series else "3"
    
    reps = input(f"{Fore.CYAN}Número de repetições (padrão: 12): {Style.RESET_ALL}").strip()
    reps = reps if reps else "12"
    
    # Construir detalhes do exercício
    detalhes = f"{exercicio} ({series}x{reps}, {serie_config}, {descanso})"
    
    # Adicionar ao treino
    treino_usuario.setdefault(dia, {}).setdefault(grupo, []).append(detalhes)
    
    imprimir_sucesso(f"{exercicio} adicionado ao treino de {dia}!")
    
    # Verificar se deseja adicionar outro exercício
    if confirmar_acao("Deseja adicionar mais um exercício para este dia?"):
        adicionar_exercicio()

def remover_exercicio():
    """Remove um exercício do treino"""
    limpar_tela()
    imprimir_titulo("Remover Exercício do Treino")
    
    if not treino_usuario:
        imprimir_aviso("Nenhum exercício adicionado ao treino.")
        pausar()
        return
    
    # Selecionar dia
    dias_com_treino = list(treino_usuario.keys())
    if not dias_com_treino:
        imprimir_aviso("Nenhum dia com treino configurado.")
        pausar()
        return
    
    print("Dias com treino configurado:")
    dia_escolhido = dias_com_treino[selecionar_da_lista(dias_com_treino, "Selecione o dia") - 1]
    
    # Selecionar grupo muscular
    grupos_no_dia = list(treino_usuario[dia_escolhido].keys())
    if not grupos_no_dia:
        imprimir_aviso(f"Nenhum grupo muscular configurado para {dia_escolhido}.")
        pausar()
        return
    
    print(f"\nGrupos musculares em {dia_escolhido}:")
    grupo_escolhido = grupos_no_dia[selecionar_da_lista(grupos_no_dia, "Selecione o grupo muscular") - 1]
    
    # Selecionar exercício
    exercicios_no_grupo = treino_usuario[dia_escolhido][grupo_escolhido]
    if not exercicios_no_grupo:
        imprimir_aviso(f"Nenhum exercício configurado para {grupo_escolhido} em {dia_escolhido}.")
        pausar()
        return
    
    print(f"\nExercícios de {grupo_escolhido} em {dia_escolhido}:")
    ex_idx = selecionar_da_lista(exercicios_no_grupo, "Selecione o exercício para remover") - 1
    exercicio_removido = exercicios_no_grupo[ex_idx]
    
    # Confirmar remoção
    if confirmar_acao(f"Tem certeza que deseja remover: {exercicio_removido}?"):
        # Remover exercício
        treino_usuario[dia_escolhido][grupo_escolhido].pop(ex_idx)
        imprimir_sucesso(f"{exercicio_removido} removido com sucesso!")
        
        # Limpar grupos vazios
        if not treino_usuario[dia_escolhido][grupo_escolhido]:
            del treino_usuario[dia_escolhido][grupo_escolhido]
            imprimir_aviso(f"Grupo muscular '{grupo_escolhido}' removido de {dia_escolhido}, pois não tem mais exercícios.")
        
        # Limpar dias vazios
        if not treino_usuario[dia_escolhido]:
            del treino_usuario[dia_escolhido]
            imprimir_aviso(f"Treino de {dia_escolhido} removido completamente, pois não há mais exercícios.")
    else:
        imprimir_aviso("Operação cancelada.")
    
    pausar()

def editar_exercicio():
    """Edita um exercício existente"""
    limpar_tela()
    imprimir_titulo("Editar Exercício")
    
    if not treino_usuario:
        imprimir_aviso("Nenhum exercício adicionado ao treino.")
        pausar()
        return
    
    # Selecionar dia
    dias_com_treino = list(treino_usuario.keys())
    if not dias_com_treino:
        imprimir_aviso("Nenhum dia com treino configurado.")
        pausar()
        return
    
    print("Dias com treino configurado:")
    dia_escolhido = dias_com_treino[selecionar_da_lista(dias_com_treino, "Selecione o dia") - 1]
    
    # Selecionar grupo muscular
    grupos_no_dia = list(treino_usuario[dia_escolhido].keys())
    if not grupos_no_dia:
        imprimir_aviso(f"Nenhum grupo muscular configurado para {dia_escolhido}.")
        pausar()
        return
    
    print(f"\nGrupos musculares em {dia_escolhido}:")
    grupo_escolhido = grupos_no_dia[selecionar_da_lista(grupos_no_dia, "Selecione o grupo muscular") - 1]
    
    # Selecionar exercício
    exercicios_no_grupo = treino_usuario[dia_escolhido][grupo_escolhido]
    if not exercicios_no_grupo:
        imprimir_aviso(f"Nenhum exercício configurado para {grupo_escolhido} em {dia_escolhido}.")
        pausar()
        return
    
    print(f"\nExercícios de {grupo_escolhido} em {dia_escolhido}:")
    ex_idx = selecionar_da_lista(exercicios_no_grupo, "Selecione o exercício para editar") - 1
    exercicio_atual = exercicios_no_grupo[ex_idx]
    
    # Menu de edição
    limpar_tela()
    imprimir_titulo(f"Editando: {exercicio_atual}")
    print(f"{Fore.YELLOW}1.{Style.RESET_ALL} Substituir por outro exercício")
    print(f"{Fore.YELLOW}2.{Style.RESET_ALL} Editar configuração (séries, reps, etc)")
    print(f"{Fore.YELLOW}3.{Style.RESET_ALL} Voltar")
    
    escolha = obter_escolha_menu([1, 2, 3])
    
    if escolha == 1:
        # Substituir exercício
        novo_exercicio = selecionar_exercicio(grupo_escolhido)
        # Manter as configurações atuais (extrair entre parênteses)
        config = exercicio_atual.split("(")[1].split(")", 1)[0] if "(" in exercicio_atual else ""
        novo_ex_completo = f"{novo_exercicio} ({config})" if config else novo_exercicio
        treino_usuario[dia_escolhido][grupo_escolhido][ex_idx] = novo_ex_completo
        imprimir_sucesso(f"Exercício substituído por {novo_exercicio}!")
    
    elif escolha == 2:
        # Editar configuração
        nome_exercicio = exercicio_atual.split(" (")[0] if " (" in exercicio_atual else exercicio_atual
        
        # Novas configurações
        serie_config = aplicar_drop_set()
        descanso = sugerir_tempo_descanso()
        
        # Configurar número de séries e repetições
        series = input(f"\n{Fore.CYAN}Número de séries: {Style.RESET_ALL}").strip()
        reps = input(f"{Fore.CYAN}Número de repetições: {Style.RESET_ALL}").strip()
        
        # Atualizar exercício
        detalhes = f"{nome_exercicio} ({series}x{reps}, {serie_config}, {descanso})"
        treino_usuario[dia_escolhido][grupo_escolhido][ex_idx] = detalhes
        imprimir_sucesso("Configuração atualizada com sucesso!")
    
    pausar()

def mostrar_treino(dia_especifico=None):
    """Mostra o treino completo ou de um dia específico"""
    limpar_tela()
    
    if not treino_usuario:
        imprimir_aviso("Nenhum exercício adicionado ao treino.")
        pausar()
        return
    
    # Se um dia específico foi solicitado
    if dia_especifico:
        if dia_especifico not in treino_usuario:
            imprimir_aviso(f"Não há treino configurado para {dia_especifico}.")
            pausar()
            return
        
        dias_para_mostrar = [dia_especifico]
        imprimir_titulo(f"Treino de {dia_especifico}")
    else:
        dias_para_mostrar = sorted(treino_usuario.keys(), 
                                  key=lambda x: DIAS_SEMANA.index(x) if x in DIAS_SEMANA else 999)
        imprimir_titulo("Treino da Semana")
    
    data = []
    for dia in dias_para_mostrar:
        grupos = treino_usuario[dia]
        for grupo, exercicios_lista in grupos.items():
            exercicios_formatados = "\n".join([f"• {ex}" for ex in exercicios_lista])
            data.append([dia, grupo, exercicios_formatados])
    
    headers = [f"{Fore.CYAN}Dia{Style.RESET_ALL}", 
               f"{Fore.CYAN}Grupo Muscular{Style.RESET_ALL}", 
               f"{Fore.CYAN}Exercícios{Style.RESET_ALL}"]
    
    tabela = tabulate(data, headers=headers, tablefmt="fancy_grid", stralign="left")
    print(tabela)
    
    pausar()

def visualizar_treino_por_dia():
    """Visualiza o treino de um dia específico"""
    limpar_tela()
    imprimir_titulo("Visualizar Treino por Dia")
    
    if not treino_usuario:
        imprimir_aviso("Nenhum exercício adicionado ao treino.")
        pausar()
        return
    
    # Dias disponíveis + opção para todos
    dias_disponiveis = sorted(treino_usuario.keys(), 
                             key=lambda x: DIAS_SEMANA.index(x) if x in DIAS_SEMANA else 999)
    
    if not dias_disponiveis:
        imprimir_aviso("Nenhum treino configurado.")
        pausar()
        return
    
    dias_disponiveis.append("Todos os dias")
    
    print("Selecione o dia para visualizar:")
    escolha = selecionar_da_lista(dias_disponiveis) - 1
    
    if escolha == len(dias_disponiveis) - 1:
        # Mostrar todos os dias
        mostrar_treino()
    else:
        # Mostrar dia específico
        mostrar_treino(dias_disponiveis[escolha])

def sugerir_exercicios():
    """Sugere exercícios para um grupo muscular"""
    limpar_tela()
    imprimir_titulo("Sugestões de Exercícios")
    
    # Selecionar grupo muscular
    grupo = selecionar_grupo_muscular()
    
    imprimir_titulo(f"Sugestões para {grupo}")
    for i, ex in enumerate(exercicios[grupo], 1):
        print(f"{Fore.YELLOW}{i}.{Style.RESET_ALL} {ex}")
    
    pausar()

def criar_pasta_backups():
    """Cria a pasta de backups se não existir"""
    if not os.path.exists(PASTA_BACKUP):
        try:
            os.makedirs(PASTA_BACKUP)
            return True
        except Exception as e:
            imprimir_erro(f"Erro ao criar pasta de backups: {e}")
            return False
    return True

def fazer_backup_automatico():
    """Faz um backup automático do treino atual"""
    if not criar_pasta_backups():
        return False
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo_backup = os.path.join(PASTA_BACKUP, f"treino_backup_{timestamp}.json")
    
    try:
        with open(arquivo_backup, "w") as arquivo:
            json.dump(treino_usuario, arquivo, indent=4)
        return True
    except Exception as e:
        imprimir_erro(f"Erro ao fazer backup: {e}")
        return False

def salvar_treino():
    """Salva o treino em um arquivo JSON"""
    limpar_tela()
    imprimir_titulo("Salvar Treino")
    
    # Verificar se há algo para salvar
    if not treino_usuario:
        imprimir_aviso("Nenhum exercício adicionado ao treino para salvar.")
        pausar()
        return
    
    # Fazer backup automático antes de salvar
    fazer_backup_automatico()
    
    # Salvar arquivo principal
    try:
        # Garantir que a pasta existe
        os.makedirs(os.path.dirname(ARQUIVO_TREINO), exist_ok=True)
        
        with open(ARQUIVO_TREINO, "w") as arquivo:
            json.dump(treino_usuario, arquivo, indent=4)
        
        imprimir_sucesso(f"Treino salvo com sucesso em: {ARQUIVO_TREINO}")
    except Exception as e:
        imprimir_erro(f"Erro ao salvar: {e}")
    
    pausar()

def carregar_treino():
    """Carrega o treino de um arquivo JSON"""
    global treino_usuario
    limpar_tela()
    imprimir_titulo("Carregar Treino")
    
    opcoes = ["Carregar treino principal", "Carregar de um backup", "Cancelar"]
    
    for i, opcao in enumerate(opcoes, 1):
        print(f"{Fore.YELLOW}{i}.{Style.RESET_ALL} {opcao}")
    
    escolha = obter_escolha_menu(opcoes)
    
    if escolha == 1:
        # Carregar arquivo principal
        try:
            with open(ARQUIVO_TREINO, "r") as arquivo:
                treino_usuario = json.load(arquivo)
            imprimir_sucesso("Treino carregado com sucesso!")
        except FileNotFoundError:
            imprimir_aviso("Nenhum treino salvo encontrado.")
        except Exception as e:
            imprimir_erro(f"Erro ao carregar: {e}")
    
    elif escolha == 2:
        # Carregar de um backup
        if not os.path.exists(PASTA_BACKUP):
            imprimir_aviso("Nenhum backup encontrado.")
            pausar()
            return
        
        # Listar arquivos de backup
        backups = [f for f in os.listdir(PASTA_BACKUP) if f.endswith('.json')]
        
        if not backups:
            imprimir_aviso("Nenhum arquivo de backup encontrado.")
            pausar()
            return
        
        print("\nBackups disponíveis:")
        backups.sort(reverse=True)  # Mais recentes primeiro
        
        # Mostrar os backups formatados
        for i, backup in enumerate(backups, 1):
            # Extrair timestamp do nome do arquivo
            timestamp = backup.replace("treino_backup_", "").replace(".json", "")
            data_formatada = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%d/%m/%Y %H:%M:%S")
            print(f"{Fore.YELLOW}{i}.{Style.RESET_ALL} {data_formatada}")
        
        escolha_backup = obter_escolha_menu(backups)
        arquivo_backup = os.path.join(PASTA_BACKUP, backups[escolha_backup-1])
        
        try:
            with open(arquivo_backup, "r") as arquivo:
                treino_usuario = json.load(arquivo)
            imprimir_sucesso("Backup carregado com sucesso!")
        except Exception as e:
            imprimir_erro(f"Erro ao carregar backup: {e}")
    
    pausar()

def exportar_treino():
    """Exporta o treino para outros formatos"""
    limpar_tela()
    imprimir_titulo("Exportar Treino")
    
    if not treino_usuario:
        imprimir_aviso("Nenhum exercício adicionado ao treino para exportar.")
        pausar()
        return
    
    opcoes = ["Exportar para TXT", "Exportar para CSV", "Voltar"] # ANOTAÇÃO: ARRUMAR EXPORTAÇÃO EM FORMATO CSV
    
    print("Selecione o formato de exportação:")
    for i, opcao in enumerate(opcoes, 1):
        print(f"{Fore.YELLOW}{i}.{Style.RESET_ALL} {opcao}")
    
    escolha = obter_escolha_menu(opcoes)
    
    if escolha == 3:  # Voltar
        return
    
    # Definir caminho para salvar
    pasta_documentos = os.path.expanduser("~/Documents")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        if escolha == 1:  # TXT
            arquivo_exportacao = os.path.join(pasta_documentos, f"treino_export_{timestamp}.txt")
            
            with open(arquivo_exportacao, "w", encoding="utf-8") as arquivo:
                arquivo.write("=== FICHA DE TREINO ===\n\n")
                
                # Ordenar dias da semana
                dias_ordenados = sorted(treino_usuario.keys(), 
                                      key=lambda x: DIAS_SEMANA.index(x) if x in DIAS_SEMANA else 999)
                
                for dia in dias_ordenados:
                    arquivo.write(f"--- {dia} ---\n")
                    
                    for grupo, exercicios_lista in treino_usuario[dia].items():
                        arquivo.write(f"\n* {grupo}:\n")
                        
                        for ex in exercicios_lista:
                            arquivo.write(f"  - {ex}\n")
                    
                    arquivo.write("\n")
            
            imprimir_sucesso(f"Treino exportado com sucesso para TXT: {arquivo_exportacao}")
        
        elif escolha == 2:  # CSV
            arquivo_exportacao = os.path.join(pasta_documentos, f"treino_export_{timestamp}.csv")
            
            with open(arquivo_exportacao, "w", encoding="utf-8") as arquivo:
                arquivo.write("Dia,Grupo Muscular,Exercício,Detalhes\n")
                
                # Ordenar dias da semana
                dias_ordenados = sorted(treino_usuario.keys(), 
                                      key=lambda x: DIAS_SEMANA.index(x) if x in DIAS_SEMANA else 999)
                
                for dia in dias_ordenados:
                    for grupo, exercicios_lista in treino_usuario[dia].items():
                        for ex in exercicios_lista:
                            # Dividir o exercício em nome e detalhes
                            if " (" in ex:
                                nome_ex = ex.split(" (")[0]
                                detalhes = "(" + ex.split(" (")[1]
                            else:
                                nome_ex = ex
                                detalhes = ""
                            
                            linha = f'"{dia}","{grupo}","{nome_ex}","{detalhes}"\n'
                            arquivo.write(linha)
            
            imprimir_sucesso(f"Treino exportado com sucesso para CSV: {arquivo_exportacao}")
    
    except Exception as e:
        imprimir_erro(f"Erro durante a exportação: {e}")
    
    pausar()

def limpar_treino():
    """Limpa o treino atual"""
    global treino_usuario
    limpar_tela()
    imprimir_titulo("Limpar Treino")
    
    if not treino_usuario:
        imprimir_aviso("Nenhum exercício adicionado ao treino para limpar.")
        pausar()
        return
    
    # Confirmar a operação
    if confirmar_acao("Tem certeza que deseja LIMPAR TODO o treino? Esta ação não pode ser desfeita!"):
        # Fazer backup antes de limpar
        if fazer_backup_automatico():
            imprimir_sucesso("Um backup do treino atual foi criado antes da limpeza.")
        
        # Limpar treino
        treino_usuario = {}
        imprimir_sucesso("Treino completamente limpo!")
    else:
        imprimir_aviso("Operação cancelada.")
    
    pausar()

def menu_principal():
    """Exibe o menu principal"""
    while True:
        limpar_tela()
        imprimir_titulo("GERENCIADOR DE TREINO")
        
        print(f"{Fore.YELLOW}1.{Style.RESET_ALL} Adicionar Exercício")
        print(f"{Fore.YELLOW}2.{Style.RESET_ALL} Remover Exercício")
        print(f"{Fore.YELLOW}3.{Style.RESET_ALL} Editar Exercício")
        print(f"{Fore.YELLOW}4.{Style.RESET_ALL} Visualizar Treino")
        print(f"{Fore.YELLOW}5.{Style.RESET_ALL} Sugestões de Exercícios")
        print(f"{Fore.YELLOW}6.{Style.RESET_ALL} Salvar Treino")
        print(f"{Fore.YELLOW}7.{Style.RESET_ALL} Carregar Treino")
        print(f"{Fore.YELLOW}8.{Style.RESET_ALL} Exportar Treino")
        print(f"{Fore.YELLOW}9.{Style.RESET_ALL} Limpar Treino")
        print(f"{Fore.YELLOW}0.{Style.RESET_ALL} Sair")
        
        opcoes = list(range(10))  # 0-9
        escolha = obter_escolha_menu(opcoes, "Digite sua escolha: ")
        
        if escolha == 1:
            adicionar_exercicio()
        elif escolha == 2:
            remover_exercicio()
        elif escolha == 3:
            editar_exercicio()
        elif escolha == 4:
            visualizar_treino_por_dia()
        elif escolha == 5:
            sugerir_exercicios()
        elif escolha == 6:
            salvar_treino()
        elif escolha == 7:
            carregar_treino()
        elif escolha == 8:
            exportar_treino()
        elif escolha == 9:
            limpar_treino()
        elif escolha == 0:
            if confirmar_acao("Tem certeza que deseja sair?"):
                # Perguntar se deseja salvar antes de sair se houver alterações
                if treino_usuario:
                    if confirmar_acao("Deseja salvar o treino antes de sair?"):
                        salvar_treino()
                
                limpar_tela()
                imprimir_titulo("Até a próxima!")
                print(f"{Fore.GREEN}Obrigado por usar o Gerenciador de Treino!{Style.RESET_ALL}")
                sys.exit(0)

def inicializar():
    """Inicializa o aplicativo"""
    limpar_tela()
    imprimir_titulo("GERENCIADOR DE TREINO")
    print(f"{Fore.GREEN}Bem-vindo ao Gerenciador de Treino!{Style.RESET_ALL}")
    
    # Tentar carregar treino existente
    try:
        global treino_usuario
        if os.path.exists(ARQUIVO_TREINO):
            if confirmar_acao("Treino anterior encontrado. Deseja carregá-lo?"):
                with open(ARQUIVO_TREINO, "r") as arquivo:
                    treino_usuario = json.load(arquivo)
                imprimir_sucesso("Treino carregado com sucesso!")
    except Exception as e:
        imprimir_erro(f"Erro ao carregar treino anterior: {e}")
    
    pausar()
    menu_principal()

# Iniciar o programa
if __name__ == "__main__":
    try:
        inicializar()
    except KeyboardInterrupt:
        limpar_tela()
        print(f"\n{Fore.YELLOW}Programa encerrado pelo usuário.{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        limpar_tela()
        print(f"\n{Fore.RED}Erro inesperado: {e}{Style.RESET_ALL}")
        sys.exit(1)

