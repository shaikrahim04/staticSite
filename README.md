# staticSite

A simple static site generator written in Python.

## Overview

**staticSite** converts your Markdown content into a static HTML website.  
It supports headings, paragraphs, code blocks, blockquotes, lists, bold, italic, inline code, links, and images.  
It recursively processes all markdown files in the `content` directory and outputs HTML to the `docs` directory, preserving the directory structure.  
Static assets from the `static` directory are copied to `docs`.

## Features

- Converts Markdown files to HTML using a customizable template.
- Recursively processes all markdown files in the `content` directory.
- Preserves directory structure in the generated `docs` directory.
- Copies static assets (CSS, images, etc.) from `static` to `docs`.
- Supports GitHub Pages deployment (just serve the `docs` directory).

## Usage

1. **Prepare your content:**
   - Place Markdown files in the `content` directory (subdirectories supported).
   - Place static assets (CSS, images, etc.) in the `static` directory.
   - Create a `template.html` file in the project root with `{{ Title }}` and `{{ Content }}` placeholders.

2. **Generate your site:**
   ```bash
   python3 src/main.py
   ```

3. **View your site:**
   - Generated HTML files and static assets will be in the `docs` directory.
   - You can serve this directory locally or deploy it to GitHub Pages.

## Example `template.html`

```html
<!DOCTYPE html>
<html>
<head>
  <title>{{ Title }}</title>
  <link rel="stylesheet" href="/style.css">
</head>
<body>
  {{ Content }}
</body>
</html>
```

## Running Tests

- All unit tests are in files named `test_*.py` in the `src` directory.
- To run all tests:
  ```bash
  python3 -m unittest discover src
  ```

## Deploying to GitHub Pages

1. Push your repository to GitHub.
2. In your repository settings, set GitHub Pages to serve from the `/docs` directory on the `main` branch.
3. Commit and push your generated `docs` directory.

## Project Structure

```
staticSite/
├── content/         # Your markdown files (site content)
├── docs/            # Generated HTML site (output)
├── static/          # Static assets (CSS, images, etc.)
├── src/             # Source code
│   ├── main.py
│   ├── markdown_to_blocks.py
│   ├── htmlnode.py
│   ├── textnode.py
│   ├── inline_markdown.py
│   └── test_*.py
├── template.html    # Your HTML template
└── README.md
```
This project is based on the ["Build a Static Site Generator in Python"](https://www.boot.dev/courses/build-static-site-generator-python) course from [Boot.dev](https://www.boot.dev/).

---
