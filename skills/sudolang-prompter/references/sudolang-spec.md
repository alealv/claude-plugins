# SudoLang v2.0 Specification Reference

## Overview

SudoLang is a pseudolanguage for LLM interactions that combines natural language clarity with programming constructs. Models understand it natively without special prompting.

## Core Syntax

### Variables & Assignment
```sudolang
name = "value"
count += 1
score -= 10
```

### Template Strings
```sudolang
greeting = "Hello, $name!"    # Interpolation
literal = "Cost: \$50"        # Escaped $
```

### Destructuring
```sudolang
[first, second, ...rest] = items
{ name, age } = person
```

## Control Flow

### Conditionals
```sudolang
status = if (age >= 18) "adult" else "minor"

if (condition) {
  action()
}
```

### Loops
```sudolang
for each item in collection {
  process(item)
}

while (active) {
  update()
}

loop {
  # infinite until break
}
```

### Range Operator
```sudolang
1..5        # yields 1, 2, 3, 4, 5
items[0..2] # first three items
```

## Functions

Functions are inferred by LLMs - explicit definition rarely needed:
```sudolang
# Implicit - just use it
summarize(text)
translate(content, to="Spanish")

# Explicit when needed
doubleIt(n) => n * 2
```

### Pipe Operator
Chain operations elegantly:
```sudolang
data |> parse |> validate |> transform |> save
text |> summarize |> translate(to="French")
```

## Interfaces

Define structure and behavior:
```sudolang
Character {
  name
  health = 100
  attack(target) => target.health -= 10
}
```

### Composition Over Inheritance
```sudolang
Flyable { fly() }
Swimmable { swim() }

Duck {
  ...Flyable
  ...Swimmable
  quack()
}
```

## Constraints vs Requirements

### Constraints (Soft Rules)
Declarative rules the AI continuously respects:
```sudolang
Constraints {
  Use simple, playful language.
  Keep responses under 200 words.
  PG-13 content only.
}
```

### Requirements (Hard Rules)
Enforce with errors on violation:
```sudolang
Requirements {
  throw "Error" if input.length > 1000
  warn "Unusual input" if input contains "TODO"
}
```

## Commands

Shorthand for common operations:
```sudolang
/help
/explain topic
/summarize document
/translate text to="Spanish"
```

## Modifiers

Customize behavior inline:
```sudolang
explain(topic):length=short, detail=simple;
analyze(data):depth=comprehensive, format=bullets;
```

## Options Block

Configure program behavior:
```sudolang
Options {
  depth: 1..10 | "kindergarten".."PhD"
  tone: formal | casual | technical
  language: en | es | fr
}
```

## Semantic Pattern Matching

```sudolang
match shape {
  { type: "circle", radius } => area = pi * radius^2
  { type: "rectangle", width, height } => area = width * height
  _ => throw "Unknown shape"
}
```

## Markdown Integration

Markdown is executable - use it for:
- Program preambles describing AI role/expertise
- Section organization
- Documentation that affects behavior

## Key Principles

1. **Natural language first** - Use code only when it adds clarity
2. **Lean into inference** - Let LLM figure out obvious functions
3. **Composition over inheritance** - Use interfaces and spread
4. **Conciseness wins** - Brevity with clarity
5. **No constructors** - Use factory functions if needed

## Common Patterns

### Role Definition
```sudolang
# Expert Code Reviewer

You are a senior software engineer specializing in code quality.

Constraints {
  Focus on maintainability and readability.
  Provide actionable feedback.
  Be constructive, not critical.
}
```

### Workflow Definition
```sudolang
ReviewWorkflow {
  State {
    code
    findings = []
    severity_levels = [critical, major, minor, suggestion]
  }

  /review code {
    analyze(code) |> categorize |> prioritize |> format
  }
}
```

### Interactive Assistant
```sudolang
Assistant {
  Constraints {
    Ask clarifying questions when ambiguous.
    Confirm understanding before proceeding.
  }

  /help => explain available commands
  /task description => break down into steps |> execute
}
```
