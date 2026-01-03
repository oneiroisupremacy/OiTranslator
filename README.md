```markdown
# Oi Translator

A simple and powerful subtitle translator powered by ZhipuAI (GLM-4). Supports batch processing for whole seasons and intelligent tag preservation.

## Features

- **Batch Processing:** Translate multiple files or entire folders at once.
- **Free AI Models:** Uses free-tier models like `glm-4.6v-flash`.
- **Smart Tag Handling:** Keeps formatting tags (position, colors) but removes sound tags (`[MUSIC]`, etc.).
- **Network Protection:** Auto-pauses on connection failure and resumes when internet is back.
- **Custom Output:** Flexible naming (e.g., add `_Indo` suffix automatically).
- **Estimated Time:** Shows real-time ETA during translation.

## Installation

1. Make sure you have **Python 3.8+** installed.
2. Download or clone this project.
3. Install required libraries:

```bash
pip install -r requirements.txt
```

> **Note:** If you are on Linux and get an error about `tkinter`, install it via: `sudo apt-get install python3-tk`

## Quick Start

1. Get your API Key from [ZhipuAI Open Platform](https://open.bigmodel.cn/).
2. Run the application:

```bash
python main.py
```

3. Paste your API Key in the top field and click **Save**.
4. Add a file or folder, then click **Start Translation**.

## Troubleshooting

- **Error 1211 (Model Not Found):** 
  Verify your API Key. Try selecting a different model in the dropdown (e.g., `glm-3-turbo`).
  
- **Internet Issues:** 
  The app will auto-pause if the connection drops. Click "Resume" when your internet is stable.

## License

MIT License
```
