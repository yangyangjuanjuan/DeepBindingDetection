<p align="center">
  <img src ="https://github.com/yangyangjuanjuan/DeepBindingDetection/blob/master/plots/DeepBindingDetection.png" alt="test"/>
</p>

  
------

Apply deep learning on predicting transcription factor (TF) binding sites
------

Deep Binding Detection (DBD) is a tool building a Recurrent Nearual Network (with Long Short Term Memory (LSTM) architecture) to discriminate transcription factor (TF) binding sites from non-binding sites. 

Instead of applying LSTM RNN on TF binding sites identification in the master branch, bidirectional LSTM structure is used in this branch.

The motivation of doing this analysis is: there could be a spacial correlation between nucleotides at different positions, but this correlation should be direction irrelevant. Thus a bidirectional LSTM RNN should not show a performance improvement. Instead, because of the more sophisticated structure, the bidirectional LSTM model may require more training to get equivalent performance.     

The architecture of this bidirectional LSTM model is shown as follows, the figure was taken from https://github.com/hycis/bidirectional_RNN.

<p align="center">
  <img src ="https://github.com/yangyangjuanjuan/DeepBindingDetection/blob/bidirectional/plots/bidirectional_lstm.png" alt="structure" width="480"/>
</p>

### Troubleshooting
Any comments and suggestions are highly appreciated.
