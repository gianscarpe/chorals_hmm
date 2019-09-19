from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import os
import main_gui as hmm

app = Flask(__name__)
bootstrap = Bootstrap(app)

testset = None

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

@app.route('/train', methods = ['POST'])
def training():
    if request.method == "POST":
        parameters = request.form
        size = parameters.get("size")
        if size != "all":
            size = int(parameters.get("size"))
        iter = int(parameters.get("n_iter"))
        components = int(parameters.get("n_components"))
        trainset, testset, vocabs = hmm.init(os.path.join(hmm.DATA_DIR, 'music21', 'bach_states_dataset.pkl'), size)
        obs_train, train_lengths = hmm.prepare_dataset(trainset)
        obs_test, test_lengths = hmm.prepare_dataset(testset)
        model = hmm.train(components, iter, len(vocabs), obs_train, train_lengths, size)
        print(model)
    return render_template("train_hmm.html", link="/", flag = True)

@app.route('/test', methods = ['POST'])
def testing():
    if request.method == "POST":
        file = request.files["file"]

    return render_template("train_hmm.html", link="/")
if __name__ == '__main__':
    app.run(debug=True)