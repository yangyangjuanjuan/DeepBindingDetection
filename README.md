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
  <img src ="https://github.com/yangyangjuanjuan/DeepBindingDetection/blob/bidirectional/plots/bidirectional_lstm.png" alt="structure" width="400"/>
</p>

### Results
Obtained results are as expected. Generally, if both LSTM model and bi-directional LSTM model receive same training, the later one will have worse performance. By considering bi-directional LSTM model has more sophisticated structure and double LSTM layers, double training time for bi-directional LSTM was also checked. For some TFs, bi-directional LSTM has better performance after being trained longer time. The following figures show the comparison between two models. For each row, left panel shows comparison plot for both models trained at same time, but in right panel, bi-directional LSTM was trained longer. 

<p align="center">
  <img src ="https://github.com/yangyangjuanjuan/DeepBindingDetection/blob/bidirectional/plots/FOS_1.png" alt="structure" width="300"/>
  <img src ="https://github.com/yangyangjuanjuan/DeepBindingDetection/blob/bidirectional/plots/FOS_2.png" alt="structure" width="300"/>
</p>

<p align="center">
  <img src ="https://github.com/yangyangjuanjuan/DeepBindingDetection/blob/bidirectional/plots/RFX5_1.png" alt="structure" width="300"/>
  <img src ="https://github.com/yangyangjuanjuan/DeepBindingDetection/blob/bidirectional/plots/RFX5_2.png" alt="structure" width="300"/>
</p>

<p align="center">
  <img src ="https://github.com/yangyangjuanjuan/DeepBindingDetection/blob/bidirectional/plots/STAT1_1.png" alt="structure" width="300"/>
  <img src ="https://github.com/yangyangjuanjuan/DeepBindingDetection/blob/bidirectional/plots/STAT1_2.png" alt="structure" width="300"/>
</p>

### Troubleshooting
Any comments and suggestions are highly appreciated.
