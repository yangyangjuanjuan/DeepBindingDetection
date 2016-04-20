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
Representative binding site sequences $S_t$








