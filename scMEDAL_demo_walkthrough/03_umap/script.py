# Stage 3: UMAP visualisation (corresponds to notebook code cells 11 and 12)
# This file is for reading only.

# Take the latent representations of the training set (types=["train"]), fold 1 (splits=[1]),
# reduce each model to 2 dimensions with UMAP, and plot coloured by Patient_group / batch / celltype.
# A control plot of the raw input data (PCA, then UMAP) is also drawn (file names contain input_pca).
# Plots and intermediate csv files are saved in outputs/.../AML_demo_mine/umap_19batches_seed_5/
#   plots_axis/   plots with axes    plots_noaxis/  plots without axes    umap_csv/  UMAP coordinates
# Note: if these csv files already exist, the function reuses them instead of recomputing.
# The log shows "Directory does not exist ... splits_2/3/4/5":
# quick mode trains only fold 1, so the directories of the other folds never existed; this is not an error.
processors = aml.umap(model_folder_dict, types=["train"], splits=[1])
processors

# ---- Code cell 12: image viewer ----
# This cell (long, omitted here) only displays: it uses glob to find all images matching
# *umap*/*plots_axis*/*umap* under AML_demo_mine, shrinks them to thumbnails and embeds them in the
# notebook, one row per model.
# It does not generate any new files ("no files written").
