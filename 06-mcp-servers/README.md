![Chapter 06: MCP Servers](images/chapter-header.png)

> **Copilot が GitHub issues を読み込み、データベースを確認し、PR を作成できたら... すべてターミナルから操作できたらどうでしょう？**

これまで Copilot は、`@` で参照したファイル・会話履歴・トレーニングデータなど、直接渡された情報しか扱えませんでした。しかし、Copilot 自身が GitHub リポジトリを確認したり、プロジェクトファイルを参照したり、ライブラリの最新ドキュメントを調べたりできるとしたら、どうなるでしょうか？

それを実現するのが MCP（Model Context Protocol）です。MCP は Copilot を外部サービスに接続し、リアルタイムの実データにアクセスできるようにする仕組みです。Copilot が接続する各サービスを「MCP サーバー」と呼びます。この章では、いくつかの接続を設定し、Copilot がどれほど強力になるかを体験します。

> 💡 **MCP をすでにご存知の方は？** [クイックスタート](#-use-the-built-in-github-mcp) に飛んで動作確認とサーバー設定を始めましょう。

## 🎯 学習目標

この章を終えると、以下のことができるようになります：

- MCP とは何か、なぜ重要かを理解する
- `/mcp` コマンドで MCP サーバーを管理する
- GitHub・ファイルシステム・ドキュメント用の MCP サーバーを設定する
- book app プロジェクトで MCP を活用したワークフローを使う
- カスタム MCP サーバーをいつ・どのように作るかを理解する（オプション）

> ⏱️ **所要時間の目安**：約50分（読書15分 + ハンズオン35分）

---

## 🧩 現実世界の例え：ブラウザ拡張機能

<img src="images/browser-extensions-analogy.png" alt="MCP Servers are like Browser Extensions" width="800"/>

MCP サーバーをブラウザの拡張機能のようなものと考えてみましょう。ブラウザ単体でもウェブページを表示できますが、拡張機能を使うと追加のサービスに接続できます：

| ブラウザ拡張機能 | 接続先 | MCP の対応 |
|-------------------|---------------------|----------------|
| パスワードマネージャー | パスワード保管庫 | **GitHub MCP** → リポジトリ・issues・PR |
| Grammarly | 文章解析サービス | **Context7 MCP** → ライブラリドキュメント |
| ファイルマネージャー | クラウドストレージ | **Filesystem MCP** → ローカルプロジェクトファイル |

拡張機能がなくてもブラウザは十分に使えますが、拡張機能を加えると格段にパワフルになります。MCP サーバーも Copilot に対して同じことをします。GitHub の issues・ファイルシステム・最新ドキュメントなど、リアルなデータソースに接続できるようになります。

***MCP サーバーは Copilot を外の世界—GitHub、リポジトリ、ドキュメント—とつなぎます***

> 💡 **重要なポイント**：MCP がなければ、Copilot は `@` で明示的に共有したファイルしか参照できません。MCP があれば、プロジェクトを自律的に探索し、GitHub リポジトリを確認し、ドキュメントを調べることができます—すべて自動的に。

---

<img src="images/quick-start-mcp.png" alt="Power cable connecting with bright electrical spark surrounded by floating tech icons representing MCP server connections" width="800"/>

# クイックスタート：30秒で MCP を体験

## 組み込みの GitHub MCP サーバーを使ってみよう
設定する前に、まず MCP を実際に動かしてみましょう。
GitHub MCP サーバーはデフォルトで組み込まれています。次のコマンドを試してみてください：

```bash
copilot
> List the recent commits in this repository
```

Copilot が実際のコミットデータを返したなら、MCP が動作しています。これが GitHub MCP サーバーがあなたの代わりに GitHub にアクセスしている様子です。ただし、GitHub は *1つ* のサーバーに過ぎません。この章では、さらに多くのサーバー（ファイルシステムアクセス・最新ドキュメントなど）を追加して、Copilot をさらに強力にする方法を学びます。

---

## `/mcp show` コマンド

`/mcp show` を使うと、設定済みの MCP サーバーと有効・無効の状態を確認できます：

```bash
copilot

> /mcp show

MCP Servers:
✓ github (enabled) - GitHub integration
✓ filesystem (enabled) - File system access
```

> 💡 **GitHub サーバーしか表示されない場合**、それは正常です！追加の MCP サーバーをまだ設定していなければ、GitHub のみが表示されます。次のセクションで追加していきましょう。

> 📚 **MCP 管理コマンドをすべて確認したい方**は、チャット内の `/mcp` スラッシュコマンド、またはターミナルから直接 `copilot mcp` コマンドで管理できます。この章の末尾にある[コマンドリファレンス](#-additional-mcp-commands)をご覧ください。

<details>
<summary>🎬 動作を確認する</summary>

![MCP Status Demo](images/mcp-status-demo.gif)

*デモの出力はあくまで一例です。モデル・ツール・応答は実際と異なる場合があります。*

</details>

---

## MCP で何が変わるか？

MCP があるとないとでは、実際にこれだけ違います：

**MCP なし：**
```bash
> What's in GitHub issue #42?

"I don't have access to GitHub. You'll need to copy and paste the issue content."
```

**MCP あり：**
```bash
> What's in GitHub issue #42 of this repository?

Issue #42: Login fails with special characters
Status: Open
Labels: bug, priority-high
Description: Users report that passwords containing...
```

MCP によって、Copilot は実際の開発環境を認識できるようになります。

> 📚 **公式ドキュメント**：[About MCP](https://docs.github.com/copilot/concepts/context/mcp) で MCP と GitHub Copilot の連携についてより深く学べます。

---

# MCP サーバーの設定

<img src="images/configuring-mcp-servers.png" alt="Hands adjusting knobs and sliders on a professional audio mixing board representing MCP server configuration" width="800"/>

MCP の動作を確認したところで、追加のサーバーを設定していきましょう。このセクションでは、設定ファイルの形式と新しいサーバーの追加方法を説明します。

---

## MCP 設定ファイル

MCP サーバーは `~/.copilot/mcp-config.json`（ユーザーレベル、すべてのプロジェクトに適用）または `.vscode/mcp.json`（プロジェクトレベル、現在のワークスペースのみ）で設定します。

```json
{
  "mcpServers": {
    "server-name": {
      "type": "local",
      "command": "npx",
      "args": ["@package/server-name"],
      "tools": ["*"]
    }
  }
}
```

*ほとんどの MCP サーバーは npm パッケージとして配布されており、`npx` コマンドで実行します。*

<details>
<summary>💡 <strong>JSON が初めての方へ</strong> クリックして各フィールドの意味を確認する</summary>

| フィールド | 意味 |
|-------|---------------|
| `"mcpServers"` | すべての MCP サーバー設定のコンテナ |
| `"server-name"` | 任意の名前（例：「github」、「filesystem」） |
| `"type": "local"` | サーバーがローカルマシンで動作する |
| `"command": "npx"` | 実行するプログラム（npx は npm パッケージを実行する） |
| `"args": [...]` | コマンドに渡す引数 |
| `"tools": ["*"]` | このサーバーのすべてのツールを許可する |

**JSON の重要なルール：**
- 文字列にはダブルクォート `"` を使う（シングルクォートは不可）
- 最後の項目にカンマをつけない
- 有効な JSON であること（不安な場合は [JSON バリデーター](https://jsonlint.com/) を使う）

</details>

---

## MCP サーバーの追加

GitHub MCP サーバーは組み込み済みで設定不要です。以下は追加できるサーバーです。**興味のあるものを選ぶか、順番に進めてください。**

| やりたいこと | 移動先 |
|---|---|
| Copilot にプロジェクトファイルを参照させたい | [Filesystem サーバー](#filesystem-server) |
| 最新のライブラリドキュメントを取得したい | [Context7 サーバー](#context7-server-documentation) |
| オプションの拡張（カスタムサーバー、web_fetch）を試したい | [応用編](#beyond-the-basics) |

<details>
<summary><strong>Filesystem サーバー</strong> - Copilot にプロジェクトファイルを参照させる</summary>
<a id="filesystem-server"></a>

### Filesystem サーバー

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    }
  }
}
```

> 💡 **`.` パスについて**：`.` は「カレントディレクトリ」を意味します。Copilot は起動した場所を基点にファイルにアクセスします。Codespace では、ワークスペースのルートになります。`/workspaces/copilot-cli-for-beginners` のように絶対パスを指定することもできます。

`~/.copilot/mcp-config.json` に追加して Copilot を再起動してください。

</details>

<details>
<summary><strong>Context7 サーバー</strong> - 最新のライブラリドキュメントを取得する</summary>
<a id="context7-server-documentation"></a>

### Context7 サーバー（ドキュメント）

Context7 は、人気のフレームワークやライブラリの最新ドキュメントへのアクセスを Copilot に提供します。古くなっている可能性のあるトレーニングデータに頼るのではなく、実際の最新ドキュメントを取得します。

```json
{
  "mcpServers": {
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

- ✅ **API キー不要** 
- ✅ **アカウント不要** 
- ✅ **コードはローカルに保持**

`~/.copilot/mcp-config.json` に追加して Copilot を再起動してください。

</details>

<details>
<summary><strong>応用編</strong> - カスタムサーバーと Web アクセス（オプション）</summary>
<a id="beyond-the-basics"></a>

上記のコアサーバーに慣れたら試せるオプション機能です。

### Microsoft Learn MCP サーバー

これまで紹介したMCPサーバー（filesystem、Context7）はすべてローカルマシンで動作します。しかし MCP サーバーはリモートでも動作します。つまり、URL を指定するだけで Copilot CLI が残りを処理してくれます。`npx` も `python` も不要で、ローカルプロセスや依存関係のインストールも必要ありません。

[Microsoft Learn MCP Server](https://github.com/microsoftdocs/mcp) はその好例です。Copilot CLI が公式 Microsoft ドキュメント（Azure・Microsoft Foundry などの AI トピック・.NET・Microsoft 365 など）に直接アクセスできるようにし、モデルのトレーニングデータに頼るのではなく、ドキュメントの検索・全ページ取得・公式コードサンプルの検索ができます。

- ✅ **API キー不要** 
- ✅ **アカウント不要** 
- ✅ **ローカルインストール不要**

**`/plugin install` で簡単インストール：**

JSON 設定ファイルを手動で編集する代わりに、1コマンドでインストールできます：

```bash
copilot

> /plugin install microsoftdocs/mcp
```

このコマンドを実行すると、サーバーと関連するエージェントスキルが自動的に追加されます。インストールされるスキルは以下のとおりです：

- **microsoft-docs**：概念・チュートリアル・情報の検索
- **microsoft-code-reference**：API の検索・コードサンプル・トラブルシューティング
- **microsoft-skill-creator**：Microsoft 技術に関するカスタムスキルを生成するメタスキル

**使用例：**
```bash
copilot

> What's the recommended way to deploy a Python app to Azure App Service? Search Microsoft Learn.
```

📚 詳細：[Microsoft Learn MCP Server の概要](https://learn.microsoft.com/training/support/mcp-get-started)

### `web_fetch` による Web アクセス

Copilot CLI には任意の URL からコンテンツを取得できる組み込みの `web_fetch` ツールがあります。ターミナルを離れることなく README・API ドキュメント・リリースノートを取り込むのに便利です。MCP サーバーは必要ありません。

アクセス可能な URL は `~/.copilot/config.json`（Copilot の一般設定）で制御できます。これは MCP サーバーの定義ファイル `~/.copilot/mcp-config.json` とは別のファイルです。

```json
{
  "permissions": {
    "allowedUrls": [
      "https://api.github.com/**",
      "https://docs.github.com/**",
      "https://*.npmjs.org/**"
    ],
    "blockedUrls": [
      "http://**"
    ]
  }
}
```

**使用例：**
```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

### カスタム MCP サーバーの作成

自分の API・データベース・社内ツールに Copilot を接続したいですか？Python でカスタム MCP サーバーを構築できます。既製のサーバー（GitHub、filesystem、Context7）がほとんどのユースケースをカバーしているため、これは完全にオプションです。

📖 book app を例にした完全なウォークスルーは [カスタム MCP サーバーガイド](mcp-custom-server.md) をご覧ください。

📚 背景知識については [MCP for Beginners コース](https://github.com/microsoft/mcp-for-beginners) を参照してください。

</details>

<a id="complete-configuration-file"></a>

### 完全な設定ファイル

filesystem と Context7 サーバーを含む完全な `mcp-config.json` は以下のとおりです：

> 💡 **注意：** GitHub MCP は組み込み済みです。設定ファイルへの追加は不要です。

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    },
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

グローバルアクセスには `~/.copilot/mcp-config.json` として、プロジェクト固有の設定には `.vscode/mcp.json` として保存してください。

---

# MCP サーバーを使う

MCP サーバーの設定ができたので、実際に何ができるか見てみましょう。

<img src="images/using-mcp-servers.png" alt="Using MCP Servers - Hub-and-spoke diagram showing a Developer CLI connected to GitHub, Filesystem, Context7, and Custom/Web Fetch servers" width="800" />

---

## サーバーの使用例

**試したいサーバーを選ぶか、順番に進めてください。**

| 試したいこと | 移動先 |
|---|---|
| GitHub リポジトリ・issues・PR | [GitHub サーバー](#github-server-built-in) |
| プロジェクトファイルの参照 | [Filesystem サーバーの使用](#filesystem-server-usage) |
| ライブラリドキュメントの検索 | [Context7 サーバーの使用](#context7-server-usage) |
| カスタムサーバー・Microsoft Learn MCP・web_fetch の使用 | [応用編の使用](#beyond-the-basics-usage) |

<details>
<summary><strong>GitHub サーバー（組み込み）</strong> - リポジトリ・issues・PR などにアクセス</summary>
<a id="github-server-built-in"></a>

### GitHub サーバー（組み込み）

GitHub MCP サーバーは**組み込み済み**です。Copilot にログインしていれば（初期セットアップ時に行いました）、すでに動作しています。設定は不要です！

> 💡 **動作しない場合は？** `/login` を実行して GitHub で再認証してください。

<details>
<summary><strong>Dev Container での認証</strong></summary>

- **GitHub Codespaces**（推奨）：認証は自動的に行われます。`gh` CLI が Codespace トークンを継承します。操作は不要です。
- **ローカル Dev Container（Docker）**：コンテナ起動後に `gh auth login` を実行し、Copilot を再起動してください。

**認証のトラブルシューティング：**
```bash
# Check if you're authenticated
gh auth status

# If not, log in
gh auth login

# Verify GitHub MCP is connected
copilot
> /mcp show
```

</details>

| 機能 | 例 |
|---------|----------|
| **リポジトリ情報** | コミット・ブランチ・コントリビューターの表示 |
| **Issues** | issues の一覧・作成・検索・コメント |
| **Pull requests** | PR の表示・差分確認・PR 作成・ステータス確認 |
| **コード検索** | リポジトリ全体のコード検索 |
| **Actions** | ワークフローの実行状況の確認 |

```bash
copilot

# See recent activity in this repo
> List the last 5 commits in this repository

Recent commits:
1. abc1234 - Update chapter 05 skills examples (2 days ago)
2. def5678 - Add book app test fixtures (3 days ago)
3. ghi9012 - Fix typo in chapter 03 README (4 days ago)
...

# Explore the repo structure
> What branches exist in this repository?

Branches:
- main (default)
- chapter6 (current)

# Search for code patterns across the repo
> Search this repository for files that import pytest

Found 1 file:
- samples/book-app-project/tests/test_books.py
```

> 💡 **自分のフォークで作業していますか？** このコースリポジトリをフォークしていれば、issues や pull requests の作成などの書き込み操作も試せます。以下の演習でその練習をします。

> ⚠️ **結果が表示されない場合**、GitHub MCP はローカルファイルだけでなく、リポジトリのリモート（github.com 上）に対して操作します。リポジトリにリモートが設定されているか確認してください：`git remote -v` を実行して確認できます。

</details>

<details>
<summary><strong>Filesystem サーバー</strong> - プロジェクトファイルを参照・分析する</summary>
<a id="filesystem-server-usage"></a>

### Filesystem サーバー

設定が完了すると、filesystem MCP は Copilot が自動的に使用できるツールを提供します：

```bash
copilot

> How many Python files are in the book-app-project directory?

Found 3 Python files in samples/book-app-project/:
- book_app.py
- books.py
- utils.py

> What's the total size of the data.json file?

samples/book-app-project/data.json: 2.4 KB

> Find all functions that don't have type hints in the book app

Found 2 functions without type hints:
- samples/book-app-project/utils.py:10 - get_user_choice()
- samples/book-app-project/utils.py:14 - get_book_details()
```

</details>

<details>
<summary><strong>Context7 サーバー</strong> - ライブラリドキュメントを検索する</summary>
<a id="context7-server-usage"></a>

### Context7 サーバー

```bash
copilot

> What are the best practices for using pytest fixtures?

From pytest Documentation:

Fixtures - Use fixtures to provide a fixed baseline for tests:

    import pytest

    @pytest.fixture
    def sample_books():
        return [
            {"title": "1984", "author": "George Orwell", "year": 1949},
            {"title": "Dune", "author": "Frank Herbert", "year": 1965},
        ]

    def test_find_by_author(sample_books):
        # fixture is automatically passed as argument
        results = [b for b in sample_books if "Orwell" in b["author"]]
        assert len(results) == 1

Best practices:
- Use fixtures instead of setup/teardown methods
- Use tmp_path fixture for temporary files
- Use monkeypatch for modifying environment
- Scope fixtures appropriately (function, class, module, session)

> How can I apply this to the book app's test file?

# Copilot now knows the official pytest patterns
# and can apply them to samples/book-app-project/tests/test_books.py
```

</details>

<details>
<summary><strong>応用編</strong> - カスタムサーバーと web_fetch の使用</summary>
<a id="beyond-the-basics-usage"></a>

### 応用編

**カスタム MCP サーバー**：[カスタム MCP サーバーガイド](mcp-custom-server.md) を参照して book-lookup サーバーを作成した場合は、ブックコレクションに直接クエリを実行できます：

```bash
copilot

> Look up information about "1984" using the book lookup server. Search for books by George Orwell
```

**Microsoft Learn MCP**：[Microsoft Learn MCP サーバー](#microsoft-learn-mcp-server)をインストールした場合は、公式 Microsoft ドキュメントを直接参照できます：

```bash
copilot

> How do I configure managed identity for an Azure Function? Search Microsoft Learn.
```

**Web Fetch**：組み込みの `web_fetch` ツールを使って任意の URL からコンテンツを取得できます：

```bash
copilot

> Fetch and summarize the README from https://github.com/facebook/react
```

</details>

---

## 複数サーバーを組み合わせたワークフロー

これらのワークフローは、開発者が「もうこれなしでは作業したくない」と言う理由を示しています。各例では、1回のセッションで複数の MCP サーバーを組み合わせています。

<img src="images/issue-to-pr-workflow.png" alt="Issue to PR Workflow using MCP - Shows the complete flow from getting a GitHub issue through creating a pull request" width="800"/>

*MCP ワークフロー全体像：GitHub MCP がリポジトリデータを取得し、Filesystem MCP がコードを探索し、Context7 MCP がベストプラクティスを提供し、Copilot が分析を担当します*

以下の各例は独立しています。**興味のあるものを選ぶか、すべて読んでください。**

| 確認したいこと | 移動先 |
|---|---|
| 複数のサーバーの連携 | [マルチサーバー探索](#multi-server-exploration) |
| 1セッションで issue から PR まで | [Issue-to-PR ワークフロー](#issue-to-pr-workflow) |
| プロジェクトの健全性チェック | [ヘルスダッシュボード](#health-dashboard) |

<details>
<summary><strong>マルチサーバー探索</strong> - filesystem・GitHub・Context7 を1セッションで組み合わせる</summary>
<a id="multi-server-exploration"></a>

#### 複数の MCP サーバーで Book App を探索する

```bash
copilot

# Step 1: Use filesystem MCP to explore the book app
> List all Python files in samples/book-app-project/ and summarize
> what each file does

Found 3 Python files:
- book_app.py: CLI entry point with command routing (list, add, remove, find)
- books.py: BookCollection class with data persistence via JSON
- utils.py: Helper functions for user input and display

# Step 2: Use GitHub MCP to check recent changes
> What were the last 3 commits that touched files in samples/book-app-project/?

Recent commits affecting book app:
1. abc1234 - Add test fixtures for BookCollection (2 days ago)
2. def5678 - Add find_by_author method (5 days ago)
3. ghi9012 - Initial book app setup (1 week ago)

# Step 3: Use Context7 MCP for best practices
> What are Python best practices for JSON data persistence?

From Python Documentation:
- Use context managers (with statements) for file I/O
- Handle JSONDecodeError for corrupted files
- Use dataclasses for structured data
- Consider atomic writes to prevent data corruption

# Step 4: Synthesize a recommendation
> Based on the book app code and these best practices,
> what improvements would you suggest?

Suggestions:
1. Add input validation in add_book() for empty strings and invalid years
2. Consider atomic writes in save_books() to prevent data corruption
3. Add type hints to utils.py functions (get_user_choice, get_book_details)
```

<details>
<summary>🎬 MCP ワークフローの動作を確認する</summary>

![MCP Workflow Demo](images/mcp-workflow-demo.gif)

*デモの出力はあくまで一例です。モデル・ツール・応答は実際と異なる場合があります。*

</details>

**結果**：コードの探索 → 履歴の確認 → ベストプラクティスの検索 → 改善計画。**3つの MCP サーバーを使って、すべて1つのターミナルセッションから実行できます。**

</details>

<details>
<summary><strong>Issue-to-PR ワークフロー</strong> - ターミナルを離れることなく GitHub issue から pull request まで</summary>
<a id="issue-to-pr-workflow"></a>

#### Issue-to-PR ワークフロー（自分のリポジトリで）

書き込み権限を持つ自分のフォークやリポジトリで最もうまく機能します：

> 💡 **今すぐ試せなくても大丈夫です。** 読み取り専用のクローンをお使いの場合は、課題で練習します。今はフローを理解するために読んでください。

```bash
copilot

> Get the details of GitHub issue #1

Issue #1: Add input validation for book year
Status: Open
Description: The add_book function accepts any year value...

> @samples/book-app-project/books.py Fix the issue described in issue #1

[Copilot implements year validation in add_book()]

> Run the tests to make sure the fix works

All 8 tests passed ✓

> Create a pull request titled "Add year validation to book app"

✓ Created PR #2: Add year validation to book app
```

**コピペなし。コンテキストの切り替えなし。ターミナルセッション1つで完結。**

</details>

<details>
<summary><strong>ヘルスダッシュボード</strong> - 複数のサーバーを使ってプロジェクトの健全性を素早く確認する</summary>
<a id="health-dashboard"></a>

#### Book App ヘルスダッシュボード

```bash
copilot

> Give me a health report for the book app project:
> 1. List all functions across the Python files in samples/book-app-project/
> 2. Check which functions have type hints and which don't
> 3. Show what tests exist in samples/book-app-project/tests/
> 4. Check the recent commit history for this directory

Book App Health Report
======================

📊 Functions Found:
- books.py: 8 methods in BookCollection (all have type hints ✓)
- book_app.py: 6 functions (4 have type hints, 2 missing)
- utils.py: 3 functions (1 has type hints, 2 missing)

🧪 Test Coverage:
- test_books.py: 8 test functions covering BookCollection
- Missing: no tests for book_app.py CLI functions
- Missing: no tests for utils.py helper functions

📝 Recent Activity:
- 3 commits in the last week
- Most recent: added test fixtures

Recommendations:
- Add type hints to utils.py functions
- Add tests for book_app.py CLI handlers
- All files well-sized (<100 lines) - good structure!
```

**結果**：複数のデータソースを数秒で集約。手動でやろうとすると、grep の実行・行数のカウント・git log の確認・テストファイルの閲覧が必要で、15分以上かかる作業です。

</details>

---

# 練習

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

**🎉 基本をマスターしました！** MCP の概念を理解し、サーバーの設定方法を確認し、実際のワークフローを見てきました。今度は自分で試してみましょう。

---

## ▶️ 実際に試してみよう

あなたの番です！以下の演習で、book app プロジェクトを使った MCP サーバーの活用を練習しましょう。

### 演習 1：MCP の状態を確認する

まず、利用可能な MCP サーバーを確認します：

```bash
copilot

> /mcp show
```

GitHub サーバーが有効として表示されるはずです。表示されない場合は `/login` を実行して認証してください。

---

### 演習 2：Filesystem MCP で Book App を探索する

filesystem サーバーを設定済みの場合は、book app の探索に使ってみましょう：

```bash
copilot

> How many Python files are in samples/book-app-project/?
> What functions are defined in each file?
```

**期待される結果**：Copilot が `book_app.py`・`books.py`・`utils.py` を関数とともに一覧表示します。

> 💡 **filesystem MCP をまだ設定していない場合**は、上の[完全な設定ファイル](#complete-configuration-file)セクションの JSON から設定ファイルを作成してください。その後 Copilot を再起動します。

---

### 演習 3：GitHub MCP でリポジトリの履歴を確認する

組み込みの GitHub MCP でこのコースのリポジトリを探索しましょう：

```bash
copilot

> List the last 5 commits in this repository

> What branches exist in this repository?
```

**期待される結果**：Copilot が GitHub リモートの最近のコミットメッセージとブランチ名を表示します。

> ⚠️ **Codespace をお使いの場合**、これは自動的に機能します。認証は継承されます。ローカルクローンの場合は、`gh auth status` でログイン済みであることを確認してください。

---

### 演習 4：複数の MCP サーバーを組み合わせる

filesystem と GitHub MCP を1つのセッションで組み合わせてみましょう：

```bash
copilot

> Read samples/book-app-project/data.json and tell me what books are
> in the collection. Then check the recent commits to see when this
> file was last modified.
```

**期待される結果**：Copilot が JSON ファイルを読み込み（filesystem MCP）、「The Hobbit」・「1984」・「Dune」・「To Kill a Mockingbird」・「Mysterious Book」の5冊を一覧表示し、GitHub のコミット履歴を確認します。

**自己チェック**：「リポジトリのコミット履歴を確認する」が、手動で `git log` を実行してプロンプトに貼り付けるよりも優れている理由を説明できれば、MCP を理解できています。

---

## 📝 課題

### メインチャレンジ：Book App MCP 探索

book app プロジェクトで MCP サーバーを一緒に使う練習をしましょう。以下のステップを1つの Copilot セッションで完了してください：

1. **MCP の動作確認**：`/mcp show` を実行し、少なくとも GitHub サーバーが有効であることを確認する
2. **filesystem MCP の設定**（まだの場合）：filesystem サーバーの設定で `~/.copilot/mcp-config.json` を作成する
3. **コードの探索**：filesystem サーバーを使うよう Copilot に依頼する：
   - `samples/book-app-project/books.py` のすべての関数を一覧表示する
   - `samples/book-app-project/utils.py` の型ヒントが欠けている関数を確認する
   - `samples/book-app-project/data.json` を読み込んでデータ品質の問題を特定する（ヒント：最後のエントリを確認）
4. **リポジトリの活動確認**：GitHub MCP を使うよう Copilot に依頼する：
   - `samples/book-app-project/` 内のファイルに触れた最近のコミットを一覧表示する
   - オープンな issues や pull requests があるか確認する
5. **サーバーの組み合わせ**：1つのプロンプトで Copilot に依頼する：
   - `samples/book-app-project/tests/test_books.py` のテストファイルを読む
   - テスト済みの関数と `books.py` のすべての関数を比較する
   - 不足しているテストカバレッジをまとめる

**成功基準**：filesystem と GitHub MCP のデータを1つの Copilot セッションでシームレスに組み合わせられ、各 MCP サーバーが応答に何を提供したかを説明できること。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**ステップ 1：MCP の確認**
```bash
copilot
> /mcp show
# Should show "github" as enabled
# If not, run: /login
```

**ステップ 2：設定ファイルの作成**

上の[完全な設定ファイル](#complete-configuration-file)セクションの JSON を使って `~/.copilot/mcp-config.json` として保存してください。

**ステップ 3：確認すべきデータ品質の問題**

`data.json` の最後の本は：
```json
{
  "title": "Mysterious Book",
  "author": "",
  "year": 0,
  "read": false
}
```
著者が空で年が 0。それがデータ品質の問題です！

**ステップ 5：テストカバレッジの比較**

`test_books.py` のテストがカバーしている関数：`add_book`・`mark_as_read`・`remove_book`・`get_unread_books`・`find_book_by_title`。`load_books`・`save_books`・`list_books` などの関数には直接テストがありません。`book_app.py` の CLI 関数と `utils.py` のヘルパー関数にはまったくテストがありません。

**MCP が動作しない場合**：設定ファイルを編集した後 Copilot を再起動してください。

</details>

### ボーナスチャレンジ：カスタム MCP サーバーを作る

さらに深く学びたいですか？[カスタム MCP サーバーガイド](mcp-custom-server.md) に従って、任意の API に接続する Python 製の MCP サーバーを作ってみましょう。

---

<details>
<summary>🔧 <strong>よくある間違いとトラブルシューティング</strong>（クリックして展開）</summary>

### よくある間違い

| 間違い | 何が起こるか | 対処法 |
|---------|--------------|-----|
| GitHub MCP が組み込み済みであることを知らない | 手動でインストール・設定しようとする | GitHub MCP はデフォルトで含まれています。まずは「このリポジトリの最近のコミットを一覧表示して」と試してみましょう |
| 設定ファイルの場所を間違える | MCP 設定を見つけられない・編集できない | ユーザーレベルの設定は `~/.copilot/mcp-config.json`、プロジェクトレベルは `.vscode/mcp.json` です |
| 設定ファイルの JSON が無効 | MCP サーバーが読み込まれない | `/mcp show` で設定を確認し、JSON 構文を検証してください |
| MCP サーバーの認証を忘れる | 「認証に失敗しました」エラーが表示される | 一部の MCP は個別の認証が必要です。各サーバーの要件を確認してください |

### トラブルシューティング

**「MCP server not found」** - 以下を確認してください：
1. npm パッケージが存在するか：`npm view @modelcontextprotocol/server-github`
2. 設定が有効な JSON であるか
3. サーバー名が設定と一致しているか

`/mcp show` で現在の設定を確認してください。

**「GitHub authentication failed」** - 組み込みの GitHub MCP は `/login` の認証情報を使用します。次を試してください：

```bash
copilot
> /login
```

GitHub で再認証されます。問題が続く場合は、GitHub アカウントがアクセスしているリポジトリに必要な権限を持っているか確認してください。

**「MCP server failed to start」** - サーバーのログを確認してください：
```bash
# Run the server command manually to see errors
npx -y @modelcontextprotocol/server-github
```

**MCP のツールが利用できない** - サーバーが有効になっているか確認してください：
```bash
copilot

> /mcp show
# Check if server is listed and enabled
```

サーバーが無効になっている場合は、再有効化する方法について下の[追加の `/mcp` コマンド](#-additional-mcp-commands)を参照してください。

</details>

---

<details>
<summary>📚 <strong>追加の MCP コマンド</strong>（クリックして展開）</summary>
<a id="-additional-mcp-commands"></a>

MCP サーバーは2つの方法で管理できます：**チャットセッション内のスラッシュコマンド**を使うか、**ターミナルから直接 `copilot mcp` コマンド**を使う（チャットセッション不要）かです。

### オプション 1：スラッシュコマンド（チャットセッション内）

`copilot` を起動中に使えます：

| コマンド | 機能 |
|---------|--------------|
| `/mcp show` | 設定済みの MCP サーバーとその状態を表示 |
| `/mcp add` | 新しいサーバーを追加するインタラクティブな設定 |
| `/mcp edit <server-name>` | 既存のサーバー設定を編集 |
| `/mcp enable <server-name>` | 無効なサーバーを有効化（セッションをまたいで持続） |
| `/mcp disable <server-name>` | サーバーを無効化（セッションをまたいで持続） |
| `/mcp delete <server-name>` | サーバーを完全に削除 |
| `/mcp auth <server-name>` | OAuth を使用する MCP サーバーで再認証（例：アカウント切り替え後） |

### オプション 2：`copilot mcp` コマンド（ターミナルから）

チャットセッションを開始することなく、ターミナルから直接 MCP サーバーを管理することもできます：

```bash
# List all configured MCP servers
copilot mcp list

# Enable a server
copilot mcp enable filesystem

# Disable a server
copilot mcp disable context7
```

> 💡 **どちらを使えばよい？** チャットセッション中は `/mcp` スラッシュコマンドを使いましょう。セッションを開始する前にサーバー設定を素早く確認・変更したい場合は `copilot mcp` をターミナルから使いましょう。

このコースでは、ほとんどの場合 `/mcp show` だけで十分です。その他のコマンドは、管理するサーバーが増えてきたときに役立ちます。

</details>

---

# まとめ

## 🔑 重要なポイント

1. **MCP** は Copilot を外部サービス（GitHub・ファイルシステム・ドキュメント）に接続する
2. **GitHub MCP は組み込み済み** - 設定不要、`/login` するだけ
3. **Filesystem と Context7** は `~/.copilot/mcp-config.json` で設定する
4. **マルチサーバーワークフロー** は1セッションで複数のデータソースを組み合わせる
5. **サーバー管理の2つの方法**：チャット内の `/mcp` スラッシュコマンド、またはターミナルから `copilot mcp`
6. **カスタムサーバー** で任意の API に接続できる（オプション、付録ガイドで解説）

> 📋 **クイックリファレンス**：コマンドとショートカットの完全なリストは [GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference) をご覧ください。

---

## ➡️ 次のステップ

これですべての構成要素が揃いました：モード・コンテキスト・ワークフロー・エージェント・スキル・MCP。いよいよすべてを組み合わせましょう。

**[第07章：すべてを組み合わせる](../07-putting-it-together/README.md)** では、以下を学びます：

- エージェント・スキル・MCP を統合したワークフローへの組み合わせ方
- アイデアからマージ済み PR までの完全な機能開発
- フックによる自動化
- チーム環境でのベストプラクティス

---

**[← 第05章に戻る](../05-skills/README.md)** | **[第07章へ進む →](../07-putting-it-together/README.md)**
