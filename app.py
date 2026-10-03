from flask import Flask, render_template, request, jsonify, send_file
from io import BytesIO
import os
from dotenv import load_dotenv

from services.github_service import GitHubService
from services.repository_analyzer import RepositoryAnalyzer
from services.gemma_service import GemmaService

load_dotenv()

app = Flask(__name__)

github_service = GitHubService()
analyzer = RepositoryAnalyzer(github_service)
gemma_service = GemmaService()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json() or {}
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "Please enter a GitHub repository URL."}), 400

    owner, repo = github_service.parse_repo_url(url)
    if not owner or not repo:
        return jsonify({"error": "Please enter a valid public GitHub repository URL."}), 400

    try:
        repo_info = github_service.get_repo_info(owner, repo)
    except Exception as e:
        msg = str(e)
        if "404" in msg:
            return jsonify({"error": "Repository not found or inaccessible."}), 404
        return jsonify({"error": "GitHub API failure."}), 500

    try:
        analyzed = analyzer.analyze(owner, repo, url)
        return jsonify({"success": True, "analysis": analyzed})
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json() or {}
    analysis = data.get("analysis", {})

    if not analysis:
        return jsonify({"error": "No analysis data provided."}), 400

    try:
        readme = gemma_service.generate_readme(analysis)
        return jsonify({"success": True, "readme": readme})
    except Exception as e:
        return jsonify({"error": "README generation failed. Please try again."}), 500


@app.route("/api/download", methods=["POST"])
def download():
    data = request.get_json() or {}
    readme = data.get("readme", "")
    if not readme:
        return jsonify({"error": "No README content."}), 400
    buffer = BytesIO(readme.encode("utf-8"))
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="README.md",
        mimetype="text/markdown",
    )


if __name__ == "__main__":
    app.run(debug=True)
