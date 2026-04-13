![Chapter 02: Context and Conversations](images/chapter-header.png)

> **AIがコードベース全体を、1ファイルずつではなく一度に把握できたらどうでしょう？**

この章では、GitHub Copilot CLIの真の力である「コンテキスト」を解き放ちます。`@`構文を使ってファイルやディレクトリを参照し、Copilot CLIにコードベースを深く理解させる方法を学びます。セッションをまたいで会話を維持する方法、数日後にまったく同じ場所から作業を再開する方法、そして複数ファイルにまたがる分析が単一ファイルのレビューでは見逃すバグを発見する様子も確認できます。

## 🎯 学習目標

この章を終えると、以下のことができるようになります：

- `@`構文を使ってファイル、ディレクトリ、画像を参照する
- `--resume` と `--continue` で過去のセッションを再開する
- [コンテキストウィンドウ](../GLOSSARY.md#context-window)の仕組みを理解する
- 効果的なマルチターン会話を書く
- 複数プロジェクトのワークフローでディレクトリの権限を管理する

> ⏱️ **推定時間**：約50分（読書20分 + ハンズオン30分）

---

## 🧩 実世界のたとえ：同僚と働く

<img src="images/colleague-context-analogy.png" alt="Context Makes the Difference - Without vs With Context" width="800"/>

*同僚と同様に、Copilot CLIは心を読むことはできません。より多くの情報を提供することで、人間にもCopilotにも、的確なサポートができます！*

バグを同僚に説明する場面を想像してください：

> **コンテキストなし**：「ブックアプリが動かない。」

> **コンテキストあり**：「`books.py`の`find_book_by_title`関数を見て。大文字・小文字を区別しないマッチングをしていない。」

Copilot CLIにコンテキストを渡すには、*`@`構文*を使って特定のファイルを指定します。

---

# 基礎編：基本的なコンテキスト

<img src="images/essential-basic-context.png" alt="Glowing code blocks connected by light trails representing how context flows through Copilot CLI conversations" width="800"/>

このセクションでは、コンテキストを効果的に活用するために必要なすべてを扱います。まずはこの基礎をマスターしましょう。

---

## @ 構文

`@`記号は、プロンプト内でファイルやディレクトリを参照するために使います。「このファイルを見て」とCopilot CLIに伝える方法です。

> 💡 **注意**：このコースのすべてのサンプルは、このリポジトリに含まれる`samples/`フォルダを使っているので、すべてのコマンドを直接試せます。

### 今すぐ試してみよう（セットアップ不要）

手元の任意のファイルで試せます：

```bash
copilot

# 手元の任意のファイルを指定
> Explain what @package.json does
> Summarize @README.md
> What's in @.gitignore and why?
```

> 💡 **手元にプロジェクトがない場合**は、簡単なテストファイルを作成してみましょう：
> ```bash
> echo "def greet(name): return 'Hello ' + name" > test.py
> copilot
> > What does @test.py do?
> ```

### 基本的な @ パターン

| パターン | 機能 | 使用例 |
|---------|------|--------|
| `@file.py` | 単一ファイルを参照 | `Review @samples/book-app-project/books.py` |
| `@folder/` | ディレクトリ内の全ファイルを参照 | `Review @samples/book-app-project/` |
| `@file1.py @file2.py` | 複数ファイルを参照 | `Compare @samples/book-app-project/book_app.py @samples/book-app-project/books.py` |

### 単一ファイルの参照

```bash
copilot

> Explain what @samples/book-app-project/utils.py does
```

---

<details>
<summary>🎬 動作を確認する！</summary>

![File Context Demo](images/file-context-demo.gif)

*デモの出力は異なる場合があります。モデル、ツール、応答は表示されているものと異なります。*

</details>

---

### 複数ファイルの参照

```bash
copilot

> Compare @samples/book-app-project/book_app.py and @samples/book-app-project/books.py for consistency
```

### ディレクトリ全体の参照

```bash
copilot

> Review all files in @samples/book-app-project/ for error handling
```

---

## クロスファイルインテリジェンス

ここでコンテキストがスーパーパワーになります。単一ファイルの分析は便利ですが、複数ファイルにまたがる分析は変革的です。

<img src="images/cross-file-intelligence.png" alt="Cross-File Intelligence - comparing single-file vs cross-file analysis showing how analyzing files together reveals bugs, data flow, and patterns invisible in isolation" width="800"/>

### デモ：複数ファイルにまたがるバグを発見する

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/books.py
>
> How do these files work together? What's the data flow?
```

> 💡 **上級者向けオプション**：セキュリティに焦点を当てた複数ファイル分析を試すには、Pythonセキュリティサンプルを使ってみましょう：
> ```bash
> > @samples/buggy-code/python/user_service.py @samples/buggy-code/python/payment_processor.py
> > Find security vulnerabilities that span BOTH files
> ```

---

<details>
<summary>🎬 動作を確認する！</summary>

![Multi-File Demo](images/multi-file-demo.gif)

*デモの出力は異なる場合があります。モデル、ツール、応答は表示されているものと異なります。*

</details>

---

**Copilot CLIが発見すること**：

```
Cross-Module Analysis
=====================

1. DATA FLOW PATTERN
   book_app.py creates BookCollection instance and calls methods
   books.py defines BookCollection class and manages data persistence

   Flow: book_app.py (UI) → books.py (business logic) → data.json (storage)

2. DUPLICATE DISPLAY FUNCTIONS
   book_app.py:9-21    show_books() function
   utils.py:28-36      print_books() function

   Impact: Two nearly identical functions doing the same thing. If you update
   one (like changing the format), you must remember to update the other.

3. INCONSISTENT ERROR HANDLING
   book_app.py handles ValueError from year conversion
   books.py silently returns None/False on errors

   Pattern: No unified approach to error handling across modules
```

**なぜこれが重要か**：単一ファイルのレビューでは全体像を把握できません。複数ファイルにまたがる分析によってのみ以下が明らかになります：
- **重複コード**：統合すべきもの
- **データフローパターン**：コンポーネントがどのように連携しているか
- **アーキテクチャの問題**：保守性に影響を与えるもの

---

### デモ：60秒でコードベースを理解する

<img src="images/codebase-understanding.png" alt="Split-screen comparison showing manual code review taking 1 hour versus AI-assisted analysis taking 10 seconds" width="800" />

新しいプロジェクトに参加した場合でも、Copilot CLIを使えばすぐに把握できます。

```bash
copilot

> @samples/book-app-project/
>
> In one paragraph, what does this app do and what are its biggest quality issues?
```

**得られる結果**：
```
This is a CLI book collection manager that lets users add, list, remove, and
search books stored in a JSON file. The biggest quality issues are:

1. Duplicate display logic - show_books() and print_books() do the same thing
2. Inconsistent error handling - some errors raise exceptions, others return False
3. No input validation - year can be 0, empty strings accepted for title/author
4. Missing tests - no test coverage for critical functions like find_book_by_title

Priority fix: Consolidate duplicate display functions and add input validation.
```

**結果**：コードを1時間かけて読む作業が10秒に圧縮されます。どこに集中すべきかが一目でわかります。

---

## 実践的な例

### 例1：コンテキストを使ったコードレビュー

```bash
copilot

> @samples/book-app-project/books.py Review this file for potential bugs

# Copilot CLI now has the full file content and can give specific feedback:
# "Line 49: Case-sensitive comparison may miss books..."
# "Line 29: JSON decode errors are caught but data corruption isn't logged..."

> What about @samples/book-app-project/book_app.py?

# Now reviewing book_app.py, but still aware of books.py context
```

### 例2：コードベースを理解する

```bash
copilot

> @samples/book-app-project/books.py What does this module do?

# Copilot CLI reads books.py and understands the BookCollection class

> @samples/book-app-project/ Give me an overview of the code structure

# Copilot CLI scans the directory and summarizes

> How does the app save and load books?

# Copilot CLI can trace through the code it's already seen
```

<details>
<summary>🎬 マルチターン会話の動作を確認する！</summary>

![Multi-Turn Demo](images/multi-turn-demo.gif)

*デモの出力は異なる場合があります。モデル、ツール、応答は表示されているものと異なります。*

</details>

### 例3：複数ファイルのリファクタリング

```bash
copilot

> @samples/book-app-project/book_app.py @samples/book-app-project/utils.py
> I see duplicate display functions: show_books() and print_books(). Help me consolidate these.

# Copilot CLI sees both files and can suggest how to merge the duplicate code
```

---

## セッション管理

セッションは作業中に自動保存されます。過去のセッションを再開して、続きから作業を始められます。

### セッションの自動保存

すべての会話は自動的に保存されます。通常通り終了するだけです：

```bash
copilot

> @samples/book-app-project/ Let's improve error handling across all modules

[... do some work ...]

> /exit
```

### 直近セッションの再開

```bash
# 続きから始める
copilot --continue
```

### 特定セッションの再開

```bash
# インタラクティブにセッションを選ぶ
copilot --resume

# またはIDを指定して特定のセッションを再開
copilot --resume abc123
```

> 💡 **セッションIDはどうやって調べる？** 覚える必要はありません。IDなしで`copilot --resume`を実行すると、過去のセッション一覧がインタラクティブに表示され、名前・ID・最終アクティブ日時が確認できます。選ぶだけでOKです。
>
> **複数のターミナルでの動作は？** 各ターミナルウィンドウは独自のコンテキストを持つ独立したセッションです。3つのターミナルでCopilot CLIを開いていれば、それは3つの別セッションです。どのターミナルからでも`--resume`でセッション一覧を参照できます。`--continue`フラグはどのターミナルかに関わらず最後に閉じたセッションを開きます。
>
> **再起動せずにセッションを切り替えられる？** はい。アクティブなセッション内から`/resume`スラッシュコマンドを使います：
> ```
> > /resume
> # 切り替えるセッション一覧が表示される
> ```

### セッションを整理する

後から見つけやすいように、わかりやすい名前を付けましょう：

```bash
copilot

> /rename book-app-review
# Session renamed for easier identification
```

### コンテキストの確認と管理

ファイルや会話を追加するにつれて、Copilot CLIの[コンテキストウィンドウ](../GLOSSARY.md#context-window)が埋まっていきます。管理に役立つコマンドがいくつかあります：

```bash
copilot

> /context
Context usage: 62k/200k tokens (31%)

> /clear
# Abandons the current session (no history saved) and starts a fresh conversation

> /new
# Ends the current session (saving it to history for search/resume) and starts a fresh conversation

> /rewind
# Opens a timeline picker allowing you to roll back to an earlier point in your conversation
```

> 💡 **`/clear` や `/new` を使うタイミング**：books.pyをレビューしていてutils.pyの話に切り替えたい場合は、先に/newを実行しましょう（セッション履歴が不要なら/clear）。そうしないと古いコンテキストが残り、回答が混乱することがあります。

> 💡 **ミスをした、または別のアプローチを試したい場合**：`/rewind`（またはEscキーを2回押す）を使うと**タイムラインピッカー**が開き、会話の任意の時点に戻れます。最後の操作だけでなく、どの時点にでも戻れます。全部やり直さずに間違った道筋から引き返したいときに便利です。

---

### 続きから再開する

<img src="images/session-persistence-timeline.png" alt="Timeline showing how GitHub Copilot CLI sessions persist across days - start on Monday, resume on Wednesday with full context restored" width="800"/>

*セッションは終了時に自動保存されます。数日後に再開しても、ファイル・課題・進捗がすべて復元されます。*

複数日にわたるワークフローを想像してみましょう：

```bash
# Monday: Start book app review
copilot

> /rename book-app-review
> @samples/book-app-project/books.py
> Review and number all code quality issues

Quality Issues Found:
1. Duplicate display functions (book_app.py & utils.py) - MEDIUM
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

> Fix issue #1 (duplicate functions)
# Work on the fix...

> /exit
```

```bash
# Wednesday: Resume exactly where you left off
copilot --continue

> What issues remain unfixed from our book app review?

Remaining issues from our book-app-review session:
2. No input validation for empty strings - MEDIUM
3. Year can be 0 or negative - LOW
4. No type hints on all functions - LOW
5. Missing error logging - LOW

Issue #1 (duplicate functions) was fixed on Monday.

> Let's tackle issue #2 next
```

**これが強力な理由**：数日後、Copilot CLIは以下をすべて覚えています：
- 作業していた正確なファイル
- 課題の番号付きリスト
- すでに対処済みのもの
- 会話のコンテキスト

再説明不要。ファイルの再読み込み不要。作業をそのまま続けるだけです。

---

**🎉 基礎はこれで完了！** `@`構文、セッション管理（`--continue`/`--resume`/`/rename`）、コンテキストコマンド（`/context`/`/clear`）をマスターすれば、十分に生産的に作業できます。以下はオプションです。準備ができたときに戻ってきましょう。

---

# オプション：さらに深く探る

<img src="images/optional-going-deeper.png" alt="Abstract crystal cave in blue and purple tones representing deeper exploration of context concepts" width="800"/>

これらのトピックは上記の基礎の上に構築されています。**興味のあるものを選ぶか、[練習](#practice)に進みましょう。**

| 学びたいこと | ジャンプ先 |
|---|---|
| ワイルドカードパターンと上級セッションコマンド | [追加の @ パターンとセッションコマンド](#additional-patterns) |
| 複数プロンプトにまたがるコンテキストの積み重ね | [コンテキスト対応の会話](#context-aware-conversations) |
| トークン制限と `/compact` | [コンテキストウィンドウの理解](#understanding-context-windows) |
| 参照するファイルの選び方 | [参照対象の選択](#choosing-what-to-reference) |
| スクリーンショットやモックアップの分析 | [画像の操作](#working-with-images) |

<details>
<summary><strong>追加の @ パターンとセッションコマンド</strong></summary>
<a id="additional-patterns"></a>

### 追加の @ パターン

上級者向けに、Copilot CLIはワイルドカードパターンや画像参照もサポートしています：

| パターン | 機能 |
|---------|------|
| `@folder/*.py` | フォルダ内のすべての .py ファイル |
| `@**/test_*.py` | 再帰的ワイルドカード：あらゆる場所のテストファイルを検索 |
| `@image.png` | UIレビュー用の画像ファイル |

```bash
copilot

> Find all TODO comments in @samples/book-app-project/**/*.py
```

### セッション情報の表示

```bash
copilot

> /session
# Shows current session details and workspace summary

> /usage
# Shows session metrics and statistics
```

### セッションの共有

```bash
copilot

> /share file ./my-session.md
# セッションをmarkdownファイルとしてエクスポート

> /share gist
# セッションをGitHub gistとして作成

> /share html
# セッションを自己完結型のインタラクティブなHTMLファイルとしてエクスポート
# チームメンバーとの共有や後日参照するための洗練されたセッションレポートに便利
```

</details>

<details>
<summary><strong>コンテキスト対応の会話</strong></summary>
<a id="context-aware-conversations"></a>

### コンテキスト対応の会話

複数のターンが積み重なっていくマルチターン会話こそが、Copilot CLIの真骨頂です。

#### 例：段階的な改善

```bash
copilot

> @samples/book-app-project/books.py Review the BookCollection class

Copilot CLI: "The class looks functional, but I notice:
1. Missing type hints on some methods
2. No validation for empty title/author
3. Could benefit from better error handling"

> Add type hints to all methods

Copilot CLI: "Here's the class with complete type hints..."
[Shows typed version]

> Now improve error handling

Copilot CLI: "Building on the typed version, here's improved error handling..."
[Adds validation and proper exceptions]

> Generate tests for this final version

Copilot CLI: "Based on the class with types and error handling..."
[Generates comprehensive tests]
```

各プロンプトが前の作業の上に積み重なっていく様子に注目してください。これがコンテキストの力です。

</details>

<details>
<summary><strong>コンテキストウィンドウの理解</strong></summary>
<a id="understanding-context-windows"></a>

### コンテキストウィンドウの理解

基礎編で`/context`と`/clear`はすでに学びました。ここではコンテキストウィンドウの仕組みをより深く解説します。

すべてのAIには「コンテキストウィンドウ」があり、一度に考慮できるテキストの量が決まっています。

<img src="images/context-window-visualization.png" alt="Context Window Visualization" width="800"/>

*コンテキストウィンドウは机のようなもの：一度に置けるものの量が限られています。ファイル、会話履歴、システムプロンプトがすべてスペースを占有します。*

#### 上限に達したときの動作

```bash
copilot

> /context

Context usage: 45,000 / 128,000 tokens (35%)

# As you add more files and conversation, this grows

> @large-codebase/

Context usage: 120,000 / 128,000 tokens (94%)

# Warning: Approaching context limit

> @another-large-file.py

Context limit reached. Older context will be summarized.
```

#### `/compact` コマンド

会話を失いたくないがコンテキストが埋まってきた場合、`/compact`で履歴を要約してトークンを解放します：

```bash
copilot

> /compact
# 会話履歴を要約してコンテキストスペースを解放
# 重要な発見や決定事項は保持される
```

#### コンテキスト効率化のヒント

| 状況 | 操作 | 理由 |
|------|------|------|
| 新しいトピックを始める | `/clear` | 不要なコンテキストを削除 |
| 間違った方向に進んだ | `/rewind` | 任意の以前の時点に戻る |
| 長い会話 | `/compact` | 履歴を要約してトークンを解放 |
| 特定のファイルが必要 | `@folder/`ではなく`@file.py` | 必要なものだけ読み込む |
| 上限に近づいた | `/new` または `/clear` | 新鮮なコンテキスト |
| 複数のトピック | トピックごとに`/rename` | 正しいセッションに簡単に再開 |

#### 大規模コードベースでのベストプラクティス

1. **具体的に指定する**：`@samples/book-app-project/`ではなく`@samples/book-app-project/books.py`
2. **トピック間でコンテキストをクリアする**：フォーカスを切り替えるときは`/new`または`/clear`
3. **`/compact`を使う**：会話を要約してコンテキストを解放
4. **複数セッションを活用する**：機能やトピックごとに1セッション

</details>

<details>
<summary><strong>参照対象の選択</strong></summary>
<a id="choosing-what-to-reference"></a>

### 参照対象の選択

コンテキストにおいて、すべてのファイルが同等というわけではありません。賢く選ぶためのガイドを紹介します：

#### ファイルサイズの考慮

| ファイルサイズ | おおよその[トークン数](../GLOSSARY.md#token) | 戦略 |
|------------|--------------------------|------|
| 小（100行未満） | ~500〜1,500トークン | 自由に参照できる |
| 中（100〜500行） | ~1,500〜7,500トークン | 特定ファイルを参照 |
| 大（500行以上） | 7,500トークン以上 | 厳選し、特定ファイルを使う |
| 超大（1000行以上） | 15,000トークン以上 | 分割するかセクションを絞る |

**具体的な例：**
- ブックアプリの4つのPythonファイル合計 ≈ 2,000〜3,000トークン
- 典型的なPythonモジュール（200行） ≈ 3,000トークン
- Flask APIファイル（400行） ≈ 6,000トークン
- package.json ≈ 200〜500トークン
- 短いプロンプトと応答 ≈ 500〜1,500トークン

> 💡 **コードのクイック目安**：コード行数に~15を掛けるとおおよそのトークン数になります。あくまで目安です。

#### 含めるべきファイル・除外すべきファイル

**高価値**（含める）：
- エントリーポイント（`book_app.py`、`main.py`、`app.py`）
- 質問対象の特定ファイル
- 対象ファイルが直接インポートするファイル
- 設定ファイル（`requirements.txt`、`pyproject.toml`）
- データモデルやデータクラス

**低価値**（除外を検討）：
- 生成ファイル（コンパイル出力、バンドル済みアセット）
- Node modulesやvendorディレクトリ
- 大きなデータファイルやフィクスチャ
- 質問と無関係なファイル

#### 指定の粒度スペクトル

```
広く指定 ────────────────────────► 具体的に指定
@samples/book-app-project/                      @samples/book-app-project/books.py:47-52
     │                                       │
     └─ すべてをスキャン                     └─ 必要なものだけ
        （コンテキストを多く使う）               （コンテキストを節約）
```

**広く指定するとき**（`@samples/book-app-project/`）：
- コードベースの初期探索
- 多くのファイルにまたがるパターン検索
- アーキテクチャレビュー

**具体的に指定するとき**（`@samples/book-app-project/books.py`）：
- 特定の問題のデバッグ
- 特定ファイルのコードレビュー
- 単一関数についての質問

#### 実践例：段階的なコンテキスト読み込み

```bash
copilot

# ステップ1：構造から始める
> @package.json What frameworks does this project use?

# ステップ2：回答に基づいて絞り込む
> @samples/book-app-project/ Show me the project structure

# ステップ3：重要なものに集中する
> @samples/book-app-project/books.py Review the BookCollection class

# ステップ4：必要に応じて関連ファイルを追加
> @samples/book-app-project/book_app.py @samples/book-app-project/books.py How does the CLI use the BookCollection?
```

この段階的なアプローチにより、コンテキストを集中かつ効率的に保てます。

</details>

<details>
<summary><strong>画像の操作</strong></summary>
<a id="working-with-images"></a>

### 画像の操作

`@`構文を使って会話に画像を含めたり、**クリップボードから貼り付ける**（Cmd+V / Ctrl+V）こともできます。Copilot CLIはスクリーンショット、モックアップ、ダイアグラムを分析して、UIデバッグ、デザイン実装、エラー分析を支援します。

```bash
copilot

> @images/screenshot.png What is happening in this image?

> @images/mockup.png Write the HTML and CSS to match this design. Place it in a new file called index.html and put the CSS in styles.css.
```

> 📖 **詳細はこちら**：サポートされているフォーマット、実践的なユースケース、画像とコードを組み合わせるヒントについては、[追加のコンテキスト機能](../appendices/additional-context.md#working-with-images)を参照してください。

</details>

---

# 練習

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

コンテキストとセッション管理のスキルを活かす時間です。

---

## ▶️ 自分で試してみよう

### プロジェクト全体のレビュー

このコースには直接レビューできるサンプルファイルが含まれています。copilotを起動して、次のプロンプトを実行してみましょう：

```bash
copilot

> @samples/book-app-project/ Give me a code quality review of this project

# Copilot CLI will identify issues like:
# - Duplicate display functions
# - Missing input validation
# - Inconsistent error handling
```

> 💡 **自分のファイルで試したい場合**は、小さなPythonプロジェクト（`mkdir -p my-project/src`）を作成し、.pyファイルをいくつか追加してから`@my-project/src/`でレビューしましょう。サンプルコードの作成もcopilotに頼めます！

### セッションワークフロー

```bash
copilot

> /rename book-app-review
> @samples/book-app-project/books.py Let's add input validation for empty titles

[Copilot CLIが検証アプローチを提案]

> Implement that fix
> Now consolidate the duplicate display functions in @samples/book-app-project/
> /exit

# 後から - 続きから再開
copilot --continue

> Generate tests for the changes we made
```

---

デモを完了したら、次のバリエーションを試してみましょう：

1. **クロスファイルチャレンジ**：book_app.pyとbooks.pyの連携を分析する：
   ```bash
   copilot
   > @samples/book-app-project/book_app.py @samples/book-app-project/books.py
   > What's the relationship between these files? Are there any code smells?
   ```

2. **セッションチャレンジ**：セッションを開始して`/rename my-first-session`で名前を付け、何か作業して`/exit`で終了し、`copilot --continue`を実行してみましょう。何をしていたか覚えていますか？

3. **コンテキストチャレンジ**：セッションの途中で`/context`を実行してみましょう。何トークン使っていますか？`/compact`を試してから再度確認してみましょう。（`/compact`の詳細は「さらに深く探る」の[コンテキストウィンドウの理解](#understanding-context-windows)を参照）

**自己確認**：`@folder/`がファイルを個別に開くより強力な理由を説明できれば、コンテキストを理解したということです。

---

## 📝 課題

### メインチャレンジ：データフローを追跡する

ハンズオン例ではコード品質レビューと入力検証に焦点を当てました。今度は同じコンテキストスキルを別のタスクに活用してみましょう。アプリ内でデータがどのように移動するかを追跡します：

1. インタラクティブセッションを開始する：`copilot`
2. `books.py`と`book_app.py`を一緒に参照する：
   `@samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json. What functions are involved at each step?`
3. 追加コンテキストとしてデータファイルを参照する：
   `@samples/book-app-project/data.json What happens if this JSON file is missing or corrupted? Which functions would fail?`
4. クロスファイルの改善提案を求める：
   `@samples/book-app-project/books.py @samples/book-app-project/utils.py Suggest a consistent error-handling strategy that works across both files.`
5. セッション名を変更する：`/rename data-flow-analysis`
6. `/exit`で終了し、`copilot --continue`で再開してデータフローに関するフォローアップ質問をする

**成功基準**：複数ファイルにまたがるデータを追跡し、名前付きセッションを再開し、クロスファイルの提案を得られること。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**始め方：**
```bash
cd /path/to/copilot-cli-for-beginners
copilot
> @samples/book-app-project/books.py @samples/book-app-project/book_app.py Trace how a book goes from user input to being saved in data.json.
> @samples/book-app-project/data.json What happens if this file is missing or corrupted?
> /rename data-flow-analysis
> /exit
```

再開するには：`copilot --continue`

**便利なコマンド：**
- `@file.py` - 単一ファイルを参照
- `@folder/` - フォルダ内の全ファイルを参照（末尾の`/`に注意）
- `/context` - 使用中のコンテキスト量を確認
- `/rename <name>` - 再開しやすいようにセッションに名前を付ける

</details>

### ボーナスチャレンジ：コンテキストの上限

1. `@samples/book-app-project/`でブックアプリのファイルをすべて一度に参照する
2. 異なるファイル（`books.py`、`utils.py`、`book_app.py`、`data.json`）についていくつか詳細な質問をする
3. `/context`を実行して使用量を確認する。どれくらい早く埋まりますか？
4. `/compact`を使ってスペースを回収する練習をして、その後会話を続ける
5. より具体的なファイル参照（フォルダ全体ではなく`@samples/book-app-project/books.py`など）を試して、コンテキスト使用量への影響を確認する

---

<details>
<summary>🔧 <strong>よくあるミスとトラブルシューティング</strong>（クリックして展開）</summary>

### よくあるミス

| ミス | 結果 | 修正方法 |
|------|------|---------|
| ファイル名の前に`@`を忘れる | Copilot CLIが"books.py"を通常テキストとして扱う | `@samples/book-app-project/books.py`のようにファイルを参照する |
| セッションが自動的に持続すると思い込む | 新しく`copilot`を起動すると以前のコンテキストはすべて消える | `--continue`（最後のセッション）または`--resume`（セッションを選ぶ）を使う |
| 現在ディレクトリ外のファイルを参照する | 「Permission denied」または「File not found」エラー | `/add-dir /path/to/directory`でアクセスを許可する |
| トピック切り替え時に`/clear`を使わない | 古いコンテキストが新トピックの回答を混乱させる | 異なるタスクを始める前に`/clear`を実行する |

### トラブルシューティング

**「File not found」エラー** - 正しいディレクトリにいるか確認する：

```bash
pwd  # 現在のディレクトリを確認
ls   # ファイルを一覧表示

# その後copilotを起動して相対パスを使う
copilot

> Review @samples/book-app-project/books.py
```

**「Permission denied」** - ディレクトリを許可リストに追加する：

```bash
copilot --add-dir /path/to/directory

# またはセッション内で：
> /add-dir /path/to/directory
```

**コンテキストが埋まりすぎる場合**：
- ファイル参照をより具体的にする
- 異なるトピックの間に`/clear`を使う
- 複数セッションに分けて作業する

</details>

---

# まとめ

## 🔑 重要なポイント

1. **`@`構文**でCopilot CLIにファイル、ディレクトリ、画像のコンテキストを渡せる
2. **マルチターン会話**はコンテキストが蓄積されるにつれて積み重なっていく
3. **セッションは自動保存**される：`--continue`または`--resume`で続きから始められる
4. **コンテキストウィンドウ**には制限がある：`/clear`、`/compact`、`/context`、`/new`、`/rewind`で管理する
5. **権限フラグ**（`--add-dir`、`--allow-all`）で複数ディレクトリへのアクセスを制御する。慎重に使おう！
6. **画像参照**（`@screenshot.png`）でUIの問題を視覚的にデバッグできる

> 📚 **公式ドキュメント**：コンテキスト、セッション、ファイル操作の完全なリファレンスは[Copilot CLIの使い方](https://docs.github.com/copilot/how-tos/copilot-cli/use-copilot-cli)を参照してください。

> 📋 **クイックリファレンス**：コマンドとショートカットの一覧は[GitHub Copilot CLIコマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)を参照してください。

---

## ➡️ 次のステップ

Copilot CLIにコンテキストを渡せるようになったので、実際の開発タスクに活用しましょう。今学んだコンテキストのテクニック（ファイル参照、クロスファイル分析、セッション管理）は、次の章の強力なワークフローの基礎となります。

**[第3章：開発ワークフロー](../03-development-workflows/README.md)**では以下を学びます：

- コードレビューのワークフロー
- リファクタリングパターン
- デバッグ支援
- テスト生成
- Git連携

---

**[← 第1章に戻る](../01-setup-and-first-steps/README.md)** | **[第3章へ進む →](../03-development-workflows/README.md)**
