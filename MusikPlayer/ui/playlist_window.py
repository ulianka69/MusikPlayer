import customtkinter as ctk
from tkinter import ttk


class PlaylistWindow(ctk.CTkToplevel):
    """Окно со списком всех треков (таблица)"""

    PRIMARY = "#ff4081"
    SECONDARY = "#7c4dff"
    BG_DARK = "#0f0c29"
    BG_SURFACE = "#1e1e2e"
    BG_CARD = "#28283c"
    TEXT = "#ffffff"
    TEXT_DIM = "#b0b0d0"

    def __init__(self, master, player_window):
        super().__init__(master)

        self.player_window = player_window
        self.title("📋 Список треков")
        self.geometry("900x600")
        self.configure(fg_color=self.BG_DARK)

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        # ===== ВЕРХНЯЯ ПАНЕЛЬ =====
        top = ctk.CTkFrame(self, fg_color=self.BG_SURFACE, corner_radius=0)
        top.pack(fill="x")

        ctk.CTkLabel(
            top, text="🔍",
            font=ctk.CTkFont(size=16),
            text_color=self.TEXT
        ).pack(side="left", padx=(15, 5), pady=12)

        self.search_var = ctk.StringVar()
        self.search_var.trace("w", lambda *a: self.refresh())

        self.search_entry = ctk.CTkEntry(
            top,
            textvariable=self.search_var,
            placeholder_text="Поиск по названию или исполнителю...",
            width=280,
            height=34,
            fg_color=self.BG_CARD,
            border_color=self.SECONDARY,
            text_color=self.TEXT
        )
        self.search_entry.pack(side="left", padx=5, pady=12)

        self.sort_var = ctk.StringVar(value="Без сортировки")
        ctk.CTkOptionMenu(
            top,
            values=["Без сортировки", "По названию", "По исполнителю", "По длительности"],
            variable=self.sort_var,
            command=lambda x: self.refresh(),
            fg_color=self.BG_CARD,
            button_color=self.SECONDARY,
            button_hover_color=self.PRIMARY,
            width=180,
            height=34
        ).pack(side="left", padx=5, pady=12)

        ctk.CTkButton(
            top, text="📂 Добавить",
            width=120, height=34,
            fg_color=self.PRIMARY,
            hover_color=self.SECONDARY,
            command=self.add_folder
        ).pack(side="right", padx=5, pady=12)

        ctk.CTkButton(
            top, text="🗑 Удалить",
            width=110, height=34,
            fg_color=self.BG_CARD,
            hover_color="#c62828",
            command=self.remove_selected
        ).pack(side="right", padx=5, pady=12)

        # ===== ТАБЛИЦА =====
        table_frame = ctk.CTkFrame(self, fg_color=self.BG_DARK)
        table_frame.pack(fill="both", expand=True, padx=15, pady=15)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Custom.Treeview",
            background=self.BG_CARD,
            foreground=self.TEXT,
            fieldbackground=self.BG_CARD,
            borderwidth=0,
            rowheight=34,
            font=("Segoe UI", 11)
        )
        style.configure(
            "Custom.Treeview.Heading",
            background=self.PRIMARY,
            foreground=self.TEXT,
            borderwidth=0,
            font=("Segoe UI", 11, "bold")
        )
        style.map(
            "Custom.Treeview",
            background=[("selected", self.PRIMARY)],
            foreground=[("selected", self.TEXT)]
        )
        style.map(
            "Custom.Treeview.Heading",
            background=[("active", self.SECONDARY)]
        )

        columns = ("num", "title", "artist", "album", "duration")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
            selectmode="browse"
        )

        self.tree.heading("num", text="№")
        self.tree.heading("title", text="Название")
        self.tree.heading("artist", text="Исполнитель")
        self.tree.heading("album", text="Альбом")
        self.tree.heading("duration", text="Время")

        self.tree.column("num", width=50, anchor="center")
        self.tree.column("title", width=300, anchor="w")
        self.tree.column("artist", width=200, anchor="w")
        self.tree.column("album", width=200, anchor="w")
        self.tree.column("duration", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Double-Button-1>", self._on_double_click)
        self.tree.bind("<Return>", self._on_double_click)

        # ===== НИЗ =====
        bottom = ctk.CTkFrame(self, fg_color=self.BG_SURFACE, corner_radius=0)
        bottom.pack(fill="x")

        self.stats_label = ctk.CTkLabel(
            bottom, text="Треков: 0  •  Общее время: 0:00",
            font=ctk.CTkFont(size=11),
            text_color=self.TEXT_DIM
        )
        self.stats_label.pack(side="left", padx=15, pady=8)

        ctk.CTkButton(
            bottom, text="❌ Закрыть",
            width=100, height=28,
            fg_color=self.BG_CARD,
            hover_color=self.SECONDARY,
            command=self.destroy
        ).pack(side="right", padx=15, pady=8)

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        tracks = list(self.player_window.playlist)

        query = self.search_var.get().lower().strip()
        if query:
            tracks = [
                t for t in tracks
                if query in t.title.lower() or query in t.artist.lower()
            ]

        sort_mode = self.sort_var.get()
        if sort_mode == "По названию":
            tracks.sort(key=lambda t: t.title.lower())
        elif sort_mode == "По исполнителю":
            tracks.sort(key=lambda t: t.artist.lower())
        elif sort_mode == "По длительности":
            tracks.sort(key=lambda t: t.duration)

        total_seconds = 0
        current = self._current_track()

        for i, track in enumerate(tracks):
            marker = "▶ " if track is current else "  "
            self.tree.insert(
                "", "end",
                iid=str(id(track)),
                values=(
                    f"{marker}{i + 1}",
                    track.title,
                    track.artist,
                    track.album,
                    track.get_duration_str()
                )
            )
            total_seconds += track.duration

        total_min = total_seconds // 60
        total_sec = total_seconds % 60
        total_h = total_min // 60
        total_m = total_min % 60
        time_str = f"{total_h}:{total_m:02d}:{total_sec:02d}" if total_h else f"{total_m}:{total_sec:02d}"

        self.stats_label.configure(
            text=f"Треков: {len(tracks)}  •  Общее время: {time_str}"
        )

    def _current_track(self):
        idx = self.player_window.current_index
        if 0 <= idx < len(self.player_window.playlist):
            return self.player_window.playlist[idx]
        return None

    def _on_double_click(self, event):
        selection = self.tree.selection()
        if not selection:
            return

        iid = selection[0]
        for i, track in enumerate(self.player_window.playlist):
            if str(id(track)) == iid:
                self.player_window.play_track(i)
                break

    def add_folder(self):
        self.player_window.open_folder()
        self.refresh()

    def remove_selected(self):
        selection = self.tree.selection()
        if not selection:
            return

        iid = selection[0]
        for i, track in enumerate(self.player_window.playlist):
            if str(id(track)) == iid:
                del self.player_window.playlist[i]
                break

        self.refresh()