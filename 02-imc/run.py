from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form["nome"]
        peso = request.form["peso"].replace(',', '.')  # Trocar vírgula por ponto
        altura = request.form["altura"].replace(',', '.')  # Trocar vírgula por ponto

        try:
            peso = float(peso)
            altura = float(altura)
        except ValueError:
            print("Erro ao converter peso ou altura para float.")
            return redirect("/")  # Redireciona se houver erro

        imc_valor = round(peso / (altura ** 2), 2)  # Cálculo do IMC

        # Determinar o status do IMC
        if imc_valor < 18.5:
            status = "Abaixo do peso"
        elif 18.5 <= imc_valor < 25:
            status = "Peso normal"
        elif 25 <= imc_valor < 30:
            status = "Excesso de peso"
        elif 30 <= imc_valor < 35:
            status = "Obesidade"
        else:
            status = "Obesidade extrema"

        caminho_arquivo = 'models/imc.txt'

        with open(caminho_arquivo, 'a') as arquivo:
            arquivo.write(f"{nome};{peso};{altura};{imc_valor};{status}\n")  # Incluindo IMC e status

        return redirect("/")

    return render_template("index.html")

@app.route("/ver_imc")
def consultar_imc():
    imc_list = []
    caminho_arquivo = 'models/imc.txt'

    try:
        with open(caminho_arquivo, 'r') as arquivo:
            for linha in arquivo:
                item = linha.strip().split(';')
                if len(item) == 5:  # Verificar se há 5 elementos
                    imc_list.append({
                        'nome': item[0],
                        'peso': item[1],
                        'altura': item[2],
                        'imc': round(float(item[3]), 2),  # Convertendo o IMC para float
                        'status': item[4]  # Status do IMC
                    })
                else:
                    print(f"Linha ignorada por estar incompleta: {linha.strip()}")
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    return render_template("ver_imc.html", prod=imc_list)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=True)
 
 