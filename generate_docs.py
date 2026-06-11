
import os
import argparse
import glob
import re
from github import Github
import google.generativeai as genai

# --- Configuration --- #
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# --- Helper Functions --- #
def validate_github_url(url):
    """Validates if the string is a valid GitHub repository URL."""
    pattern = r"https?://github\.com/[\w\.-]+/[\w\.-]+"
    return re.match(pattern, url)

def get_repo_content(repo_full_name):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(repo_full_name)

    content = {
        "readme": "",
        "package_files": {},
        "workflow_files": {}
    }

    try:
        readme = repo.get_contents("README.md")
        content["readme"] = readme.decoded_content.decode()
    except Exception:
        print(f"No README.md found for {repo_full_name}.")

    package_file_names = ["package.json", "requirements.txt", "pom.xml", "build.gradle", "go.mod", "Cargo.toml"]
    for file_name in package_file_names:
        try:
            file_content = repo.get_contents(file_name)
            content["package_files"][file_name] = file_content.decoded_content.decode()
        except Exception:
            pass

    try:
        workflow_dir = repo.get_contents(".github/workflows")
        for file_content in workflow_dir:
            if file_content.type == "file":
                content["workflow_files"][file_content.name] = file_content.decoded_content.decode()
    except Exception:
        pass

    return content

def generate_markdown(model, prompt_template, repo_data):
    prompt = prompt_template.format(repo_data=repo_data)
    response = model.generate_content(prompt)
    return response.text

def create_pagination(current_doc, all_docs):
    pagination_links = []
    current_index = all_docs.index(current_doc)

    if current_index > 0:
        prev_doc = all_docs[current_index - 1]
        pagination_links.append(f"[< Previous: {prev_doc.replace('_', ' ').title()}](/{prev_doc}.md)")

    if current_index < len(all_docs) - 1:
        next_doc = all_docs[current_index + 1]
        pagination_links.append(f"[Next: {next_doc.replace('_', ' ').title()} >](/{next_doc}.md)")

    return " | ".join(pagination_links)

# --- Main Logic --- #
def main():
    parser = argparse.ArgumentParser(description="Generate documentation for GitHub repositories.")
    parser.add_argument("--input_folder", default="input_links", help="Folder containing text files with repo links")
    args = parser.parse_args()

    raw_links = []
    # Scan input_folder for any .txt or .md files containing links
    files = glob.glob(os.path.join(args.input_folder, "*"))
    for file_path in files:
        if os.path.isfile(file_path) and not file_path.endswith(".gitkeep"):
            with open(file_path, "r") as f:
                content = f.read().strip()
                if content:
                    # Split by lines or spaces in case multiple links are in one file
                    raw_links.extend(re.split(r'\s+', content))

    # URL Validation and Deduplication
    valid_links = []
    seen_repos = set()
    
    for link in raw_links:
        link = link.strip().rstrip("/")
        if validate_github_url(link):
            repo_path = link.split("github.com/")[1].lower()
            if repo_path not in seen_repos:
                valid_links.append(link)
                seen_repos.add(repo_path)
            else:
                print(f"Skipping duplicate repository: {link}")
        elif link:
            print(f"Skipping invalid GitHub URL: {link}")

    if not valid_links:
        print("No valid, unique repository links found to process.")
        return

    model = genai.GenerativeModel("gemini-3.5-flash")

    for repo_link in valid_links:
        try:
            repo_full_name = repo_link.split("github.com/")[1].strip("/")
            print(f"Processing {repo_full_name}...")
            repo_data = get_repo_content(repo_full_name)

            doc_prompts = {
                "overview": "Generate a unique 'Overview' for this project. Explain its value and purpose.\n\nData: {repo_data}",
                "architecture": "Generate an 'Architecture Guide'. Explain components and tech stack.\n\nData: {repo_data}",
                "deploy_guide": "Generate a unique 'Deployment Guide'. Provide step-by-step hosting/deployment instructions.\n\nData: {repo_data}",
                "how_to_use": "Generate a 'How to Use' guide. Provide clear usage examples and commands.\n\nData: {repo_data}"
            }

            doc_order = ["overview", "architecture", "deploy_guide", "how_to_use"]
            
            for doc_name in doc_order:
                print(f"Generating {doc_name}...")
                content = generate_markdown(model, doc_prompts[doc_name], repo_data)
                pagination = create_pagination(doc_name, doc_order)
                
                final_content = content + (f"\n\n---\n\n{pagination}" if pagination else "")
                
                os.makedirs("docs", exist_ok=True)
                with open(f"docs/{doc_name}.md", "w") as f:
                    f.write(final_content)
                print(f"Saved docs/{doc_name}.md")

        except Exception as e:
            print(f"Error processing {repo_link}: {e}")

if __name__ == "__main__":
    main()
