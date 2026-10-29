"""验证 scMEDAL 环境:逐个导入 demo 需要的包并打印版本。
用法:/opt/anaconda3/envs/scMEDAL38/bin/python verify_env.py
任何一行报 ImportError,就说明对应的包没装好。"""
import sys
import warnings

warnings.filterwarnings("ignore")  # tensorflow_addons 已停止维护,会打印 EOL 警告,忽略即可

print("Python:", sys.version.split()[0])  # 应为 3.8.20

import tensorflow as tf                      # 深度学习框架(Mac 版 tensorflow-macos 2.13.0)
import keras                                 # 2.13.1,与 TF 2.13 配套
import tensorflow_probability as tfp         # 概率层,scMEDAL-RE 的随机效应用到
import tensorflow_addons as tfa              # 作者依赖,代码里只在 import 处用到
import scanpy, anndata, umap                 # 单细胞数据处理 / 降维
import numpy, pandas, scipy, sklearn
import genomap                               # genomap 可视化(demo 的 genomap 步骤)

print("TF", tf.__version__, "| keras", keras.__version__, "| TFP", tfp.__version__, "| TFA", tfa.__version__)
print("scanpy", scanpy.__version__, "| anndata", anndata.__version__, "| numpy", numpy.__version__, "| pandas", pandas.__version__)

# Mac 没有 CUDA GPU,这里只会看到 CPU;demo 的 quick 模式在 CPU 上也能跑,只是慢。
print("设备:", [d.device_type for d in tf.config.list_physical_devices()])
print("环境验证通过 ✔")
