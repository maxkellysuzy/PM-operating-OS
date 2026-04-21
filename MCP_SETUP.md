# MCP Setup Guide

When you run `./scripts/setup.sh`, PM-OS **automatically generates** `.mcp.json` at the project root with configs for the MCPs you selected. You just need to add your API keys and tokens.

---

## Quick Start

1. **Run setup** — `./scripts/setup.sh` (or say "onboard" in Claude Code)
2. **Open** `.mcp.json` at the project root
3. **Replace placeholders** with your real keys (see below)
4. **Restart Claude Code** (or run `/mcp reload`) — MCPs load when this repo is open

---

## Where to Get Your Keys

### Slack

| Placeholder | Where to get it |
|-------------|-----------------|
| `YOUR_SLACK_BOT_TOKEN` | [Slack API](https://api.slack.com/apps) → Create App → Bot User OAuth Token (starts with `xoxb-`) |
| `YOUR_SLACK_TEAM_ID` | Slack workspace URL: `https://app.slack.com/client/T01234567/` — the `T01234567` part is your Team ID. Or: Workspace settings → Organization ID |

**Steps:** Create a Slack app, add `chat:write`, `channels:history`, `users:read` scopes, install to workspace, copy the Bot Token.

### Microsoft Teams

Teams MCP access is available via community connectors. Configure the server entry in `.mcp.json` with your tenant + bot credentials, or use an OAuth-based hosted connector if your org provides one. The feedback-analyzer and weekly-planner agents work with either Slack *or* Teams — point them at whichever MCP is configured.

### Google Drive

Uses OAuth — no env vars needed in config. On first use:

1. Run `npx @modelcontextprotocol/server-gdrive auth`
2. Follow the browser flow to authorize
3. Credentials save to `~/.gdrive-server-credentials.json`

If you hit auth issues, see [server-gdrive README](https://github.com/modelcontextprotocol/servers/tree/main/src/gdrive).

### GitHub

| Placeholder | Where to get it |
|-------------|-----------------|
| `YOUR_GITHUB_TOKEN` | [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens) → Generate (classic) → enable `repo`, `read:org` |

### Figma

**Hosted Figma MCP** (default): No keys needed — uses Figma's hosted MCP. When you use it, you'll be prompted to authorize in the browser.

**Figma Context MCP** (Framelink — optional): For layout/design data that improves one-shot implementation, PM-OS can add [Figma Context MCP](https://github.com/GLips/Figma-Context-MCP) (Framelink). Setup adds it when you enable Figma during onboarding.

| Placeholder | Where to get it |
|-------------|-----------------|
| `YOUR_FIGMA_API_KEY` | [Figma account → Settings → Personal access tokens](https://www.figma.com/settings) → Generate new token |

Config (auto-added when Figma is enabled): `npx -y figma-developer-mcp --stdio` with `FIGMA_API_KEY` in env.

### Browser (Playwright)

**No keys needed.** Enabled by default. Uses [`@playwright/mcp`](https://www.npmjs.com/package/@playwright/mcp) (official repo: [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)) to give Claude Code a browser it can control — navigate pages, click buttons, fill forms, take screenshots. Requires Node.js 18+.

Works out of the box for testing web apps, verifying UI changes, or walking through demo flows. See the [Playwright MCP README](https://github.com/microsoft/playwright-mcp) for tool reference.

---

### Atlassian (Jira, Confluence, Compass)

When you enable **Jira** or **Confluence** in onboarding, setup adds the [Atlassian Rovo MCP Server](https://github.com/atlassian/atlassian-mcp-server) to `.mcp.json` (remote URL: `https://mcp.atlassian.com/v1/mcp`).

- **Auth:** On first use in Claude Code, complete the **OAuth 2.1** flow in your browser (or use an API token if your org enables it).
- **No placeholder keys** — authorize when Claude Code prompts you.
- **Docs:** [Atlassian MCP Server README](https://github.com/atlassian/atlassian-mcp-server) — prerequisites, permissions, troubleshooting.

### Google Workspace CLI (optional — not an MCP)

For full **Google Workspace** access (Drive, Gmail, Calendar, Sheets, Docs, Chat) from the command line, you can install the [Google Workspace CLI](https://github.com/googleworkspace/cli) (`gws`). This is separate from the Google Drive MCP; use it when you want CLI/scripted access.

1. **Install:** `npm install -g @googleworkspace/cli`
2. **One-time setup:** `gws auth setup` (creates GCP project, enables APIs, OAuth login)
3. **Subsequent login:** `gws auth login`

Then use `gws drive ...`, `gws gmail ...`, etc. No entry in `.mcp.json` — it's a CLI.

---

## Other MCPs (Linear, Notion, etc.)

For MCPs not in our auto-generated config, add them via Claude Code's `/mcp` command or by editing `.mcp.json` directly.

Using the `/mcp` command:
1. In Claude Code chat, run `/mcp`
2. Follow prompts to add a server (name, command/URL, env vars)
3. Claude Code writes the entry to `.mcp.json` (project) or `~/.claude.json` (user)

Or edit `.mcp.json` directly — the schema matches `{"mcpServers": {...}}`.

| MCP | Notes |
|-----|-------|
| Jira / Confluence | Auto-added when you enable them in onboarding (Atlassian MCP). See **Atlassian** above. |
| Linear | Use Linear's official MCP or a community server |
| Notion | Use Notion's official MCP |
| Databricks | Community MCP available |

---

## Troubleshooting

**MCPs not loading?**
- Restart Claude Code after editing `.mcp.json` (or run `/mcp reload`)
- Run `/mcp` to list loaded servers and their status
- Check Claude Code logs for MCP errors

**Slack: "invalid_auth"?**
- Regenerate your Bot Token
- Ensure the app is installed to your workspace
- Check Team ID matches your workspace

**Google Drive: auth fails?**
- Run `npx @modelcontextprotocol/server-gdrive auth` in terminal
- Ensure you have a Google Cloud project with Drive API enabled (for custom setups)

**Project vs user config**
- `.mcp.json` at this repo's root = **project-level** — only active when PM-OS is open
- `~/.claude.json` or `~/.claude/mcp.json` = **user-level** — active in all Claude Code sessions
- We use project-level so your work MCPs stay scoped to this setup
