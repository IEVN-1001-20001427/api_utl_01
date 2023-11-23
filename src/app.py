from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def index():
    title = 'IEVN-1001'
    list = ['juan', 'fulanito', 'menganito']
    return render_template('index.html', title=title, list=list)

@app.route('/uno')
def uno():
    return render_template('uno.html')

@app.route('/dos')
def dos():
    return render_template('dos.html')

@app.route('/hola')
def hola():
    return '<h1>server say HI</h1>'

@app.route('/user/<string:user>')
def user(user):
    return "el usuario es: {}".format(user)

@app.route('/numero/<int:n1>')
def numero(n1):
    return "el numero es: {}".format(n1)

@app.route('/user/<string:nom>/<int:id>')
def doublevariable(nom, id):
    return "<h1>el usuario es: {}, su id es: {}</h1>".format(nom, id)

@app.route('/numero/<float:n2>/<float:n3>')
def suma(n2,n3):
    return "la suma es es: {}".format(n2+n3)

@app.route('/default')
@app.route('/default/<string:nm>')
def default(nm = '404 err'):
    return "<h1>Default {}</h1>".format(nm)

if __name__ == "__main__":
    app.run(debug=True)