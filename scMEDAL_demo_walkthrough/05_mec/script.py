# 阶段 5:MEC 分类器(对应 notebook 第 17、18 个代码格)
# 本文件只用于阅读理解。`model_paths` 在 notebook 第 5 格由 model_folder_dict 拼出来,
# 指向两个模型的潜在空间文件夹。

from models.models import train_model_on_named_experiment

# MEC(Mixed Effects Classifier):在已经训练好的潜在表示上,再训练一个分类器,
# 目标是预测 Patient_group(3 类:AML / control / cellline),看潜在表示里有多少"患者组"信息。
# 汇总表里的指标名带 RF(RFAccuracy 等),这里的分类器是随机森林。

# 实验 A:只用 FE 的潜在空间
train_model_on_named_experiment(
    "MEC", "AML",
    train_kwargs={"quick": True, "results_path_dict": model_paths},
    model_kwargs={
        "n_pred": 3,                       # 预测 3 个类别
        "bio_col": "Patient_group",        # 预测目标列
        "models_list": list(model_paths.keys()),
        "latent_keys_config": {"fe_latent": "scmedalfe_latent"},   # 只喂 FE 的潜在表示
    },
)

# 实验 B:FE + RE 两个潜在空间拼起来
train_model_on_named_experiment(
    "MEC", "AML",
    train_kwargs={"quick": True, "results_path_dict": model_paths},
    model_kwargs={
        "n_pred": 3,
        "bio_col": "Patient_group",
        "models_list": list(model_paths.keys()),
        "latent_keys_config": {"fe_latent": "scmedalfe_latent", "re_latent": "scmedalre_latent"},
    },
)

# 汇总所有 MEC 运行的结果(在测试集上)
from utils.compare_results_utils import get_all_mec_metrics
df, _ = get_all_mec_metrics(AML_OUTPUTS_DIR, AML_EXPERIMENT_NAME, split="test")
df
# 重要:这个函数会汇总 mec/ 文件夹里"所有"运行,不只是这一次,
# 所以表里每种配置会出现多行(不同运行时间)。要看自己的,按 run_name 末尾的时间挑。
