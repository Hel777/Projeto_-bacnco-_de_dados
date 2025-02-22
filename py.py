import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3


class banco_dados:
    def __init__(self):
        self.banco()
        self.tabela()

    def banco(self):
        self.conn = sqlite3.connect("Dados_clientes.db")
        self.cursor = self.conn.cursor()

    def tabela(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS pessoas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                cpf TEXT,
                concecionaria TEXT,
                vendedor TEXT,
                data_instalacao TEXT,
                contato TEXT
            )"""
        )

    def inserir(self, nome, cpf, concecionaria, vendedor, data_instalacao, contato):
        self.cursor.execute(
            "INSERT INTO pessoas (nome, cpf, concecionaria, vendedor, data_instalacao, contato) VALUES (?,?,?,?,?,?)",
            (nome, cpf, concecionaria, vendedor, data_instalacao, contato),
        )
        self.conn.commit()

    def buscar_todos(self):
        self.cursor.execute("SELECT * FROM pessoas")
        return self.cursor.fetchall()

    def deletar(self, id):
        self.cursor.execute("DELETE FROM pessoas WHERE id =?", (id,))
        self.conn.commit()

    def fechar_conexao(self):
        self.conn.close()


class application:
    def __init__(self):
        self.banco = banco_dados()
        self.root = tk.Tk()
        self.config_tela()
        self.widgets()
        self.carregar_dados()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def enviar(self):
        nome = self.nome_entry.get()
        cpf = self.cpf_entry.get()
        concecionaria = self.concecionaria_entry.get()
        vendedor = self.vendedor_entry.get()
        data_instalacao = self.data_instalacao_entry.get()
        contato = self.contato_entry.get()

        try:
            if (
                nome
                and cpf
                and concecionaria
                and vendedor
                and data_instalacao
                and contato
            ):
                with open("arquivo10.txt", "a") as dados10:
                    dados10.write(
                        f"Nome do cliente: {nome}\nCPF do cliente: {cpf}\nConcecionária: {concecionaria}\nVendedor: {vendedor}\nData de Instalação: {data_instalacao}\nContato: {contato}\n\n"
                    )

                self.banco.inserir(
                    nome, cpf, concecionaria, vendedor, data_instalacao, contato
                )

                messagebox.showinfo("Dados enviados com Sucesso")

                self.nome_entry.delete(0, tk.END)
                self.cpf_entry.delete(0, tk.END)
                self.concecionaria_entry.delete(0, tk.END)
                self.vendedor_entry.delete(0, tk.END)
                self.data_instalacao_entry.delete(0, tk.END)
                self.contato_entry.delete(0, tk.END)

                self.carregar_dados()

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def config_tela(self):
        self.root.configure(bg="#4682B4")
        self.root.title("Dados")
        self.root.geometry("1280x1024")
        self.root.resizable(False, False)

    def widgets(self):
        # Widgets aqui (mesmo código que você já tem)
        # ...

        # NOME DO CLIENTE
        nome_label = tk.Label(self.root, text="Nome do cliente:")
        nome_label.place(relx=0.4, rely=0.12)

        self.nome_entry = tk.Entry(self.root, fg="black", bg="white")
        self.nome_entry.place(relx=0.4, rely=0.14)

        # CPF DO CLIENTE

        CPF_label = tk.Label(self.root, text="CPF:")
        CPF_label.place(relx=0.4, rely=0.17)

        self.cpf_entry = tk.Entry(self.root, fg="black", bg="white")
        self.cpf_entry.place(relx=0.4, rely=0.19)

        # Concecionária

        concecionaria_label = tk.Label(self.root, text="Concecionária:")
        concecionaria_label.place(relx=0.4, rely=0.22)

        self.concecionaria_entry = tk.Entry(self.root, fg="black", bg="white")
        self.concecionaria_entry.place(relx=0.4, rely=0.24)

        # Vendedor

        vendedor_label = tk.Label(self.root, text="Vendedor:")
        vendedor_label.place(relx=0.4, rely=0.27)

        self.vendedor_entry = tk.Entry(self.root, fg="black", bg="white")
        self.vendedor_entry.place(relx=0.4, rely=0.29)

        # Data_instalação

        data_instalacao_label = tk.Label(self.root, text="Data da instalacão:")
        data_instalacao_label.place(relx=0.4, rely=0.32)

        self.data_instalacao_entry = tk.Entry(self.root, fg="black", bg="white")
        self.data_instalacao_entry.place(relx=0.4, rely=0.34)

        # contato do cliente

        contato_label = tk.Label(self.root, text="Contato:")
        contato_label.place(relx=0.4, rely=0.37)

        self.contato_entry = tk.Entry(self.root, bg="white")
        self.contato_entry.place(relx=0.4, rely=0.39)

        # BOTÃO DE ENVIAR

        button = tk.Button(self.root, bg="green", text="ENVIAR", command=self.enviar)
        button.place(relx=0.435, rely=0.43)

        deletar_button = tk.Button(
            self.root, bg="red", text="DELETAR", command=self.deletar_selecionado
        )
        deletar_button.place(relx=0.435, rely=0.9)

        # TREEVIEW

        self.tree = ttk.Treeview(
            self.root,
            columns=(
                "ID",
                "Nome",
                "cpf",
                "Concecionária",
                "Vendedor",
                "Data_instalação",
                "Contato",
            ),
            show="headings",
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("cpf", text="CPF")
        self.tree.heading("Concecionária", text="Concecionária")
        self.tree.heading("Vendedor", text="Vendedor")
        self.tree.heading("Data_instalação", text="Data_instalação")
        self.tree.heading("Contato", text="Contato")

        self.tree.place(relx=0.032, rely=0.5, width=1200, height=400)

        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        scrollbar.place(relx=0.96, rely=0.5, height=400)  # Posicionar a barra de rolagem

        self.tree.configure(yscrollcommand=scrollbar.set)

    def carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        dados = self.banco.buscar_todos()

        for row in dados:
            self.tree.insert("", "end", values=row)

    def deletar_selecionado(self):
        try:
            item_selecionado = self.tree.selection()[0]
            id_para_deletar = self.tree.item(item_selecionado)["values"][0]

            confirmacao = messagebox.askyesno(
                "Confirmação",
                f"Tem certeza que deseja deletar o registro com ID {id_para_deletar}?",
            )

            if confirmacao:
                self.banco.deletar(id_para_deletar)
                messagebox.showinfo("Sucesso", "Registro deletado com sucesso.")
                self.carregar_dados()

        except IndexError:
            messagebox.showerror("Erro", "Nenhum registro selecionado para deletar.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao deletar o registro: {e}")

    def on_closing(self):
        self.banco.fechar_conexao()
        self.root.destroy()


application()
