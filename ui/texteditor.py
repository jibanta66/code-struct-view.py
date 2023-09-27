import tkinter as tk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import filedialog

class TextEditor(tk.Toplevel):
    def __init__(self, parent, square_id):
        super().__init__(parent)
        self.square_id = square_id

        self.title("Text Editor")
        self.geometry("400x300")

        # Create a menu bar
        menubar = Menu(self)
        self.config(menu=menubar)

        # Create a "File" menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)

        # Add "Save" option to the "File" menu
        file_menu.add_command(label="Save", command=self.save_file)

        # Add "Close" option to the "File" menu
        file_menu.add_command(label="Close", command=self.close_editor)

        # Create a scrolled text widget
        self.text_widget = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.text_widget.pack(expand=True, fill="both")

        # Open a text editor, increment the count
        parent.open_text_editor(self.square_id)

    def get_text(self):
        return self.text_widget.get("1.0", tk.END)

    def set_text(self, text):
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", text)

    def save_file(self):
        text_to_save = self.get_text()
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

        if file_path:
            with open(file_path, "w") as file:
                file.write(text_to_save)

    def close_editor(self):
        # Close the text editor, decrement the count
        self.master.close_text_editor()
        self.destroy()
