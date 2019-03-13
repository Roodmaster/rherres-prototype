# RHerres-Prototype

## CharlesBottens_

This is the prototype for my Bachelor Thesis.

It was build and tested on Python 3.68 and Tensorflow 1.12 (GPU) and all required dependencies.

It also runs on Tensorflow 1.13, but will throw Warning Messages, due to changes that will be made for Tensorflow 2.0.
So one can assume that it won't work with Tensorflow 2.0 anymore.

Credit to https://github.com/sherjilozair/char-rnn-tensorflow which I used as my ML-model.


## Installation

It's recommended to setup a virtual environment to install the dependencies without interfering with your normal setup. 
(I recommend using Anaconda https://www.anaconda.com/distribution/). 

After downloading and installing Anaconda, you want to setup a virtual environment. Open your terminal or shell:

- conda create -n yourenvname python=3.6 anaconda

You can then activate the virtual environment:

- source activate yourenvname

Install tensorflow into your virtual environment:

- conda install -n yourenvname tensorflow=1.12

After installation is finished, run game.py (in your virtual environment):

- python game.py

To deactivate the virtual environment:

- conda deactivate

## Tipps

If you have other Python-Versions installed or are on a Mac, you might have to use "python3" and "pip3" when using those commands outside of your virtual environment.