import os
from typing import Dict, Any, Optional
from google import genai
from google.genai import types


class GemmaService:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.model = os.getenv("GEMMA_MODEL", "gemma-3-1b-it")
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None

    def generate_readme(self, repo_data: Dict[str, Any]) -> str:
        if not self.client:
            raise Exception("Google API key not configured")

        prompt = self._build_prompt(repo_data)
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=4096,
                    top_p=0.95,
                ),
            )
            return self._extract_markdown(response.text if hasattr(response, "text") else str(response))
        except Exception as e:
            raise Exception(f"README generation failed: {str(e)}")

    def _build_prompt(self, repo_data: Dict[str, Any]) -> str:
        file_contents = repo_data.get("file_contents", {})
        contents_str = "\n\n".join([f"=== {path} ===\n{c}" for path, c in file_contents.items()])

        prompt = f"""You are an expert technical documentation writer. Generate a professional GitHub README.md using ONLY information provided. Do NOT invent features, commands, dependencies, APIs, databases, environment variables, licenses, or installation steps unless explicitly supported by the evidence.

REPOSITORY ANALYSIS:
- Name: {repo_data.get('name')}
- Owner: {repo_data.get('owner')}/{repo_data.get('repo')}
- Description: {repo_data.get('description')}
- Language: {repo_data.get('language')}
- Languages: {repo_data.get('languages')}
- Topics: {repo_data.get('topics')}
- Default branch: {repo_data.get('default_branch')}
- Important files: {repo_data.get('important_files')}

REPOSITORY STRUCTURE:
{repo_data.get('structure')}

FILE CONTENTS (evidence):
{contents_str}

INSTRUCTIONS:
1. Generate clean Markdown - do NOT wrap in ```markdown ``` block.
2. Include sections only if supported by evidence. Omit if insufficient evidence.
3. Suggested sections if applicable: # Project Name, ## Overview, ## Features, ## Tech Stack, ## Installation, ## Usage, ## Project Structure, ## Configuration, ## Screenshots (omit if no evidence), ## Future Improvements (only if obvious from evidence), ## License (only if found in files).
4. If information is missing, omit rather than guessing.
5. Focus on factual description based on structure, languages, dependencies in files.
6. Return ONLY the markdown content.
"""
        return prompt

    def _extract_markdown(self, text: str) -> str:
        if not text:
            return ""
        # Remove markdown code fences if present
        text = text.strip()
        if text.startswith("```"):
            lines = text.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip().startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines)
        return text
