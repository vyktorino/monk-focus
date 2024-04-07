import tkinter as tk
from vocabulary_app import VocabularyApp

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = VocabularyApp(root)
    root.mainloop()
