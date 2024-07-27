import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

class FileRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Renamer Rithy")
        
        # Set window size (width x height)
        self.root.geometry("400x300")  # Change this to your desired width and height

        # Directory selection
        self.dir_label = tk.Label(root, text="Select Directory:")
        self.dir_label.pack(pady=10)

        self.dir_button = tk.Button(root, text="Browse", command=self.browse_directory)
        self.dir_button.pack(pady=5)

        self.dir_path_label = tk.Label(root, text="No directory selected")
        self.dir_path_label.pack(pady=5)

        # Status label
        self.status_label = tk.Label(root, text="Status: Ready")
        self.status_label.pack(pady=10)

        # Rename button
        self.rename_button = tk.Button(root, text="Rename Files", command=self.rename_files)
        self.rename_button.pack(pady=20)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_path_label.config(text=directory)
            self.directory = directory

    def rename_files(self):
        if not hasattr(self, 'directory'):
            messagebox.showerror("Error", "No directory selected")
            return

        self.status_label.config(text="Status: Renaming files...")
        self.root.update_idletasks()  # Update the GUI to reflect the status change
        
        files = os.listdir(self.directory)
        pattern = re.compile(r'^\d+_')  # Regex to match filenames starting with a number followed by an underscore

        renamed_files = []
        errors = []

        for file_name in files:
            match = pattern.match(file_name)
            if match:
                # Remove the prefix (number + underscore)
                new_file_name = file_name[match.end():]
                old_file_path = os.path.join(self.directory, file_name)
                new_file_path = os.path.join(self.directory, new_file_name)
                
                if old_file_path == new_file_path:
                    # Skip renaming if the old and new file paths are the same
                    continue
                
                if os.path.exists(new_file_path):
                    # Handle the case where the new file name already exists
                    base, ext = os.path.splitext(new_file_name)
                    counter = 1
                    while os.path.exists(new_file_path):
                        new_file_name = f"{base}_{counter}{ext}"
                        new_file_path = os.path.join(self.directory, new_file_name)
                        counter += 1

                try:
                    # Rename the file
                    os.rename(old_file_path, new_file_path)
                    renamed_files.append((file_name, new_file_name))
                except Exception as e:
                    errors.append(f"Failed to rename '{file_name}' to '{new_file_name}': {e}")

        # Update status and show result
        if renamed_files:
            renamed_list = "\n".join([f"{old} -> {new}" for old, new in renamed_files])
            self.status_label.config(text="Status: Renaming completed")
            messagebox.showinfo("Renaming Completed", f"The following files were renamed:\n{renamed_list}")
        else:
            self.status_label.config(text="Status: No files matched the pattern")
            messagebox.showinfo("Renaming Completed", "No files matched the pattern.")

        if errors:
            error_list = "\n".join(errors)
            messagebox.showwarning("Renaming Errors", f"Some files could not be renamed:\n{error_list}")

        self.root.update_idletasks()  # Ensure the status label update is visible

if __name__ == "__main__":
    root = tk.Tk()
    app = FileRenamerApp(root)
    root.mainloop()
