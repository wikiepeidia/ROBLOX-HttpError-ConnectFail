import tkinter as tk
from tkinter import simpledialog

class ErrorDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Failed to download or apply critical settings, please check your internet connection. Error info: HttpError: ConnectFail").grid(row=0)
        return None # initial focus

    def buttonbox(self):
        box = tk.Frame(self)

        tk.Button(box, text="Retry", command=self.retry, default=tk.ACTIVE).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(box, text="Cancel", command=self.cancel).pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.retry)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def retry(self, event=None):
        self.show_error()
        self.destroy()

    def cancel(self, event=None):
        self.destroy()

    def show_error(self):
        ErrorDialog(root)

root = tk.Tk()
root.withdraw()  # Hide the main window

ErrorDialog(root)

root.mainloop()