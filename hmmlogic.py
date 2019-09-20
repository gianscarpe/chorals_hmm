from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap
import os
import numpy
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

@app.route('/sample', methods = ['POST'])
def sample():
    image = None
    midi = None
    framework = request.form.get('generator_framework')
    if request.method == "POST":
        model_name = request.files['model'].filename
        model = hmm.load_pickle(os.path.join(hmm.MODELS_DIR, 'hmm', model_name))
        image, midi = hmm.generate_sample(model, model_name, framework)
    return render_template("music_generator.html", image = image, link = "/", midi = midi)

@app.route('/train', methods = ['POST'])
def training():
    flag_test = False
    if request.method == "POST":
        parameters = request.form
        framework = parameters.get("framework")
        size = parameters.get("size")
        if size != "all":
            size = int(parameters.get("size"))
        iter = int(parameters.get("n_iter"))
        components = int(parameters.get("n_components"))
        trainset, testset, vocabs = hmm.init(os.path.join(hmm.DATA_DIR, 'music21', 'bach_states_dataset.pkl'), size)
        if framework == "hmml":
            obs_train, train_lengths = hmm.prepare_dataset(trainset)
            obs_vocab = [numpy.array([[i] for i, _ in enumerate(vocabs)]).reshape(-1, 1)]
            train_lengths.insert(0, len(vocabs))
            obs_train = obs_vocab + obs_train
        else:
            obs_train = trainset
            train_lengths = None

        model, name = hmm.train(components, iter, len(vocabs), obs_train, train_lengths, size, framework)
        session['framework'] = framework
        session['model'] = name
        session['size'] = size
        if model is not None:
            flag_test = True

    return render_template("train_hmm.html", link="/", flag = True, flag_test = flag_test)

@app.route('/test', methods = ['POST'])
def testing():
    model_name = session['model'] + '.pkl'
    size = session['size']
    framework = session['framework']
    model = hmm.load_pickle(os.path.join(hmm.MODELS_DIR, 'hmm', model_name))
    if request.method == "POST":
        if request.files['testset'].filename != "":
            pkl = request.files['testset']
            testset = hmm.load_pickle(os.path.join(hmm.DATA_DIR, 'music21', pkl.filename))
        else:
            dataset = hmm.load_pickle(os.path.join(hmm.DATA_DIR, 'music21', 'bach_states_dataset.pkl'))
            testset = dataset[size:]
    if framework == "hmml":
        obs_test, test_lengths = hmm.prepare_dataset(testset)
    else:
        obs_test = testset
    infs, means = hmm.test(model, obs_test, framework)
    return render_template("train_hmm.html", link="/", flag_test = True, infs = infs, means = means)

if __name__ == '__main__':
    app.run(debug=True)