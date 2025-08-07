#!/usr/bin/env python3
"""Send Wayland clipboard content to Gemini and show explanation."""

import os
import sys
import subprocess

import requests
import tkinter as tk


def get_clipboard() -> str:
    """Return current Wayland clipboard text using wl-paste."""
    result = subprocess.run(
        ["wl-paste"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout


def ask_gemini(text: str, api_key: str) -> str:
    """Ask Gemini to explain the provided text."""
    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-pro:generateContent"
    )
    headers = {"Content-Type": "application/json"}
    prompt = f"Explain the following text:\n\n{text}"
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}],
            }
        ]
    }
    response = requests.post(url, headers=headers, params={"key": api_key}, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


def show_text(text: str) -> None:
    """Display text in a simple Tkinter window."""
    root = tk.Tk()
    root.title("Gemini Explanation")
    widget = tk.Text(root, wrap="word")
    widget.insert("1.0", text)
    widget.config(state="disabled")
    widget.pack(expand=True, fill="both")
    root.mainloop()


def main() -> int:
    api_key = os.getenv("GEMINI_KEY")
    if not api_key:
        print("GEMINI_KEY environment variable not set", file=sys.stderr)
        return 1
    try:
        clip = get_clipboard().strip()
    except subprocess.CalledProcessError as err:
        print(f"Failed to read clipboard: {err.stderr}", file=sys.stderr)
        return 1
    try:
        explanation = ask_gemini(clip, api_key)
    except requests.RequestException as err:
        print(f"Gemini request failed: {err}", file=sys.stderr)
        return 1
    show_text(explanation)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

