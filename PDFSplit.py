from PyPDF2 import PdfReader, PdfWriter
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import re

# set the background color
bg_color = "#2c3e50"
# set the foreground color
fg_color = "#ecf0f1"
# set the accent color
accent_color = "#3498db"


def select_file():
    global file_path
    file_path = filedialog.askopenfilename()


def split_pdf():
    pdf = PdfReader(file_path)
    num_pages = len(pdf.pages)
    page_counter = 0
    input_dir = os.path.dirname(file_path)
    output_dir = os.path.join(input_dir, os.path.splitext(
        os.path.basename(file_path))[0] + "_Students")
    os.makedirs(output_dir, exist_ok=True)
    page_list = []

    progress_bar['maximum'] = num_pages

    for page_num in reversed(range(0, num_pages)):

        page = pdf.pages[page_num]
        text = page.extract_text()
        # temp array for reversing pages later
        page_list.insert(0, page)

        if "DO NOT MARK" in text:
            writer = PdfWriter()
            for x in page_list:
                writer.add_page(x)
            first_line = text.split("\n")[0]
            # extract student ID number from first line of text
            match = re.search(r"\((\d+)\)", first_line)
            output_file_name = match.group(1) + ".pdf"
            output_file_path = os.path.join(output_dir, output_file_name)
            with open(output_file_path, 'wb') as out:
                writer.write(out)
            page_list = []

        page_counter += 1
        progress_bar['value'] = page_counter
        root.update_idletasks()

    # show a message box when the process is complete
    tk.messagebox.showinfo(
        "PDF Splitter", "The PDF has been split into multiple files.")


# create a GUI window
root = tk.Tk()
root.title("PDF Splitter")
root.geometry("500x300")
root.resizable(False, False)
root.config(bg=bg_color)

# create a label for the input file
input_label = tk.Label(root, text="Select a PDF file:", font=(
    "Helvetica", 12), bg=bg_color, fg=fg_color)
input_label.pack(pady=10)

# create a button to select the input file
select_button = tk.Button(root, text="Select", font=(
    "Helvetica", 12), bg=accent_color, fg=fg_color, command=select_file)
select_button.pack(pady=10)

# create a progress bar
progress_bar = ttk.Progressbar(
    root, orient='horizontal', length=400, mode='determinate', value=0, maximum=100)
progress_bar.pack(pady=10)

# create a button to start the process
split_button = tk.Button(root, text="Split PDF", font=(
    "Helvetica", 14), bg=accent_color, fg=fg_color, command=split_pdf)
split_button.pack(pady=10)

# run the GUI loop
root.mainloop()
