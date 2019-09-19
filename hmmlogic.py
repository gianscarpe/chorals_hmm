from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap
import os
import main_gui as hmm

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = "secret"

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
    flag_test = False
    if request.method == "POST":
        parameters = request.form
        size = parameters.get("size")
        if size != "all":
            size = int(parameters.get("size"))
        iter = int(parameters.get("n_iter"))
        components = int(parameters.get("n_components"))
        trainset, testset, vocabs = hmm.init(os.path.join(hmm.DATA_DIR, 'music21', 'bach_states_dataset.pkl'), size)
        obs_train, train_lengths = hmm.prepare_dataset(trainset)
        model, name = hmm.train(components, iter, len(vocabs), obs_train, train_lengths, size)
        session['model'] = name
        session['size'] = size
        if model is not None:
            flag_test = True

    return render_template("train_hmm.html", link="/", flag = True, flag_test = flag_test)

@app.route('/test', methods = ['POST'])
def testing():
    model_name = session['model'] + '.pkl'
    size = session['size']
    model = hmm.load_pickle(os.path.join(hmm.MODELS_DIR, 'hmm', model_name))
    if request.method == "POST":
        if request.files['testset'].filename != "":
            pkl = request.files['testset']
            testset = hmm.load_pickle(os.path.join(hmm.DATA_DIR, 'music21', pkl.filename))
        else:
            dataset = hmm.load_pickle(os.path.join(hmm.DATA_DIR, 'music21', 'bach_states_dataset.pkl'))
            testset = dataset[size:]

    obs_test, test_lengths = hmm.prepare_dataset(testset)
    infs, means = hmm.test(model, obs_test)
    return render_template("train_hmm.html", link="/", flag_test = True, infs = infs, means = means)

if __name__ == '__main__':
    app.run(debug=True)