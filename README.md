# staticSite

A simple static site generator written in Python.

## Features

- Converts Markdown files to HTML using a template.
- Supports headings, paragraphs, code blocks, blockquotes, ordered/unordered lists, bold, italic, inline code, links, and images.
- Recursively processes all markdown files in the `content` directory and outputs HTML to the `public` directory, preserving directory structure.
- Copies static assets from the `static` directory to `public`.

## Usage

1. **Prepare your content:**
   - Place your Markdown files in the `content` directory.
   - Place your static assets (CSS, images, etc.) in the `static` directory.
   - Create a `template.html` file with `{{ Title }}` and `{{ Content }}` placeholders.

2. **Run the generator:**
   ```bash
   python3 src/main.py
   ```

3. **View your site:**
   - Generated HTML files will be in the `public` directory, ready to be served.

## Development

- All source code is in the `src` directory.
- Unit tests are in files named `test_*.py` (e.g., `test_markdown_to_blocks.py`).
- To run all tests:
  ```bash
  python3 -m unittest discover src
  ```

## Example

A minimal `template.html`:

```html
<!DOCTYPE html>
<html>
<head>
  <title>{{ Title }}</title>
</head>
<body>
  {{ Content }}
</body>
</html>
```

---

**Project by Abdulrahim**
