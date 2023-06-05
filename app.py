from tkinter import * 
from tkinter import ttk
import sqlite3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser

# Cria a janela
root = Tk()

class Relatorios():
    def print_cliente(self):
        webbrowser.open("cliente.pdf")

    def gerar_relarorio(self):
        self.c = canvas.Canvas("cliente.pdf")

        self.codigo_rel = self.codigo_entry.get()
        self.nome_rel = self.nome_entry.get()
        self.telefone_rel = self.telefone_entry.get()
        self.endereco_rel = self.endereco_entry.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 750, 'Ficha do Cliente')

        self.c.setFont("Helvetica-Bold", 14)
        self.c.drawString(50, 690, 'Codigo: ')
        self.c.drawString(50, 670, 'Nome: ')
        self.c.drawString(50, 650, 'Telefone: ')
        self.c.drawString(50, 630, 'Endereço: ')

        self.c.setFont("Helvetica", 14)
        self.c.drawString(150, 690, self.codigo_rel)
        self.c.drawString(150, 670, self.nome_rel)
        self.c.drawString(150, 650, self.telefone_rel)
        self.c.drawString(150, 630, self.endereco_rel)

        self.c.rect(20, 600, 600, 1, fill=True, stroke=False)

        self.c.showPage()
        self.c.save()
        self.print_cliente()


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

    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.telefone = self.telefone_entry.get()
        self.endereco = self.endereco_entry.get()

    # Adiciona um novo cliente
    def add_cliente(self):
        self.variaveis()
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

    def OnDoubleClick(self, event):
        self.limpa_tela()
        self.lista_cli.selection()

        for n in self.lista_cli.selection():
            col1, col2, col3, col4 = self.lista_cli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)
            self.endereco_entry.insert(END, col4)

    def deleta_cliente(self):
        self.variaveis()
        self.concta_db()

        clientes_delete_query = """DELETE FROM clientes WHERE id = ? """        
        dados = self.codigo

        self.cursor.execute(clientes_delete_query, dados)
        self.conn.commit()
        self.deconecta_db()
        self.limpa_tela()
        self.listar_clientes()

    def altera_cliente(self):
        self.variaveis()
        self.concta_db()

        clientes_update_query = """UPDATE clientes SET nome_cliente = ?, telefone = ?, endereco = ?
                    WHERE id = ?"""
        dados = (self.nome, self.telefone, self.endereco, self.codigo)

        self.cursor.execute(clientes_update_query, dados)
        self.conn.commit()
        self.deconecta_db()
        self.listar_clientes()
        self.limpa_tela()

    def busca_cliente(self):
        self.concta_db()
        self.lista_cli.delete(*self.lista_cli.get_children())

        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()    

        self.cursor.execute("""SELECT id, nome_cliente, telefone, endereco 
                        FROM clientes
                        WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC"""% nome)
        busca_nome_cliente = self.cursor.fetchall()

        for i in busca_nome_cliente:
            self.lista_cli.insert("", END, values=i)

        self.limpa_tela()            
        self.deconecta_db()
        

class Application(Funcs, Relatorios):
    def __init__(self):
        self.root = root
        self.tela()      
        self.frames_da_tela()
        self.criar_botoes()
        self.lista_frame2()
        self.cria_tabelas()
        self.listar_clientes()
        self.menus()
        root.mainloop()
    
    def tela(self):
        self.root.title("Cadastro de Clientes")
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
                                 font=('verdana', 8, 'bold'), command=self.busca_cliente)
        self.bt_buscar.place(relx=0.31, rely=0.1, relheight=0.1, relwidth=0.1)

        # Criar botão salvar
        self.bt_salvar = Button(self.frame_1, text='Salvar', bd=2, bg='#107DB2', fg='white',
                                 font=('verdana', 8, 'bold'), command=self.add_cliente)
        self.bt_salvar.place(relx=0.61, rely=0.1, relheight=0.1, relwidth=0.1)

        # Criar botão editar
        self.bt_editar= Button(self.frame_1, text='Alterar', bd=2, bg='#107DB2', fg='white',
                                 font=('verdana', 8, 'bold'), command=self.altera_cliente)
        self.bt_editar.place(relx=0.72, rely=0.1, relheight=0.1, relwidth=0.1)

        # Criar botão excluir
        self.bt_excluir = Button(self.frame_1, text='Apagar', bd=2, bg='#107DB2', fg='white',
                                 font=('verdana', 8, 'bold'), command=self.deleta_cliente)
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
        self.lista_cli.bind("<Double-1>", self.OnDoubleClick)           
    def menus(self):
        menubar = Menu(self.root)     
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()
        menubar.add_cascade(label="Opções", menu=filemenu)
        menubar.add_cascade(label="Relatórios", menu=filemenu2)

        filemenu.add_command(label="Limpar Cliente", command=self.limpa_tela)
        filemenu.add_command(label="Sair", command=Quit)

        filemenu2.add_command(label="Ficha do Cliente", command=self.gerar_relarorio)
        

# Executa a aplicação
Application()





