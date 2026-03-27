# Importações do Flask: criação da app, templates, requisições, redirecionamento e mensagens
from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, get_db #importa as funcoes do arquivo database

app = Flask(__name__)
app.secret_key = 'minha_chave' #Ela serve para o Flask assinar as sessões e mensagens flash com segurança

init_db()

@app.route('/')
def index():
    db = get_db() #faz conexão com o banco
    clientes = db.execute('SELECT * FROM clientes ORDER BY id DESC').fetchall() #chama clientes
    db.close() #fecha o db
    return render_template('index.html', clientes=clientes)

@app.route('/novo', methods=['GET', 'POST']) #rota para cadastrar novo cliente
def novo():
    if  request.method == 'POST':
        nome = request.form['nome'].strip()
        email = request.form['email'].strip()
        telefone = request.form['telefone'].strip() #strip remove espacos em branco antes e depois do nome
        if not nome or not telefone or not email :
            flash('Erro. Verique os campos preenchidos', 'erro') # erro e sucesso serve para o HTML saber como estilizar a mensagem
            return render_template('form.html', titulo='Novo Cliente', cliente=None)
        db = get_db() #abre conexao com db
        db.execute('INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)', (nome, email, telefone))
        db.commit() #salva a conexao com db
        db.close()  #fecha conexao com db
        flash('Cliente salvo com sucesso', 'sucesso')
        return redirect(url_for('index')) 
    return render_template('form.html', titulo='Novo Cliente', cliente=None) # retorna o formulário vazio para cadastrar um novo cliente

@app.route('/editar/<int:id>', methods= ['GET', 'POST']) #EDICAO/ update
def editar(id):
    db = get_db() #abre conexao com o banco
    cliente = db.execute( 'SELECT * FROM clientes WHERE id = ?', (id,)).fetchone()
    if not cliente:
        flash('Esse cliente não existe', 'erro')
        return redirect(url_for('index'))
    
    if request.method =='POST':
        nome = request.form['nome'].strip()
        email = request.form['email'].strip()
        telefone = request.form['telefone'].strip()
        if not nome or not telefone or not email:
            flash('Erro', 'erro')
            return render_template('form.html', titulo='Editar Cliente', cliente=cliente)
        db.execute('UPDATE clientes SET nome=?, email=?,telefone=? WHERE id = ?', (nome, email, telefone, id))
        db.commit() #salva
        db.close() #fecha
        flash('Cliente editado com sucesso', 'sucesso')
        return redirect(url_for('index'))
    

    return render_template ('form.html', titulo='Editar Cliente', cliente=cliente) # retorna o formulário de edição com os dados do cliente preenchidos


@app.route('/deletar/<int:id>', methods = ['POST']) #DELETE
def deletar(id):
    db = get_db()
    db.execute('DELETE FROM clientes WHERE  id = ?', (id,)) #TUPLA DE ELEMENTO PRECISA DE VIRGULA
    db.commit()
    db.close()
    flash('Cliente deletado', 'sucesso')
    return redirect(url_for('index')) #retorna o navegador para outra rota e cliente esta deletado

if __name__ == '__main__':
    app.run(debug=True)