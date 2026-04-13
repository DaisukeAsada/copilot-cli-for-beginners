![Chapter 07: Putting It All Together](images/chapter-header.png)

> **これまで学んだすべてがここで統合されます。アイデアからマージ済み PR まで、1 つのセッションで完結します。**

この章では、これまで学んできたすべての内容を完全なワークフローとして統合します。マルチエージェント協調を使った機能開発、コミット前にセキュリティ問題を検出する pre-commit フックのセットアップ、CI/CD パイプラインへの Copilot 統合、そして 1 つのターミナルセッションでアイデアからマージ済み PR まで進める方法を学びます。ここでこそ、GitHub Copilot CLI が真の生産性倍増ツールとして機能します。

> 💡 **メモ**: この章では、これまで学んだすべてを組み合わせる方法を紹介します。**生産性を上げるためにエージェント・スキル・MCP は必須ではありません（とはいえ、非常に役立ちます）。** 基本ワークフロー「説明 → 計画 → 実装 → テスト → レビュー → リリース」は、第 00〜03 章の組み込み機能だけで実現できます。

## 🎯 学習目標

この章を終えると、以下のことができるようになります：

- エージェント・スキル・MCP (Model Context Protocol) を統合ワークフローで組み合わせられる
- マルチツールアプローチで機能を完全に構築できる
- フックを使った基本的な自動化を設定できる
- プロフェッショナルな開発のベストプラクティスを適用できる

> ⏱️ **所要時間の目安**: 約 75 分（読書 15 分 + ハンズオン 60 分）

---

## 🧩 現実世界のたとえ：オーケストラ

<img src="images/orchestra-analogy.png" alt="Orchestra Analogy - Unified Workflow" width="800"/>

交響楽団にはさまざまなセクションがあります：
- **弦楽器**は基盤を担います（コアワークフローのように）
- **金管楽器**は力強さを加えます（専門知識を持つエージェントのように）
- **木管楽器**は彩りを添えます（機能を拡張するスキルのように）
- **打楽器**はリズムを刻みます（外部システムに接続する MCP のように）

それぞれのセクション単独では限られた音しか出せませんが、優れた指揮のもとで一体となったとき、壮大な音楽が生まれます。

**この章で学ぶのはまさにそれです！**<br>
*指揮者がオーケストラを束ねるように、あなたはエージェント・スキル・MCP を統合ワークフローへと指揮します*

それでは、コードの変更・テスト生成・レビュー・PR 作成をすべて 1 つのセッションで行うシナリオを見ていきましょう。

---

## アイデアから PR マージまで、1 セッションで

エディタ・ターミナル・テストランナー・GitHub UI を行き来してそのたびにコンテキストを失う代わりに、すべてのツールを 1 つのターミナルセッションにまとめられます。このパターンの詳細は、以下の[統合パターン](#パワーユーザー向け統合パターン)セクションで解説します。

```bash
# Start Copilot in interactive mode
copilot

> I need to add a "list unread" command to the book app that shows only
> books where read is False. What files need to change?

# Copilot creates high-level plan...

# SWITCH TO PYTHON-REVIEWER AGENT
> /agent
# Select "python-reviewer"

> @samples/book-app-project/books.py Design a get_unread_books method.
> What is the best approach?

# Python-reviewer agent produces:
# - Method signature and return type
# - Filter implementation using list comprehension
# - Edge case handling for empty collections

# SWITCH TO PYTEST-HELPER AGENT
> /agent
# Select "pytest-helper"

> @samples/book-app-project/tests/test_books.py Design test cases for
> filtering unread books.

# Pytest-helper agent produces:
# - Test cases for empty collections
# - Test cases with mixed read/unread books
# - Test cases with all books read

# IMPLEMENT
> Add a get_unread_books method to BookCollection in books.py
> Add a "list unread" command option in book_app.py
> Update the help text in the show_help function

# TEST
> Generate comprehensive tests for the new feature

# Multiple tests are generated similar to the following:
# - Happy path (3 tests) — filters correctly, excludes read, includes unread
# - Edge cases (4 tests) — empty collection, all read, none read, single book
# - Parametrized (5 cases) — varying read/unread ratios via @pytest.mark.parametrize
# - Integration (4 tests) — interplay with mark_as_read, remove_book, add_book, and data integrity

# Review the changes
> /review

# If review passes, use /pr to operate on the pull request for the current branch
> /pr [view|create|fix|auto]

# Or ask naturally if you want Copilot to draft it from the terminal
> Create a pull request titled "Feature: Add list unread books command"
```

**従来のアプローチ**：エディタ・ターミナル・テストランナー・ドキュメント・GitHub UI を切り替えながら作業。切り替えのたびにコンテキストが失われ、摩擦が生じます。

**重要な気づき**：あなたはアーキテクトとして専門家たちを指揮しました。詳細は彼らに任せ、あなたはビジョンに集中するだけです。

> 💡 **さらに発展させるには**：このような大規模なマルチステップの計画には、`/fleet` を試してみてください。Copilot が独立したサブタスクを並列で実行します。詳細は[公式ドキュメント](https://docs.github.com/copilot/concepts/agents/copilot-cli/fleet)をご覧ください。

---

# 追加ワークフロー

<img src="images/combined-workflows.png" alt="People assembling a colorful giant jigsaw puzzle with gears, representing how agents, skills, and MCP combine into unified workflows" width="800"/>

第 04〜06 章を完了したパワーユーザー向けに、エージェント・スキル・MCP を組み合わせて効果を倍増させるワークフローを紹介します。

## 統合パターン

すべてを組み合わせるためのメンタルモデルです：

<img src="images/integration-pattern.png" alt="The Integration Pattern - A 4-phase workflow: Gather Context (MCP), Analyze and Plan (Agents), Execute (Skills + Manual), Complete (MCP)" width="800"/>

---

## ワークフロー 1：バグの調査と修正

全ツールを統合した実践的なバグ修正の流れです：

```bash
copilot

# PHASE 1: Understand the bug from GitHub (MCP provides this)
> Get the details of issue #1

# Learn: "find_by_author doesn't work with partial names"

# PHASE 2: Research best practice (deep research with web + GitHub sources)
> /research Best practices for Python case-insensitive string matching

# PHASE 3: Find related code
> @samples/book-app-project/books.py Show me the find_by_author method

# PHASE 4: Get expert analysis
> /agent
# Select "python-reviewer"

> Analyze this method for issues with partial name matching

# Agent identifies: Method uses exact equality instead of substring matching

# PHASE 5: Fix with agent guidance
> Implement the fix using lowercase comparison and 'in' operator

# PHASE 6: Generate tests
> /agent
# Select "pytest-helper"

> Generate pytest tests for find_by_author with partial matches
> Include test cases: partial name, case variations, no matches

# PHASE 7: Commit and PR
> Generate a commit message for this fix

> Create a pull request linking to issue #1
```

---

## ワークフロー 2：コードレビューの自動化（オプション）

> 💡 **このセクションはオプションです。** pre-commit フックはチームにとって便利ですが、生産的に作業するために必須ではありません。初めて学ぶ方はスキップしても構いません。
>
> ⚠️ **パフォーマンスに関する注意**：このフックはステージされたファイルごとに `copilot -p` を呼び出すため、1 ファイルあたり数秒かかります。コミット対象が多い場合は、重要なファイルに限定するか、`/review` を使った手動レビューを検討してください。

**git フック**とは、Git が特定のタイミング（例：コミット直前）で自動的に実行するスクリプトです。これを使ってコードの自動チェックを実行できます。コミット時に Copilot の自動レビューを設定する方法を紹介します：

```bash
# Create a pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Get staged files (Python files only)
STAGED=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.py$')

if [ -n "$STAGED" ]; then
  echo "Running Copilot review on staged files..."

  for file in $STAGED; do
    echo "Reviewing $file..."

    # Use timeout to prevent hanging (60 seconds per file)
    # --allow-all auto-approves file reads/writes so the hook can run unattended.
    # Only use this in automated scripts. In interactive sessions, let Copilot ask for permission.
    REVIEW=$(timeout 60 copilot --allow-all -p "Quick security review of @$file - critical issues only" 2>/dev/null)

    # Check if timeout occurred
    if [ $? -eq 124 ]; then
      echo "Warning: Review timed out for $file (skipping)"
      continue
    fi

    if echo "$REVIEW" | grep -qi "CRITICAL"; then
      echo "Critical issues found in $file:"
      echo "$REVIEW"
      exit 1
    fi
  done

  echo "Review passed"
fi
EOF

chmod +x .git/hooks/pre-commit
```

> ⚠️ **macOS ユーザーへ**：`timeout` コマンドは macOS にはデフォルトで含まれていません。`brew install coreutils` でインストールするか、`timeout 60` を省いてシンプルな呼び出しに変更してください。

> 📚 **公式ドキュメント**：完全なフック API については [Use hooks](https://docs.github.com/copilot/how-tos/copilot-cli/use-hooks) と [Hooks configuration reference](https://docs.github.com/copilot/reference/hooks-configuration) をご覧ください。
>
> 💡 **組み込みの代替手段**：Copilot CLI には `copilot hooks` という組み込みフックシステムもあり、pre-commit などのイベントで自動実行できます。上記の手動 git フックは完全な制御が可能で、組み込みシステムは設定がより簡単です。どちらが自分のワークフローに合うか、上記ドキュメントを参照して判断してください。

これで、すべてのコミット時に簡易セキュリティレビューが実行されます：

```bash
git add samples/book-app-project/books.py
git commit -m "Update book collection methods"

# Output:
# Running Copilot review on staged files...
# Reviewing samples/book-app-project/books.py...
# Critical issues found in samples/book-app-project/books.py:
# - Line 15: File path injection vulnerability in load_from_file
#
# Fix the issue and try again.
```

---

## ワークフロー 3：新しいコードベースへのオンボーディング

新しいプロジェクトに参加するとき、コンテキスト・エージェント・MCP を組み合わせて素早くキャッチアップできます：

```bash
# Start Copilot in interactive mode
copilot

# PHASE 1: Get the big picture with context
> @samples/book-app-project/ Explain the high-level architecture of this codebase

# PHASE 2: Understand a specific flow
> @samples/book-app-project/book_app.py Walk me through what happens
> when a user runs "python book_app.py add"

# PHASE 3: Get expert analysis with an agent
> /agent
# Select "python-reviewer"

> @samples/book-app-project/books.py Are there any design issues,
> missing error handling, or improvements you would recommend?

# PHASE 4: Find something to work on (MCP provides GitHub access)
> List open issues labeled "good first issue"

# PHASE 5: Start contributing
> Pick the simplest open issue and outline a plan to fix it
```

このワークフローは `@` コンテキスト・エージェント・MCP を 1 つのオンボーディングセッションにまとめたもので、この章の前半で紹介した統合パターンそのものです。

---

# ベストプラクティスと自動化

ワークフローをより効果的にするパターンと習慣を紹介します。

---

## ベストプラクティス

### 1. 分析の前にコンテキストを収集する

分析を依頼する前に、必ずコンテキストを収集しましょう：

```bash
# Good
> Get the details of issue #42
> /agent
# Select python-reviewer
> Analyze this issue

# Less effective
> /agent
# Select python-reviewer
> Fix login bug
# Agent doesn't have issue context
```

### 2. エージェント・スキル・カスタム指示の違いを知る

それぞれのツールには得意な使いどころがあります：

```bash
# Agents: Specialized personas you explicitly activate
> /agent
# Select python-reviewer
> Review this authentication code for security issues

# Skills: Modular capabilities that auto-activate when your prompt
# matches the skill's description (you must create them first — see Ch 05)
> Generate comprehensive tests for this code
# If you have a testing skill configured, it activates automatically

# Custom instructions (.github/copilot-instructions.md): Always-on
# guidance that applies to every session without switching or triggering
```

> 💡 **重要なポイント**：エージェントとスキルはどちらもコードの分析と生成が可能です。本質的な違いは**起動方法**にあります。エージェントは明示的（`/agent`）、スキルは自動（プロンプトにマッチ）、カスタム指示は常時適用されます。

### 3. セッションを集中させる

`/rename` でセッションにラベルを付け（履歴から見つけやすくなります）、`/exit` でクリーンに終了させましょう：

```bash
# Good: One feature per session
> /rename list-unread-feature
# Work on list unread
> /exit

copilot
> /rename export-csv-feature
# Work on CSV export
> /exit

# Less effective: Everything in one long session
```

### 4. Copilot でワークフローを再利用可能にする

ワークフローを Wiki に文書化するだけでなく、Copilot が活用できる形でリポジトリに直接組み込みましょう：

- **カスタム指示**（`.github/copilot-instructions.md`）：コーディング標準・アーキテクチャルール・ビルド/テスト/デプロイ手順を常時適用するガイダンス。すべてのセッションで自動的に従われます。
- **プロンプトファイル**（`.github/prompts/`）：コードレビュー・コンポーネント生成・PR 説明などのテンプレートとして、チームで共有できる再利用可能なプロンプト。
- **カスタムエージェント**（`.github/agents/`）：セキュリティレビュアーやドキュメントライターなど、チームの誰もが `/agent` で起動できる専門ペルソナをエンコード。
- **カスタムスキル**（`.github/skills/`）：関連するときに自動起動するステップバイステップのワークフロー指示をパッケージ化。

> 💡 **メリット**：新しいチームメンバーがあなたのワークフローを無償で手に入れられます。誰かの頭の中にロックされるのではなく、リポジトリに組み込まれているからです。

---

## ボーナス：本番環境のパターン

これらのパターンはオプションですが、プロフェッショナルな環境では非常に有用です。

### PR 説明文ジェネレーター

```bash
# Generate comprehensive PR descriptions
BRANCH=$(git branch --show-current)
COMMITS=$(git log main..$BRANCH --oneline)

copilot -p "Generate a PR description for:
Branch: $BRANCH
Commits:
$COMMITS

Include: Summary, Changes Made, Testing Done, Screenshots Needed"
```

### CI/CD 統合

既存の CI/CD パイプラインを持つチームは、GitHub Actions を使ってすべての pull request に対して Copilot レビューを自動化できます。レビューコメントの自動投稿や重大な問題のフィルタリングも含みます。

> 📖 **詳細はこちら**：完全な GitHub Actions ワークフロー・設定オプション・トラブルシューティングのヒントは [CI/CD Integration](../appendices/ci-cd-integration.md) をご覧ください。

---

# 実践

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

完全なワークフローを実際に体験しましょう。

---

## ▶️ 自分で試してみよう

デモを終えたら、次のバリエーションを試してみてください：

1. **エンドツーエンドチャレンジ**：小さな機能を選びます（例：「未読の本をリスト表示」や「CSV にエクスポート」）。完全なワークフローで取り組んでみましょう：
   - `/plan` で計画
   - エージェント（python-reviewer、pytest-helper）で設計
   - 実装
   - テストを生成
   - PR を作成

2. **自動化チャレンジ**：コードレビュー自動化ワークフローの pre-commit フックをセットアップします。意図的なファイルパス脆弱性を含むコミットを作成してみましょう。ブロックされますか？

3. **自分のプロダクションワークフロー**：よく行う作業のための独自ワークフローを設計しましょう。チェックリストとして書き出してみてください。スキル・エージェント・フックで自動化できる部分はどこでしょうか？

**自己チェック**：エージェント・スキル・MCP がどのように連携するか、そしてそれぞれをいつ使うかを同僚に説明できるようになったとき、このコースを完了したといえます。

---

## 📝 課題

### メインチャレンジ：エンドツーエンドの機能実装

ハンズオン例では「未読の本をリスト表示」機能を構築しました。今度は別の機能「**年範囲で本を検索する**」について完全なワークフローを実践してみましょう：

1. Copilot を起動してコンテキストを収集します：`@samples/book-app-project/books.py`
2. `/plan Add a "search by year" command that lets users find books published between two years` で計画
3. `BookCollection` に `find_by_year_range(start_year, end_year)` メソッドを実装
4. `book_app.py` に、開始年と終了年をユーザーに入力させる `handle_search_year()` 関数を追加
5. テストを生成：`@samples/book-app-project/books.py @samples/book-app-project/tests/test_books.py Generate tests for find_by_year_range() including edge cases like invalid years, reversed range, and no results.`
6. `/review` でレビュー
7. README を更新：`@samples/book-app-project/README.md Add documentation for the new "search by year" command.`
8. コミットメッセージを生成

作業中にワークフローを記録していきましょう。

**達成基準**：Copilot CLI を使って、計画・実装・テスト・ドキュメント・レビューを含む、アイデアからコミットまでの機能開発を完結できたとき。

> 💡 **ボーナス**：第 04 章でエージェントをセットアップ済みの場合は、カスタムエージェントの作成と活用を試してみましょう。たとえば、実装レビュー用の error-handler エージェントや、README 更新用の doc-writer エージェントなどが考えられます。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**この章の冒頭にある[「アイデアから PR マージまで」](#アイデアから-pr-マージまで1-セッションで)の例のパターンに従ってください。** 主なステップは次のとおりです：

1. `@samples/book-app-project/books.py` でコンテキストを収集
2. `/plan Add a "search by year" command` で計画
3. メソッドとコマンドハンドラーを実装
4. エッジケース（無効な入力・結果なし・逆順の範囲）を含むテストを生成
5. `/review` でレビュー
6. `@samples/book-app-project/README.md` で README を更新
7. `-p` でコミットメッセージを生成

**考慮すべきエッジケース：**
- ユーザーが「2000」と「1990」を入力した場合（逆順の範囲）はどうなりますか？
- 範囲に一致する本がない場合はどうなりますか？
- ユーザーが数値以外の入力をした場合はどうなりますか？

**重要なのは完全なワークフローを実践すること**：アイデア → コンテキスト → 計画 → 実装 → テスト → ドキュメント → コミット。

</details>

---

<details>
<summary>🔧 <strong>よくある間違い</strong>（クリックして展開）</summary>

| 間違い | 何が起こるか | 対処法 |
|--------|------------|--------|
| 実装に直接飛びつく | 後で修正コストが高くなる設計上の問題を見落とす | まず `/plan` でアプローチを考える |
| 1 つのツールだけ使う | 遅く、より不完全な結果になる | 組み合わせる：分析にエージェント → 実行にスキル → 統合に MCP |
| コミット前にレビューしない | セキュリティ問題やバグが見過ごされる | 常に `/review` を実行するか [pre-commit フック](#ワークフロー-2コードレビューの自動化オプション)を使う |
| チームとワークフローを共有しない | 各自が同じことを一から考える | 共有エージェント・スキル・指示にパターンを文書化する |

</details>

---

# まとめ

## 🔑 重要なポイント

1. **統合 > 孤立**：最大の効果を発揮するにはツールを組み合わせる
2. **コンテキストを最初に**：分析の前に必要なコンテキストを収集する
3. **エージェントは分析、スキルは実行**：目的に合ったツールを使う
4. **繰り返しを自動化**：フックとスクリプトで効率を倍増させる
5. **ワークフローを文書化**：共有可能なパターンがチーム全体に恩恵をもたらす

> 📋 **クイックリファレンス**：コマンドとショートカットの完全なリストは [GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference) をご覧ください。

---

## 🎓 コース完了！

おめでとうございます！ここまで学んできた内容です：

| 章 | 学んだこと |
|----|---------| 
| 00 | Copilot CLI のインストールとクイックスタート |
| 01 | 3 つのインタラクションモード |
| 02 | `@` 構文によるコンテキスト管理 |
| 03 | 開発ワークフロー |
| 04 | 特化型エージェント |
| 05 | 拡張可能なスキル |
| 06 | MCP による外部接続 |
| 07 | 統合プロダクションワークフロー |

これで、GitHub Copilot CLI を開発ワークフローの真の生産性倍増ツールとして活用する準備が整いました。

## ➡️ 次のステップ

学習はここで終わりではありません：

1. **毎日実践する**：実際の作業に Copilot CLI を活用する
2. **カスタムツールを作る**：自分のニーズに合ったエージェントとスキルを作成する
3. **知識を共有する**：チームがこれらのワークフローを採用できるよう支援する
4. **最新情報をフォローする**：GitHub Copilot のアップデートで新機能を確認する

### リソース

- [GitHub Copilot CLI ドキュメント](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
- [Community Skills](https://github.com/topics/copilot-skill)

---

**よく頑張りました！さあ、素晴らしいものを作っていきましょう。**

**[← 第 06 章に戻る](../06-mcp-servers/README.md)** | **[コースホームに戻る →](../README.md)**
