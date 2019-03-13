# RHerres-Prototype

## CharlesBottens_

This is a Python text adventure and the prototype for my bachelor thesis "CharlesBottens". 

It was build and tested on Python 3.68 and Tensorflow 1.12 (GPU) and all their dependencies. 

If you simply want to run the game, the CPU version of Tensorflow will suffice.

Using Tensorflow 1.12 (GPU) requires a NVIDIA graphics card as well as CUDA 9.0.

The game also runs on Tensorflow 1.13, but might throw Warning-Messages your way, due to changes that will be made for Tensorflow 2.0. So one can assume that it won't work with Tensorflow 2.0 anymore.

- Thanks to Phillip Johnson and his book: "Make Your Own Python Text Adventure" (2018).
- Credit to https://github.com/sherjilozair/char-rnn-tensorflow. I used his ML-model in my prototype.


## Installation

It's recommended to setup a virtual environment to install the dependencies without interfering with your normal setup, since Tensorflow 1.12 (and 1.13) require Python versions 3.4, 3.5 or 3.6.

If you use one of those Python versions, open your terminal and move to the right directory (cd path/to/RHerres-Prototype). 

Install the requirements:

- pip install -r requirements.txt

And start the game:

- python game.py


If you are using a different version of Python, I can recommend Anaconda (https://www.anaconda.com/distribution/) or Virtualenv (https://virtualenv.pypa.io/en/stable/) to setup a virtual environment where you can safely install Python 3.6x into. 

I'll use Anaconda as an example. After installing Anaconda, open your terminal, shell or Anaconda-Prompt (Windows).

* With a command line tool open, type the following:

- conda create -n yourenvname python=3.6 anaconda


* Install tensorflow into your virtual environment:

- conda install -n yourenvname tensorflow=1.12


* You can then activate the virtual environment:

- source activate yourenvname


* After installation is finished, run game.py (in your virtual environment):

- python game.py


* To deactivate the virtual environment:

- conda deactivate

## Tipps

If you have other Python versions installed or are on a Mac, you might have to use "python3" and "pip3" when using those commands outside of your virtual environment.

If you don't want to use Anaconda, here is an installation guideline from Tensorflow, which uses a Python-Installer, Pip and Virtualenv: https://www.tensorflow.org/install/pip

If you use a Windows-Machine, starting the Anaconda-Prompt in admin mode might work better.