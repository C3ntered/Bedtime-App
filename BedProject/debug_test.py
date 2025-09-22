import tkinter as tk
from tkinter import messagebox

class SimpleTest:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Debug Test")
        self.root.geometry("400x300")
        self.root.configure(bg="red")
        
        # Main container
        self.container = tk.Frame(self.root, bg="blue")
        self.container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.show_page1()
        
    def clear_container(self):
        print("Clearing container...")
        for widget in self.container.winfo_children():
            print(f"Destroying: {widget}")
            widget.destroy()
            
    def show_page1(self):
        print("Showing page 1")
        self.clear_container()
        
        label = tk.Label(self.container, text="PAGE 1", font=("Arial", 24), bg="yellow")
        label.pack(pady=50)
        
        button = tk.Button(self.container, text="Go to Page 2", command=self.show_page2)
        button.pack()
        
    def show_page2(self):
        print("Showing page 2")
        self.clear_container()
        
        label = tk.Label(self.container, text="PAGE 2", font=("Arial", 24), bg="green")
        label.pack(pady=50)
        
        button = tk.Button(self.container, text="Back to Page 1", command=self.show_page1)
        button.pack()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SimpleTest()
    app.run()