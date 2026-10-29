# 阶段 0:准备工作(对应 notebook 第 1、7 格附近)
# 本文件只用于阅读理解,不是为独立运行设计的。

import os

# 必须先切到仓库根目录:仓库里的 models/ utils/ analysis/ 是普通文件夹(不是 pip 安装的包),
# 只有当前目录是仓库根时 `import models` 才找得到。
# 原 notebook 这里写的是作者服务器上的路径(被注释掉),要改成你自己的。
os.chdir(os.path.expanduser(os.environ.get("SCMEDAL_REPO", "~/scMEDAL_for_scRNAseq")))  # 改成你 clone 官方仓库的位置

# 唯一的"入口函数":按名字训练某个模型 + 某个数据集的"命名实验"。
# 命名实验里已经写好了数据路径、批次数(AML = 19 个批次)、分类数等配置(见 utils/defaults.py)。
from models.models import train_model_on_named_experiment

# ---- 训练完成之后,notebook 里需要手动指定"用哪一次训练的结果做分析" ----
# 每次训练都会在 outputs/AML/latent_space/<数据集>/<模型名>/ 下新建一个以时间结尾的文件夹,
# 所以必须把文件夹名填进字典,否则后面的分析找不到文件(原 notebook 里填的是作者自己的日期)。
# 注意:同一模型可以有很多次运行,选错时间就等于分析了别的模型。
model_folder_dict = {
    "scmedalfe": "run_crossval_loss_gen_weight-1_loss_recon_weight-1000_loss_class_weight-1_n_latent_dims-50_layer_units-512-132_scaling-min_max_model_type-scmedalfe_batch_size-512_epochs-500_patience-30_sample_size-10000_2026-10-29_00-15",
    "scmedalre": "run_crossval_loss_recon_weight-110_loss_latent_cluster_weight-0.1_n_latent_dims-50_layer_units-512-132_scaling-min_max_batch_size-512_epochs-500_patience-30_sample_size-10000_2026-10-29_00-16",
}

# ---- 创建分析对象(notebook 第 7 格)----
import analysis.analysis as aa

# analysis_name 决定结果写到 outputs/AML/compare_models/<数据集>/<analysis_name>/ 。
# 用新名字(AML_demo_mine)是为了不和别人已有的结果混在一起:
# aml.umap() 发现同名文件已存在时会直接复用,不会重新计算。
analysis_name = "AML_demo_mine"
aml = aa.AMLAnalysis(model_folder_dict, analysis_name)
