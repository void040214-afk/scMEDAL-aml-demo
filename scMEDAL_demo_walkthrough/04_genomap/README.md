# 阶段 4:genomap

代码见 [script.py](script.py)。

## 在做什么

genomap 把一个细胞的 2,916 个基因表达值排成一张 2D 的"基因图像"。这里取 Mono / Mono-like 两类细胞,把**同一个细胞**在这些状态下的图像并排放在一起:

1. 原始输入(`input_train`)
2. FE 的重建(`fe_ae_recon_train`)
3. RE 重建成不同批次(`recon_batch_train_BM5`、`..._MUTZ3`、`..._AML420B`)

标题里红色的那张是该细胞原本所在的批次(`original batch`),其余带 `cf batch` 的是"换成别的批次后"的重建(cf = counterfactual,反事实)。颜色范围固定在 -1 到 2。

## 结果:`results/genomap_1.png` ~ `genomap_4.png`

我只仔细看了第 1 张(细胞 `MUTZ3_TAAATCTGATTT_Mono-like`),其余 3 张结构相同,我没有逐张查看:

![](results/genomap_1.png)

- 第 1、2 张(输入和 FE 重建)看起来很相似,整体偏平滑,说明 FE 重建基本还原了输入。
- 后 3 张(RE 重建到不同批次)对比度明显更强,边缘出现大片亮黄色,而且三个批次之间的图案不同。这说明 RE 的重建里带有批次特异的成分,换批次后基因表达的"样子"会变。
- 也就是说,RE 能把同一个细胞"换"到不同批次再重建出来,不同批次的结果有可见差别。这是对这一张图的观察,不是统计结论。

## 注意

- 日志显示每个目标批次只抽到 1 到 2 个符合条件的细胞,并出现了 `No cells available ... Skipping batch` 的提示,另外随机补了 296 个细胞凑样本(日志原文没有完全看懂每一行的含义),所以这是几个细胞的**定性**展示,不能代表整体。
- `num_iter=200` 是作者标注的"快速测试"设置。
- 输出目录里除了这 4 张图,还有 `singlecell_gene_std_acrossbatches/` 等其他图,这次没有展开。
