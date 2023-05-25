from tkinter import * 
from tkinter import ttk
import sqlite3

# Cria a janela
root = Tk()

class Funcs():
    # Limpas os campos da tela
    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.endereco_entry.delete(0, END)
    
    #Conecta o banco de dados
    def concta_db(self):
        self.conn = sqlite3.connect('clientes.bd')
        self.cursor = self.conn.cursor(); print('Conectando ao Banco de Dados...')
    
    # Desconecta do banco de ddos
    def deconecta_db(self):
        self.conn.close(); print('Deconectando do Banco de Dados...')

    # Cria as tabelas do banco
    def cria_tabelas(self):
        self.concta_db()
        table_create_query = '''CREATE TABLE IF NOT EXISTS clientes(
                 id INTEGER PRIMARY KEY,
                 nome_cliente CHAR(40) NOT NULL,
                 telefone INTEGER(20),
                 endereco CHAR(50)  
            );'''
        self.cursor.execute(table_create_query); print('Tabelas criadas...')
        self.conn.commit()
        self.deconecta_db()
    # Adiciona um novo cliente
    def add_cliente(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.telefone = self.telefone_entry.get()
        self.endereco = self.endereco_entry.get()

        self.concta_db()

        clientes_insert_query = '''INSERT INTO clientes(nome_cliente, telefone, endereco)
                VALUES(?, ?, ?)        
        '''
        dados = (self.nome, self.telefone, self.endereco)

        self.cursor.execute(clientes_insert_query, dados)
        self.conn.commit()       
        self.deconecta_db()

        # Depois de adicionar um novo cliente inclui o novo cliente e atualiza a lista
        self.listar_clientes()
        self.limpa_tela()

    # Lista os clientes na tela 
    def listar_clientes(self):
        self.lista_cli.delete(*self.lista_cli.get_children())
        self.concta_db()

        clientes_select_query = '''SELECT id, nome_cliente, telefone, endereco
                                FROM clientes
                                ORDER BY nome_cliente ASC;
                            '''

        rows = self.cursor.execute(clientes_select_query)

        # Insere os clientes na view da lista
        for row in rows:
            self.lista_cli.insert("", END, values=row)

        self.deconecta_db()

class Application(Funcs):
    def __init__(self):
        self.root = root
        self.tela()      
        self.frames_da_tela()
        self.criar_botoes()
        self.lista_frame2()
        self.cria_tabelas()
        self.listar_clientes()
        root.mainloop()
    
    def tela(self):
        self.root.title("Despesas")
        self.root.configure(bg='#2F4F4F')
        self.root.geometry('700x500')
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=700)
        self.root.minsize(width=600, height=500)

    # Cria os frames da tela 
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bg='#DFE3EE', 
                             highlightbackground='#1E3743', highlightthickness=3)
        self.frame_1.place(relx=0.02 , rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = Frame(self.root, bg='#DFE3EE', 
                             highlightbackground='#1E3743', highlightthickness=3)
        self.frame_2.place(relx=0.02 , rely=0.5, relwidth=0.96, relheight=0.46)

    # Cria os botões da tela
    def criar_botoes(self):
        # Criar botão limpar
        self.bt_limpar = Button(self.frame_1, text='Limpar', bd=2, bg='#107DB2', fg='white',
                                 font=('verdana', 8, 'bold'), command=self.limpa_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relheight=0.1, relwidth=0.1)
        
        # Criar botão buscar
        self.bt_buscar = Button(self.frame_1, text='Buscar', bd=2, bg='#107DB2', fg='white',
                                 font=('verdana', 8, 'bold'))
        self.bt_buscar.place(relx=0.31, rely=0.1, relheight=0.1, relwidth=0.1)

        # Criar botão salvar
        self.bt_salvar = Button(self.frame_1, text='Salvar', bd=2, bg='#107DB2', fg='white',
                                 font=('verdana', 8, 'bold'), command=self.add_cliente)
        self.bt_salvar.place(relx=0.61, rely=0.1, relheight=0.1, relwidth=0.1)

        # Criar botão editar
        self.bt_editar= Button(self.frame_1, text='Editar', bd=2, bg='#107DB2', fg='white',
                                 font=('verdana', 8, 'bold'))
        self.bt_editar.place(relx=0.72, rely=0.1, relheight=0.1, relwidth=0.1)

        # Criar botão excluir
        self.bt_excluir = Button(self.frame_1, text='Apagar', bd=2, bg='#107DB2', fg='white',
                                 font=('verdana', 8, 'bold'))
        self.bt_excluir.place(relx=0.83, rely=0.1, relheight=0.1, relwidth=0.1)

        # Criar a label e entrada do código
        self.lb_codigo = Label(self.frame_1, text='Código', bg='#DFE3EE')
        self.lb_codigo.place(relx=0.05, rely=0.02, relheight=0.08)

        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.05, rely=0.1, relwidth=0.12)

        # Criar a label e entrada do nome
        self.lb_nome = Label(self.frame_1, text='Nome', bg='#DFE3EE')
        self.lb_nome.place(relx=0.05, rely=0.35, relheight=0.08)

        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.88)

        # Criar a label e entrada do telefone
        self.lb_telefone= Label(self.frame_1, text='Telefone', bg='#DFE3EE')
        self.lb_telefone.place(relx=0.05, rely=0.6, relheight=0.08)

        self.telefone_entry = Entry(self.frame_1)
        self.telefone_entry.place(relx=0.05, rely=0.7, relwidth=0.25)

        # Criar a label e entrada do endereço
        self.lb_endereco = Label(self.frame_1, text='Endereço', bg='#DFE3EE')
        self.lb_endereco.place(relx=0.33, rely=0.60, relheight=0.08)

        self.endereco_entry = Entry(self.frame_1)
        self.endereco_entry.place(relx=0.33, rely=0.7, relwidth=0.6)

    # Cria a Treeview
    def lista_frame2(self):
        self.lista_cli = ttk.Treeview(self.frame_2, height=3, column=('col1', 'col2', 'col3', 'col4'))
        self.lista_cli.heading('#0', text="")
        self.lista_cli.heading('#1', text="Código")
        self.lista_cli.heading('#2', text="Nome")
        self.lista_cli.heading('#3', text="Telefone")
        self.lista_cli.heading('#4', text="Endereço")

        self.lista_cli.column('#0', width=1)
        self.lista_cli.column('#1', width=30)
        self.lista_cli.column('#2', width=250)
        self.lista_cli.column('#3', width=50)
        self.lista_cli.column('#4', width=200)

        self.lista_cli.place(relx=0.02, rely=0.01, relwidth=0.95, relheight=0.85)

        self.scrooll_lista = Scrollbar(self.frame_2, orient='vertical')
        self.scrooll_lista.configure(command=self.lista_cli.yview)
        self.scrooll_lista.place(relx=0.96, rely=0.01, relwidth=0.04, relheight=0.85)

# Executa a aplicação
Application()





