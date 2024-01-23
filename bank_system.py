from flask import Flask, render_template, request

app = Flask(__name__)

class Banco:
    def __init__(self):
        self.saldo = 0
        self.transacoes = []

    def deposito(self, valor):
        if valor < 0:
            return "Não é possível depositar um valor negativo."
        
        self.saldo += valor
        self.transacoes.append(f'Depósito: + ${valor:.2f}')

    def saque(self, valor):
        if valor < 0:
            return "Não é possível sacar um valor negativo."

        if len([t for t in self.transacoes if 'Saque' in t]) >= 3:
            return "Não é possível fazer mais saques hoje. Limite atingido."

        if valor > 500:
            return "Não é possível saques com valor acima de $500,00."
        
        if valor > self.saldo:
            return "Não é possível sacar o dinheiro. Saldo indisponível."

        self.saldo -= valor
        self.transacoes.append(f'Saque: - ${valor:.2f}')

    def extrato(self):
        if not self.transacoes:
            return ["Não foram realizadas movimentações"]
        
        extrato = self.transacoes + [f'Saldo Atual: ${self.saldo:.2f}']
        return extrato

cliente = Banco()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deposito', methods=['POST'])
def deposito():
    valor = float(request.form['valor'])
    cliente.deposito(valor)
    return render_template('index.html', extrato=cliente.extrato())

@app.route('/saque', methods=['POST'])
def saque():
    valor = float(request.form['valor'])
    mensagem = cliente.saque(valor)
    return render_template('index.html', extrato=cliente.extrato(), mensagem=mensagem)

if __name__ == '__main__':
    app.run(debug=True)
