import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkMessageBox
import random
import database


class VocabularyApp:
    def __init__(self, root):
        self.root = root
        self.db = database.Database()
        self.db.create_db_tables()
        self.create_widgets()
        self.load_sentences()
        self.load_monk_data()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.tab_new_sentence = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_new_sentence, text="New Sentence")
        self.create_new_sentence_tab()

        self.tab_saved_sentences = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_saved_sentences, text="Saved Sentences")
        self.create_saved_sentences_tab()

        self.tab_monk = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_monk, text="Monk")
        self.create_monk_tab()

    def create_new_sentence_tab(self):
        lbl_word_types = tk.Label(self.tab_new_sentence, text="", font=("Arial", 20))
        lbl_word_types.pack()

        lbl_words = tk.Label(self.tab_new_sentence, text="", font=("Arial", 20))
        lbl_words.pack()

        self.txt_sentence = tk.Text(
            self.tab_new_sentence, height=2, width=30, font=("Arial", 20)
        )
        self.txt_sentence.pack()

        btn_new_words = tk.Button(
            self.tab_new_sentence,
            text="New Words",
            command=self.new_words,
            font=("Arial", 20),
        )
        btn_new_words.pack()

        btn_save_sentence = tk.Button(
            self.tab_new_sentence,
            text="Save Sentence",
            command=self.save_sentence,
            font=("Arial", 20),
        )
        btn_save_sentence.pack()

        self.new_sentence_widgets = {
            "lbl_word_types": lbl_word_types,
            "lbl_words": lbl_words,
        }

    def create_saved_sentences_tab(self):
        self.saved_sentences_listbox = tk.Listbox(
            self.tab_saved_sentences, font=("Arial", 14), width=50
        )
        self.saved_sentences_listbox.pack(fill="both", expand=True)

        btn_delete_sentence = tk.Button(
            self.tab_saved_sentences,
            text="Delete Sentence",
            command=self.delete_sentence,
            font=("Arial", 14),
        )
        btn_delete_sentence.pack()

    def create_monk_tab(self):
        self.lbl_monk_level = tk.Label(
            self.tab_monk, text="Monk Level:", font=("Arial", 16)
        )
        self.lbl_monk_level.pack()

        self.lbl_monk_concentration = tk.Label(
            self.tab_monk, text="Concentration Points:", font=("Arial", 16)
        )
        self.lbl_monk_concentration.pack()

    def load_sentences(self):
        sentences = self.db.load_sentences()
        for sentence in sentences:
            display_text = f"{sentence[1]}: {sentence[2]} - Difficulty: {sentence[3]}"
            self.saved_sentences_listbox.insert(tk.END, display_text)
            self.saved_sentences_listbox.itemconfig(tk.END, bg="lightblue")

    def load_monk_data(self):
        # For simplicity, initializing with default values
        self.monk_level = 1
        self.monk_concentration_points = 0
        self.update_monk_display()

    def new_words(self):
        word_types, words = self.db.fetch_words()
        self.new_sentence_widgets["lbl_word_types"].config(text=" - ".join(word_types))
        self.new_sentence_widgets["lbl_words"].config(text=" - ".join(words))

    def save_sentence(self):
        sentence = self.txt_sentence.get("1.0", "end-1c")
        word = self.new_sentence_widgets["lbl_words"].cget("text")

        # Check if the sentence length is zero
        if len(sentence.strip()) == 0:
            tkMessageBox.showerror("Error", "Please enter a non-empty sentence.")
            return

        difficulty_score = self.db.analyze_sentence_difficulty(sentence)

        self.db.save_sentence(word, sentence, difficulty_score)

        self.monk_concentration_points += difficulty_score
        self.update_monk_display()

        tkMessageBox.showinfo("Sentence Saved", "The sentence has been saved.")
        self.saved_sentences_listbox.insert(
            tk.END, f"{word}: {sentence} - Difficulty: {difficulty_score}"
        )
        self.saved_sentences_listbox.itemconfig(tk.END, bg="lightblue")

    def delete_sentence(self):
        selected_index = self.saved_sentences_listbox.curselection()
        if not selected_index:
            tkMessageBox.showerror("Error", "Please select a sentence to delete.")
            return

        confirm = tkMessageBox.askyesno(
            "Delete Sentence", "Are you sure you want to delete this sentence?"
        )
        if confirm:
            selected_id = selected_index[0] + 1  # Add 1 to match the database id
            self.db.delete_sentence(selected_id)
            self.saved_sentences_listbox.delete(selected_index)
            tkMessageBox.showinfo("Success", "Sentence deleted successfully.")

    def update_monk_display(self):
        self.lbl_monk_level.config(text=f"Monk Level: {self.monk_level}")
        self.lbl_monk_concentration.config(
            text=f"Concentration Points: {self.monk_concentration_points}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = VocabularyApp(root)
    root.mainloop()
