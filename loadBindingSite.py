__author__ = 'Jichen Yang'
"""
This script is what created the dataset pickled.

1) You need to have a folder named "Xmers" including all sampled x-mers as negative cases.

2) positive cases: binding sites. Under "bindingsites" folder. As an example, file 'loadBindingSite/binding_sites_CDX2'
looks like:
>hg19_chr6:165505065-165505075(+)
aaGAGCAATAAACtg
>hg19_chr6:165505089-165505099(+)
ggGAGCCATAAAAgt
>hg19_chr1:17923770-17923780(-)
aaGAGCCATAAAAac
According to the length of binding site, this script will try to find negative x-mers with the same length.

3) Then run this script.
"""

import numpy
import random
import pickle as pkl
from collections import OrderedDict
import glob
import os

def build_dict():
    '''
    :param N_nucleotide: default number of typies of nucleotide is 4
    :return: dict
    '''
    print('Building a simple dictionary..')
    worddict={'a':2,'c':3,'g':4,'t':5}
    return worddict

def grab_bindingsites(path, dictionary):
    '''
    :param path: path to binding site
    :param dictionary: dictionary
    :return: a list seqs[]
    '''
    sentences = []
    currdir = os.getcwd()
    os.chdir(currdir+path)
    #os.chdir(currdir+'\\loadBindingSite\\bindingsites\\')
    for ff in glob.glob("binding_sites*"):
        with open(ff, 'r') as f:
            for line in f.readlines():
                if not line.startswith('>'):
                    sentences.append(list(line.strip().lower()))
    os.chdir(currdir)
    seqs = [None] * len(sentences)
    for idx, ss in enumerate(sentences):
        seqs[idx] = [dictionary[w] if w in dictionary else 1 for w in ss]
    return seqs

def grab_xmers(path,length,dictionary):
    '''
    :param path: path to binding site
    :param length: the length of correspond positive case (binding site)
    :param dictionary: dictionary
    :return: a list seqs[]
    '''
    sentences = []
    currdir = os.getcwd()
    os.chdir(currdir+path)
    #os.chdir(currdir+'\\loadBindingSite\\Xmers\\')
    for ff in glob.glob(length.__str__()+"*"):
        with open(ff, 'r') as f:
            for line in f.readlines():
                sentences.append(list(line.strip().lower()))
    os.chdir(currdir)
    seqs = [None] * len(sentences)
    for idx, ss in enumerate(sentences):
        seqs[idx] = [dictionary[w] if w in dictionary else 1 for w in ss]
    return seqs

def main():
    path = ''
    dictionary = build_dict()
    for folder in os.listdir("./bindingsites"):
        print("working on "+folder+"...")
        train_x_pos = grab_bindingsites(path+'/bindingsites/'+folder, dictionary)
        bindingsitelength=len(train_x_pos[0])
        train_x_neg = grab_xmers(path+'/Xmers',bindingsitelength,dictionary)
        if(len(train_x_neg)>10000):
            train_x_neg=train_x_neg[:10000]
        train_x = train_x_pos + train_x_neg
        train_y = [1] * len(train_x_pos) + [0] * len(train_x_neg)

        n_samples = len(train_x)
        sidx = numpy.random.permutation(n_samples)
        n_train= int(numpy.round(n_samples * (1. - 0.2)))

        test_set_x = [train_x[s] for s in sidx[n_train:]]
        test_set_y = [train_y[s] for s in sidx[n_train:]]
        train_set_x = [train_x[s] for s in sidx[:n_train]]
        train_set_y = [train_y[s] for s in sidx[:n_train]]

        f = open(os.getcwd()+path+'/bindingsitespkl/'+folder+'_bindingsites.pkl', 'wb')
        pkl.dump((train_set_x, train_set_y), f, -1)
        pkl.dump((test_set_x, test_set_y), f, -1)
        f.close()

    f = open('TFbinding.dict.pkl', 'wb')
    pkl.dump(dictionary, f, -1)
    f.close()

if __name__ == '__main__':
    numpy.random.seed(seed=20160416)
    random.seed(20160416)
    main()

















