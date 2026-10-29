# Stage 0: setup (corresponds to notebook cells 1 and 7)
# This file is for reading only and is not designed to run on its own.

import os

# We must first change to the repository root: models/, utils/ and analysis/ are plain folders
# (not pip-installed packages), so `import models` only works when the current directory is the repo root.
# The original notebook has the authors' server path here (commented out); change it to your own.
os.chdir(os.path.expanduser(os.environ.get("SCMEDAL_REPO", "~/scMEDAL_for_scRNAseq")))  # change to where you cloned the official repository

# The only "entry function": trains a "named experiment" (one model + one dataset) by name.
# The named experiment already holds the data path, number of batches (AML = 19 batches),
# number of classes and so on (see utils/defaults.py).
from models.models import train_model_on_named_experiment

# ---- After training, the notebook needs you to specify which training run to analyse ----
# Every training run creates a new folder ending with a timestamp under
# outputs/AML/latent_space/<dataset>/<model name>/, so the folder name must be put into the dict,
# otherwise the later analysis cannot find the files (the original notebook has the authors' own dates).
# Note: the same model can have many runs; picking the wrong timestamp means analysing a different model.
model_folder_dict = {
    "scmedalfe": "run_crossval_loss_gen_weight-1_loss_recon_weight-1000_loss_class_weight-1_n_latent_dims-50_layer_units-512-132_scaling-min_max_model_type-scmedalfe_batch_size-512_epochs-500_patience-30_sample_size-10000_2026-10-29_00-15",
    "scmedalre": "run_crossval_loss_recon_weight-110_loss_latent_cluster_weight-0.1_n_latent_dims-50_layer_units-512-132_scaling-min_max_batch_size-512_epochs-500_patience-30_sample_size-10000_2026-10-29_00-16",
}

# ---- Create the analysis object (notebook cell 7) ----
import analysis.analysis as aa

# analysis_name decides where results are written: outputs/AML/compare_models/<dataset>/<analysis_name>/.
# A new name (AML_demo_mine) is used so that results are not mixed with anyone else's:
# when aml.umap() finds a file with the same name it reuses it instead of recomputing.
analysis_name = "AML_demo_mine"
aml = aa.AMLAnalysis(model_folder_dict, analysis_name)
