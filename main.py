"""news-image-20261120: copy the poster to the output directory.

Standard library only. The image itself is committed as entry.png;
this program just copies it to $MAKEFUN_OUTPUT_DIR/entry.png.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    out_path = Path(out_dir) / "entry.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", out_path)


if __name__ == "__main__":
    main()
