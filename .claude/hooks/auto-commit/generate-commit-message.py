#!/usr/bin/env python3
"""
Generate intelligent commit messages using Claude API.
Analyzes git diffs to create meaningful conventional commit messages.
"""

import os
import sys
import json

def generate_commit_message(diff_text: str, file_list: str) -> tuple[str, str, str]:
    """
    Generate commit message using Claude API.

    Args:
        diff_text: Git diff output
        file_list: Newline-separated list of changed files

    Returns:
        Tuple of (commit_type, scope, description)

    Raises:
        Exception: If API call fails or API key not found
    """
    try:
        from anthropic import Anthropic
    except ImportError:
        raise Exception("anthropic package not installed")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise Exception("ANTHROPIC_API_KEY not set")

    client = Anthropic(api_key=api_key)

    # Truncate diff if too large (Claude has token limits)
    max_diff_length = 50000
    if len(diff_text) > max_diff_length:
        diff_text = diff_text[:max_diff_length] + "\n\n... (diff truncated)"

    prompt = f"""Analyze this git diff and generate a concise conventional commit message.

Changed files:
{file_list}

Git diff:
{diff_text}

Generate a commit message following conventional commits format. Respond with ONLY a JSON object in this exact format:
{{
  "type": "feat|fix|docs|refactor|test|build|ci|chore",
  "scope": "optional-scope-from-primary-directory",
  "description": "short description in imperative mood (max 50 chars)"
}}

Rules:
- type: Choose the most appropriate conventional commit type
- scope: Use the primary directory name if appropriate (e.g., "src", "docs"), or leave empty
- description: Be specific and concise, use imperative mood (e.g., "add user auth", not "added user auth")
- Focus on WHAT changed, not HOW it changed
- Avoid generic descriptions like "update files" or "make changes"

Examples:
- feat(auth): add password validation
- fix(api): handle null responses correctly
- docs(readme): update installation steps
- refactor(utils): simplify error handling
- test(user): add edge case coverage

Respond with ONLY the JSON object, no other text."""

    try:
        message = client.messages.create(
            model="claude-3-5-haiku-20241022",  # Fast and cheap for this task
            max_tokens=150,
            temperature=0.3,  # Low temp for consistent, focused responses
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        response_text = message.content[0].text.strip()

        # Extract JSON (handle markdown code blocks if present)
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        data = json.loads(response_text)

        commit_type = data.get("type", "chore")
        scope = data.get("scope", "")
        description = data.get("description", "update files")

        return (commit_type, scope, description)

    except Exception as e:
        raise Exception(f"API call failed: {str(e)}")


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: generate-commit-message.py <diff-file> <files-file>", file=sys.stderr)
        sys.exit(1)

    diff_file = sys.argv[1]
    files_file = sys.argv[2]

    try:
        with open(diff_file, 'r') as f:
            diff_text = f.read()

        with open(files_file, 'r') as f:
            file_list = f.read()

        commit_type, scope, description = generate_commit_message(diff_text, file_list)

        # Output in format: type|scope|description
        print(f"{commit_type}|{scope}|{description}")
        sys.exit(0)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
