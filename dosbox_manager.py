import json
import os

# Define o caminho para o arquivo de perfis de forma centralizada
CAMINHO_PERFIS = os.path.join("config", "perfis.json")

def carregar_perfis():
    """
    Carrega os perfis de jogos do arquivo perfis.json.
    Retorna uma lista de perfis. Se o arquivo não existir, retorna uma lista vazia.
    """
    try:
        with open(CAMINHO_PERFIS, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existe ou está vazio/corrompido, retorna uma lista vazia
        return []

def salvar_perfis(perfis):
    """
    Salva a lista completa de perfis no arquivo perfis.json.
    """
    # Garante que a pasta 'config' exista
    os.makedirs(os.path.dirname(CAMINHO_PERFIS), exist_ok=True)
    with open(CAMINHO_PERFIS, 'w', encoding='utf-8') as f:
        # indent=4 deixa o arquivo JSON formatado e legível
        json.dump(perfis, f, indent=4, ensure_ascii=False)

def salvar_novo_perfil(novo_perfil):
    """
    Carrega os perfis existentes, adiciona um novo perfil e salva tudo.
    """
    perfis_existentes = carregar_perfis()
    perfis_existentes.append(novo_perfil)
    salvar_perfis(perfis_existentes)
    # utils/dosbox_manager.py (adicionar no final do arquivo)

import subprocess # Módulo para executar programas externos

# Define o caminho para o executável do DOSBox
CAMINHO_DOSBOX_EXE = os.path.join("dosbox", "DOSBox.exe")

# utils/dosbox_manager.py (substituir a função inteira)

def gerar_e_executar_jogo(perfil):
    """
    Gera um arquivo .conf para um jogo específico, usando configurações personalizadas se existirem,
    e o executa com o DOSBox.
    """
    if not os.path.exists(CAMINHO_DOSBOX_EXE):
        mensagem_erro = f"ERRO: DOSBox.exe não encontrado em '{os.path.abspath(CAMINHO_DOSBOX_EXE)}'"
        print(mensagem_erro)
        return False, mensagem_erro

    # --- Lógica de Configuração ---
    # Pega as configurações do perfil. Se não existirem, usa um dicionário vazio.
    config = perfil.get("dosbox_config", {})
    
    # Define valores padrão e os substitui pelos do perfil se existirem
    fullscreen = config.get("fullscreen", "false")
    output = config.get("output", "opengl")
    cycles = config.get("cycles", "auto")
    
    # --- Geração do .conf ---
    caminho_pasta_jogo_abs = os.path.abspath(perfil["caminho_pasta_jogo"])
    caminho_conf = os.path.join(caminho_pasta_jogo_abs, "dosbox_launcher.conf")
    
    # O conteúdo do .conf agora usa as variáveis de configuração
    conf_content = f"""
[sdl]
fullscreen = {fullscreen}
fulldouble = false
fullresolution = desktop
windowresolution = 1024x768
output = {output}

[cpu]
cycles = {cycles}

[autoexec]
@ECHO OFF
MOUNT C "{caminho_pasta_jogo_abs}"
C:
cls
{perfil['executavel_relativo']}
EXIT
"""
    
    try:
        with open(caminho_conf, 'w', encoding='utf-8') as f:
            f.write(conf_content.strip())
        
        comando = [os.path.abspath(CAMINHO_DOSBOX_EXE), "-conf", caminho_conf, "-noconsole"]
        print(f"Executando comando: {' '.join(comando)}")
        subprocess.Popen(comando)
        return True, "Jogo iniciado com sucesso."
        
    except Exception as e:
        mensagem_erro = f"Erro ao gerar .conf ou executar o DOSBox: {e}"
        print(mensagem_erro)
        return False, mensagem_erro

    # Pega o caminho absoluto da pasta do jogo para evitar problemas
    caminho_pasta_jogo_abs = os.path.abspath(perfil["caminho_pasta_jogo"])
    
    # Define o nome do arquivo de configuração dentro da própria pasta do jogo
    caminho_conf = os.path.join(caminho_pasta_jogo_abs, "dosbox_launcher.conf")
    
    # Cria o conteúdo do arquivo .conf. Este é o coração da execução.
    conf_content = f"""
[sdl]
fullscreen = false
fulldouble = false
fullresolution = desktop
windowresolution = 1024x768
output = opengl

[cpu]
cycles = auto

[autoexec]
# Os comandos abaixo serão executados automaticamente pelo DOSBox
@ECHO OFF
MOUNT C "{caminho_pasta_jogo_abs}"
C:
cls
{perfil['executavel_relativo']}
EXIT
"""
    
    try:
        # Salva o conteúdo no arquivo .conf
        with open(caminho_conf, 'w', encoding='utf-8') as f:
            # .strip() remove espaços em branco extras do início e do fim
            f.write(conf_content.strip())
        
        # Monta o comando completo para executar o DOSBox
        # O -noconsole esconde a janela de status do DOSBox
        comando = [os.path.abspath(CAMINHO_DOSBOX_EXE), "-conf", caminho_conf, "-noconsole"]
        
        print(f"Executando comando: {' '.join(comando)}")
        
        # Inicia o DOSBox com o .conf do jogo.
        # Popen não bloqueia nosso launcher, ele continua funcionando.
        subprocess.Popen(comando)
        return True, "Jogo iniciado com sucesso."
        
    except Exception as e:
        mensagem_erro = f"Erro ao gerar .conf ou executar o DOSBox: {e}"
        print(mensagem_erro)
        return False, mensagem_erro
        # utils/dosbox_manager.py (adicionar no final do arquivo)

def remover_perfil(id_jogo_para_remover):
    """
    Remove um perfil da lista de perfis baseado no seu id_jogo.
    """
    perfis_atuais = carregar_perfis()
    
    # Cria uma nova lista com todos os perfis, exceto o que queremos remover
    perfis_atualizados = [p for p in perfis_atuais if p.get('id_jogo') != id_jogo_para_remover]
    
    # Salva a nova lista de perfis no arquivo
    salvar_perfis(perfis_atualizados)
    print(f"Perfil com ID '{id_jogo_para_remover}' foi removido.")
    # utils/dosbox_manager.py (adicionar no final do arquivo)

def atualizar_perfil(id_jogo_para_atualizar, novos_dados):
    """
    Encontra um perfil pelo ID e atualiza seus dados.
    'novos_dados' é um dicionário com as chaves a serem atualizadas.
    Ex: {'nome_amigavel': 'Novo Nome'}
    """
    perfis_atuais = carregar_perfis()
    
    # Itera sobre a lista de perfis para encontrar e atualizar o perfil correto
    for i, perfil in enumerate(perfis_atuais):
        if perfil.get('id_jogo') == id_jogo_para_atualizar:
            # Atualiza o dicionário do perfil com os novos dados
            perfis_atuais[i].update(novos_dados)
            break # Interrompe o loop uma vez que o perfil foi encontrado e atualizado
    
    # Salva a lista de perfis, agora com o item atualizado
    salvar_perfis(perfis_atuais)
    print(f"Perfil com ID '{id_jogo_para_atualizar}' foi atualizado.")