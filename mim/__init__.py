from pathlib import Path
import os
from single_source import get_version

_ver_path = Path(__file__).parent.parent
__VERSION__ = get_version(__name__, _ver_path)
