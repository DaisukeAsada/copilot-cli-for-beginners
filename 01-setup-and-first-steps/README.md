![Chapter 01: First Steps](images/chapter-header.png)

> **AIがバグを瞬時に発見し、わかりにくいコードを説明し、動くスクリプトを生成する様子を見てみましょう。そして GitHub Copilot CLI の3つの使い方を学びます。**

この章から本番が始まります！開発者たちが GitHub Copilot CLI を「シニアエンジニアをいつでも呼び出せる存在」と表現する理由を、実際に体験してもらいます。AIがセキュリティバグを数秒で発見し、複雑なコードをわかりやすく説明し、動くスクリプトを即座に生成する様子を目の当たりにします。そして3つのインタラクションモード（Interactive、Plan、Programmatic）を習得し、どの場面でどのモードを使えばよいかを把握できるようになります。

> ⚠️ **前提条件**: 事前に **[Chapter 00: Quick Start](../00-quick-start/README.md)** を完了してください。以下のデモを実行する前に、GitHub Copilot CLI のインストールと認証が必要です。

## 🎯 学習目標

この章を終えると、次のことができるようになります：

- ハンズオンデモを通じて GitHub Copilot CLI が生産性にもたらす効果を体験する
- タスクに応じて適切なモード（Interactive、Plan、Programmatic）を選択する
- スラッシュコマンドを使ってセッションを操作する

> ⏱️ **所要時間の目安**: 約45分（読む：15分 + ハンズオン：30分）

---

# はじめての Copilot CLI 体験

<img src="images/first-copilot-experience.png" alt="Developer sitting at a desk with code on the monitor and glowing particles representing AI assistance" width="800"/>

さっそく試して、Copilot CLI が何をできるか見てみましょう。

---

## まず使ってみる：はじめてのプロンプト

印象的なデモに入る前に、今すぐ試せるシンプルなプロンプトから始めましょう。**コードリポジトリは不要です！** ターミナルを開いて Copilot CLI を起動してください：

```bash
copilot
```

初心者向けのプロンプトをいくつか試してみましょう：

```
> Explain what a dataclass is in Python in simple terms

> Write a function that sorts a list of dictionaries by a specific key

> What's the difference between a list and a tuple in Python?

> Give me 5 best practices for writing clean Python code
```

Python を使っていなくても大丈夫！お好みの言語で質問してください。

自然に会話できる感覚に気づくはずです。同僚に話しかけるように、普通に質問するだけでいいのです。探索が終わったら `/exit` と入力してセッションを終了してください。

**重要なポイント**: GitHub Copilot CLI は会話形式です。特別な構文は必要ありません。普通の言葉で質問するだけです。

## 実際に動かしてみよう

では、なぜ開発者たちが「シニアエンジニアをいつでも呼び出せる感覚」と表現するのか、実際に見ていきましょう。

> 📖 **例の見方**: `>` で始まる行は、Copilot CLI のインタラクティブセッション内で入力するプロンプトです。`>` がない行は、ターミナルで実行するシェルコマンドです。

> 💡 **サンプル出力について**: このコースで示すサンプル出力はあくまで例示です。Copilot CLI のレスポンスは毎回異なるため、あなたの結果は文言・書式・詳細度が異なります。正確なテキストではなく、*返ってくる情報の種類*に注目してください。

### デモ1：数秒でコードレビュー

このコースには、意図的にコード品質の問題を含むサンプルファイルが含まれています。ローカル環境で作業していてまだリポジトリをクローンしていない場合は、以下の `git clone` コマンドを実行し、`copilot-cli-for-beginners` フォルダに移動してから `copilot` コマンドを実行してください。

```bash
# ローカルで作業していてまだクローンしていない場合はリポジトリをクローン
git clone https://github.com/github/copilot-cli-for-beginners
cd copilot-cli-for-beginners

# Copilot を起動
copilot
```

Copilot CLI のインタラクティブセッションに入ったら、次を実行してください：

```
> Review @samples/book-app-project/book_app.py for code quality issues and suggest improvements
```

> 💡 **`@` 記号は何のためにあるの？** `@` 記号は Copilot CLI にファイルを読むよう伝えます。詳しくは Chapter 02 で学びます。今はそのままコマンドをコピーして使ってください。

---

<details>
<summary>🎬 実際の動作を見てみよう！</summary>

![Code Review Demo](images/code-review-demo.gif)

*デモの出力は毎回異なります。使用するモデルやツール、レスポンスの内容は表示例と異なる場合があります。*

</details>

---

**まとめ**: プロフェッショナルなコードレビューが数秒で完了します。手動レビューなら……もっと時間がかかりますよね！

---

### デモ2：わかりにくいコードを説明させる

コードを見ても何をしているのかわからない、そんな経験はありませんか？Copilot CLI セッションで試してみましょう：

```
> Explain what @samples/book-app-project/books.py does in simple terms
```

---

<details>
<summary>🎬 実際の動作を見てみよう！</summary>

![Explain Code Demo](images/explain-code-demo.gif)

*デモの出力は毎回異なります。使用するモデルやツール、レスポンスの内容は表示例と異なる場合があります。*

</details>

---

**何が起こるか**：（あなたの出力は異なります）Copilot CLI がファイルを読み込み、コードを理解して、わかりやすい言葉で説明してくれます。

```
This is a book collection management module using Python dataclasses.

Think of it like a digital bookshelf:
- Book is a dataclass - a simple way to store book information (title, author, year, read status)
- BookCollection manages the entire collection and handles saving/loading

Key components:

1. @dataclass decorator (line 8)
   - Automatically creates __init__, __repr__, etc.
   - Clean way to define data structures in Python

2. BookCollection class (line 16)
   - Maintains a list of Book objects
   - Handles persistence with JSON file I/O
   - load_books() reads from data.json
   - save_books() writes to data.json using asdict()

3. Book operations:
   - add_book() - creates and saves new books
   - find_book_by_title() - searches collection
   - mark_as_read() - updates read status
   - find_by_author() - filters by author name

Common pattern: Read from JSON → Work with Python objects → Write back to JSON
```

**まとめ**: 複雑なコードを、忍耐強いメンターのように説明してもらえます。

---

### デモ3：動くコードを生成する

本来なら15分かけてググるような関数も、セッション内でそのまま頼めます：

```
> Write a Python function that takes a list of books and returns statistics: 
  total count, number read, number unread, oldest and newest book
```

---

<details>
<summary>🎬 実際の動作を見てみよう！</summary>

![Generate Code Demo](images/generate-code-demo.gif)

*デモの出力は毎回異なります。使用するモデルやツール、レスポンスの内容は表示例と異なる場合があります。*

</details>

---

**何が起こるか**: コピーしてすぐに動かせる完成した関数が、数秒で生成されます。

探索が終わったらセッションを終了してください：

```
> /exit
```

**まとめ**: 即座に結果が得られ、しかもずっと同じセッションで作業を続けられます。

---

# モードとコマンド

<img src="images/modes-and-commands.png" alt="Futuristic control panel with glowing screens, dials, and equalizers representing Copilot CLI modes and commands" width="800"/>

Copilot CLI でできることを見てきました。次は、これらの機能を*効果的に使う方法*を理解しましょう。カギとなるのは、状況に応じて3つのインタラクションモードを使い分けることです。

> 💡 **注意**: Copilot CLI には **Autopilot** モードもあります。このモードでは入力を待たずにタスクを進めていきます。強力なモードですが、フルの権限付与が必要で、プレミアムリクエストを自律的に消費します。このコースでは以下の3つのモードに集中します。基本に慣れたら Autopilot も紹介します。

---

## 🧩 現実世界のたとえ：外食する

GitHub Copilot CLI の使い方は、外食に例えると理解しやすくなります。お店に行くことを決めてから注文するまで、状況に応じてアプローチが変わるように：

| モード | 外食のたとえ | 使うとき |
|--------|------------|---------|
| **Plan** | レストランへのGPSルート | 複雑なタスク - ルートを確認し、立ち寄り場所をチェックし、計画を合意してから出発 |
| **Interactive** | ウェイターとの会話 | 探索・反復 - 質問し、カスタマイズし、リアルタイムでフィードバックをもらう |
| **Programmatic** | ドライブスルーでの注文 | 素早く具体的なタスク - 作業環境にとどまりながら、すぐに結果を得る |

外食と同様、それぞれのアプローチをいつ使えばよいか、自然と感覚でわかるようになります。

<img src="images/ordering-food-analogy.png" alt="Three Ways to Use GitHub Copilot CLI - Plan Mode (GPS route to restaurant), Interactive Mode (talking to waiter), Programmatic Mode (drive-through)" width="800"/>

*タスクに応じてモードを選ぶ：Plan はまず計画を立てるとき、Interactive は対話的なやり取りが必要なとき、Programmatic はすぐに一回限りの結果が欲しいとき*

### どのモードから始めればいい？

**Interactive モードから始めてください。**
- 試行錯誤しながら追加質問ができる
- 会話を通じて自然にコンテキストが積み上がっていく
- `/clear` でかんたんにやり直せる

慣れてきたら試してみましょう：
- **Programmatic モード** (`copilot -p "<プロンプト>"`)：素早い一回限りの質問に
- **Plan モード** (`/plan`)：コーディング前に詳しく計画を立てたいときに

---

## 3つのモード

### モード1：Interactive モード（最初はここから）

<img src="images/interactive-mode.png" alt="Interactive Mode - Like talking to a waiter who can answer questions and adjust the order" width="250"/>

**最適な用途**: 探索・反復・複数ターンの会話。質問に答えながら、フィードバックを受けて注文をその場で調整できるウェイターとの会話のようなものです。

インタラクティブセッションを開始する：

```bash
copilot
```

ここまで見てきたように、自然に入力できるプロンプトが表示されます。使えるコマンドを確認するには、次のように入力してください：

```
> /help
```

**重要なポイント**: Interactive モードはコンテキストを維持します。各メッセージが前の内容を引き継ぐため、本当の会話のように続けられます。

#### Interactive モードの例

```bash
copilot

> Review @samples/book-app-project/utils.py and suggest improvements

> Add type hints to all functions

> Make the error handling more robust

> /exit
```

各プロンプトが前の回答を踏まえて積み重なっていることに注目してください。毎回ゼロから始めるのではなく、会話として続いています。

---

### モード2：Plan モード

<img src="images/plan-mode.png" alt="Plan Mode - Like planning a route before a trip using GPS" width="250"/>

**最適な用途**: 実行前にアプローチを確認したい複雑なタスク。GPSで旅行前にルートを計画するのと似ています。

Plan モードは、コードを書く前にステップバイステップの計画を立てるのに役立ちます。`/plan` コマンドを使うか、**Shift+Tab** を押して Plan モードに切り替えてください：

> 💡 **ヒント**: **Shift+Tab** はモードを循環させます：Interactive → Plan → Autopilot。インタラクティブセッション中にいつでも押してモードを切り替えられます。

```bash
copilot

> /plan Add a "mark as read" command to the book app
```

**Plan モードの出力例：** （実際の出力は異なります）

```
📋 実装計画

ステップ1: book_app.py のコマンドハンドラーを更新
  - "mark" コマンド用の elif ブランチを追加
  - handle_mark_as_read() 関数を作成

ステップ2: ハンドラー関数を実装
  - ユーザーに本のタイトルを入力させる
  - collection.mark_as_read(title) を呼び出す
  - 成功/失敗メッセージを表示

ステップ3: ヘルプテキストを更新
  - 利用可能なコマンド一覧に "mark" を追加
  - コマンドの使い方を説明

ステップ4: フローをテスト
  - 本を追加する
  - 既読としてマークする
  - リスト出力で状態が変わったことを確認する

実装を進めますか？[Y/n]
```

**重要なポイント**: Plan モードでは、コードを書く前にアプローチを確認・修正できます。計画が完成したら、後で参照できるようにファイルに保存するよう Copilot CLI に頼むこともできます。たとえば「この計画を `mark_as_read_plan.md` に保存して」と言えば、計画の詳細が書かれた Markdown ファイルが作成されます。

> 💡 **もっと複雑なものを試したい？** `/plan Add search and filter capabilities to the book app` を試してみましょう。Plan モードはシンプルな機能からフルアプリケーションまでスケールします。

> 📚 **Autopilot モード**: Shift+Tab が **Autopilot** という3つ目のモードを循環することに気づいたかもしれません。Autopilot モードでは、各ステップの入力を待たずに計画全体を進めていきます。タスクを同僚に渡して「終わったら教えて」と言うようなイメージです。一般的なワークフローは「計画を立てる → 承認する → Autopilot」で、まず計画を上手に書けるようになる必要があります。Interactive モードと Plan モードに慣れてから、準備ができたら[公式ドキュメント](https://docs.github.com/copilot/concepts/agents/copilot-cli/autopilot)を参照してください。

---

### モード3：Programmatic モード

<img src="images/programmatic-mode.png" alt="Programmatic Mode - Like using a drive-through for a quick order" width="250"/>

**最適な用途**: 自動化・スクリプト・CI/CD・一回限りのコマンド。ウェイターと話す必要なく手早く注文できるドライブスルーのようなものです。

対話不要の一回限りのコマンドには `-p` フラグを使います：

```bash
# コードを生成する
copilot -p "Write a function that checks if a number is even or odd"

# 素早いヘルプを得る
copilot -p "How do I read a JSON file in Python?"
```

**重要なポイント**: Programmatic モードはすぐに答えを返して終了します。会話はなく、入力→出力のみです。

<details>
<summary>📚 <strong>さらに深く：スクリプトでの Programmatic モード</strong>（クリックして展開）</summary>

慣れてきたら、シェルスクリプト内で `-p` を使えます：

```bash
#!/bin/bash

# コミットメッセージを自動生成する
COMMIT_MSG=$(copilot -p "Generate a commit message for: $(git diff --staged)")
git commit -m "$COMMIT_MSG"

# ファイルをレビューする
copilot --allow-all -p "Review @myfile.py for issues"
```
> ⚠️ **`--allow-all` について**: このフラグはすべての権限確認をスキップし、Copilot CLI がファイルの読み取り、コマンドの実行、URL へのアクセスを確認なしで行えるようにします。これは Programmatic モード（`-p`）で必要です。インタラクティブセッションがないため、アクションを承認できないからです。自分で書いたプロンプトに対してのみ、かつ信頼できるディレクトリでのみ `--allow-all` を使ってください。信頼できない入力や機密性の高いディレクトリでは絶対に使用しないでください。

</details>

---

## 必須スラッシュコマンド

これらのコマンドは Interactive モードで使えます。**まずはこの6つだけ覚えれば**、日常の90%のケースに対応できます：

| コマンド | 内容 | 使うとき |
|---------|------|---------|
| `/clear` | 会話をクリアして最初から始める | 話題を変えたいとき |
| `/help` | 利用可能なコマンドを一覧表示する | コマンドを忘れたとき |
| `/model` | AIモデルを確認または切り替える | AIモデルを変更したいとき |
| `/plan` | コーディング前に作業を計画する | より複雑な機能のとき |
| `/research` | GitHubとWeb情報源を使った深い調査 | コーディング前にトピックを調べたいとき |
| `/exit` | セッションを終了する | 作業が終わったとき |

はじめの一歩はここまでです！慣れてきたら追加コマンドも探索してみましょう。

> 📚 **公式ドキュメント**: [CLI コマンドリファレンス](https://docs.github.com/copilot/reference/cli-command-reference)でコマンドとフラグの完全な一覧が確認できます。

<details>
<summary>📚 <strong>追加コマンド</strong>（クリックして展開）</summary>

> 💡 上記の必須コマンドだけで日常的な使い方の多くをカバーできます。もっと詳しく探索する準備ができたときのためにここに参照情報を載せています。

### エージェント環境

| コマンド | 内容 |
|---------|------|
| `/agent` | 利用可能なエージェントを閲覧・選択する |
| `/init` | リポジトリ用の Copilot 指示を初期化する |
| `/mcp` | MCP サーバーの設定を管理する |
| `/skills` | 拡張機能のためのスキルを管理する |

> 💡 エージェントは [Chapter 04](../04-agents-custom-instructions/README.md)、スキルは [Chapter 05](../05-skills/README.md)、MCP サーバーは [Chapter 06](../06-mcp-servers/README.md) で解説します。

### モデルとサブエージェント

| コマンド | 内容 |
|---------|------|
| `/delegate` | タスクを GitHub Copilot クラウドエージェントに引き継ぐ |
| `/fleet` | 複雑なタスクを並列サブタスクに分割して高速化する |
| `/model` | AIモデルを確認または切り替える |
| `/tasks` | バックグラウンドのサブエージェントと切り離されたシェルセッションを表示する |

### コード

| コマンド | 内容 |
|---------|------|
| `/diff` | 現在のディレクトリで行われた変更をレビューする |
| `/pr` | 現在のブランチのプルリクエストを操作する |
| `/research` | GitHubとWebを使って深い調査を行う |
| `/review` | コードレビューエージェントを実行して変更を分析する |
| `/terminal-setup` | マルチライン入力サポートを有効にする（shift+enter / ctrl+enter） |

### 権限

| コマンド | 内容 |
|---------|------|
| `/add-dir <directory>` | ディレクトリを許可リストに追加する |
| `/allow-all [on\|off\|show]` | すべての権限確認を自動承認する。`on` で有効化、`off` で無効化、`show` で現在の状態を確認 |
| `/cwd`, `/cd [directory]` | 作業ディレクトリを確認または変更する |
| `/list-dirs` | 許可されているすべてのディレクトリを表示する |

> ⚠️ **注意して使う**: `/allow-all` は確認プロンプトをスキップします。信頼できるプロジェクトでは便利ですが、信頼できないコードには注意してください。

### セッション

| コマンド | 内容 |
|---------|------|
| `/clear` | 現在のセッションを破棄し（履歴は保存されない）、新しい会話を開始する |
| `/compact` | コンテキスト使用量を減らすために会話を要約する |
| `/context` | コンテキストウィンドウのトークン使用量を可視化して表示する |
| `/new` | 現在のセッションを終了し（検索・再開のために履歴に保存）、新しい会話を開始する |
| `/resume` | 別のセッションに切り替える（セッションIDを指定することもできる） |
| `/rename` | 現在のセッションの名前を変更する（省略するとAIが自動生成） |
| `/rewind` | タイムラインピッカーを開いて、会話の以前の時点に戻る |
| `/usage` | セッションの使用量メトリクスと統計を表示する |
| `/session` | セッション情報とワークスペースのサマリーを表示する |
| `/share` | セッションをMarkdownファイル、GitHub Gist、または独立したHTMLファイルとしてエクスポートする |

### ヘルプとフィードバック

| コマンド | 内容 |
|---------|------|
| `/changelog` | CLIバージョンの変更履歴を表示する |
| `/feedback` | GitHubにフィードバックを送信する |
| `/help` | 利用可能なすべてのコマンドを表示する |
| `/theme` | ターミナルのテーマを確認または設定する |

### クイックシェルコマンド

`!` を先頭につけるとAIを経由せずにシェルコマンドを直接実行できます：

```bash
copilot

> !git status
# AI を使わず git status を直接実行する

> !python -m pytest tests/
# pytest を直接実行する
```

### モデルの切り替え

Copilot CLI は OpenAI、Anthropic、Google などの複数のAIモデルに対応しています。利用できるモデルはサブスクリプションのレベルや地域によって異なります。`/model` を使って選択肢を確認し、切り替えることができます：

```bash
copilot
> /model

# 利用可能なモデルが表示され、選択できます。Sonnet 4.5 を選びましょう。
```

> 💡 **ヒント**: モデルによって消費する「プレミアムリクエスト」の量が異なります。**1x** と表示されているモデル（Claude Sonnet 4.5 など）はデフォルトとして最適です。高性能で効率的です。倍率の高いモデルはプレミアムリクエストクォータをより早く消費するため、本当に必要なときのためにとっておきましょう。

</details>

---

# 練習

<img src="../images/practice.png" alt="Warm desk setup with monitor showing code, lamp, coffee cup, and headphones ready for hands-on practice" width="800"/>

学んだことを実際に動かしてみましょう。

---

## ▶️ 自分で試してみよう

### インタラクティブな探索

Copilot を起動して、フォローアッププロンプトを使って book app を少しずつ改善していきましょう：

```bash
copilot

> Review @samples/book-app-project/book_app.py - what could be improved?

> Refactor the if/elif chain into a more maintainable structure

> Add type hints to all the handler functions

> /exit
```

### 機能を計画する

コードを書く前に `/plan` を使って Copilot CLI に実装を整理させましょう：

```bash
copilot

> /plan Add a search feature to the book app that can find books by title or author

# 計画を確認する
# 承認または修正する
# ステップバイステップで実装されるのを見る
```

### Programmatic モードで自動化する

`-p` フラグを使うと、Interactive モードに入らずターミナルから直接 Copilot CLI を実行できます。リポジトリのルートから、次のスクリプトをターミナル（Copilot の中ではなく）にコピー＆ペーストして、book app のすべての Python ファイルをレビューしましょう。

```bash
# book app のすべての Python ファイルをレビューする
for file in samples/book-app-project/*.py; do
  echo "Reviewing $file..."
  copilot --allow-all -p "Quick code quality review of @$file - critical issues only"
done
```

**PowerShell (Windows):**

```powershell
# book app のすべての Python ファイルをレビューする
Get-ChildItem samples/book-app-project/*.py | ForEach-Object {
  $relativePath = "samples/book-app-project/$($_.Name)";
  Write-Host "Reviewing $relativePath...";
  copilot --allow-all -p "Quick code quality review of @$relativePath - critical issues only" 
}
```

---

デモを完了したら、次のバリエーションも試してみましょう：

1. **インタラクティブチャレンジ**: `copilot` を起動して book app を探索する。`@samples/book-app-project/books.py` について質問し、改善を3回続けてリクエストしてみましょう。

2. **Plan モードチャレンジ**: `/plan Add rating and review features to the book app` を実行する。計画をよく読んでみましょう。意味はありますか？

3. **Programmatic チャレンジ**: `copilot --allow-all -p "List all functions in @samples/book-app-project/book_app.py and describe what each does"` を実行する。一発で成功しましたか？

---

## 📝 課題

### メインチャレンジ：Book App のユーティリティを改善する

ハンズオンの例では `book_app.py` のレビューとリファクタリングに取り組みました。今度は別のファイル `utils.py` で同じスキルを練習しましょう：

1. インタラクティブセッションを開始する: `copilot`
2. Copilot CLI にファイルを要約させる: `@samples/book-app-project/utils.py What does each function in this file do?`
3. 入力バリデーションの追加を依頼する: "Add validation to `get_user_choice()` so it handles empty input and non-numeric entries"
4. エラーハンドリングの改善を依頼する: "What happens if `get_book_details()` receives an empty string for the title? Add guards for that."
5. docstring の追加を依頼する: "Add a comprehensive docstring to `get_book_details()` with parameter descriptions and return values"
6. プロンプト間でコンテキストがどう引き継がれるかを観察する。各改善が前の内容の上に積み重なっていく
7. `/exit` で終了する

**成功基準**: 入力バリデーション・エラーハンドリング・docstring が追加された改善版の `utils.py` が、複数ターンの会話を通じて完成していること。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**試してみるサンプルプロンプト:**
```bash
> @samples/book-app-project/utils.py What does each function in this file do?
> Add validation to get_user_choice() so it handles empty input and non-numeric entries
> What happens if get_book_details() receives an empty string for the title? Add guards for that.
> Add a comprehensive docstring to get_book_details() with parameter descriptions and return values
```

**よくある問題:**
- Copilot CLI が確認質問をしてきたら、自然に答えれば大丈夫
- コンテキストは引き継がれるので、各プロンプトは前の内容の上に積み重なる
- やり直したい場合は `/clear` を使う

</details>

### ボーナスチャレンジ：モードを比較する

例では検索機能に `/plan`、一括レビューに `-p` を使いました。今度は1つの新しいタスクで3つのモードをすべて試してみましょう。`BookCollection` クラスに `list_by_year()` メソッドを追加します：

1. **Interactive**: `copilot` → メソッドを設計・構築するよう段階的に依頼する
2. **Plan**: `/plan Add a list_by_year(start, end) method to BookCollection that filters books by publication year range`
3. **Programmatic**: `copilot --allow-all -p "@samples/book-app-project/books.py Add a list_by_year(start, end) method that returns books published between start and end year inclusive"`

**振り返り**: どのモードが一番自然に感じましたか？それぞれをどんなときに使いますか？

---

<details>
<summary>🔧 <strong>よくある間違いとトラブルシューティング</strong>（クリックして展開）</summary>

### よくある間違い

| 間違い | 何が起きるか | 対処法 |
|--------|------------|--------|
| `/exit` の代わりに `exit` と入力する | Copilot CLI が "exit" をコマンドではなくプロンプトとして扱う | スラッシュコマンドは必ず `/` で始める |
| 複数ターンの会話に `-p` を使う | 各 `-p` の呼び出しは独立しており、以前の呼び出しを記憶しない | コンテキストを積み上げる会話には Interactive モード（`copilot`）を使う |
| `$` や `!` を含むプロンプトを引用符で囲まない | Copilot CLI が見る前にシェルが特殊文字を解釈してしまう | プロンプトを引用符で囲む: `copilot -p "What does $HOME mean?"` |

### トラブルシューティング

**"Model not available"** - お使いのサブスクリプションではすべてのモデルが利用できない場合があります。`/model` で利用可能なモデルを確認してください。

**"Context too long"** - 会話でコンテキストウィンドウ全体を使い切っています。`/clear` でリセットするか、新しいセッションを開始してください。

**"Rate limit exceeded"** - 数分待ってから再試行してください。バッチ処理には Programmatic モードを使い、間に遅延を入れることを検討してください。

</details>

---

# まとめ

## 🔑 重要なポイント

1. **Interactive モード**は探索と反復のためのモードです。コンテキストが引き継がれます。それまでに話したことを覚えている相手との会話のようなものです。
2. **Plan モード**は通常、より複雑なタスクのためのモードです。実装前に計画を確認しましょう。
3. **Programmatic モード**は自動化のためのモードです。対話は必要ありません。
4. **必須コマンド**（`/help`、`/clear`、`/plan`、`/research`、`/model`、`/exit`）で日常のほとんどに対応できます。

> 📋 **クイックリファレンス**: コマンドとショートカットの完全な一覧は [GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference) を参照してください。

---

## ➡️ 次のステップ

3つのモードを理解したところで、次は Copilot CLI にコードのコンテキストを与える方法を学びましょう。

**[Chapter 02: Context and Conversations](../02-context-conversations/README.md)** では以下を学びます：

- ファイルやディレクトリを参照するための `@` 構文
- `--resume` と `--continue` を使ったセッション管理
- コンテキスト管理が Copilot CLI を真に強力にする仕組み

---

**[← コースホームに戻る](../README.md)** | **[Chapter 02 に進む →](../02-context-conversations/README.md)**
