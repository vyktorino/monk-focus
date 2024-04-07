import sqlite3
import random
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkMessageBox
import pandas as pd
import jieba.posseg as pseg

# Constants
VALID_COMBINATIONS = [
    ["n", "v", "n"],  # noun - verb - noun
    ["adj", "n", "v"],  # adjective - noun - verb
    ["adv", "v", "n"],  # adverb - verb - noun
    ["n", "v", "adj"],  # noun - verb - adjective
    ["n", "prep", "n"],  # noun - preposition - noun
    ["conj", "n", "v"],  # conjunction - noun - verb
    ["n", "v", "adv"],  # noun - verb - adverb
    ["v", "conj", "v"],  # verb - conjunction - verb
    ["n", "v", "exp"],  # noun - verb - expression
    ["exp", "v", "n"],  # expression - verb - noun
]


class Database:
    def __init__(self):
        self.DB_FILE = "hsk4.db"
        self.SENTENCES_DB_FILE = "saved_sentences.db"

    def create_db_tables(self):
        conn = sqlite3.connect(self.DB_FILE)
        c = conn.cursor()
        # Create vocabulary table
        c.execute(
            """CREATE TABLE IF NOT EXISTS vocabulary
                    (character text, type text)"""
        )
        conn = sqlite3.connect(self.SENTENCES_DB_FILE)
        c = conn.cursor()
        # Create sentences table with the id column
        c.execute(
            """CREATE TABLE IF NOT EXISTS saved_sentences
                    (id INTEGER PRIMARY KEY, word text, sentence text, difficulty integer)"""
        )
        conn.commit()
        conn.close()

    def fetch_words(self):
        conn = sqlite3.connect(self.DB_FILE)
        c = conn.cursor()
        word_types = random.choice(VALID_COMBINATIONS)
        words = []
        for word_type in word_types:
            c.execute(f"SELECT character FROM vocabulary WHERE type='{word_type}'")
            word_list = [item[0] for item in c.fetchall()]
            if word_type == "n" and "n" in words:
                word = random.choice(word_list)
                while word in words:
                    word = random.choice(word_list)
                words.append(word)
            else:
                words.append(random.choice(word_list))
        conn.close()
        return word_types, words

    def load_sentences(self):
        conn = sqlite3.connect(self.SENTENCES_DB_FILE)
        c = conn.cursor()
        c.execute("SELECT id, word, sentence, difficulty FROM saved_sentences")
        sentences = c.fetchall()
        conn.close()
        return sentences

    def save_sentence(self, word, sentence, difficulty_score):
        conn = sqlite3.connect(self.SENTENCES_DB_FILE)
        c = conn.cursor()
        c.execute(
            """INSERT INTO saved_sentences (word, sentence, difficulty) VALUES (?,?,?)""",
            (word, sentence, difficulty_score),
        )
        conn.commit()
        conn.close()

    def delete_sentence(self, selected_id):
        conn = sqlite3.connect(self.SENTENCES_DB_FILE)
        c = conn.cursor()
        c.execute("DELETE FROM saved_sentences WHERE id=?", (selected_id,))
        conn.commit()
        conn.close()

    def analyze_sentence_difficulty(self, sentence):
        words = pseg.cut(sentence)
        difficulty_score = 0
        for word, flag in words:
            if flag.startswith("n"):  # Nouns
                difficulty_score += 1
            elif flag.startswith("v"):  # Verbs
                difficulty_score += 2
            elif flag.startswith("a"):  # Adjectives
                difficulty_score += 2
            elif flag.startswith("d"):  # Adverbs
                difficulty_score += 2
            elif flag.startswith("c"):  # Conjunctions
                difficulty_score += 1
        return difficulty_score
