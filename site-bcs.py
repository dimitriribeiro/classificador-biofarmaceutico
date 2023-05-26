import os
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for, redirect, jsonify, flash

load_dotenv()


#carregando base de dados de base
dataset_api = pd.read_csv('insumos_farmaceuticos.csv')


app = Flask(__name__)

#criando conexao de banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
db = SQLAlchemy(app)


class Subs:
    def __init__(self, nome, referencia, cls_terap, solubilidade, cls_biofarm):
        self.nome = nome
        self.referencia = referencia
        self.cls_terap = cls_terap
        self.solubilidade = solubilidade
        self.cls_biofarm = cls_biofarm

        self.lista = [self.nome, self.referencia, self.cls_terap, self.solubilidade, self.cls_biofarm]

    def __getitem__(self, item):
        return self.lista[item]

@app.route('/')
def bem_vindo():
    return render_template('bem-vindo.html')

@app.route('/irparaosite')
def irparaosite():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html', titulo_head='SCB - API Helper')


@app.route('/cadastrar')
def novo():
    etiquetas = ['nome', 'referência', 'classe terapêutica', 'solubilidade', 'classificação biofarmacêutica']
    return render_template('cadastro.html', titulo='Requisiçao de Cadastro', labels_forms=etiquetas)

@app.route('/solicitacao', methods=['POST', ])
def solicitar():
    global dataset_api

    nome = request.form['nome'].title()
    referencia = request.form['referência']
    cls_terap = request.form['classe terapêutica']
    solubilidade = request.form['solubilidade']
    cls_biofarm = request.form['classificação biofarmacêutica']

    substancia = Subs(nome, referencia, cls_terap, solubilidade, cls_biofarm)
    try:
        nova_linha = {
            'nome': substancia.nome,
            'referencia': substancia.referencia,
            'cls_terap': substancia.cls_terap,
            'solubilidade': substancia.solubilidade,
            'cls_biofarm': substancia.cls_biofarm
        }
        novo_dataset = dataset_api.append(nova_linha, ignore_index=True)
        novo_dataset.to_csv('insumos_farmaceuticos.csv', index=False)
        return redirect('/')
    except:
        return redirect('/alerta')


@app.route('/alerta')
def alerta():
    return redirect('/cadastrar')


@app.route('/apiclassificacaobiofarm')
def pegar_api():
    global dataset_api
    data_json = dataset_api.to_json(orient='records', force_ascii=False)
    return data_json


app.run(debug=True, host='0.0.0.0', port=8080)
