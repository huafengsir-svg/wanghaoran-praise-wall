# 主讲老师好评墙 - 项目说明与部署指南

## 项目概述

这是一个高中在线教育机构主讲老师（王淏然老师）的学员好评墙页面。

- 自动扫描两个好评截图文件夹，生成瀑布流展示页面
- 支持按届别筛选（全部 / 2025届 / 2028届）
- 支持点击查看大图、左右切换
- 采用分页加载：首屏 50 条，点击「加载更多」分批加载

## 当前在线地址

**Netlify（推荐，已部署成功）**：
https://tubular-cheesecake-749230.netlify.app/

**GitHub 仓库**：
https://github.com/huafengsir-svg/wanghaoran-praise-wall

> GitHub Pages 曾尝试启用，但因截图文件较多（438 张）导致构建卡住/失败，最终采用 Netlify 方案。

## 文件结构

```
.
├── index.html                              # 最终生成的 HTML 页面
├── build_praise_wall.py                    # 自动生成 index.html 的脚本
├── praise-wall-deploy.zip                  # 用于 Netlify 部署的压缩包（临时文件）
├── README.md                               # 项目说明
├── AGENTS.md                               # 本文件
├── .nojekyll                               # 禁用 GitHub Pages Jekyll 构建
├── .gitignore
├── 王淏然老师2025届学生好评整理/            # 2025届学员好评截图
└── 王淏然老师2028届学生好评整理/            # 2028届学员好评整理
```

## 本地预览

直接用浏览器打开 `index.html` 即可。

## 更新好评墙

当新增、删除或修改好评截图后，运行：

```bash
cd /Users/wanghuafeng/Desktop/AI项目/主讲老师好评墙
python3 build_praise_wall.py
```

脚本会自动扫描两个截图文件夹，重新生成 `index.html`。

## 部署到 Netlify

当前使用 Netlify Drop 手动部署。Netlify 账号已通过 GitHub 登录：

- GitHub 用户名：`huafengsir-svg`
- Netlify 登录邮箱：`huafengsir@icloud.com`
- 登录方式：Sign in with GitHub

### 部署步骤

1. 确保已运行 `python3 build_praise_wall.py` 生成最新 `index.html`
2. 打包部署文件：

   ```bash
   cd /Users/wanghuafeng/Desktop/AI项目/主讲老师好评墙
   rm -f praise-wall-deploy.zip
   zip -r praise-wall-deploy.zip index.html "王淏然老师2025届学生好评整理" "王淏然老师2028届学生好评整理" -x "*.DS_Store"
   ```

3. 访问 https://app.netlify.com/drop
4. 使用 GitHub 账号登录（账号见上文）
5. 将 `praise-wall-deploy.zip` 拖入上传区域
6. 等待部署完成，获取新的 `xxx.netlify.app` 链接
7. 将新链接更新到本文件和 `README.md`

### 注意事项

- 每次 Drop 会生成一个新的随机子域名站点
- 旧站点可在 Netlify 后台删除或保留
- 如需固定域名，可后续配置自定义域名

## 常见修改

### 修改老师姓名

编辑 `build_praise_wall.py` 中的 `TEACHER_NAME` 变量：

```python
TEACHER_NAME = "王淏然"
```

然后重新生成 `index.html` 并部署。

### 修改分页数量

编辑 `build_praise_wall.py` 中的 `PAGE_SIZE`：

```javascript
const PAGE_SIZE = 50;
```

然后重新生成并部署。

### 添加新的届别/分类

1. 在 `build_praise_wall.py` 的 `YEARS` 列表中添加新分类：

   ```python
   YEARS = [
       ("2025届", "王淏然老师2025届学生好评整理"),
       ("2028届", "王淏然老师2028届学生好评整理"),
       ("2031届", "王淏然老师2031届学生好评整理"),
   ]
   ```

2. 创建对应文件夹并放入截图
3. 重新生成并部署

### 修改样式/布局

直接修改 `build_praise_wall.py` 中的 CSS 和 HTML 模板部分，然后重新生成 `index.html`。

## 技术栈

- 纯静态 HTML + CSS + JavaScript
- Python 3 用于生成页面
- 无外部依赖

## 已知问题

- GitHub Pages 不适合本项目：截图文件较多时构建耗时极长且容易失败
- 建议始终使用 Netlify 部署
