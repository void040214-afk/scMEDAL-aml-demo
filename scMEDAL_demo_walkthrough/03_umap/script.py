# 阶段 3:UMAP 可视化(对应 notebook 第 11、12 个代码格)
# 本文件只用于阅读理解。

# 取训练集(types=["train"])第 1 折(splits=[1])的潜在表示,
# 每个模型用 UMAP 降到 2 维,再分别按 Patient_group / batch / celltype 上色出图。
# 同时还会画一份"原始输入数据 PCA 后再 UMAP"的图作对照(文件名含 input_pca)。
# 图和中间 csv 保存在 outputs/.../AML_demo_mine/umap_19batches_seed_5/
#   plots_axis/   带坐标轴的图    plots_noaxis/  不带坐标轴的图    umap_csv/  UMAP 坐标
# 注意:如果这些 csv 已存在,函数会直接复用而不重新计算。
# 日志里会出现 "Directory does not exist ... splits_2/3/4/5":
# 因为 quick 模式只训练了第 1 折,其他折的目录本来就不存在,不是错误。
processors = aml.umap(model_folder_dict, types=["train"], splits=[1])
processors

# ---- 第 12 个代码格:图片查看器 ----
# 这一格(很长,此处省略)只做展示:用 glob 在 AML_demo_mine 下找出
# *umap*/*plots_axis*/*umap* 的所有图片,缩小成缩略图后嵌进 notebook,每个模型一行。
# 它不会生成任何新文件("no files written")。
