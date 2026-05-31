#!/bin/bash
# OPC Insights 自动推送脚本
# 网络恢复后自动推送到 GitHub

cd ~/opc-insights

echo "🔄 尝试推送到 GitHub..."

# 方法1: 禁用代理推送
git -c http.proxy= -c https.proxy= push --set-upstream origin main

if [ $? -eq 0 ]; then
    echo "✅ 推送成功！"
else
    echo "⚠️ 推送失败，等待5分钟后重试..."
    sleep 300
    git -c http.proxy= -c https.proxy= push --set-upstream origin main
    if [ $? -eq 0 ]; then
        echo "✅ 重试推送成功！"
    else
        echo "❌ 推送失败，请手动检查网络后运行: cd ~/opc-insights && git push"
    fi
fi