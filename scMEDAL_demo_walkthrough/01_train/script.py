# 阶段 1:训练 scMEDAL-FE 和 scMEDAL-RE(对应 notebook 第 3 个代码格)
# 本文件只用于阅读理解。

from models.models import train_model_on_named_experiment

# 第一个参数:模型名。"scMEDAL-FE" = 固定效应(Fixed Effects)模型;"scMEDAL-RE" = 随机效应(Random Effects)模型。
# 第二个参数:命名实验 "AML"(急性髓系白血病,38,417 个细胞 × 2,916 个高变基因,19 个批次/供体)。
# model_kwargs={"n_latent_dims": 50}:把每个细胞压缩成 50 维的潜在表示。
# train_kwargs={"quick": True}:快速模式 = 只跑 1 个 fold、10 个 epoch。
#   论文里是 5 折 × 500 个 epoch(带早停),所以这里的数值只能用来比较模型之间的相对关系,
#   不能和论文里的绝对数字比。
scmedalfe_aml = train_model_on_named_experiment(
    "scMEDAL-FE", "AML",
    model_kwargs={"n_latent_dims": 50},
    train_kwargs={"quick": True},
)
scmedalre_aml = train_model_on_named_experiment(
    "scMEDAL-RE", "AML",
    model_kwargs={"n_latent_dims": 50},
    train_kwargs={"quick": True},
)

# 训练会写出三类文件(都在 outputs/AML/ 下,文件夹名以运行时间结尾):
#   saved_models/  模型权重
#   latent_space/  训练后每个细胞的 50 维潜在表示(后面所有分析读的就是这个)+ history_allfolds.csv(每个 epoch 的损失)
#   figures/       损失曲线等图
