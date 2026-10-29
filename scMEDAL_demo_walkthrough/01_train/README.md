# 阶段 1:训练

代码见 [script.py](script.py)。

## 在做什么

分别训练两个自编码器类模型,输入是每个细胞的 2,916 个基因表达值,输出是 50 维的潜在表示:

- **scMEDAL-FE**(固定效应):从列名(`adv_loss`、`acc`)看,训练里带有一个批次相关的分类/对抗分支,目的是让潜在表示里少含批次信息。这一点是我根据列名推断的,没有读模型代码确认。
- **scMEDAL-RE**(随机效应):列名里有 `la_clus_loss`(潜在空间聚类损失)和 `kld`(KL 散度),用来让潜在空间学到批次相关的结构。同样是根据列名的推断。

quick 模式:1 折 × 10 个 epoch。论文是 5 折 × 500 个 epoch。

## 结果(第 1 个 epoch → 第 10 个 epoch,数据来自 `history_allfolds.csv`)

**FE(`00-15`)**

| 指标 | epoch 0 | epoch 9 |
|---|---|---|
| recon_loss(重建误差) | 0.0452 | 0.0016 |
| val_recon_loss(验证集) | 0.0034 | 0.0015 |
| adv_loss | 2.27 | 1.46 |
| val_total_loss | 0.78 | -0.14 |

**RE(`00-16`)**

| 指标 | epoch 0 | epoch 9 |
|---|---|---|
| recon_loss | 0.9426 | 0.5269 |
| val_recon_loss | 0.2481 | 0.4363 |
| la_clus_loss | 2.861 | 2.024 |
| total_loss | 105.5 | 59.7 |
| val_total_loss | 27.6 | 48.2 |

## 怎么读

- 两个模型的训练损失都在下降,训练是正常的。
- RE 的 `val_recon_loss`(0.25 → 0.44)在上升,而训练的 recon_loss 在下降。这是 10 个 epoch 里能看到的现象,我没有深入分析原因,也没有跑更多轮来验证它是否会继续上升。
- 曲线图见 `results/`:`fe_loss.png`、`fe_recon_loss.png`、`re_loss.png`、`re_loss_KLD.png`。

## 日志里的红色警告

```
Early stopping conditioned on metric `val_loss` which is not available
Can save best model only with val_loss available, skipping
```

早停和"保存最佳模型"这两个回调监控的是 `val_loss`,但模型实际记录的是 `val_total_loss`,所以回调没有生效。quick 模式只有 10 个 epoch,早停本来也不会触发;"保存最佳模型"被跳过意味着保存的是最后一个 epoch 的权重。
