'''
Build a classifier for descriminating TF binding sites
'''

from __future__ import print_function
import numpy

from keras.preprocessing import sequence
from keras.models import Model
from keras.layers import Dense, Dropout, Embedding, LSTM, Input, merge

import six.moves.cPickle as pickle

import sys
import time
import os

import numpy
import random

import bindingsites

datasets = {'bindingsites': (bindingsites.load_data, bindingsites.prepare_data)}
def get_dataset(name):
    return datasets[name][0], datasets[name][1]

# Set the random number generators' seeds for consistency
SEED = 123
numpy.random.seed(SEED)


if __name__ == '__main__':
    numpy.random.seed(seed=20160416)
    random.seed(20160416)
    maxlen=100
    n_words=10000  # Vocabulary size
    batch_size=16
    test_size=-1
    for TF in os.listdir("./bindingsites")[0:1]:
        print("modelling for TF "+TF)
        datafile='./bindingsitespkl_highscorenegative/'+TF+'_bindingsites.pkl'
        load_data, prepare_data = get_dataset('bindingsites')
        print('Loading data')
        train, valid, test = load_data(path=datafile,n_words=n_words, 
            valid_portion=0.0, maxlen=maxlen)
        if test_size > 0:
            idx = numpy.arange(len(test[0]))
            numpy.random.shuffle(idx)
            idx = idx[:test_size]
            test = ([test[0][n] for n in idx], [test[1][n] for n in idx])
        print('Building model')
        (X_train, y_train)= train
        (X_test, y_test)= test
        X_train = sequence.pad_sequences(X_train, maxlen=maxlen)
        X_test = sequence.pad_sequences(X_test, maxlen=maxlen)
        print(len(X_train), 'train sequences')
        print(len(X_test), 'test sequences')
        y_train = numpy.array(y_train)
        y_test = numpy.array(y_test)

        sequence = Input(shape=(maxlen,), dtype='int32')
        ## The input of LSTM must have the shape (nb_samples, timesteps, features)
        embeded=Embedding(10, 8, input_length=maxlen)(sequence)
        forwards = LSTM(64)(embeded)
        backwards = LSTM(64, go_backwards=True)(embeded)

        merged = merge([forwards, backwards], mode='concat', concat_axis=-1)
        after_dp = Dropout(0.25)(merged)
        output = Dense(1, activation='sigmoid')(after_dp)

        model = Model(input=sequence, output=output)

        model.compile('adam', 'binary_crossentropy', metrics=['accuracy'])
        print('Train...')
        model.fit(X_train,y_train,
            batch_size=batch_size,
            nb_epoch=3,
            validation_data=[X_test, y_test])
