import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

from organizer import organize_files, undo_last_organization


# Select folder
def select_folder():
    folder = filedialog.askdirectory()

    if folder:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder)


# Update progress bar
def update_progress(current, total):

    if total > 0:
        percentage = (current / total) * 100

        progress_bar["value"] = percentage

        progress_label.config(
            text=f"Organizing files... {current}/{total} ({percentage:.0f}%)"
        )

        root.update_idletasks()


# Organize files
def organize():

    folder = folder_entry.get()

    if not folder:
        messagebox.showwarning(
            "Warning",
            "Please select a folder first."
        )
        return

    try:

        progress_bar["value"] = 0

        progress_label.config(
            text="Starting organization..."
        )

        organize_button.config(
            state="disabled"
        )

        undo_button.config(
            state="disabled"
        )

        root.update_idletasks()

        # Organize files
        total_files, category_counts = organize_files(
            folder,
            update_progress
        )

        # Result
        result_label.config(
            text=f"✓ {total_files} files organized successfully!"
        )

        # Statistics
        stats_label.config(
            text=(
                f"Images: {category_counts['Images']}    "
                f"Documents: {category_counts['Documents']}    "
                f"Videos: {category_counts['Videos']}\n"
                f"Audio: {category_counts['Audio']}    "
                f"Archives: {category_counts['Archives']}    "
                f"Code: {category_counts['Code']}    "
                f"Others: {category_counts['Others']}"
            )
        )

        progress_bar["value"] = 100

        progress_label.config(
            text=f"Completed! {total_files}/{total_files} files organized."
        )

        organize_button.config(
            state="normal"
        )

        # Enable Undo
        if total_files > 0:
            undo_button.config(
                state="normal"
            )

        messagebox.showinfo(
            "Success",
            f"{total_files} files organized successfully."
        )

    except Exception as error:

        organize_button.config(
            state="normal"
        )

        messagebox.showerror(
            "Error",
            f"Something went wrong:\n{error}"
        )


# Undo organization
def undo():

    try:

        restored_files = undo_last_organization()

        if restored_files > 0:

            result_label.config(
                text=f"↩ {restored_files} files restored successfully!"
            )

            progress_bar["value"] = 0

            progress_label.config(
                text="Last organization has been undone."
            )

            stats_label.config(
                text="No files organized yet."
            )

            undo_button.config(
                state="disabled"
            )

            messagebox.showinfo(
                "Undo Complete",
                f"{restored_files} files restored successfully."
            )

        else:

            messagebox.showwarning(
                "Nothing to Undo",
                "There is no previous organization to undo."
            )

    except Exception as error:

        messagebox.showerror(
            "Error",
            f"Could not undo the organization:\n{error}"
        )


# -----------------------------
# Main Window
# -----------------------------

root = tk.Tk()

root.title("File Organizer")
root.geometry("700x650")
root.resizable(False, False)

root.configure(
    bg="#f4f6f8"
)


# -----------------------------
# Header
# -----------------------------

header = tk.Frame(
    root,
    bg="#1f2937",
    height=110
)

header.pack(
    fill="x"
)


title = tk.Label(
    header,
    text="📁 File Organizer",
    font=("Arial", 26, "bold"),
    fg="white",
    bg="#1f2937"
)

title.pack(
    pady=(20, 5)
)


subtitle = tk.Label(
    header,
    text="Organize your files automatically",
    font=("Arial", 11),
    fg="#d1d5db",
    bg="#1f2937"
)

subtitle.pack()


# -----------------------------
# Main Content
# -----------------------------

content = tk.Frame(
    root,
    bg="#f4f6f8"
)

content.pack(
    fill="both",
    expand=True
)


instruction = tk.Label(
    content,
    text="Select the folder you want to organize",
    font=("Arial", 13, "bold"),
    bg="#f4f6f8",
    fg="#1f2937"
)

instruction.pack(
    pady=(25, 15)
)


# Folder selection
folder_frame = tk.Frame(
    content,
    bg="#f4f6f8"
)

folder_frame.pack()


folder_entry = tk.Entry(
    folder_frame,
    width=48,
    font=("Arial", 11),
    relief="solid",
    bd=1
)

folder_entry.pack(
    side="left",
    ipady=8,
    padx=(0, 10)
)


browse_button = tk.Button(
    folder_frame,
    text="Browse",
    command=select_folder,
    font=("Arial", 11, "bold"),
    width=10,
    cursor="hand2"
)

browse_button.pack(
    side="left",
    ipady=5
)


# Organize button
organize_button = tk.Button(
    content,
    text="ORGANIZE FILES",
    command=organize,
    font=("Arial", 12, "bold"),
    width=22,
    height=2,
    cursor="hand2"
)

organize_button.pack(
    pady=18
)


# -----------------------------
# Progress Bar
# -----------------------------

progress_label = tk.Label(
    content,
    text="Ready",
    font=("Arial", 10),
    bg="#f4f6f8",
    fg="#4b5563"
)

progress_label.pack(
    pady=(5, 5)
)


progress_bar = ttk.Progressbar(
    content,
    orient="horizontal",
    length=450,
    mode="determinate"
)

progress_bar.pack(
    pady=(0, 15)
)


# -----------------------------
# Undo Button
# -----------------------------

undo_button = tk.Button(
    content,
    text="↩ UNDO LAST ORGANIZATION",
    command=undo,
    font=("Arial", 11, "bold"),
    width=28,
    height=2,
    state="disabled",
    cursor="hand2"
)

undo_button.pack(
    pady=5
)


# -----------------------------
# Result
# -----------------------------

result_label = tk.Label(
    content,
    text="",
    font=("Arial", 12, "bold"),
    bg="#f4f6f8",
    fg="#166534"
)

result_label.pack(
    pady=8
)


# -----------------------------
# Statistics
# -----------------------------

statistics_title = tk.Label(
    content,
    text="File Statistics",
    font=("Arial", 13, "bold"),
    bg="#f4f6f8",
    fg="#1f2937"
)

statistics_title.pack(
    pady=(5, 5)
)


stats_label = tk.Label(
    content,
    text="No files organized yet.",
    font=("Arial", 10),
    bg="#f4f6f8",
    fg="#4b5563",
    justify="center"
)

stats_label.pack(
    pady=5
)


# Supported categories
info_label = tk.Label(
    content,
    text="Supported: Images • Documents • Videos • Audio • Archives • Code",
    font=("Arial", 9),
    bg="#f4f6f8",
    fg="#6b7280"
)

info_label.pack(
    pady=8
)


# -----------------------------
# Footer
# -----------------------------

footer = tk.Label(
    root,
    text="Python File Organization Utility",
    font=("Arial", 9),
    bg="#e5e7eb",
    fg="#4b5563"
)

footer.pack(
    fill="x",
    ipady=8
)


# Start application
root.mainloop()