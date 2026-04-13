# カスタム MCP サーバーの構築

> ⚠️ **このコンテンツは完全にオプションです。** GitHub、filesystem、Context7 などの既製 MCP サーバーだけでも Copilot CLI を十分に活用できます。このガイドは、Copilot を独自の内部 API に接続したい開発者向けです。詳しくは [MCP for Beginners course](https://github.com/microsoft/mcp-for-beginners) をご覧ください。
>
> **前提条件：**
> - Python に慣れていること
> - `async`/`await` パターンを理解していること
> - システムに `pip` が使えること（この dev container には含まれています）
>
> **[← Chapter 06: MCP Servers に戻る](README.md)**

---

Copilot を自分の API に接続したいですか？このガイドでは、このコースを通じて使ってきた book app プロジェクトをベースに、本の情報を検索するシンプルな MCP サーバーを Python で構築する方法を説明します。

## プロジェクトのセットアップ

```bash
mkdir book-lookup-mcp-server
cd book-lookup-mcp-server
pip install mcp
```

> 💡 **`mcp` パッケージとは？** MCP サーバーを構築するための公式 Python SDK です。プロトコルの詳細を自動で処理してくれるので、ツールの実装に集中できます。

## サーバーの実装

`server.py` というファイルを作成します：

```python
# server.py
import json
from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("book-lookup")

# Sample book database (in a real server, this could query an API or database)
BOOKS_DB = {
    "978-0-547-92822-7": {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "year": 1937,
        "genre": "Fantasy",
    },
    "978-0-451-52493-5": {
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "genre": "Dystopian Fiction",
    },
    "978-0-441-17271-9": {
        "title": "Dune",
        "author": "Frank Herbert",
        "year": 1965,
        "genre": "Science Fiction",
    },
}


@mcp.tool()
def lookup_book(isbn: str) -> str:
    """Look up a book by its ISBN and return title, author, year, and genre."""
    book = BOOKS_DB.get(isbn)
    if book:
        return json.dumps(book, indent=2)
    return f"No book found with ISBN: {isbn}"


@mcp.tool()
def search_books(query: str) -> str:
    """Search for books by title or author. Returns all matching results."""
    query_lower = query.lower()
    results = [
        {**book, "isbn": isbn}
        for isbn, book in BOOKS_DB.items()
        if query_lower in book["title"].lower()
        or query_lower in book["author"].lower()
    ]
    if results:
        return json.dumps(results, indent=2)
    return f"No books found matching: {query}"


@mcp.tool()
def list_all_books() -> str:
    """List all books in the database with their ISBNs."""
    books_list = [
        {"isbn": isbn, "title": book["title"], "author": book["author"]}
        for isbn, book in BOOKS_DB.items()
    ]
    return json.dumps(books_list, indent=2)


if __name__ == "__main__":
    mcp.run()
```

**何が起きているか：**

| 部分 | 役割 |
|------|-------------|
| `FastMCP("book-lookup")` | "book-lookup" という名前のサーバーを作成する |
| `@mcp.tool()` | 関数を Copilot が呼び出せるツールとして登録する |
| 型ヒント＋docstring | 各ツールの機能と必要なパラメータを Copilot に伝える |
| `mcp.run()` | サーバーを起動してリクエストを待ち受ける |

> 💡 **デコレータを使う理由は？** `@mcp.tool()` デコレータを付けるだけで OK です。MCP SDK が関数名・型ヒント・docstring を自動で読み取り、ツールのスキーマを生成します。JSON スキーマを手書きする必要はありません！

## 設定

`~/.copilot/mcp-config.json` に以下を追加します：

```json
{
  "mcpServers": {
    "book-lookup": {
      "type": "local",
      "command": "python3",
      "args": ["./book-lookup-mcp-server/server.py"],
      "tools": ["*"]
    }
  }
}
```

## 使い方

```bash
copilot

> Look up the book with ISBN 978-0-547-92822-7

{
  "title": "The Hobbit",
  "author": "J.R.R. Tolkien",
  "year": 1937,
  "genre": "Fantasy"
}

> Search for books by Orwell

[
  {
    "title": "1984",
    "author": "George Orwell",
    "year": 1949,
    "genre": "Dystopian Fiction",
    "isbn": "978-0-451-52493-5"
  }
]

> List all available books

[Shows all books in the database with ISBNs]
```

## 次のステップ

基本的なサーバーを構築したら、以下のことができます：

1. **ツールを追加する** - `@mcp.tool()` 関数を増やすだけで、Copilot が呼び出せるツールが増えます
2. **実際の API に接続する** - モックの `BOOKS_DB` を実際の API 呼び出しやデータベースクエリに置き換えます
3. **認証を追加する** - API キーやトークンを安全に扱います
4. **サーバーを共有する** - PyPI に公開して他の人が `pip` でインストールできるようにします

## リソース

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Example MCP Servers](https://github.com/modelcontextprotocol/servers)
- [MCP for Beginners Course](https://github.com/microsoft/mcp-for-beginners)

---

**[← Chapter 06: MCP Servers に戻る](README.md)**
