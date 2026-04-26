import os

def listar_executaveis(caminho_pasta):
    """
    Lista todos os arquivos com extensão .exe, .bat, ou .com em uma pasta.
    A busca não diferencia maiúsculas de minúsculas.
    Retorna uma lista com os nomes dos arquivos.
    """
    executaveis = []
    extensoes_validas = ['.exe', '.bat', '.com']
    
    try:
        for arquivo in os.listdir(caminho_pasta):
            # Pega a extensão e a converte para minúsculas para comparação
            extensao = os.path.splitext(arquivo)[1].lower()
            if extensao in extensoes_validas:
                executaveis.append(arquivo)
    except FileNotFoundError:
        print(f"Erro: A pasta {caminho_pasta} não foi encontrada.")
        return []
        
    return executaveis