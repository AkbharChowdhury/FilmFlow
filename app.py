import tkinter as tk
from tkinter import ttk


class FilmFlowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FilmFlow")
        self.root.geometry("500x400")
        self.root.resizable(True, True)

        # Main frame with border
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title label
        self.title_label = ttk.Label(
            self.main_frame,
            text="Title",
            font=("Arial", 12)
        )
        self.title_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        # Title entry
        self.title_entry = ttk.Entry(self.main_frame, width=40)
        self.title_entry.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))

        # Genres label
        self.genres_label = ttk.Label(
            self.main_frame,
            text="Genres",
            font=("Arial", 12)
        )
        self.genres_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 10))

        # Genre checkboxes
        self.genre_vars = {}
        self.genres = ["Action", "Animation", "Drama", 'War']

        row = 3
        for genre in self.genres:
            # var = tk.BooleanVar(value=(genre == "Animation"))  # Animation pre-checked
            cb = ttk.Checkbutton(
                self.main_frame,
                text=genre,
                variable=var
            )
            cb.grid(row=row, column=0, sticky=tk.W, pady=5)
            self.genre_vars[genre] = var
            row += 1

        # Add Movie button
        self.add_btn = ttk.Button(
            self.main_frame,
            text="Add Movie",
            command=self.add_movie
        )
        self.add_btn.grid(row=row, column=0, pady=(20, 0))

    def add_movie(self):
        """Handle Add Movie button click"""
        title = self.title_entry.get().strip()
        selected_genres = [
            genre for genre, var in self.genre_vars.items()
            if var.get()
        ]

        # Here you would call your FilmFlowDB method
        print(f"Title: {title}")
        print(f"Selected Genres: {selected_genres}")

        # Example DB call (uncomment when connected):
        # if title:
        #     genre_ids = self.get_genre_ids(selected_genres)
        #     db.add_movie_and_genres(title, set(genre_ids))
        #     self.title_entry.delete(0, tk.END)  # Clear form


if __name__ == "__main__":
    root = tk.Tk()
    app = FilmFlowApp(root)
    root.mainloop()