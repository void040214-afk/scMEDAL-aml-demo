# Stage 2: clustering scores (corresponds to notebook code cell 9)
# This file is for reading only. `aml` and `model_folder_dict` come from 00_setup/script.py.

# Read the 50-dimensional latent space of each model and compute clustering quality with two labels,
# "batch" and "cell type":
#   1/db        = reciprocal of the Davies-Bouldin index (larger is better)
#   ch          = Calinski-Harabasz index (larger is better)
#   silhouette  = silhouette coefficient (-1 to 1, larger is better)
# Meaning: a higher score = when grouped by this label, groups are tighter inside and farther apart.
#   - High score for "batch" = the latent space separates by batch (batch information is encoded)
#   - High score for "cell type" = the latent space separates by cell type (biological information is kept)
res = aml.clustering_scores(model_folder_dict)

# The result table is also written to files such as test_allscores.csv under outputs/.../AML_demo_mine/.
# Only 1 fold was run, so the confidence intervals (CI_lower / CI_upper) are all NaN, which is normal;
# by default they are computed assuming 5 folds with 4 degrees of freedom
# (see utils.compare_results_utils.process_confidence_intervals).
res
