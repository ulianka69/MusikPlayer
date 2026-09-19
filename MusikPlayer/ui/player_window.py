import os
import random
from tkinter import filedialog, messagebox
import customtkinter as ctk

from models.track import Track
from player.audio_player import AudioPlayer
from ui.playlist_window import PlaylistWindow


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class PlayerWindow(ctk.CTk):
    

    PRIMARY = "#ff4081"
    SECONDARY = "#7c4dff"
    BG_DARK = "#0f0c29"
    BG_SURFACE = "#1e1e2e"
    BG_CARD = "#28283c"
    TEXT = "#ffffff"
    TEXT_DIM = "#b0b0d0"

    def __init__(self):
        super().__init__()

        self.title("🎵 Music Player")
        self.geometry("420x700")
        self.configure(fg_color=self.BG_DARK)
        self.resizable(False, False)

        self.audio_player = AudioPlayer()
        self.playlist = []
        self.current_index = -1
        self.is_shuffle = False
        self.is_repeat = False
        self.playlist_window = None

        self._build_ui()
        self._bind_hotkeys()
        self._update_progress()

    def _build_ui(self):
       
        ctk.CTkLabel(
            self, text="🎵 MUSIC PLAYER",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=self.PRIMARY
        ).pack(pady=(20, 10))

    
        self.cover_frame = ctk.CTkFrame(
            self, width=220, height=220,
            fg_color=self.BG_CARD, corner_radius=15
        )
        self.cover_frame.pack(pady=10)
        self.cover_frame.pack_propagate(False)

        self.cover_label = ctk.CTkLabel(
            self.cover_frame, text="♪",
            font=ctk.CTkFont(size=90),
            text_color=self.PRIMARY
        )
        self.cover_label.pack(expand=True, fill="both")

       
        self.track_title = ctk.CTkLabel(
            self, text="Трек не выбран",
            font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold"),
            text_color=self.TEXT,
            wraplength=380
        )
        self.track_title.pack(pady=(15, 3))

        self.track_artist = ctk.CTkLabel(
            self, text="—",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=self.TEXT_DIM
        )
        self.track_artist.pack()

        self.track_album = ctk.CTkLabel(
            self, text="",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.SECONDARY
        )
        self.track_album.pack(pady=(0, 10))

      
        progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        progress_frame.pack(fill="x", padx=35, pady=(10, 5))

        self.progress_bar = ctk.CTkSlider(
            progress_frame, from_=0, to=100,
            progress_color=self.PRIMARY,
            button_color=self.PRIMARY,
            button_hover_color=self.SECONDARY,
            fg_color=self.BG_CARD, height=14
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x")

        time_frame = ctk.CTkFrame(self, fg_color="transparent")
        time_frame.pack(fill="x", padx=35)

        self.time_current = ctk.CTkLabel(
            time_frame, text="0:00",
            font=ctk.CTkFont(family="Courier New", size=11),
            text_color=self.TEXT_DIM
        )
        self.time_current.pack(side="left")

        self.time_total = ctk.CTkLabel(
            time_frame, text="0:00",
            font=ctk.CTkFont(family="Courier New", size=11),
            text_color=self.TEXT_DIM
        )
        self.time_total.pack(side="right")

       
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(pady=15)

        btn_kw = dict(
            width=50, height=50,
            font=ctk.CTkFont(size=20),
            fg_color=self.BG_CARD,
            hover_color=self.SECONDARY,
            corner_radius=25,
            cursor="hand2"
        )

        self.open_btn = ctk.CTkButton(
            controls, text="📂", command=self.open_folder, **btn_kw
        )
        self.open_btn.pack(side="left", padx=4)

        self.prev_btn = ctk.CTkButton(
            controls, text="⏮", command=self.play_previous, **btn_kw
        )
        self.prev_btn.pack(side="left", padx=4)

        self.play_btn = ctk.CTkButton(
            controls, text="▶",
            width=80, height=80,
            font=ctk.CTkFont(size=32, weight="bold"),
            fg_color=self.PRIMARY,
            hover_color=self.SECONDARY,
            corner_radius=40,
            cursor="hand2",
            command=self.toggle_play_pause
        )
        self.play_btn.pack(side="left", padx=10)

        self.next_btn = ctk.CTkButton(
            controls, text="⏭", command=self.play_next, **btn_kw
        )
        self.next_btn.pack(side="left", padx=4)

       
        extra = ctk.CTkFrame(self, fg_color="transparent")
        extra.pack(pady=(0, 15))

        small_kw = dict(
            width=50, height=40,
            font=ctk.CTkFont(size=16),
            fg_color=self.BG_CARD,
            hover_color=self.SECONDARY,
            corner_radius=20,
            cursor="hand2"
        )

        self.shuffle_btn = ctk.CTkButton(
            extra, text="🔀", command=self.toggle_shuffle, **small_kw
        )
        self.shuffle_btn.pack(side="left", padx=4)

        self.repeat_btn = ctk.CTkButton(
            extra, text="🔁", command=self.toggle_repeat, **small_kw
        )
        self.repeat_btn.pack(side="left", padx=4)

        self.list_btn = ctk.CTkButton(
            extra, text="📋 Список",
            width=110, height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=self.SECONDARY,
            hover_color=self.PRIMARY,
            corner_radius=20,
            cursor="hand2",
            command=self.open_playlist_window
        )
        self.list_btn.pack(side="left", padx=4)

       
        volume_frame = ctk.CTkFrame(self, fg_color="transparent")
        volume_frame.pack(fill="x", padx=60, pady=10)

        ctk.CTkLabel(
            volume_frame, text="🔊",
            font=ctk.CTkFont(size=18),
            text_color=self.TEXT
        ).pack(side="left", padx=5)

        self.volume_slider = ctk.CTkSlider(
            volume_frame, from_=0, to=100,
            command=self._on_volume_change,
            progress_color=self.PRIMARY,
            button_color=self.PRIMARY,
            button_hover_color=self.SECONDARY,
            fg_color=self.BG_CARD, height=14
        )
        self.volume_slider.set(70)
        self.volume_slider.pack(side="left", fill="x", expand=True, padx=5)

        self.volume_label = ctk.CTkLabel(
            volume_frame, text="70%",
            font=ctk.CTkFont(family="Courier New", size=11),
            text_color=self.TEXT_DIM, width=40
        )
        self.volume_label.pack(side="right")

        self.status_label = ctk.CTkLabel(
            self, text="Готов к работе",
            font=ctk.CTkFont(size=11),
            text_color=self.TEXT_DIM
        )
        self.status_label.pack(pady=(5, 15))

    
    def _bind_hotkeys(self):
        self.bind("<space>", lambda e: self.toggle_play_pause())
        self.bind("<Right>", lambda e: self.play_next())
        self.bind("<Left>", lambda e: self.play_previous())
        self.bind("<Up>", lambda e: self.volume_slider.set(min(100, self.volume_slider.get() + 5)))
        self.bind("<Down>", lambda e: self.volume_slider.set(max(0, self.volume_slider.get() - 5)))
        self.bind("<Control-l>", lambda e: self.open_playlist_window())

   
    def _on_volume_change(self, value):
        v = int(value)
        self.audio_player.set_volume(v / 100.0)
        self.volume_label.configure(text=f"{v}%")

    def open_folder(self):
        folder = filedialog.askdirectory(title="Выберите папку с музыкой")
        if not folder:
            return

        print("\n" + "=" * 50)
        print(f"📂 Выбрана папка: {folder}")

       
        try:
            all_files = os.listdir(folder)
        except Exception as e:
            print(f"❌ Ошибка чтения папки: {e}")
            messagebox.showerror("Ошибка", f"Не удалось прочитать папку:\n{e}")
            return

        print(f"📁 Всего файлов: {len(all_files)}")
        print("Файлы в папке:")
        for f in all_files[:30]: 
            print(f"   • {f}")
        if len(all_files) > 30:
            print(f"   ... и ещё {len(all_files) - 30}")

       
        exts = (".mp3", ".wav", ".ogg", ".flac", ".m4a")
        print(f"\n🔍 Ищем файлы с расширениями: {exts}")

        files = sorted([
            os.path.join(folder, f)
            for f in all_files
            if f.lower().endswith(exts)
        ])

        print(f"🎵 Найдено аудиофайлов: {len(files)}")
        print("=" * 50 + "\n")

        if not files:
            
            help_text = (
                f"В папке нет аудиофайлов!\n\n"
                f"Папка: {folder}\n"
                f"Всего файлов: {len(all_files)}\n\n"
                f"Поддерживаются:\n"
                f"  • MP3\n"
                f"  • WAV\n"
                f"  • OGG\n"
                f"  • FLAC\n"
                f"  • M4A\n\n"
                f"Смотрите консоль для деталей."
            )
            messagebox.showwarning("Пусто", help_text)
            self.status_label.configure(text="❌ Треки не найдены")
            return

       
        loaded = 0
        errors = 0
        for f in files:
            try:
                track = Track(f)
                
                try:
                    import pygame
                    sound = pygame.mixer.Sound(f)
                    track.duration = int(sound.get_length())
                except Exception as dur_err:
                    print(f"⚠️ Длительность не определена для {os.path.basename(f)}: {dur_err}")
                    track.duration = 0

                self.playlist.append(track)
                loaded += 1
                print(f"✅ [{loaded}] {track.artist} — {track.title}  ({track.get_duration_str()})")
            except Exception as e:
                errors += 1
                print(f"❌ Ошибка загрузки {os.path.basename(f)}: {e}")

        self.status_label.configure(
            text=f"✅ Загружено треков: {loaded}" + (f" (ошибок: {errors})" if errors else "")
        )

       
        if self.playlist_window and self.playlist_window.winfo_exists():
            self.playlist_window.refresh()

    def play_track(self, index):
        
        if index < 0 or index >= len(self.playlist):
            return

        self.current_index = index
        track = self.playlist[index]

        if self.audio_player.load(track.file_path):
            self.audio_player.play()
            self.play_btn.configure(text="⏸")

            self.track_title.configure(text=track.title)
            self.track_artist.configure(text=track.artist)
            self.track_album.configure(text=track.album)
            self.time_total.configure(text=track.get_duration_str())

            self.status_label.configure(
                text=f"▶ Воспроизведение: {track.title}"
            )

            if self.playlist_window and self.playlist_window.winfo_exists():
                self.playlist_window.refresh()
        else:
            self.status_label.configure(text=f"❌ Ошибка воспроизведения")

    def toggle_play_pause(self):
        
        if self.current_index == -1:
            if self.playlist:
                self.play_track(0)
            return

        state = self.audio_player.toggle_play_pause()
        self.play_btn.configure(text="⏸" if state == "playing" else "▶")

    def play_next(self):
       
        if not self.playlist:
            return

        if self.is_shuffle:
            next_index = random.randint(0, len(self.playlist) - 1)
        else:
            next_index = (self.current_index + 1) % len(self.playlist)

        self.play_track(next_index)

    def play_previous(self):
        
        if not self.playlist:
            return
        prev_index = (self.current_index - 1) % len(self.playlist)
        self.play_track(prev_index)

    def toggle_shuffle(self):
       
        self.is_shuffle = not self.is_shuffle
        self.shuffle_btn.configure(
            fg_color=self.PRIMARY if self.is_shuffle else self.BG_CARD
        )
        self.status_label.configure(
            text=f"🔀 Случайный порядок: {'вкл' if self.is_shuffle else 'выкл'}"
        )

    def toggle_repeat(self):
        
        self.is_repeat = not self.is_repeat
        self.repeat_btn.configure(
            fg_color=self.PRIMARY if self.is_repeat else self.BG_CARD
        )
        self.status_label.configure(
            text=f"🔁 Повтор: {'вкл' if self.is_repeat else 'выкл'}"
        )

    def open_playlist_window(self):
        
        if self.playlist_window and self.playlist_window.winfo_exists():
            self.playlist_window.focus()
            self.playlist_window.refresh()
        else:
            self.playlist_window = PlaylistWindow(self, self)

    
    def _update_progress(self):
       
        if self.current_index >= 0:
            track = self.playlist[self.current_index]
            if self.audio_player.is_playing and track.duration > 0:
                pos = self.audio_player.get_position()
                self.progress_bar.set(min((pos / track.duration) * 100, 100))
                self.time_current.configure(text=self._format_time(pos))

           
            if self.audio_player.is_playing and not self.audio_player.is_busy():
                self.audio_player.is_playing = False
                if self.is_repeat:
                    self.play_track(self.current_index)
                else:
                    self.play_next()

        self.after(500, self._update_progress)

    def _format_time(self, seconds):
        return f"{seconds // 60}:{seconds % 60:02d}"

    def _on_close(self):
       
        if self.audio_player:
            self.audio_player.close()
        self.destroy()