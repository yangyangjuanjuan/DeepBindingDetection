<p align="center">
  <img src ="https://github.com/yangyangjuanjuan/DeepBindingDetection/blob/master/plots/DeepBindingDetection.png" alt="test"/>
</p>

  
------

Apply deep learning on predicting transcription factor (TF) binding sites
------

Deep Binding Detection (DBD) is a tool building a Recurrent Nearual Network (with Long Short Term Memory (LSTM) architecture) to descriminate transcription factor (TF) binding sites from non-binding sites. 

The position-weight matrix (PWM) is a representation of a transcription factor binding site (TFBS) sequence pattern and can be estimated by a small number of representative TFBS sequences. However, PWM method assumes independence between individual nucleotide positions, which performs poorly when some co-occurrence nucleotides observed. RNN is naturally designed to capture the correlation between different inputs, and might be a good solution for TFBS prediction question.

Based on "LSTM Networks for Sentiment Analysis" (as introduced by http://deeplearning.net/tutorial/lstm.html), DBD tries to apply this LSTM  architecture on addressing TFBS prediction question. It shows the prediction was greatly improved by LSTM model by comparing to the PWM method. 

### Comparison

#### TFBS and noncoding sequences
Representative binding site sequences for each TF were obtained from JASPAR and TFBSShape databases. For identifying non-regulatory genomic regions, PeakSeq-processed peak files in UCSC BED format for more than 400 human ChIP-seq experiments were downloaded from ENCODE project, and then combined into a file that was used to mask the noncoding regions to obtain a noncoding, non-TFBS (NCNT) region. Non-binding sequences were then sampled from this NCNT region and would be used as negative cases when train and test model.

#### Traditional PWM scoring and threshold
For each TF, multiple binding sequences were compiled into a corresponding PWM, which then be applied on non-binding sequences sampled from NCNT region. The 0.9998 quantile of the obtained PWM score distribution was used as the PWM score threshold.

#### LSTM prediction
DBD stores classification results as well as some statistics (training error, testing error, true positives, false positives, true negatives, false negatives, PPV, and accuracy) at each save point.  






