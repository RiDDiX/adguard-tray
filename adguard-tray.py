#!/usr/bin/env python3
"""
AdGuard Tray – entry point.
Run directly:  python adguard-tray.py
"""
import sys
from pathlib import Path

# Allow running from the project root without installation
sys.path.insert(0, str(Path(__file__).parent))

if "--version" in sys.argv or "-V" in sys.argv:
    from adguard_tray import __version__
    print(f"adguard-tray {__version__}")
    sys.exit(0)

from adguard_tray.main import main

if __name__ == "__main__":
    main()
