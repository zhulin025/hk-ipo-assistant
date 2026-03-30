# GitHub Pages 配置说明

## 📄 启用 GitHub Pages

由于 `gh` CLI 没有直接启用 Pages 的选项，需要手动配置：

### 方法一：GitHub 网页配置（推荐）

1. 访问仓库：https://github.com/zhulin025/hk-ipo-assistant
2. 点击 **Settings** 标签
3. 左侧菜单选择 **Pages**
4. 在 **Build and deployment** 下：
   - Source: 选择 **Deploy from a branch**
   - Branch: 选择 **gh-pages** 分支，文件夹选择 **/(root)**
5. 点击 **Save**

### 方法二：使用 GitHub API

```bash
# 启用 GitHub Pages
curl -X POST \
  -H "Authorization: Bearer $(gh auth token)" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/zhulin025/hk-ipo-assistant/pages \
  -d '{"source":{"branch":"gh-pages","path":"/"}}'
```

## 🌐 访问地址

启用后，网页应用将在以下地址可用：

**https://zhulin025.github.io/hk-ipo-assistant/**

## 📝 注意事项

1. **静态页面**：GitHub Pages 只能托管静态 HTML/CSS/JS
2. **API 限制**：FastAPI 后端无法在 Pages 上运行
3. **数据源**：需要确保数据源允许跨域访问（CORS）

## 🔧 替代方案

如果需要运行完整的 Web 应用（包括后端 API），建议使用：

- **Vercel** - 支持 Serverless Functions
- **Railway** - 支持完整的应用部署
- **Render** - 免费层级支持 Web 服务

---

*最后更新：2026-03-30*
