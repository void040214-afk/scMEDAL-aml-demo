# Stage 5: MEC classifier

Code: [script.py](script.py). Raw summary table: [results_MEC_RF_summary_all_runs.csv](results_MEC_RF_summary_all_runs.csv).

## What it does

On top of the already-trained latent representations, a classifier is trained to predict `Patient_group` (3 classes: AML / control / cellline), to measure how much "patient group" information the latent representations contain. The metric in the table is named `RFAccuracy`, so the classifier is a random forest (judged from the metric name). Two inputs are compared:

- The FE latent representation only
- The FE and RE latent representations concatenated

## Results

The summary table has 2 rows for each configuration because it covers **all** runs in `mec/`. **Ours are the `00-37` rows**; `00-08` is an earlier run:

| Input | Run time | Accuracy | Balanced accuracy | Random-baseline accuracy |
|---|---|---|---|---|
| FE only | 00-08 (old) | 83.28 | 60.62 | 61.41 |
| **FE only** | **00-37 (ours)** | **84.94** | **64.94** | 61.41 |
| FE + RE | 00-08 (old) | 99.06 | 98.26 | 61.41 |
| **FE + RE** | **00-37 (ours)** | **99.14** | **98.43** | 61.41 |

## How to read it

- **FE + RE is clearly better than FE only**: accuracy 84.94 → 99.14, balanced accuracy 64.94 → 98.43. The notebook's conclusion ("classification is better when combined") holds in our results. The old and new runs agree, so this is not a coincidence.
- With FE only, accuracy (84.94) and balanced accuracy (64.94) differ a lot. Balanced accuracy is the mean recall over classes, so this means the smaller classes are recognised poorly with FE only. After adding RE the two numbers are almost equal and every class is recognised well.
- "Random-baseline accuracy 61.41" is a column produced by the code; I did not check exactly how it is computed.
- A possible reason (my speculation, not verified): Patient_group is strongly correlated with batch/donor, and the RE latent representation encodes batch information, so concatenating RE greatly improves classification. Verifying this would need extra experiments, for example splitting with whole batches held out.
- These are 1-fold × 10-epoch results, without confidence intervals.
