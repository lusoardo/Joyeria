from flask import Flask, render_template

app = Flask(__name__)
nombre = "Joyeria"

@app.route('/')
def index():
   return render_template('index.html', nombre=nombre)



if __name__ == '__main__':
   app.run(debug=True)

