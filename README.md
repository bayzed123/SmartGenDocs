
# SmartGen Docs - Zero-Configuration Auto-Docs Platform

## Overview

**SmartGen Docs** is an innovative, zero-configuration documentation automation platform that leverages AI to generate comprehensive, high-quality documentation for open-source projects. By simply providing a GitHub repository link, the platform automatically generates three unique markdown documents: an Overview, Architecture/Components guide, and Setup Guidelines. The entire workflow is powered by GitOps principles and integrated with Google's Gemini API for intelligent content generation.

## Key Features

- **Zero Configuration**: Simply add a GitHub repository link to `config.json` and push to trigger automatic documentation generation.
- **AI-Powered Content Generation**: Uses Google Gemini API to generate unique, high-quality documentation.
- **GitOps Workflow**: Fully automated CI/CD pipeline using GitHub Actions.
- **Three-Document Structure**: Generates Overview, Architecture/Components, and Setup Guidelines.
- **Automatic Pagination**: Generated documents include navigation links for seamless browsing.
- **Premium UI**: Dark-themed landing page with glassmorphism design using Tailwind CSS.

## Architecture

### System Components

1. **Frontend**: `index.html` - Premium dark-themed landing page with Tailwind CSS
2. **Python Automation Script**: `generate_docs.py` - Fetches repository data and generates documentation
3. **GitHub Actions Workflow**: Triggers on `config.json` changes and orchestrates the documentation generation
4. **Configuration File**: `config.json` - Contains the repository link to be documented

### Workflow

```
User updates config.json with GitHub repo link
    ↓
Push to main branch
    ↓
GitHub Actions workflow triggers
    ↓
Python script fetches repo data via GitHub API
    ↓
Data sent to Gemini API for processing
    ↓
Three markdown files generated (Overview, Architecture, Setup)
    ↓
Pagination links added
    ↓
Files saved to /docs directory
    ↓
Auto-commit back to repository via Pull Request
```

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- GitHub account with a public repository
- Google Gemini API key
- GitHub Personal Access Token

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bayzed123/SmartGenDocs.git
   cd SmartGenDocs
   ```

2. **Install Python dependencies**:
   ```bash
   pip install PyGithub google-generativeai
   ```

3. **Set up environment variables**:
   ```bash
   export GITHUB_TOKEN="your_github_token"
   export GEMINI_API_KEY="your_gemini_api_key"
   ```

4. **Configure the target repository**:
   Edit `config.json` and add the GitHub repository link:
   ```json
   {
     "repository_link": "https://github.com/owner/repository"
   }
   ```

5. **Push to trigger automation**:
   ```bash
   git add config.json
   git commit -m "Add repository link for documentation"
   git push origin main
   ```

### Manual Execution

To run the documentation generation script manually:

```bash
python generate_docs.py "https://github.com/owner/repository"
```

## File Structure

```
SmartGenDocs/
├── index.html                 # Landing page UI
├── generate_docs.py          # Python automation script
├── config.json               # Configuration file
├── README.md                 # This file
├── docs/                     # Generated documentation
│   ├── overview.md
│   ├── architecture_components.md
│   └── setup_guidelines.md
└── .github/
    └── workflows/
        └── main.yml          # GitHub Actions workflow
```

## Usage

### Step 1: Configure Repository Link
Edit `config.json` with your target repository:
```json
{
  "repository_link": "https://github.com/your-org/your-repo"
}
```

### Step 2: Push Changes
```bash
git add config.json
git commit -m "Update repository link"
git push origin main
```

### Step 3: Monitor Workflow
The GitHub Actions workflow will automatically trigger. Monitor the workflow run in the Actions tab of your repository.

### Step 4: Review Generated Documentation
Once the workflow completes, a pull request will be created with the generated documentation in the `docs/` directory.

## Configuration

### config.json

The main configuration file contains the GitHub repository link:

```json
{
  "repository_link": "https://github.com/owner/repository"
}
```

## API Integration

### GitHub API

The script uses the PyGithub library to fetch:
- README.md content
- Package/dependency files (package.json, requirements.txt, pom.xml, etc.)
- GitHub Actions workflow files

### Gemini API

The script sends repository data to Google Gemini API for generating:
- **Overview**: High-level project description
- **Architecture/Components**: Technical architecture details
- **Setup Guidelines**: Installation and setup instructions

## GitHub Actions Workflow

The workflow is triggered on:
- **Event**: Push to main branch
- **Condition**: Changes to `config.json`

The workflow performs:
1. Checks out the repository
2. Sets up Python environment
3. Installs dependencies
4. Reads repository link from config.json
5. Executes the documentation generation script
6. Creates a pull request with generated documentation

## Security

- GitHub Token and Gemini API Key are stored as GitHub Secrets
- Never commit sensitive credentials to the repository
- Use environment variables for local development

## Troubleshooting

### Common Issues

**Issue**: "No README.md found"
- **Solution**: Ensure the target repository has a README.md file

**Issue**: "Workflow fails to trigger"
- **Solution**: Verify that `config.json` is properly formatted and the repository link is valid

**Issue**: "API rate limits exceeded"
- **Solution**: Wait for the rate limit to reset or upgrade your API plan

## Contributing

Contributions are welcome! Please follow these guidelines:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

## Roadmap

- [ ] Support for multiple repository links
- [ ] Custom documentation templates
- [ ] Integration with other AI models
- [ ] Web-based dashboard for configuration
- [ ] Scheduled documentation updates

## Acknowledgments

- Built with [PyGithub](https://github.com/PyGithub/PyGithub)
- Powered by [Google Gemini API](https://ai.google.dev/)
- UI crafted with [Tailwind CSS](https://tailwindcss.com/)

---

**SmartGen Docs** - Automating documentation for the open-source community.
