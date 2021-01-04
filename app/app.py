from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def root():
    return "<h1>Lukas Rieger's Cloud DevOps Engineer Capstone Project!</h1>"


@app.route('/new')
def new():
    return "<h1>This is another endpoint.</h1>"


@app.route('/add', methods=['GET'])
def add():
    try:
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
    except ValueError:
        return "<h3>Invalid input</h3>"

    result = a + b
    return jsonify(result)


@app.route('/mult', methods=['GET'])
def mult():
    try:
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
    except ValueError:
        return "<h3>Invalid input</h3>"

    result = a * b
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)