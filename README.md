```
# Oi Translator

<div align="center">
  <h3>Fast, Free, & Open Source Subtitle Translator</h3>
  <p>Powered by ZhipuAI (GLM-4) • Batch Processing • Smart Tag Preservation</p>
</div>

---

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)

**Oi Translator** is a cross-platform desktop application designed to translate subtitle files (.srt, .vtt) efficiently using the power of free AI models from ZhipuAI (GLM-4). Perfect for translating whole seasons of TV series or single movie files with ease.

## 🌟 Features

*   **Batch Processing:** Translate single files or entire folders (Seasons) at once.
*   **Free AI Models:** Utilizes free tier models like `glm-4.6v-flash` and `glm-4.5-flash`.
*   **Smart Tag Handling:** Intelligently removes non-dialog tags (like `[MUSIC]`, `(SOUND)`) while preserving essential subtitle formatting (like `{\pos(...)}`).
*   **Pause & Resume:** Control the translation process manually.
*   **Auto-Pause:** Automatically pauses when internet connection is lost and resumes when reconnected.
*   **Custom Output Naming:** Flexible output file naming using custom suffixes or language codes (e.g., `_{lang}`).
*   **ETA Calculation:** Real-time estimation of translation time.
*   **Bilingual UI:** Clean English/Indonesian interface support.

## 📋 Prerequisites

*   **Python 3.8+** installed on your system.
*   **API Key** from [ZhipuAI Open Platform (BigModel.cn)](https://open.bigmodel.cn/).

## 🚀 Installation

1.  **Clone or Download** this repository.
2.  Navigate to the project folder:
    ```bash
    cd Oi-Translator
    ```
3.  Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

> **Note for Linux Users:** If you encounter an error about `tkinter`, install it via your package manager:
> `sudo apt-get install python3-tk`

## 🛠️ Configuration (API Key)

1.  Go to [https://open.bigmodel.cn/](https://open.bigmodel.cn/).
2.  Sign up and verify your account.
3.  Go to the **User Center -> API Keys**.
4.  Copy your API Key (Format: `id.secret`).
5.  Run `main.py` and paste the key into the application's input field, then click **Save**.

## 💻 Usage

1.  **Run the Application:**
    ```bash
    python main.py
    ```
2.  **Select Input:**
    *   Click **"Add Single File"** for one subtitle file.
    *   Click **"Add Batch Folder"** for a folder containing multiple files (e.g., a TV Series Season).
3.  **Settings:**
    *   **Target Language:** Set your desired output language (e.g., "Indonesian").
    *   **Output Suffix:** Define how the output file is named. Use `{lang}` to auto-insert the language name.
        *   Example: Input `movie.srt` + Suffix `_{lang}` -> Output `movie_Indonesian.srt`.
    *   **Speed Mode:** Choose between `Safe`, `Standard`, or `Aggressive` (affects API request rate).
4.  **Start:** Click **"START TRANSLATION"**.
5.  **Control:** You can click **"PAUSE"** to stop temporarily or **"STOP"** to end the process.


## ⚙️ Troubleshooting

*   **Error 1211 (Model not found):** Ensure your API Key is correct and your account is verified on ZhipuAI. Try switching the model name in the dropdown (e.g., `glm-3-turbo`).
*   **Connection Error:** The app features "Auto-Pause". If your internet is unstable, it will pause automatically. Wait for the internet to stabilize and click **Resume**.
*   **Encoding Issues:** The tool uses `chardet` to automatically detect file encoding.

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Credits

*   Powered by [ZhipuAI (BigModel)](https://open.bigmodel.cn/)
*   Built with Python & Tkinter.
```
