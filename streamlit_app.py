"""Streamlit Cloud entrypoint."""

import sys
from pathlib import Path

# Streamlit Cloud installs deps from requirements.txt only; add src for imports.
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from sg_insights.dashboard.app import render_dashboard

render_dashboard()
