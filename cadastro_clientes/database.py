import sqlite3 
DB_PATH = 'clientes.db'

def get_db():  #abre e retorna uma conexao com o banco
    conn= sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  #faz com que cada linha do banco de dados possa ser acessada pelo nome da coluna em vez de por número.
    return conn


def init_db(): #cria a tabela clientes caso ela nao exista
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT,' \
    'nome TEXT NOT NULL,' \
    'email TEXT NOT NULL,' \
    'telefone TEXT NOT NULL)')
    conn.commit()
    conn.close()