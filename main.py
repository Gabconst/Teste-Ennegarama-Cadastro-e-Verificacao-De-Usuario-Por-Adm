import tkinter as tk
from tkinter import ttk, messagebox
import json
from perguntas import perguntas


def salvar_dados(dados):
    with open('dados_usuarios.txt', 'a') as file:
        file.write(json.dumps(dados) + '\n')


def carregar_dados():
    try:
        with open('dados_usuarios.txt', 'r') as file:
            return [json.loads(line) for line in file]
    except FileNotFoundError:
        return []


def salvar_todos_os_dados(dados):
    with open('dados_usuarios.txt', 'w') as file:
        for usuario in dados:
            file.write(json.dumps(usuario) + '\n')


def tela_login_adm():
    login_window = tk.Toplevel()
    login_window.title("Login do Administrador")
    login_window.configure(bg='black')

    tk.Label(login_window, text="Usuário:", bg='black', fg='white').grid(row=0, column=0)
    tk.Label(login_window, text="Senha:", bg='black', fg='white').grid(row=1, column=0)

    usuario_entry = tk.Entry(login_window)
    senha_entry = tk.Entry(login_window, show="*")
    usuario_entry.grid(row=0, column=1)
    senha_entry.grid(row=1, column=1)

    def login():
        if usuario_entry.get() == "ADM" and senha_entry.get() == "adm123":
            login_window.destroy()
            tela_adm()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")

    ttk.Button(login_window, text="Login", command=login).grid(row=2, column=1)


def tela_adm():
    adm_window = tk.Toplevel()
    adm_window.title("Dados dos Usuários")
    adm_window.configure(bg='black')

    dados = carregar_dados()

    def atualizar_lista_usuarios():
        lista_usuarios.delete(0, tk.END)
        for usuario in dados:
            lista_usuarios.insert(tk.END, usuario['nome'])

    def consultar_usuario():
        selected_index = lista_usuarios.curselection()
        if selected_index:
            usuario = dados[selected_index[0]]
            detalhes_usuario.delete(1.0, tk.END)
            detalhes_usuario.insert(tk.END, json.dumps(usuario, indent=4))
        else:
            messagebox.showwarning("Atenção", "Selecione um usuário para consultar.")

    def apagar_usuario():
        selected_index = lista_usuarios.curselection()
        if selected_index:
            confirm = messagebox.askyesno("Confirmação", "Tem certeza que deseja apagar este usuário?")
            if confirm:
                dados.pop(selected_index[0])
                salvar_todos_os_dados(dados)
                atualizar_lista_usuarios()
                detalhes_usuario.delete(1.0, tk.END)
                messagebox.showinfo("Informação", "Usuário apagado com sucesso.")
        else:
            messagebox.showwarning("Atenção", "Selecione um usuário para apagar.")

    frame_lista = tk.Frame(adm_window, bg='black')
    frame_lista.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_lista, text="Usuários Cadastrados", bg='black', fg='white').pack()

    lista_usuarios = tk.Listbox(frame_lista, bg='black', fg='white', selectbackground='gray')
    lista_usuarios.pack(fill=tk.BOTH, expand=True)

    frame_detalhes = tk.Frame(adm_window, bg='black')
    frame_detalhes.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(frame_detalhes, text="Detalhes do Usuário", bg='black', fg='white').pack()

    detalhes_usuario = tk.Text(frame_detalhes, bg='black', fg='white')
    detalhes_usuario.pack(fill=tk.BOTH, expand=True)

    frame_botoes = tk.Frame(adm_window, bg='black')
    frame_botoes.pack(fill=tk.X, padx=10, pady=10)

    ttk.Button(frame_botoes, text="Consultar", command=consultar_usuario).pack(side=tk.LEFT, padx=5)
    ttk.Button(frame_botoes, text="Apagar", command=apagar_usuario).pack(side=tk.LEFT, padx=5)

    atualizar_lista_usuarios()


def iniciar_teste(dados_usuario):
    def proxima_pergunta(index, resultados):
        if index == len(perguntas):
            # Calcula o tipo de personalidade do Eneagrama
            contagem_resultados = [0] * 9
            for r in resultados:
                contagem_resultados[r - 1] += 1
            tipo_personalidade = contagem_resultados.index(max(contagem_resultados)) + 1

            dados_usuario['tipo_personalidade'] = tipo_personalidade
            salvar_dados(dados_usuario)
            messagebox.showinfo("Teste Concluído",
                                f"Obrigado por completar o teste! Seu tipo de personalidade do Eneagrama é {tipo_personalidade}.")
            teste_window.destroy()
            return

        pergunta = perguntas[index]
        pergunta_label.config(text=pergunta['pergunta'])

        for i, opcao in enumerate(pergunta['opcoes']):
            botoes_opcoes[i].config(text=opcao, command=lambda r=pergunta['resultado'][i]: responder(r))

    def responder(resultado):
        resultados.append(resultado)
        proxima_pergunta(len(resultados), resultados)

    teste_window = tk.Toplevel()
    teste_window.title("Teste de Personalidade")
    teste_window.configure(bg='black')

    pergunta_label = tk.Label(teste_window, text="", wraplength=400, bg='black', fg='white')
    pergunta_label.pack()

    botoes_opcoes = [ttk.Button(teste_window) for _ in range(4)]
    for botao in botoes_opcoes:
        botao.pack(fill='x')

    resultados = []
    proxima_pergunta(0, resultados)


def tela_cadastro():
    cadastro_window = tk.Toplevel()
    cadastro_window.title("Cadastro de Usuário")
    cadastro_window.configure(bg='black')

    tk.Label(cadastro_window, text="Nome:", bg='black', fg='white').grid(row=0, column=0)
    tk.Label(cadastro_window, text="Idade:", bg='black', fg='white').grid(row=1, column=0)
    tk.Label(cadastro_window, text="Gênero:", bg='black', fg='white').grid(row=2, column=0)
    tk.Label(cadastro_window, text="Nacionalidade:", bg='black', fg='white').grid(row=3, column=0)

    nome_entry = tk.Entry(cadastro_window)
    idade_entry = tk.Entry(cadastro_window)

    genero_var = tk.StringVar()
    nacionalidade_var = tk.StringVar()

    nome_entry.grid(row=0, column=1)
    idade_entry.grid(row=1, column=1)

    ttk.Combobox(cadastro_window, textvariable=genero_var, values=["Masculino", "Feminino", "Neutro"]).grid(row=2,
                                                                                                            column=1)
    ttk.Combobox(cadastro_window, textvariable=nacionalidade_var,
                 values=["Brasil", "EUA", "Canadá", "Japão", "Alemanha"]).grid(row=3, column=1)

    def cadastrar():
        dados_usuario = {
            "nome": nome_entry.get(),
            "idade": idade_entry.get(),
            "genero": genero_var.get(),
            "nacionalidade": nacionalidade_var.get()
        }
        cadastro_window.destroy()
        iniciar_teste(dados_usuario)

    ttk.Button(cadastro_window, text="Cadastrar", command=cadastrar).grid(row=4, column=1)


def main():
    root = tk.Tk()
    root.title("Teste de Personalidade do Eneagrama")
    root.configure(bg='black')

    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 12), padding=6)
    style.configure('TLabel', background='black', foreground='white', font=('Helvetica', 12))
    style.configure('TEntry', background='black', foreground='white', font=('Helvetica', 12))
    style.configure('TCombobox', background='black', foreground='white', font=('Helvetica', 12))

    ttk.Button(root, text="Cadastro de Usuário", command=tela_cadastro).pack(fill='x', padx=10, pady=5)
    ttk.Button(root, text="Login do Administrador", command=tela_login_adm).pack(fill='x', padx=10, pady=5)

    root.mainloop()

main()

if __name__ == "_main_":
    main()