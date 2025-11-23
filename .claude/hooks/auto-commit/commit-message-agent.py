#!/usr/bin/env python3
"""
Commit Message Generation Agent

An autonomous agent powered by Claude Haiku that analyzes git diffs and generates
intelligent, context-aware commit messages following conventional commit standards.

This agent operates independently, reasoning about code changes to produce
meaningful commit messages that accurately describe what changed and why.
"""

import os
import sys
import json
from typing import Tuple


class CommitMessageAgent:
    """
    Autonomous agent for generating commit messages.

    Uses Claude 3.5 Haiku model for fast, cost-effective analysis of code changes.
    """

    MODEL = "claude-3-5-haiku-20241022"
    MAX_DIFF_LENGTH = 50000  # Token limit consideration

    SYSTEM_PROMPT = """You are an expert software engineer specialized in writing clear,
meaningful commit messages. You analyze code changes and generate commit messages that
accurately describe WHAT changed and WHY it matters.

Your task is to:
1. Analyze the provided git diff carefully
2. Understand the scope and intent of the changes
3. Identify the primary type of change
4. Generate a concise, specific commit message

Follow conventional commit format strictly:
- type: feat|fix|docs|refactor|test|build|ci|chore
- scope: primary directory or component (optional)
- description: imperative mood, specific, max 50 chars

Be specific. Avoid generic descriptions like "update files" or "make changes".
Focus on the business logic or functional impact, not implementation details."""

    def __init__(self):
        """Initialize the agent with API credentials."""
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise EnvironmentError("ANTHROPIC_API_KEY not set")

        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("anthropic package not installed: pip install anthropic")

    def analyze_changes(self, diff_text: str, file_list: str) -> Tuple[str, str, str]:
        """
        Analyze git changes and generate commit message components.

        Args:
            diff_text: Full git diff output
            file_list: Newline-separated list of changed files

        Returns:
            Tuple of (type, scope, description)

        Raises:
            Exception: If agent fails to generate valid commit message
        """
        # Truncate diff if too large
        if len(diff_text) > self.MAX_DIFF_LENGTH:
            diff_text = diff_text[:self.MAX_DIFF_LENGTH] + "\n\n[... diff truncated for length]"

        user_prompt = self._build_analysis_prompt(diff_text, file_list)

        try:
            response = self.client.messages.create(
                model=self.MODEL,
                max_tokens=200,
                temperature=0.2,  # Low temp for consistent, focused analysis
                system=self.SYSTEM_PROMPT,
                messages=[{
                    "role": "user",
                    "content": user_prompt
                }]
            )

            result_text = response.content[0].text.strip()
            return self._parse_response(result_text)

        except Exception as e:
            raise Exception(f"Agent analysis failed: {str(e)}")

    def _build_analysis_prompt(self, diff_text: str, file_list: str) -> str:
        """Build the analysis prompt for the agent."""
        return f"""Analyze this code change and generate a commit message.

CHANGED FILES:
{file_list}

GIT DIFF:
{diff_text}

Generate a commit message following conventional commits format.

Respond with ONLY a JSON object:
{{
  "type": "feat|fix|docs|refactor|test|build|ci|chore",
  "scope": "primary-directory-or-component",
  "description": "specific description in imperative mood"
}}

Examples of GOOD descriptions:
- "add password validation to registration"
- "fix null pointer in user service"
- "extract email validation to utility"
- "add integration tests for auth flow"

Examples of BAD descriptions (too generic):
- "update files"
- "make changes"
- "add new functionality"
- "fix bugs"

Analyze the changes and respond with the JSON object only."""

    def _parse_response(self, response_text: str) -> Tuple[str, str, str]:
        """Parse agent response into commit message components."""
        # Extract JSON from response (handle markdown code blocks)
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        try:
            data = json.loads(response_text)
            commit_type = data.get("type", "chore").strip()
            scope = data.get("scope", "").strip()
            description = data.get("description", "update files").strip()

            # Validate type
            valid_types = {"feat", "fix", "docs", "refactor", "test", "build", "ci", "chore"}
            if commit_type not in valid_types:
                commit_type = "chore"

            return (commit_type, scope, description)

        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse agent response: {str(e)}")


def main():
    """Main entry point for the commit message agent."""
    if len(sys.argv) < 3:
        print("Usage: commit-message-agent.py <diff-file> <files-file>", file=sys.stderr)
        print("", file=sys.stderr)
        print("This agent analyzes git changes and generates conventional commit messages.", file=sys.stderr)
        print(f"Model: {CommitMessageAgent.MODEL}", file=sys.stderr)
        sys.exit(1)

    diff_file = sys.argv[1]
    files_file = sys.argv[2]

    try:
        # Load input files
        with open(diff_file, 'r', encoding='utf-8', errors='ignore') as f:
            diff_text = f.read()

        with open(files_file, 'r', encoding='utf-8', errors='ignore') as f:
            file_list = f.read()

        # Initialize and run agent
        agent = CommitMessageAgent()
        commit_type, scope, description = agent.analyze_changes(diff_text, file_list)

        # Output in format: type|scope|description
        print(f"{commit_type}|{scope}|{description}")
        sys.exit(0)

    except EnvironmentError as e:
        print(f"Configuration error: {str(e)}", file=sys.stderr)
        sys.exit(2)
    except ImportError as e:
        print(f"Dependency error: {str(e)}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Agent error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
