# Machine Learning-Model, which was created here: https://github.com/sherjilozair/char-rnn-tensorflow
# Script is used in this prototype in a modified state, so it is only loaded once upon game start and can therefor farely quickly generate new text
#!/usr/bin/env python

from __future__ import print_function

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
from six.moves import cPickle


from six import text_type

import tensorflow as tf
from model import Model

save_dir = 'save'
with open(os.path.join(save_dir, 'config.pkl'), 'rb') as f:
    saved_args = cPickle.load(f)
with open(os.path.join(save_dir, 'chars_vocab.pkl'), 'rb') as f:
    chars, vocab = cPickle.load(f)
model = Model(saved_args, training=False)

def sample(nrchars = 360, prime = u'', sample = 1.2):

    #Use most frequent char if no prime is given
    if prime == '':
        prime = chars[0]
    
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state(save_dir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            data = model.sample(sess, chars, vocab, nrchars, prime,
                               sample).encode('utf-8')
            return data.decode("utf-8")


