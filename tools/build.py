#!/usr/bin/env python3
"""Entry point: build the Aurora AI Elementor template kit."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aurora.build import build  # noqa: E402

if __name__ == "__main__":
    sys.exit(build())
