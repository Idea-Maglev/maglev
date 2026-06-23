#!/bin/bash
set -e

UPSTREAM_BASE=${MAGLEV_UPSTREAM_URL:-"https://raw.githubusercontent.com/Idea-Maglev/maglev/release"}
INSTALLER_URL="${UPSTREAM_BASE}/maglev_installer.py"
TEMP_INSTALLER="/tmp/maglev_installer_$$.py"

OKCYAN='\033[96m'
OKGREEN='\033[92m'
FAIL='\033[91m'
ENDC='\033[0m'

echo -e "${OKCYAN}Maglev Distribution Engine (Shell Entry)${ENDC}"
echo "========================================"

if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${FAIL}❌ 错误: 未找到 Python。请安装 Python 3.6+ 后重试。${ENDC}"
    exit 1
fi

echo -e "📥 下载安装器脚本..."
if ! curl -sSL "$INSTALLER_URL" -o "$TEMP_INSTALLER"; then
    echo -e "${FAIL}❌ 错误: 无法从远端下载安装器。请检查网络或 MAGLEV_UPSTREAM_URL 环境变量。${ENDC}"
    exit 1
fi

$PYTHON_CMD "$TEMP_INSTALLER" "$@"
EXIT_CODE=$?

rm -f "$TEMP_INSTALLER"
exit $EXIT_CODE
