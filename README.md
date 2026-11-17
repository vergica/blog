# 梅岭随记

Hugo + PaperMod 静态博客，正式域名 https://northvision.cn/ 。

## 编辑与发布

在鸡哥编辑 content 下的文章与 static 下的附件，先本地预览，再提交并推送到 main。GitHub Actions 会自动构建并部署 GitHub Pages。构建固定使用 Hugo 0.167.0 extended；主题文件随仓库保存。

## 本地预览

使用 Hugo 0.167.0 extended 运行 `hugo server --bind 127.0.0.1`。生成的 public 与 resources 不提交。草稿可通过文章头部的 draft 字段控制，但公开仓库中的源文件本身仍然公开。

GitHub Pages 初次部署时使用项目预览地址；绑定自有域名后，自动构建会使用 Pages 提供的正式地址。切换 DNS 前先核对预览结果。
