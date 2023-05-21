import json
import pandas as pd
from sweetify import sweetify
from flask import Flask, render_template, request, url_for, redirect, jsonify, flash

dataset_api = pd.read_csv('insumos_farmaceuticos.csv')
print(dataset_api.columns)
app = Flask(__name__)


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
def pegar_api(json=json):
    dataset = {'nome_substancia': json.dumps(dataset_api['nome'].to_list()),
               'classe_bio_farm': json.dumps(dataset_api['cls_biofarm'].to_list())}
    return jsonify(dataset)


app.run(host='0.0.0.0', port=8080)
