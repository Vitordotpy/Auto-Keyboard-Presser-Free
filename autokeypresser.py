import keyboard
import threading
import time
import tkinter as tk

class AutoKeyboardPresser:
    def __init__(self):
        self.sequence = []
        self.running = False
        self.click_count = 0
        self.delay = 0.1  # Tempo padrão entre os cliques (em segundos)
        self.root = tk.Tk()
        self.root.title("Auto Keyboard Presser")
        
        self.config_button = tk.Button(self.root, text="Configurar Teclas", command=self.configure_keys, font=("Arial", 12), bg="black", fg="white", highlightcolor="gray", activebackground="gray", activeforeground="white", borderwidth=2)
        self.config_button.pack(pady=8)
        
        self.save_button = tk.Button(self.root, text="Salvar", command=self.save_sequence, state=tk.DISABLED, font=("Arial", 12), bg="black", fg="white", highlightcolor="gray", activebackground="gray", activeforeground="white", borderwidth=2)
        self.save_button.pack(pady=8)
        
        self.start_button = tk.Button(self.root, text="Iniciar", command=self.start_pressing, font=("Arial", 12), bg="black", fg="white", highlightcolor="gray", activebackground="gray", activeforeground="white", borderwidth=2)
        self.start_button.pack(pady=8)
        
        self.stop_button = tk.Button(self.root, text="Parar", command=self.stop_pressing, font=("Arial", 12), bg="black", fg="white", highlightcolor="gray", activebackground="gray", activeforeground="white", borderwidth=2)
        self.stop_button.pack(pady=8)
        
        self.info_label = tk.Label(self.root, text="Teclas selecionadas: ", font=("Arial", 12))
        self.info_label.pack(pady=8)
        
        self.click_count_label = tk.Label(self.root, text="Contador de cliques: 0", font=("Arial", 12))
        self.click_count_label.pack(pady=8)
        
        self.delay_label = tk.Label(self.root, text="Tempo entre os cliques (em segundos):", font=("Arial", 12))
        self.delay_label.pack(pady=8)
        
        self.delay_entry = tk.Entry(self.root)
        self.delay_entry.pack(pady=8)
        
    def configure_keys(self):
        if self.running:
            return
        keyboard.on_press(self.record_sequence)
        self.config_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)
        
    def record_sequence(self, event):
        self.sequence.append(event.name)
        self.info_label.config(text="Teclas selecionadas: {}".format(", ".join(self.sequence)))
        
    def save_sequence(self):
        keyboard.unhook_all()
        self.config_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)
        
    def press_keys(self):
        while self.running:
            for key in self.sequence:
                if not self.running:
                    break
                keyboard.press_and_release(key)
                self.click_count += 1
                self.click_count_label.config(text="Contador de cliques: {}".format(self.click_count))
                time.sleep(self.delay)
        
    def start_pressing(self):
        if self.running:
            return
        if self.delay_entry.get() != "":
            try:
                self.delay = float(self.delay_entry.get())
            except ValueError:
                tk.messagebox.showerror("Erro", "Por favor, insira um valor numérico para o tempo entre os cliques.")
                return
        self.running = True
        self.delay_entry.config(state=tk.DISABLED)
        self.press_thread = threading.Thread(target=self.press_keys)
        self.press_thread.start()
        
    def stop_pressing(self):
        self.running = False
        self.sequence = []
        self.info_label.config(text="Teclas selecionadas: ")
        self.click_count = 0
        self.click_count_label.config(text="Contador de cliques: 0")
        self.delay_entry.config(state=tk.NORMAL)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AutoKeyboardPresser()
    app.run()
