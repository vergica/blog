#!/bin/bash
# 梅岭随记 一键部署脚本
# 用法: ./deploy.sh
set -e

BLOG_DIR="$HOME/blog"
WEB_DIR="/var/www/northvision"

echo "🔨 构建 Hugo 站点..."
cd "$BLOG_DIR"
hugo --logLevel info

echo "📦 同步到 Web 目录..."
sudo rsync -a --delete "$BLOG_DIR/public/" "$WEB_DIR/"
sudo chown -R caddy:caddy "$WEB_DIR"

echo "✅ 部署完成! https://northvision.cn"
