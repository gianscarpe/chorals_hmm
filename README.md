# Bach Chorales

##Usage

Scriviamo come si usa il main

##HMM
```
```

## FHMM

```

params = {
    'hidden_alphabet_size': K,
    'n_hidden_chains': M,
    'observed_alphabet_size': D,
    'n_observed_chains': 1,
}

```

Packages needed to play MIDI song:

* timidity: `sudo apt install timidity`
* fluid-soundfont-gm: `sudo apt install fluid-soundfont-gm`

To play a song run `timidity -Os filename.mid`

Packages needed to show scores:

* musescore: `sudo apt install musescore`

Primi results:  
**HMM m21 40 stati : 200       -3032.9579          +0.1118**  
#infs bach 137 on 335-length  
AVG bach: -584.5778445063416  

#infs beethoven 15 on 15-length  
AVG beethoven: -inf  

#infs mozart 15 on 15-length  
AVG mozart: -inf  

