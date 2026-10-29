# Stage 1: Training

Code: [script.py](script.py).

## What it does

Two autoencoder-style models are trained separately. The input is the 2,916 gene-expression values of each cell and the output is a 50-dimensional latent representation:

- **scMEDAL-FE** (fixed effects): judging from the column names (`adv_loss`, `acc`), training includes a batch-related classification/adversarial branch intended to keep batch information out of the latent representation. This is inferred from the column names; I did not read the model code to confirm it.
- **scMEDAL-RE** (random effects): the column names include `la_clus_loss` (latent-space clustering loss) and `kld` (KL divergence), used to make the latent space learn batch-related structure. This is likewise inferred from the column names.

Quick mode: 1 fold × 10 epochs. The paper uses 5 folds × 500 epochs.

## Results (epoch 1 → epoch 10, from `history_allfolds.csv`)

**FE (`00-15`)**

| Metric | epoch 0 | epoch 9 |
|---|---|---|
| recon_loss (reconstruction error) | 0.0452 | 0.0016 |
| val_recon_loss (validation set) | 0.0034 | 0.0015 |
| adv_loss | 2.27 | 1.46 |
| val_total_loss | 0.78 | -0.14 |

**RE (`00-16`)**

| Metric | epoch 0 | epoch 9 |
|---|---|---|
| recon_loss | 0.9426 | 0.5269 |
| val_recon_loss | 0.2481 | 0.4363 |
| la_clus_loss | 2.861 | 2.024 |
| total_loss | 105.5 | 59.7 |
| val_total_loss | 27.6 | 48.2 |

## How to read it

- The training loss of both models decreases, so training is working normally.
- The RE `val_recon_loss` (0.25 → 0.44) goes up while the training recon_loss goes down. This is what is visible within 10 epochs; I did not analyse the cause or run more epochs to check whether it keeps rising.
- The curves are in `results/`: `fe_loss.png`, `fe_recon_loss.png`, `re_loss.png`, `re_loss_KLD.png`.

## Red warnings in the log

```
Early stopping conditioned on metric `val_loss` which is not available
Can save best model only with val_loss available, skipping
```

The early-stopping and "save best model" callbacks monitor `val_loss`, but the models actually log `val_total_loss`, so the callbacks have no effect. Quick mode has only 10 epochs, so early stopping would not trigger anyway; skipping "save best model" means the weights of the last epoch are what gets saved.
