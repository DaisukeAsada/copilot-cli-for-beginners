![GitHub Copilot CLI for Beginners](./images/copilot-banner.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)&ensp;
[![Open project in GitHub Codespaces](https://img.shields.io/badge/Codespaces-Open-blue?style=flat-square&logo=github)](https://codespaces.new/github/copilot-cli-for-beginners?hide_repo_select=true&ref=main&quickstart=true)&ensp;
[![Official Copilot CLI documentation](https://img.shields.io/badge/GitHub-CLI_Documentation-00a3ee?style=flat-square&logo=github)](https://docs.github.com/en/copilot/how-tos/copilot-cli)&ensp;
[![Join AI Foundry Discord](https://img.shields.io/badge/Discord-AI_Community-blue?style=flat-square&logo=discord&color=5865f2&logoColor=fff)](https://aka.ms/foundry/discord)

🎯 [学習内容](#-学習内容) &ensp; ✅ [前提条件](#-前提条件) &ensp; 🤖 [Copilot ファミリー](#-github-copilot-ファミリーを理解する) &ensp; 📚 [コース構成](#-コース構成) &ensp; 📋 [コマンドリファレンス](#-github-copilot-cli-コマンドリファレンス)

# GitHub Copilot CLI for Beginners

> **✨ AI を活用したコマンドライン支援で、開発ワークフローを強化しましょう。**

GitHub Copilot CLI は、AI によるサポートをターミナルに直接届けます。ブラウザやコードエディターに切り替えることなく、コマンドラインを離れずに質問したり、フル機能のアプリケーションを生成したり、コードレビューやテスト生成、デバッグを行えます。

頼れる同僚が 24 時間 365 日そばにいて、コードを読み、わかりにくいパターンを説明し、作業を素早く進める手助けをしてくれるようなイメージです！

> 📘 **Web ブラウザで学びたい方へ:** このコースは GitHub 上でそのまま進められます。また [Awesome Copilot](https://awesome-copilot.github.com/learning-hub/cli-for-beginners/) でも閲覧できます。

このコースの対象者：

- コマンドラインから AI を活用したい **ソフトウェア開発者**
- IDE 統合よりキーボード操作を好む **ターミナルユーザー**
- AI を使ったコードレビューや開発プラクティスを標準化したい **チーム**

<a href="https://aka.ms/githubcopilotdevdays" target="_blank">
  <picture>
    <img src="./images/copilot-dev-days.png" alt="GitHub Copilot Dev Days - Find or host an event" width="100%" />
  </picture>
</a>

## 🎯 学習内容

このハンズオンコースでは、GitHub Copilot CLI をゼロから使いこなせるようになります。全チャプターを通じて 1 つの Python 製ブックコレクションアプリを使い、AI を活用したワークフローで段階的に改善していきます。最終的には、コードレビュー・テスト生成・デバッグ・ワークフローの自動化をすべてターミナルから自信を持って行えるようになります。

**AI の経験は不要です。** ターミナルを使えれば、このコースを学べます。

**こんな方におすすめ：** 開発者、学生、ソフトウェア開発の経験がある方。

## ✅ 前提条件

開始前に以下を準備してください：

- **GitHub アカウント**: [無料で作成](https://github.com/signup)<br>
- **GitHub Copilot へのアクセス**: [無料プラン](https://github.com/features/copilot/plans)、[月額サブスクリプション](https://github.com/features/copilot/plans)、または [学生・教員向け無料プラン](https://education.github.com/pack)<br>
- **ターミナルの基本操作**: `cd`、`ls`、コマンドの実行に慣れていること

## 🤖 GitHub Copilot ファミリーを理解する

GitHub Copilot は、AI を活用したツール群へと進化しました。各ツールの概要は以下のとおりです：

| 製品 | 動作環境 | 説明 |
|---------|---------------|----------|
| [**GitHub Copilot CLI**](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started)<br>（本コース） | ターミナル | ターミナルネイティブな AI コーディングアシスタント |
| [**GitHub Copilot**](https://docs.github.com/copilot) | VS Code、Visual Studio、JetBrains など | Agent mode、チャット、インラインサジェスト |
| [**Copilot on GitHub.com**](https://github.com/copilot) | GitHub | リポジトリについての没入型チャット、エージェントの作成など |
| [**GitHub Copilot cloud agent**](https://docs.github.com/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks) | GitHub | Issue をエージェントにアサインし、PR を受け取る |

本コースでは **GitHub Copilot CLI** に焦点を当て、AI による支援をターミナルに直接届けます。

## 📚 コース構成

![GitHub Copilot CLI Learning Path](images/learning-path.png)

| チャプター | タイトル | 作るもの |
|:-------:|-------|-------------------|
| 00 | 🚀 [クイックスタート](./00-quick-start/README.md) | インストールと動作確認 |
| 01 | 👋 [はじめの一歩](./01-setup-and-first-steps/README.md) | ライブデモ + 3 つのインタラクションモード |
| 02 | 🔍 [コンテキストと会話](./02-context-conversations/README.md) | 複数ファイルプロジェクトの分析 |
| 03 | ⚡ [開発ワークフロー](./03-development-workflows/README.md) | コードレビュー、デバッグ、テスト生成 |
| 04 | 🤖 [専門 AI アシスタントの作成](./04-agents-custom-instructions/README.md) | ワークフロー向けカスタムエージェント |
| 05 | 🛠️ [繰り返し作業の自動化](./05-skills/README.md) | 自動ロードされるスキル |
| 06 | 🔌 [GitHub・データベース・API への接続](./06-mcp-servers/README.md) | MCP サーバーの統合 |
| 07 | 🎯 [すべてを組み合わせる](./07-putting-it-together/README.md) | 完全な機能ワークフロー |

## 📖 コースの進め方

各チャプターは同じ構成で進みます：

1. **現実世界のアナロジー**: 身近な例でコンセプトを理解する
2. **コアコンセプト**: 必要な知識を学ぶ
3. **ハンズオン例**: 実際にコマンドを実行して結果を確認する
4. **課題**: 学んだ内容を練習する
5. **次のステップ**: 次のチャプターのプレビュー

**コード例はそのまま実行できます。** このコースのすべての copilot テキストブロックはターミナルにコピーして実行できます。

## 📋 GitHub Copilot CLI コマンドリファレンス

**[GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)** では、Copilot CLI を効果的に使うためのコマンドやキーボードショートカットを確認できます。

## 🙋 ヘルプとサポート

- 🐛 **バグを見つけた？** [Issue を開く](https://github.com/github/copilot-cli-for-beginners/issues)
- 🤝 **コントリビュートしたい？** PR 歓迎！
- 📚 **公式ドキュメント:** [GitHub Copilot CLI ドキュメント](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)

## ライセンス

このプロジェクトは MIT オープンソースライセンスのもとで提供されています。詳細は [LICENSE](./LICENSE) ファイルをご参照ください。

