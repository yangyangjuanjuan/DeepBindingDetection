__author__ = 'Jichen Yang'
"""
This script is to evaluate the TF binding sites performance
between lstm and tranditional PWM method

Evaluation will be done in two situations: 1) negative seqs 
were randomly sampled from the whole NBNCLS; 2) a part of 
negative seqs were selected that they got HIGH PWM score. The
first situation is ok but a small part of sampled negative 
cases (by comparing to the whole genome) may not well reflect
the problem and both methods can give very high PPV. The second
situation is designed that PWM method will give some FP, then
compare the performance.
"""

import six.moves.cPickle as pickle
import matplotlib.pyplot as plt
import os
import glob
import numpy
import random

def build_dict():
	'''
	:param N_nucleotide: default number of typies of nucleotide is 4
	:return: dict
	'''
	print('Building a simple dictionary..')
	worddict={'a':2,'c':3,'g':4,'t':5}
	return worddict

def load_test_seqs(path="./bindingsitespkl_highscorenegative", TF="Ar"):
	'''
	:param path: path to testing sequences
	:param TF: name of TF
	'''
	print("loading testing seqs from "+path)
	pklfile = path+'/'+TF+"_bindingsites.pkl"
	f = open(pklfile, 'rb')
	train_set = pickle.load(f)
	test_set = pickle.load(f)
	f.close()
	test_set_x, test_set_y = test_set
	return test_set_x, test_set_y

def load_PWM(path="./BSPHighPWMScoreNonBinding/PWM", TF="Ar"):
	'''
	:param path: path to PWM
	:param TF: name of TF
	'''
	print("loading PWM...")
	PWMfile = path+'/PWM_'+TF+".csv"
	PWM=[]
	with open(PWMfile, 'r') as f:
		for line in f.readlines():
			PWM.append(float(line))
	return PWM

def grab_xmers(path,length,dictionary):
	'''
	this step is necessary to determine cutoff of PWM method
	:param path: path to binding site
	:param length: the length of correspond positive case (binding site)
	:param dictionary: dictionary
	:return: a list seqs[]
	'''
	sentences = []
	currdir = os.getcwd()
	os.chdir(currdir+path)
	for ff in glob.glob(length.__str__()+"*"):
		with open(ff, 'r') as f:
			for line in f.readlines():
				sentences.append(list(line.strip().lower()))
	os.chdir(currdir)
	seqs = [None] * len(sentences)
	for idx, ss in enumerate(sentences):
		seqs[idx] = [dictionary[w] if w in dictionary else 1 for w in ss]
	return seqs

def get_PWMscore(seqs,PWM):
	'''
	Use PWM to get score for given seqs list
	:param seqs: sequence list
	:param PWM: given PWM
	:return: a list PWMscores[]
	'''
	seq_len = len(seqs[0])
	seq_PWMscore = [0] * len(seqs)
	for idx, ss in enumerate(seqs):
		for idx2, c in enumerate(ss):
			seq_PWMscore[idx] += PWM[(c-2)*seq_len + idx2]
	return seq_PWMscore


def show_hist(seq_PWMscore):
	'''
	Show hist to check PWM score distribution
	'''
	plt.hist(seq_PWMscore)
	plt.title("seqs PWM scores")
	plt.xlabel("Value")
	plt.ylabel("Frequency")
	plt.show()
	return

def evaluate(PWMscores,seqs_class,PWM_cutoff):
	'''
	Evaluate the performance
	'''
	TP=0;TN=0;FP=0;FN=0;PPV=-1.0
	for idx, score in enumerate(PWMscores):
		if score>PWM_cutoff and seqs_class[idx]==1:
			TP+=1
		elif score>PWM_cutoff and seqs_class[idx]==0:
			FP+=1
		elif score<PWM_cutoff and seqs_class[idx]==1:
			FN+=1
		elif score<PWM_cutoff and seqs_class[idx]==0:
			TN+=1
	if (TP+FP)>0:
		PPV=float(TP)/(TP+FP)
	return [TP,TN,FP,FN,PPV]

def example():
	dictionary = build_dict()
	seqs_test,seqs_class =load_test_seqs()
	numpy.array(seqs_class).sum()
	seq_len = len(seqs_test[0])
	seq_nonbinding = grab_xmers(path='/Xmers', length=seq_len,dictionary=dictionary)
	seq_PWM = load_PWM()
	seq_PWMscore = get_PWMscore(seq_nonbinding,seq_PWM)
	## show_hist(seq_PWMscore)
	PWM_cutoff = numpy.percentile(seq_PWMscore, 99.98)
	seq_testscore = get_PWMscore(seqs_test,seq_PWM)
	## show_hist(seq_testscore)
	TP,TN,FP,FN,PPV = evaluate(seq_testscore,seqs_class,PWM_cutoff)
	ACC = float(TP+TN)/(TP+FP+FN+TN)
	print('PPV: ', PPV, '; Accuracy:', ACC)

if __name__ == '__main__':
	numpy.random.seed(seed=20160416)
	dictionary = build_dict()
	random.seed(20160416)
	tosave=[]
	for TF in os.listdir("./bindingsites"):
		print("evaluating PWM method for "+TF)
		seqs_test,seqs_class =load_test_seqs(path="./bindingsitespkl_highscorenegative", TF=TF)
		print("number of positive test seqs: ", numpy.array(seqs_class).sum())
		print("total number of test seqs: ", len(seqs_class))
		seq_len = len(seqs_test[0])
		seq_nonbinding = grab_xmers(path='/Xmers', length=seq_len,dictionary=dictionary)
		seq_PWM = load_PWM(path="./BSPHighPWMScoreNonBinding/PWM", TF=TF)
		seq_PWMscore = get_PWMscore(seq_nonbinding,seq_PWM)
		## show_hist(seq_PWMscore)
		PWM_cutoff = numpy.percentile(seq_PWMscore, 99.98)
		print('PWM cutoff: ',PWM_cutoff)
		seq_testscore = get_PWMscore(seqs_test,seq_PWM)
		## show_hist(seq_testscore)
		TP,TN,FP,FN,PPV = evaluate(seq_testscore,seqs_class,PWM_cutoff)
		ACC = float(TP+TN)/(TP+FP+FN+TN)
		print('TP: ', TP, '; TN:', TN, '; FP:', FP, '; FN:', FN)
		print('PPV: ', PPV, '; Accuracy:', ACC)
		tosave.append([len(seqs_class),TP, TN, FP, FN, PPV, TF, PWM_cutoff])
	numpy.savez('./saves_PWMresult/PWMresults.npz', TF_stats=tosave)
