# Stage 4: genomap (corresponds to notebook code cells 14 and 15)
# This file is for reading only.

# genomap: arranges the 2,916 gene-expression values of a cell into a 2D "gene image" according to the
# relationships between genes.
# Here it is used to compare how the gene-expression image of the same cell changes for the raw input,
# the FE reconstruction, and the RE reconstruction into different batches.
batches = ["AML420B", "BM5", "MUTZ3"]      # the 3 batches to look at
celltype = ["Mono", "Mono-like"]           # only these two cell types
# Prerequisite: genomap uses the FE and RE reconstructions, so the Stage 1 training must be finished first
selected_models = {k: model_folder_dict[k] for k in ("scmedalfe", "scmedalre")}

pipeline, summary = aml.genomap(
    selected_models,
    n_batches=19,            # the data has 19 batches in total
    num_iter=200,            # genomap iterations; author's comment: 200 for a quick test, otherwise 100 (as written, not checked which is more appropriate)
    cell_id_col="Cell",      # column name of the cell ID in the metadata
    gene_index_col="Gene",   # column name of the gene names
    celltype=["Mono", "Mono-like"],
    batches=batches,
    model="scmedalre",       # use the RE reconstruction as the "cell moved to another batch"
    typ="train",
    split=1,
    add_inputs_fe=True,      # also include the raw input and the FE reconstruction for side-by-side comparison
    extra_recon="fe",
    min_val=-1,              # colour range of the plots: -1 to 2
    max_val=2,
)
# The log line "Selected 1 cell from batch XXX" means only 1 matching cell was drawn from each batch,
# and another 296 cells were drawn to fill the sample; so what is finally shown is a handful of cells,
# not a statistical result, and can only be used for qualitative observation.

# ---- Code cell 15: display the images ----
# It only uses glob to find the images in
# AML_demo_mine/genomap/genomap_plots/*/genomap_plots_scfewbatches_nogenelabels/* and displays them one by one.
