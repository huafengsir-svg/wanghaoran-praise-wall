# 王淏然老师 · 学员好评墙

高中在线教育机构主讲老师好评墙页面，自动汇总学员好评截图，以瀑布流形式展示。

## 在线访问

部署后访问链接：TODO

## 项目结构

```
.
├── index.html                      # 好评墙页面
├── build_praise_wall.py            # 自动生成 index.html 的脚本
├── 王淏然老师2025届学生好评整理/    # 2025届学员好评截图
└── 王淏然老师2028届学生好评整理/    # 2028届学员好评截图
```

## 本地预览

直接用浏览器打开 `index.html` 即可。

## 更新好评墙

新增或删除截图后，运行：

```bash
python3 build_praise_wall.py
```

脚本会自动扫描两个截图文件夹并重新生成 `index.html`。

## 部署到 GitHub Pages

1. 将本仓库推送到 GitHub
2. 进入仓库 Settings → Pages
3. Source 选择 `Deploy from a branch`，Branch 选择 `main`，路径选择 `/(root)`
4. 保存后即可通过 `https://你的用户名.github.io/仓库名/` 访问
