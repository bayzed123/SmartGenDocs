
# SmartGen Docs Wiki

Welcome to the official Wiki for **SmartGen Docs**. This guide provides in-depth technical details, workflow explanations, and advanced usage instructions for the platform.

## 📌 Table of Contents
1. [Introduction](#introduction)
2. [Core Architecture](#core-architecture)
3. [The AI Engine (Gemini 3.5 Flash)](#the-ai-engine)
4. [GitOps Workflow](#gitops-workflow)
5. [Troubleshooting](#troubleshooting)
6. [Developer Credits](#developer-credits)

---

## 1. Introduction
SmartGen Docs is designed to solve the problem of outdated or missing documentation in open-source projects. By using a "Link-to-Docs" approach, it removes the friction of manual writing and keeps documentation in sync with the codebase.

## 2. Core Architecture
The platform is built on three main pillars:
- **Python Backend**: Handles repository fetching via the GitHub API and coordinates with the Gemini API.
- **GitHub Actions**: Acts as the orchestrator, triggering scans on every push to the `input_links/` folder.
- **Tailwind CSS Frontend**: A premium, glassmorphism-based UI that serves as the portal for all generated documentation.

## 3. The AI Engine
We use **Google Gemini 3.5 Flash** to analyze repositories. The engine doesn't just copy text; it understands:
- **Codebase Structure**: Identifying key components and their roles.
- **Dependencies**: Extracting setup requirements from `package.json`, `requirements.txt`, etc.
- **Workflows**: Understanding CI/CD pipelines to generate accurate deployment guides.

## 4. GitOps Workflow
The system follows a strict GitOps pattern:
1. **Input**: User commits a link to `input_links/`.
2. **Trigger**: GitHub Actions detects the change.
3. **Process**: The Python script runs, generating both Markdown and HTML files.
4. **Output**: The script commits the new files back to the `main` branch.
5. **Live**: The documentation is instantly available via unique URLs in the `docs/` folder.

## 5. Troubleshooting
- **Invalid URL**: Ensure your link starts with `https://github.com/`.
- **Private Repos**: Currently, the system only supports **public** repositories.
- **Quota Limits**: If documentation fails to generate, check your Gemini API quota.

## 6. Developer Credits
**SmartGen Docs** is envisioned and developed by:
### **Sayad Md Bayezid Hosan**
🌐 [Official Website](https://www.sayadbayezid.com)
🐙 [GitHub Profile](https://github.com/bayzed123)

---

*Last Updated: June 2026*
