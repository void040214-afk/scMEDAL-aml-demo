"""All the code run so far after the environment was set up (annotated).

This file is a "record + explanation"; every section corresponds to a step we actually executed.
Section A runs in a terminal / script; sections B and C are code cells 1 and 3 of demo_aml.ipynb.
"""

# =============================================================================
# Section A: check that the AML data is complete (read-only, no file is modified)
# Data location: scMEDAL_for_scRNAseq/data/AML_data/log_transformed_2916hvggenes/
# =============================================================================
import os
import numpy as np
import pandas as pd

DATA = os.path.join(os.path.expanduser(os.environ.get("SCMEDAL_REPO", "~/scMEDAL_for_scRNAseq")), "data/AML_data/log_transformed_2916hvggenes")

# exprMatrix.npy: cell x gene expression matrix (log-transformed, 2916 highly variable genes).
# mmap_mode="r" reads from disk only when needed instead of loading all 448MB into memory at once.
X = np.load(f"{DATA}/exprMatrix.npy", mmap_mode="r")
print(X.shape, X.dtype)          # expected (38417, 2916) float32

# meta.csv: one annotation row per cell (cell type CellType, patient group Patient_group, etc.)
meta = pd.read_csv(f"{DATA}/meta.csv")
print(meta.shape)                # expected (38417, 38); the number of rows must match the matrix

# 5 cross-validation splits, each with train / val / test.
# Checks: the three parts add up to the total number of cells; matrix rows == meta rows; number of genes == 2916.
for s in range(1, 6):
    rows = []
    for part in ("train", "val", "test"):
        Xp = np.load(f"{DATA}/splits/split_{s}/{part}/exprMatrix.npy", mmap_mode="r")
        mp = pd.read_csv(f"{DATA}/splits/split_{s}/{part}/meta.csv")
        assert Xp.shape[0] == len(mp) and Xp.shape[1] == 2916
        rows.append(Xp.shape[0])
    assert sum(rows) == 38417
# Result: all checks passed. Patient_group has three classes (AML / control / cellline),
# which corresponds to n_pred=3 of the MEC classifier later.


# =============================================================================
# Section B: notebook code cell 1 -- change the working directory and import
# =============================================================================
import os

# Jupyter treats demo/ (where the notebook lives) as the current directory by default,
# while models/, utils/ and analysis/ are one level up (the repository root),
# so we must chdir to the repository root first, otherwise `from models.models import ...` fails with
# ModuleNotFoundError: No module named 'models'.
# (In the original notebook this line is commented out and still contains the authors' own path.)
os.chdir(os.path.expanduser(os.environ.get("SCMEDAL_REPO", "~/scMEDAL_for_scRNAseq")))  # change to where you cloned the official repository

# The only entry function: trains a preset experiment by "model name + dataset name".
from models.models import train_model_on_named_experiment
# The OUTPUTS_DIR printed on import is where results are saved: <repo>/outputs
# The red WARNINGs (Adam is slow on M1/M2, lr is deprecated) are just hints and can be ignored.


# =============================================================================
# Section C: notebook code cell 3 -- train the two models
# =============================================================================
# "scMEDAL-FE" = fixed-effects model
# "scMEDAL-RE" = random-effects model, with an extra la_clus_loss (latent-space clustering term) in the loss
# "AML" = dataset name, corresponding to the data checked above
# n_latent_dims=50: the latent space (compressed representation) has 50 dimensions
# quick=True: quick mode -- only 1 fold and 10 epochs
#            (the paper uses 5 folds x 500 epochs, so the results here are only a demonstration, not paper numbers)
scmedalfe_aml = train_model_on_named_experiment(
    "scMEDAL-FE", "AML", model_kwargs={"n_latent_dims": 50}, train_kwargs={"quick": True})
scmedalre_aml = train_model_on_named_experiment(
    "scMEDAL-RE", "AML", model_kwargs={"n_latent_dims": 50}, train_kwargs={"quick": True})

# After training, each model writes three kinds of files under outputs/AML/:
#   saved_models/  model weights
#   latent_space/  50-dimensional latent representations of train/val/test cells (clustering, UMAP and MEC all read this)
#   figures/       training curves and other plots
# Directory names carry a timestamp, e.g. ..._2026-10-29_00-15.
#
# Two things that are easy to misread:
#  1) The directory name says epochs-500, but that name is built from the default parameters;
#     quick mode overrides model_params['epochs'] to 10 in models/base.py, so only 10 epochs are actually trained.
#  2) The "Early stopping ... val_loss which is not available" warning in the log:
#     the callback monitors val_loss, but the model logs val_total_loss, so early stopping and
#     "save best model" do not take effect.
#     10 epochs would never trigger early stopping anyway, so this has no effect on the demo.
