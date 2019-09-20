from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap
import os
import numpy
import main_gui as hmm

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = "secret"

@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
def index():
    if request.method == "GET":
        parameters = request.args
        type = parameters.get('hmm_type')
        train = parameters.get('train')
        generate = parameters.get('generate')
        session['type'] = type
        if train == "train":
            result = render_template("train_hmm.html", link = "/", type = type)
        elif generate == "generate":
            result = render_template("music_generator.html", link = "/", type = type)
        else:
            result = render_template("index.html")
    return result

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
    type = session['type']
    framework = request.form.get('generator_framework')
    if request.method == "POST":
        model_name = request.files['model'].filename
        if type == "hmm":
            model = hmm.load_pickle(os.path.join(hmm.MODELS_DIR, 'hmm', model_name))
            image, midi = hmm.generate_sample_hmm(model, model_name, framework)
        else:
            model = hmm.load_pickle(os.path.join(hmm.MODELS_DIR, 'fhmm', model_name))
            image, midi = hmm.generate_sample_fhmm(model, model_name)
    print(image,midi)
    return render_template("music_generator.html", image = image, link = "/", midi = midi)

@app.route('/train', methods = ['POST'])
def training():
    flag_test = False
    if request.method == "POST":
        parameters = request.form
        type = session['type']
        if type == "hmm":
            framework = parameters.get("framework")
            session['framework'] = framework
        else:
            K = int(parameters.get('k_value'))
        size = parameters.get("size")
        if size != "all":
            size = int(parameters.get("size"))
        iter = int(parameters.get("n_iter"))
        components = int(parameters.get("n_components"))

        if type == "hmm":
            trainset, testset, vocabs = hmm.init(os.path.join(hmm.DATA_DIR, 'music21', 'bach_states_dataset.pkl'), size, type)
            if framework == "hmml":
                obs_train, train_lengths = hmm.prepare_dataset(trainset)
                obs_vocab = [numpy.array([[i] for i, _ in enumerate(vocabs)]).reshape(-1, 1)]
                train_lengths.insert(0, len(vocabs))
                obs_train = obs_vocab + obs_train
            else:
                obs_train = trainset
                train_lengths = None
            model, name = hmm.train_hmm(components, iter, len(vocabs), obs_train, train_lengths, size, framework)
        else:
            trainset, testset, vocabs = hmm.init(os.path.join(hmm.DATA_DIR, 'chorales', 'music21', 'chorales_states_dataset.pkl'), size, type)
            D = len(vocabs)
            model, name = hmm.train_fhmm(D, components, K, iter, size, trainset)

        session['model'] = name
        session['size'] = size
        if model is not None:
            flag_test = True

    return render_template("train_hmm.html", link="/", flag = True, flag_test = flag_test, type = type)

@app.route('/test', methods = ['POST'])
def testing():
    model_name = session['model'] + '.pkl'
    size = session['size']
    type = session['type']
    infs = means = result = ""
    if type == "hmm":
        framework = session['framework']
        model = hmm.load_pickle(os.path.join(hmm.MODELS_DIR, 'hmm', model_name))
    else:
        model = hmm.load_pickle(os.path.join(hmm.MODELS_DIR, 'fhmm', model_name))

    if request.method == "POST":
        if request.files['testset'].filename != "":
            pkl = request.files['testset']
            testset = hmm.load_pickle(os.path.join(hmm.DATA_DIR, 'music21', pkl.filename))
        else:
            if type == "hmm":
                dataset = hmm.load_pickle(os.path.join(hmm.DATA_DIR, 'music21', 'bach_states_dataset.pkl'))
                testset = dataset[size:]
            else:
                dataset = hmm.load_pickle(os.path.join(hmm.DATA_DIR, 'chorales', 'music21', 'chorales_states_dataset.pkl'))
                testset = dataset[size:]

    if type == "hmm":
        if framework == "hmml":
            obs_test, test_lengths = hmm.prepare_dataset(testset)
        else:
            obs_test = testset
        infs, means = hmm.test_hmm(model, obs_test, framework)
    else:
        result = hmm.test_fhmm(model, testset)

    return render_template("train_hmm.html", link="/", flag_test = True, infs = infs, means = means, result = result, type = type)

if __name__ == '__main__':
    app.run(debug=True)