# PM Operating System

A PM operating system that **accelerates product work** by giving LLMs **shared context**. It connects to where you work (Slack, Teams, Drive, Jira, Figma, Databricks, etc. via MCPs), includes PM skills (PRDs, strategy, launch, exec updates), and maintains a living context of your strategy and decisions — evolving into a **context graph** that compounds over time. Built for **Claude Code** (with legacy Cursor support).

**Created by [@Sach1ng](https://github.com/Sach1ng) and [@hardiktiwari](https://github.com/hardiktiwari)**

---

## Quick start (self-serve onboarding)

1. **Clone this repo**
   ```bash
   git clone https://github.com/Sach1ng/PM-operating-OS.git
   cd PM-operating-OS
   ```

2. **Run onboarding** — Open the repo in Claude Code, then in chat say: **"onboard"** or **"PM-OS setup"**. Answer the questions; the agent writes config and runs setup automatically. MCPs (tool connections) are the **last step** and **optional** — you can skip and add them later via Claude Code's `/mcp` command or by editing `.mcp.json`.
   - *Or* manually edit `config/pm-os-config.yaml` and run `./scripts/setup.sh`

3. **That's it** — `CLAUDE.md`, `.claude/agents/`, `.claude/skills/`, and `.mcp.json` load automatically when the workspace is open. (Add `--copy` to also deploy to `~/.claude/` for cross-project use.)

---

## What's included

| Type | What it is | How it's customized |
|------|------------|---------------------|
| **CLAUDE.md** | Persistent project context Claude Code loads every session | Your product, role, org, deprioritization signals, domain context |
| **Skills** (`.claude/skills/`) | On-demand PM capabilities | Goals, VIPs, PRD template, expanded PM workflows |
| **Sub-agents** (`.claude/agents/`) | Specialized assistants (feedback analysis, planning, strategy review, exec updates, retrospective) | Slack/Teams channel, Google docs, goals |
| **MCP servers** (`.mcp.json`) | Tool connections Claude Code loads on startup | Your selected tools (Slack, Teams, Drive, Jira, GitHub, Figma...) |
| **Knowledge layer** (`knowledge/`) | Strategy and domain context (personas, metrics, competitive landscape) | Customize in `knowledge/` |
| **Memory** (`memory/`) | Trajectory store — accumulated agent outputs, decision traces, knowledge snapshots | Builds automatically as you use agents |

---

## Structure (after onboarding)

| Folder / file | Purpose |
|---------------|---------|
| **CLAUDE.md** | Project context Claude Code loads automatically (PM Chief of Staff persona + domain context + Learned sections). Generated from `templates/CLAUDE.md.template` + `config/pm-os-config.yaml`. |
| **.claude/agents/** | Sub-agents Claude Code invokes via the Agent tool (onboarding, company-researcher, feedback-analyzer, weekly-planner, strategy-reviewer, exec-update-generator, retrospective, etc.) |
| **.claude/skills/** | Skills Claude Code invokes via the Skill tool (PRD writer, working-backwards, strategy-connector, what-if, decision-logger, etc.) |
| **.mcp.json** | MCP server definitions (Slack, Teams, Drive, Jira, GitHub, Figma...). Claude Code loads on startup. |
| **config/** | Your answers → `pm-os-config.yaml` |
| **templates/** | Jinja2 templates for CLAUDE.md, agents, skills |
| **scripts/** | `setup.sh` / `setup.py` — generates personalized files |
| **output/** | Staging area for generated files (gitignored) |
| **skills/** | Source for prd-writer, working-backwards, and expanded PM skills (copied into `.claude/skills/` by setup) |
| **knowledge/** | Strategy docs (personas, metrics, competitive landscape) — referenced by CLAUDE.md and agents |
| **memory/** | Context graph trajectory store — decision traces, agent outputs, knowledge snapshots |
| **docs/agents.md** | Agent documentation (all agents, trigger phrases, requirements) |
| **AGENTS.md / .cursor/** | Legacy Cursor IDE files — kept for users who want to run PM-OS in Cursor alongside Claude Code. |

---

## CLAUDE.md, skills, and agents — what's the difference?

| | What it is | In plain terms |
|---|------------|----------------|
| **CLAUDE.md** | Always-on project context Claude Code loads every session | How *you* work: standards, org context, prioritization |
| **Skills** | On-demand "how-to" Claude Code uses when the task fits | PM capabilities: PRDs, working backwards, prioritization |
| **Sub-agents** | Specialized assistants Claude Code delegates to | Concrete tasks: feedback analysis, daily planning, strategy review |

---

## PM Workflows

| Workflow | Skills |
|----------|--------|
| **Planning** | strategy-connector, working-backwards |
| **Building** | prd-writer, one-pager, experiment-designer |
| **Shipping** | launch-readiness, launch-post |
| **Communicating** | exec-communicator, stakeholder-update |
| **Learning** | experiment-writeup, feedback-analyzer |
| **Operating** | weekly-planner, meeting-to-actions, action-item-prioritizer |
| **Context graph** | decision-logger, what-if, knowledge-updater, retrospective |

---

## Knowledge Layer

The `knowledge/` directory holds strategy and domain context that agents and rules reference:

- **_template/** — Copy this folder and rename it for your domain (e.g., `my-product/`)
- **examples/** — Fully worked-out examples using public investor data from **Spotify, Netflix, Shopify, and Uber** (SEC 10-Ks, earnings calls, investor presentations)

**How to customize:** Edit the markdown files in `knowledge/` to reflect your product, team, and current strategy. Browse `knowledge/examples/` to see how real companies' strategy, segments, and metrics map to the template. The strategy-reviewer agent and domain context rule use this context automatically.

---

## Context Graph — Memory Layer

PM OS includes a **memory layer** that turns it from a static configuration system into a context graph where reasoning accumulates over time. Inspired by [context graph infrastructure](https://www.linkedin.com/pulse/how-do-you-build-context-graph-jaya-gupta-xicwe/) — the idea that the next wave of AI won't just store data, it will capture the *reasoning* that connects data to decisions.

### How it works

Every agent **reads from memory before starting** (what happened last time, what trends are emerging) and **writes to memory after completing** (structured summary of findings). This creates three capabilities:

| Capability | What it does | How |
|------------|-------------|-----|
| **Temporal awareness** | Agents know what happened before | Feedback analyzer in March knows what February found; weekly planner knows what got done vs. dropped |
| **Cross-agent context** | Agents read each other's outputs | Exec update pulls from feedback, plans, decisions, and reviews — no manual stitching |
| **Compounding intelligence** | Context gets richer over time | More runs → better trend detection, drift analysis, and simulation grounding |

### Memory structure

```
memory/
├── decisions/            # Decision traces — the "why" behind key calls
├── feedback/             # Feedback analyzer outputs over time
├── weekly-plans/         # Weekly planner outputs
├── strategy-reviews/     # Strategy reviewer scorecards
├── exec-updates/         # Executive status updates
└── knowledge-snapshots/  # Versioned snapshots for drift detection
```

### Context graph skills and agents

| Name | Type | What it does |
|------|------|-------------|
| **decision-logger** | Skill | Captures structured decision traces after key PM moments (PRD approvals, scope changes, launch/kill calls) |
| **what-if** | Skill | Simulates impact of proposed decisions using accumulated context — strategy, past decisions, customer feedback, execution history |
| **knowledge-updater** | Skill | Updates knowledge docs with automatic snapshotting for drift detection |
| **retrospective** | Agent | Reads across all memory to surface patterns, strategy drift, execution velocity, and blind spots |

### Getting started with memory

Memory builds automatically as you use PM OS agents. To accelerate:

1. **Log a few key decisions** — Say *"log this decision"* after your next prioritization call or PRD approval
2. **Run feedback analysis** — Each run saves to memory, building a trend baseline
3. **Plan your week** — Weekly plans accumulate, creating an execution history
4. **Run a retrospective** — Say *"retrospective"* once you have 5+ memory entries to see patterns emerge

---

## Manual setup (without the script)

If you prefer not to run the setup script:

- Edit `config/pm-os-config.yaml` with your answers
- Edit `CLAUDE.md` directly with your product/role/goals
- Skills already live in `skills/` — copy into `.claude/skills/` (or symlink) so Claude Code picks them up

---

## Requirements

**Required:**
- **Claude Code** (CLI, desktop app, or IDE extension) — any edition with sub-agent + MCP support
- **Python 3** (for setup script; `pip install -r requirements.txt`)

**Optional (for agents that connect to external tools):**
- **Slack, Microsoft Teams, Google Drive, GitHub, Figma** — Setup auto-generates `.mcp.json` for these. You just add your API keys. See [MCP_SETUP.md](MCP_SETUP.md).
- **Jira, Linear, Notion, etc.** — Add via Claude Code's `/mcp` command or by editing `.mcp.json` directly.

> **15+ skills work immediately without any MCP.** During onboarding, MCPs are the **last step** and **optional** — you can skip and connect them anytime via Claude Code's `/mcp` command or by editing `.mcp.json`. See [MCP_SETUP.md](MCP_SETUP.md).

---

## Feedback Analyzer (Slack / Teams)

If you enabled the feedback analyzer:

1. Configure the **Slack** or **Microsoft Teams** MCP in `.mcp.json` with access to your feedback channel.
2. In Claude Code chat, say: *"Analyze feedback"*, *"Slack feedback analysis"*, or *"Customer feedback"*.
3. The agent searches your configured channel, classifies feedback by theme, and returns a PM report.

See [docs/agents.md](docs/agents.md) for details.

---

## Authors

| | GitHub | Role |
|---|---|---|
| **Sachin** | [@Sach1ng](https://github.com/Sach1ng) | Co-creator | https://www.linkedin.com/in/sachinkgupta1
| **Hardik** | [@hardiktiwari](https://github.com/hardiktiwari) | Co-creator |  https://www.linkedin.com/in/hardik-tiwari

## Contributing

To add a new skill, create a folder in `skills/` with a `SKILL.md` following the existing format.

---

## Disclaimer

*This is a personal project and is not affiliated with, endorsed by, or representative of any employer.*

## License

MIT — see [LICENSE](LICENSE) for details.
