Attention to Visual Motion fMRI data 
====================================

This dataset was collected by Christian Buchel and is described in the 
paper:

Buchel, C and K. Friston (1997). Modulation of Connectivity in Visual 
Pathways by Attention: Cortical Interactions Evaluated with Structural 
Equation Modelling and fMRI, Cerebral Cortex, December, 7, pp 768-778.

This archive contains the smoothed, spatially normalised, realigned,
slice-time corrected images in the directory 'functional'. 
The directory 'structural' contains a spatially normalised structural image.
All processing took place using SPM96. See above paper for further details. 

The archive contains the files:

functional/snffM00640_*.{hdr,img}
structural/nsM00587_002.{hdr,img}}
factors.mat
block_regressors.mat
multi_condition.mat
multi_block_regressors.mat
README_DATA.txt

The file 'factors.mat' contains a labelling of the scans in terms of the 
experimental 'factors', photic stimulation, motion and attention. They 
are specified in terms on block onsets.
