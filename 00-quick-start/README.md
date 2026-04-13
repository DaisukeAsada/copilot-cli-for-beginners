![Chapter 00: Quick Start](images/chapter-header.png)

ようこそ！この章では、GitHub Copilot CLI (Command Line Interface) のインストール、GitHubアカウントでのサインイン、そして動作確認を行います。セットアップのための章です。準備が整ったら、Chapter 01 からいよいよ本番のデモが始まります！

## 🎯 学習目標

この章を終えると、以下が完了しています：

- GitHub Copilot CLI のインストール
- GitHub アカウントでのサインイン
- 簡単なテストによる動作確認

> ⏱️ **所要時間の目安**：約10分（読む：5分 + 実践：5分）

---

## ✅ 前提条件

- **Copilot アクセス付きの GitHub アカウント**。[サブスクリプションオプションを見る](https://github.com/features/copilot/plans)。学生・教員の方は [GitHub Education](https://education.github.com/pack) を通じて Copilot Pro を無料で利用できます。
- **ターミナルの基本操作**：`cd` や `ls` などのコマンドに慣れていること

### 「Copilot アクセス」とは

GitHub Copilot CLI を使用するには、有効な Copilot サブスクリプションが必要です。[github.com/settings/copilot](https://github.com/settings/copilot) でご自身のステータスを確認できます。次のいずれかが表示されるはずです：

- **Copilot Individual** - 個人サブスクリプション
- **Copilot Business** - 組織経由
- **Copilot Enterprise** - エンタープライズ経由
- **GitHub Education** - 認定学生・教員向け無料プラン

「You don't have access to GitHub Copilot」と表示された場合は、無料オプションの利用、プランへの加入、またはアクセスを提供している組織への参加が必要です。

---

## インストール

> ⏱️ **時間の目安**：インストールに2〜5分、認証にさらに1〜2分かかります。

### GitHub Codespaces（セットアップ不要）

前提条件をインストールしたくない場合は GitHub Codespaces を使用できます。GitHub Copilot CLI がすぐに使える状態で用意されており（サインインは必要）、Python と pytest もプリインストールされています。

1. このリポジトリを [フォーク](https://github.com/github/copilot-cli-for-beginners/fork) して自分の GitHub アカウントに追加する
2. **Code** > **Codespaces** > **Create codespace on main** を選択
3. コンテナのビルドが完了するまで数分待つ
4. 準備完了！Codespace 環境でターミナルが自動的に開きます。

> 💡 **Codespace での確認**：`cd samples/book-app-project && python book_app.py help` を実行して、Python とサンプルアプリが正常に動作することを確認しましょう。

### ローカルへのインストール

ローカルマシンで Copilot CLI とコースのサンプルを実行したい場合は、以下の手順に従ってください。

1. リポジトリをクローンして、コースのサンプルをマシンに取得する：

    ```bash
    git clone https://github.com/github/copilot-cli-for-beginners
    cd copilot-cli-for-beginners
    ```

2. 以下のいずれかの方法で Copilot CLI をインストールする。

    > 💡 **どれを選べばいい？** Node.js がインストール済みなら `npm` を使うのが手軽です。それ以外は、ご利用のシステムに合ったオプションを選んでください。

    ### 全プラットフォーム (npm)

    ```bash
    # Node.js がインストールされていれば、これが手っ取り早い方法です
    npm install -g @github/copilot
    ```

    ### macOS/Linux (Homebrew)

    ```bash
    brew install copilot-cli
    ```

    ### Windows (WinGet)

    ```bash
    winget install GitHub.Copilot
    ```

    ### macOS/Linux (インストールスクリプト)

    ```bash
    curl -fsSL https://gh.io/copilot-install | bash
    ```

---

## 認証

`copilot-cli-for-beginners` リポジトリのルートでターミナルを開き、CLI を起動してフォルダへのアクセスを許可します。

```bash
copilot
```

リポジトリを含むフォルダを信頼するかどうか確認が求められます（まだ信頼していない場合）。今回のみ信頼するか、今後のセッションでも継続して信頼するかを選択できます。

<img src="images/copilot-trust.png" alt="Trusting files in a folder with the Copilot CLI" width="800"/>

フォルダを信頼した後、GitHub アカウントでサインインできます。

```
> /login
```

**次に起こること：**

1. Copilot CLI にワンタイムコード（例：`ABCD-1234`）が表示される
2. GitHub のデバイス認証ページがブラウザで開く。まだサインインしていない場合は GitHub にサインインする
3. 表示されたコードを入力する
4. 「Authorize」を選択して GitHub Copilot CLI へのアクセスを許可する
5. ターミナルに戻ると、サインイン完了！

<img src="images/auth-device-flow.png" alt="Device Authorization Flow - showing the 5-step process from terminal login to signed-in confirmation" width="800"/>

*デバイス認証フロー：ターミナルでコードを生成し、ブラウザで確認すると、Copilot CLI の認証が完了します。*

**ヒント**：サインイン状態はセッションをまたいで維持されます。トークンが期限切れになるか明示的にサインアウトしない限り、再認証は不要です。

---

## 動作確認

### ステップ 1：Copilot CLI をテストする

サインインできたら、Copilot CLI が正常に動作しているか確認しましょう。まだ起動していない場合はターミナルで CLI を起動し、次のように入力してみてください：

```bash
> Say hello and tell me what you can help with
```

応答を受け取ったら、CLI を終了できます：

```bash
> /exit
```

---

<details>
<summary>🎬 実際の動作を見てみよう！</summary>

![Hello Demo](images/hello-demo.gif)

*デモの出力は環境によって異なります。使用するモデル、ツール、応答内容はここに示されたものと異なる場合があります。*

</details>

---

**期待される出力**：Copilot CLI の機能を紹介するフレンドリーな応答。

### ステップ 2：サンプルのBook Appを実行する

このコースには、CLI を使って探索・改善していくサンプルアプリが用意されています *(コードは /samples/book-app-project にあります)*。始める前に *Python 製の本コレクション管理ターミナルアプリ* が正常に動作することを確認しておきましょう。システムに応じて `python` または `python3` を使用してください。

> **注意：** コース全体で主に使用するのは Python 版（`samples/book-app-project`）です。ローカルマシンを選んだ場合は [Python 3.10+](https://www.python.org/downloads/) が必要です（Codespace にはすでにインストール済み）。JavaScript 版（`samples/book-app-project-js`）と C# 版（`samples/book-app-project-cs`）も用意されているので、好みの言語を選んでください。各サンプルにはその言語でのアプリ実行手順を記載した README があります。

```bash
cd samples/book-app-project
python book_app.py list
```

**期待される出力**：「The Hobbit」「1984」「Dune」などを含む5冊の本のリスト。

### ステップ 3：Book App で Copilot CLI を試す

ステップ 2 を実行した場合は、まずリポジトリのルートに戻ります：

```bash
cd ../..   # 必要に応じてリポジトリのルートに戻る
copilot 
> What does @samples/book-app-project/book_app.py do?
```

**期待される出力**：Book App の主要な機能とコマンドの概要。

エラーが表示された場合は、下の[トラブルシューティング](#トラブルシューティング)を確認してください。

完了したら Copilot CLI を終了できます：

```bash
> /exit
```

---

## ✅ 準備完了！

インストールはここまでです。Chapter 01 からいよいよ本番が始まります：

- AI が Book App をレビューし、コード品質の問題を即座に発見する様子を見る
- Copilot CLI の3つの使い方を学ぶ
- 平易な日本語（自然言語）から動くコードを生成する

**[Chapter 01: First Steps へ進む →](../01-setup-and-first-steps/README.md)**

---

## トラブルシューティング

### "copilot: command not found"

CLI がインストールされていません。別のインストール方法を試してみてください：

```bash
# brew が失敗した場合は npm を試す：
npm install -g @github/copilot

# またはインストールスクリプト：
curl -fsSL https://gh.io/copilot-install | bash
```

### "You don't have access to GitHub Copilot"

1. [github.com/settings/copilot](https://github.com/settings/copilot) で Copilot サブスクリプションを確認する
2. 会社のアカウントを使用している場合は、組織が CLI アクセスを許可しているか確認する

### "Authentication failed"

再認証を行ってください：

```bash
copilot
> /login
```

### ブラウザが自動的に開かない

[github.com/login/device](https://github.com/login/device) を手動で開き、ターミナルに表示されたコードを入力してください。

### トークンが期限切れ

`/login` を再度実行するだけです：

```bash
copilot
> /login
```

### それでも解決しない場合

- [GitHub Copilot CLI のドキュメント](https://docs.github.com/copilot/concepts/agents/about-copilot-cli) を確認する
- [GitHub Issues](https://github.com/github/copilot-cli/issues) で検索する

---

## 🔑 まとめ

1. **GitHub Codespace はすぐに始める最も手軽な方法** - Python、pytest、GitHub Copilot CLI がすべてプリインストールされているので、すぐにデモに入れます
2. **複数のインストール方法** - Homebrew、WinGet、npm、インストールスクリプトの中からシステムに合ったものを選んでください
3. **認証は一度だけ** - トークンが期限切れになるまでサインイン状態が続きます
4. **Book App は動いている** - コース全体を通じて `samples/book-app-project` を使用します

> 📚 **公式ドキュメント**：[Copilot CLI をインストールする](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started)（インストールオプションと要件）

> 📋 **クイックリファレンス**：[GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)でコマンドとショートカットの完全なリストを確認できます。

---

**[Chapter 01: First Steps へ進む →](../01-setup-and-first-steps/README.md)**
