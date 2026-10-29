# Stage 2: Clustering scores

Code: [script.py](script.py). Full table: [results_test_allscores.csv](results_test_allscores.csv).

## What it does

For the 50-dimensional latent space of each model, three scores are computed with respect to two labels, "batch" and "cell type". **All three metrics are better when larger**:

| Metric | Meaning |
|---|---|
| 1/db | Reciprocal of the Davies-Bouldin index |
| ch | Calinski-Harabasz index |
| silhouette | Silhouette coefficient, ranging from -1 to 1 |

A high score for a label means that, when the latent space is grouped by that label, the groups are tighter inside and farther apart from each other.

## Results (values from the two screenshots)

| Label | Metric | scMEDAL-FE | scMEDAL-RE |
|---|---|---|---|
| batch | 1/db | 0.09 | 0.49 |
| batch | ch | 116.2 | 1779.5 |
| batch | silhouette | -0.18 | 0.42 |
| celltype | 1/db | 0.18 | 0.19 |
| celltype | ch | 1006.41 | 224.11 |
| celltype | silhouette | -0.01 | -0.05 |

(Which rows are batch and which are celltype was determined from the position of the headers in the screenshots.)

## How to read it

- **Batch: RE is clearly higher on all three metrics.** The RE latent space has strong batch structure. The notebook comment also says "RE's batch clustering scores are all higher than FE's".
- **Cell type: FE has the higher ch (1006 vs 224)**, 1/db is almost the same, and silhouette is close to 0 for both.
- This matches the design intent that FE carries less batch information and RE encodes batch information (this is my understanding of the method, not something this table proves by itself).
- All confidence intervals are NaN because only 1 fold was run.
- The cell-type silhouette is close to 0 for both models, meaning neither model separates cell types cleanly after 10 epochs of training. Whether this is caused by the short training or something else was not verified.
