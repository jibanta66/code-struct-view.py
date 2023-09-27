import tkinter as tk
from tkinter import filedialog

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open Folder", command=self.open_folder)
        self.file_menu.add_command(label="Save File", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.close_window)

        self.view_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="tools", menu=self.view_menu)
        self.view_menu.add_command(label="Show List", command=self.show_list)

        self.help_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)

    def open_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            print("Selected folder:", folder_path)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            print("Selected file for saving:", file_path)

    def close_window(self):
        self.root.destroy()

    def show_about(self):
        # Add your About dialog logic here
        pass

    def show_list(self):
        # Create a new window to display the list
        list_window = tk.Toplevel(self.root)
        list_window.title("List Window")

        # Create a listbox widget to display the list
        listbox = tk.Listbox(list_window)
        listbox.pack()

        # Insert some sample items into the list
        for item in ["Item 1", "Item 2", "Item 3"]:
            listbox.insert(tk.END, item)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()
