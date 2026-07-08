#!/usr/bin/env python3
"""
Generate test Obsidian notes for quick testing of Obsidian AI Brain
Run: python create_test_notes.py
"""

import os
import json
from pathlib import Path

def create_test_notes():
    """Create sample notes in obsidian_vault"""
    
    vault_path = Path("obsidian_vault")
    vault_path.mkdir(exist_ok=True)
    
    # Sample notes with markdown formatting and tags
    notes = {
        "01_getting_started.md": """# Getting Started with Python

This is a foundational note about Python programming.

## What is Python?

Python is a high-level, interpreted programming language known for its simplicity and readability.

### Key Features
- Easy to learn and read
- Versatile (web, data science, automation)
- Large standard library
- Active community

## Basic Syntax

```python
# Hello World
print("Hello, World!")
```

## Related Topics
- [[Data Science Basics]]
- [[Python Best Practices]]
- [[Programming Concepts]]

Tags: #python #programming #beginner
""",
        
        "02_data_science.md": """# Data Science Basics

An introduction to the field of data science and its applications.

## What is Data Science?

Data science is an interdisciplinary field that uses scientific methods, processes, algorithms and systems to extract knowledge and insights from structured and unstructured data.

## Key Components

1. **Statistics** - Understanding data distributions
2. **Programming** - Implementing solutions (Python, R)
3. **Domain Knowledge** - Understanding the problem
4. **Visualization** - Communicating insights

## Tools and Technologies

- Python (pandas, NumPy, scikit-learn)
- SQL (data querying)
- Machine Learning frameworks (TensorFlow, PyTorch)
- Visualization (Matplotlib, Seaborn, Plotly)

## Important Concepts
- [[Machine Learning Algorithms]]
- [[Getting Started with Python]]
- [[Data Visualization]]

Tags: #datascience #ai #analytics
""",
        
        "03_machine_learning.md": """# Machine Learning Algorithms

An overview of common machine learning algorithms and their applications.

## What is Machine Learning?

Machine Learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed.

## Types of Learning

### Supervised Learning
- Regression (predicting continuous values)
- Classification (predicting categories)
- Examples: [[Getting Started with Python]], Linear Regression

### Unsupervised Learning
- Clustering (grouping similar data)
- Dimensionality reduction
- Pattern discovery

### Reinforcement Learning
- Learning through rewards and punishments
- Game playing, robotics

## Popular Algorithms

| Algorithm | Type | Use Case |
|-----------|------|----------|
| Linear Regression | Supervised | Predicting continuous values |
| Decision Trees | Supervised | Classification |
| K-Means | Unsupervised | Clustering |
| Neural Networks | Both | Complex pattern recognition |

## Related Reading
- [[Data Science Basics]]
- [[Programming Concepts]]

Tags: #ml #ai #algorithms #datascience
""",
        
        "04_programming_concepts.md": """# Programming Concepts

Core programming concepts that apply across languages.

## Object-Oriented Programming (OOP)

OOP is a programming paradigm based on the concept of objects, which can contain data and code.

### Key OOP Principles
- **Encapsulation** - Bundling data and methods
- **Inheritance** - Deriving new classes from existing ones
- **Polymorphism** - Using objects of different types interchangeably
- **Abstraction** - Hiding complex implementation details

## Functional Programming

A programming paradigm where computation is treated as the evaluation of mathematical functions.

### Key Concepts
- First-class functions
- Pure functions (no side effects)
- Immutability
- Higher-order functions

## Design Patterns

Reusable solutions to common programming problems.

- Singleton
- Factory
- Observer
- Strategy

## Important to Know
- [[Getting Started with Python]]
- [[Data Science Basics]]

Tags: #programming #concepts #architecture
""",
        
        "05_ai_ethics.md": """# AI Ethics

Important considerations when developing AI systems.

## What is AI Ethics?

AI Ethics is concerned with the responsible development and deployment of AI systems that respect human values, rights, and dignity.

## Key Concerns

1. **Bias and Fairness**
   - Algorithmic bias can perpetuate discrimination
   - Need diverse training data
   - Regular audits for bias

2. **Transparency and Explainability**
   - Users should understand how AI makes decisions
   - Black box models are problematic
   - Need interpretable AI

3. **Privacy**
   - Data protection and security
   - Informed consent
   - Data minimization

4. **Accountability**
   - Who is responsible for AI decisions?
   - Clear governance frameworks
   - Liability considerations

## Related Topics
- [[Machine Learning Algorithms]]
- [[Data Science Basics]]

Tags: #ai #ethics #responsibility #governance
""",
    }
    
    # Create notes
    created_count = 0
    for filename, content in notes.items():
        filepath = vault_path / filename
        filepath.write_text(content, encoding='utf-8')
        created_count += 1
        print(f"✅ Created: {filename}")
    
    print(f"\n{'='*50}")
    print(f"Created {created_count} test notes in obsidian_vault/")
    print(f"{'='*50}")
    
    # Show what was created
    print("\nNotes created:")
    for note in vault_path.glob("*.md"):
        size = note.stat().st_size
        print(f"  - {note.name} ({size} bytes)")
    
    print("\n✅ Ready to run scripts!")
    print("\nNext steps:")
    print("1. Start Ollama: ollama serve")
    print("2. Run scanner: python obsidian_01_vault_scanner.py")
    print("3. Continue with other scripts...")

if __name__ == "__main__":
    try:
        create_test_notes()
    except Exception as e:
        print(f"❌ Error creating notes: {e}")
        exit(1)
