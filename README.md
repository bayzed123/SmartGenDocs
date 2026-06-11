
# <img src="https://raw.githubusercontent.com/bayzed123/SmartGenDocs/main/logo.png" width="48" align="center"> SmartGen Docs

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![Gemini 3.5 Flash](https://img.shields.io/badge/AI-Gemini%203.5%20Flash-orange.svg)](https://ai.google.dev/)

**SmartGen Docs** is an autonomous, zero-configuration documentation platform that leverages AI to transform public GitHub repositories into professional documentation sites instantly. Built with a GitOps mindset, it automates the entire lifecycle from repository scanning to live deployment.

---

## 🚀 How to Add Documentation

Generating high-quality docs for any public repository is as simple as uploading a link.

### 1. Prepare the Repository Link
The system expects a standard public GitHub URL:
`https://github.com/owner/repository`

### 2. Upload to `input_links/`
- Navigate to the `input_links/` directory.
- Create a new text file (e.g., `project-link.txt`).
- Paste your GitHub URL into the file and commit the changes.

### 3. Automated GitOps Pipeline
Once you push your change, the **SmartGen Docs Engine** automatically:
- **Validates** the URL and checks for duplicates.
- **Scans** the repository using **Gemini 3.5 Flash**.
- **Generates** 4 unique live HTML pages:
  - **Overview**: Core value and project goals.
  - **Architecture**: Technical design and components.
  - **Deployment Guide**: Step-by-step hosting instructions.
  - **How to Use**: Practical examples and CLI guides.
- **Deploys** the updates directly to your live website.

---

## 🛠 System Features

| Feature | Description |
| :--- | :--- |
| **Zero Configuration** | No setup files required in the target repository. |
| **Instant Live** | Changes are committed directly to the `main` branch for immediate updates. |
| **Separate URLs** | Each documentation category has its own unique, shareable URL. |
| **Smart Validation** | Automatic deduplication and invalid link filtering. |

---

## 📂 Project Structure

```bash
SmartGenDocs/
├── input_links/      # 📥 Upload repo links here to trigger scan
├── docs/             # 📄 Auto-generated Live HTML & Markdown
├── index.html        # 🌐 Premium Landing Page UI
├── generate_docs.py  # 🧠 AI Engine (Python + Gemini 3.5 Flash)
└── .github/          # ⚙️ GitOps Workflow (GitHub Actions)
```

---

## 👨‍💻 Developer
Developed with ❤️ by **[Sayad Md Bayezid Hosan](https://www.sayadbayezid.com)**.

---

**SmartGen Docs** - *Empowering Open Source with AI-Driven Documentation.*
