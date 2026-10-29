# 阶段 4:genomap(对应 notebook 第 14、15 个代码格)
# 本文件只用于阅读理解。

# genomap:把一个细胞的 2,916 个基因表达值,按基因之间的关系排成一张 2D "基因图像"。
# 这里用它来对比:同一个细胞,在原始输入、FE 重建、以及 RE 重建到不同批次时,基因表达图像有什么变化。
batches = ["AML420B", "BM5", "MUTZ3"]      # 想看的 3 个批次
celltype = ["Mono", "Mono-like"]           # 只取这两类细胞
# 前提:genomap 要用到 FE 和 RE 的重建结果,所以必须先完成阶段 1 的训练
selected_models = {k: model_folder_dict[k] for k in ("scmedalfe", "scmedalre")}

pipeline, summary = aml.genomap(
    selected_models,
    n_batches=19,            # 数据共 19 个批次
    num_iter=200,            # genomap 迭代次数;作者注释:快速测试用 200,否则 100(原文如此,未核对哪个更合适)
    cell_id_col="Cell",      # 元数据里细胞 ID 的列名
    gene_index_col="Gene",   # 基因名的列名
    celltype=["Mono", "Mono-like"],
    batches=batches,
    model="scmedalre",       # 用 RE 的重建作为"换批次后的细胞"
    typ="train",
    split=1,
    add_inputs_fe=True,      # 同时加入原始输入和 FE 重建,方便并排对比
    extra_recon="fe",
    min_val=-1,              # 画图的颜色范围:-1 到 2
    max_val=2,
)
# 日志里 "Selected 1 cell from batch XXX" 表示每个批次只抽到 1 个符合条件的细胞,
# 另外再抽 296 个细胞凑样本;所以最终展示的是少数几个细胞,不是统计结果,只能用来定性观察。

# ---- 第 15 个代码格:显示图片 ----
# 只是用 glob 找到 AML_demo_mine/genomap/genomap_plots/*/genomap_plots_scfewbatches_nogenelabels/*
# 里的图,逐个 display 出来。
