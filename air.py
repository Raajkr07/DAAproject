import tkinter as tk
from tkinter import messagebox, scrolledtext
import heapq

def dijkstra(graph, start, end):
    queue = [(0, start, [])]
    visited = set()
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]
        if node == end:
            return path, cost
        for (adj, weight) in graph.get(node, []):
            if adj not in visited:
                heapq.heappush(queue, (cost + weight, adj, path))
    return None, float('inf')

class AirRoutePlannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(" Air Route Planner with Dijkstra's Algorithm")
        self.root.geometry("800x700")
        self.root.config(bg="#e6f2ff")

        self.airports = []
        self.routes = []

        style = {"bg": "#ffffff", "padx": 10, "pady": 10, "bd": 2, "relief": "ridge"}

        # Title
        tk.Label(root, text=" Air Route Planner", font=("Helvetica", 20, "bold"), bg="#e6f2ff", fg="#004080").pack(pady=10)

        # --- Airports Frame ---
        frame_airports = tk.LabelFrame(root, text="Airports", font=("Arial", 12, "bold"), fg="#004080", **style)
        frame_airports.pack(padx=10, pady=5, fill="x")

        tk.Label(frame_airports, text="Airport Code:", font=("Arial", 10), bg="#ffffff").grid(row=0, column=0, sticky="w")
        self.entry_airport = tk.Entry(frame_airports)
        self.entry_airport.grid(row=0, column=1)
        self.add_button("Add", self.add_airport, frame_airports).grid(row=0, column=2, padx=5)

        self.airports_listbox = tk.Listbox(frame_airports, height=5, font=("Courier", 10))
        self.airports_listbox.grid(row=1, column=0, columnspan=3, pady=5, sticky="we")
        self.add_button("Remove Selected", self.remove_airport, frame_airports).grid(row=2, column=0, columnspan=3, pady=5)

        # --- Routes Frame ---
        frame_routes = tk.LabelFrame(root, text="Routes", font=("Arial", 12, "bold"), fg="#004080", **style)
        frame_routes.pack(padx=10, pady=5, fill="x")

        labels = ["Source:", "Destination:", "Distance (km):"]
        for i, text in enumerate(labels):
            tk.Label(frame_routes, text=text, font=("Arial", 10), bg="#ffffff").grid(row=0, column=i * 2)

        self.entry_source = tk.Entry(frame_routes, width=10)
        self.entry_destination = tk.Entry(frame_routes, width=10)
        self.entry_distance = tk.Entry(frame_routes, width=10)

        self.entry_source.grid(row=0, column=1)
        self.entry_destination.grid(row=0, column=3)
        self.entry_distance.grid(row=0, column=5)
        self.add_button("Add Route", self.add_route, frame_routes).grid(row=0, column=6, padx=5)

        self.routes_listbox = tk.Listbox(frame_routes, height=5, width=90, font=("Courier", 10))
        self.routes_listbox.grid(row=1, column=0, columnspan=7, pady=5)

        self.add_button("Remove Selected", self.remove_route, frame_routes).grid(row=2, column=0, columnspan=7)
        self.add_button("Load Indian City Routes", self.load_indian_routes, frame_routes).grid(row=3, column=0, columnspan=7, pady=5)

        # --- Shortest Path Frame ---
        frame_path = tk.LabelFrame(root, text="Shortest Path", font=("Arial", 12, "bold"), fg="#004080", **style)
        frame_path.pack(padx=10, pady=5, fill="both", expand=True)

        tk.Label(frame_path, text="From:", bg="#ffffff").grid(row=0, column=0, sticky="e")
        self.entry_start = tk.Entry(frame_path, width=10)
        self.entry_start.grid(row=0, column=1)

        tk.Label(frame_path, text="To:", bg="#ffffff").grid(row=0, column=2, sticky="e")
        self.entry_end = tk.Entry(frame_path, width=10)
        self.entry_end.grid(row=0, column=3)

        self.add_button("Find Shortest Path", self.find_shortest_path, frame_path).grid(row=0, column=4, padx=5)

        self.result_text = scrolledtext.ScrolledText(frame_path, width=85, height=10, state="disabled", font=("Arial", 10))
        self.result_text.grid(row=1, column=0, columnspan=5, pady=10)

    def add_button(self, text, command, parent):
        btn = tk.Button(parent, text=text, command=command, bg="#007acc", fg="white", font=("Arial", 10, "bold"))
        btn.bind("<Enter>", lambda e: btn.config(bg="#005f99"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#007acc"))
        return btn

    def add_airport(self):
        airport = self.entry_airport.get().strip().upper()
        if airport and airport not in self.airports:
            self.airports.append(airport)
            self.airports_listbox.insert(tk.END, airport)
        else:
            messagebox.showwarning("Warning", "Invalid or duplicate airport.")
        self.entry_airport.delete(0, tk.END)

    def remove_airport(self):
        selected = self.airports_listbox.curselection()
        if not selected: return
        idx = selected[0]
        airport = self.airports_listbox.get(idx)
        self.airports_listbox.delete(idx)
        if airport in self.airports:
            self.airports.remove(airport)
        self.routes = [r for r in self.routes if r[0] != airport and r[1] != airport]
        self.refresh_routes_list()

    def add_route(self):
        src = self.entry_source.get().strip().upper()
        dst = self.entry_destination.get().strip().upper()
        try:
            dist = float(self.entry_distance.get().strip())
        except ValueError:
            messagebox.showwarning("Warning", "Distance must be a number.")
            return
        if src and dst and src != dst:
            self.routes.append((src, dst, dist))
            self.routes_listbox.insert(tk.END, f"{src} <-> {dst} | {dist} km")
            for airport in (src, dst):
                if airport not in self.airports:
                    self.airports.append(airport)
                    self.airports_listbox.insert(tk.END, airport)
        self.entry_source.delete(0, tk.END)
        self.entry_destination.delete(0, tk.END)
        self.entry_distance.delete(0, tk.END)

    def remove_route(self):
        selected = self.routes_listbox.curselection()
        if selected:
            idx = selected[0]
            del self.routes[idx]
            self.refresh_routes_list()

    def refresh_routes_list(self):
        self.routes_listbox.delete(0, tk.END)
        for r in self.routes:
            self.routes_listbox.insert(tk.END, f"{r[0]} <-> {r[1]} | {r[2]} km")

    def find_shortest_path(self):
        start = self.entry_start.get().strip().upper()
        end = self.entry_end.get().strip().upper()
        if start not in self.airports or end not in self.airports:
            messagebox.showerror("Error", "Invalid start or end airport.")
            return
        graph = {a: [] for a in self.airports}
        for u, v, w in self.routes:
            graph[u].append((v, w))
            graph[v].append((u, w))
        path, total = dijkstra(graph, start, end)
        result = f"📍 Shortest Path from {start} to {end}:\n"
        if path:
            result += " ➡️ ".join(path) + f"\n🧭 Total Distance: {total} km"
        else:
            result += "No path found."
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, result)
        self.result_text.configure(state="disabled")

    def load_indian_routes(self):
        self.airports = ["DEL", "MUM", "BLR", "CHN", "HYD", "KOL"]
        self.routes = [
            ("DEL", "MUM", 1414), ("DEL", "BLR", 2150), ("DEL", "CHN", 2180),
            ("DEL", "HYD", 1570), ("DEL", "KOL", 1530), ("MUM", "BLR", 984),
            ("MUM", "CHN", 1338), ("MUM", "HYD", 709), ("MUM", "KOL", 1961),
            ("BLR", "CHN", 346), ("BLR", "HYD", 570), ("BLR", "KOL", 1871),
            ("CHN", "HYD", 627), ("CHN", "KOL", 1660), ("HYD", "KOL", 1496)
        ]
        self.airports_listbox.delete(0, tk.END)
        for airport in self.airports:
            self.airports_listbox.insert(tk.END, airport)
        self.refresh_routes_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = AirRoutePlannerGUI(root)
    root.mainloop()
