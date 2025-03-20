import json
import streamlit as st
import streamlit.components.v1 as components

class BookCollection:
    """A class to manage a collection of books, allowing users to store and organize their reading materials."""

    def __init__(self):
        """Initialize a new book collection with an empty list and set up file storage."""
        self.book_list = []
        self.storage_file = "books_data.json"
        self.read_from_file()

    def read_from_file(self):
        """Load saved books from a JSON file into memory.
        If the file doesn't exist or is corrupted, start with an empty collection."""
        try:
            with open(self.storage_file, "r") as file:
                self.book_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.book_list = []

    def save_to_file(self):
        """Store the current book collection to a JSON file for permanent storage."""
        with open(self.storage_file, "w") as file:
            json.dump(self.book_list, file, indent=4)

    def add_book(self, title, author, year, genre, read):
        """Add a new book to the collection."""
        new_book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read,
        }
        self.book_list.append(new_book)
        self.save_to_file()

    def delete_book(self, title):
        """Remove a book from the collection using its title."""
        self.book_list = [book for book in self.book_list if book["title"].lower() != title.lower()]
        self.save_to_file()

    def find_books(self, search_text):
        """Search for books in the collection by title or author name."""
        return [book for book in self.book_list if search_text.lower() in book["title"].lower() or search_text.lower() in book["author"].lower()]

    def get_books(self):
        """Return all books."""
        return self.book_list

    def get_reading_progress(self):
        """Calculate and return reading progress."""
        total_books = len(self.book_list)
        completed_books = sum(1 for book in self.book_list if book["read"])
        completion_rate = (completed_books / total_books * 100) if total_books > 0 else 0
        return total_books, completion_rate

# Initialize the BookCollection class
book_manager = BookCollection()

# Apply Light Yellow Background and Green/Black Text using Streamlit
page_bg = """
<style>
    .stApp {
        background: #FFF9C4;
    }
    .stSidebar {
        background: #FFF9C4;
        padding: 20px;
        border-radius: 10px;
    }
    h1, h2, h3, h4, h5, h6, p, label {
        color: green;
    }
    .stButton>button {
        background-color: black;
        color: white;
    }
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Streamlit UI
st.title("📚 Personal Library")

# Sidebar - Add a New Book
st.sidebar.markdown("""<div class='stSidebar'><h3 style='color:green;'>Add a New Book</h3></div>""", unsafe_allow_html=True)
title = st.sidebar.text_input("Title")
author = st.sidebar.text_input("Author")
year = st.sidebar.text_input("Publication Year")
genre = st.sidebar.text_input("Genre")
read = st.sidebar.checkbox("Mark as Read")

if st.sidebar.button("Add Book"):
    if title and author:
        book_manager.add_book(title, author, year, genre, read)
        st.sidebar.success("Book added successfully!")
    else:
        st.sidebar.error("Please enter both title and author.")

# Search Functionality
search_text = st.text_input("Search by Title or Author")
if search_text:
    found_books = book_manager.find_books(search_text)
    if found_books:
        st.subheader("Search Results")
        for book in found_books:
            st.write(f"📖 {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'✔️ Read' if book['read'] else '❌ Unread'}")
    else:
        st.warning("No matching books found.")

# Display All Books
st.subheader("📚 Your Book Collection")
all_books = book_manager.get_books()
if all_books:
    for book in all_books:
        st.write(f"📖 {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'✔️ Read' if book['read'] else '❌ Unread'}")
else:
    st.write("No books in your collection.")

# Delete a Book
book_to_delete = st.text_input("Enter the title of the book to delete")
if st.button("Delete Book"):
    book_manager.delete_book(book_to_delete)
    st.success("Book deleted successfully!")

# Show Reading Progress
st.subheader("📊 Reading Progress")
total_books, completion_rate = book_manager.get_reading_progress()
st.write(f"Total Books: {total_books}")
st.progress(completion_rate / 100)
st.write(f"Reading Completion: {completion_rate:.2f}%")