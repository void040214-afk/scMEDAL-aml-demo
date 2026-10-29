# 阶段 2:聚类分数

代码见 [script.py](script.py),完整表见 [results_test_allscores.csv](results_test_allscores.csv)。

## 在做什么

对两个模型的 50 维潜在空间,分别按"批次"和"细胞类型"两种标签打分,3 个指标**都是越大越好**:

| 指标 | 含义 |
|---|---|
| 1/db | Davies-Bouldin 指数的倒数 |
| ch | Calinski-Harabasz 指数 |
| silhouette | 轮廓系数,范围 -1 到 1 |

某个标签的分数高,说明潜在空间里按这个标签分组后,组内更紧、组间更开。

## 结果(两张截图里的数值)

| 标签 | 指标 | scMEDAL-FE | scMEDAL-RE |
|---|---|---|---|
| batch | 1/db | 0.09 | 0.49 |
| batch | ch | 116.2 | 1779.5 |
| batch | silhouette | -0.18 | 0.42 |
| celltype | 1/db | 0.18 | 0.19 |
| celltype | ch | 1006.41 | 224.11 |
| celltype | silhouette | -0.01 | -0.05 |

(batch 和 celltype 的分组是我按截图里表头的位置判断的。)

## 怎么读

- **批次:RE 三项都明显更高**。RE 的潜在空间里批次结构强。notebook 注释也说"RE 的批次聚类分数都比 FE 高"。
- **细胞类型:FE 的 ch 更高(1006 对 224)**,1/db 几乎一样,silhouette 两个都接近 0。
- 这与"FE 少含批次信息、RE 编码批次信息"的设计意图一致(这是我对方法的理解,不是这张表本身证明的)。
- 所有置信区间是 NaN:只跑了 1 折。
- 细胞类型的 silhouette 两个都接近 0,说明在 10 个 epoch 的训练下,没有哪个模型把细胞类型分得很干净;这是训练很短造成的还是别的原因,这次没有验证。
