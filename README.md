# scMEDAL AML Demo Reproduction (BMI5101 Group Project)

This repository reproduces the official `demo/demo_aml.ipynb` of [scMEDAL](https://github.com/DeepLearningForPrecisionHealthLab/scMEDAL_for_scRNAseq) on the AML dataset (38,417 cells × 2,916 genes, 19 batches), and splits the notebook into five stages that are easier to read. The original project and paper belong to the UTSW authors; see [UTSW_License.txt](UTSW_License.txt) (academic and research use only).

## Results at a glance (quick mode: 1 fold × 10 epochs)

- The scMEDAL-FE latent space mixes batches better and separates cell types more clearly; the scMEDAL-RE latent space splits into small clusters by batch.
- Predicting Patient_group from FE + RE combined raises accuracy from 84.94% to 99.14%.
- Quick mode is only suitable for comparing the two models relative to each other. Do not compare the absolute numbers with the paper.

## Repository layout

| Path | Contents |
|---|---|
| `READING_ORDER.md` | Suggested reading order |
| `scMEDAL_demo_walkthrough/` | Stages 00–05: `script.py` (annotated, for reading only), `README.md`, result figures |
| `scMEDAL_setup/` | Environment script `setup_scMEDAL38.sh`, `verify_env.py`, `requirements_mac.txt`, `demo_steps_so_far.py` |
| `patches/mac_compat.patch` | The two changes to the official repository needed to run on Apple Silicon |
| `notebook/demo_aml_mac_run.ipynb` | The notebook we actually ran (with outputs) |

## How to reproduce

1. (Optional) Set the location of the official repository; the default is `~/scMEDAL_for_scRNAseq`:
   `export SCMEDAL_REPO=/your/path`
2. Run `bash scMEDAL_setup/setup_scMEDAL38.sh`. It clones the official repository, creates a Python 3.8.20 conda environment and installs the dependencies (Apple Silicon Mac).
3. Apply the patch from the root of the official repository:
   `git apply <this repo>/patches/mac_compat.patch`
   - `random_effects.py`: makes the `tensorflow_addons` import optional (it has no prebuilt wheel for Apple Silicon and is not actually used by the code).
   - `utils/defaults.py`: `ROOT_PATH` now defaults to the repository directory and can be overridden with `SCMEDAL_ROOT`.
4. Download the data from Figshare, DOI [10.6084/m9.figshare.28414367](https://doi.org/10.6084/m9.figshare.28414367), and place it under `data/AML_data/` in the official repository. This repository does not include the data or trained models.
5. Run `python scMEDAL_setup/verify_env.py` to check the environment, then run the official notebook.

## Notes

The same model has several runs under `outputs/`. See the "run batches" section in `scMEDAL_demo_walkthrough/README.md` for which run each stage uses.
