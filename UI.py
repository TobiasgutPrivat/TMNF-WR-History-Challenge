import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from WRHistoryChallenge import WRHistoryChallenge
from WRImprovement import format_time

class WRHistoryChallengeUI:
    def __init__(self, root, wr_history_challenge: WRHistoryChallenge):
        self.root = root
        self.wr_history_challenge = wr_history_challenge
        self.root.title("WR History Challenge")

        # Create a Style for ttkbootstrap
        self.style = Style(theme="darkly")
        
        # Create the main frame
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.pack(fill="both", expand=True)

        # Skipped WR Improvements Section
        self.skipped_frame = ttk.LabelFrame(self.frame, text="Skipped WR Improvements", padding=10)
        self.skipped_frame.pack(fill="x", padx=10, pady=10)

        self.skipped_listbox = tk.Listbox(self.skipped_frame, height=6, width=50)
        self.skipped_listbox.pack(side="left", fill="y")

        self.scrollbar = ttk.Scrollbar(self.skipped_frame, orient="vertical", command=self.skipped_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.skipped_listbox.config(yscrollcommand=self.scrollbar.set)

        # Selected WR Improvement Section
        self.selected_frame = ttk.LabelFrame(self.frame, text="Selected WR Improvement", padding=10)
        self.selected_frame.pack(fill="x", padx=10, pady=10)

        self.selected_label = ttk.Label(self.selected_frame, text="", anchor="w")
        self.selected_label.pack(fill="x")

        self.set_pb_button = ttk.Button(self.selected_frame, text="Reload PBs", command=self.LoadCurrentPBs)
        self.set_pb_button.pack(fill="x", pady=5)

        self.play_button = ttk.Button(self.selected_frame, text="Play against Ghost", command=self.play_selected)
        self.play_button.pack(fill="x", pady=5)

        self.next_button = ttk.Button(self.selected_frame, text="Next", command=self.select_next_unbeaten)
        self.next_button.pack(fill="x", pady=5)

        # Next Unbeaten WR Improvements Section
        self.next_frame = ttk.LabelFrame(self.frame, text="Next Unbeaten WR Improvements", padding=10)
        self.next_frame.pack(fill="x", padx=10, pady=10)

        self.next_listbox = tk.Listbox(self.next_frame, height=6, width=50)
        self.next_listbox.pack(side="left", fill="y")

        self.next_scrollbar = ttk.Scrollbar(self.next_frame, orient="vertical", command=self.next_listbox.yview)
        self.next_scrollbar.pack(side="right", fill="y")
        self.next_listbox.config(yscrollcommand=self.next_scrollbar.set)

        # Navigation for selecting the WR Improvement index
        self.index_label = ttk.Label(self.frame, text="Select WR Improvement Index")
        self.index_label.pack(pady=10)

        self.index_entry = ttk.Entry(self.frame)
        self.index_entry.pack(fill="x")
        self.index_entry.bind("<Return>", self.on_index_change)

        # Initialize UI with current state
        self.update_ui()

    def update_ui(self):
        # Skipped WR Improvements
        skipped_wr = self.wr_history_challenge.GetSkippedWRImprovements()
        self.skipped_listbox.delete(0, tk.END)
        for improvement in skipped_wr:
            self.skipped_listbox.insert(tk.END, f"{improvement.track_name} - {format_time(improvement.replay_time)} - {improvement.user_name}")

        # Selected WR Improvement
        track_name, user_name, replay_time, pb_time = self.wr_history_challenge.getSelectedWRImprovementInfo()
        self.selected_label.config(text=f"Track: {track_name}\nUser: {user_name}\nTime: {replay_time}\nCurrent PB: {pb_time if pb_time else 'None'}")

        # Next Unbeaten WR Improvements
        next_wrs = self.wr_history_challenge.GetNextUnbeatenWRImprovements()
        self.next_listbox.delete(0, tk.END)
        for next_wr in next_wrs:
            if next_wr:
                self.next_listbox.insert(tk.END, f"{next_wr.track_name} - {format_time(next_wr.replay_time)} - {next_wr.user_name}")

    def play_selected(self):
        self.wr_history_challenge.playSelectedWRImprovement()

    def select_next_unbeaten(self):
        self.wr_history_challenge.selectNextUnbeatenWRImprovement()
        self.update_ui()

    def LoadCurrentPBs(self):
        self.wr_history_challenge.LoadCurrentPBs()
        self.update_ui()

    def on_index_change(self, event):
        try:
            index = int(self.index_entry.get())
            if 0 <= index < len(self.wr_history_challenge.WRImprovements):
                self.wr_history_challenge.selectedWRImprovementIndex = index
                self.update_ui()
            else:
                self.show_error("Index out of range")
        except ValueError:
            self.show_error("Invalid index")

    def show_error(self, message):
        error_window = tk.Toplevel(self.root)
        error_window.title("Error")
        ttk.Label(error_window, text=message).pack(padx=10, pady=10)
        ttk.Button(error_window, text="OK", command=error_window.destroy).pack(pady=10)