"""Verify the scMEDAL environment: import every package the demo needs and print its version.
Usage: /opt/anaconda3/envs/scMEDAL38/bin/python verify_env.py
If any line raises an ImportError, the corresponding package is not installed correctly."""
import sys
import warnings

warnings.filterwarnings("ignore")  # tensorflow_addons is no longer maintained and prints an EOL warning; ignore it

print("Python:", sys.version.split()[0])  # should be 3.8.20

import tensorflow as tf                      # deep-learning framework (tensorflow-macos 2.13.0 on Mac)
import keras                                 # 2.13.1, matches TF 2.13
import tensorflow_probability as tfp         # probabilistic layers, used for the random effects in scMEDAL-RE
import tensorflow_addons as tfa              # author's dependency; the code only uses it at import time
import scanpy, anndata, umap                 # single-cell data handling / dimensionality reduction
import numpy, pandas, scipy, sklearn
import genomap                               # genomap visualisation (the genomap step of the demo)

print("TF", tf.__version__, "| keras", keras.__version__, "| TFP", tfp.__version__, "| TFA", tfa.__version__)
print("scanpy", scanpy.__version__, "| anndata", anndata.__version__, "| numpy", numpy.__version__, "| pandas", pandas.__version__)

# A Mac has no CUDA GPU, so only the CPU is shown here; the demo's quick mode also runs on CPU, just slowly.
print("Devices:", [d.device_type for d in tf.config.list_physical_devices()])
print("Environment check passed ✔")
