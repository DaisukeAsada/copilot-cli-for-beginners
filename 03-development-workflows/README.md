![Chapter 03: Development Workflows](images/chapter-header.png)

> **AIが、あなたが気づかなかったバグを見つけてくれたら？**

この章では、GitHub Copilot CLI を毎日使うツールとして活用します。テスト・リファクタリング・デバッグ・Git など、日々の開発ワークフローの中で使い方を学びます。

## 🎯 学習目標

この章を終えると、以下のことができるようになります。

- Copilot CLI で包括的なコードレビューを実施できる
- レガシーコードを安全にリファクタリングできる
- AI の支援を受けながらバグをデバッグできる
- テストを自動生成できる
- Git ワークフローに Copilot CLI を統合できる

> ⏱️ **目安時間**: 約60分（読書15分 + ハンズオン45分）

---

## 🧩 実世界のたとえ: 大工のワークフロー

大工は道具の使い方を知っているだけでなく、さまざまな作業に合わせた*ワークフロー*を持っています。

<img src="images/carpenter-workflow-steps.png" alt="Craftsman workshop showing three workflow lanes: Building Furniture (Measure, Cut, Assemble, Finish), Fixing Damage (Assess, Remove, Repair, Match), and Quality Check (Inspect, Test Joints, Check Alignment)" width="800"/>

同様に、開発者もタスクごとにワークフローを持っています。GitHub Copilot CLI はこれらのワークフローを強化し、日常のコーディング作業をより効率的・効果的にします。

---

# 5つのワークフロー

<img src="images/five-workflows.png" alt="Five glowing neon icons representing code review, testing, debugging, refactoring, and git integration workflows" width="800"/>

以下の各ワークフローは独立しています。今の状況に合うものを選んで取り組んでも、すべて順番にこなしても構いません。

---

## 好きなところから始めよう

この章では開発者がよく使う5つのワークフローを紹介します。**ただし、一度にすべて読む必要はありません！** 各ワークフローは以下の折りたたみセクションで独立して完結しています。現在のプロジェクトに合ったものを選んで取り組んでください。後でいつでも他のワークフローに戻ることができます。

<img src="images/five-workflows-swimlane.png" alt="Five Development Workflows: Code Review, Refactoring, Debugging, Test Generation, and Git Integration shown as horizontal swimlanes" width="800"/>

| やりたいこと | 移動先 |
|---|---|
| マージ前にコードをレビューしたい | [ワークフロー1: コードレビュー](#workflow-1-code-review) |
| 煩雑なコードやレガシーコードを整理したい | [ワークフロー2: リファクタリング](#workflow-2-refactoring) |
| バグを追跡して修正したい | [ワークフロー3: デバッグ](#workflow-3-debugging) |
| コードのテストを生成したい | [ワークフロー4: テスト生成](#workflow-4-test-generation) |
| より良いコミットと PR を書きたい | [ワークフロー5: Git 連携](#workflow-5-git-integration) |
| コーディング前に調査したい | [クイックヒント: 計画・コーディング前の調査](#quick-tip-research-before-you-plan-or-code) |
| バグ修正ワークフローの全体像を見たい | [総まとめ: バグ修正ワークフロー](#putting-it-all-together-bug-fix-workflow) |

**下のワークフローを展開して**、GitHub Copilot CLI が各開発プロセスをどのように強化するか確認してみましょう。

---

<a id="workflow-1-code-review"></a>
<details>
<summary><strong>ワークフロー1: コードレビュー</strong> - ファイルのレビュー、/review エージェントの使用、重要度チェックリストの作成</summary>

<img src="images/code-review-swimlane-single.png" alt="Code review workflow: review, identify issues, prioritize, generate checklist." width="800"/>

### 基本レビュー

この例では `@` シンボルを使ってファイルを参照し、Copilot CLI がレビューのためにそのファイルの内容に直接アクセスできるようにしています。

```bash
copilot

> Review @samples/book-app-project/book_app.py for code quality
```

---

<details>
<summary>🎬 実際の動作を見てみよう！</summary>

![Code Review Demo](images/code-review-demo.gif)

*デモの出力は異なります。お使いのモデル、ツール、および応答はここに示されているものと異なります。*

</details>

---

### 入力バリデーションのレビュー

特定の懸念点（ここでは入力バリデーション）にレビューを絞り込むには、プロンプトで確認したいカテゴリを列挙します。

```text
copilot

> Review @samples/book-app-project/utils.py for input validation issues. Check for: missing validation, error handling gaps, and edge cases
```


### プロジェクト全体のクロスファイルレビュー

`@` でディレクトリ全体を参照すると、Copilot CLI がプロジェクト内のすべてのファイルを一度にスキャンできます。

```bash
copilot

> @samples/book-app-project/ Review this entire project. Create a markdown checklist of issues found, categorized by severity
```

### インタラクティブなコードレビュー

マルチターン会話を使ってより深く掘り下げます。まず広い範囲でレビューし、セッションを再起動せずに追加の質問をします。

```bash
copilot

> @samples/book-app-project/book_app.py Review this file for:
> - Input validation
> - Error handling
> - Code style and best practices

# Copilot CLI provides detailed review

> The user input handling - are there any edge cases I'm missing?

# Copilot CLI shows potential issues with empty strings, special characters

> Create a checklist of all issues found, prioritized by severity

# Copilot CLI generates prioritized action items
```

### レビューチェックリストテンプレート

Copilot CLI に特定のフォーマット（ここでは重要度別に分類した Markdown チェックリスト）で出力するよう指示します。issue に貼り付けて使えます。

```bash
copilot

> Review @samples/book-app-project/ and create a markdown checklist of issues found, categorized by:
> - Critical (data loss risks, crashes)
> - High (bugs, incorrect behavior)
> - Medium (performance, maintainability)
> - Low (style, minor improvements)
```

### Git の変更内容を理解する（/review に重要）

`/review` コマンドを使う前に、git における2種類の変更を理解しておきましょう。

| 変更の種類 | 意味 | 確認方法 |
|-------------|---------------|------------|
| **ステージ済みの変更** | `git add` で次のコミット対象にしたファイル | `git diff --staged` |
| **ステージ前の変更** | 変更済みだがまだ追加していないファイル | `git diff` |

```bash
# クイックリファレンス
git status           # ステージ済み・未ステージ両方を表示
git add file.py      # ファイルをコミット対象にステージ
git diff             # ステージ前の変更を表示
git diff --staged    # ステージ済みの変更を表示
```

### /review コマンドの使い方

`/review` コマンドは組み込みの **code-review エージェント**を呼び出します。ステージ済み・未ステージの変更をノイズの少ない高品質な出力で分析するよう最適化されています。フリーフォームのプロンプトを書く代わりに、スラッシュコマンドで専用の組み込みエージェントを起動できます。

```bash
copilot

> /review
# ステージ済み・未ステージの変更に対して code-review エージェントを起動
# 焦点を絞った実行可能なフィードバックを提供

> /review Check for security issues in authentication
# 特定のフォーカスエリアを指定してレビューを実行
```

> 💡 **ヒント**: code-review エージェントは未コミットの変更があるときに最も効果的です。より集中したレビューのために `git add` でファイルをステージしましょう。

</details>

---

<a id="workflow-2-refactoring"></a>
<details>
<summary><strong>ワークフロー2: リファクタリング</strong> - コードの再構成、関心の分離、エラーハンドリングの改善</summary>

<img src="images/refactoring-swimlane-single.png" alt="Refactoring workflow: assess code, plan changes, implement, verify behavior." width="800"/>

### シンプルなリファクタリング

> **まずこれを試してみましょう:** `@samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.`

シンプルな改善から始めましょう。ブックアプリでこれらを試してみてください。各プロンプトは `@` ファイル参照と具体的なリファクタリング指示を組み合わせているので、Copilot CLI は何を変更すべきかを正確に把握できます。

```bash
copilot

> @samples/book-app-project/book_app.py The command handling uses if/elif chains. Refactor it to use a dictionary dispatch pattern.

> @samples/book-app-project/utils.py Add type hints to all functions

> @samples/book-app-project/book_app.py Extract the book display logic into utils.py for better separation of concerns
```

> 💡 **リファクタリングが初めての方は？** 複雑な変換に取り組む前に、型ヒントの追加や変数名の改善など、シンプルなリクエストから始めましょう。

---

<details>
<summary>🎬 実際の動作を見てみよう！</summary>

![Refactor Demo](images/refactor-demo.gif)

*デモの出力は異なります。お使いのモデル、ツール、および応答はここに示されているものと異なります。*

</details>

---

### 関心の分離

1つのプロンプトで複数のファイルを `@` で参照し、リファクタリングの一環として Copilot CLI がファイル間でコードを移動できるようにします。

```bash
copilot

> @samples/book-app-project/utils.py @samples/book-app-project/book_app.py
> The utils.py file has print statements mixed with logic. Refactor to separate display functions from data processing.
```

### エラーハンドリングの改善

関連する2つのファイルを提供し、横断的な関心事を説明することで、Copilot CLI が両方のファイルにわたって一貫した修正を提案できます。

```bash
copilot

> @samples/book-app-project/utils.py @samples/book-app-project/books.py
> These files have inconsistent error handling. Suggest a unified approach using custom exceptions.
```

### ドキュメントの追加

各 docstring に含めるべき内容を詳細な箇条書きで指定し、Copilot CLI が正確に記述できるようにします。

```bash
copilot

> @samples/book-app-project/books.py Add comprehensive docstrings to all methods:
> - Include parameter types and descriptions
> - Document return values
> - Note any exceptions raised
> - Add usage examples
```

### テストを使った安全なリファクタリング

マルチターン会話で関連する2つのリクエストをつなげます。まずテストを生成し、そのテストをセーフティネットとしてリファクタリングを実施します。

```bash
copilot

> @samples/book-app-project/books.py Before refactoring, generate tests for current behavior

# まずテストを取得する

> Now refactor the BookCollection class to use a context manager for file operations

# 安心してリファクタリング - テストが動作の保持を検証
```

</details>

---

<a id="workflow-3-debugging"></a>
<details>
<summary><strong>ワークフロー3: デバッグ</strong> - バグの追跡、セキュリティ監査、ファイルをまたいだ問題の追跡</summary>

<img src="images/debugging-swimlane-single.png" alt="Debugging workflow: understand error, locate root cause, fix, test." width="800"/>

### シンプルなデバッグ

> **まずこれを試してみましょう:** `@samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.`

何がおかしいかを説明することから始めましょう。バグのあるブックアプリで試せる一般的なデバッグパターンを以下に示します。各プロンプトは `@` ファイル参照と明確な症状の説明を組み合わせているので、Copilot CLI はバグを特定して診断できます。

```bash
copilot

# パターン: 「Xを期待したがYになった」
> @samples/book-app-buggy/books_buggy.py Users report that searching for "The Hobbit" returns no results even though it's in the data. Debug why.

# パターン: 「予期しない動作」
> @samples/book-app-buggy/book_app_buggy.py When I remove a book that doesn't exist, the app says it was removed. Help me find why.

# パターン: 「間違った結果」
> @samples/book-app-buggy/books_buggy.py When I mark one book as read, ALL books get marked. What's the bug?
```

> 💡 **デバッグのヒント**: *症状*（実際に起きていること）と*期待する動作*（本来どうなるべきか）を説明してください。Copilot CLI が残りを解決します。

---

<details>
<summary>🎬 実際の動作を見てみよう！</summary>

![Fix Bug Demo](images/fix-bug-demo.gif)

*デモの出力は異なります。お使いのモデル、ツール、および応答はここに示されているものと異なります。*

</details>

---

### 「バグ探偵」 - AI が関連バグを発見する

ここでコンテキストを考慮したデバッグが輝きます。バグのあるブックアプリでこのシナリオを試してみましょう。`@` でファイル全体を提供し、ユーザーが報告した症状だけを説明します。Copilot CLI は根本原因を追跡し、近くにある別のバグも見つけることがあります。

```bash
copilot

> @samples/book-app-buggy/books_buggy.py
>
> Users report: "Finding books by author name doesn't work for partial names"
> Debug why this happens
```

**Copilot CLI の動作**:
```
根本原因: 80行目が部分一致（in）ではなく完全一致（==）を使用しています。

80行目: return [b for b in self.books if b.author == author]

find_by_author 関数は完全一致が必要です。「Tolkien」で検索しても
「J.R.R. Tolkien」の本は見つかりません。

修正: 大文字小文字を無視した部分一致に変更:
return [b for b in self.books if author.lower() in b.author.lower()]
```

**なぜ重要か**: Copilot CLI はファイル全体を読み込み、バグレポートのコンテキストを理解し、明確な説明付きで具体的な修正を提案します。

> 💡 **おまけ**: Copilot CLI はファイル全体を分析するため、頼んでいない*別の*問題も発見することがよくあります。たとえば、著者検索を修正しながら、`find_book_by_title` の大文字小文字のバグも指摘するかもしれません！

### 実世界のセキュリティサイドバー

自分のコードをデバッグすることも重要ですが、本番アプリケーションのセキュリティ脆弱性を理解することは不可欠です。この例を試してみましょう: 見慣れないファイルに Copilot CLI を向けて、セキュリティ問題を監査させます。

```bash
copilot

> @samples/buggy-code/python/user_service.py Find all security vulnerabilities in this Python user service
```

このファイルは、本番アプリでよく見られる実世界のセキュリティパターンを示しています。

> 💡 **よく出てくるセキュリティ用語:**
> - **SQL インジェクション**: ユーザー入力がデータベースクエリに直接組み込まれ、攻撃者が悪意あるコマンドを実行できる脆弱性
> - **パラメータ化クエリ**: 安全な代替手法 - プレースホルダー（`?`）がユーザーデータと SQL コマンドを分離する
> - **競合状態（Race condition）**: 2つの操作が同時に起きて互いに干渉する問題
> - **XSS（クロスサイトスクリプティング）**: 攻撃者が悪意あるスクリプトをウェブページに注入する攻撃

---

### エラーの理解

スタックトレースを `@` ファイル参照と一緒にプロンプトに直接貼り付けると、Copilot CLI がエラーをソースコードにマッピングできます。

```bash
copilot

> I'm getting this error:
> AttributeError: 'NoneType' object has no attribute 'title'
>     at show_books (book_app.py:19)
>
> @samples/book-app-project/book_app.py Explain why and how to fix it
```

### テストケースを使ったデバッグ

正確な入力と観察された出力を説明することで、Copilot CLI が推論できる具体的で再現可能なテストケースを提供します。

```bash
copilot

> @samples/book-app-buggy/books_buggy.py The remove_book function has a bug. When I try to remove "Dune",
> it also removes "Dune Messiah". Debug this: explain the root cause and provide a fix.
```

### コードをまたいだ問題の追跡

複数のファイルを参照し、データフローをまたいで追いかけて問題の発生源を特定するよう Copilot CLI に依頼します。

```bash
copilot

> Users report that the book list numbering starts at 0 instead of 1.
> @samples/book-app-buggy/book_app_buggy.py @samples/book-app-buggy/books_buggy.py
> Trace through the list display flow and identify where the issue occurs
```

### データ問題の理解

コードを読むデータファイルを一緒に提供することで、Copilot CLI がエラーハンドリングの改善を提案する際に全体像を把握できます。

```bash
copilot

> @samples/book-app-project/data.json @samples/book-app-project/books.py
> Sometimes the JSON file gets corrupted and the app crashes. How should we handle this gracefully?
```

</details>

---

<a id="workflow-4-test-generation"></a>
<details>
<summary><strong>ワークフロー4: テスト生成</strong> - 包括的なテストとエッジケースを自動生成する</summary>

<img src="images/test-gen-swimlane-single.png" alt="Test Generation workflow: analyze function, generate tests, include edge cases, run." width="800"/>

> **まずこれを試してみましょう:** `@samples/book-app-project/books.py Generate pytest tests for all functions including edge cases`

### 「テスト爆発」 - 2件のテスト vs 15件以上のテスト

手動でテストを書く場合、開発者は通常2〜3件の基本的なテストを作成します：
- 有効な入力のテスト
- 無効な入力のテスト
- エッジケースのテスト

Copilot CLI に包括的なテストを生成させるとどうなるか見てみましょう！このプロンプトは `@` ファイル参照と構造化された箇条書きリストを使って、Copilot CLI を十分なテストカバレッジへと導きます：

```bash
copilot

> @samples/book-app-project/books.py Generate comprehensive pytest tests. Include tests for:
> - Adding books
> - Removing books
> - Finding by title
> - Finding by author
> - Marking as read
> - Edge cases with empty data
```

---

<details>
<summary>🎬 実際の動作を見てみよう！</summary>

![Test Generation Demo](images/test-gen-demo.gif)

*デモの出力は異なります。お使いのモデル、ツール、および応答はここに示されているものと異なります。*

</details>

---

**What you get**: 15+ comprehensive tests including:

```python
class TestBookCollection:
    # Happy path
    def test_add_book_creates_new_book(self):
        ...
    def test_list_books_returns_all_books(self):
        ...

    # Find operations
    def test_find_book_by_title_case_insensitive(self):
        ...
    def test_find_book_by_title_returns_none_when_not_found(self):
        ...
    def test_find_by_author_partial_match(self):
        ...
    def test_find_by_author_case_insensitive(self):
        ...

    # Edge cases
    def test_add_book_with_empty_title(self):
        ...
    def test_remove_nonexistent_book(self):
        ...
    def test_mark_as_read_nonexistent_book(self):
        ...

    # Data persistence
    def test_save_books_persists_to_json(self):
        ...
    def test_load_books_handles_missing_file(self):
        ...
    def test_load_books_handles_corrupted_json(self):
        ...

    # Special characters
    def test_add_book_with_unicode_characters(self):
        ...
    def test_find_by_author_with_special_characters(self):
        ...
```

**結果**: 30秒で、1時間かけて考えて書くようなエッジケーステストが手に入ります。

---

### ユニットテスト

1つの関数を対象に、テストしたい入力カテゴリを列挙すると、Copilot CLI が集中した網羅的なユニットテストを生成します。

```bash
copilot

> @samples/book-app-project/utils.py Generate comprehensive pytest tests for get_book_details covering:
> - Valid input
> - Empty strings
> - Invalid year formats
> - Very long titles
> - Special characters in author names
```

### テストの実行

ツールチェーンについて平易な言葉で質問すると、Copilot CLI が適切なシェルコマンドを生成してくれます。

```bash
copilot

> How do I run the tests? Show me the pytest command.

# Copilot CLI が応答:
# cd samples/book-app-project && python -m pytest tests/
# 詳細出力の場合: python -m pytest tests/ -v
# print 文を表示する場合: python -m pytest tests/ -s
```

### 特定シナリオのテスト

カバーしたい高度なシナリオやトリッキーなシナリオを列挙すると、Copilot CLI がハッピーパスを超えたテストを生成します。

```bash
copilot

> @samples/book-app-project/books.py Generate tests for these scenarios:
> - Adding duplicate books (same title and author)
> - Removing a book by partial title match
> - Finding books when collection is empty
> - File permission errors during save
> - Concurrent access to the book collection
```

### 既存ファイルへのテスト追加

1つの関数に対して*追加*のテストを依頼すると、Copilot CLI が既存のテストを補完する新しいケースを生成します。

```bash
copilot

> @samples/book-app-project/books.py
> Generate additional tests for the find_by_author function with edge cases:
> - Author name with hyphens (e.g., "Jean-Paul Sartre")
> - Author with multiple first names
> - Empty string as author
> - Author name with accented characters
```

</details>

---

<a id="workflow-5-git-integration"></a>
<details>
<summary><strong>ワークフロー5: Git 連携</strong> - コミットメッセージ、PR の説明、/pr、/delegate、/diff</summary>

<img src="images/git-integration-swimlane-single.png" alt="Git Integration workflow: stage changes, generate message, commit, create PR." width="800"/>

> 💡 **このワークフローは git の基本的な知識（ステージ、コミット、ブランチ）を前提としています。** git が初めての方は、まず他の4つのワークフローから始めることをおすすめします。

### コミットメッセージの生成

> **まずこれを試してみましょう:** `copilot -p "Generate a conventional commit message for: $(git diff --staged)"` — 変更をステージしてからこれを実行すると、Copilot CLI がコミットメッセージを書いてくれます。

この例では `-p` インラインプロンプトフラグとシェルのコマンド置換を使って、`git diff` の出力を Copilot CLI に直接パイプし、ワンショットでコミットメッセージを生成します。`$(...)` 構文は括弧内のコマンドを実行し、その出力を外側のコマンドに挿入します。

```bash

# 変更内容を確認
git diff --staged

# [Conventional Commit](../GLOSSARY.md#conventional-commit) 形式でコミットメッセージを生成
# （"feat(books): add search" や "fix(data): handle empty input" のような構造化メッセージ）
copilot -p "Generate a conventional commit message for: $(git diff --staged)"

# 出力: "feat(books): add partial author name search
#
# - Update find_by_author to support partial matches
# - Add case-insensitive comparison
# - Improve user experience when searching authors"
```

---

<details>
<summary>🎬 実際の動作を見てみよう！</summary>

![Git Integration Demo](images/git-integration-demo.gif)

*デモの出力は異なります。お使いのモデル、ツール、および応答はここに示されているものと異なります。*

</details>

---

### 変更の説明

`git show` の出力を `-p` プロンプトにパイプして、最後のコミットをわかりやすく要約してもらいます。

```bash
# このコミットは何を変えたか？
copilot -p "Explain what this commit does: $(git show HEAD --stat)"
```

### PR の説明

`git log` の出力と構造化されたプロンプトテンプレートを組み合わせて、完全なプルリクエストの説明を自動生成します。

```bash
# ブランチの変更から PR の説明を生成
copilot -p "Generate a pull request description for these changes:
$(git log main..HEAD --oneline)

Include:
- Summary of changes
- Why these changes were made
- Testing done
- Breaking changes? (yes/no)"
```

### インタラクティブモードで /pr を使う（現在のブランチ）

Copilot CLI のインタラクティブモードでブランチを操作している場合、`/pr` コマンドを使ってプルリクエストを操作できます。`/pr` を使って PR を表示・作成・修正したり、ブランチの状態に基づいて Copilot CLI に自動判断させたりできます。

```bash
copilot

> /pr [view|create|fix|auto]
```

### プッシュ前のレビュー

`-p` プロンプト内で `git diff main..HEAD` を使って、ブランチ全体の変更をプッシュ前に素早く確認します。

```bash
# プッシュ前の最終確認
copilot -p "Review these changes for issues before I push:
$(git diff main..HEAD)"
```

### バックグラウンドタスクに /delegate を使う

`/delegate` コマンドは作業を GitHub Copilot のクラウドエージェントに引き渡します。`/delegate` スラッシュコマンド（または `&` ショートカット）を使って、明確に定義されたタスクをバックグラウンドエージェントにオフロードできます。

```bash
copilot

> /delegate Add input validation to the login form

# または & プレフィックスショートカットを使用:
> & Fix the typo in the README header

# Copilot CLI:
# 1. 変更を新しいブランチにコミット
# 2. ドラフトのプルリクエストを作成
# 3. GitHub 上でバックグラウンドで作業
# 4. 完了したらレビューをリクエスト
```

他の作業に集中しながら完了させたい、明確に定義されたタスクに最適です。

### セッションの変更を確認する /diff

`/diff` コマンドは現在のセッション中に行われたすべての変更を表示します。このスラッシュコマンドを使って、コミットする前に Copilot CLI が変更したすべての内容をビジュアルで確認できます。

```bash
copilot

# 変更をいくつか加えた後...
> /diff

# このセッションで変更されたすべてのファイルのビジュアル diff を表示
# コミット前のレビューに最適
```

</details>

---

## クイックヒント: 計画・コーディング前の調査

ライブラリを調べたり、ベストプラクティスを理解したり、馴染みのないトピックを探索したりする場合は、コードを書く前に `/research` でディープな調査を実行できます：

```bash
copilot

> /research What are the best Python libraries for validating user input in CLI apps?
```

Copilot は GitHub リポジトリとウェブソースを検索し、参照付きのサマリーを返します。新しい機能を始める前に、根拠のある意思決定をしたいときに便利です。結果は `/share` で共有できます。

> 💡 **ヒント**: `/research` は `/plan` の*前*に使うと効果的です。アプローチを調査してから実装を計画しましょう。

---

## 総まとめ: バグ修正ワークフロー

報告されたバグを修正するための完全なワークフローです：

```bash

# 1. バグレポートを理解する
copilot

> Users report: 'Finding books by author name doesn't work for partial names'
> @samples/book-app-project/books.py Analyze and identify the likely cause

# 2. 問題をデバッグする（同じセッションを継続）
> Based on the analysis, show me the find_by_author function and explain the issue

> Fix the find_by_author function to handle partial name matches

# 3. 修正のテストを生成する
> @samples/book-app-project/books.py Generate pytest tests specifically for:
> - Full author name match
> - Partial author name match
> - Case-insensitive matching
> - Author name not found

# 4. コミットメッセージを生成する
copilot -p "Generate commit message for: $(git diff --staged)"

# 出力: "fix(books): support partial author name search"
```

### バグ修正ワークフローのまとめ

| ステップ | アクション | Copilot コマンド |
|------|--------|-----------------|
| 1 | バグを理解する | `> [バグを説明] @relevant-file.py Analyze the likely cause` |
| 2 | 詳細な分析を得る | `> Show me the function and explain the issue` |
| 3 | 修正を実装する | `> Fix the [specific issue]` |
| 4 | テストを生成する | `> Generate tests for [specific scenarios]` |
| 5 | コミットする | `copilot -p "Generate commit message for: $(git diff --staged)"` |

---

# 練習

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

それでは、これらのワークフローを実際に試してみましょう。

---

## ▶️ 自分で試してみよう

デモを完了したら、以下のバリエーションを試してみてください：

1. **バグ探偵チャレンジ**: `samples/book-app-buggy/books_buggy.py` の `mark_as_read` 関数のデバッグを Copilot CLI に依頼してみましょう。1冊だけでなくすべての本が既読になってしまう理由を説明してくれましたか？

2. **テストチャレンジ**: ブックアプリの `add_book` 関数のテストを生成してみましょう。自分では思いつかなかったエッジケースをいくつ含んでいましたか？

3. **コミットメッセージチャレンジ**: ブックアプリのファイルに何か小さな変更を加えてステージし（`git add .`）、以下を実行してみましょう：
   ```bash
   copilot -p "Generate a conventional commit message for: $(git diff --staged)"
   ```
   素早く書いた自分のメッセージより良かったですか？

**セルフチェック**: 「このバグをデバッグして」が「バグを探して」より強力な理由（コンテキストが重要！）を説明できれば、開発ワークフローを理解しています。

---

## 📝 課題

### メインチャレンジ: リファクタリング・テスト・リリース

ハンズオンの例は `find_book_by_title` とコードレビューに焦点を当てていました。今度は `book-app-project` の別の関数で同じワークフロースキルを練習しましょう：

1. **レビュー**: `books.py` の `remove_book()` をエッジケースと潜在的な問題についてレビューするよう Copilot CLI に依頼する：
   `@samples/book-app-project/books.py Review the remove_book() function. What happens if the title partially matches another book (e.g., "Dune" vs "Dune Messiah")? Are there any edge cases not handled?`
2. **リファクタリング**: 大文字小文字を無視したマッチングや、本が見つからない場合の適切なフィードバックなど、エッジケースに対応するよう `remove_book()` の改善を Copilot CLI に依頼する
3. **テスト**: 改善された `remove_book()` 関数のための pytest テストを、以下を網羅する形で生成する：
   - 存在する本の削除
   - 大文字小文字を無視したタイトルマッチング
   - 存在しない本の場合に適切なフィードバックを返す
   - 空のコレクションからの削除
4. **レビュー**: 変更をステージして `/review` を実行し、残った問題を確認する
5. **コミット**: Conventional Commit メッセージを生成する：
   `copilot -p "Generate a conventional commit message for: $(git diff --staged)"`

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**各ステップのサンプルプロンプト:**

```bash
copilot

# ステップ1: レビュー
> @samples/book-app-project/books.py Review the remove_book() function. What edge cases are not handled?

# ステップ2: リファクタリング
> Improve remove_book() to use case-insensitive matching and return a clear message when the book isn't found. Show me the before and after code.

# ステップ3: テスト
> Generate pytest tests for the improved remove_book() function, including:
> - Removing a book that exists
> - Case-insensitive matching ("dune" should remove "Dune")
> - Book not found returns appropriate response
> - Removing from an empty collection

# ステップ4: レビュー
> /review

# ステップ5: コミット
> Generate a conventional commit message for this refactor
```

**ヒント:** `remove_book()` を改善した後、Copilot CLI に「このファイルの他の関数で同じような改善が必要なものはありますか？」と尋ねてみましょう。`find_book_by_title()` や `find_by_author()` にも同様の変更を提案するかもしれません。

</details>

### ボーナスチャレンジ: Copilot CLI でアプリケーションを作成する

> 💡 **注意**: この GitHub Skills の演習では Python ではなく **Node.js** を使用します。練習する GitHub Copilot CLI のテクニック（issue の作成、コードの生成、ターミナルからのコラボレーション）はどの言語にも適用できます。

この演習では、開発者が GitHub Copilot CLI を使って issue を作成し、コードを生成し、Node.js の電卓アプリを構築しながらターミナルからコラボレーションする方法を示します。CLI のインストール、テンプレートとエージェントの使用、反復的なコマンドライン駆動の開発を練習できます。

##### <img src="../images/github-skills-logo.png" width="28" align="center" /> [Start the "Create applications with the Copilot CLI" Skills Exercise](https://github.com/skills/create-applications-with-the-copilot-cli)

---

<details>
<summary>🔧 <strong>よくあるミスとトラブルシューティング</strong>（クリックして展開）</summary>

### よくあるミス

| ミス | 何が起きるか | 対処法 |
|---------|--------------|-----|
| 「このコードをレビューして」のような曖昧なプロンプトを使う | 特定の問題を見逃す一般的なフィードバック | 具体的に: 「SQL インジェクション、XSS、認証の問題をレビューして」 |
| コードレビューに `/review` を使わない | 最適化された code-review エージェントを使い損ねる | `/review` を使う（ノイズの少ない出力に最適化されている） |
| コンテキストなしに「バグを探して」と頼む | Copilot CLI が何のバグか分からない | 症状を説明する: 「ユーザーがYしたときにXが起きると報告している」 |
| フレームワークを指定せずにテストを生成させる | 間違った構文やアサーションライブラリのテストが生成される | 指定する: 「Jest を使ってテストを生成して」や「pytest を使って」 |

### トラブルシューティング

**レビューが不完全に見える** - 何を探すかをより具体的に指定する：

```bash
copilot

# 代わりに:
> Review @samples/book-app-project/book_app.py

# こう試す:
> Review @samples/book-app-project/book_app.py for input validation, error handling, and edge cases
```

**テストが自分のフレームワークと合わない** - フレームワークを指定する：

```bash
copilot

> @samples/book-app-project/books.py Generate tests using pytest (not unittest)
```

**リファクタリングで動作が変わってしまう** - 動作を保持するよう Copilot CLI に指示する：

```bash
copilot

> @samples/book-app-project/book_app.py Refactor command handling to use dictionary dispatch. IMPORTANT: Maintain identical external behavior - no breaking changes
```

</details>

---

# まとめ

## 🔑 重要なポイント

<img src="images/specialized-workflows.png" alt="Specialized Workflows for Every Task: Code Review, Refactoring, Debugging, Testing, and Git Integration" width="800"/>

1. **コードレビュー**は具体的なプロンプトで包括的になる
2. **リファクタリング**はテストを先に生成することで安全になる
3. **デバッグ**はエラーとコードの両方を Copilot CLI に見せることで効果的になる
4. **テスト生成**はエッジケースとエラーシナリオを含めるべき
5. **Git 連携**はコミットメッセージと PR の説明を自動化する

> 📋 **クイックリファレンス**: コマンドとショートカットの完全なリストは [GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)をご覧ください。

---

## ✅ チェックポイント: 基本スキルをマスターしました

**おめでとうございます！** これで GitHub Copilot CLI を生産的に使うためのすべてのコアスキルが身につきました：

| スキル | 章 | できるようになったこと |
|-------|---------|----------------|
| 基本コマンド | 第1章 | インタラクティブモード、プランモード、プログラマティックモード（-p）、スラッシュコマンドを使える |
| コンテキスト | 第2章 | `@` でファイルを参照し、セッションを管理し、コンテキストウィンドウを理解できる |
| ワークフロー | 第3章 | コードのレビュー、リファクタリング、デバッグ、テスト生成、git との統合ができる |

第4〜6章では、さらに強力な追加機能を紹介します。学ぶ価値は十分にあります。

---

## 🛠️ 自分だけのワークフローを構築する

GitHub Copilot CLI の「正しい使い方」はひとつではありません。自分のパターンを作る際のヒントをいくつか紹介します：

> 📚 **公式ドキュメント**: GitHub からの推奨ワークフローとヒントは [Copilot CLI のベストプラクティス](https://docs.github.com/copilot/how-tos/copilot-cli/cli-best-practices)をご覧ください。

- **些細でない作業には `/plan` から始めましょう。** 実行前にプランを磨く - 良いプランは良い結果につながります。
- **うまくいったプロンプトを保存しましょう。** Copilot CLI がミスをしたとき、何が悪かったかをメモしてください。時間が経つにつれ、これがあなた個人のプレイブックになります。
- **自由に実験してください。** 長くて詳細なプロンプトを好む開発者もいれば、短いプロンプトとフォローアップを好む開発者もいます。さまざまなアプローチを試して、自分に合うものを見つけましょう。

> 💡 **次の章では**: 第4章と第5章で、ベストプラクティスをカスタム指示とスキルとしてコード化し、Copilot CLI が自動的に読み込む方法を学びます。

---

## ➡️ 次のステップ

残りの章では、Copilot CLI の機能をさらに拡張する追加機能を紹介します：

| 章 | 内容 | 必要なとき |
|---------|----------------|---------------------|
| 第4章: エージェント | 特化した AI ペルソナを作成する | ドメインエキスパート（フロントエンド、セキュリティ）が必要なとき |
| 第5章: スキル | タスク用の指示を自動読み込みする | 同じプロンプトを繰り返し使うとき |
| 第6章: MCP | 外部サービスに接続する | GitHub やデータベースのライブデータが必要なとき |

**おすすめ**: コアワークフローを1週間試してみてから、具体的なニーズが出てきたら第4〜6章に戻りましょう。

---

## 追加トピックへ続く

**[第4章: エージェントとカスタム指示](../04-agents-custom-instructions/README.md)**では以下を学びます：

- 組み込みエージェントの使用（`/plan`、`/review`）
- 特化したエージェントの作成（フロントエンドエキスパート、セキュリティ監査員）（`.agent.md` ファイルを使用）
- マルチエージェントのコラボレーションパターン
- プロジェクト標準のためのカスタム指示ファイル

---

**[← Back to Chapter 02](../02-context-conversations/README.md)** | **[Continue to Chapter 04 →](../04-agents-custom-instructions/README.md)**
