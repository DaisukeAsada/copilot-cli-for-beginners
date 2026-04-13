# CI/CD 連携

> 📖 **前提**: この付録を読む前に [第7章: 総まとめ](../07-putting-it-together/README.md) を完了してください。
>
> ⚠️ **この付録は既存の CI/CD パイプラインを持つチーム向けです。** GitHub Actions や CI/CD の概念が初めての方は、第7章の [コードレビューの自動化](../07-putting-it-together/README.md#workflow-3-code-review-automation-optional) セクションにある、よりシンプルな pre-commit フックの方法から始めてください。

この付録では、GitHub Copilot CLI を CI/CD パイプラインに統合して、プルリクエストのコードレビューを自動化する方法を紹介します。

---

## GitHub Actions ワークフロー

このワークフローは、プルリクエストが作成または更新されたときに変更されたファイルを自動レビューします：

```yaml
# .github/workflows/copilot-review.yml
name: Copilot Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Needed to compare with main branch

      - name: Install Copilot CLI
        run: npm install -g @github/copilot

      - name: Review Changed Files
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Get list of changed JS/TS files
          FILES=$(git diff --name-only origin/main...HEAD | grep -E '\.(js|ts|jsx|tsx)$' || true)
          
          if [ -z "$FILES" ]; then
            echo "No JavaScript/TypeScript files changed"
            exit 0
          fi
          
          echo "# Copilot Code Review" > review.md
          echo "" >> review.md
          
          for file in $FILES; do
            echo "Reviewing $file..."
            echo "## $file" >> review.md
            echo "" >> review.md
            
            # Use --silent to suppress progress output
            copilot --allow-all -p "Quick security and quality review of @$file. List only critical issues." --silent >> review.md 2>/dev/null || echo "Review skipped" >> review.md
            echo "" >> review.md
          done

      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            
            // Only post if there's meaningful content
            if (review.includes('CRITICAL') || review.includes('HIGH')) {
              github.rest.issues.createComment({
                issue_number: context.issue.number,
                owner: context.repo.owner,
                repo: context.repo.repo,
                body: review
              });
            } else {
              console.log('No critical issues found, skipping comment');
            }
```

---

## 設定オプション

### レビュースコープの絞り込み

特定の種類の問題にレビューを集中させることができます：

```yaml
# Security-only review
copilot --allow-all -p "Security review of @$file. Check for: SQL injection, XSS, hardcoded secrets, authentication issues." --silent

# Performance-only review
copilot --allow-all -p "Performance review of @$file. Check for: N+1 queries, memory leaks, blocking operations." --silent
```

### 大きな PR の処理

ファイル数の多い PR は、バッチ処理または件数制限を検討してください：

```yaml
# Limit to first 10 files
FILES=$(git diff --name-only origin/main...HEAD | grep -E '\.(js|ts)$' | head -10)

# Or set a timeout per file
timeout 60 copilot --allow-all -p "Review @$file" --silent || echo "Review timed out"
```

### チーム設定

チーム全体で一貫したレビューを行うために、共有設定を作成します：

```json
// .copilot/config.json (committed to repo)
{
  "model": "claude-sonnet-4.5",
  "permissions": {
    "allowedPaths": ["src/**/*", "tests/**/*"],
    "deniedPaths": [".env*", "secrets/**/*", "*.min.js"]
  }
}
```

---

## 代替案: PR レビューボット

より高度なレビューワークフローには、GitHub Copilot のクラウドエージェントの使用を検討してください：

```yaml
# .github/workflows/copilot-agent-review.yml
name: Request Copilot Review

on:
  pull_request:
    types: [opened, ready_for_review]

jobs:
  request-review:
    runs-on: ubuntu-latest
    steps:
      - name: Request Copilot Review
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.pulls.requestReviewers({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number,
              reviewers: ['copilot[bot]']
            });
```

---

## CI/CD 連携のベストプラクティス

1. **`--silent` フラグを使用する** - ログをきれいに保つためにプログレス出力を抑制する
2. **タイムアウトを設定する** - レビューのハングアップがパイプラインをブロックしないようにする
3. **ファイルタイプを絞り込む** - 関連ファイルのみをレビューする（生成コードや依存関係はスキップ）
4. **レート制限を意識する** - 大きな PR ではレビューの間隔を空ける
5. **適切に失敗処理する** - レビューの失敗でマージをブロックしない。ログに記録して続行する

---

## トラブルシューティング

### CI で「認証に失敗しました」

ワークフローに正しいパーミッションが設定されているか確認してください：

```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

### レビューがタイムアウトする

タイムアウトを延長するか、スコープを絞り込んでください：

```bash
timeout 120 copilot --allow-all -p "Quick review of @$file - critical issues only" --silent
```

### 大きなファイルでのトークン上限

非常に大きなファイルはスキップしてください：

```bash
if [ $(wc -l < "$file") -lt 500 ]; then
  copilot --allow-all -p "Review @$file" --silent
else
  echo "Skipping $file (too large)"
fi
```

---

**[← Back to Chapter 07](../07-putting-it-together/README.md)** | **[Return to Appendices](README.md)**
