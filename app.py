#IMPORTS FLASK
from flask import Flask, render_template, request
#IMPORTS ML
import joblib
import pandas as pd

app = Flask(__name__)
#Necessário para o funcionamento da ML
model = joblib.load(open("models/obesidade.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return render_template("entrada.html")
    else:
        return render_template("entrada.html")
@app.route("/resposta", methods=["POST"])
def resposta():
    genero = request.form["gênero"]
    idade = float(request.form["idade"].replace(',', '.'))
    altura = float(request.form["altura"].replace(',', '.'))
    peso = float(request.form["peso"].replace(',', '.'))
    historico = request.form["histórico"]
    favc = request.form["FAVC"]
    fcvc = float(request.form["FCVC"].replace(',', '.'))
    ncp = float(request.form["NCP"].replace(',', '.'))
    caec = request.form["CAEC"]
    fumo = request.form["fumo"]
    ch2o = float(request.form["CH2O"].replace(',', '.'))
    scc = request.form["SCC"]
    faf = float(request.form["FAF"].replace(',', '.'))
    tue = float(request.form["TUE"].replace(',', '.'))
    calc = request.form["CALC"]
    mtrans = request.form["MTRANS"]

    #Fazendo uso da ML
    #Criando um DataFrame com os novos dados
    novos_dados = pd.DataFrame([[genero, idade, altura, peso, historico, favc, fcvc, ncp, caec, fumo, ch2o, scc, faf, tue, calc, mtrans]],
                                    columns=['Gender', 'Age', 'Height', 'Weight', 'family_history_with_overweight', 'FAVC', 'FCVC', 'NCP',
                                             'CAEC', 'SMOKE', 'CH2O', 'SCC', 'FAF', 'TUE', 'CALC', 'MTRANS'])
    #Fazendo previsões nos novos dados
    prediction = model.predict(novos_dados)

    return render_template("saída.html", gênero=genero,
                           idade=int(idade),
                           altura=str(altura).replace('.', ','),
                           peso=str(peso).replace('.', ','),
                           histórico=historico,
                           FAVC=favc,
                           FCVC=int(fcvc),
                           NCP=int(ncp),
                           CAEC=caec,
                           fumo=fumo,
                           CH2O=int(ch2o),
                           SCC=scc,
                           FAF=int(faf),
                           TUE=int(tue),
                           CALC=calc,
                           MTRANS=mtrans,
                           prediction=prediction)
@app.route("/exemplo")
def exemplo():
    return render_template("exemplo.html")

if __name__ == "__main__":
    app.run(debug=True)