"""环境配置完成之后、到目前为止做过的所有代码(带注释)。

这个文件是"记录 + 讲解"用的,每一段都对应你实际执行过的一步。
段 A 在终端 / 脚本里跑;段 B、C 是 demo_aml.ipynb 的第 1、3 个代码格。
"""

# =============================================================================
# 段 A:检查 AML 数据是否完整(只读,不改任何文件)
# 数据位置:scMEDAL_for_scRNAseq/data/AML_data/log_transformed_2916hvggenes/
# =============================================================================
import os
import numpy as np
import pandas as pd

DATA = os.path.join(os.path.expanduser(os.environ.get("SCMEDAL_REPO", "~/scMEDAL_for_scRNAseq")), "data/AML_data/log_transformed_2916hvggenes")

# exprMatrix.npy:细胞 x 基因的表达矩阵(log 变换后,2916 个高变基因)。
# mmap_mode="r" 只在需要时从磁盘读,不把 448MB 一次性装进内存。
X = np.load(f"{DATA}/exprMatrix.npy", mmap_mode="r")
print(X.shape, X.dtype)          # 期望 (38417, 2916) float32

# meta.csv:每个细胞一行的注释(细胞类型 CellType、病人分组 Patient_group 等)
meta = pd.read_csv(f"{DATA}/meta.csv")
print(meta.shape)                # 期望 (38417, 38),行数要和矩阵一致

# 5 个交叉验证 split,每个里有 train / val / test。
# 检查:三份行数相加 == 总细胞数;矩阵行数 == meta 行数;基因数 == 2916。
for s in range(1, 6):
    rows = []
    for part in ("train", "val", "test"):
        Xp = np.load(f"{DATA}/splits/split_{s}/{part}/exprMatrix.npy", mmap_mode="r")
        mp = pd.read_csv(f"{DATA}/splits/split_{s}/{part}/meta.csv")
        assert Xp.shape[0] == len(mp) and Xp.shape[1] == 2916
        rows.append(Xp.shape[0])
    assert sum(rows) == 38417
# 结果:全部通过。Patient_group 有 AML / control / cellline 三类,
# 对应后面 MEC 分类器的 n_pred=3。


# =============================================================================
# 段 B:notebook 第 1 个代码格 —— 切换工作目录并导入
# =============================================================================
import os

# Jupyter 默认把 notebook 所在的 demo/ 当作当前目录,
# 而 models/、utils/、analysis/ 在它的上一级(仓库根目录),
# 所以必须先 chdir 到仓库根目录,否则 `from models.models import ...` 会报
# ModuleNotFoundError: No module named 'models'。
# (原 notebook 里这行是注释掉的,写的还是作者自己的路径。)
os.chdir(os.path.expanduser(os.environ.get("SCMEDAL_REPO", "~/scMEDAL_for_scRNAseq")))  # 改成你 clone 官方仓库的位置

# 唯一入口函数:按"模型名 + 数据集名"训练一个预设好的实验。
from models.models import train_model_on_named_experiment
# 导入时打印的 OUTPUTS_DIR 就是结果保存位置:<仓库>/outputs
# 红色 WARNING(Adam 在 M1/M2 上慢、lr 已过时)只是提示,可以忽略。


# =============================================================================
# 段 C:notebook 第 3 个代码格 —— 训练两个模型
# =============================================================================
# "scMEDAL-FE" = 固定效应(fixed effects)模型
# "scMEDAL-RE" = 随机效应(random effects)模型,损失里多了 la_clus_loss(潜空间聚类项)
# "AML" = 数据集名,对应上面检查过的那份数据
# n_latent_dims=50:潜空间(压缩后的表示)有 50 维
# quick=True:快速模式 —— 只跑 1 个 fold、10 个 epoch
#            (论文是 5 fold x 500 epoch,所以这里的结果只是演示,不是论文数字)
scmedalfe_aml = train_model_on_named_experiment(
    "scMEDAL-FE", "AML", model_kwargs={"n_latent_dims": 50}, train_kwargs={"quick": True})
scmedalre_aml = train_model_on_named_experiment(
    "scMEDAL-RE", "AML", model_kwargs={"n_latent_dims": 50}, train_kwargs={"quick": True})

# 每个模型训练完会写三类东西到 outputs/AML/ 下:
#   saved_models/  模型权重
#   latent_space/  训练/验证/测试细胞的 50 维潜空间表示(后面聚类、UMAP、MEC 都读它)
#   figures/       训练曲线等图
# 目录名里带时间戳,例如 ..._2026-10-29_00-15。
#
# 注意两个容易误解的地方:
#  1) 目录名里写着 epochs-500,但那是默认参数拼出来的名字;
#     quick 模式在 models/base.py 里把 model_params['epochs'] 覆盖成了 10,实际只训练 10 个 epoch。
#  2) 日志里的 "Early stopping ... val_loss which is not available" 警告:
#     回调监控的是 val_loss,但模型记录的是 val_total_loss,所以早停和"保存最佳模型"没生效。
#     10 个 epoch 本来就不会早停,对 demo 没影响。
