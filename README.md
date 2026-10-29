# scMEDAL AML demo 复现(BMI5101 小组作业)

复现 [scMEDAL](https://github.com/DeepLearningForPrecisionHealthLab/scMEDAL_for_scRNAseq) 官方 `demo/demo_aml.ipynb`(AML 数据,38,417 细胞 × 2,916 基因,19 个批次),并把 notebook 拆成 5 个阶段便于阅读。原项目与论文版权归 UTSW 作者所有,许可见 [UTSW_License.txt](UTSW_License.txt)(仅限学术和研究用途)。

## 结果摘要(quick 模式:1 折 × 10 epoch)

- scMEDAL-FE 的潜在空间批次混合得更好、细胞类型更清楚;scMEDAL-RE 的潜在空间按批次分成小团。
- 用 FE + RE 合起来预测 Patient_group,准确率从 84.94% 升到 99.14%。
- quick 模式只适合比较两个模型的相对关系,不能与论文绝对数字比较。

## 目录

| 路径 | 内容 |
|---|---|
| `READING_ORDER.md` | 阅读顺序 |
| `scMEDAL_demo_walkthrough/` | 00–05 六个阶段:`script.py`(仅供阅读)、`README.md`、结果图表 |
| `scMEDAL_setup/` | 环境脚本 `setup_scMEDAL38.sh`、`verify_env.py`、`requirements_mac.txt`、`demo_steps_so_far.py` |
| `patches/mac_compat.patch` | 官方仓库在 Apple Silicon 上运行所需的两处改动 |
| `notebook/demo_aml_mac_run.ipynb` | 我们实际跑过的 notebook(含输出) |

## 复现步骤

1. 设置仓库位置(可选,默认 `~/scMEDAL_for_scRNAseq`):`export SCMEDAL_REPO=/你的路径`
2. `bash scMEDAL_setup/setup_scMEDAL38.sh`:clone 官方仓库、建 Python 3.8.20 环境、装依赖(Apple Silicon Mac)。
3. 打补丁:在官方仓库根目录运行 `git apply <本仓库>/patches/mac_compat.patch`
   - `random_effects.py`:`tensorflow_addons` 导入改为可选(它在 Apple Silicon 上无预编译包,且代码未实际使用)。
   - `utils/defaults.py`:`ROOT_PATH` 默认取仓库目录,可用 `SCMEDAL_ROOT` 覆盖。
4. 下载数据:Figshare DOI [10.6084/m9.figshare.28414367](https://doi.org/10.6084/m9.figshare.28414367),放到官方仓库 `data/AML_data/`。本仓库不含数据和训练模型。
5. `python scMEDAL_setup/verify_env.py` 验证环境,然后运行官方 notebook。

## 注意

同一模型在 `outputs/` 里有多次运行,详见 `scMEDAL_demo_walkthrough/README.md` 的"运行批次"说明。
