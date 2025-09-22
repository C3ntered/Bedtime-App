import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
import os
from datetime import datetime

class BedtimeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bedtime Routine")
        self.root.geometry("600x700")
        self.root.configure(bg="#2c3e50")
        
        # Data file for journal entries
        self.data_file = "bedtime_journal.json"
        
        # Timer variables
        self.timer_running = False
        self.timer_seconds = 0
        
        # Checklist setup
        self.tasks = {
            "Tooth Paste": tk.BooleanVar(),
            "Tooth Brush": tk.BooleanVar(), 
            "Floss": tk.BooleanVar(),
            "Face Wash": tk.BooleanVar(),
            "Pajamas": tk.BooleanVar()
        }
        
        # Create main container
        self.main_frame = tk.Frame(self.root, bg="#2c3e50")
        self.main_frame.pack(fill="both", expand=True)
        
        # Start with checklist
        self.show_checklist()
        
    def clear_main_frame(self):
        """Remove all widgets from the main frame"""
        print("CLEARING MAIN FRAME")
        for widget in self.main_frame.winfo_children():
            print(f"Destroying widget: {widget}")
            widget.destroy()
        print("MAIN FRAME CLEARED")
        
    def show_checklist(self):
        self.clear_main_frame()
        
        # Create content frame
        content_frame = tk.Frame(self.main_frame, bg="#34495e", pady=20)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(content_frame, text="Bedtime Checklist", 
                              font=("Arial", 24, "bold"), fg="#ecf0f1", bg="#34495e")
        title_label.pack(pady=20)
        
        # Checkboxes
        for task, var in self.tasks.items():
            checkbox = tk.Checkbutton(content_frame, text=task, variable=var,
                                    font=("Arial", 14), fg="#ecf0f1", bg="#34495e",
                                    selectcolor="#3498db", activebackground="#34495e")
            checkbox.pack(pady=5, anchor="w", padx=50)

        # Next button
        next_button = tk.Button(content_frame, text="Start Timer", 
                               command=self.check_items, font=("Arial", 14, "bold"),
                               bg="#27ae60", fg="white", pady=10, padx=30,
                               relief="flat", cursor="hand2")
        next_button.pack(pady=30)
        
    def check_items(self):
        print("CHECKING ITEMS...")
        if all(var.get() for var in self.tasks.values()):
            print("ALL ITEMS CHECKED - SHOWING TIMER")
            self.show_timer()
        else:
            print("NOT ALL ITEMS CHECKED")
            messagebox.showinfo("Incomplete", "Please complete all checklist items first!")
            
    def show_timer(self):
        print("SHOWING TIMER PAGE")
        self.clear_main_frame()
        
        # Create content frame
        content_frame = tk.Frame(self.main_frame, bg="#34495e", pady=20)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        print("TIMER CONTENT FRAME CREATED AND PACKED")
        
        # Title
        title_label = tk.Label(content_frame, text="Brush Your Teeth!", 
                              font=("Arial", 24, "bold"), fg="#ecf0f1", bg="#34495e")
        title_label.pack(pady=20)
        
        # Timer display
        self.timer_label = tk.Label(content_frame, text="02:00", 
                                   font=("Arial", 48, "bold"), fg="#e74c3c", bg="#34495e")
        self.timer_label.pack(pady=30)
        
        # Button frame
        button_frame = tk.Frame(content_frame, bg="#34495e")
        button_frame.pack(pady=20)
        
        # Start button
        self.start_button = tk.Button(button_frame, text="Start Timer", 
                                     command=self.start_timer, font=("Arial", 14, "bold"),
                                     bg="#3498db", fg="white", pady=10, padx=20,
                                     relief="flat", cursor="hand2")
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        # Reset button
        self.reset_button = tk.Button(button_frame, text="Reset", 
                                     command=self.reset_timer, font=("Arial", 14),
                                     bg="#95a5a6", fg="white", pady=10, padx=20,
                                     relief="flat", cursor="hand2")
        self.reset_button.pack(side=tk.LEFT, padx=10)

    def start_timer(self):
        if not self.timer_running:
            self.timer_seconds = 120  # 2 minutes
            self.timer_running = True
            self.start_button.config(text="Running...", state="disabled")
            self.countdown()
            
    def countdown(self):
        if self.timer_running and self.timer_seconds > 0:
            minutes, secs = divmod(self.timer_seconds, 60)
            self.timer_label.config(text=f"{minutes:02d}:{secs:02d}")
            self.timer_seconds -= 1
            self.root.after(1000, self.countdown)
        elif self.timer_seconds <= 0:
            self.timer_label.config(text="Time's Up!", fg="#27ae60")
            self.timer_running = False
            self.start_button.config(text="Continue to Journal", state="normal", 
                                   bg="#27ae60", command=self.show_journal)
            
    def reset_timer(self):
        self.timer_running = False
        self.timer_seconds = 120
        self.timer_label.config(text="02:00", fg="#e74c3c")
        self.start_button.config(text="Start Timer", state="normal", 
                               bg="#3498db", command=self.start_timer)
        
    def show_journal(self):
        self.clear_main_frame()
        
        # Create scrollable content
        canvas = tk.Canvas(self.main_frame, bg="#34495e")
        scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#34495e")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda _: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        # Title
        title_label = tk.Label(scrollable_frame, text="Evening Reflection", 
                              font=("Arial", 24, "bold"), fg="#ecf0f1", bg="#34495e")
        title_label.pack(pady=20)
        
        # Questions
        questions = [
            "How did your day go overall?",
            "What are you grateful for today?",
            "What's one thing you want to improve tomorrow?",
            "How are you feeling right now?"
        ]
        
        self.answers = {}
        
        for question in questions:
            q_label = tk.Label(scrollable_frame, text=question, 
                              font=("Arial", 12, "bold"), fg="#ecf0f1", bg="#34495e")
            q_label.pack(pady=(20, 5), anchor="w")
            
            text_widget = tk.Text(scrollable_frame, height=3, width=60, 
                                 font=("Arial", 11), wrap=tk.WORD)
            text_widget.pack(pady=(0, 10), padx=20)
            self.answers[question] = text_widget
            
        # Save button
        save_button = tk.Button(scrollable_frame, text="Save & Complete", 
                               command=self.save_journal, font=("Arial", 14, "bold"),
                               bg="#8e44ad", fg="white", pady=10, padx=30,
                               relief="flat", cursor="hand2")
        save_button.pack(pady=20)
        
    def save_journal(self):
        # Collect answers
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "answers": {}
        }
        
        for question, text_widget in self.answers.items():
            entry["answers"][question] = text_widget.get("1.0", tk.END).strip()
            
        # Load existing data
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
            else:
                data = []
        except:
            data = []
            
        # Add new entry
        data.append(entry)
        
        # Save data
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("Success", "Journal entry saved! Sweet dreams! 🌙")
            self.root.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
            
    def run(self):
        self.root.mainloop()

# Create and run the app
if __name__ == "__main__":
    app = BedtimeApp()
    app.run()