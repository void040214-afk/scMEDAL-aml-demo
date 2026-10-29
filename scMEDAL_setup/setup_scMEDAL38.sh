#!/bin/bash
# =============================================================================
# scMEDAL demo 环境配置(Apple Silicon Mac, Python 3.8.20)
# 用法:bash setup_scMEDAL38.sh
# 每一步都可以单独复制到终端执行;脚本遇到错误会立刻停止(set -e)。
# =============================================================================
set -e

REPO_DIR="${SCMEDAL_REPO:-$HOME/scMEDAL_for_scRNAseq}"   # 仓库位置
ENV_NAME="scMEDAL38"                                     # conda 环境名
MIRROR="https://pypi.tuna.tsinghua.edu.cn/simple"        # pip 镜像;在国外/镜像报错时清空: MIRROR=""

# -----------------------------------------------------------------------------
# 第 1 步:克隆仓库
# --depth 1 只拉最新一次提交,体积小、网络差时更快。
# 之前的 clone 只有 .git 没有文件(中途断了),所以才需要重新克隆。
# -----------------------------------------------------------------------------
if [ ! -f "$REPO_DIR/README.md" ]; then
  rm -rf "$REPO_DIR"
  git clone --depth 1 https://github.com/DeepLearningForPrecisionHealthLab/scMEDAL_for_scRNAseq.git "$REPO_DIR"
fi

# -----------------------------------------------------------------------------
# 第 2 步:创建 conda 环境(Python 3.8.20)
# 作者 README 指定 3.8.20。TensorFlow 2.13.1 只支持 Python 3.8~3.11,
# 所以不能用 3.13。3.8 虽然已 EOL(没有安全更新),但 PyPI 上
# tensorflow / numba / numpy / scipy / h5py 都仍有 3.8 + arm64 的预编译包。
# -----------------------------------------------------------------------------
if ! conda env list | grep -q "^$ENV_NAME "; then
  conda create -n "$ENV_NAME" python=3.8.20 -y
fi
PY="/opt/anaconda3/envs/$ENV_NAME/bin/python"   # 直接用环境里的 python/pip,避免装到别的环境
PIP="$PY -m pip"

# -----------------------------------------------------------------------------
# 第 3 步:生成适合 Mac 的 requirements_mac.txt
# 作者给的 scMEDAL_requirements.txt 是 Linux 上的 `pip freeze`,直接装会失败:
#   (a) 含 `xxx @ file:///home/conda/...` 本地路径包(ipython、jedi、six 等),你的机器上不存在;
#       它们会作为别的包的依赖被自动装上,所以直接删掉。
#   (b) genomap 是 git 链接,单独装(第 5 步),避免 pip 解析时拉 GitHub 卡住。
#   (c) pysam / nipype / nibabel / lxml 等神经影像包在 arm64 上没有预编译包要编译,
#       而且 demo 用不到,删掉。
# -----------------------------------------------------------------------------
REQ_SRC="$REPO_DIR/scMEDAL_env/scMEDAL_requirements.txt"
REQ_MAC="$REPO_DIR/scMEDAL_env/requirements_mac.txt"
grep -vE "file://|@ git|^(pysam|nipype|nibabel|prov|lxml|rdflib|pydot|etelemetry|ci-info|traits|simplejson|looseversion|texttable|pipdeptree|stdlib-list|networkx)==" \
  "$REQ_SRC" > "$REQ_MAC"

# 两处必须手动修正(作者的 freeze 文件本身有问题):
#   (d) exceptiongroup 1.3.0 要求 typing_extensions>=4.6,但 TensorFlow 2.13 要求 <4.6(文件里固定 4.5.0),
#       互相冲突 -> 降到 1.2.2(它不依赖 typing_extensions)。
sed -i '' 's/^exceptiongroup==1.3.0/exceptiongroup==1.2.2/' "$REQ_MAC"
#   (e) Apple Silicon 上 `tensorflow==2.13.1` 只是个壳,真正依赖 tensorflow-macos==2.13.1,
#       而 Python 3.8 没有这个版本(最高 2.13.0)-> 直接装 tensorflow-macos==2.13.0。
sed -i '' 's/^tensorflow==2.13.1/tensorflow-macos==2.13.0/' "$REQ_MAC"

# -----------------------------------------------------------------------------
# 第 4 步:安装依赖
# 清华镜像加速;--timeout/--retries 应对网络不稳。约 167 个包,TensorFlow 最大。
# -----------------------------------------------------------------------------
if [ -n "$MIRROR" ]; then
  $PIP install -r "$REQ_MAC" -i "$MIRROR" --timeout 120 --retries 10
else
  $PIP install -r "$REQ_MAC" --timeout 120 --retries 10
fi

# -----------------------------------------------------------------------------
# 第 5 步:安装 genomap(固定到作者使用的那个提交)
# --no-deps:不让它改动我们已经固定好的包版本。
# -----------------------------------------------------------------------------
$PIP install "git+https://github.com/xinglab-ai/genomap.git@d09395a04c26c02b73c8efe9db7dbce24306305d" --no-deps

# -----------------------------------------------------------------------------
# 第 6 步:注册 Jupyter 内核,notebook 里选 "Python (scMEDAL38)"
# -----------------------------------------------------------------------------
$PY -m ipykernel install --user --name "$ENV_NAME" --display-name "Python ($ENV_NAME)"

# -----------------------------------------------------------------------------
# 第 7 步:验证(导入所有关键包)
# -----------------------------------------------------------------------------
$PY "$(dirname "$0")/verify_env.py"

# -----------------------------------------------------------------------------
# 之后还需要(不在本脚本里):
#  A) ROOT_PATH:README 要求把 utils/defaults.py 里的 ROOT_PATH 改成仓库路径。
#  B) 数据:从 Figshare(DOI 10.6084/m9.figshare.28414367)下载 AML 预处理数据,
#     解压到 $REPO_DIR/data/AML_data/log_transformed_2916hvggenes/ (含 exprMatrix.npy、meta.csv、splits/split_1..5)
#  C) 运行 demo/demo_aml.ipynb(内核选 Python (scMEDAL38))
# -----------------------------------------------------------------------------
