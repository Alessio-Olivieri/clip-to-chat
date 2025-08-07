# clip-to-chat

A small utility that reads the current Wayland clipboard and asks the Gemini LLM to explain it. The response is shown in a separate window.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Ensure `wl-paste` is available (part of [wl-clipboard](https://github.com/bugaevc/wl-clipboard)).
3. Set your Gemini API key:
   ```bash
   export GEMINI_KEY="your_api_key_here"
   ```
4. Run the script:
   ```bash
   python clip_to_chat.py
   ```

This will open a window containing the model's explanation of the clipboard contents.
