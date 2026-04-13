# 追加コンテキスト機能

> 📖 **前提**: この付録を読む前に [第2章: コンテキストと会話](../02-context-conversations/README.md) を完了してください。

この付録では2つの追加コンテキスト機能を紹介します。画像の利用と、複数ディレクトリにまたがるパーミッション管理です。

---

## 画像の利用

`@` 構文を使って会話に画像を含めることができます。Copilot はスクリーンショット、モックアップ、図表などのビジュアルコンテンツを分析できます。

### 基本的な画像参照

```bash
copilot

> @screenshot.png What's happening in this UI?

# Copilot analyzes the image and responds

> @mockup.png @current-design.png Compare these two designs

# You can also drag and drop images or paste from clipboard
```

### 対応画像フォーマット

| フォーマット | 最適な用途 |
|--------|----------|
| PNG | スクリーンショット、UI モックアップ、図表 |
| JPG/JPEG | 写真、複雑な画像 |
| GIF | シンプルな図表（最初のフレームのみ） |
| WebP | ウェブのスクリーンショット |

### 画像の実用的な活用例

**1. UI デバッグ**
```bash
> @bug-screenshot.png The button doesn't align properly. What CSS might cause this?
```

**2. デザインの実装**
```bash
> @figma-export.png Write the HTML and Tailwind CSS to match this design
```

**3. エラーの分析**
```bash
> @error-screenshot.png What does this error mean and how do I fix it?
```

**4. アーキテクチャのレビュー**
```bash
> @whiteboard-diagram.png Convert this architecture diagram to a Mermaid diagram I can put in docs
```

**5. ビフォー/アフターの比較**
```bash
> @before.png @after.png What changed between these two versions of the UI?
```

### 画像とコードの組み合わせ

コードコンテキストと組み合わせると、画像はさらに威力を発揮します：

```bash
copilot

> @screenshot-of-bug.png @src/components/Header.jsx
> The header looks wrong in the screenshot. What's causing it in the code?
```

### 画像利用のヒント

- **スクリーンショットをトリミング**して関連部分だけを見せる（コンテキストトークンの節約になります）
- 分析してほしい UI 要素は**コントラストを高く**する
- **必要なら注釈を付ける** - 問題のある箇所を円で囲んだり強調してからアップロードする
- **1つの概念につき1枚の画像** - 複数画像も使えますが、焦点を絞ることが大切です

---

## パーミッションのパターン

デフォルトでは、Copilot は現在のディレクトリのファイルにアクセスできます。他の場所のファイルにアクセスするにはアクセス許可を付与する必要があります。

### ディレクトリの追加

```bash
# 許可リストにディレクトリを追加する
copilot --add-dir /path/to/other/project

# 複数のディレクトリを追加する
copilot --add-dir ~/workspace --add-dir /tmp
```

### すべてのパスを許可する

```bash
# パスの制限を完全に無効にする（慎重に使用してください）
copilot --allow-all-paths
```

### セッション内での操作

```bash
copilot

> /add-dir /path/to/other/project
# そのディレクトリのファイルを参照できるようになります

> /list-dirs
# 許可されているすべてのディレクトリを確認する
```

### 自動化での利用

```bash
# 非インタラクティブなスクリプトですべてのパーミッションを許可する
copilot -p "Review @src/" --allow-all

# または覚えやすいエイリアスを使用する
copilot -p "Review @src/" --yolo
```

### 複数ディレクトリアクセスが必要なケース

パーミッションが必要になる一般的なシナリオ：

1. **モノレポ作業** - パッケージをまたいだコードの比較
2. **クロスプロジェクトのリファクタリング** - 共有ライブラリの更新
3. **ドキュメントプロジェクト** - 複数のコードベースの参照
4. **移行作業** - 旧実装と新実装の比較

---

**[← Back to Chapter 02](../02-context-conversations/README.md)** | **[Return to Appendices](README.md)**
