# Architecture and Components Document: SmartGen Docs

This document provides a comprehensive, highly technical architectural blueprint of **SmartGen Docs**, a zero-configuration, AI-powered documentation automation platform. It describes how the components interact under the hood, the data pipeline flow, and the GitOps implementation strategy.

---

## 1. System Architecture Overview

SmartGen Docs operates as a reactive, event-driven GitOps system. Rather than relying on a persistent backend server, it utilizes **serverless automation** through GitHub Actions triggered by changes in declarative configuration files. 

The system decomposes into four primary architectural layers:

```
                                 [ User Interaction Layer ]
                                             │
                                     Commits config.json
                                             ▼
                                  [ Version Control System ]
                                  (GitHub Repository State)
                                             │
                                  Triggers Action Workflow
                                             ▼
                             [ Orchestration & Execution Layer ]
                                 (GitHub Actions Runner)
                                             │
                            Spawns & injects secret environment
                                             ▼
                               [ Core Automation Script ] ─── (Reads config.json)
                                   (generate_docs.py)
                                     /               \
                       Queries API  /                 \ Queries API
                                   ▼                   ▼
                     [ Target GitHub Repo ]      [ LLM Engine ]
                     (Metadata, README, deps)  (Google Gemini API)
                                   \                   /
                         Raw Data   \                 / Markdown Contents
                                     ▼               ▼
                              [ Context Assembly & Post-Processing ]
                                (Pagination & Link Generation)
                                             │
                                  Writes /docs/ directory
                                             ▼
                                    [ Git Commit/PR ]
                                 (Publishes docs to Repo)
```

---

## 2. Component Breakdown

### 2.1 Configuration Layer (`config.json`)
At the core of the platform's "Zero-Configuration" philosophy is a single declarative configuration file. 
* **Role**: Acts as the single source of truth (SSoT) defining the target project state.
* **Schema**:
  ```json
  {
    "repository_link": "https://github.com/owner/repository"
  }
  ```
* **Architectural Impact**: Modifying this file mutates the repository's desired state, initiating the CI/CD pipeline.

### 2.2 Client-Facing Landing Page (`index.html`)
* **Role**: Provides a modern, dark-themed, conversion-focused landing page showcasing platform value, architecture pipelines, and setup steps.
* **Technology Stack**: HTML5, Tailwind CSS (leveraging utility classes for modern glassmorphism design effects), Custom SVG graphics.
* **Hosting**: Designed for static hosting environments (such as GitHub Pages, Vercel, or Netlify).

### 2.3 Orchestration Engine (`generate_docs.py`)
This is the core Python application engine. It acts as an integration gateway between GitHub's content APIs and Google's Generative AI infrastructure.

```
┌────────────────────────────────────────────────────────────────────────┐
│                          generate_docs.py                              │
│                                                                        │
│  ┌──────────────────────┐    ┌──────────────────┐    ┌──────────────┐  │
│  │    Config Parser     │───►│  GitHub Scraper  │───►│  LLM Client  │  │
│  └──────────────────────┘    └────────┬─────────┘    └──────┬───────┘  │
│                                       │                     │          │
│                                       ▼                     ▼          │
│  ┌──────────────────────┐    ┌──────────────────┐    ┌──────────────┐  │
│  │   Output Generator   │◄───│  Doc Linker Engine│◄───│ Prompt Builder│  │
│  └──────────────────────┘    └──────────────────┘    └──────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

The script is broken down into modular procedural tasks:
1. **Config Parser**: Reads the `config.json` schema to identify the target Git repository.
2. **GitHub Repository Scraper**: Authenticates with GitHub via a personal access token (`GITHUB_TOKEN`) and parses the target repository using `PyGithub`. It collects:
   * **Base Readme**: Fetches primary descriptions.
   * **Project Manifests/Dependency Files**: Inspects manifest files (e.g., `package.json`, `requirements.txt`, `pom.xml`, `go.mod`, `Cargo.toml`) to automatically identify the codebase's languages, frameworks, and developer environments.
   * **CI/CD Configuration**: Evaluates existing GitHub actions pipelines within `.github/workflows/` to understand building/testing workflows.
3. **Prompt Builder & Context Window Optimizer**: Programmatically creates systemic prompt contexts injected with scraped codebase metadata.
4. **LLM Client Interface**: Handles payload delivery and TLS handshaking with Google's Gemini API via the `google-generativeai` SDK.
5. **Document Linker Engine (Pagination)**: Iterates over generated buffers, dynamically prepends/appends markdown pagination markers, and builds sequential navigation footers (e.g., linking `overview.md` to `architecture_components.md`).
6. **Output File Generator**: Persists the structured Markdown outputs into the local `/docs` file tree.

### 2.4 Automation and Deployment Layer (`.github/workflows/main.yml`)
The continuous integration and GitOps delivery pipelines are governed by a GitHub Actions YAML configuration.
* **Activation Trigger**: Runs exclusively when pushes containing modifications to `config.json` are committed to the `main` branch.
* **Execution Environment**: Installs and provisions a secure runner instance running `ubuntu-latest`.
* **Execution Lifecycle**:
  1. **Checkout Action**: Clones the host repository.
  2. **Python Environment Setup**: Provisions `python3.x` with caching enabled for PyPI dependencies.
  3. **Dependency Resolution**: Installs critical SDKs (`PyGithub`, `google-generativeai`).
  4. **Engine Execution**: Runs `generate_docs.py` using repository-injected secrets.
  5. **Auto-PR/Commit Action**: Automatically creates a pull request or pushes code directly back to the active repository, updating the `/docs` directory.

---

## 3. Data Flow and Integration Patterns

The sequence diagram below displays the real-time processing chain executed during a single automation cycle:

```
┌──────┐          ┌──────────────┐       ┌──────────────┐       ┌────────────┐       ┌────────────┐
│ User │          │  Git Commit  │       │ PyGithub API │       │ Gemini API │       │ local /docs│
└──┬───┘          └──────┬───────┘       └──────┬───────┘       └─────┬──────┘       └─────┬──────┘
   │                     │                      │                     │                    │
   │ Commit config.json  │                      │                     │                    │
   ├────────────────────►│                      │                     │                    │
   │                     │                      │                     │                    │
   │                     │ Trigger Action       │                     │                    │
   │                     ├─────────────────────►│                     │                    │
   │                     │                      │                     │                    │
   │                     │ Fetch Target Repo Metadata                 │                    │
   │                     ├─────────────────────►│                     │                    │
   │                     │                      │                     │                    │
   │                     │◄─────────────────────┤                     │                    │
   │                     │ Return Target Readme & Dependencies        │                    │
   │                     │                      │                     │                    │
   │                     │ Build Prompt Payload & Request Document Synthesis                │
   │                     ├───────────────────────────────────────────►│                    │
   │                     │                      │                     │                    │
   │                     │◄───────────────────────────────────────────┤                    │
   │                     │ Return 3-Part Markdown Text Stream         │                    │
   │                     │                      │                     │                    │
   │                     │ Post-process, paginate & generate internal navigation links     │
   │                     ├────────────────────────────────────────────────────────────────►│
   │                     │                      │                     │                    │
   │                     │                      │                     │                    │ Create Pull Request
   │                     ├─────────────────────────────────────────────────────────────────┼──────────┐
   │                     │◄────────────────────────────────────────────────────────────────┼──────────┘
   │                     │                                                                 │
```

### 3.1 GitHub API Integration Strategy (`PyGithub`)
The application fetches target repository signals via high-performance REST APIs. It relies on the token context to bypass heavy rate limits applied to unauthenticated IP addresses:
* **Repository Analysis**: Resolves the namespace owner and repository string.
* **Content Scoping**: Extracts target `README.md` raw contents.
* **Dependency Fingerprinting**: Searches for explicit manifest profiles to reconstruct the project's application profile without downloading the full source tree.

### 3.2 Google Gemini API Integration Strategy (`google-generativeai`)
SmartGen Docs uses Google Gemini to generate documentation from collected project information. The integration utilizes a custom prompting technique:
* **System Prompt Constraints**: Restricts the model from writing hypothetical explanations. It enforces explicit technical alignment with the dependencies, build tools, and structure retrieved from the GitHub API.
* **Three-Part Output Synthesis**: The LLM engine is prompted to return documentation split into three distinct files:
  1. `overview.md`: High-level value propositions, features, and technology summary.
  2. `architecture_components.md`: System topology, component interactions, and modular layout.
  3. `setup_guidelines.md`: Exact installation, execution, configuration steps, and environment settings.

---

## 4. GitOps Workflow and Security Design

```
             ┌────────────────────────────────────────────────────────┐
             │                  Developer Workstation                 │
             │           Modifies target link in config.json          │
             └───────────────────────────┬────────────────────────────┘
                                         │
                                         ▼
             ┌────────────────────────────────────────────────────────┐
             │                     GitHub Remote                      │
             │      Validates secrets (GITHUB_TOKEN, GEMINI_API_KEY)  │
             └───────────────────────────┬────────────────────────────┘
                                         │
                                         ▼
             ┌────────────────────────────────────────────────────────┐
             │                 GitHub Actions Runner                  │
             │            Executes containerized script               │
             └───────────────────────────┬────────────────────────────┘
                                         │
                                         ▼
             ┌────────────────────────────────────────────────────────┐
             │                   PR Generation Phase                  │
             │   Proposes updates isolated to safe feature-branch      │
             └────────────────────────────────────────────────────────┘
```

### 4.1 Push-to-Trigger Mechanics
To reduce continuous deployment (CD) resource waste, the workflow triggers only on pushes that modify the `config.json` file. This is configured in the action workflow as:
```yaml
on:
  push:
    paths:
      - 'config.json'
```

### 4.2 Security and Secrets Architecture
The system employs strict separation of secrets to prevent security issues when handling access tokens:
* **Credential Injection**: No API keys or tokens are stored in the code. Secret variables are injected into the runner's execution shell environment at runtime:
  * `GITHUB_TOKEN`: Manages read/write privileges for the hosting repository to parse dependency profiles and write back pull requests.
  * `GEMINI_API_KEY`: Authenticates calls to Google's AI services.
* **Output Quarantine**: Generated files are not forced directly into protected production branches. Instead, the workflow generates a branch and opens a Pull Request. This provides a manual review step where developers can verify AI-generated text before merging it into their main branch.

---

## 5. Performance and Scalability Considerations

| Vector | Challenge | Mitigation Strategy |
| :--- | :--- | :--- |
| **GitHub API Rate Limits** | Unauthenticated requests are limited to 60/hour. | The pipeline utilizes authenticated connections via custom-configured personal access tokens (PATs), raising limits to 5,000 requests per hour. |
| **LLM Context Window Limit** | Heavy codebases with complex sub-directories can overflow traditional LLM input contexts. | Instead of scanning and submitting every source file, the orchestrator only retrieves dependency manifest trees and README structures, keeping the input context compact and efficient. |
| **Concurrent Execution Collisions** | Multiple commits pushed in rapid succession can trigger race conditions on target output branches. | GitHub Actions are configured with concurrency group cancellation rules, instantly aborting older pending runs when a newer commit is pushed. |

---

[< Previous: Overview](/overview.md) | [Next: Setup Guidelines >](/setup_guidelines.md)