# Development testing

Quick reference for testing main use cases before release or after changes.

## Prerequisites

- Python 3 with `pip install -r requirements.txt` (PyYAML, Jinja2)
- Repo root = workspace (e.g. `PM-operating-OS/`)

## Use cases tested

### 1. Setup with default config (`--output-only`)

```bash
./scripts/setup.sh --output-only
```

**Expect:** No copy to `~/.cursor`. Output under `output/`: rules, agents, skills. `.cursor/mcp.json` generated when config has at least one tool enabled.

**Verify:**
- `output/rules/` — chief-of-staff + domain-context `.mdc`
- `output/agents/` — onboarding, company-researcher (+ subagents), feedback-analyzer, weekly-planner, strategy-reviewer, exec-update-generator, retrospective
- `output/skills/` — all enabled skills (prd-writer, working-backwards, etc.)
- `memory/` — directory present

### 2. MCP config generation

With `config/pm-os-config.yaml`:

- **slack, google_drive, browser = true** → `.cursor/mcp.json` has `slack`, `google_drive`, `browser`.
- **jira or confluence = true** → adds `atlassian` (URL `https://mcp.atlassian.com/v1/mcp`).
- **figma = true** → adds `figma` (hosted) + `figma_developer` (Framelink, env `FIGMA_API_KEY`).

Re-run setup after toggling tools and confirm `mcp.json` entries.

### 3. Full deploy (copy to Cursor)

```bash
./scripts/setup.sh --copy
```

**Expect:** Same generation, then copy from `output/` to `~/.cursor/` (rules, agents, skills). User restarts Cursor to load.

### 4. Onboarding flow (manual check)

- Open repo in Cursor, say **"onboard"** or **"PM-OS setup"**.
- Confirm agent asks: confirm → company + role → company research runs → identity, stakeholders, goals, tools, Slack/Drive details (if Y), skills & agents, then **MCPs optional last**.
- After answers, agent writes `config/pm-os-config.yaml` and runs `./scripts/setup.sh --copy`.

### 5. Key paths and templates

- `templates/rules/*.mdc.template`, `templates/agents/*.md.template`, `templates/skills/**/SKILL.md.template` — exist and render.
- `knowledge/_template/` and `knowledge/examples/` — present for knowledge layer.
- `.cursor/agents/onboarding.md` — present for project-local onboarding.

## Last run

- **Setup (output-only):** OK — rules, agents, skills, MCP (3 then 6 with jira+figma) generated.
- **MCP variants:** OK — atlassian and figma_developer added when tools enabled.
- **Push:** `main` up to date with origin.
