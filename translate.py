import os
import yaml
import openai
import subprocess
import re
from glob import glob

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TARGET_LANG = os.getenv('TARGET_LANG', 'Persian') # Default: Persian
TARGET_LANG_CODE = os.getenv('TARGET_LANG_CODE', 'fa') # Default: fa
FILE_EXTS = os.getenv('FILE_EXTS','md') # Default: Markdown files
OUTPUT_FORMAT = os.getenv('OUTPUT_FORMAT', '*-{lang}.{ext}') # Default: *-fa.md

if not OPENAI_API_KEY:
    raise ValueError('Missing OpenAI API key!')

openai.api_key = OPENAI_API_KEY


def extract_yaml_and_content(md_text):
    match = re.match(r"^---\n(.*?)\n---\n(.*)", md_text, re.DOTALL)
    if match:
        yaml_part, content = match.group()
        yaml_data = yaml.safe_load(yaml_part)
        return yaml_data, content.strip()
    return None, md_text.strip()


def reconstruct_markdown(yaml_data, translated_content):
    yaml_str = yaml.dump(yaml_data, allow_unicode=True, default_flow_style=False)
    return f"---\n{yaml_str}---\n\n{translated_content}"


def translate_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": f"You are a translator specializing in software development. Preserve YAML metadata and technical terms. Translate the text to {TARGET_LANG}."
            },
            {"role": "user", "content": f"Translate this text to {TARGET_LANG} while keeping YAML keys unchanged:\n{text}"},
        ],
    )
    return response["choices"][0]["message"]["content"].strip()


def get_changed_files():
    changed_files = []
    for ext in FILE_EXTS:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "--", f"*.{ext.strip()}"],
            capture_output=True,
            text=True,
        )
        changed_files.extend([file.strip() for file in result.stdout.split("\n") if file.strip()])
    return changed_files


def get_translated_filename(file_path):
    ext = file_path.split(".")[-1]
    base_name = ".".join(file_path.split(".")[:-1])  # Remove extension
    lang_code = f'-{TARGET_LANG_CODE.lower()}'
    return OUTPUT_FORMAT.replace("{lang}", lang_code).replace("{ext}", ext).replace("*", base_name)


def main():
    changed_files = get_changed_files()
    if not changed_files:
        print("No changed files detected.")
        return

    for file_path in changed_files:
        print(f"Processing: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            file_text = f.read()

        # Extract YAML front matter if it's an md file
        if file_path.endswith(".md"):
            yaml_data, content = extract_yaml_and_content(file_text)
        else:
            yaml_data, content = None, file_text.strip()

        translated_content = translate_text(content)

        # Reconstruct if it's markdown with YAML front matter
        translated_file_text = (
            reconstruct_markdown(yaml_data, translated_content)
            if yaml_data
            else translated_content
        )

        # Generate target filename
        translated_file_path = get_translated_filename(file_path)

        # Save translated file
        with open(translated_file_path, "w", encoding="utf-8") as f:
            f.write(translated_file_text)

        print(f"Translated file saved to: {translated_file_path}")

    # Git commit and push
    subprocess.run(["git", "config", "--global", "user.name", "github-actions[bot]"])
    subprocess.run(["git", "config", "--global", "user.email", "github-actions[bot]@users.noreply.github.com"])
    subprocess.run(["git", "add", "*"])
    subprocess.run(["git", "commit", "-m", f"Add translated files in {TARGET_LANG}"])
    subprocess.run(["git", "push"])

if __name__ == "__main__":
    main()