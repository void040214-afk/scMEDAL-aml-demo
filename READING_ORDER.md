# scMEDAL AML demo package: reading order

Original project: https://github.com/DeepLearningForPrecisionHealthLab/scMEDAL_for_scRNAseq

1. `scMEDAL_demo_walkthrough/README.md`: overview and the overall workflow.
2. Read the stages in order. For each stage, read its README first, then `script.py` and `results/`:
   - `00_setup`: preparation (only `script.py`)
   - `01_train`: training FE / RE
   - `02_clustering_scores`: clustering scores
   - `03_umap`: UMAP plots
   - `04_genomap`: genomap plots
   - `05_mec`: MEC classification results
3. To reproduce the environment, see `scMEDAL_setup/`:
   - `setup_scMEDAL38.sh`: environment script (Apple Silicon Mac, Python 3.8.20, every step commented)
   - `verify_env.py`: checks the environment
   - `demo_steps_so_far.py`: data check and an annotated record of the first notebook cells
   - `requirements_mac.txt`: dependencies adapted for Mac (modified from the official `scMEDAL_requirements.txt`)
4. To see the real code, clone the repository above and read `demo/demo_aml.ipynb`, `models/`, `analysis/` and `utils/defaults.py`.

Notes:
- The `script.py` files in the walkthrough are for reading only and cannot be run on their own.
- The results come from quick mode (1 fold × 10 epochs) and are only suitable for comparing the two models against each other.
- The repository path in the scripts defaults to `~/scMEDAL_for_scRNAseq`. Set the environment variable `SCMEDAL_REPO` to point to where you cloned it.
- This package does not include the data (download the preprocessed AML data from Figshare, DOI 10.6084/m9.figshare.28414367) or the trained models.
