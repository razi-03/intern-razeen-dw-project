#!/usr/bin/env python3
"""Quick verification of Obsidian AI Brain installation"""

print("=" * 60)
print("  Obsidian AI Brain - Installation Verification")
print("=" * 60)
print()

# Test each package
packages = [
    ('yaml', 'PyYAML'),
    ('torch', 'Torch'),
    ('chromadb', 'ChromaDB'),
    ('sentence_transformers', 'Sentence Transformers'),
    ('langchain', 'LangChain'),
    ('streamlit', 'Streamlit'),
    ('ollama', 'Ollama'),
    ('networkx', 'NetworkX'),
    ('pandas', 'Pandas'),
    ('matplotlib', 'Matplotlib'),
    ('requests', 'Requests'),
]

success_count = 0
failed_list = []

for module_name, display_name in packages:
    try:
        module = __import__(module_name)
        version = getattr(module, '__version__', 'installed')
        print(f"✅ {display_name:25} {version}")
        success_count += 1
    except ImportError as e:
        print(f"❌ {display_name:25} MISSING")
        failed_list.append(display_name)

print()
print("=" * 60)
print(f"Result: {success_count}/11 packages verified")
print("=" * 60)

if failed_list:
    print(f"\n⚠️  Missing packages:")
    for pkg in failed_list:
        print(f"   - {pkg}")
    print(f"\nFix with: pip install -r obsidian_requirements_python312.txt")
else:
    print("\n✅ All packages verified! Ready to run Obsidian scripts.")
    print("\nNext steps:")
    print("  1. Make sure Ollama is running: ollama serve")
    print("  2. Run scripts in order:")
    print("     python obsidian_01_vault_scanner.py")
    print("     python obsidian_02_note_parser.py")
    print("     ... etc")
    print("  3. Launch dashboard: streamlit run obsidian_07_streamlit_ui.py")

print()
