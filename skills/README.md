# Claude Code Skills

This directory contains skills that enhance Claude's capabilities for specific domains or tools.

## Available Skills

### justfile-expert

Expert guidance for Just task runner and justfiles with modern syntax and best practices.

**Triggers:** Working with justfiles, build automation, task recipes, Just syntax errors

**Features:**
- Modern recipe groups with correct `[group: 'name']` syntax
- Common patterns (subcommands, parameters, dependencies, attributes)
- Critical mistakes section with correct/incorrect examples
- Cross-platform considerations
- Comprehensive troubleshooting guide
- Advanced reference documentation

**Structure:**
- `SKILL.md` - Core patterns, quick reference, common mistakes
- `references/just-docs.md` - Advanced features, complete function reference

## Skill Structure

Each skill follows the official Claude skill format:

```
skill-name/
├── SKILL.md                    # Required: Main skill content
│   ├── YAML frontmatter       # name and description
│   └── Markdown body          # Instructions and patterns
└── references/                 # Optional: Detailed documentation
    └── detailed-docs.md
```

### SKILL.md

Contains:
- **Frontmatter (YAML)**: `name` and `description` (triggers skill loading)
- **Body (Markdown)**: Core patterns, quick start, common mistakes

**Keep concise** - Only essential patterns and workflows. Move detailed reference material to `references/`.

### references/

Detailed documentation loaded on-demand:
- API references
- Complete function listings
- Advanced patterns
- Detailed examples

## Using Skills

Skills are installed to `.claude/skills/` in your project:

```bash
# Using claude-tools installer
claude-tools /path/to/project
```

Or manually copy the `.skill` file to your project's `.claude/skills/` directory.

## Creating Skills

To create a new skill, use the skill-creator:

1. **Initialize**: Run the init script from skill-creator
   ```bash
   python3 scripts/init_skill.py skill-name --path /path/to/output
   ```

2. **Edit**: Update `SKILL.md` with:
   - Comprehensive description in frontmatter (this triggers the skill)
   - Core patterns and quick reference in body
   - Move detailed docs to `references/`

3. **Package**: Validate and package the skill
   ```bash
   python3 scripts/package_skill.py /path/to/skill-folder
   ```

### Best Practices

**Conciseness is key:**
- Default assumption: Claude is already smart
- Only add context Claude doesn't have
- Prefer examples over explanations
- Keep SKILL.md under 500 lines
- Move detailed content to references/

**Description field:**
- Include WHAT the skill does
- Include WHEN to use it (file types, scenarios, tasks)
- Be comprehensive - this is the primary trigger

**Structure:**
- Quick start with common patterns
- Show mistakes with WRONG/CORRECT examples
- Link to references/ for advanced topics
- Include real-world examples

## Distribution

Skills are distributed as `.skill` files (zip archives with .skill extension) that can be:
- Shared directly
- Installed via claude-tools
- Copied to project `.claude/skills/` directories

## Contributing

When adding skills:
1. Use skill-creator's init script
2. Follow the official skill structure
3. Keep SKILL.md concise and practical
4. Add comprehensive descriptions
5. Test with real use cases
6. Package with the packaging script
7. Update this README
