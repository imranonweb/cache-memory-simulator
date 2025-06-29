import tkinter as tk
from tkinter import ttk

def simulate_cache(input_data, slots, policy):
    cache = []                    
    hits = 0                      
    misses = 0                    
    time = 0                      
    timestamps = {}              

    result_log = []              
    cache_snapshots = []         
    hit_miss_info = []           

    for value in input_data:
        time += 1                

        if value in cache:
            hits += 1
            result_log.append(f"{value} → HIT")
            hit_miss_info.append("HIT")

            if policy == "LRU":
                timestamps[value] = time
        else:
            misses += 1
            result_log.append(f"{value} → MISS")
            hit_miss_info.append("MISS")

            if len(cache) < slots:
                cache.append(value)
            else:
                if policy == "FIFO":
                    cache.pop(0)
                elif policy == "LRU":
                    lru = min(timestamps, key=timestamps.get)
                    cache.remove(lru)
                    timestamps.pop(lru)
                cache.append(value)

            if policy == "LRU":
                timestamps[value] = time

        cache_snapshots.append(list(cache))

    total = hits + misses
    ratio = round((hits / total) * 100, 2) if total > 0 else 0

    return hits, misses, ratio, result_log, cache_snapshots, hit_miss_info

class CacheSimGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CacheCraft: Cache Memory Simulator")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f4f7")

        self.data_var = tk.StringVar()
        self.slots_var = tk.IntVar(value=4)
        self.policy_var = tk.StringVar(value="FIFO")

        self.build_widgets()
        self.build_canvas()

    def build_widgets(self):
        title_label = tk.Label(
            self.root,
            text="🧠 CacheCraft: Cache Memory Simulator",
            font=("Segoe UI", 22, "bold"),
            bg="#f0f4f7",
            fg="#2c3e50"
        )
        title_label.pack(pady=(20, 10))

        frame = tk.Frame(self.root, bg="#f0f4f7")
        frame.pack(pady=10)

        tk.Label(frame, text="Enter numbers (space-separated):", bg="#f0f4f7", font=("Arial", 11)).grid(row=0, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.data_var, width=50, font=("Arial", 11)).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Number of slots:", bg="#f0f4f7", font=("Arial", 11)).grid(row=1, column=0, sticky="w")
        tk.Scale(
            frame,
            from_=1,
            to=10,
            orient="horizontal",
            variable=self.slots_var,
            length=200,
            sliderlength=30,
            troughcolor="skyblue",
            bd=0,
            highlightthickness=0
        ).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(frame, text="Replacement Policy:", bg="#f0f4f7", font=("Arial", 11)).grid(row=2, column=0, sticky="w")
        ttk.Combobox(frame, textvariable=self.policy_var, values=["FIFO", "LRU"], width=10, font=("Arial", 10)).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Button(
            self.root,
            text="Simulate",
            bg="#4caf50",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.run_simulation
        ).pack(pady=10)

        tk.Label(self.root, text="Simulation Output:", bg="#f0f4f7", font=("Arial", 12, "bold")).pack()
        self.result_text = tk.Text(self.root, height=10, width=100, bg="#ffffff", fg="#333", font=("Consolas", 11))
        self.result_text.pack(pady=10)

    def build_canvas(self):
        self.canvas_frame = tk.LabelFrame(self.root, text="Cache Visualization", bg="#f0f4f7", font=("Arial", 12, "bold"))
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

        canvas_container = tk.Frame(self.canvas_frame, bg="#f0f4f7")
        canvas_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_container, bg="white", height=350)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scroll_y = tk.Scrollbar(canvas_container, orient="vertical", command=self.canvas.yview)
        self.scroll_y.grid(row=0, column=1, sticky="ns")

        self.scroll_x = tk.Scrollbar(canvas_container, orient="horizontal", command=self.canvas.xview)
        self.scroll_x.grid(row=1, column=0, sticky="ew")

        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        canvas_container.rowconfigure(0, weight=1)
        canvas_container.columnconfigure(0, weight=1)

    def draw_cache(self):
        self.canvas.delete("all")
        box_width = 60
        box_height = 30
        padding_x = 10
        padding_y = 10
        spacing_x = box_width + 20

        max_height = max(len(snap) for snap in self.cache_snapshots)

        for step, snapshot in enumerate(self.cache_snapshots):
            color = "#c8facc" if self.hit_miss_info[step] == "HIT" else "#ffcccc"
            for i, val in enumerate(snapshot):
                x0 = padding_x + step * spacing_x
                y0 = padding_y + i * (box_height + 10)
                x1 = x0 + box_width
                y1 = y0 + box_height

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#555", width=2)
                self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=str(val), font=("Arial", 11, "bold"))

            label = "H" if self.hit_miss_info[step] == "HIT" else "M"
            self.canvas.create_text(
                padding_x + step * spacing_x + box_width / 2,
                padding_y + max_height * (box_height + 10) + 15,
                text=label,
                font=("Arial", 11, "bold"),
                fill="#2e2e2e"
            )

        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def run_simulation(self):
        self.result_text.delete(1.0, tk.END)
        try:
            input_data = list(map(int, self.data_var.get().strip().split()))
            slots = self.slots_var.get()
            policy = self.policy_var.get()

            self.hits, self.misses, self.ratio, self.log, self.cache_snapshots, self.hit_miss_info = simulate_cache(
                input_data, slots, policy)

            for line in self.log:
                self.result_text.insert(tk.END, line + "\n")

            summary = f"\nTotal Hits: {self.hits}\nTotal Misses: {self.misses}\nHit Ratio: {self.ratio}%"
            self.result_text.insert(tk.END, summary + "\n")

            self.draw_cache()

        except Exception as e:
            self.result_text.insert(tk.END, f"Error: {str(e)}")

if __name__ == '__main__':
    root = tk.Tk()
    app = CacheSimGUI(root)
    root.mainloop()
