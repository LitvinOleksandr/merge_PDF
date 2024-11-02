import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def merge_pdfs(pdf_list, output):
    pdf_writer = PyPDF2.PdfWriter()

    for pdf in pdf_list:
        pdf_reader = PyPDF2.PdfReader(pdf)
        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])

    with open(output, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

def select_files():
    files = filedialog.askopenfilenames(title="Выберите PDF файлы", filetypes=[("PDF files", "*.pdf")])
    return list(files)

def save_file():
    return filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

def show_selected_files(files):
    preview = tk.Toplevel()
    preview.title("Выбранные PDF файлы")
    for file in files:
        tk.Label(preview, text=file).pack()
    tk.Button(preview, text="ОК", command=preview.destroy).pack(pady=10)

def reorder_files(files):
    reordered_files = files[:]
    for i, file in enumerate(files):
        new_position = simpledialog.askinteger(
            "Порядок файлов",
            f"Текущая позиция файла '{file}' - {i + 1}. Введите новую позицию:",
            initialvalue=i + 1,
            minvalue=1,
            maxvalue=len(files)
        )
        if new_position is not None and 1 <= new_position <= len(files):
            # Перемещаем файл на новую позицию
            reordered_files.insert(new_position - 1, reordered_files.pop(i))
    return reordered_files

def merge_files():
    pdf_files = select_files()
    if pdf_files:
        pdf_files = reorder_files(pdf_files)  # Добавляем возможность поменять порядок
        output_file = save_file()
        if output_file:
            show_selected_files(pdf_files)
            merge_pdfs(pdf_files, output_file)
            messagebox.showinfo("Успех", f"PDF файлы успешно объединены в {output_file}")
        else:
            messagebox.showwarning("Предупреждение", "Вы не указали имя выходного файла.")
    else:
        messagebox.showwarning("Предупреждение", "Вы не выбрали файлы для объединения.")

def main():
    root = tk.Tk()
    root.title("Объединение PDF файлов")

    merge_button = tk.Button(root, text="Объединить PDF файлы", command=merge_files)
    merge_button.pack(pady=20)
    root.geometry("300x200")
    root.mainloop()

if __name__ == "__main__":
    main()
