import base64
import mimetypes

from pathlib import Path
from tkinter import TclError, Tk, filedialog
from langchain.messages import HumanMessage

MAX_IMAGE_SIZE_BYTES = 10_000_000


def choose_image_file() -> Path:
    """Let the user choose a graphical picker or enter an image path."""
    while True:
        print("How would you like to provide an image?")
        print("1. Choose an image using the file picker")
        print("2. Paste or type an image path")
        choice = input("Select 1 or 2: ").strip()

        if choice == "1":
            return _choose_image_with_picker()
        elif choice == "2":
            filename = input("Image path: ").strip().strip('"').strip("'")
            if not filename:
                raise SystemExit("No image path provided.")
            return Path(filename).expanduser()

        print("Please enter 1 or 2.")


def _choose_image_with_picker() -> Path:
    root = None
    try:
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        filename = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.webp"),
                ("All files", "*.*"),
            ],
        )
    except TclError:
        filename = input("File picker unavailable. Enter image path: ").strip()
        filename = filename.strip('"').strip("'")
    finally:
        if root is not None:
            root.destroy()

    if not filename:
        raise SystemExit("No image selected.")

    return Path(filename).expanduser()


def image_to_data_url(image_path: Path) -> str:
    image_path = image_path.expanduser().resolve()

    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    mime_type, _ = mimetypes.guess_type(str(image_path))
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError(f"Not an image file: {image_path}")

    if image_path.stat().st_size > MAX_IMAGE_SIZE_BYTES:
        max_size_mb = MAX_IMAGE_SIZE_BYTES // 1_000_000
        raise ValueError(
            f"Image exceeds the maximum allowed size of {max_size_mb} MB."
        )

    with image_path.open("rb") as image_file:
        image_bytes = image_file.read(MAX_IMAGE_SIZE_BYTES + 1)

    if len(image_bytes) > MAX_IMAGE_SIZE_BYTES:
        max_size_mb = MAX_IMAGE_SIZE_BYTES // 1_000_000
        raise ValueError(
            f"Image exceeds the maximum allowed size of {max_size_mb} MB."
        )

    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{image_b64}"


def build_image_message(image_path: Path, prompt: str) -> HumanMessage:
    return HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_to_data_url(image_path)}},
        ]
    )
