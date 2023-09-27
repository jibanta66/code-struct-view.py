

import tkinter as tk
from menubar import MainMenu
from texteditor import TextEditor

class Pen:
    def __init__(self, canvas):
        self.canvas = canvas
        self.is_drawing = False
        self.prev_x = None
        self.prev_y = None

    def start_drawing(self, event):
        self.is_drawing = True
        self.prev_x = event.x
        self.prev_y = event.y

    def stop_drawing(self, event):
        self.is_drawing = False
        self.prev_x = None
        self.prev_y = None

    def draw(self, event):
        if self.is_drawing:
            x, y = event.x, event.y
            if self.prev_x is not None and self.prev_y is not None:
                self.canvas.create_line(self.prev_x, self.prev_y, x, y)
            self.prev_x = x
            self.prev_y = y

class SquareContainer:
    def __init__(self, canvas, x, y, size, label):
        self.canvas = canvas
        self.size = size
        self.label = label
        self.square = Square(self, x, y, size)  # Pass the SquareContainer instance as the first argument
        self.label_id = None
        self.update_label(x, y)

    def update_label(self, x, y):
        if self.label_id is not None:
            self.canvas.delete(self.label_id)
        self.label_id = self.canvas.create_text(x, y + self.size / 2 + 10, text=self.label, fill="black")

    def update_label_position(self, x, y):
        label_x = x + self.size / 2
        label_y = y + self.size / 2 + 10
        self.canvas.coords(self.label_id, label_x, label_y)

class Square:
    def __init__(self, square_container, x, y, size):
        self.square_container = square_container  # Store the reference to the SquareContainer instance
        self.canvas = square_container.canvas
        self.size = size
        self.shape = None
        self.start_x = None
        self.start_y = None
        self.is_clicked = False
        self.id = None
        self.text_editor = None

        self.draw(x, y)

    def draw(self, x, y):
        self.start_x = x - self.size / 2
        self.start_y = y - self.size / 2
        x2, y2 = x + self.size / 2, y + self.size / 2
        self.shape = self.canvas.create_rectangle(self.start_x, self.start_y, x2, y2, fill="blue")

        self.id = len(self.canvas.find_all())

        self.canvas.tag_bind(self.shape, '<ButtonPress-1>', self.on_press)
        self.canvas.tag_bind(self.shape, '<B1-Motion>', self.on_drag)
        self.canvas.tag_bind(self.shape, '<ButtonRelease-1>', self.on_release)
        self.canvas.tag_bind(self.shape, '<Double-Button-1>', self.on_double_click)

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_release(self, event):
        pass

    def on_double_click(self, event):
        if not self.is_clicked:
            self.text_editor = TextEditor(self.canvas, self.id)
            self.is_clicked = True
        else:
            self.is_clicked = False

    def on_drag(self, event):
        # Check if drawing mode is not active
        if not self.canvas.master.drawing_mode:
            x, y = event.x, event.y
            delta_x = x - self.start_x
            delta_y = y - self.start_y
            self.canvas.move(self.shape, delta_x, delta_y)
            self.start_x = x
            self.start_y = y

            # Update the label's position using the SquareContainer's method
            if self.square_container:
                self.square_container.update_label_position(x, y)

class CanvasApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Nodes and Edges")
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)
        self.minimize_button = tk.Button(self, text="Minimize", command=self.minimize_window)
        self.minimize_button.pack(fill="x")
        self.exit_button = tk.Button(self, text="Exit", command=self.close_window)
        self.exit_button.pack(fill="x")
        self.draw_button = tk.Button(self, text="Draw", command=self.toggle_draw)
        self.draw_button.pack(fill="x")
        self.square_button = tk.Button(self, text="Square", command=self.create_square)
        self.square_button.pack(fill="x")
        self.main_menu = MainMenu(self)
        self.pen = Pen(self.canvas)
        self.drawing_mode = False
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.zoom_factor = 1.0

        self.editor_count = 0  # Initialize the editor count variable
        self.editor_labels = []  # Store references to editor labels

        # Add a button to display the editor count
        self.show_count_button = tk.Button(self, text="Show Editor Count", command=self.show_editor_count)
        self.show_count_button.pack(fill="x")

    def minimize_window(self):
        self.iconify()

    def close_window(self):
        self.destroy()

    def toggle_draw(self):
        self.drawing_mode = not self.drawing_mode
        if self.drawing_mode:
            self.canvas.config(cursor="pencil")
            self.canvas.bind("<Button-1>", self.pen.start_drawing)
            self.canvas.bind("<ButtonRelease-1>", self.pen.stop_drawing)
            self.canvas.bind("<Motion>", self.pen.draw)
        else:
            self.canvas.config(cursor="")
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.canvas.unbind("<Motion>")
            self.pen.stop_drawing()

    def zoom(self, event):
        if event.delta > 0:
            zoom_factor = 1.1
        else:
            zoom_factor = 1 / 1.1
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.canvas.scale("all", x, y, zoom_factor, zoom_factor)

    def create_square(self):
        canvas_center_x = self.canvas.winfo_reqwidth() / 2
        canvas_center_y = self.canvas.winfo_reqheight() / 2
        square_container = SquareContainer(self.canvas, canvas_center_x, canvas_center_y, 50, "Label")

        # Increment the editor count and update the label
        self.editor_count += 1
        self.update_editor_label()

    def open_text_editor(self, square_id):
        self.editor_count += 1
        self.update_editor_label()

    def close_text_editor(self):
        self.editor_count -= 1
        self.update_editor_label()

    def update_editor_label(self):
        # Remove existing editor count labels
        for label in self.editor_labels:
            label.destroy()
        self.editor_labels = []

        # Create and display the new editor count label
        editor_label = tk.Label(self, text=f"Editors Open: {self.editor_count}")
        editor_label.pack(fill="x")
        self.editor_labels.append(editor_label)

    def show_editor_count(self):
        # Create a message box to display the editor count
        editor_count_message = f"Editors Open: {self.editor_count}"
        tk.messagebox.showinfo("Editor Count", editor_count_message)

if __name__ == "__main__":
    app = CanvasApp()
    app.mainloop()