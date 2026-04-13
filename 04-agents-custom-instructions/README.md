![Chapter 04: Agents and Custom Instructions](images/chapter-header.png)

> **Python コードレビュアー、テスト専門家、セキュリティレビュアーを一つのツールで雇えるとしたら？**

Chapter 03 では、コードレビュー・リファクタリング・デバッグ・テスト生成・git 連携といった重要なワークフローをマスターしました。これらを使いこなすことで、GitHub Copilot CLI での生産性は大幅に向上しています。では、さらに一歩進めてみましょう。

これまで Copilot CLI は汎用アシスタントとして使ってきました。エージェントを使うと、特定の専門家としての役割を与えることができます。たとえば、型ヒントと PEP 8 を徹底するコードレビュアーや、pytest のテストケースを書くテスト専門家などです。同じプロンプトでも、専門的な指示を持つエージェントに任せると、出力の質が格段に上がることを実感できるでしょう。

## 🎯 学習目標

この章を終えると、以下のことができるようになります。

- 組み込みエージェント（Plan：`/plan`、Code-review：`/review`）の使い方と、自動エージェント（Explore・Task）の仕組みを理解する
- エージェントファイル（`.agent.md`）を使って専門エージェントを作成する
- 特定のドメインに特化したタスクにエージェントを活用する
- `/agent` や `--agent` でエージェントを切り替える
- プロジェクト固有の標準に合わせたカスタム指示ファイルを作成する

> ⏱️ **目安の所要時間**: 約55分（読書 20分 + ハンズオン 35分）

---

## 🧩 現実世界のアナロジー：専門家を雇う

家のことで困ったとき、一人の「なんでも屋」に頼むのではなく、専門家に相談しますよね。

| 問題 | 専門家 | 理由 |
|---------|------------|-----|
| 水漏れ | 配管工 | 配管の規格を知り、専用工具を持っている |
| 電気の配線 | 電気工事士 | 安全基準を熟知し、法令に準拠している |
| 屋根の葺き替え | 屋根工 | 素材の知識があり、地域の気候を考慮できる |

エージェントも同じ仕組みです。汎用 AI の代わりに、特定のタスクに集中し、適切なプロセスを知っているエージェントを使いましょう。指示は一度設定するだけで、コードレビュー・テスト・セキュリティ・ドキュメント作成など、必要なときにいつでも再利用できます。

<img src="images/hiring-specialists-analogy.png" alt="Hiring Specialists Analogy - Just as you call specialized tradespeople for house repairs, AI agents are specialized for specific tasks like code review, testing, security, and documentation" width="800" />

---

# エージェントを使う

組み込みエージェントとカスタムエージェントをすぐに使ってみましょう。

---

## *エージェントが初めての方へ* まずはここから！
エージェントを使ったことがない方も、作ったことがない方も、このコースを始めるために必要なことをすべてご紹介します。

1. **今すぐ*組み込み*エージェントを試す：**
   ```bash
   copilot
   > /plan Add input validation for book year in the book app
   ```
   これで Plan エージェントが呼び出され、ステップごとの実装計画が作成されます。

2. **カスタムエージェントのサンプルを見る：** エージェントの指示定義はとても簡単です。提供されている [python-reviewer.agent.md](../.github/agents/python-reviewer.agent.md) ファイルを見て、パターンを確認しましょう。

3. **コアコンセプトを理解する：** エージェントとは、ジェネラリストではなく専門家に相談するようなものです。「フロントエンドエージェント」はアクセシビリティやコンポーネントパターンに自動的に集中します。エージェントの指示にすでに記載されているので、毎回リマインドする必要はありません。


## 組み込みエージェント

**Chapter 03 の開発ワークフローで、すでに一部の組み込みエージェントを使っています！**
<br>`/plan` と `/review` は実は組み込みエージェントです。内部でどう動いているかがわかりましたね。以下が全リストです：

| エージェント | 呼び出し方 | 役割 |
|-------|---------------|--------------|
| **Plan** | `/plan` または `Shift+Tab`（モード切り替え） | コーディング前にステップごとの実装計画を作成する |
| **Code-review** | `/review` | ステージ済み・未ステージの変更を、具体的でアクション可能なフィードバックでレビューする |
| **Init** | `/init` | プロジェクト設定ファイル（指示ファイル・エージェントファイル）を生成する |
| **Explore** | *自動* | コードベースの探索・分析を Copilot に依頼したとき内部で使用される |
| **Task** | *自動* | テスト・ビルド・lint・依存関係インストールなどのコマンドを実行する |

<br>

**組み込みエージェントの活用例** - Plan・Code-review・Explore・Task の呼び出し例

```bash
copilot

# Plan エージェントを呼び出して実装計画を作成
> /plan Add input validation for book year in the book app

# Code-review エージェントで変更をレビュー
> /review

# Explore・Task エージェントは関連する場面で自動的に呼び出されます：
> Run the test suite        # Task エージェントを使用

> Explore how book data is loaded    # Explore エージェントを使用
```

Task エージェントについて：バックグラウンドで動作し、進行状況を管理・追跡して、わかりやすい形式で結果を報告します。

| 結果 | 表示内容 |
|---------|--------------|
| ✅ **成功** | 簡潔なサマリー（例：「All 247 tests passed」「Build succeeded」） |
| ❌ **失敗** | スタックトレース・コンパイルエラー・詳細ログを含む全出力 |


> 📚 **公式ドキュメント**: [GitHub Copilot CLI Agents](https://docs.github.com/copilot/how-tos/use-copilot-agents/use-copilot-cli#use-custom-agents)

---

# Copilot CLI にエージェントを追加する

独自のエージェントをワークフローに追加するのは簡単です！一度定義すれば、あとは指定するだけで使えます。

<img src="images/using-agents.png" alt="Four colorful AI robots standing together, each with different tools representing specialized agent capabilities" width="800"/>

## 🗂️ エージェントを追加する

エージェントファイルは `.agent.md` という拡張子を持つ Markdown ファイルです。YAML frontmatter（メタデータ）と Markdown の指示、この2つのパートで構成されています。

> 💡 **YAML frontmatter が初めての方へ** ファイルの先頭に `---` で囲まれた設定ブロックのことです。YAML は `キー: 値` の形式で書くだけです。それ以降は通常の Markdown です。

最小構成のエージェント例：

```markdown
---
name: my-reviewer
description: Code reviewer focused on bugs and security issues
---

# Code Reviewer

You are a code reviewer focused on finding bugs and security issues.

When reviewing code, always check for:
- SQL injection vulnerabilities
- Missing error handling
- Hardcoded secrets
```

> 💡 **必須 vs 任意**: `description` フィールドは必須です。`name`・`tools`・`model` などのフィールドは任意です。

## エージェントファイルの配置場所

| 場所 | スコープ | 用途 |
|----------|-------|----------|
| `.github/agents/` | プロジェクト固有 | プロジェクトの規約を共有するチーム向けエージェント |
| `~/.copilot/agents/` | グローバル（全プロジェクト） | どこでも使える個人用エージェント |

**このプロジェクトには [.github/agents/](../.github/agents/) フォルダにサンプルエージェントファイルが含まれています**。自分で書いても、提供されているものをカスタマイズしてもかまいません。

<details>
<summary>📂 このコースのサンプルエージェントを見る</summary>

| ファイル | 説明 |
|------|-------------|
| `hello-world.agent.md` | 最小構成の例 - まずここから |
| `python-reviewer.agent.md` | Python コード品質レビュアー |
| `pytest-helper.agent.md` | pytest テスト専門家 |

```bash
# または個人用エージェントフォルダにコピーする（すべてのプロジェクトで利用可能）
cp .github/agents/python-reviewer.agent.md ~/.copilot/agents/
```

コミュニティのエージェントについては [github/awesome-copilot](https://github.com/github/awesome-copilot) をご覧ください。

</details>


## 🚀 カスタムエージェントの使い方（2通り）

### インタラクティブモード
インタラクティブモード内で `/agent` を使うとエージェントの一覧が表示され、使用するエージェントを選択できます。
エージェントを選択すると、そのエージェントとの会話が続きます。

```bash
copilot
> /agent
```

別のエージェントに切り替えたり、デフォルトモードに戻したりする場合は、再度 `/agent` コマンドを使います。

### プログラムモード

エージェントを指定して新しいセッションを直接開始します。

```bash
copilot --agent python-reviewer
> Review @samples/book-app-project/books.py
```

> 💡 **エージェントの切り替え**: `/agent` または `--agent` をいつでも使って別のエージェントに切り替えられます。通常の Copilot CLI に戻すには、`/agent` でエージェントなしを選択してください。

---

# エージェントをより深く理解する

<img src="images/creating-custom-agents.png" alt="Robot being assembled on a workbench surrounded by components and tools representing custom agent creation" width="800"/>

> 💡 **このセクションはオプションです。** 組み込みエージェント（`/plan`・`/review`）だけでほとんどのワークフローには十分です。カスタムエージェントは、作業全体に一貫して専門的な知識を適用したいときに作成しましょう。

以下のトピックはそれぞれ独立しています。**興味のあるものを選んで読んでください - すべてを一度に読む必要はありません。**

| やりたいこと | ジャンプ先 |
|---|---|
| エージェントが汎用プロンプトより優れている理由を見る | [スペシャリスト vs 汎用](#specialist-vs-generic-see-the-difference) |
| 複数のエージェントを組み合わせる | [複数エージェントで作業する](#working-with-multiple-agents) |
| エージェントの整理・命名・共有 | [エージェントの整理と共有](#organizing--sharing-agents) |
| プロジェクトの常時コンテキストを設定する | [Copilot 向けのプロジェクト設定](#configuring-your-project-for-copilot) |
| YAML プロパティとツールを調べる | [エージェントファイルリファレンス](#agent-file-reference) |

以下のシナリオを選択して展開してください。

---

<a id="specialist-vs-generic-see-the-difference"></a>
<details>
<summary><strong>スペシャリスト vs 汎用：違いを見る</strong> - エージェントが汎用プロンプトより優れた出力を生む理由</summary>

## スペシャリスト vs 汎用：違いを見る

これがエージェントの真価を発揮する場面です。違いを見てみましょう。

### エージェントなし（汎用 Copilot）

```bash
copilot

> Add a function to search books by year range in the book app
```

**汎用出力**:
```python
def search_by_year_range(books, start_year, end_year):
    results = []
    for book in books:
        if book['year'] >= start_year and book['year'] <= end_year:
            results.append(book)
    return results
```

基本的な実装。動作はします。でも、多くのものが欠けています。

---

### Python Reviewer エージェントを使った場合

```bash
copilot

> /agent
# Select "python-reviewer"

> Add a function to search books by year range in the book app
```

**専門家による出力**:
```python
from typing import List, Dict, Any

def search_by_year_range(
    books: List[Dict[str, Any]],
    start_year: int,
    end_year: int
) -> List[Dict[str, Any]]:
    """
    Search for books within a specified year range.

    Args:
        books: List of book dictionaries
        start_year: Starting year (inclusive)
        end_year: Ending year (inclusive)

    Returns:
        List of books published within the year range

    Raises:
        ValueError: If start_year is greater than end_year
        TypeError: If year values are not integers
    """
    if not isinstance(start_year, int) or not isinstance(end_year, int):
        raise TypeError("Year values must be integers")

    if start_year > end_year:
        raise ValueError(f"Start year ({start_year}) cannot be greater than end year ({end_year})")

    return [
        book for book in books
        if isinstance(book.get('year'), int)
        and start_year <= book['year'] <= end_year
    ]
```

**python-reviewer エージェントが自動的に含めるもの**：
- ✅ すべてのパラメーターと戻り値への型ヒント
- ✅ Args・Returns・Raises を含む包括的な docstring
- ✅ 適切なエラーハンドリングを伴う入力バリデーション
- ✅ パフォーマンス向上のためのリスト内包表記
- ✅ エッジケースの処理（year の値が欠落・無効な場合）
- ✅ PEP 8 準拠のフォーマット
- ✅ 防御的プログラミングの実践

**違い**：同じプロンプトで、劇的に高品質な出力。エージェントは、あなたが頼むのを忘れそうな専門知識を自動的に持ち込んでくれます。

</details>

---

<a id="working-with-multiple-agents"></a>
<details>
<summary><strong>複数エージェントで作業する</strong> - スペシャリストの組み合わせ・セッション中の切り替え・エージェントのツールとしての利用</summary>

## 複数エージェントで作業する

複数のスペシャリストが一つの機能に協力するとき、真の力が発揮されます。

### 例：シンプルな機能の開発

```bash
copilot

> I want to add a "search by year range" feature to the book app

# Use python-reviewer for design
> /agent
# Select "python-reviewer"

> @samples/book-app-project/books.py Design a find_by_year_range method. What's the best approach?

# Switch to pytest-helper for test design
> /agent
# Select "pytest-helper"

> @samples/book-app-project/tests/test_books.py Design test cases for a find_by_year_range method.
> What edge cases should we cover?

# Synthesize both designs
> Create an implementation plan that includes the method implementation and comprehensive tests.
```

**重要なポイント**：あなたがスペシャリストを指揮するアーキテクト役です。細部はエージェントに任せ、あなたはビジョンを担います。

<details>
<summary>🎬 実際の動作を見る！</summary>

![Python Reviewer Demo](images/python-reviewer-demo.gif)

*デモの出力は参考例です - 使用するモデル・ツール・レスポンスは表示内容と異なる場合があります。*

</details>

### エージェントのツールとしての利用

エージェントが設定されている場合、Copilot は複雑なタスクの実行中にそれらをツールとして呼び出すこともできます。フルスタックの機能開発を依頼すると、Copilot が適切なスペシャリストエージェントに自動的に各パートを委任することがあります。

</details>

---

<a id="organizing--sharing-agents"></a>
<details>
<summary><strong>エージェントの整理と共有</strong> - 命名・ファイル配置・指示ファイル・チームでの共有</summary>

## エージェントの整理と共有

### エージェントの命名

エージェントファイルを作成するとき、名前は重要です。`/agent` や `--agent` のあとに入力するものであり、チームメンバーがエージェントリストで目にするものです。

| ✅ 良い名前 | ❌ 避けるべき名前 |
|--------------|----------|
| `frontend` | `my-agent` |
| `backend-api` | `agent1` |
| `security-reviewer` | `helper` |
| `react-specialist` | `code` |
| `python-backend` | `assistant` |

**命名規則：**
- 小文字とハイフンを使う：`my-agent-name.agent.md`
- ドメインを含める：`frontend`・`backend`・`devops`・`security`
- 必要に応じて具体的にする：単なる `frontend` ではなく `react-typescript`

---

### チームとの共有

エージェントファイルを `.github/agents/` に配置すれば、バージョン管理されます。リポジトリに push すると、すべてのチームメンバーが自動的に利用できます。ただし、エージェントは Copilot がプロジェクトから読み込むファイルの一種にすぎません。**指示ファイル**もサポートされており、こちらは `/agent` を実行しなくても、すべてのセッションに自動的に適用されます。

考え方のヒント：エージェントはオンデマンドで呼び出すスペシャリスト、指示ファイルは常に有効なチームのルールです。

### ファイルの配置場所

2つのメインの配置場所についてはすでに説明しました（[エージェントファイルの配置場所](#where-to-put-agent-files)を参照）。以下の決定ツリーを使って選びましょう。

<img src="images/agent-file-placement-decision-tree.png" alt="Decision tree for where to put agent files: experimenting → current folder, team use → .github/agents/, everywhere → ~/.copilot/agents/" width="800"/>

**シンプルに始めましょう：** まずプロジェクトフォルダに `*.agent.md` ファイルを1つ作ります。満足できたら、恒久的な場所に移動してください。

エージェントファイルに加えて、Copilot は**プロジェクトレベルの指示ファイル**も自動的に読み込みます。`/agent` は不要です。`AGENTS.md`・`.instructions.md`・`/init` については、後述の[Copilot 向けのプロジェクト設定](#configuring-your-project-for-copilot)をご覧ください。

</details>

---

<a id="configuring-your-project-for-copilot"></a>
<details>
<summary><strong>Copilot 向けのプロジェクト設定</strong> - AGENTS.md・指示ファイル・/init によるセットアップ</summary>

## Copilot 向けのプロジェクト設定

エージェントはオンデマンドで呼び出すスペシャリストです。**プロジェクト設定ファイル**はそれとは異なります。Copilot はすべてのセッションで自動的にこれらを読み込み、プロジェクトの規約・技術スタック・ルールを把握します。誰も `/agent` を実行する必要はなく、リポジトリで作業する全員に常にコンテキストが適用されます。

### /init を使ったクイックセットアップ

最も手軽に始める方法は、Copilot に設定ファイルを生成させることです。

```bash
copilot
> /init
```

Copilot がプロジェクトをスキャンして、プロジェクトに合わせた指示ファイルを作成します。その後、自由に編集できます。

### 指示ファイルの形式

| ファイル | スコープ | 備考 |
|------|-------|-------|
| `AGENTS.md` | プロジェクトルートまたはネスト | **クロスプラットフォーム標準** - Copilot および他の AI アシスタントで動作 |
| `.github/copilot-instructions.md` | プロジェクト | GitHub Copilot 専用 |
| `.github/instructions/*.instructions.md` | プロジェクト | 詳細なトピック別指示 |
| `CLAUDE.md`・`GEMINI.md` | プロジェクトルート | 互換性のためサポート |

> 🎯 **まず始めるなら？** プロジェクト指示には `AGENTS.md` を使いましょう。他の形式は必要に応じて後で試せます。

### AGENTS.md

`AGENTS.md` は推奨フォーマットです。[オープンスタンダード](https://agents.md/)として Copilot および他の AI コーディングツールで動作します。リポジトリのルートに置くと、Copilot が自動的に読み込みます。このプロジェクト自身の [AGENTS.md](../AGENTS.md) が実際の例です。

典型的な `AGENTS.md` には、プロジェクトのコンテキスト・コードスタイル・セキュリティ要件・テスト標準が記述されます。`/init` で生成するか、サンプルファイルのパターンに従って自分で書いてみましょう。

### カスタム指示ファイル（.instructions.md）

より細かい制御を望むチーム向けに、指示をトピック別のファイルに分割できます。各ファイルは一つの関心事をカバーし、自動的に適用されます。

```
.github/
└── instructions/
    ├── python-standards.instructions.md
    ├── security-checklist.instructions.md
    └── api-design.instructions.md
```

> 💡 **注意**: 指示ファイルはどの言語でも使えます。この例はコースプロジェクトに合わせて Python を使っていますが、TypeScript・Go・Rust など、チームが使う任意の技術向けにも同様のファイルを作成できます。

**コミュニティの指示ファイルを探す**: .NET・Angular・Azure・Python・Docker などの技術向けに作られた指示ファイルは [github/awesome-copilot](https://github.com/github/awesome-copilot) で見つかります。

### カスタム指示の無効化

すべてのプロジェクト固有設定を Copilot に無視させたい場合（デバッグや動作比較に便利）：

```bash
copilot --no-custom-instructions
```

</details>

---

<a id="agent-file-reference"></a>
<details>
<summary><strong>エージェントファイルリファレンス</strong> - YAML プロパティ・ツールエイリアス・完全な例</summary>

## エージェントファイルリファレンス

### より詳しい例

[最小構成のエージェント形式](#-add-your-agents) はすでに確認しました。ここでは `tools` プロパティを使った、より本格的なエージェントを紹介します。`~/.copilot/agents/python-reviewer.agent.md` を作成しましょう：

```markdown
---
name: python-reviewer
description: Python code quality specialist for reviewing Python projects
tools: ["read", "edit", "search", "execute"]
---

# Python Code Reviewer

You are a Python specialist focused on code quality and best practices.

**Your focus areas:**
- Code quality (PEP 8, type hints, docstrings)
- Performance optimization (list comprehensions, generators)
- Error handling (proper exception handling)
- Maintainability (DRY principles, clear naming)

**Code style requirements:**
- Use Python 3.10+ features (dataclasses, type hints, pattern matching)
- Follow PEP 8 naming conventions
- Use context managers for file I/O
- All functions must have type hints and docstrings

**When reviewing code, always check:**
- Missing type hints on function signatures
- Mutable default arguments
- Proper error handling (no bare except)
- Input validation completeness
```

### YAML プロパティ

| プロパティ | 必須 | 説明 |
|----------|----------|-------------|
| `name` | いいえ | 表示名（省略するとファイル名が使われる） |
| `description` | **はい** | エージェントの役割 - Copilot がいつ提案するかを判断するための説明 |
| `tools` | いいえ | 使用できるツールのリスト（省略するとすべてのツールが使用可能）。下記のツールエイリアスを参照。 |
| `target` | いいえ | `vscode` または `github-copilot` のみに限定する |

### ツールエイリアス

`tools` リストで使用する名前：
- `read` - ファイルの内容を読み込む
- `edit` - ファイルを編集する
- `search` - ファイルを検索する（grep・glob）
- `execute` - シェルコマンドを実行する（別名：`shell`・`Bash`）
- `agent` - 他のカスタムエージェントを呼び出す

> 📖 **公式ドキュメント**: [Custom agents configuration](https://docs.github.com/copilot/reference/custom-agents-configuration)
>
> ⚠️ **VS Code のみ**: `model` プロパティ（AI モデルを選択するもの）は VS Code では動作しますが、GitHub Copilot CLI ではサポートされていません。クロスプラットフォームのエージェントファイルに含めても問題なく、GitHub Copilot CLI は無視します。

### さらなるエージェントテンプレート

> 💡 **初心者向けメモ**: 以下の例はテンプレートです。**特定の技術は自分のプロジェクトで使っているものに置き換えてください。** 大切なのは具体的な技術ではなく、エージェントの*構造*です。

このプロジェクトには [.github/agents/](../.github/agents/) フォルダに実際の例が含まれています：
- [hello-world.agent.md](../.github/agents/hello-world.agent.md) - 最小構成の例、まずここから
- [python-reviewer.agent.md](../.github/agents/python-reviewer.agent.md) - Python コード品質レビュアー
- [pytest-helper.agent.md](../.github/agents/pytest-helper.agent.md) - pytest テスト専門家

コミュニティのエージェントは [github/awesome-copilot](https://github.com/github/awesome-copilot) をご覧ください。

</details>

---

# 練習

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

独自のエージェントを作成して、実際に動かしてみましょう。

---

## ▶️ 実際に試してみよう

```bash

# Create the agents directory (if it doesn't exist)
mkdir -p .github/agents

# Create a code reviewer agent
cat > .github/agents/reviewer.agent.md << 'EOF'
---
name: reviewer
description: Senior code reviewer focused on security and best practices
---

# Code Reviewer Agent

You are a senior code reviewer focused on code quality.

**Review priorities:**
1. Security vulnerabilities
2. Performance issues
3. Maintainability concerns
4. Best practice violations

**Output format:**
Provide issues as a numbered list with severity tags:
[CRITICAL], [HIGH], [MEDIUM], [LOW]
EOF

# Create a documentation agent
cat > .github/agents/documentor.agent.md << 'EOF'
---
name: documentor
description: Technical writer for clear and complete documentation
---

# Documentation Agent

You are a technical writer who creates clear documentation.

**Documentation standards:**
- Start with a one-sentence summary
- Include usage examples
- Document parameters and return values
- Note any gotchas or limitations
EOF

# Now use them
copilot --agent reviewer
> Review @samples/book-app-project/books.py

# Or switch agents
copilot
> /agent
# Select "documentor"
> Document @samples/book-app-project/books.py
```

---

## 📝 課題

### メインチャレンジ：専門エージェントチームを作る

ハンズオン例では `reviewer` と `documentor` エージェントを作成しました。今度は別のタスク—book app のデータバリデーション改善—でエージェントの作成と活用を練習しましょう。

1. book app に合わせたエージェントファイル（`.agent.md`）を3つ作成し、`.github/agents/` に配置する（エージェントごとに1ファイル）
2. 作成するエージェント：
   - **data-validator**：`data.json` の欠落・不正データをチェック（著者が空・year=0・フィールドが欠落など）
   - **error-handler**：Python コードのエラーハンドリングの一貫性をレビューし、統一されたアプローチを提案する
   - **doc-writer**：docstring と README の内容を生成・更新する
3. 各エージェントを book app で使う：
   - `data-validator` → `@samples/book-app-project/data.json` を監査する
   - `error-handler` → `@samples/book-app-project/books.py` と `@samples/book-app-project/utils.py` をレビューする
   - `doc-writer` → `@samples/book-app-project/books.py` に docstring を追加する
4. コラボレーション：`error-handler` でエラーハンドリングのギャップを特定し、次に `doc-writer` で改善されたアプローチをドキュメント化する

**成功の基準**：3つのエージェントが一貫して高品質な出力を生成し、`/agent` でそれらを切り替えられること。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**スターターテンプレート**：`.github/agents/` にエージェントごとに1ファイル作成する：

`data-validator.agent.md`:
```markdown
---
description: Analyzes JSON data files for missing or malformed entries
---

You analyze JSON data files for missing or malformed entries.

**Focus areas:**
- Empty or missing author fields
- Invalid years (year=0, future years, negative years)
- Missing required fields (title, author, year, read)
- Duplicate entries
```

`error-handler.agent.md`:
```markdown
---
description: Reviews Python code for error handling consistency
---

You review Python code for error handling consistency.

**Standards:**
- No bare except clauses
- Use custom exceptions where appropriate
- All file operations use context managers
- Consistent return types for success/failure
```

`doc-writer.agent.md`:
```markdown
---
description: Technical writer for clear Python documentation
---

You are a technical writer who creates clear Python documentation.

**Standards:**
- Google-style docstrings
- Include parameter types and return values
- Add usage examples for public methods
- Note any exceptions raised
```

**エージェントのテスト：**

> 💡 **注意：** `samples/book-app-project/data.json` はすでにローカルのリポジトリに含まれているはずです。見当たらない場合は、ソースリポジトリからオリジナルのバージョンをダウンロードしてください：
> [data.json](https://github.com/github/copilot-cli-for-beginners/blob/main/samples/book-app-project/data.json)

```bash
copilot
> /agent
# Select "data-validator" from the list
> @samples/book-app-project/data.json Check for books with empty author fields or invalid years
```

**ヒント：** YAML frontmatter の `description` フィールドはエージェントが機能するために必須です。

</details>

### ボーナスチャレンジ：指示ライブラリ

オンデマンドで呼び出すエージェントは作れました。今度は逆側、つまり `/agent` 不要でセッションごとに Copilot が自動的に読み込む**指示ファイル**を試してみましょう。

`.github/instructions/` フォルダを作成し、少なくとも3つの指示ファイルを追加しましょう：
- `python-style.instructions.md`：PEP 8 と型ヒントの規約を適用する
- `test-standards.instructions.md`：テストファイルでの pytest の規約を適用する
- `data-quality.instructions.md`：JSON データエントリのバリデーションを行う

各指示ファイルを book app のコードでテストしましょう。

---

<details>
<summary>🔧 <strong>よくあるミスとトラブルシューティング</strong>（クリックして展開）</summary>

### よくあるミス

| ミス | 起きること | 対処法 |
|---------|--------------|-----|
| エージェントの frontmatter に `description` がない | エージェントが読み込まれないか、発見されない | YAML frontmatter に必ず `description:` を含める |
| エージェントファイルの配置場所が間違っている | 使おうとしたときにエージェントが見つからない | `~/.copilot/agents/`（個人用）または `.github/agents/`（プロジェクト用）に配置する |
| `.agent.md` ではなく `.md` を使っている | ファイルがエージェントとして認識されないことがある | `python-reviewer.agent.md` のように名前を付ける |
| エージェントのプロンプトが長すぎる | 30,000文字の上限に達することがある | エージェント定義は簡潔に保ち、詳細な指示はスキルを使う |

### トラブルシューティング

**エージェントが見つからない** - エージェントファイルが以下のどちらかの場所に存在するか確認してください：
- `~/.copilot/agents/`
- `.github/agents/`

利用可能なエージェントを一覧表示する：

```bash
copilot
> /agent
# すべての利用可能なエージェントが表示される
```

**エージェントが指示に従わない** - プロンプトをより明確にし、エージェント定義に詳細を追加しましょう：
- バージョンを含む特定のフレームワーク・ライブラリ
- チームの規約
- コードパターンの例

**カスタム指示が読み込まれない** - プロジェクトで `/init` を実行してプロジェクト固有の指示をセットアップしましょう：

```bash
copilot
> /init
```

または無効になっていないか確認する：
```bash
# 指示を読み込ませたい場合は --no-custom-instructions を使わないこと
copilot  # デフォルトでカスタム指示を読み込む
```

</details>

---

# まとめ

## 🔑 重要なポイント

1. **組み込みエージェント**：`/plan` と `/review` は直接呼び出す；Explore と Task は自動的に動作する
2. **カスタムエージェント**は `.agent.md` ファイルで定義するスペシャリスト
3. **優れたエージェント**は明確な専門知識・標準・出力形式を持つ
4. **マルチエージェント連携**で専門知識を組み合わせ、複雑な問題を解決する
5. **指示ファイル**（`.instructions.md`）はチームの標準を自動適用のためにコード化する
6. **一貫した出力**は適切に定義されたエージェントの指示から生まれる

> 📋 **クイックリファレンス**: コマンドとショートカットの完全なリストは [GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)をご覧ください。

---

## ➡️ 次のステップ

エージェントは Copilot がコードに*どう取り組み、具体的なアクションを取るか*を変えます。次は**スキル**について学びます。スキルは*どのようなステップ*を踏むかを変えるものです。エージェントとスキルの違いが気になりますか？Chapter 05 でその答えを正面から取り上げます。

**[Chapter 05: Skills System](../05-skills/README.md)** では、以下を学びます：

- プロンプトからスキルが自動トリガーされる仕組み（スラッシュコマンド不要）
- コミュニティスキルのインストール
- SKILL.md ファイルを使ったカスタムスキルの作成
- エージェント・スキル・MCP の違い
- それぞれの使いどころ

---

**[← Back to Chapter 03](../03-development-workflows/README.md)** | **[Continue to Chapter 05 →](../05-skills/README.md)**
