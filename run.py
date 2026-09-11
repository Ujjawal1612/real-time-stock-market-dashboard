"""Convenience launcher: streamlit run app/dashboard.py"""

import subprocess
import sys

subprocess.run(
    [sys.executable, "-m", "streamlit", "run", "app/dashboard.py"],
    check=False,
)
