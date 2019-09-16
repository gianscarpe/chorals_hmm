from flask import Flask, render_template, send_from_directory
from flask_bootstrap import Bootstrap
#import main_hmm

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", link1 = "/music_generator", link2 = "/train_hmm")

@app.route('/train_hmm')
def train_hmm():
    return render_template("train_hmm.html", link = "/")

@app.route('/music_generator')
def music_generator():
    return render_template("music_generator.html", link = "/")

@app.route('/sample')
def sample():
    print("Call function")
    midi = "static/generated_hmm_60_10_200.mid"
    return render_template("music_generator.html", image = "static/image.png", link = "/", midi = midi)

if __name__ == '__main__':
    app.run(debug=True)