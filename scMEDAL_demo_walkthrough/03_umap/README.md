# Stage 3: UMAP

Code: [script.py](script.py).

## What it does

The 50-dimensional latent representations of the two models are reduced to 2 dimensions with UMAP. Each model gets 3 plots, coloured by `Patient_group`, `batch` and `celltype`. The plots are in `results/`:

| | Patient_group | batch | celltype |
|---|---|---|---|
| FE | ![](results/fe_Patient_group.png) | ![](results/fe_batch.png) | ![](results/fe_celltype.png) |
| RE | ![](results/re_Patient_group.png) | ![](results/re_batch.png) | ![](results/re_celltype.png) |

## How to read it

- **FE**: the points form one continuous shape. In the batch plot the colours are mixed and not separated by batch; in the cell-type plot regions along the shape are visible (for example T cells and plasma cells each occupy a block).
- **RE**: it splits into many separate small clusters. In the batch plot each small cluster is mostly a single colour, i.e. the clusters follow batches; in the cell-type plot the colours are mixed within a cluster.
- This agrees with the Stage 2 numbers: RE has the higher batch scores, FE has the higher cell-type score.

## Notes

- These plots come from the `AML_demo_mine` directory and use the models trained at 00:15/00:16 (file time 00:33, checked).
- The `Directory does not exist ... splits_2/3/4/5` messages in the log are not errors: quick mode trains only fold 1.
- The shape of a UMAP differs slightly from run to run (random seed, batch sampling), so look at the overall trend rather than the exact shape.
