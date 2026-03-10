#!/usr/bin/env python3
"""
AdGuard Tray – entry point.
Run directly:  python adguard-tray.py
"""
import sys
from pathlib import Path

# Allow running from the project root without installation
sys.path.insert(0, str(Path(__file__).parent))

from adguard_tray.main import main

if __name__ == "__main__":
    main()
