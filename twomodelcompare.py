__author__ = 'Jichen Yang'
"""
This script is to load saved TF binding sites predictions by
LSTM method.
"""

import six.moves.cPickle as pickle
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import os
import glob
import numpy
import random

def load_saves(path="./saves_highPWMscore", TF="example"):
	'''
	:param path: path to folder saving all results from LSTM
	:param TF: name of TF
	'''
	print("loading LSTM results for "+TF)
	savedfile = path+'/lstm_'+TF+".npz"
	with numpy.load(savedfile) as data:
		records=data['records']
		records=records.tolist()
		print("Have "+str(len(records))+" data points (TFs).")
	return records

def load_saves_LSTM(path="../loadBindingSite/saves_highPWMscore", TF="FOS"):
	'''
	:param path: path to folder saving all results from LSTM
	:param TF: name of TF
	'''
	print("loading LSTM results for "+TF)
	savedfile = path+'/lstm_'+TF+".npz"
	with numpy.load(savedfile) as data:
		history_errs=data['history_errs']
		history_stats=data['history_stats']
		print("Have "+str(history_stats.shape[0])+" data points.")
	return history_errs,history_stats

def compute_ACC(TP,TN,FP,FN):
	return (float(TP)+float(TN))/(float(TP)+float(TN)+float(FP)+float(FN))

def load_PWMsaves(path="./saves_PWMresult/PWMresults.npz"):
	'''
	:param path: path to folder saving all results from LSTM
	:param TF: name of TF
	'''
	print("loading PWM results...")
	savedfile = path
	with numpy.load(savedfile) as data:
		TF_stats=data['TF_stats']
		print("Have "+str(TF_stats.shape[0])+" TF results avaliable.")
	return TF_stats

def compute_ACC(TP,TN,FP,FN):
	return (float(TP)+float(TN))/(float(TP)+float(TN)+float(FP)+float(FN))

if __name__ == '__main__':
	numpy.random.seed(seed=20160416)
	random.seed(20160416)
	allTF = ['FOS', 'STAT1', 'JUNB', 'POU2F2', 'RFX5', 'Egr1', 'IRF1', 'CEBPA', 'JUND', 'EBF1', 'TFAP2C', 'CDX2', 'NRF1', 'NFYA', 'Stat3', 'TP53', 'EHF', 'NFE2_MAF', 'FLI1', 'ELF1', 'RUNX2', 'ELK4', 'GATA2', 'YY1', 'FOXP2', 'TP63', 'ZNF263', 'SMAD2_SMAD3_SM', 'USF2', 'MAFK', 'PRDM1', 'MEF2A', 'E2F4', 'FOSL2', 'E2F1', 'ZBTB33', 'HSF1', 'MAFF', 'FOXP1', 'GATA3', 'SRF', 'TFAP2A', 'JUN', 'NR2C2', 'Ar', 'JUN (var.2)', 'FOXH1', 'MAX', 'E2F6', 'KLF5', 'REST', 'NFKB1', 'SP1', 'TCF7L2', 'MEF2C', 'FOXA1', 'BATF_JUN', 'CEBPB', 'HNF4A', 'JUND (var.2)', 'SP2', 'ESR1', 'USF1', 'NFYB', 'ESRRA', 'Pax5', 'RFX2', 'ZEB1', 'STAT2_STAT1', 'HNF4G', 'ESR2', 'FOSL1', 'DUX4']
	TF_stats=load_PWMsaves()
	idx=numpy.arange(len(TF_stats))
	TF_stats_names=[TF_stats[n][6] for n in idx]

	pdf = matplotlib.backends.backend_pdf.PdfPages("./plots/PWM_results.pdf")
	totalN =[TF_stats[n][0] for n in idx]
	totalN = [int(n) for n in totalN]
	plt.figure()
	plt.hist(totalN,20,facecolor='green',alpha=0.5)
	plt.title("Hist. for number of TF testing seqs")
	plt.ylabel("Frequency")
	plt.savefig(pdf, format='pdf')

	allPPV=[TF_stats[n][5] for n in idx]
	allPWMcutoff=[TF_stats[n][7] for n in idx]
	allPPV = [float(n) for n in allPPV]
	allPWMcutoff = [float(n) for n in allPWMcutoff]
	plt.figure()
	plt.hist(allPPV,20,facecolor='green',alpha=0.5)
	plt.title("Hist. for PWM PPV of all TFs")
	plt.ylabel("Frequency")
	plt.savefig(pdf, format='pdf')
	plt.figure()
	plt.hist(allPWMcutoff,20,facecolor='green',alpha=0.5)
	plt.title("Hist. for PWM cutoff of all TFs")
	plt.ylabel("Frequency")
	plt.savefig(pdf, format='pdf')

	pdf.close()

	pdf = matplotlib.backends.backend_pdf.PdfPages("./plots/twomodels_compare2.pdf")
	records=load_saves(TF="1to26")
	TFs=records.keys()
	print(TFs)
	for TF in allTF[:26]:
		## PWM method
		## for history_stats, it saves [TotalN, TP, TN, FP, FN, PPV (for train), TotalN, TP, TN, FP, FN, PPV (for valid), TotalN, TP, TN, FP, FN, PPV (for test)]
		idx_in_PWMresults=TF_stats_names.index(TF)
		PPV_PWM=allPPV[idx_in_PWMresults]
		ACC_PWM=(float(TF_stats[idx_in_PWMresults][1]) + float(TF_stats[idx_in_PWMresults][2]))/(float(TF_stats[idx_in_PWMresults][1]) + float(TF_stats[idx_in_PWMresults][2]) + float(TF_stats[idx_in_PWMresults][3]) + float(TF_stats[idx_in_PWMresults][4]))

		## error curve
		idx=numpy.arange(len(records[TF]['val_loss']))
		test_errs=records[TF]['val_loss']
		plt.figure()
		plt.plot(idx, test_errs, 'bo', idx, test_errs, 'k')
		plt.title("Test errs for "+TF)
		plt.xlabel("save points")
		plt.savefig(pdf, format='pdf')

		## PPV is not avaliable at this time
		# test_PPVs=[history_stats[n][17] for n in idx]
		# fig = plt.figure()
		# ax = fig.add_subplot(111)
		# plt.plot(idx, test_PPVs, 'bo', idx, test_PPVs, 'k')
		# plt.plot(idx, [max(test_PPVs)]*len(idx),linestyle='--', color='r',)
		# ax.annotate(str(max(test_PPVs)), xy=(0, max(test_PPVs)), xytext=(0, max(test_PPVs)),color='b')
		# plt.plot(idx, [PPV_PWM]*len(idx),linestyle='--', color='gray',)
		# ax.annotate('PWM PPV:'+str(PPV_PWM), xy=(0, PPV_PWM), xytext=(0, PPV_PWM),color='gray')
		# plt.title("Test PPV trend for " + TF + 
		# 	"; No. of train:" + str(int(history_stats[0][0])) +
		# 	"; No. of test:" + str(int(history_stats[0][12])))
		# plt.xlabel("save points")
		# plt.savefig(pdf, format='pdf')

		## bidirectional LSTM method and PWM method
		test_AACs=records[TF]['val_acc']
		fig = plt.figure()
		ax = fig.add_subplot(111)
		plt.plot(idx, test_AACs, 'bo', idx, test_AACs, 'k')
		plt.plot(idx, [max(test_AACs)]*len(idx),linestyle='--', color='r',)
		ax.annotate('bidirection LSTM:'+str(max(test_AACs)), xy=(0, max(test_AACs)), xytext=(0, max(test_AACs)),color='r')
		plt.plot(idx, [ACC_PWM]*len(idx),linestyle='--', color='gray',)
		ax.annotate('PWM:'+str(ACC_PWM), xy=(0, ACC_PWM), xytext=(0, ACC_PWM),color='gray')
		
		history_errs,history_stats=load_saves_LSTM(TF=TF)
		idx2=numpy.arange(len(history_errs))
		test_AACs=[compute_ACC(history_stats[n][13],history_stats[n][14],history_stats[n][15],history_stats[n][16]) for n in idx2]
		#plt.plot(range(len(test_AACs)), test_AACs, 'bo', idx, test_AACs, 'k', color='blue')
		plt.plot(idx, [max(test_AACs)]*len(idx),linestyle='--', color='blue',)
		ax.annotate('LSTM:'+str(max(test_AACs)), xy=(0, max(test_AACs)), xytext=(0, max(test_AACs)),color='b')
		
		plt.title("Test ACC trend for " + TF)
		plt.xlabel("save points")
		plt.savefig(pdf, format='pdf')

		plt.close("all")
	pdf.close()

		
		
