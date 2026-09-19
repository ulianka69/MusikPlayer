
from ui.player_window import PlayerWindow


def main():
    print("=" * 50)
    print("🎵 Music Player запущен")
    print("=" * 50)
    print("Управление:")
    print("  Space       — Play/Pause")
    print("  ←  /  →     — Предыдущий / Следующий")
    print("  ↑  /  ↓     — Громкость")
    print("  Ctrl + L    — Открыть список треков")
    print("=" * 50)

    app = PlayerWindow()
    app.protocol("WM_DELETE_WINDOW", app._on_close)
    app.mainloop()


if __name__ == "__main__":
    main()