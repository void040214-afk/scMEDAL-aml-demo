# scMEDAL AML demo 资料包 —— 阅读顺序

原项目:https://github.com/DeepLearningForPrecisionHealthLab/scMEDAL_for_scRNAseq

1. `scMEDAL_demo_walkthrough/README.md`  —— 总览与整体流程
2. 按阶段阅读,每个阶段先读 README,再看 script.py 和 results/:
   - `00_setup`          准备(只有 script.py)
   - `01_train`          训练 FE / RE
   - `02_clustering_scores`  聚类分数
   - `03_umap`           UMAP 图
   - `04_genomap`        genomap 图
   - `05_mec`            MEC 分类结果
3. 想复现环境:`scMEDAL_setup/`
   - `setup_scMEDAL38.sh`  环境配置脚本(Apple Silicon Mac,Python 3.8.20,每步有注释)
   - `verify_env.py`       验证环境
   - `demo_steps_so_far.py`  数据检查、notebook 前几格的带注释记录
   - `requirements_mac.txt`  适配 Mac 后的依赖(由官方 scMEDAL_requirements.txt 修改而来)
4. 想看真实代码:克隆上面的仓库,看 `demo/demo_aml.ipynb`、`models/`、`analysis/`、`utils/defaults.py`

说明:
- 拆解里的 script.py 仅用于阅读,不能独立运行。
- 结果是 quick 模式(1 折 × 10 个 epoch),只适合比较两个模型的相对关系。
- 脚本里的仓库路径默认是 `~/scMEDAL_for_scRNAseq`,可用环境变量 `SCMEDAL_REPO` 指向你 clone 的位置。
- 本资料包不含数据(AML 预处理数据需从 Figshare DOI 10.6084/m9.figshare.28414367 下载)和训练模型。
