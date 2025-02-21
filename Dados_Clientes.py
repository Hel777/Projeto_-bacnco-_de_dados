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
            """ CREATE TABLE IF NOT EXISTS pessoas (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, idade INTEGER)"""
        )

    def inserir(self, nome, idade):
        self.cursor.execute(
            "INSERT INTO pessoas (nome, idade) VALUES (?,?)", (nome, idade)
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
        self.banco = (
            banco_dados()
        )  # sso permite que a classe application acesse todos os métodos e atributos da classe banco_dados.

        self.root = tk.Tk()
        self.config_tela()
        self.widgets()
        self.carregar_dados()
        self.root.mainloop()

    def enviar(self):
        nome = self.nome_entry.get()
        idade = self.idade_entry.get()

        try:
            if nome and idade:
                with open("arquivo10.txt", "a") as dados10:

                    dados10.write(
                        f"Nome do cliente: {nome} \n idade do cliente: {idade} \n"
                    )

                self.banco.inserir(nome, idade)

                messagebox.showinfo("Dados enviados com Sucesso")

                self.nome_entry.delete(0, tk.END)
                self.idade_entry.delete(0, tk.END)

                self.carregar_dados()  # Atualiza a Treeview após inserção

        except Exception as e:
            print(f"Ouve um erro de {e}")
            messagebox.showerror("Ouve um erro")

    def config_tela(self):
        self.root.configure(bg="#4682B4")
        self.root.title("Dados")
        self.root.geometry("1280x1024")
        self.root.resizable(False, False)

    def widgets(self):

        # NOME DO CLIENTE
        nome_label = tk.Label(self.root, text="Nome do cliente:")
        nome_label.place(relx=0.4, rely=0.12)

        self.nome_entry = tk.Entry(self.root, fg="black", bg="white")
        self.nome_entry.place(relx=0.4, rely=0.14)

        # CPF DO CLIENTE

        CPF_label = tk.Label(self.root, text="CPF:")
        CPF_label.place(relx=0.4, rely=0.17)

        self.idade_entry = tk.Entry(self.root, fg="black", bg="white")
        self.idade_entry.place(relx=0.4, rely=0.19)

        # contato do cliente

        contato_label = tk.Label(self.root, text="Contato:")
        contato_label.place(relx=0.4, rely=0.22)

        self.contato_entry = tk.Entry(self.root, fg="black", bg="white")
        self.contato_entry.place(relx=0.4, rely=0.24)

        # Concecionária

        concecionaria_label = tk.Label(self.root, text="Concecionária:")
        concecionaria_label.place(relx=0.4, rely=0.22)

        self.contato_entry = tk.Entry(self.root, fg="black", bg="white")
        self.contato_entry.place(relx=0.4, rely=0.24)

        # Vendedor

        vendedor_label = tk.Label(self.root, text="Vendedor:")
        vendedor_label.place(relx=0.4, rely=0.27)

        self.vendedor_entry = tk.Entry(self.root, fg="black", bg="white")
        self.vendedor_entry.place(relx=0.4, rely=0.29)

        # Data_instalação

        data_instalacao_label = tk.Label(self.root, text="Data da instalacao:")
        data_instalacao_label.place(relx=0.4, rely=0.32)

        self.vendedor_entry = tk.Entry(self.root, fg="black", bg="white")
        self.vendedor_entry.place(relx=0.4, rely=0.34)

        # BOTÃO DE ENVIAR

        button = tk.Button(self.root, bg="green", text="ENVIAR", command=self.enviar)
        button.place(relx=0.4, rely=0.5)

        deletar_button = tk.Button(
            self.root, bg="red", text="DELETAR", command=self.deletar_selecionado
        )
        deletar_button.place(relx=0.4, rely=0.9)

        # TREEVIEW

        self.tree = ttk.Treeview(
            self.root, columns=("ID", "Nome", "Idade"), show="headings"
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Idade", text="Idade")
        self.tree.place(relx=0.1, rely=0.7, width=700, height=200)

    def carregar_dados(self):

        # limpar a treeview antes de carregar novos dados

        for row in self.tree.get_children():
            self.tree.delete(row)

        dados = self.banco.buscar_todos()  # Atualiza a Treeview após inserção

        # INSERIR DADOS NA TREEVIEW

        for row in dados:
            self.tree.insert("", "end", values=row)

    def deletar_selecionado(self):

        try:
            item_selecionado = self.tree.selection()[
                0
            ]  # para pegar o primeiro item selecionado
            id_para_deletar = self.tree.item(item_selecionado)["values"][0]

            confirmacao = messagebox.askyesno(
                "Confirmação",
                f"Tem certeza que deseja deletar o registro com ID {id_para_deletar}?",
            )

            if confirmacao:
                # deleta o dado do banco de dados
                self.banco.deletar(id_para_deletar)

                messagebox.showinfo("Sucesso", "Registro deletado com sucesso.")

                # Atualizar treeview

                self.carregar_dados()

        except IndexError:
            messagebox.showerror("Erro", "Nenhum registro selecionado para deletar.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao deletar o registro: {e}")


application()
