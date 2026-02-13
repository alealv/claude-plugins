---
name: sudolang-prompter
description: Create efficient, well-structured LLM prompts using SudoLang pseudolanguage syntax. Use when asked to create, write, design, or build a prompt, system prompt, AI instruction, or LLM configuration. Also use when users want to define AI behaviors, personas, workflows, or agent instructions. Triggers on requests like "create a prompt for...", "write a system prompt", "design an AI assistant", "build a chatbot prompt", or any task involving prompt engineering.
---

# SudoLang Prompt Builder

Build LLM prompts using SudoLang - a pseudolanguage combining natural language with programming constructs for clearer, more maintainable prompts.

## Quick Reference

### Structure Template
```sudolang
# [Role/Title]

[Natural language description of expertise and purpose]

Constraints {
  [Behavioral rules the AI should follow]
}

Interface {
  State { [tracked variables] }
  /command => [action]
}
```

### Key Constructs

| Construct | Use For |
|-----------|---------|
| `Constraints {}` | Soft rules AI respects continuously |
| `Requirements {}` | Hard rules with error on violation |
| `State {}` | Track conversation variables |
| `/command` | Define user-invokable actions |
| `\|>` pipe | Chain operations: `input \|> step1 \|> step2` |
| `$var` | Template interpolation |
| Modifiers | `action():length=short, tone=casual;` |

### Examples

**Simple Assistant:**
```sudolang
# Writing Coach

Expert editor helping improve clarity and impact.

Constraints {
  Give specific, actionable feedback.
  Maintain the author's voice.
  Limit suggestions to 3 per review.
}

/review text => analyze |> suggest improvements |> explain reasoning
```

**Stateful Workflow:**
```sudolang
# Interview Conductor

State {
  questions = []
  answers = []
  current_topic
}

Constraints {
  Ask one question at a time.
  Build on previous answers.
  Stay professional but warm.
}

/start topic {
  current_topic = topic
  generate opening question for $topic
}

/next => analyze last answer |> generate follow-up
/summarize => compile answers into insights
```

## Process

1. **Define the role** - Use markdown header + natural language description
2. **Set constraints** - List behavioral rules in `Constraints {}` block
3. **Add state** if needed - Track variables across conversation
4. **Define commands** - Create `/command` shortcuts for common actions
5. **Use pipes** for workflows - Chain operations with `|>`

## When to Use What

- **Natural language**: Role descriptions, context, nuanced instructions
- **Constraints block**: Consistent behavioral rules
- **Interfaces**: Complex agents with state and commands
- **Pipes**: Multi-step workflows
- **Modifiers**: Adjustable parameters like length, tone, detail

## Full Specification

For complete syntax including loops, pattern matching, and advanced features, see [references/sudolang-spec.md](references/sudolang-spec.md).
