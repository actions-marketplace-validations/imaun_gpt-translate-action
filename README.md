# 🚀 Translate Files with OpenAI API (GitHub Action)
---
This GitHub Action detects changes in specified file types (Markdown, JSON, TXT, etc.), translates the modified content using OpenAI GPT-4, and commits the translations back to your repository.

✅ Supports multiple file extensions
✅ Preserves YAML front matter in markdown files
✅ Allows custom output file formats
✅ Automatically commits and pushes translated files

---
## 🛠 How It Works
- Detects changed files (based on extensions like .md, .json, .txt).
- Extracts and preserves YAML front matter (if applicable).
- Sends content to OpenAI API for translation.
- Saves the translated version with a custom filename format (e.g., *-fr.md, translated_*.json).
- Commits and pushes the translated files back to the repository.

---
📌 Example Usage
Add the following workflow to your `.github/workflows/translate.yml` file:

```yaml
name: Translate Files

on:
  push:
    branches:
      - main

jobs:
  translate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Run Translation Action
        uses: imaun/gpt-translate-action@v1.0
        with:
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
          target_language: "French"
          file_extensions: "md,json,txt"
          output_format: "translated_*.{ext}"
```
## ⚙️ Inputs
- `openai_api_key` (Required): Your OpenAI API key (stored as a GitHub Secret).
- `target_lang`: The language to translate into (default: **Persian**).
- `target_lang_code`: The language code to be used in output format (default: **fa**).
- `file_exts`: Comma-separated list of file types to process (default: **md**).
- `output_format`: Format for translated files. Use {lang} for language and {ext} for extension.

## 🎯 Example Output Filenames
- "*-{lang}.{ext}": about-fa.md
- "translated_*.{ext}": translated_about.json

## 🔑 Setting Up OpenAI API Key
- Go to **Settings** → **Secrets and Variables** → **Actions** in your repository.
- Click **New Repository Secret**.
- Add a secret named `OPENAI_API_KEY` and paste your OpenAI API key.

