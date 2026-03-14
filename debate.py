import tkinter as tk
from tkinter import ttk
import ollama
import threading
import time
import random
import math

MODEL = "smollm2:1.7b"

class RealtimeCollisionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CONVICTION ENGINE: ASYNC INTERRUPT")
        self.root.geometry("1400x900")
        self.root.configure(bg="#050505")
        
        # Shared State
        self.current_context = "The universe is a cold, mathematical accident."
        self.interrupt_event = threading.Event()
        self.active_speaker = None
        
        # Agent States
        self.elias = {"hr": 72, "anger": 10, "pos": 400, "mood": "neutral", "color": "#3498db"}
        self.maya = {"hr": 70, "anger": 10, "pos": 1000, "mood": "neutral", "color": "#e74c3c"}
        
        self.setup_ui()
        self.animate_loop()
        
        # Start the "Director" thread
        threading.Thread(target=self.director, daemon=True).start()

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, bg="#0a0a0a", height=300, highlightthickness=0)
        self.canvas.pack(fill=tk.X, pady=10)

        self.pane = tk.Frame(self.root, bg="#050505")
        self.pane.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.elias_ui = self.create_box(self.pane, "ELIAS", self.elias["color"], tk.LEFT)
        self.maya_ui = self.create_box(self.pane, "MAYA", self.maya["color"], tk.RIGHT)

    def create_box(self, parent, name, color, side):
        frame = tk.Frame(parent, bg="#111", borderwidth=1, relief=tk.FLAT)
        frame.pack(side=side, fill=tk.BOTH, expand=True, padx=10)
        tk.Label(frame, text=name, bg="#111", fg=color, font=("Arial", 12, "bold")).pack(pady=5)
        text_area = tk.Text(frame, bg="#000", fg="#eee", font=("Consolas", 12), height=15, wrap=tk.WORD, state='disabled', padx=15, pady=15)
        text_area.pack(expand=True, fill=tk.BOTH)
        return {"text": text_area, "name": name}

    def draw_human(self, x, state, color, flipped=False):
        c, t = self.canvas, time.time()
        # Breathing/Sway
        b, s = math.sin(t*2)*2, math.cos(t*1.5)*3
        hx, hy = x + s, 80 + b
        
        # Face
        c.create_oval(hx-20, hy-20, hx+20, hy+20, outline=color, width=2)
        # Mouth
        if state["mood"] == "talking":
            m = abs(math.sin(t*18))*10
            c.create_oval(hx-5, hy+5, hx+5, hy+5+m, outline=color)
        elif state["mood"] == "stunned":
            c.create_oval(hx-3, hy+8, hx+3, hy+12, outline=color) # Small 'o'
        else:
            c.create_line(hx-7, hy+10, hx+7, hy+10, fill=color)

        # Body/Limbs
        ny, wy = hy+20, hy+80
        c.create_line(hx, ny, x, wy, fill=color, width=3)
        # Arms - throw up if stunned
        ang = math.radians(140 if state["mood"]=="talking" else (40 if state["mood"]=="stunned" else 0))
        hax = x - (math.cos(ang)*40 if not flipped else -math.cos(ang)*40)
        hay = ny + 20 + math.sin(ang)*40
        c.create_line(hx, ny+10, hax, hay, fill=color, width=2)

    def animate_loop(self):
        self.canvas.delete("all")
        self.draw_human(self.elias["pos"], self.elias, self.elias["color"])
        self.draw_human(self.maya["pos"], self.maya, self.maya["color"], True)
        self.root.after(30, self.animate_loop)

    def stream_text(self, agent_ui, agent_state, text):
        agent_ui["text"].config(state='normal')
        agent_ui["text"].insert(tk.END, "\n")
        
        words = text.split()
        for word in words:
            if self.interrupt_event.is_set():
                agent_ui["text"].insert(tk.END, "... [CUT OFF]", "meta")
                agent_state["mood"] = "stunned"
                break
            
            agent_ui["text"].insert(tk.END, word + " ")
            agent_ui["text"].see(tk.END)
            # Typing speed jitter
            time.sleep(random.uniform(0.08, 0.2))
        
        agent_ui["text"].config(state='disabled')

    def director(self):
        # The logic that forces the "Real Human" vibe
        while True:
            # Pick speaker based on context or randomness
            speaker_ui = self.elias_ui if random.random() > 0.5 else self.maya_ui
            speaker_state = self.elias if speaker_ui == self.elias_ui else self.maya
            other_state = self.maya if speaker_ui == self.elias_ui else self.elias
            
            self.interrupt_event.clear()
            speaker_state["mood"] = "talking"
            other_state["mood"] = "neutral"
            
            # Generate response
            persona = "Grumpy surgeon, materialist, short sentences." if speaker_ui == self.elias_ui else "Spiritual mother, sharp, uses 'u' and 'rly'."
            res = ollama.chat(model=MODEL, messages=[
                {"role": "system", "content": f"ACT AS {persona} Max 12 words. Be blunt."},
                {"role": "user", "content": self.current_context}
            ])
            
            text = res['message']['content'].strip()
            self.current_context = text
            
            # Start streaming in a way that can be interrupted
            self.stream_text(speaker_ui, speaker_state, text)
            
            speaker_state["mood"] = "neutral"
            time.sleep(random.uniform(1, 2))

if __name__ == "__main__":
    root = tk.Tk()
    app = RealtimeCollisionGUI(root)
    root.mainloop()