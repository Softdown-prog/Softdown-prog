import tkinter
from tkinter import filedialog, simpledialog, messagebox
import shutil
import json
import customtkinter as ctk
import os
import zipfile
from PIL import Image

# --- Classe para a janela de diálogo de seleção de executável ---
class SelectExecutableDialog(ctk.CTkToplevel):
    def __init__(self, parent, executables, current_exe=None):
        super().__init__(parent)
        self.title("Selecionar Executável")
        self.geometry("350x250")
        self.transient(parent)
        self.grab_set()
        self.executables = executables
        self.result = None
        self.label = ctk.CTkLabel(self, text="Qual arquivo inicia o jogo?")
        self.label.pack(padx=20, pady=10)
        initial_value = current_exe if current_exe in self.executables else self.executables[0]
        self.radio_var = ctk.StringVar(value=initial_value)
        for exe in self.executables:
            radio = ctk.CTkRadioButton(self, text=exe, variable=self.radio_var, value=exe)
            radio.pack(padx=20, pady=5, anchor="w")
        self.ok_button = ctk.CTkButton(self, text="Confirmar", command=self.on_ok)
        self.ok_button.pack(padx=20, pady=20)
    def on_ok(self):
        self.result = self.radio_var.get()
        self.destroy()
    def get_selection(self):
        self.wait_window()
        return self.result

# --- Classe para a janela de edição do jogo ---
class EditGameDialog(ctk.CTkToplevel):
    def __init__(self, parent, perfil):
        super().__init__(parent)
        self.title(f"Editando '{perfil['nome_amigavel']}'")
        self.geometry("400x300")
        self.transient(parent)
        self.grab_set()
        self.perfil = perfil
        self.resultado = None
        ctk.CTkLabel(self, text="Nome do Jogo:").pack(padx=20, pady=(10,0), anchor="w")
        self.nome_entry = ctk.CTkEntry(self, width=360)
        self.nome_entry.insert(0, perfil['nome_amigavel'])
        self.nome_entry.pack(padx=20, pady=5, anchor="w")
        self.label_executavel = ctk.CTkLabel(self, text=f"Executável Atual: {perfil['executavel_relativo']}")
        self.label_executavel.pack(padx=20, pady=(10,0), anchor="w")
        self.change_exe_button = ctk.CTkButton(self, text="🔎 Alterar Executável", command=self.alterar_executavel)
        self.change_exe_button.pack(padx=20, pady=5, anchor="w")
        self.novo_executavel = perfil['executavel_relativo']
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(padx=20, pady=20, fill="x", side="bottom")
        self.save_button = ctk.CTkButton(self.button_frame, text="Salvar Alterações", command=self.salvar)
        self.save_button.pack(side="right", padx=(10,0))
        self.cancel_button = ctk.CTkButton(self.button_frame, text="Cancelar", command=self.destroy, fg_color="gray")
        self.cancel_button.pack(side="right")
    def alterar_executavel(self):
        executaveis = file_utils.listar_executaveis(self.perfil['caminho_pasta_jogo'])
        if not executaveis:
            messagebox.showwarning("Aviso", "Não há outros executáveis nesta pasta.", parent=self)
            return
        dialog = SelectExecutableDialog(self, executaveis, self.novo_executavel)
        selecao = dialog.get_selection()
        if selecao:
            self.novo_executavel = selecao
            self.label_executavel.configure(text=f"Executável Atual: {self.novo_executavel}")
    def salvar(self):
        nome_get = self.nome_entry.get()
        if not nome_get.strip():
            messagebox.showerror("Erro", "O nome do jogo não pode estar vazio.", parent=self)
            return
        self.resultado = {"nome_amigavel": nome_get, "executavel_relativo": self.novo_executavel}
        self.destroy()
    def get_data(self):
        self.wait_window()
        return self.resultado

# --- Classe para a janela de configuração do DOSBox ---
class ConfigDosboxDialog(ctk.CTkToplevel):
    def __init__(self, parent, perfil):
        super().__init__(parent)
        self.title("Configurar DOSBox")
        self.geometry("400x350")
        self.transient(parent)
        self.grab_set()
        self.resultado = None
        config = perfil.get("dosbox_config", {})
        ctk.CTkLabel(self, text="Tela:").pack(padx=20, pady=(10,0), anchor="w")
        self.fullscreen_var = ctk.StringVar(value=config.get("fullscreen", "false"))
        self.fullscreen_check = ctk.CTkCheckBox(self, text="Iniciar em tela cheia", variable=self.fullscreen_var, onvalue="true", offvalue="false")
        self.fullscreen_check.pack(padx=20, pady=5, anchor="w")
        ctk.CTkLabel(self, text="Saída de Vídeo:").pack(padx=20, pady=(10,0), anchor="w")
        self.output_var = ctk.StringVar(value=config.get("output", "opengl"))
        self.output_menu = ctk.CTkOptionMenu(self, values=["surface", "opengl", "openglnb", "ddraw"], variable=self.output_var)
        self.output_menu.pack(padx=20, pady=5, fill="x")
        ctk.CTkLabel(self, text="Ciclos de CPU (ex: auto, max, 30000):").pack(padx=20, pady=(10,0), anchor="w")
        self.cycles_entry = ctk.CTkEntry(self, placeholder_text=config.get("cycles", "auto"))
        self.cycles_entry.insert(0, config.get("cycles", "auto"))
        self.cycles_entry.pack(padx=20, pady=5, fill="x")
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(padx=20, pady=20, fill="x", side="bottom")
        self.save_button = ctk.CTkButton(self.button_frame, text="Salvar", command=self.salvar)
        self.save_button.pack(side="right", padx=(10,0))
        self.cancel_button = ctk.CTkButton(self.button_frame, text="Cancelar", command=self.destroy, fg_color="gray")
        self.cancel_button.pack(side="right")
    def salvar(self):
        self.resultado = {"fullscreen": self.fullscreen_var.get(), "output": self.output_var.get(), "cycles": self.cycles_entry.get()}
        self.destroy()
    def get_data(self):
        self.wait_window()
        return self.resultado

# --- Classe Principal da Aplicação ---
class DOSBoxLauncherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Launcher DOSBox")
        self.geometry("1024x768")

        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(base_path, "assets", "icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Erro ao definir o ícone: {e}")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Coluna Esquerda
        self.frame_esquerda = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_esquerda.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_esquerda.grid_rowconfigure(0, weight=1)
        self.frame_esquerda.grid_rowconfigure(1, weight=0)
        self.frame_lista_jogos = ctk.CTkFrame(self.frame_esquerda)
        self.frame_lista_jogos.grid(row=0, column=0, sticky="nsew")
        self.frame_lista_jogos.grid_columnconfigure(0, weight=1)
        self.frame_lista_jogos.grid_rowconfigure(1, weight=1)
        label_lista_jogos = ctk.CTkLabel(self.frame_lista_jogos, text="Meus Jogos", font=ctk.CTkFont(size=16, weight="bold"))
        label_lista_jogos.grid(row=0, column=0, padx=10, pady=10)
        self.scrollable_frame_jogos = ctk.CTkScrollableFrame(self.frame_lista_jogos)
        self.scrollable_frame_jogos.grid(row=1, column=0, padx=10, pady=(0,10), sticky="nsew")
        self.frame_botoes_acao = ctk.CTkFrame(self.frame_esquerda)
        self.frame_botoes_acao.grid(row=1, column=0, sticky="ew", pady=(10,0))
        self.botao_importar = ctk.CTkButton(self.frame_botoes_acao, text="📂 Importar Pasta", command=self.importar_jogo_ui)
        self.botao_importar.pack(padx=10, pady=(10, 5), fill="x")
        self.botao_importar_zip = ctk.CTkButton(self.frame_botoes_acao, text="📦 Importar .ZIP", command=self.importar_zip_ui)
        self.botao_importar_zip.pack(padx=10, pady=(0, 5), fill="x")
        self.botao_jogar = ctk.CTkButton(self.frame_botoes_acao, text="▶️ Jogar", command=self.jogar_selecionado, state="disabled")
        self.botao_jogar.pack(padx=10, pady=5, fill="x")
        self.botao_editar = ctk.CTkButton(self.frame_botoes_acao, text="🔁 Editar", command=self.editar_jogo_ui, state="disabled")
        self.botao_editar.pack(padx=10, pady=5, fill="x")
        self.botao_config_dosbox = ctk.CTkButton(self.frame_botoes_acao, text="🎛️ Configurar DOSBox", command=self.configurar_dosbox_ui, state="disabled")
        self.botao_config_dosbox.pack(padx=10, pady=5, fill="x")
        self.botao_remover = ctk.CTkButton(self.frame_botoes_acao, text="🗑️ Remover", command=self.remover_jogo_ui, state="disabled", fg_color="red", hover_color="darkred")
        self.botao_remover.pack(padx=10, pady=5, fill="x")

        # Coluna Direita
        self.frame_direita = ctk.CTkFrame(self)
        self.frame_direita.grid(row=0, column=1, padx=(0,10), pady=10, sticky="nsew")
        self.frame_direita.grid_columnconfigure(0, weight=1)
        self.frame_direita.grid_rowconfigure(0, weight=1)
        self.label_imagem_preview = ctk.CTkLabel(self.frame_direita, text="Selecione um jogo para ver a imagem", font=ctk.CTkFont(size=16), text_color="gray")
        self.label_imagem_preview.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.perfil_selecionado = None
        self.botoes_jogos = {}
        self.atualizar_lista_jogos()

    def atualizar_lista_jogos(self):
        for widget in self.scrollable_frame_jogos.winfo_children():
            widget.destroy()
        self.botoes_jogos.clear()
        self.botao_jogar.configure(state="disabled")
        self.botao_editar.configure(state="disabled")
        self.botao_remover.configure(state="disabled")
        self.botao_config_dosbox.configure(state="disabled")
        self.perfil_selecionado = None
        self.label_imagem_preview.configure(image=None, text="Selecione um jogo para ver a imagem")
        self.perfis = dosbox_manager.carregar_perfis()
        self.perfis.sort(key=lambda p: p.get('nome_amigavel', '').lower())
        for perfil in self.perfis:
            nome_amigavel = perfil.get("nome_amigavel", "Nome não encontrado")
            btn_jogo = ctk.CTkButton(self.scrollable_frame_jogos, text=nome_amigavel, command=lambda p=perfil: self.selecionar_jogo(p))
            btn_jogo.pack(padx=10, pady=5, fill="x")
            self.botoes_jogos[perfil['id_jogo']] = btn_jogo

    def selecionar_jogo(self, perfil_clicado):
        self.perfil_selecionado = perfil_clicado
        for perfil_id, botao in self.botoes_jogos.items():
            if perfil_id == self.perfil_selecionado['id_jogo']:
                botao.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["hover_color"])
            else:
                botao.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        self.botao_jogar.configure(state="normal")
        self.botao_editar.configure(state="normal")
        self.botao_remover.configure(state="normal")
        self.botao_config_dosbox.configure(state="normal")
        caminho_imagem = self.perfil_selecionado.get("caminho_imagem")
        if caminho_imagem and os.path.exists(caminho_imagem):
            try:
                imagem_pil = Image.open(caminho_imagem)
                # Usamos winfo_width() e winfo_height() para obter o tamanho do widget dinamicamente
                # É necessário chamar self.update_idletasks() para garantir que as dimensões estejam calculadas
                self.update_idletasks()
                largura_max = self.label_imagem_preview.winfo_width()
                altura_max = self.label_imagem_preview.winfo_height()
                imagem_pil.thumbnail((largura_max - 20, altura_max - 20))
                ctk_imagem = ctk.CTkImage(light_image=imagem_pil, dark_image=imagem_pil, size=imagem_pil.size)
                self.label_imagem_preview.configure(image=ctk_imagem, text="")
            except Exception as e:
                self.label_imagem_preview.configure(image=None, text=f"Erro ao carregar imagem:\n{e}")
        else:
            self.label_imagem_preview.configure(image=None, text="Imagem não definida")

    def jogar_selecionado(self):
        if not self.perfil_selecionado: return
        sucesso, mensagem = dosbox_manager.gerar_e_executar_jogo(self.perfil_selecionado)
        if not sucesso: messagebox.showerror("Erro ao Iniciar", mensagem)

    def _finalizar_importacao(self, pasta_destino, nome_base):
        executaveis = file_utils.listar_executaveis(pasta_destino)
        if not executaveis:
            messagebox.showerror("Erro", "Nenhum executável (.exe, .bat, .com) encontrado.", parent=self)
            shutil.rmtree(pasta_destino); return
        dialog_exe = SelectExecutableDialog(self, executaveis)
        executavel_selecionado = dialog_exe.get_selection()
        if not executavel_selecionado:
            shutil.rmtree(pasta_destino); return
        nome_amigavel = simpledialog.askstring("Nome do Jogo", "Digite um nome para o jogo:", initialvalue=nome_base.replace("_", " ").title(), parent=self)
        if not nome_amigavel:
            shutil.rmtree(pasta_destino); return
        messagebox.showinfo("Imagem do Jogo", "Agora, selecione um arquivo de imagem (ex: capa do jogo).", parent=self)
        caminho_imagem = filedialog.askopenfilename(title="Selecione uma imagem", filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if not caminho_imagem: caminho_imagem = ""
        novo_perfil = {
            "id_jogo": os.path.basename(pasta_destino), "nome_amigavel": nome_amigavel,
            "caminho_pasta_jogo": pasta_destino, "executavel_relativo": executavel_selecionado,
            "caminho_imagem": caminho_imagem,
            "dosbox_config": {"fullscreen": "false", "output": "opengl", "cycles": "auto"}
        }
        dosbox_manager.salvar_novo_perfil(novo_perfil)
        messagebox.showinfo("Sucesso", f"O jogo '{nome_amigavel}' foi importado!")
        self.atualizar_lista_jogos()

    def importar_jogo_ui(self):
        pasta_origem = filedialog.askdirectory(title="Selecione a pasta do jogo")
        if not pasta_origem: return
        nome_jogo_base = os.path.basename(pasta_origem)
        pasta_destino = os.path.join("games", nome_jogo_base)
        contador = 1
        while os.path.exists(pasta_destino):
            pasta_destino = os.path.join("games", f"{nome_jogo_base}_{contador}")
            contador += 1
        try:
            shutil.copytree(pasta_origem, pasta_destino)
            self._finalizar_importacao(pasta_destino, nome_jogo_base)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao copiar: {e}")

    def importar_zip_ui(self):
        caminho_zip = filedialog.askopenfilename(title="Selecione o arquivo .ZIP", filetypes=[("Arquivos ZIP", "*.zip")])
        if not caminho_zip: return
        nome_base = os.path.splitext(os.path.basename(caminho_zip))[0]
        pasta_destino = os.path.join("games", nome_base)
        contador = 1
        while os.path.exists(pasta_destino):
            pasta_destino = os.path.join("games", f"{nome_base}_{contador}")
            contador += 1
        try:
            os.makedirs(pasta_destino)
            with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
                zip_ref.extractall(pasta_destino)
            self._finalizar_importacao(pasta_destino, nome_base)
        except zipfile.BadZipFile:
            messagebox.showerror("Erro", "Arquivo .ZIP inválido ou corrompido."); shutil.rmtree(pasta_destino)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def remover_jogo_ui(self):
        if not self.perfil_selecionado: return
        nome_jogo = self.perfil_selecionado['nome_amigavel']
        id_jogo = self.perfil_selecionado['id_jogo']
        if not messagebox.askyesno("Confirmar", f"Remover o jogo '{nome_jogo}'?"): return
        dosbox_manager.remover_perfil(id_jogo)
        caminho_pasta_jogo = self.perfil_selecionado['caminho_pasta_jogo']
        if messagebox.askyesno("Apagar Pasta?", f"Perfil removido. Deseja apagar a pasta do jogo?"):
            if os.path.exists(caminho_pasta_jogo):
                try:
                    shutil.rmtree(caminho_pasta_jogo)
                    messagebox.showinfo("Sucesso", "Jogo e arquivos removidos.")
                except Exception as e:
                    messagebox.showerror("Erro", f"Não foi possível apagar a pasta: {e}")
        else:
            messagebox.showinfo("Concluído", "Perfil do jogo removido.")
        self.atualizar_lista_jogos()

    def editar_jogo_ui(self):
        if not self.perfil_selecionado: return
        dialog = EditGameDialog(self, self.perfil_selecionado)
        dados_atualizados = dialog.get_data()
        if dados_atualizados:
            dosbox_manager.atualizar_perfil(self.perfil_selecionado['id_jogo'], dados_atualizados)
            self.atualizar_lista_jogos()
            messagebox.showinfo("Sucesso", "Informações do jogo atualizadas.")

    def configurar_dosbox_ui(self):
        if not self.perfil_selecionado: return
        dialog = ConfigDosboxDialog(self, self.perfil_selecionado)
        novas_configs = dialog.get_data()
        if novas_configs:
            dados_para_atualizar = {"dosbox_config": novas_configs}
            dosbox_manager.atualizar_perfil(self.perfil_selecionado['id_jogo'], dados_para_atualizar)
            self.perfil_selecionado.get("dosbox_config", {}).update(novas_configs)
            messagebox.showinfo("Sucesso", "Configurações do DOSBox salvas!")


if __name__ == "__main__":
    from utils import dosbox_manager, file_utils
    
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    app = DOSBoxLauncherApp()
    app.mainloop()