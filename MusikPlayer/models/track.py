import os


class Track:

    def __init__(self, file_path):
        self.file_path = file_path
        self.title = "Неизвестно"
        self.artist = "Неизвестен"
        self.album = "Неизвестен"
        self.duration = 0
        self.year = ""

        self._parse_from_filename()
        self._parse_id3v1()

    def _parse_from_filename(self):
        """Парсит имя файла: 'Artist - Title.mp3'"""
        name = os.path.basename(self.file_path)
        name = os.path.splitext(name)[0]


        if ". " in name[:4]:
            name = name.split(". ", 1)[-1]

        if " - " in name:
            parts = name.split(" - ", 1)
            self.artist = parts[0].strip()
            self.title = parts[1].strip()
        else:
            self.title = name

    def _parse_id3v1(self):

        try:
            with open(self.file_path, "rb") as f:
                f.seek(-128, 2)
                tag = f.read(128)

                if tag[:3] != b"TAG":
                    return

                def decode(data):
                    for enc in ("cp1251", "utf-8", "latin1"):
                        try:
                            return data.decode(enc).strip("\x00 ").strip()
                        except Exception:
                            continue
                    return ""

                title = decode(tag[3:33])
                artist = decode(tag[33:63])
                album = decode(tag[63:93])
                year = decode(tag[93:97])

                if title:
                    self.title = title
                if artist:
                    self.artist = artist
                if album:
                    self.album = album
                if year:
                    self.year = year
        except Exception:
            pass

    def get_duration_str(self):
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}"

    def __str__(self):
        return f"{self.artist} — {self.title}"

    def __repr__(self):
        return f"Track({self.title}, {self.artist})"
