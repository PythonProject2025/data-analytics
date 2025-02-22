from tkinter import filedialog, messagebox

def open_file_dialog():
    """
    Opens a file dialog to let the user select a file.
    Returns the selected file path if valid, otherwise None.
    """
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("CSV Files", "*.csv"), ("Image Files", "*.png;*.jpg;*.jpeg")]
    )

    if not file_path:
        return None  # User canceled file selection

    # Determine file type
    if file_path.endswith((".csv", ".png", ".jpg", ".jpeg")):
        #messagebox.showinfo("File Selected", f"Selected File: {file_path}")
        return file_path
    else:
        messagebox.showerror("Invalid File", "Please select a valid CSV or zip file.")
        return None
