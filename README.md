<p align="left">
  <img src="https://raw.githubusercontent.com/kgcodex/doxite/main/Dx2.png" width="40" align="center" style="border-radius: 2px"/>
  <span style="font-size: 32px; font-weight: 700; vertical-align: middle; margin-left: 8px; ">doxite</span>
</p>
<div align="center">
  <img src="https://raw.githubusercontent.com/kgcodex/doxite/main/Dx2.png" alt="preview" width="700" style="border-radius: 14px;" />
</div>

**Doxite** is a minimal static site generator written in Python.  
It converts Markdown files into static HTML using a custom Markdown parser and provides a simple CLI workflow for bootstrapping a project and generating pages.

<div align="center">
<a href="https://pypi.org/project/doxite/">
    <img src="https://img.shields.io/pypi/v/doxite.svg" alt="PyPI version">
</a>
<a href="https://pypi.org/project/doxite/">
    <img src="https://img.shields.io/pypi/pyversions/doxite.svg" alt="Python version">
</a>
<a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
</a>
</div>

> Current status: **early-stage / in active development**  
> The Markdown parser is implemented and working, and the CLI scaffold has started. The full static site generation pipeline is still being built.

---

## Features

### Implemented
- Custom Markdown parser written from scratch in Python
- HTML AST / node-based rendering pipeline
- Support for common Markdown block types:
  - Headings
  - Paragraphs
  - Blockquotes
  - Fenced code blocks
  - Ordered lists
  - Unordered lists
- Support for inline Markdown syntax:
  - Bold
  - Italic
  - Inline code
  - Links
  - Images
- CLI-based project initialization with `doxite init`
- Fixture-based parser tests comparing generated HTML against expected HTML

### Planned
- Built-in page template injection
- Public asset copying
- `doxite serve`
- `doxite watch`
- Frontmatter support
- Better theming / template system
- Improved CLI UX and project scaffolding

---

## Why this project?

Doxite started as an experiment to understand how static site generators work internally rather than relying on an existing Markdown or SSG library.

The goal is to build a lightweight, hackable static site generator with:
- a custom Markdown parser
- a simple build pipeline
- a clean Python CLI
- minimal dependencies

---

## Installation

```bash
pip install doxite
```

or with `uv`:

```bash
uv add doxite
```

---

## Quick Start

Initialize a new Doxite project:

```bash
doxite init my-site
```

This creates a basic project structure:

```text
my-site/
├── public/
└── src/
    └── index.md
```

Or initialize in the current directory:

```bash
doxite init .
```

---

## Current CLI

### `doxite init`

Bootstraps a new Doxite project in the given directory.

```bash
doxite init my-site
```

or:

```bash
doxite init .
```

At the moment, the CLI is intentionally minimal and mainly focused on project scaffolding while the rest of the SSG pipeline is being built.

---

## Project Status

Doxite is currently in an early development stage.

### Working today
- Markdown parsing
- HTML rendering from the parsed Markdown AST
- Project initialization CLI
- `doxite init`
- `doxite build`

### In progress
- Internal template injection for rendered pages
- Static asset handling

---

## Markdown Support

Doxite currently supports the following Markdown constructs:

### Block-level
- `#` to `######` headings
- Paragraphs
- Blockquotes using `>`
- Ordered lists using `1.`
- Unordered lists using `-`
- Fenced code blocks using triple backticks

### Inline
- `*bold*`
- `_italic_`
- `` `code` ``
- `[link](url)`
- `![image](url)`

---

## Design Notes

A few implementation choices in the current parser are intentionally simplified:

* The Markdown parser is a lightweight custom parser, not a full CommonMark implementation.
* It is designed as a streaming / line-oriented parser with a focus on simplicity and performance.
* The current block parsing behavior intentionally favors a straightforward single-pass design over strict CommonMark compliance.

The goal is not to perfectly replicate every edge case of existing Markdown parsers, but to build a practical and understandable SSG core.

---
## Roadmap

✅Build custom Markdown parser

✅Add HTML node rendering

✅Add parser tests with fixtures

✅Add basic CLI with doxite init and doxite build

✅Implement page build pipeline (partially)

✅Inject rendered content into a base HTML template

⬜Copy public assets to output directory

⬜Add doxite serve

⬜ Add doxite watch

⬜ Add frontmatter support

⬜ Improve theme/template support

---
## Contributing

Issues, ideas, and feedback are welcome.

Doxite is still early, so the architecture and feature set are evolving quickly.