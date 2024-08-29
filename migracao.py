import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import customtkinter as ctk
import oracledb


global banco_selecionado

# Criação de uma variável global para armazenar os detalhes de conexão do banco de dados
db_config = {"user": "root",
    "password": "S@nx5497",
    "host": "localhost"}


# Configurações do banco de dados Oracle
db_configorcl = {
    "user": "system",
    "password": "system",
    "host": "192.168.0.17",
    "port": "1521",
    "service_name": "orcl"
}

#Cnfiguração do oracle sql
def janela_config_bd02(banco_selecionado):
    
    janela05 = tk.Toplevel()
    janela05.title("Configuração do Banco de Dados Oracle")
    janela05.geometry("900x450")

    # Criação input campos par conexão do bd
    tk.Label(janela05, text="Usuário:").grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(janela05, width=20)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(janela05, text="Senha:").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(janela05, width=20, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(janela05, text="Host:").grid(row=2, column=0, padx=10, pady=10)
    host_entry = tk.Entry(janela05, width=20)
    host_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(janela05, text="Porta:").grid(row=3, column=0, padx=10, pady=10)
    port_entry = tk.Entry(janela05, width=20)
    port_entry.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(janela05, text="Nome do Serviço:").grid(row=4, column=0, padx=10, pady=10)
    service_name_entry = tk.Entry(janela05, width=20)
    service_name_entry.grid(row=4, column=1, padx=10, pady=10)

    def salva_config():

        # Salva as informações de entrada
        db_config["user"] = username_entry.get()
        db_config["password"] = password_entry.get()
        db_config["host"] = host_entry.get()
        db_config["port"] = port_entry.get()
        db_config["service_name"] = service_name_entry.get()

        janela05.destroy()
        # Aqui você pode chamar a função que usa as credenciais do banco de dados
        conecta_oracle()

       # migrar_banco(banco_selecionado)

    conect_button = tk.Button(master=janela05, text="CONECTAR", command=salva_config)
    conect_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    voltar_button = tk.Button(janela05, text="VOLTAR", command=janela05.destroy)
    voltar_button.grid(row=5, column=2, columnspan=2, padx=10, pady=10)

    print("Banco selecionado 2:", banco_selecionado)


def migrar_banco(banco_selecionado):
    mysql_conn = None
    try:
        # Conecta ao banco de dados Oracle
        conn = oracledb.connect(user=db_configorcl["user"], password=db_configorcl["password"],
               dsn=f'{db_configorcl["host"]}:{db_configorcl["port"]}/{db_configorcl["service_name"]}')

        print("Conexão com o banco de dados Oracle bem-sucedida!")
        
        sql = "SELECT username FROM dba_users"
        # Cria um novo banco de dados Oracle com o nome do banco selecionado
        cursor = conn.cursor()
        cursor.execute(sql)
        #cursor.execute("SELECT USERNAME FROM DBA_USERS")
        # Fetcha os resultados da consulta
        usuarios = cursor.fetchall()
        # Imprime os usuários
        for usuario in usuarios:
            print(usuario[0])



        cursor.execute(f"CREATE DATABASE {banco_selecionado} CHARACTER SET UTF8;")

        


        # Migrar tabelas do banco de dados MySQL para o banco de dados Oracle
        mysql_conn = mysql.connector.connect(
            user=db_config["user"],
            password=db_config["password"],
            host=db_config["host"],
            database=banco_selecionado
        )

        mysql_cursor = mysql_conn.cursor()
        mysql_cursor.execute("SHOW TABLES;")
        tables = [row[0] for row in mysql_cursor.fetchall()]

        for table in tables:
            mysql_cursor.execute(f"DESCRIBE {table};")
            columns = [row[0] for row in mysql_cursor.fetchall()]
            column_types = [row[1] for row in mysql_cursor.fetchall()]

            create_table_sql = f"CREATE TABLE {table} ("

            for i, column in enumerate(columns):
                create_table_sql += f"{column} {column_types[i]}, "
            create_table_sql = create_table_sql[:-2] + ");"

            cursor.execute(create_table_sql)

            mysql_cursor.execute(f"SELECT * FROM {table};")

            rows = mysql_cursor.fetchall()

            for row in rows:
                insert_sql = f"INSERT INTO {table} VALUES ("

                for value in row:
                    insert_sql += f"'{value}', "

                insert_sql = insert_sql[:-2] + ");"

                cursor.execute(insert_sql)


        conn.commit()

        print("Migração do banco de dados concluída com sucesso!")

    except oracledb.Error as error:
        messagebox.showerror("Erro de Migração", f"Erro ao migrar o banco de dados: {error}")

    finally:
        if mysql_conn is not None:  # Verifique se a variável foi atribuída
            mysql_conn.close()
        conn.close()



def conecta_oracle():
    try:
        # Conecta ao banco de dados Oracle
        conn = oracledb.connect(user=db_config["user"], password=db_config["password"],
                                 dsn=f'{db_config["host"]}:{db_config["port"]}/{db_config["service_name"]}')
        print("Conexão com o banco de dados Oracle bem-sucedida mermão!")
        # Adicione aqui o código para realizar operações no banco de dados, como consulta de dados
        conn.close()
    except oracledb.Error as error:
        messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados Oracle: {error}")



# Criação da janela tabelas
def janela_tabela(banco_selecionado):
    
    janela4 = tk.Toplevel()
    janela4.title("FSW MIGRAÇÇÃO DE DDOS")
    janela4.geometry("900x450")  # Define o tamanho da janela
    janela4.resizable(False, False) 

    # Conectar ao banco de dados MySQL
    try:
        cnx = mysql.connector.connect(
            user=db_config["user"],
            password=db_config["password"],
            host=db_config["host"],
            database=banco_selecionado
        )

        cursor = cnx.cursor()
        cursor.execute("show tables;")
        rows = cursor.fetchall()
        table_options = [row[0] for row in rows]
        #table_options = [...]  
        #table_options.insert(0, "TABELAS") 

    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        return


    # Set os valores do combobox
    #table_options = [...]  
    #table_options.insert(0, "TABELAS") 

    tabelas_combobox = ttk.Combobox(janela4, font=("Helvetica", 12))
    tabelas_combobox['values'] = table_options
    tabelas_combobox.current(0)
    tabelas_combobox.grid(row=3, column=0, padx=10, pady=10)

    # Label para o banco selecionado
    banco_label = tk.Label(janela4, text="BANCO SELECIONADO", font=("Helvetica", 12))
    banco_label.grid(row=0, column=0, padx=10, pady=10)

    # Label para exibir o nome do banco selecionado
    banco_nome = tk.Label(janela4, text=banco_selecionado, font=("Helvetica", 12)) 
    banco_nome.grid(row=1, column=0, padx=10, pady=10)

    estrutura_dados_var = tk.BooleanVar(value=False)
    estrutura_dados_checkbox = tk.Checkbutton(janela4, text="MGRAR ESTRUTURA E DADOS", variable=estrutura_dados_var, font=("Helvetica", 12))
    estrutura_dados_checkbox.grid(row=4, column=0, padx=10, pady=10)

    # Checkbox para migrar somente estrutura
    somente_estrutura_var = tk.BooleanVar(value=False)
    somente_estrutura_checkbox = tk.Checkbutton(janela4, text="MGRAR SOMENTE ESTRUTURA", variable=somente_estrutura_var, font=("Helvetica", 12))
    somente_estrutura_checkbox.grid(row=5, column=0, padx=10, pady=10)

    # Botão "SIM"
    #sim_button = tk.Button(master=janela4, text="SIM", command=janela_config_bd02)
    sim_button = tk.Button(master=janela4, text="SIM", command=lambda: janela_config_bd02(banco_selecionado))
    sim_button.configure(font=("Helvetica", 18))
    sim_button.grid(row=6, column=0, padx=100, pady=100)

    # Botão "NÃO"
    nao_button = tk.Button(janela4, text="NÃO", command=janela4.destroy)
    nao_button.configure(font=("Helvetica", 18))
    nao_button.grid(row=6, column=2, padx=430, pady=100)

    print("Banco selecionado:", banco_selecionado)


# função para conectar ao BD MySQL
def janela_config_bd01():

    config_janela = tk.Toplevel()
    config_janela.title("Configuração do Banco de Dados MySQL")
    config_janela.geometry("900x450")

    # Criação input campos par conexão do bd
    tk.Label(config_janela, text="Usuário:").grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(config_janela, width=20)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(config_janela, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(config_janela, width=20, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(config_janela, text="Host:").grid(row=2, column=0, padx=10, pady=10)
    host_entry = tk.Entry(config_janela, width=20)
    host_entry.grid(row=2, column=1, padx=10, pady=10)
 
    def salva_config():

        # Salva as nformações de entrada
        db_config["user"] = username_entry.get()
        db_config["password"] = password_entry.get()
        db_config["host"] = host_entry.get()

        config_janela.destroy()
        janela_mysql()

    conect_button = tk.Button(master=config_janela, text="CONECTAR", command=salva_config)
    conect_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    voltar_button = tk.Button(config_janela, text="VOLTAR", command=config_janela.destroy)
    voltar_button.grid(row=4, column=2, columnspan=2, padx=10, pady=10)


    #Criacao d janela de acesso ao Mysql
def janela_mysql():

    janela03 = tk.Tk()
    janela03.title("FSW MIGRAÇÃO DE DADOS")
    janela03.geometry("900x450")  # Define o tamanho da janela
    janela03.resizable(False, False)  # Evita que a janela seja redimensionada


    # Conectar ao banco de dados MySQL
    try:
        cnx = mysql.connector.connect(
            user=db_config["user"],
            password=db_config["password"],
            host=db_config["host"]
        
        )
        cursor = cnx.cursor()
        # Selecionar um banco de dados padrão
        cursor.execute("use clinica_medica;")

        cursor.execute("CALL sp_listar_bancos();")
        rows = cursor.fetchall()
        database_options = [row[0] for row in rows]
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        return

    # Criaçao dos botões de confirmação
    sim_button = tk.Button(master=janela03, text="Sim", command=lambda: janela_tabela(database_variable.get()))
    sim_button.configure(font=("Helvetica", 18))
    sim_button.grid(row=1, column=0, padx=70, pady=80)

    nao_button = tk.Button(janela03, text="Não", command=janela03.destroy)
    nao_button.configure(font=("Helvetica", 18))
    nao_button.grid(row=1, column=1, padx=250, pady=100)


    # Criação do combo box seleção do banco de dados
    database_label = tk.Label(janela03, text="Selecione o Banco de Dados:", font=("Helvetica", 12))
    database_label.grid(row=0, column=0, padx=100, pady=100)
    database_variable = tk.StringVar(janela03)
    database_variable.set(database_options[0]) 
    database_dropdown = ttk.Combobox(janela03, textvariable=database_variable, values=database_options, font=("Helvetica", 12))
    database_dropdown.grid(row=0, column=1, padx=100, pady=100)

    def update_banco_selecionado(event):
        banco_selecionado = database_variable.get()

        database_dropdown.bind("<<ComboboxSelected>>", update_banco_selecionado)


        # Cria uma variável global para armazenar o banco de dados selecionado
        #banco_selecionado = database_variable.get()
        print("Banco selecionado:", banco_selecionado)

    #janela_mysql.mainloop()

    # Close the connection
    cursor.close()
    cnx.close()


# Criação da janela principal seleção do bd para migração
janela01 = tk.Tk()
janela01.title("FSW Migração de Bancos de Dados")
janela01.geometry("900x450")  # Define o tamanho da janela
janela01.resizable(False, False)  # Evita que a janela seja redimensionada

# Define a fonte para os elementos da interface
font_title = ("Helvetica", 14, "bold")
font_label = ("Helvetica", 10)

# Cria o label para a escolha do banco
banco_label = tk.Label(janela01, text="ECOLHA O BANCO DE DADOS PARA MIGRAÇÃO", font=font_label)
banco_label.pack()

# Cria a caixa de seleção para o banco de dados
banco_var = tk.StringVar(value="MySQL PARA ORACLE")
banco_options = ["MySQL PARA ORACLE", "ORACLE PARA MySQL"]
banco_combobox = ttk.Combobox(janela01, textvariable=banco_var, values=banco_options, state="readonly")
banco_combobox.pack(pady=5)


# Cria os botões Sim e Não

def sim_button_clicked():

    if banco_var.get() == "MySQL PARA ORACLE":
        janela_config_bd01()

    else:
        print("Opção inválida")

sim_button = tk.Button(janela01, text="SIM", width=10, height=2, command=sim_button_clicked)
sim_button.pack(side="left", padx=100)

nao_button = tk.Button(janela01, text="NÃO", width=10, height=2, command=janela01.destroy)
nao_button.pack(side="right", padx=100)

# Executa a interface gráfica
janela01.mainloop()