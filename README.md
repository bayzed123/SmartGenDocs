
# SmartGen Docs - Zero-Configuration Auto-Docs Platform

## 🚀 Instant Documentation for Any Public Repo

**SmartGen Docs** is an AI-powered platform that automatically scans public GitHub repositories and generates comprehensive, high-quality documentation. Built with a GitOps workflow, it turns a simple repository link into a live documentation site instantly.

---

## 📖 How to Add New Documentation

The system is designed to be completely autonomous. To generate documentation for a new repository, follow these simple steps:

### Step 1: Prepare Your Link
Ensure you have the full URL of a **public** GitHub repository.
Example: `https://github.com/facebook/react`

### Step 2: Upload to `input_links/`
1.  Navigate to the `input_links/` folder in this repository.
2.  Create a new text file (e.g., `my-repo.txt`).
3.  Paste your GitHub link inside the file and save it.
    *   *Note: You can also update the existing `config.json` if you prefer.*

### Step 3: Automated Scan & Deploy
Once you push your change, the following happens automatically:
1.  **Validation**: The system checks if the URL is a valid GitHub link.
2.  **Deduplication**: It ensures the same repository isn't scanned twice.
3.  **AI Generation**: Google Gemini 3.5 Flash scans the repo's code, structure, and metadata.
4.  **Live Update**: Four unique guides (Overview, Architecture, Deployment, and Usage) are generated and committed directly to the `docs/` folder.
5.  **Instant Live**: The landing page updates immediately to reflect the new documentation.

---

## 🛠 System Behavior & Verification

To ensure the highest quality of documentation, the system performs the following checks:

| Feature | Description |
| :--- | :--- |
| **URL Validation** | Only valid `https://github.com/owner/repo` formats are accepted. |
| **Duplicate Prevention** | The system keeps track of scanned repositories and skips duplicates to save API quota. |
| **Empty Link Handling** | Blank files or invalid strings are automatically ignored. |
| **Public Access** | The system can only scan public repositories where code is accessible via the GitHub API. |

---

## 📂 Project Structure

```bash
SmartGenDocs/
├── input_links/      # 📥 UPLOAD LINKS HERE (Trigger Folder)
├── docs/             # 📄 AUTO-GENERATED MARKDOWN (Live Content)
├── index.html        # 🌐 PREMIUM LANDING PAGE (Live UI)
├── generate_docs.py  # 🧠 AI ENGINE (Gemini 3.5 Flash)
└── .github/          # ⚙️ GITOPS PIPELINE (GitHub Actions)
```

---

## 🛠 Technical Setup (For Developers)

### Prerequisites
- Python 3.x
- Google Gemini API Key
- GitHub Personal Access Token

### Local Usage
```bash
# Install dependencies
pip install PyGithub google-generativeai

# Run manually
export GITHUB_TOKEN="your_token"
export GEMINI_API_KEY="your_key"
python generate_docs.py
```

---

## 🤝 Contributing
Feel free to fork this repository and add your own documentation links to the `input_links/` folder!

---

**SmartGen Docs** - *Powered by AI, Delivered by GitOps.*
