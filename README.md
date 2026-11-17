# 梅岭随记

Hugo + PaperMod 静态博客，正式域名 https://northvision.cn/ 。

## 编辑与发布

在鸡哥编辑 content 下的文章与 static 下的附件，先本地预览，再提交并推送到 main。GitHub Actions 会自动构建并部署 GitHub Pages。构建固定使用 Hugo 0.167.0 extended；主题文件随仓库保存。

## 本地预览

使用 Hugo 0.167.0 extended 运行 `hugo server --bind 127.0.0.1`。生成的 public 与 resources 不提交。草稿可通过文章头部的 draft 字段控制，但公开仓库中的源文件本身仍然公开。

正式域名为 https://northvision.cn/ 。main 推送后自动发布，构建固定生成 HTTPS 链接。初次迁移已通过 GitHub 预览地址验证，正式域名的 DNS 由 DNSPod 管理。
