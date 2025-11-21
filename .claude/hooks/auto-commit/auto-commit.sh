#!/usr/bin/env bash
# Auto-commit hook for Claude Code
# Automatically commits changes after task completion with intelligent commit grouping

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RESET='\033[0m'

# Configuration
MAX_COMMIT_AGE_SECONDS=300  # 5 minutes - if last commit is older, create new commit
MIN_FILES_FOR_SPLIT=10      # If more than this many files changed, consider splitting

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Not a git repository, skipping auto-commit${RESET}" >&2
    exit 0
fi

# Check if there are any changes to commit
if git diff --quiet && git diff --cached --quiet; then
    echo "No changes to commit" >&2
    exit 0
fi

# Get the last commit info
LAST_COMMIT_TIMESTAMP=$(git log -1 --format=%ct 2>/dev/null || echo "0")
CURRENT_TIMESTAMP=$(date +%s)
TIME_SINCE_LAST_COMMIT=$((CURRENT_TIMESTAMP - LAST_COMMIT_TIMESTAMP))

# Get last commit message and author
LAST_COMMIT_MSG=$(git log -1 --format=%B 2>/dev/null || echo "")
LAST_COMMIT_AUTHOR=$(git log -1 --format=%an 2>/dev/null || echo "")

# Check if last commit was by Claude
IS_CLAUDE_COMMIT=false
if echo "$LAST_COMMIT_AUTHOR" | grep -q "Claude"; then
    IS_CLAUDE_COMMIT=true
fi

# Get changed files
CHANGED_FILES=$(git diff --name-only && git diff --cached --name-only | sort -u)
NUM_CHANGED_FILES=$(echo "$CHANGED_FILES" | wc -l | tr -d ' ')

# Get git diff for analysis
GIT_DIFF=$(git diff && git diff --cached)

# Analyze the changes to determine commit message
analyze_changes() {
    local diff="$1"
    local files="$2"

    # Determine the primary type of change
    local has_new_files=false
    local has_deletions=false
    local has_modifications=false
    local has_renames=false

    # Check file status
    while IFS= read -r file; do
        if [ -z "$file" ]; then continue; fi

        if git diff --cached --name-status | grep -q "^A.*$file"; then
            has_new_files=true
        elif git diff --cached --name-status | grep -q "^D.*$file"; then
            has_deletions=true
        elif git diff --cached --name-status | grep -q "^M.*$file"; then
            has_modifications=true
        elif git diff --cached --name-status | grep -q "^R.*$file"; then
            has_renames=true
        fi
    done <<< "$files"

    # Analyze content for commit type
    local commit_type="chore"
    local scope=""
    local description=""

    # Determine commit type based on changes
    if echo "$diff" | grep -q "test.*\.py\|test.*\.js\|test.*\.ts\|\.spec\.\|\.test\."; then
        commit_type="test"
        description="add/update tests"
    elif echo "$diff" | grep -q "^+.*function.*export\|^+.*export.*function\|^+.*class\|^+.*def "; then
        commit_type="feat"
        description="add new functionality"
    elif echo "$diff" | grep -q "^-.*function\|^-.*class\|^-.*def "; then
        commit_type="refactor"
        description="refactor code"
    elif echo "$diff" | grep -q "README\|CHANGELOG\|\.md"; then
        commit_type="docs"
        description="update documentation"
    elif echo "$diff" | grep -q "package\.json\|requirements\.txt\|Cargo\.toml\|go\.mod\|pyproject\.toml"; then
        commit_type="build"
        description="update dependencies"
    elif echo "$diff" | grep -q "\.github\|\.gitlab\|Dockerfile\|docker-compose"; then
        commit_type="ci"
        description="update CI/CD configuration"
    elif echo "$diff" | grep -q "^-.*bug\|^+.*fix"; then
        commit_type="fix"
        description="fix bugs"
    elif $has_new_files && ! $has_modifications && ! $has_deletions; then
        commit_type="feat"
        description="add new files"
    elif $has_deletions && ! $has_new_files; then
        commit_type="chore"
        description="remove unused files"
    elif $has_renames; then
        commit_type="refactor"
        description="reorganize files"
    fi

    # Determine scope from file paths
    local primary_dir=$(echo "$files" | head -1 | cut -d'/' -f1)
    if [ -n "$primary_dir" ] && [ "$primary_dir" != "." ]; then
        scope="$primary_dir"
    fi

    echo "${commit_type}|${scope}|${description}"
}

# Stage all changes
git add -A

# Get analysis
ANALYSIS=$(analyze_changes "$GIT_DIFF" "$CHANGED_FILES")
COMMIT_TYPE=$(echo "$ANALYSIS" | cut -d'|' -f1)
COMMIT_SCOPE=$(echo "$ANALYSIS" | cut -d'|' -f2)
COMMIT_DESC=$(echo "$ANALYSIS" | cut -d'|' -f3)

# Build commit message
if [ -n "$COMMIT_SCOPE" ]; then
    COMMIT_MSG="${COMMIT_TYPE}(${COMMIT_SCOPE}): ${COMMIT_DESC}"
else
    COMMIT_MSG="${COMMIT_TYPE}: ${COMMIT_DESC}"
fi

# Add Claude signature
COMMIT_MSG="${COMMIT_MSG}

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"

# Determine if we should amend or create new commit
SHOULD_AMEND=false

if [ "$IS_CLAUDE_COMMIT" = true ] && [ $TIME_SINCE_LAST_COMMIT -lt $MAX_COMMIT_AGE_SECONDS ]; then
    # Check if this is a continuation/refactor of the last commit
    LAST_COMMIT_TYPE=$(echo "$LAST_COMMIT_MSG" | head -1 | cut -d':' -f1 | sed 's/(.*//')

    # Similar commit types that can be combined
    if [ "$COMMIT_TYPE" = "$LAST_COMMIT_TYPE" ] || \
       ([ "$COMMIT_TYPE" = "refactor" ] && [ "$LAST_COMMIT_TYPE" != "feat" ]) || \
       ([ "$COMMIT_TYPE" = "chore" ] && [ "$LAST_COMMIT_TYPE" = "refactor" ]); then

        # Check if the files overlap significantly
        LAST_COMMIT_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD 2>/dev/null || echo "")

        # Count overlapping files
        OVERLAP_COUNT=0
        while IFS= read -r file; do
            if echo "$LAST_COMMIT_FILES" | grep -q "^${file}$"; then
                OVERLAP_COUNT=$((OVERLAP_COUNT + 1))
            fi
        done <<< "$CHANGED_FILES"

        # If more than 30% of files overlap, consider amending
        LAST_FILE_COUNT=$(echo "$LAST_COMMIT_FILES" | wc -l | tr -d ' ')
        if [ $LAST_FILE_COUNT -gt 0 ]; then
            OVERLAP_PERCENTAGE=$((OVERLAP_COUNT * 100 / LAST_FILE_COUNT))
            if [ $OVERLAP_PERCENTAGE -gt 30 ]; then
                SHOULD_AMEND=true
            fi
        fi
    fi
fi

# Check if there are any conflicts with amending
if [ "$SHOULD_AMEND" = true ]; then
    # Check if the commit has been pushed
    if git branch -r --contains HEAD | grep -q "origin"; then
        echo -e "${YELLOW}Last commit has been pushed, creating new commit instead of amending${RESET}" >&2
        SHOULD_AMEND=false
    fi
fi

# Perform the commit
if [ "$SHOULD_AMEND" = true ]; then
    echo -e "${BLUE}Amending previous commit...${RESET}" >&2
    git commit --amend --no-edit
    echo -e "${GREEN}✓ Changes amended to previous commit${RESET}" >&2
else
    echo -e "${BLUE}Creating new commit...${RESET}" >&2
    git commit -m "$COMMIT_MSG"
    echo -e "${GREEN}✓ Created commit: ${COMMIT_MSG%%$'\n'*}${RESET}" >&2
fi

# Show commit info
echo "" >&2
echo -e "${BLUE}Commit details:${RESET}" >&2
git log -1 --stat --color=always >&2

exit 0
