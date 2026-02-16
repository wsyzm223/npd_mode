# 首次推送到 GitHub 的步骤

按顺序在项目目录 `e:\npd_mode` 下执行以下命令（在终端或 Cursor 的终端里均可）。

## 1. 初始化并做第一次提交

```bash
cd e:\npd_mode
git init
git add .
git status
git commit -m "Initial commit: NPD 模型核心逻辑与 Windows 界面"
```

## 2. 关联远程仓库并推送

把下面命令里的 **`<你的仓库URL>`** 换成你在 GitHub 上建好的仓库地址，例如：  
`https://github.com/你的用户名/npd_mode.git`

```bash
git remote add origin <你的仓库URL>
git branch -M main
git push -u origin main
```

若 GitHub 上创建仓库时勾选了「Add a README」，需要先拉再推：

```bash
git remote add origin <你的仓库URL>
git branch -M main
git pull origin main --rebase
git push -u origin main
```

## 3. 推送完成后可在 GitHub 上做的设置

- **About**：点仓库右侧 About 旁的小齿轮，填简短描述，加 Topics（如 `python` `tkinter` `mental-health` `NPD`）。
- **分支保护**：Settings → Branches → Add rule，Branch name 填 `main`，勾选「Require a pull request before merging」和「Require 1 approval」，保存。

---

推送成功后，可以删掉本文件（`GIT_首次推送步骤.md`），或保留作备忘。
