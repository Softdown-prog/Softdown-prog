# Launcher DOSBox Pro
*por softload & softdown*

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg) ![License](https://img.shields.io/badge/License-GPLv2-lightgrey.svg) ![Platform](https://img.shields.io/badge/Platform-Windows-informational.svg)

Um launcher de desktop moderno e poderoso para gerenciar e jogar seus jogos clássicos de DOS no Windows. Este projeto foi criado para simplificar a experiência de reviver os grandes clássicos, eliminando a necessidade de linhas de comando e oferecendo uma interface gráfica rica e intuitiva.


---

## 🚀 Funcionalidades Principais

* **Interface Gráfica Moderna:** Desenvolvido com CustomTkinter para uma experiência de usuário agradável, com suporte a temas claro e escuro.
* **Biblioteca de Jogos Organizada:** Seus jogos são listados automaticamente em ordem alfabética.
* **Importação Flexível:**
    * **Importar Pasta:** Adicione jogos a partir de pastas existentes no seu computador.
    * **Importar .ZIP:** Selecione um arquivo `.zip` e o launcher descompactará e importará o jogo automaticamente.
* **Gerenciamento Completo:**
    * **Editar:** Altere o nome amigável e o arquivo executável de qualquer jogo.
    * **Remover:** Apague o perfil de um jogo e, opcionalmente, os arquivos da pasta para liberar espaço.
* **Configuração por Jogo:** Ajuste fino das configurações do DOSBox (tela cheia, ciclos de CPU, saída de vídeo) para cada jogo individualmente, garantindo a melhor performance.
* **Pré-visualização Visual:** Associe uma imagem de capa a cada jogo e visualize-a diretamente na interface.
* **DOSBox Embutido:** O DOSBox já vem incluído. Não é necessária nenhuma instalação ou configuração adicional por parte do usuário final.

---

## 🛠️ Como Começar

Existem duas maneiras de usar este programa: como um usuário final (recomendado) ou como um desenvolvedor.

### Para Usuários Finais (Instalação via Executável)
1.  Vá para a seção de **"Releases"** deste repositório no GitHub.
2.  Baixe a versão mais recente do `DOSBox.Launcher.zip` (ou similar).
3.  Descompacte o arquivo em qualquer pasta do seu computador.
4.  Execute o arquivo `DOSBox Launcher.exe` que está dentro da pasta. Pronto!



### Para Desenvolvedores (Executando a partir do Código-Fonte)
1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Softdown-prog/Softdown-prog.git](https://github.com/Softdown-prog/Softdown-prog.git)
    cd Softdown-prog
    ```
2.  **Crie um ambiente virtual:**
    ```bash
    python -m venv venv
    ```
3.  **Ative o ambiente virtual:**
    ```bash
    .\venv\Scripts\activate
    ```
4.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Execute o launcher:**
    ```bash
    python src/main.py
    ```

---

## 📖 Como Usar o Launcher
* **Importar:** Use os botões **"📂 Importar Pasta"** ou **"📦 Importar .ZIP"** para adicionar seus jogos. Siga as janelas de diálogo para selecionar o executável (`.exe`, `.bat` ou `.com`), definir um nome e escolher uma imagem de capa.
* **Selecionar:** Clique em qualquer jogo na lista da esquerda para selecioná-lo. As informações e a imagem aparecerão à direita, e os botões de ação serão ativados.
* **Jogar:** Com um jogo selecionado, clique em **"▶️ Jogar"**.
* **Configurar:** Clique em **"🎛️ Configurar DOSBox"** para abrir a janela de configurações avançadas para o jogo selecionado.
* **Editar/Remover:** Use os botões **"🔁 Editar"** e **"🗑️ Remover"** para gerenciar os jogos da sua biblioteca.

---

## ⚖️ Informações de Licença
Este projeto é distribuído sob os termos da licença **GNU General Public License v2.0 (GPLv2)**.

Isso se deve ao fato de que o launcher inclui o software **DOSBox**, que é licenciado sob a GPLv2. De acordo com os termos desta licença, qualquer trabalho derivado que distribua o DOSBox deve também ser licenciado sob a GPLv2, o que inclui a obrigação de disponibilizar o código-fonte completo.

Os jogos que podem ser executados por este launcher **não** fazem parte do projeto e são de propriedade de seus respectivos detentores de direitos autorais.

---

*Documentação endossada e software desenvolvido por:*

### **softload & softdown**
*2025*
