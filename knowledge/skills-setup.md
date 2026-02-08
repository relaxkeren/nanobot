# Skills setup (Nanobot)

This doc explains **how to create and add a “skill”** to Nanobot.

In this repo, a **skill** is a small, self-contained folder containing a `SKILL.md` file. Skills are loaded into the agent context **progressively**:

- A short index (name/description/location/availability) is always shown to the agent.
- Skills marked “always” may be inlined in full.
- The agent can then load the full skill text by reading its `SKILL.md` file.

## Where skills live

Nanobot loads skills from two places (in priority order):

1. **Workspace skills (highest priority)**:
   - `{workspace}/skills/{skill-name}/SKILL.md`
2. **Built-in skills (bundled with the package)**:
   - `nanobot/skills/{skill-name}/SKILL.md`

If a skill with the same name exists in both places, the **workspace skill wins** (it “shadows” the built-in).

## Add a skill to your workspace (recommended)

This is the fastest way to add/override a skill **without changing the repo**.

1. Find your Nanobot workspace.
   - Default is typically `~/.nanobot/workspace`
   - Or whatever you configured as `agents.defaults.workspace` in `~/.nanobot/config.json`

2. Create a new folder:
   - `{workspace}/skills/{skill-name}/`

3. Create:
   - `{workspace}/skills/{skill-name}/SKILL.md`

4. Restart Nanobot (or start a new `nanobot agent` session) so the context rebuild includes your new skill.

### Minimal `SKILL.md` template

Create `SKILL.md` with **YAML frontmatter** at the top:

```markdown
---
name: my-skill
description: "One sentence: what it does and when to use it."
metadata: {"nanobot":{"requires":{"bins":["mycli"],"env":["MY_API_KEY"]}}}
---

# My Skill

Do X using Y. Include short, concrete examples.
```

Notes:

- **`name`**: should match the folder name (`my-skill`).
- **`description`**: is the main “trigger hint” the agent sees in the skill index.
- **`metadata`** (optional): a **single-line JSON** blob Nanobot parses for availability checks and behavior flags.

## Add a built-in (bundled) skill to the repo

Use this when you want the skill shipped as part of the Nanobot package.

1. Create a folder:
   - `nanobot/skills/{skill-name}/`

2. Add the required file:
   - `nanobot/skills/{skill-name}/SKILL.md`

3. (Optional) Add resource folders as needed:
   - `nanobot/skills/{skill-name}/scripts/` (executables, helpers)
   - `nanobot/skills/{skill-name}/references/` (docs to read on-demand)
   - `nanobot/skills/{skill-name}/assets/` (templates/binaries/etc.)

4. (Recommended) Update the built-in skills list table:
   - `nanobot/skills/README.md`

Packaging note: `pyproject.toml` already includes `nanobot/skills/**/*.md` (and some script patterns), so new built-in skills are typically picked up automatically by distribution builds.

## Skill metadata and availability (what Nanobot actually checks)

Nanobot reads frontmatter keys and also parses `metadata` (JSON) for a `nanobot` object.

### Availability checks (gating)

Nanobot currently considers a skill “available” if these requirements are satisfied:

- **`requires.bins`**: every named CLI is found on `PATH`
- **`requires.env`**: every named environment variable is set (non-empty)

Example:

```markdown
---
name: github
description: "Interact with GitHub using the gh CLI."
metadata: {"nanobot":{"requires":{"bins":["gh"]}}}
---
```

If requirements are missing, Nanobot will mark the skill unavailable in the skills index, and will include which requirements are missing (e.g., `CLI: gh`, `ENV: MY_API_KEY`).

### “Always-loaded” skills

If you want a skill’s **full body** to be included in the system prompt (instead of only appearing in the skills index), mark it as always-loaded in `metadata`:

```markdown
---
name: my-skill
description: "..."
metadata: {"nanobot":{"always": true}}
---
```

## Important frontmatter limitations (current implementation)

Nanobot’s frontmatter parsing is intentionally simple. To avoid subtle breakage:

- Keep **one key per line** in the frontmatter.
- Avoid nested YAML objects (they won’t parse as you expect).
- Put `metadata:` JSON on **one line**.
- Use quotes for `description` if it contains punctuation like `:` or `#`.

## Quick validation / debugging

There is no dedicated CLI command to list skills; the simplest check is to call the loader directly.

### Print discovered skills (including unavailable)

```bash
python -c 'import os; from pathlib import Path; from nanobot.agent.skills import SkillsLoader; w=Path(os.path.expanduser("~/.nanobot/workspace")); print(SkillsLoader(w).list_skills(filter_unavailable=False))'
```

### Print the skills index XML (the “progressive loading” summary)

```bash
python -c 'import os; from pathlib import Path; from nanobot.agent.skills import SkillsLoader; w=Path(os.path.expanduser("~/.nanobot/workspace")); print(SkillsLoader(w).build_skills_summary())'
```

If you use a non-default workspace, replace the path accordingly.

