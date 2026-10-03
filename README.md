# RepoScribe

RepoScribe is an AI-powered GitHub README generator that analyzes public GitHub repositories and generates professional README.md files using Gemma 4 via Google AI Studio API.

## Problem
Writing comprehensive, well-structured documentation for GitHub repositories is time-consuming. RepoScribe automates this process by analyzing repository structure, dependencies, and code to generate high-quality documentation.

## Solution
RepoScribe accepts a public GitHub repository URL, fetches and analyzes repository metadata and key files, then uses Gemma 4 to generate a clean, factual README based solely on the analyzed information.

## Features
- **GitHub Repository Analysis**: Extracts languages, frameworks, structure, and important configuration files
- **AI-Powered Generation**: Leverages Gemma 4 through Google AI Studio API
- **Markdown Preview**: Real-time preview of generated README as it would appear on GitHub
- **Copy & Download**: Easy copy to clipboard or download as README.md
- **Privacy-Focused**: API keys remain server-side; frontend never sees secrets
- **Error Handling**: Graceful handling of invalid URLs, missing repos, API failures
- **Lightweight**: Minimal dependencies, simple architecture optimized for Vercel deployment

## Architecture
- **Backend**: Flask (Python) - lightweight web framework for API routes
- **Frontend**: Vanilla HTML, CSS, JavaScript - no heavy frontend framework needed
- **AI**: Google AI Studio API with Gemma 4 (configurable model via environment variable)
- **GitHub API**: Public REST API v3 for repository metadata and file content
- **Deployment**: Vercel (Python serverless functions)

### Data Flow
1. User enters GitHub repository URL
2. Parse owner/repository
3. Fetch repo info, languages, and file tree from GitHub API
4. Analyze structure and extract important files (with size limits)
5. Send structured analysis to Gemma 4 via Google AI Studio
6. Generate and display README with Markdown preview
7. User can copy or download the result

## Tech Stack
- Python 3.12+
- Flask 3.0.3
- google-genai 1.0.0
- requests 2.32.3
- python-dotenv 1.0.1
- markdown 3.7
- Vanilla JS + Marked.js + DOMPurify for Markdown rendering

## Prerequisites
- Python 3.12+
- Google AI Studio API key ([Get one here](https://aistudio.google.com/apikey))
- (Optional) GitHub Personal Access Token for higher API rate limits

## Local Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/reposcribe.git
cd reposcribe
```

2. Create virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```
Edit `.env` and add your API keys.

5. Run the application:
```bash
python app.py
```

6. Open [http://localhost:5000](http://localhost:5000) in your browser.

## Environment Variables

| Variable | Description | Required | Default |
|---|---|---|---|
| `GOOGLE_API_KEY` | Google AI Studio API key | Yes | - |
| `GEMMA_MODEL` | Gemma model name (e.g., `gemma-3-4b-it`, `gemma-3-1b-it`, `gemma-3-12b-it`) | No | `gemma-3-1b-it` |
| `GITHUB_TOKEN` | GitHub Personal Access Token (optional, increases rate limits) | No | - |
| `MAX_FILES_ANALYZE` | Max number of important files to analyze | No | `20` |
| `MAX_CHARS_PER_FILE` | Max characters per file sent to AI | No | `20000` |
| `MAX_TOTAL_CHARS` | Max total characters sent to AI | No | `200000` |

## Usage

1. Navigate to the web app
2. Paste a public GitHub repository URL (e.g., `https://github.com/user/project`)
3. Click "Analyze Repository" to extract project information
4. Review the analysis results
5. Click "Generate README" to create documentation with Gemma
6. Preview the generated README, then Copy or Download as `README.md`

## Testing Recommendations

Test with a variety of public repositories:
- Python projects (Django/Flask)
- JavaScript/Node projects
- Small/simple repositories
- Repos with/without existing READMEs
- Invalid URLs and non-existent repos

## Security

- API keys are never exposed to the frontend - stored as server-side environment variables
- `.env` is in `.gitignore` and never committed
- Only analyzes public repositories (no GitHub OAuth required)
- Content sent to AI is limited and sanitized

## Deployment to Vercel

### Option 1: Vercel CLI
```bash
npm i -g vercel
vercel login
vercel
```

### Option 2: GitHub Integration
1. Push this repository to GitHub
2. Go to [Vercel](https://vercel.com/)
3. Import the GitHub repository
4. Configure environment variables in Vercel Dashboard (Project Settings > Environment Variables):
   - `GOOGLE_API_KEY`
   - `GEMMA_MODEL`
   - `GITHUB_TOKEN` (optional)
5. Deploy

The `vercel.json` configuration handles Python serverless function setup.

## Limitations
- Only works with public GitHub repositories
- Large repositories may be truncated based on configured limits
- AI generation quality depends on available file evidence
- Follows principle: only generates what’s supported by repository analysis (no invented features)

## Future Improvements
- GitHub Pull Request integration to commit generated README
- Custom README templates
- Multi-language README support
- Batch repository processing

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Built for hackathon using Gemma 4 via Google AI Studio
- Powered by GitHub REST API
"