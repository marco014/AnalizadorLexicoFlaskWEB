from flask import Flask, request, render_template, flash
import lexer
import logging

app = Flask(__name__)
app.secret_key = 'clave_secreta_aleatoria'
logging.basicConfig(level=logging.DEBUG)


@app.route('/', methods=['GET', 'POST'])
def index():
    tokens = []
    codigo = ""
    file_name = ""

    if request.method == 'POST':
        logging.debug("Received POST request")

        # Manejar archivos cargados
        if 'file' in request.files and request.files['file']:
            file = request.files['file']
            file_name = file.filename
            codigo = file.read().decode('utf-8')
            logging.debug(f"Code from file: {codigo}")
            flash(f'Archivo "{file_name}" subido correctamente. El código se ha cargado.')
        elif 'codigo' in request.form and request.form['codigo']:
            codigo = request.form['codigo']
            logging.debug(f"Code from textarea: {codigo}")

        # Revisar si se seleccionó el botón "Analizar código"
        if 'analizar' in request.form:
            lexer.lexer.input(codigo)

            line_number = 1
            while True:
                tok = lexer.lexer.token()
                if not tok:
                    break

                if tok.type in lexer.reserved.values():
                    token_type = f"<Reservada {tok.type.title()}>"
                elif tok.type == 'LPAREN':
                    token_type = "<Paréntesis de apertura>"
                elif tok.type == 'RPAREN':
                    token_type = "<Paréntesis de cierre>"
                else:
                    token_type = tok.type

                tokens.append((f"Línea {line_number}", token_type, tok.value))
                logging.debug(f"Token: {tok}")

                line_number += 1

    return render_template('index.html', codigo=codigo, tokens=tokens, file_name=file_name)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
