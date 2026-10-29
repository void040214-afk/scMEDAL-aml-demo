# scMEDAL AML demo walkthrough

`demo/demo_aml.ipynb` is split into 5 stages, one folder per stage: **`script.py` (annotated code, for reading only) + result figures/tables + `README.md` (what the step does and how to read the results)**. The original notebook was not modified.

## Overall workflow

```
AML data (38,417 cells × 2,916 genes, 19 batches)
      │
 01 Train ──► scMEDAL-FE (fixed effects) and scMEDAL-RE (random effects),
      │        each giving a 50-dimensional latent representation per cell
      │
      ├─ 02 Clustering scores: how clearly the latent space separates "batch" / "cell type"
      ├─ 03 UMAP: plot the latent space
      ├─ 04 genomap: how the gene-expression image of the same cell changes when the batch is swapped
      └─ 05 MEC: predict Patient_group from the latent representations to see how much biological information they hold
```

## Summary of our results

- In the FE latent space, **batches are mixed well and cell types are clearer**; the RE latent space **splits into small clusters by batch** (02, 03).
- Combining FE and RE to predict Patient_group raises accuracy from **84.94% to 99.14%** (05).
- These are quick-mode results (1 fold × 10 epochs). They are only suitable for comparing the two models against each other, not for comparing with the absolute numbers in the paper.

## One thing to know: the runs are not all from the same batch

`outputs/` contains several runs of the same model (at different times), and some of them were not run in our notebook. This walkthrough uses:

| Stage | Run actually used |
|---|---|
| 01 Training curves | FE: `..._00-15`, RE: `..._00-16` (the same runs the analysis uses) |
| 02, 03, 04 | Analysis of FE `00-15` + RE `00-16` |
| 05 MEC | Our rows are the two `00-37` rows (`00-08` is an earlier run) |

**The training log saved in the notebook file comes from the `00-24` re-run**, which is not the same set of models as the `00-15/00-16` runs used in the later analysis. The two runs have identical settings and differ only in randomness, so the training numbers here are taken from the `history_allfolds.csv` of `00-15/00-16`, not from the notebook output.
