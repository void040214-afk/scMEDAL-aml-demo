#!/bin/bash
# =============================================================================
# scMEDAL demo environment setup (Apple Silicon Mac, Python 3.8.20)
# Usage: bash setup_scMEDAL38.sh
# Every step can also be copied into a terminal and run on its own; the script stops at the first error (set -e).
# =============================================================================
set -e

REPO_DIR="${SCMEDAL_REPO:-$HOME/scMEDAL_for_scRNAseq}"   # repository location
ENV_NAME="scMEDAL38"                                     # conda environment name
MIRROR="https://pypi.tuna.tsinghua.edu.cn/simple"        # pip mirror; clear it if the mirror errors or you are outside China: MIRROR=""

# -----------------------------------------------------------------------------
# Step 1: clone the repository
# --depth 1 fetches only the latest commit: smaller and faster on a poor network.
# An earlier clone had only .git and no files (it was interrupted), which is why a re-clone is needed.
# -----------------------------------------------------------------------------
if [ ! -f "$REPO_DIR/README.md" ]; then
  rm -rf "$REPO_DIR"
  git clone --depth 1 https://github.com/DeepLearningForPrecisionHealthLab/scMEDAL_for_scRNAseq.git "$REPO_DIR"
fi

# -----------------------------------------------------------------------------
# Step 2: create the conda environment (Python 3.8.20)
# The authors' README specifies 3.8.20. TensorFlow 2.13.1 only supports Python 3.8-3.11,
# so 3.13 cannot be used. Python 3.8 is EOL (no security updates), but PyPI still has
# 3.8 + arm64 prebuilt wheels for tensorflow / numba / numpy / scipy / h5py.
# -----------------------------------------------------------------------------
if ! conda env list | grep -q "^$ENV_NAME "; then
  conda create -n "$ENV_NAME" python=3.8.20 -y
fi
PY="/opt/anaconda3/envs/$ENV_NAME/bin/python"   # use the python/pip of this environment directly to avoid installing into another environment
PIP="$PY -m pip"

# -----------------------------------------------------------------------------
# Step 3: generate a requirements_mac.txt suitable for Mac
# The authors' scMEDAL_requirements.txt is a `pip freeze` from Linux and fails if installed directly:
#   (a) It contains local-path packages `xxx @ file:///home/conda/...` (ipython, jedi, six, ...) that do not
#       exist on your machine; they get installed automatically as dependencies of other packages,
#       so they are simply removed.
#   (b) genomap is a git link and is installed separately (step 5) so that pip does not hang pulling from GitHub.
#   (c) Neuroimaging packages such as pysam / nipype / nibabel / lxml have no prebuilt arm64 wheels and would
#       have to be compiled; the demo does not use them, so they are removed.
# -----------------------------------------------------------------------------
REQ_SRC="$REPO_DIR/scMEDAL_env/scMEDAL_requirements.txt"
REQ_MAC="$REPO_DIR/scMEDAL_env/requirements_mac.txt"
grep -vE "file://|@ git|^(pysam|nipype|nibabel|prov|lxml|rdflib|pydot|etelemetry|ci-info|traits|simplejson|looseversion|texttable|pipdeptree|stdlib-list|networkx)==" \
  "$REQ_SRC" > "$REQ_MAC"

# Two manual fixes are required (the authors' freeze file itself has problems):
#   (d) exceptiongroup 1.3.0 requires typing_extensions>=4.6, but TensorFlow 2.13 requires <4.6 (pinned to 4.5.0
#       in the file), so they conflict -> downgrade to 1.2.2 (which does not depend on typing_extensions).
sed -i '' 's/^exceptiongroup==1.3.0/exceptiongroup==1.2.2/' "$REQ_MAC"
#   (e) On Apple Silicon `tensorflow==2.13.1` is only a shell that really depends on tensorflow-macos==2.13.1,
#       and Python 3.8 does not have that version (the highest is 2.13.0) -> install tensorflow-macos==2.13.0 directly.
sed -i '' 's/^tensorflow==2.13.1/tensorflow-macos==2.13.0/' "$REQ_MAC"

# -----------------------------------------------------------------------------
# Step 4: install the dependencies
# The Tsinghua mirror speeds things up; --timeout/--retries cope with an unstable network. About 167 packages,
# TensorFlow is the largest.
# -----------------------------------------------------------------------------
if [ -n "$MIRROR" ]; then
  $PIP install -r "$REQ_MAC" -i "$MIRROR" --timeout 120 --retries 10
else
  $PIP install -r "$REQ_MAC" --timeout 120 --retries 10
fi

# -----------------------------------------------------------------------------
# Step 5: install genomap (pinned to the commit the authors used)
# --no-deps: do not let it change the package versions we have already pinned.
# -----------------------------------------------------------------------------
$PIP install "git+https://github.com/xinglab-ai/genomap.git@d09395a04c26c02b73c8efe9db7dbce24306305d" --no-deps

# -----------------------------------------------------------------------------
# Step 6: register the Jupyter kernel; choose "Python (scMEDAL38)" in the notebook
# -----------------------------------------------------------------------------
$PY -m ipykernel install --user --name "$ENV_NAME" --display-name "Python ($ENV_NAME)"

# -----------------------------------------------------------------------------
# Step 7: verify (import all key packages)
# -----------------------------------------------------------------------------
$PY "$(dirname "$0")/verify_env.py"

# -----------------------------------------------------------------------------
# Still needed afterwards (not part of this script):
#  A) Compatibility patch: in $REPO_DIR run `git apply <this repo>/patches/mac_compat.patch`
#     (it also sets ROOT_PATH in utils/defaults.py automatically, which the authors' README asks you to edit by hand).
#  B) Data: download the preprocessed AML data from Figshare (DOI 10.6084/m9.figshare.28414367) and unpack it to
#     $REPO_DIR/data/AML_data/log_transformed_2916hvggenes/ (containing exprMatrix.npy, meta.csv, splits/split_1..5)
#  C) Run demo/demo_aml.ipynb (choose the kernel Python (scMEDAL38))
# -----------------------------------------------------------------------------
