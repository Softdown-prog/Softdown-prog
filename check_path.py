import sys
import os

print("--- Informações de Diagnóstico do Python ---")

print("\n[1] Versão do Python:")
print(sys.version)

print("\n[2] Local do Executável do Python:")
print(sys.executable)

print("\n[3] Diretório de Trabalho Atual (onde o comando foi rodado):")
print(os.getcwd())

print("\n[4] Caminhos de Busca de Módulos (sys.path):")
for numero, caminho in enumerate(sys.path):
    print(f"  - {caminho}")

print("\n--- Fim do Diagnóstico ---")