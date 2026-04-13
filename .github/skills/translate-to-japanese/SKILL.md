---
name: translate-to-japanese
description: 'ファイルの内容を日本語に翻訳する。Use when: translating documentation, README, markdown, or course content to Japanese; converting English text to Japanese; localizing files to Japanese while preserving technical terms like GitHub Copilot, CLI, MCP, API, pytest, YAML, JSON.'
argument-hint: '翻訳対象のファイルパス（例: README.md）'
---

# ファイルを日本語に翻訳する

## このスキルを使う場面

- ドキュメント・README・Markdown ファイルを日本語にしたいとき
- コース教材・解説文を日本語化したいとき
- 英語のコメントや説明文を自然な日本語に変換したいとき

## 翻訳ルール

### 必ず保持する用語（翻訳しない）

以下の技術用語・固有名詞はそのまま英語で残す：

| カテゴリ | 保持する用語の例 |
|----------|----------------|
| 製品名 | GitHub Copilot, GitHub, VS Code, Visual Studio Code |
| プロトコル・仕様 | CLI, MCP, API, REST, HTTP, JSON, YAML, TOML |
| 言語・フレームワーク | Python, JavaScript, C#, Node.js, pytest, npm |
| Git 関連 | git, commit, push, pull request, branch, merge |
| ファイル名・パス | `README.md`, `.github/`, `book_app.py` など |
| コマンド・コード | コードブロック内はすべてそのまま保持 |
| UI 要素 | Copilot Chat, Copilot Edits, Agent Mode |

### 翻訳する部分

- 見出し（Markdown の `#`）
- 説明文・本文
- リストの項目（技術用語を含まない部分）
- テーブルのセル内の説明文
- コードブロック **外** の注釈・解説

## 手順

### 1. 対象ファイルを確認する

```
read_file でファイルの内容を読み込む
```

- ファイルの種類（README, チュートリアル, リファレンス など）を把握する
- コードブロックの範囲を特定する（翻訳対象外）
- YAML frontmatter がある場合は `description` フィールドも翻訳対象とする

### 2. 翻訳方針を決める

| ファイルの性質 | 方針 |
|----------------|------|
| チュートリアル・コース教材 | 親しみやすく、読者に語りかけるトーン |
| リファレンス・仕様書 | 正確・簡潔な技術文体 |
| README | 明快で実用的な日本語 |

### 3. 翻訳を実行する

翻訳品質チェックリスト：

- [ ] 技術用語・固有名詞が英語のまま残っているか
- [ ] コードブロックの内容が変更されていないか
- [ ] Markdown 構造（見出しレベル、リスト、テーブル）が崩れていないか
- [ ] YAML frontmatter の `---` デリミタが維持されているか
- [ ] 自然な日本語として読みやすいか（直訳でなく意訳）
- [ ] 文体が全体で統一されているか（敬体 or 常体）

### 4. ファイルに書き戻す

`replace_string_in_file` または `multi_replace_string_in_file` で変更を適用する。
大きなファイルは章ごとに分割して処理すること。

## 文体ガイドライン

- **教材・チュートリアル**：です・ます調（敬体）を使う
- **技術リファレンス**：だ・である調（常体）または箇条書きで簡潔に
- カタカナ語は一般的な表記に従う（例：インストール、コマンド、ファイル）
- 「〜することができます」より「〜できます」のように簡潔にする
- 受け身表現を多用せず、能動的な文体を優先する

## 注意事項

- 翻訳前に元ファイルのバックアップは不要（Git で管理されているため）
- 複数ファイルを一括翻訳する場合は、ファイルごとに翻訳品質チェックを行う
- 翻訳後は `get_errors` で Markdown の構文エラーがないか確認することを推奨
