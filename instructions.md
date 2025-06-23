  # Patch Clamp Data Analysis

Analyze your patch clamp data according to the following paper:
[Eshra A, Hirrlinger P and Hallermann S (2019): Enriched Environment Shortens the Duration of Action Potentials in Cerebellar Granule Cells. *Front. Cell. Neurosci.* 13:289.](https://doi.org/10.3389/fncel.2019.00289)

## Parameters to Determine
Try to extract the following features for each action potential (AP):
- voltage threshold
- peak 
- amplitude (peak – threshold)
- number of APs per trace
- half duration (duration measured at half maximum amplitude)
- AP frequencies per trace
  - average AP frequency
  - initial AP frequency (based on the first two APs)
  - frequency of the first five APs
- optional: rheobase (i. e., the injected current at which the first AP occurs)

![*Hallermann*, 2025](/sketch_Hallermann.png)

## Methodological Reference

Here is the corresponding methods description in the mentioned paper:
 
> The half duration of AP was measured at half maximum amplitude. The amplitude was measured from threshold to peak. The threshold was defined as the membrane voltage at which the first derivative exceeded 100 V/s. Action potentials with a peak smaller than -20 mV, an amplitude smaller than 20 mV, and a half duration smaller than 50 μs or larger than 500 μs were excluded. These exclusion criteria were chosen to ensure that only proper APs are analyzed.

In other words, you will need to compute the first derivative of the membrane potential trace to detect APs.

## Data Import

To import HEKA's `.dat`-files you can use the code from [this repository](https://github.com/HallermannLab/heka_import_test).