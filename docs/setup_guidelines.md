# Setup Guidelines: SmartGen Docs

This guide provides a comprehensive, step-by-step walkthrough to set up and run **SmartGen Docs**—a zero-configuration, AI-driven documentation platform. Follow these instructions to configure your local development environment or deploy the automated GitOps workflow.

---

## System Requirements & Prerequisites

Before initiating the installation, ensure your environment meets the following baseline requirements:

*   **Runtime Environment**: Python 3.7 or higher installed on your system.
*   **Target Repository**: A public GitHub repository for which you wish to generate documentation.
*   **Authentication & Access**:
    *   A **Google Gemini API Key** (to orchestrate documentation generation).
    *   A **GitHub Personal Access Token (PAT)** with appropriate scopes to read repository metadata and commit changes.

---

## Step-by-Step Installation

### Step 1: Clone the Repository
Retrieve the source code from the official repository and navigate into the project's root directory:

```bash
git clone https://github.com/bayzed123/SmartGenDocs.git
cd SmartGenDocs
```

### Step 2: Establish a Virtual Environment (Recommended)
To prevent dependency conflicts with your global Python environment, isolate your workspace using a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### Step 3: Install Required Dependencies
Install the required platform libraries, which include `PyGithub` for interfacing with the GitHub REST API and `google-generativeai` for interacting with the Gemini LLM engine.

```bash
pip install PyGithub google-generativeai
```

> **DevOps Tip**: Alternatively, you can install the exact pinned versions specified in the workspace dependencies list:
> ```bash
> pip install -r requirements.txt
> ```

---

## Local Configuration & Execution

For testing or manual generation without triggering a CI/CD pipeline, configure your local environment variables and run the automation script directly.

### Step 4: Configure Local Environment Variables
Expose your credentials securely to the active shell session. Replace the placeholder values with your actual API keys:

```bash
export GITHUB_TOKEN="your_github_token"
export GEMINI_API_KEY="your_gemini_api_key"
```

### Step 5: Define the Target Repository
Open the `config.json` file in your preferred text editor and update the `repository_link` block with the URL of the repository you want to document:

```json
{
  "repository_link": "https://github.com/owner/repository"
}
```

### Step 6: Manual Document Generation
Execute the core Python automation pipeline manually by running the script and passing your target repository URL as a parameter:

```bash
python generate_docs.py "https://github.com/owner/repository"
```
The script will fetch the codebase structure, construct context payloads, send them to the Gemini API, and output three generated markdown files inside the `/docs` directory.

---

## Deploying the GitOps Pipeline (GitHub Actions)

To leverage the fully automated, zero-configuration GitOps pipeline, set up the platform to run on every configuration change.

### Step 1: Configure GitHub Secrets
To allow the automated GitHub Actions runner to securely communicate with external APIs, save your secrets in your fork/repository settings:
1. Navigate to your GitHub repository: **Settings** > **Secrets and variables** > **Actions**.
2. Add the following **Repository secrets**:
   * `GITHUB_TOKEN`: Your GitHub Personal Access Token.
   * `GEMINI_API_KEY`: Your Google Gemini API Key.

### Step 2: Trigger the Automation
Commit and push a change to the configuration file. The underlying workflow (`.github/workflows/main.yml`) will detect changes to `config.json` on the `main` branch and trigger the processing runner automatically.

```bash
git add config.json
git commit -m "Add repository link for documentation"
git push origin main
```

### Step 3: Review and Merge
1. Go to the **Actions** tab of your repository to monitor the execution progress.
2. Once the workflow run is successful, the runner will automatically open a **Pull Request (PR)** containing the generated documents in the `/docs` path:
   * `overview.md`
   * `architecture_components.md`
   * `setup_guidelines.md`
3. Review and merge the PR to publish your updated documentation.

---

[< Previous: Architecture Components](/architecture_components.md)