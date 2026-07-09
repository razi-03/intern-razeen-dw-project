import json

insights = {
    "notes": {
        "01_getting_started": {
            "title": "Getting Started with Python",
            "insights": "Foundational programming knowledge",
            "key_topics": ["Python", "Programming"]
        },
        "02_data_science": {
            "title": "Data Science Basics",
            "insights": "Introduction to data science methods",
            "key_topics": ["Data Science", "Analytics"]
        },
        "03_machine_learning": {
            "title": "Machine Learning Algorithms",
            "insights": "Core ML concepts and algorithms",
            "key_topics": ["Machine Learning", "AI"]
        },
        "04_programming_concepts": {
            "title": "Programming Concepts",
            "insights": "Universal programming principles",
            "key_topics": ["Programming", "OOP"]
        },
        "05_ai_ethics": {
            "title": "AI Ethics",
            "insights": "Responsible AI development",
            "key_topics": ["Ethics", "AI"]
        }
    },
    "summary": "Your knowledge base contains 5 notes on Python, Data Science, and AI."
}

with open("data/insights.json", "w") as f:
    json.dump(insights, f, indent=2)

print("✅ Created data/insights.json")
