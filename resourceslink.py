import os

def generate_resources():
    docs_dir = "docs"
    # Ensure docs directory exists
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
        
    links = []
    # Scan docs folder for all .html files, excluding 404 and resources itself
    for filename in sorted(os.listdir(docs_dir)):
        if filename.endswith(".html") and filename not in ["404.html", "smartgen-resources.html"]:
            title = filename.replace(".html", "").replace("-", " ").title()
            links.append({"title": title, "url": filename})

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SmartGen Resources | SmartGenDocs</title>
    <style>
        body { font-family: sans-serif; line-height: 1.6; background: #f4f4f4; padding: 20px; }
        .container { max-width: 800px; margin: auto; }
        .card { background: white; border: 1px solid #ccc; padding: 20px; margin: 15px 0; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
        .card a { color: #4183c4; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>SmartGen Documentation Library</h1>
        <a href="https://bayzed123.github.io/SmartGenDocs/">← Back to Home</a>
"""

    for item in links:
        html_content += f'''
        <div class="card">
            <h3>{item['title']}</h3>
            <p>Access File: <a href="{item['url']}">{item['url']}</a></p>
        </div>'''

    html_content += "</div></body></html>"

    with open(os.path.join(docs_dir, "smartgen-resources.html"), "w") as f:
        f.write(html_content)

if __name__ == "__main__":
    generate_resources()