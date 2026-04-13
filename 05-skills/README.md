![Chapter 05: Skills System](images/chapter-header.png)

> **Copilot がチームのベストプラクティスを毎回説明しなくても自動で適用してくれたら、どうでしょう？**

この章では、Agent Skills（エージェントスキル）について学びます。スキルとは、Copilot がタスクに関連すると判断したときに自動で読み込む指示書フォルダのことです。エージェントが Copilot の「考え方」を変えるのに対して、スキルは「タスクの具体的な実行方法」を教えます。セキュリティ監査スキルを作成して Copilot がセキュリティ関連の質問に自動適用できるようにしたり、チーム標準のレビュー基準を構築してコード品質を一貫させたり、Copilot CLI・VS Code・GitHub Copilot クラウドエージェントにまたがるスキルの動作を学んだりします。


## 🎯 学習目標

この章を終えると、次のことができるようになります：

- Agent Skills の仕組みと活用タイミングを理解する
- SKILL.md ファイルでカスタムスキルを作成する
- 共有リポジトリからコミュニティスキルを利用する
- スキル・エージェント・MCP の使い分けを理解する

> ⏱️ **所要時間の目安**：約55分（読書20分 + ハンズオン35分）

---

## 🧩 実世界の例え：電動工具

汎用ドリルも便利ですが、専用のアタッチメントがあればさらに強力になります。
<img src="images/power-tools-analogy.png" alt="Power Tools - Skills Extend Copilot's Capabilities" width="800"/>


スキルも同じように機能します。作業に合わせてドリルビットを取り替えるように、Copilot にもタスクに応じたスキルを追加できます：

| スキルのアタッチメント | 目的 |
|------------|---------|
| `commit` | 一貫したコミットメッセージを生成する |
| `security-audit` | OWASP 脆弱性をチェックする |
| `generate-tests` | 包括的な pytest テストを作成する |
| `code-checklist` | チームのコード品質基準を適用する |



*スキルは Copilot の機能を拡張する専用アタッチメントです*

---

# スキルの仕組み

<img src="images/how-skills-work.png" alt="Glowing RPG-style skill icons connected by light trails on a starfield background representing Copilot skills" width="800"/>

スキルとは何か、なぜ重要なのか、エージェントや MCP とどう違うのかを学びます。

---

## *スキル初心者の方はここから！*

1. **利用可能なスキルを確認する：**
   ```bash
   copilot
   > /skills list
   ```
   すべてのスキルが表示されます。CLI 自体に同梱されている**組み込みスキル**や、プロジェクト・個人フォルダ内のスキルも含まれます。

   > 💡 **組み込みスキル**：Copilot CLI にはスキルがあらかじめインストールされています。たとえば `customizing-copilot-cloud-agents-environment` スキルは、Copilot クラウドエージェントの環境をカスタマイズするためのガイドを提供します。何もインストールしなくても利用できます。`/skills list` を実行して利用可能なスキルを確認しましょう。

2. **実際のスキルファイルを見てみる：** 提供されている [code-checklist SKILL.md](../.github/skills/code-checklist/SKILL.md) を見てパターンを確認しましょう。YAML フロントマターとマークダウン形式の指示書だけです。

3. **核心を理解する：** スキルはタスク固有の指示書で、プロンプトがスキルの説明と合致したとき Copilot が*自動的に*読み込みます。アクティベートする必要はなく、自然に質問するだけで機能します。


## スキルを理解する

Agent Skills は、指示書・スクリプト・リソースを含んだフォルダで、Copilot がタスクに関連すると判断したときに**自動的に読み込まれます**。Copilot はプロンプトを読んで合致するスキルがないかを確認し、関連する指示書を自動で適用します。

```bash
copilot

> Check books.py against our quality checklist
# Copilot detects this matches your "code-checklist" skill
# and automatically applies its Python quality checklist

> Generate tests for the BookCollection class
# Copilot loads your "pytest-gen" skill
# and applies your preferred test structure

> What are the code quality issues in this file?
# Copilot loads your "code-checklist" skill
# and checks against your team's standards
```

> 💡 **重要なポイント**：スキルはプロンプトとスキルの説明が合致したときに**自動でトリガーされます**。自然に質問するだけで、Copilot が裏側で関連スキルを適用します。スキルを直接呼び出すこともできます。その方法は次のセクションで説明します。

> 🧰 **すぐに使えるテンプレート**：[.github/skills](../.github/skills/) フォルダにコピー&ペーストで使えるシンプルなスキルが用意されています。

### スラッシュコマンドによる直接呼び出し

自動トリガーがスキルの主な使い方ですが、スキル名をスラッシュコマンドとして使って**直接呼び出す**こともできます：

```bash
> /generate-tests Create tests for the user authentication module

> /code-checklist Check books.py for code quality issues

> /security-audit Check the API endpoints for vulnerabilities
```

特定のスキルを確実に使いたい場合に、明示的にコントロールできます。

> 📝 **スキルとエージェントの呼び出しを混同しないように**：
> - **スキル**：`/スキル名 <プロンプト>`（例：`/code-checklist このファイルを確認して`）
> - **エージェント**：`/agent`（リストから選択）または `copilot --agent <名前>`（コマンドライン）
>
> スキルとエージェントで同じ名前のもの（例：「code-reviewer」）がある場合、`/code-reviewer` と入力すると**スキル**が呼び出されます（エージェントではありません）。

### スキルが使われたかどうかを確認する方法

Copilot に直接聞くことができます：

```bash
> What skills did you use for that response?

> What skills do you have available for security reviews?
```

### スキル・エージェント・MCP の比較

スキルは GitHub Copilot の拡張モデルの一部に過ぎません。エージェントや MCP サーバーとの違いを確認しましょう。

> *MCP についてはまだ心配しなくて大丈夫です。[第6章](../06-mcp-servers/)で詳しく説明します。ここでは、スキルが全体像のどこに位置するかを理解するために触れています。*

<img src="images/skills-agents-mcp-comparison.png" alt="Comparison diagram showing the differences between Agents, Skills, and MCP Servers and how they combine into your workflow" width="800"/>

| 機能 | 役割 | 使いどころ |
|---------|--------------|-------------|
| **エージェント** | AI の考え方を変える | 多くのタスクにまたがる専門知識が必要なとき |
| **スキル** | タスク固有の指示を提供する | 詳細な手順を持つ特定の繰り返しタスク |
| **MCP** | 外部サービスに接続する | API からライブデータが必要なとき |

広範な専門知識にはエージェント、特定タスクの指示にはスキル、外部データにはMCPを使いましょう。エージェントは会話中に1つ以上のスキルを使うことができます。例えば、コードチェックをエージェントに頼んだとき、`security-audit` スキルと `code-checklist` スキルの両方が自動で適用されることがあります。

> 📚 **詳細情報**：スキルのフォーマットとベストプラクティスの完全なリファレンスは、公式ドキュメント [About Agent Skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills) を参照してください。

---

## 手動プロンプトから自動的な専門知識へ

スキルの作り方を学ぶ前に、なぜ学ぶ価値があるかを確認しましょう。一貫性の向上を実感すれば、「どうやって作るか」が自然と理解できます。

### スキル導入前：バラバラなレビュー

コードレビューのたびに何かを忘れてしまうことがあります：

```bash
copilot

> Review this code for issues
# Generic review - might miss your team's specific concerns
```

あるいは、毎回長いプロンプトを書くことになります：

```bash
> Review this code checking for bare except clauses, missing type hints,
> mutable default arguments, missing context managers for file I/O,
> functions over 50 lines, print statements in production code...
```

所要時間：入力に**30秒以上**。一貫性：**記憶力次第**。

### スキル導入後：自動的なベストプラクティス

`code-checklist` スキルをインストールすれば、自然に質問するだけです：

```bash
copilot

> Check the book collection code for quality issues
```

**裏側で何が起きているか**：
1. Copilot がプロンプトの中に「コード品質」と「問題」というキーワードを検出する
2. スキルの説明を確認し、`code-checklist` スキルが合致すると判断する
3. チームの品質チェックリストを自動で読み込む
4. リストを入力しなくてもすべてのチェックを適用する

<img src="images/skill-auto-discovery-flow.png" alt="How Skills Auto-Trigger - 4-step flow showing how Copilot automatically matches your prompt to the right skill" width="800"/>

*自然に質問するだけ。Copilot がプロンプトを適切なスキルに紐付け、自動で適用します。*

**出力例**：
```
## Code Checklist: books.py

### Code Quality
- [PASS] All functions have type hints
- [PASS] No bare except clauses
- [PASS] No mutable default arguments
- [PASS] Context managers used for file I/O
- [PASS] Functions are under 50 lines
- [PASS] Variable and function names follow PEP 8

### Input Validation
- [FAIL] User input is not validated - add_book() accepts any year value
- [FAIL] Edge cases not fully handled - empty strings accepted for title/author
- [PASS] Error messages are clear and helpful

### Testing
- [FAIL] No corresponding pytest tests found

### Summary
3 items need attention before merge
```

**違いは何か**：チームの基準が毎回自動で適用され、わざわざ入力する必要がありません。

---

<details>
<summary>🎬 実際の動作を見てみましょう！</summary>

![Skill Trigger Demo](images/skill-trigger-demo.gif)

*デモの出力はサンプルです。実際のモデル・ツール・レスポンスは異なる場合があります。*

</details>

---

## スケールでの一貫性：チームの PR レビュースキル

チームに10項目のPRチェックリストがあるとします。スキルがなければ、全員が10項目を覚えなければならず、必ず誰かが1つ忘れてしまいます。`pr-review` スキルがあれば、チーム全体で一貫したレビューができます：

```bash
copilot

> Can you review this PR?
```

Copilot はチームの `pr-review` スキルを自動で読み込み、10項目すべてをチェックします：

```
PR Review: feature/user-auth

## Security ✅
- No hardcoded secrets
- Input validation present
- No bare except clauses

## Code Quality ⚠️
- [WARN] print statement on line 45 - remove before merge
- [WARN] TODO on line 78 missing issue reference
- [WARN] Missing type hints on public functions

## Testing ✅
- New tests added
- Edge cases covered

## Documentation ❌
- [FAIL] Breaking change not documented in CHANGELOG
- [FAIL] API changes need OpenAPI spec update
```

**スキルの強み**：チームの全員が同じ基準を自動で適用できます。新メンバーもチェックリストを暗記する必要がなく、スキルが代わりに対応します。

---

# カスタムスキルの作成

<img src="images/creating-managing-skills.png" alt="Human and robotic hands building a wall of glowing LEGO-like blocks representing skill creation and management" width="800"/>

SKILL.md ファイルから独自のスキルを作成しましょう。

---

## スキルの保存場所

スキルは `.github/skills/`（プロジェクト固有）または `~/.copilot/skills/`（ユーザーレベル）に保存します。

### Copilot がスキルを検索する場所

Copilot はスキルを探すために以下の場所を自動でスキャンします：

| 場所 | スコープ |
|----------|-------|
| `.github/skills/` | プロジェクト固有（git でチームと共有） |
| `~/.copilot/skills/` | ユーザー固有（個人スキル） |

### スキルの構造

各スキルは `SKILL.md` ファイルを含む専用フォルダに配置します。スクリプト・例・その他のリソースを任意で追加できます：

```
.github/skills/
└── my-skill/
    ├── SKILL.md           # Required: Skill definition and instructions
    ├── examples/          # Optional: Example files Copilot can reference
    │   └── sample.py
    └── scripts/           # Optional: Scripts the skill can use
        └── validate.sh
```

> 💡 **ヒント**：ディレクトリ名は SKILL.md フロントマターの `name` フィールドと一致させましょう（小文字・ハイフン区切り）。

### SKILL.md のフォーマット

スキルはシンプルな YAML フロントマター付きマークダウン形式を使います：

```markdown
---
name: code-checklist
description: Comprehensive code quality checklist with security, performance, and maintainability checks
license: MIT
---

# Code Checklist

When checking code, look for:

## Security
- SQL injection vulnerabilities
- XSS vulnerabilities
- Authentication/authorization issues
- Sensitive data exposure

## Performance
- N+1 query problems (running one query per item instead of one query for all items)
- Unnecessary loops or computations
- Memory leaks
- Blocking operations

## Maintainability
- Function length (flag functions > 50 lines)
- Code duplication
- Missing error handling
- Unclear naming

## Output Format
Provide issues as a numbered list with severity:
- [CRITICAL] - Must fix before merge
- [HIGH] - Should fix before merge
- [MEDIUM] - Should address soon
- [LOW] - Nice to have
```

**YAML プロパティ：**

| プロパティ | 必須 | 説明 |
|----------|----------|-------------|
| `name` | **必須** | 一意の識別子（小文字、スペースはハイフンで） |
| `description` | **必須** | スキルの機能と Copilot がいつ使うべきかの説明 |
| `license` | 任意 | このスキルに適用するライセンス |

> 📖 **公式ドキュメント**：[About Agent Skills](https://docs.github.com/copilot/concepts/agents/about-agent-skills)

### はじめてのスキルを作成する

OWASP Top 10 の脆弱性をチェックするセキュリティ監査スキルを作成しましょう：

```bash
# Create skill directory
mkdir -p .github/skills/security-audit

# Create the SKILL.md file
cat > .github/skills/security-audit/SKILL.md << 'EOF'
---
name: security-audit
description: Security-focused code review checking OWASP (Open Web Application Security Project) Top 10 vulnerabilities
---

# Security Audit

Perform a security audit checking for:

## Injection Vulnerabilities
- SQL injection (string concatenation in queries)
- Command injection (unsanitized shell commands)
- LDAP injection
- XPath injection

## Authentication Issues
- Hardcoded credentials
- Weak password requirements
- Missing rate limiting
- Session management flaws

## Sensitive Data
- Plaintext passwords
- API keys in code
- Logging sensitive information
- Missing encryption

## Access Control
- Missing authorization checks
- Insecure direct object references
- Path traversal vulnerabilities

## Output
For each issue found, provide:
1. File and line number
2. Vulnerability type
3. Severity (CRITICAL/HIGH/MEDIUM/LOW)
4. Recommended fix
EOF

# Test your skill (skills load automatically based on your prompt)
copilot

> @samples/book-app-project/ Check this code for security vulnerabilities
# Copilot detects "security vulnerabilities" matches your skill
# and automatically applies its OWASP checklist
```

**期待される出力**（実際の結果は異なる場合があります）：

```
Security Audit: book-app-project

[HIGH] Hardcoded file path (book_app.py, line 12)
  File path is hardcoded rather than configurable
  Fix: Use environment variable or config file

[MEDIUM] No input validation (book_app.py, line 34)
  User input passed directly to function without sanitization
  Fix: Add input validation before processing

✅ No SQL injection found
✅ No hardcoded credentials found
```

---

## 効果的なスキル説明の書き方

SKILL.md の `description` フィールドは非常に重要です！Copilot がスキルを読み込むかどうかはここで決まります：

```markdown
---
name: security-audit
description: Use for security reviews, vulnerability scanning,
  checking for SQL injection, XSS, authentication issues,
  OWASP Top 10 vulnerabilities, and security best practices
---
```

> 💡 **ヒント**：自然な質問の仕方に合ったキーワードを含めましょう。「セキュリティレビュー」と言うなら、説明に「セキュリティレビュー」を含めてください。

### スキルとエージェントを組み合わせる

スキルとエージェントは連携して動作します。エージェントが専門知識を提供し、スキルが具体的な指示を追加します：

```bash
# Start with a code-reviewer agent
copilot --agent code-reviewer

> Check the book app for quality issues
# code-reviewer agent's expertise combines
# with your code-checklist skill's checklist
```

---

# スキルの管理と共有

インストール済みスキルの確認、コミュニティスキルの探し方、自分のスキルの共有方法を学びます。

<img src="images/managing-sharing-skills.png" alt="Managing and Sharing Skills - showing the discover, use, create, and share cycle for CLI skills" width="800" />

---

## `/skills` コマンドによるスキル管理

`/skills` コマンドでインストール済みスキルを管理できます：

| コマンド | 機能 |
|---------|--------------|
| `/skills list` | インストール済みスキルをすべて表示する |
| `/skills info <name>` | 特定のスキルの詳細を確認する |
| `/skills add <name>` | スキルを有効化する（リポジトリやマーケットプレイスから） |
| `/skills remove <name>` | スキルを無効化またはアンインストールする |
| `/skills reload` | SKILL.md ファイルの編集後にスキルを再読み込みする |

> 💡 **覚えておきましょう**：プロンプトごとにスキルを「アクティベート」する必要はありません。インストール済みのスキルは、プロンプトが説明と合致したときに**自動でトリガーされます**。これらのコマンドは、利用可能なスキルを管理するためのものです（スキルを使うためではありません）。

### 例：スキルを確認する

```bash
copilot

> /skills list

Available skills:
- security-audit: Security-focused code review checking OWASP Top 10
- generate-tests: Generate comprehensive unit tests with edge cases
- code-checklist: Team code quality checklist
...

> /skills info security-audit

Skill: security-audit
Source: Project
Location: .github/skills/security-audit/SKILL.md
Description: Security-focused code review checking OWASP Top 10 vulnerabilities
```

---

<details>
<summary>実際の動作を見てみましょう！</summary>

![List Skills Demo](images/list-skills-demo.gif)

*デモの出力はサンプルです。実際のモデル・ツール・レスポンスは異なる場合があります。*

</details>

---

### `/skills reload` を使うタイミング

スキルの SKILL.md ファイルを作成・編集した後は、Copilot を再起動せずに `/skills reload` を実行して変更を反映させましょう：

```bash
# Edit your skill file
# Then in Copilot:
> /skills reload
Skills reloaded successfully.
```

> 💡 **知っておくと便利**：会話履歴を要約する `/compact` を使った後も、スキルは引き続き有効です。コンパクト後に再読み込みする必要はありません。

---

## コミュニティスキルの探し方と使い方

### プラグインを使ってスキルをインストールする

> 💡 **プラグインとは？** プラグインはスキル・エージェント・MCP サーバー設定をまとめてバンドルできるインストール可能なパッケージです。Copilot CLI の「アプリストア」拡張機能のようなものです。

`/plugin` コマンドでこれらのパッケージを検索・インストールできます：

```bash
copilot

> /plugin list
# Shows installed plugins

> /plugin marketplace
# Browse available plugins

> /plugin install <plugin-name>
# Install a plugin from the marketplace
```

プラグインは複数の機能をまとめてバンドルできます。1つのプラグインに、連携して動作する関連スキル・エージェント・MCP サーバー設定が含まれる場合もあります。

### コミュニティスキルのリポジトリ

コミュニティリポジトリからも既製スキルを入手できます：

- **[Awesome Copilot](https://github.com/github/awesome-copilot)** - スキルのドキュメントと例を含む GitHub Copilot 公式リソース

### コミュニティスキルを手動でインストールする

GitHub リポジトリにスキルを見つけたら、フォルダをスキルディレクトリにコピーしてください：

```bash
# Clone the awesome-copilot repository
git clone https://github.com/github/awesome-copilot.git /tmp/awesome-copilot

# Copy a specific skill to your project
cp -r /tmp/awesome-copilot/skills/code-checklist .github/skills/

# Or for personal use across all projects
cp -r /tmp/awesome-copilot/skills/code-checklist ~/.copilot/skills/
```

> ⚠️ **インストール前に確認**：プロジェクトにコピーする前に、必ずスキルの `SKILL.md` を読んでください。スキルは Copilot の動作を制御するため、悪意のあるスキルが有害なコマンドを実行したり、予期しない形でコードを変更するよう指示する可能性があります。

---

# 練習

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

学んだことを活かして、独自のスキルを作成・テストしましょう。

---

## ▶️ 実際にやってみましょう

### さらにスキルを作成する

同じパターンを持つスキルをさらに2つ紹介します。上記の「はじめてのスキルを作成する」と同様に `mkdir` + `cat` ワークフローを使うか、適切な場所にスキルをコピー&ペーストしてください。その他の例は [.github/skills](../.github/skills) にあります。

### pytest テスト生成スキル

コードベース全体で一貫した pytest 構造を確保するスキルです：

```bash
mkdir -p .github/skills/pytest-gen

cat > .github/skills/pytest-gen/SKILL.md << 'EOF'
---
name: pytest-gen
description: Generate comprehensive pytest tests with fixtures and edge cases
---

# pytest Test Generation

Generate pytest tests that include:

## Test Structure
- Use pytest conventions (test_ prefix)
- One assertion per test when possible
- Clear test names describing expected behavior
- Use fixtures for setup/teardown

## Coverage
- Happy path scenarios
- Edge cases: None, empty strings, empty lists
- Boundary values
- Error scenarios with pytest.raises()

## Fixtures
- Use @pytest.fixture for reusable test data
- Use tmpdir/tmp_path for file operations
- Mock external dependencies with pytest-mock

## Output
Provide complete, runnable test file with proper imports.
EOF
```

### チームの PR レビュースキル

チーム全体で一貫した PR レビュー基準を強制するスキルです：

```bash
mkdir -p .github/skills/pr-review

cat > .github/skills/pr-review/SKILL.md << 'EOF'
---
name: pr-review
description: Team-standard PR review checklist
---

# PR Review

Review code changes against team standards:

## Security Checklist
- [ ] No hardcoded secrets or API keys
- [ ] Input validation on all user data
- [ ] No bare except clauses
- [ ] No sensitive data in logs

## Code Quality
- [ ] Functions under 50 lines
- [ ] No print statements in production code
- [ ] Type hints on public functions
- [ ] Context managers for file I/O
- [ ] No TODOs without issue references

## Testing
- [ ] New code has tests
- [ ] Edge cases covered
- [ ] No skipped tests without explanation

## Documentation
- [ ] API changes documented
- [ ] Breaking changes noted
- [ ] README updated if needed

## Output Format
Provide results as:
- ✅ PASS: Items that look good
- ⚠️ WARN: Items that could be improved
- ❌ FAIL: Items that must be fixed before merge
EOF
```

### さらに挑戦する

1. **スキル作成チャレンジ**：3項目のチェックリストを持つ `quick-review` スキルを作成してください：
   - 裸の except 節
   - 型ヒントの欠如
   - 不明確な変数名

   `"books.py をクイックレビューして"` と聞いてテストしましょう。

2. **スキル比較**：セキュリティレビューの詳細プロンプトを手動で書く時間を計測してください。次に「このファイルのセキュリティ問題を確認して」と聞くだけで security-audit スキルが自動で読み込まれます。スキルでどれくらい時間が節約できましたか？

3. **チームスキルチャレンジ**：チームのコードレビューチェックリストについて考えてみましょう。スキルとしてまとめられますか？スキルが常にチェックすべき3つの項目を書き出してみましょう。

**自己確認**：`description` フィールドが重要な理由（Copilot がスキルを読み込むかどうかを決める仕組み）を説明できたら、スキルを理解できています。

---

## 📝 課題

### メインチャレンジ：ブックサマリースキルを作成する

上記の例では `pytest-gen` と `pr-review` スキルを作成しました。今度はまったく異なる種類のスキルを練習します：データから整形された出力を生成するスキルです。

1. 現在のスキルを一覧表示する：Copilot を起動して `/skills list` を渡します。`ls .github/skills/` でプロジェクトスキル、`ls ~/.copilot/skills/` で個人スキルも確認できます。
2. `.github/skills/book-summary/SKILL.md` に `book-summary` スキルを作成し、ブックコレクションの整形されたマークダウンサマリーを生成できるようにします
3. スキルには以下を含めてください：
   - 明確な name と description（description はマッチングに重要！）
   - 具体的な書式ルール（例：title・author・year・read status を含むマークダウンテーブル）
   - 出力の規則（例：既読ステータスに ✅/❌ を使う、年順に並び替える）
4. スキルをテストする：`@samples/book-app-project/data.json このコレクションの本をまとめて`
5. `/skills list` でスキルが自動でトリガーされることを確認する
6. `/book-summary このコレクションの本をまとめて` で直接呼び出してみる

**成功基準**：ブックコレクションについて質問したときに Copilot が自動で適用する、動作する `book-summary` スキルが完成していること。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**スターターテンプレート**：`.github/skills/book-summary/SKILL.md` を作成してください：

```markdown
---
name: book-summary
description: Generate a formatted markdown summary of a book collection
---

# Book Summary Generator

Generate a summary of the book collection following these rules:

1. Output a markdown table with columns: Title, Author, Year, Status
2. Use ✅ for read books and ❌ for unread books
3. Sort by year (oldest first)
4. Include a total count at the bottom
5. Flag any data issues (missing authors, invalid years)

Example:
| Title | Author | Year | Status |
|-------|--------|------|--------|
| 1984 | George Orwell | 1949 | ✅ |
| Dune | Frank Herbert | 1965 | ❌ |

**Total: 2 books (1 read, 1 unread)**
```

**テスト方法：**
```bash
copilot
> @samples/book-app-project/data.json Summarize the books in this collection
# The skill should auto-trigger based on the description match
```

**トリガーされない場合：** `/skills reload` を実行してからもう一度試してください。

</details>

### ボーナスチャレンジ：コミットメッセージスキル

1. 一貫したフォーマットで conventional commit メッセージを生成する `commit-message` スキルを作成する
2. 変更をステージングして「ステージングした変更のコミットメッセージを生成して」と質問してテストする
3. スキルをドキュメント化して、`copilot-skill` トピックを付けて GitHub に共有する

---

<details>
<summary>🔧 <strong>よくあるミスとトラブルシューティング</strong>（クリックして展開）</summary>

### よくあるミス

| ミス | 何が起きるか | 解決策 |
|---------|--------------|-----|
| `SKILL.md` 以外のファイル名を使う | スキルが認識されない | ファイル名は必ず `SKILL.md` にする |
| `description` フィールドが曖昧 | スキルが自動で読み込まれない | description はPRIMARYの検出メカニズム。具体的なトリガーワードを使う |
| フロントマターに `name` または `description` がない | スキルの読み込みに失敗する | YAML フロントマターに両フィールドを追加する |
| フォルダの場所が違う | スキルが見つからない | `.github/skills/skill-name/`（プロジェクト）または `~/.copilot/skills/skill-name/`（個人）を使う |

### トラブルシューティング

**スキルが使われない** - 想定どおりにスキルが使われない場合：

1. **description を確認する**：質問の仕方と合致しているか？
   ```markdown
   # NG：曖昧すぎる
   description: Reviews code

   # OK：トリガーワードが含まれている
   description: Use for code reviews, checking code quality,
     finding bugs, security issues, and best practice violations
   ```

2. **ファイルの場所を確認する**：
   ```bash
   # プロジェクトスキル
   ls .github/skills/

   # ユーザースキル
   ls ~/.copilot/skills/
   ```

3. **SKILL.md のフォーマットを確認する**：フロントマターは必須です：
   ```markdown
   ---
   name: skill-name
   description: What the skill does and when to use it
   ---

   # Instructions here
   ```

**スキルが表示されない** - フォルダ構造を確認してください：
```
.github/skills/
└── my-skill/           # フォルダ名
    └── SKILL.md        # 必ず SKILL.md（大文字小文字を区別）
```

スキルを作成・編集した後は `/skills reload` を実行して変更を確実に反映させましょう。

**スキルが読み込まれるかテストする** - Copilot に直接聞いてみてください：
```bash
> コード品質チェックに使えるスキルはありますか？
# Copilot が見つけた関連スキルを説明します
```

**スキルが実際に機能しているか確認する方法**

1. **出力フォーマットを確認する**：スキルが出力フォーマット（`[CRITICAL]` タグなど）を指定している場合、レスポンスにそれが含まれているか確認する
2. **直接聞く**：レスポンスを受け取った後、「そのレスポンスにスキルを使いましたか？」と聞く
3. **比較する**：`--no-custom-instructions` オプションで同じプロンプトを試して違いを確認する：
   ```bash
   # スキルあり
   copilot --allow-all -p "Review @file.py for security issues"

   # スキルなし（ベースライン比較）
   copilot --allow-all -p "Review @file.py for security issues" --no-custom-instructions
   ```
4. **特定のチェックを確認する**：スキルに特定のチェック（「50行を超える関数」など）が含まれている場合、出力にそれが表示されているか確認する

</details>

---

# まとめ

## 🔑 重要なポイント

1. **スキルは自動**：プロンプトがスキルの description に合致したとき Copilot が読み込む
2. **直接呼び出し**：`/スキル名` のスラッシュコマンドでスキルを直接呼び出すこともできる
3. **SKILL.md のフォーマット**：YAML フロントマター（name・description・任意の license）＋マークダウン形式の指示書
4. **場所が重要**：`.github/skills/` はプロジェクト/チーム共有、`~/.copilot/skills/` は個人用
5. **description が鍵**：自然な質問の仕方に合ったキーワードで description を書く

> 📋 **クイックリファレンス**：コマンドとショートカットの完全なリストは [GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference) を参照してください。

---

## ➡️ 次のステップ

スキルは自動読み込み指示書で Copilot の機能を拡張します。では、外部サービスへの接続はどうでしょう？そこで MCP の出番です。

**[第6章：MCP サーバー](../06-mcp-servers/README.md)** では以下を学びます：

- MCP（Model Context Protocol）とは何か
- GitHub・ファイルシステム・ドキュメントサービスへの接続
- MCP サーバーの設定方法
- マルチサーバーワークフロー

---

**[← Back to Chapter 04](../04-agents-custom-instructions/README.md)** | **[Continue to Chapter 06 →](../06-mcp-servers/README.md)**
