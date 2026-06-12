from pathlib import Path


FILE_TYPES = {
    "images":    [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
    "documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".csv"],
    "videos":    [".mp4", ".mov", ".avi", ".mkv"],
    "audio":     [".mp3", ".wav", ".flac", ".aac"],
    "code":      [".py", ".js", ".html", ".css", ".json"],
    "archives":  [".zip", ".tar", ".gz", ".rar"],
}


class FileOrganizer:
    def __init__(self, target_folder: str):
        self.folder = Path(target_folder)

    def _get_category(self, file: Path) -> str:
        """Return the category name for a file, or 'others' if unknown."""
        extension = file.suffix.lower()
        for category, extensions in FILE_TYPES.items():
            if extension in extensions:
                return category
        return "others"

    def _resolve_duplicate(self, destination: Path) -> Path:
        """If destination already exists, add _1, _2, etc. to the filename."""
        if not destination.exists():
            return destination

        counter = 1
        stem = destination.stem
        suffix = destination.suffix
        parent = destination.parent

        while True:
            new_name = parent / f"{stem}_{counter}{suffix}"
            if not new_name.exists():
                return new_name
            counter += 1

    def organize(self):
        if not self.folder.exists():
            raise FileNotFoundError(f"Folder not found: {self.folder}")

        moved = 0
        summary = {}

        for file in self.folder.iterdir():
            if file.is_dir():
                continue

            category = self._get_category(file)
            summary[category] = summary.get(category, 0) + 1
            destination = self.folder / category
            destination.mkdir(exist_ok=True)

            final_path = self._resolve_duplicate(destination / file.name)
            file.rename(final_path)
            moved += 1
            print(f"Moved: {file.name} -> {category}/")

        print(f"\nDone. {moved} file(s) organized.")
        print("Summary: ")
        for category, count in summary.items():
            print(f" {category}: {count} file(s)")

if __name__ == "__main__":
    path = input("Enter the full path to the folder you want to organize: ")
    organizer = FileOrganizer(path)
    organizer.organize()

