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


