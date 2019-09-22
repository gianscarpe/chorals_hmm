# Bach Chorales
## Introduction
We implemented a fully functional framework to test temporal probabilistic 
model for prediction and sample of music. 
We compared HMM and FHMM, 
using various library and trying with different hyper-parameters. 



## Dependencies
Packages needed to play MIDI song:

* timidity: `sudo apt install timidity`
* fluid-soundfont-gm: `sudo apt install fluid-soundfont-gm`

To play a song run `timidity -Os filename.mid`

Packages needed to show scores:

* musescore: `sudo apt install musescore`

You can install instantiate a virtual environemnt of the project using 
`conda env create --file=environment.yml`

## Usage

### Parser
You can parse a new dataset using `python parse.py`. The script generates a new 
parsed dataset and the corresponding vocabulary.


Arguments:
``` 
--path: path to the dataset directory
--to-states: parse dataset to a list of state integers
``` 
### HHM

You can train a FHMM model using `python main_fhmm.py` 
HMM arguments:
``` 
-M: numeber of chains
-K: dimension of states alphabet
-N: number of iterations
 ``` 
Dataset arguments:
 ```
 --dataset-dir: path to dataset directory
 --trainset-name: name of the dataset of training
  --trainset-size: ['all', int_value] split train/test
 --testset-name: name of the dataset of test

  ```
  arguments for training process:
 ```
 -F: framework: pom (pomegranate) or hmml (hmmlearn)
 --tol: Set the convergence tolerance
 -v: training verbose
 -s: save the model
  
```
arguments for testing process:
  ```
 --generate: generate a song using the current model 
 --skip-training: skip the training process 
    (model-path is mandatory)
 --model-path: path to a model to load
```


### FHHM

You can train a FHMM model using `python main_fhmm.py` 
FHMM arguments:
``` 
-M: numeber of chains
-K: dimension of states alphabet
-N: number of iterations
 ``` 
Dataset arguments:
 ```
 --dataset-dir: path to dataset directory
 --trainset-name: name of the dataset of training
  --trainset-size: ['all', int_value] split train/test
 --testset-name: name of the dataset of test

  ```
  arguments for training process:
 ```
 -v: training verbose
 -s: save the model
  
```
arguments for testing process:
  ```
 --generate: generate a song using the current model 
 --skip-training: skip the training process 
    (model-path is mandatory)
 --model-path: path to a model to load
```

### GUI
You can launch a GUI of the project using your favourite WSGI HTTP Server.

Gunicorn example:
  ```
gunicorn app:app.py
  ```

## Report
You can find complete report of the project at 
`relazione/Scarpellini_Belotti_Samotti_relazione.pdf` (Italian Only)


## LICENSE

Learning porpous only - no guarantee or assistance is provided.
Please respect the license and cite us.
``` 
You can find us at:

@gianscarpe: gianluca[at]scarpellini.cloud
@belerico: f.belotti8[at]campus.unimib.it or belo.fede[at]outlook.com
``` 
