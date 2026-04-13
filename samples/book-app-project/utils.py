def print_menu():
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    while True:
        choice = input("Choose an option (1-5): ").strip()
        if not choice:
            print("Please enter a number between 1 and 5.")
            continue
        if not choice.isdigit():
            print(f"'{choice}' is not a valid number. Please enter a number between 1 and 5.")
            continue
        return choice


def get_book_details():
    """Prompt the user to enter details for a new book.

    Repeatedly prompts until a non-empty title and author are provided.
    If the publication year is omitted or non-numeric, it defaults to 0.

    Returns:
        tuple[str, str, int]: A tuple of (title, author, year) where:
            - title (str): The book's title. Never empty.
            - author (str): The book's author. Never empty.
            - year (int): The publication year, or 0 if not provided / invalid.
    """
    while True:
        title = input("Enter book title: ").strip()
        if title:
            break
        print("Title cannot be empty. Please enter a title.")

    while True:
        author = input("Enter author: ").strip()
        if author:
            break
        print("Author cannot be empty. Please enter an author.")

    year_input = input("Enter publication year: ").strip()
    try:
        year = int(year_input)
    except ValueError:
        print("Invalid year. Defaulting to 0.")
        year = 0

    return title, author, year


def print_books(books):
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
