class EditorManager:
    def __init__(self):
        self.editor_count = 0

    def increment_count(self):
        self.editor_count += 1

    def decrement_count(self):
        self.editor_count -= 1

    def get_editor_count(self):
        return self.editor_count

    def export_count(self, filename):
        try:
            with open(filename, 'w') as file:
                file.write(str(self.editor_count))
            print(f"Editor count exported to {filename}")
        except Exception as e:
            print(f"Error exporting editor count: {e}")

