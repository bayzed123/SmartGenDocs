
import os
import argparse
from github import Github
import google.generativeai as genai

# --- Configuration --- #
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# --- Helper Functions --- #
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
        print("No README.md found.")

    # Fetch package/dependency files (common ones)
    package_file_names = ["package.json", "requirements.txt", "pom.xml", "build.gradle", "go.mod", "Cargo.toml"]
    for file_name in package_file_names:
        try:
            file_content = repo.get_contents(file_name)
            content["package_files"][file_name] = file_content.decoded_content.decode()
        except Exception:
            pass # File not found

    # Fetch workflow files
    try:
        workflow_dir = repo.get_contents(".github/workflows")
        for file_content in workflow_dir:
            if file_content.type == "file":
                content["workflow_files"][file_content.name] = file_content.decoded_content.decode()
    except Exception:
        print("No .github/workflows directory found.")

    return content

def generate_markdown(model, prompt_template, repo_data, doc_type):
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
    parser = argparse.ArgumentParser(description="Generate documentation for a GitHub repository using Gemini AI.")
    parser.add_argument("repo_link", help="Public GitHub repository link (e.g., https://github.com/owner/repo)")
    args = parser.parse_args()

    repo_full_name = args.repo_link.split("github.com/")[1]

    print(f"Fetching content for {repo_full_name}...")
    repo_data = get_repo_content(repo_full_name)

    model = genai.GenerativeModel("gemini-pro")

    # Define prompt templates
    overview_prompt = """
    You are an expert technical writer. Based on the following GitHub repository data, generate a comprehensive 'Overview' of the project. 
    Explain what the project is, its main purpose, and why it is useful. Focus on a high-level understanding for potential users and contributors.

    Repository Data:
    {repo_data}

    Generate the overview in Markdown format.
    """

    architecture_prompt = """
    You are an expert software architect. Based on the following GitHub repository data, generate a detailed 'Architecture/Components' document.
    Explain how the project is built under the hood, its key components, technologies used, and their interactions. 
    Assume the audience is technical developers.

    Repository Data:
    {repo_data}

    Generate the architecture document in Markdown format.
    """

    setup_guidelines_prompt = """
    You are an expert DevOps engineer. Based on the following GitHub repository data, generate 'Setup Guidelines' for the project.
    Extract the exact installation and setup commands, but rewrite the explanations uniquely and clearly. 
    Provide step-by-step instructions for getting the project up and running.

    Repository Data:
    {repo_data}

    Generate the setup guidelines in Markdown format.
    """

    doc_types = {
        "overview": overview_prompt,
        "architecture_components": architecture_prompt,
        "setup_guidelines": setup_guidelines_prompt
    }

    generated_docs = {}
    for doc_name, prompt_template in doc_types.items():
        print(f"Generating {doc_name.replace('_', ' ').title()}...")
        generated_docs[doc_name] = generate_markdown(model, prompt_template, repo_data, doc_name)

    # Save documents and add pagination
    doc_order = ["overview", "architecture_components", "setup_guidelines"]
    for doc_name in doc_order:
        file_name = f"{doc_name}.md"
        pagination = create_pagination(doc_name, doc_order)
        
        # Append pagination only if it's not empty
        final_content = generated_docs[doc_name]
        if pagination:
            final_content += f"\n\n---\n\n{pagination}"

        with open(f"docs/{file_name}", "w") as f:
            f.write(final_content)
        print(f"Saved docs/{file_name}")

    # TODO: Auto-commit changes back to the repository (will be handled by GitHub Actions or a separate step)

if __name__ == "__main__":
    main()
