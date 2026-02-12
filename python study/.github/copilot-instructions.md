<!-- Repository-specific Copilot instructions for AI coding agents -->

# Quick Orientation

- **Project type:** A small learning repository of standalone Python example scripts. Key files: `practice.py`, `loops.py`, `python_beginner.py`, `pythonDict.py`.
- **How scripts are organized:** Most files are small, top-level example scripts (no package/module structure). Many examples are commented out and some files are interactive (use `input()`).

# What an AI agent should know before editing

- **Run commands:** Use the system Python 3 interpreter. From the repo root run:

  `python3 "./loops.py"`

  Replace the filename for other scripts (macOS `zsh` shell). Do not assume a test or build system.

- **Interactive scripts:** `practice.py` and parts of `loops.py` prompt for input. Exercise caution when running in non-interactive environments.

- **Broken/incomplete files:** `practice.py` currently contains an incomplete `while` statement (syntax error). Do not run or refactor it without fixing that error first. If you fix it, prefer minimal, local changes and add a simple `if __name__ == "__main__":` guard when turning examples into runnable modules.

# Patterns and idioms found in this repo (use these as examples)

- `pythonDict.py`: demonstrates dictionary methods (`get`, `update`, `pop`, `keys`, `values`, `items`) and iterating `for key, value in student.items():` — maintain the explicit, pedagogical style when adding examples.
- `loops.py`: contains commented examples of `for`, `while`, nested loops, and simple `break`/`else` patterns. New loop examples should follow the same commented-demo approach rather than hidden utilities.
- `python_beginner.py`: shows string escaping and f-string formatting. Keep examples small and explicit.

# Editing guidelines for AI agents

- **Keep changes minimal and educational:** This repo appears intended for learning; prefer small, well-explained edits. Preserve or improve comments that explain the code.
- **Avoid large refactors:** Do not reorganize into packages or add heavy scaffolding unless the user asks for it.
- **When making runnable scripts:** Add `if __name__ == "__main__":` guards and avoid introducing external dependencies.
- **Input handling:** If converting interactive examples to non-interactive functions (for tests or automation), add parameters and keep the original interactive example as a separate, commented snippet.

# Commits and PR notes

- When committing changes, include brief context: why the change was made (e.g., "fix syntax in practice.py" or "add non-interactive demo for dict usage"). Keep commits small and focused.

# Tests and CI

- There are no tests or CI files in the repository. If you add tests, add a `README.md` or short note describing how to run them (e.g., `python -m pytest`). Do not add tests without user consent.

# Example tasks an agent can perform safely

- Fix obvious syntax mistakes (e.g., the incomplete `while` in `practice.py`) and run the corrected script locally.
- Convert a single example into a testable function and leave the original example intact.
- Improve comments to make a script clearer for learners.

# When to ask the human

- Ask before introducing new dependencies, CI, or restructuring multiple files.
- Ask if you should convert interactive examples into testable code or keep them as-is for teaching.

---
If any section is unclear or you want the instructions to be stricter/looser about refactoring and tests, tell me which parts to change.
