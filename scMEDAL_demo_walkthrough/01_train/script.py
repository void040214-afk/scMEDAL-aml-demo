# Stage 1: train scMEDAL-FE and scMEDAL-RE (corresponds to notebook code cell 3)
# This file is for reading only.

from models.models import train_model_on_named_experiment

# First argument: model name. "scMEDAL-FE" = fixed-effects model; "scMEDAL-RE" = random-effects model.
# Second argument: named experiment "AML" (acute myeloid leukemia, 38,417 cells × 2,916 highly variable genes,
#   19 batches/donors).
# model_kwargs={"n_latent_dims": 50}: compress each cell into a 50-dimensional latent representation.
# train_kwargs={"quick": True}: quick mode = only 1 fold and 10 epochs.
#   The paper uses 5 folds × 500 epochs (with early stopping), so the numbers here can only be used to
#   compare the models with each other, not against the absolute numbers in the paper.
scmedalfe_aml = train_model_on_named_experiment(
    "scMEDAL-FE", "AML",
    model_kwargs={"n_latent_dims": 50},
    train_kwargs={"quick": True},
)
scmedalre_aml = train_model_on_named_experiment(
    "scMEDAL-RE", "AML",
    model_kwargs={"n_latent_dims": 50},
    train_kwargs={"quick": True},
)

# Training writes three kinds of files (all under outputs/AML/, folder names end with the run time):
#   saved_models/  model weights
#   latent_space/  the 50-dimensional latent representation of every cell after training (all later analyses
#                  read this) + history_allfolds.csv (loss of every epoch)
#   figures/       loss curves and other plots
