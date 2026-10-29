# Stage 5: MEC classifier (corresponds to notebook code cells 17 and 18)
# This file is for reading only. `model_paths` is built from model_folder_dict in notebook cell 5 and
# points to the latent-space folders of the two models.

from models.models import train_model_on_named_experiment

# MEC (Mixed Effects Classifier): trains a classifier on top of the already-trained latent representations.
# The goal is to predict Patient_group (3 classes: AML / control / cellline) and see how much
# "patient group" information the latent representations contain.
# The metric names in the summary table carry RF (RFAccuracy etc.), so the classifier here is a random forest.

# Experiment A: FE latent space only
train_model_on_named_experiment(
    "MEC", "AML",
    train_kwargs={"quick": True, "results_path_dict": model_paths},
    model_kwargs={
        "n_pred": 3,                       # predict 3 classes
        "bio_col": "Patient_group",        # target column to predict
        "models_list": list(model_paths.keys()),
        "latent_keys_config": {"fe_latent": "scmedalfe_latent"},   # feed only the FE latent representation
    },
)

# Experiment B: FE and RE latent spaces concatenated
train_model_on_named_experiment(
    "MEC", "AML",
    train_kwargs={"quick": True, "results_path_dict": model_paths},
    model_kwargs={
        "n_pred": 3,
        "bio_col": "Patient_group",
        "models_list": list(model_paths.keys()),
        "latent_keys_config": {"fe_latent": "scmedalfe_latent", "re_latent": "scmedalre_latent"},
    },
)

# Summarise the results of all MEC runs (on the test set)
from utils.compare_results_utils import get_all_mec_metrics
df, _ = get_all_mec_metrics(AML_OUTPUTS_DIR, AML_EXPERIMENT_NAME, split="test")
df
# Important: this function summarises ALL runs in the mec/ folder, not only this one,
# so each configuration appears in several rows (different run times). To see your own,
# pick by the timestamp at the end of run_name.
