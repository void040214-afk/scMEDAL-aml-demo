# 阶段 2:聚类分数(对应 notebook 第 9 个代码格)
# 本文件只用于阅读理解。`aml`、`model_folder_dict` 来自 00_setup/script.py。

# 读取两个模型各自的 50 维潜在空间,用"批次"和"细胞类型"两种标签分别计算聚类质量:
#   1/db        = Davies-Bouldin 指数的倒数(越大越好)
#   ch          = Calinski-Harabasz 指数(越大越好)
#   silhouette  = 轮廓系数(-1 到 1,越大越好)
# 含义:分数越高 = 按这种标签分组后,组内更紧、组间更开。
#   - 对"批次"分数高 = 潜在空间里能按批次分开(批次信息被编码了)
#   - 对"细胞类型"分数高 = 潜在空间里能按细胞类型分开(生物学信息被保留了)
res = aml.clustering_scores(model_folder_dict)

# 结果表同时写到 outputs/.../AML_demo_mine/ 下的 test_allscores.csv 等文件。
# 只跑了 1 个 fold,所以置信区间(CI_lower / CI_upper)全是 NaN,这是正常的;
# 默认按 5 折、自由度 4 计算置信区间(见 utils.compare_results_utils.process_confidence_intervals)。
res
