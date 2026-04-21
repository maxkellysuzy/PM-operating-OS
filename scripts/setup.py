#!/usr/bin/env python3
"""
PM Operating System — Setup script (Claude Code edition)
Reads config/pm-os-config.yaml and generates personalized CLAUDE.md, agents, and skills.
Also generates .mcp.json for selected MCPs — users just add their API keys.
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    import yaml
    from jinja2 import Environment, FileSystemLoader
except ImportError as e:
    print("Error: Missing dependencies. Run: pip install -r requirements.txt")
    print(f"  {e}")
    sys.exit(1)


def load_config() -> dict:
    config_path = PROJECT_ROOT / "config" / "pm-os-config.yaml"
    if not config_path.exists():
        print(f"Error: Config not found at {config_path}")
        print("  1. Copy config/pm-os-config.yaml if needed")
        print("  2. Fill in your answers from ONBOARDING.md")
        sys.exit(1)
    with open(config_path) as f:
        return yaml.safe_load(f)


def build_template_context(cfg: dict) -> dict:
    """Build a flat context for Jinja2 templates."""
    identity = cfg.get("identity", {})
    stakeholders = cfg.get("stakeholders", {})
    goals = cfg.get("goals", [])
    deprioritize = cfg.get("deprioritize", {})
    slack = cfg.get("slack", {})
    gdrive = cfg.get("google_drive", {})
    domain = cfg.get("domain", {})

    ctx = {
        "product": identity.get("product", "My Product"),
        "role": identity.get("role", "PM"),
        "company": identity.get("company", "My Company"),
        "product_type": identity.get("product_type", "product"),
        "managers": ", ".join(stakeholders.get("managers", [])),
        "org_structure": stakeholders.get("org_structure", ""),
        "deprioritize": deprioritize,
        "deprioritize_flat": deprioritize.get("low_priority", []) + deprioritize.get("never_prioritize", []),
        "goals": goals,
        "vip_senders": stakeholders.get("vip_senders", []),
        "identity": identity,
        "domain": domain,
        "feedback_channel": slack.get("feedback_channel", "#feedback"),
        "feedback_channel_id": slack.get("feedback_channel_id", ""),
        "dm_recipient_id": slack.get("dm_recipient_id", ""),
        "monday_planning_doc_id": gdrive.get("monday_planning_doc_id", ""),
        "daily_standup_doc_id": gdrive.get("daily_standup_doc_id", ""),
        "pmo_sheet_url": gdrive.get("pmo_sheet_url", ""),
    }
    return ctx


def render_template(env: Environment, name: str, ctx: dict) -> str:
    template = env.get_template(name)
    return template.render(ctx)


# MCP configs we can auto-generate (official npm packages or URL-based).
# Other MCPs: user adds via Claude Code's /mcp command or by editing .mcp.json.
MCP_CONFIGS = {
    "slack": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-slack"],
        "env": {
            "SLACK_BOT_TOKEN": "YOUR_SLACK_BOT_TOKEN",
            "SLACK_TEAM_ID": "YOUR_SLACK_TEAM_ID",
        },
    },
    "google_drive": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-gdrive"],
        "env": {},
    },
    "github": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_GITHUB_TOKEN"},
    },
    "figma": {
        "url": "https://mcp.figma.com/mcp",
        "headers": {},
    },
    # Figma Context MCP (Framelink) — layout/data for AI; requires API key.
    "figma_developer": {
        "command": "npx",
        "args": ["-y", "figma-developer-mcp", "--stdio"],
        "env": {"FIGMA_API_KEY": "YOUR_FIGMA_API_KEY"},
    },
    # Atlassian (Jira, Confluence, Compass) — OAuth on first use.
    "atlassian": {
        "url": "https://mcp.atlassian.com/v1/mcp",
        "headers": {},
    },
    "browser": {
        "command": "npx",
        "args": ["@playwright/mcp@latest"],
        "env": {},
    },
}


def generate_mcp_config(cfg: dict) -> None:
    """Generate .mcp.json at project root from tools config.
    Users replace placeholders with real keys, then Claude Code loads them on startup.
    """
    tools = cfg.get("tools", {})
    tool_keys_with_mcp = set(tools.keys()) & set(MCP_CONFIGS.keys())
    if not tool_keys_with_mcp and not (tools.get("jira") or tools.get("confluence")):
        return

    mcp_servers = {}
    for tool_key, enabled in tools.items():
        if not enabled or tool_key not in MCP_CONFIGS:
            continue
        mcp_servers[tool_key] = MCP_CONFIGS[tool_key].copy()
        if "env" in mcp_servers[tool_key]:
            mcp_servers[tool_key]["env"] = dict(mcp_servers[tool_key]["env"])
    # Atlassian MCP (Jira + Confluence): add when user enables jira or confluence
    if (tools.get("jira") or tools.get("confluence")) and "atlassian" not in mcp_servers:
        mcp_servers["atlassian"] = MCP_CONFIGS["atlassian"].copy()
    # Figma Context MCP (Framelink): add when user enables figma (in addition to hosted Figma)
    if tools.get("figma") and "figma_developer" not in mcp_servers:
        mcp_servers["figma_developer"] = MCP_CONFIGS["figma_developer"].copy()
        if "env" in mcp_servers["figma_developer"]:
            mcp_servers["figma_developer"]["env"] = dict(mcp_servers["figma_developer"]["env"])

    if not mcp_servers:
        return

    mcp_path = PROJECT_ROOT / ".mcp.json"
    mcp_path.write_text(json.dumps({"mcpServers": mcp_servers}, indent=2), encoding="utf-8")
    print(f"  Generated .mcp.json ({len(mcp_servers)} MCPs)")
    print("  -> Replace placeholders in .mcp.json with your API keys. See MCP_SETUP.md")


def main():
    parser = argparse.ArgumentParser(description="PM-OS setup: generate personalized Claude Code config")
    parser.add_argument("--copy", action="store_true", help="Also deploy to ~/.claude (user-level, cross-project)")
    parser.add_argument("--symlink", action="store_true", help="Symlink to ~/.claude instead of copy")
    parser.add_argument("--output-only", action="store_true", help="Only generate to output/, don't write to project root or user dir")
    parser.add_argument("--claude-path", default=None, help="Override user Claude dir (default ~/.claude)")
    args = parser.parse_args()

    cfg = load_config()
    tools = cfg.get("tools", {})
    skills_cfg = cfg.get("skills", {})
    agents_cfg = cfg.get("agents", {})

    if args.output_only:
        mode = "output_only"
    elif args.symlink:
        mode = "symlink"
    elif args.copy:
        mode = "copy"
    else:
        mode = cfg.get("output", {}).get("mode", "project")  # default: write to project .claude/ only

    claude_path = Path(args.claude_path or cfg.get("output", {}).get("claude_path", "~/.claude")).expanduser()
    output_dir = PROJECT_ROOT / "output"
    output_dir.mkdir(exist_ok=True)

    for d in ["agents", "skills"]:
        (output_dir / d).mkdir(exist_ok=True)
        for f in (output_dir / d).iterdir():
            if f.is_file():
                f.unlink()

    env = Environment(
        loader=FileSystemLoader(PROJECT_ROOT / "templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    ctx = build_template_context(cfg)

    # 1. Generate CLAUDE.md at project root (combines chief-of-staff + domain context)
    claude_md_content = render_template(env, "CLAUDE.md.template", ctx)
    claude_md_path = output_dir / "CLAUDE.md"
    claude_md_path.write_text(claude_md_content, encoding="utf-8")
    print(f"  Generated output/CLAUDE.md")

    # Write to project root too (the actual file Claude Code reads for this workspace)
    if mode != "output_only":
        (PROJECT_ROOT / "CLAUDE.md").write_text(claude_md_content, encoding="utf-8")
        print(f"  Deployed CLAUDE.md to project root")

    # 2. Copy base agents (onboarding, company-researcher, subagents) to output/agents/
    claude_agents_src = PROJECT_ROOT / ".claude" / "agents"
    for agent_name in ("pm-os-onboarding", "company-researcher", "company-strategy", "company-product-signals"):
        agent_src = claude_agents_src / f"{agent_name}.md"
        if agent_src.exists():
            shutil.copy2(agent_src, output_dir / "agents" / f"{agent_name}.md")
            print(f"  Copied agents/{agent_name}.md")

    # 3. Feedback analyzer (if Slack/Teams + enabled)
    has_chat = tools.get("slack") or tools.get("teams")
    if has_chat and agents_cfg.get("feedback_analyzer"):
        fa_content = render_template(env, "agents/feedback-analyzer.md.template", ctx)
        (output_dir / "agents" / "feedback-analyzer.md").write_text(fa_content, encoding="utf-8")
        print(f"  Generated agents/feedback-analyzer.md")
    else:
        print(f"  Skipped agents/feedback-analyzer.md (chat={has_chat}, feedback_analyzer={agents_cfg.get('feedback_analyzer')})")

    # 4. Weekly planner (if Google Drive + chat + enabled)
    if has_chat and tools.get("google_drive") and agents_cfg.get("weekly_planner"):
        wp_content = render_template(env, "agents/weekly-planner.md.template", ctx)
        (output_dir / "agents" / "weekly-planner.md").write_text(wp_content, encoding="utf-8")
        print(f"  Generated agents/weekly-planner.md")
    else:
        print(f"  Skipped agents/weekly-planner.md")

    # 4b. Strategy reviewer (if enabled)
    if agents_cfg.get("strategy_reviewer"):
        sr_content = render_template(env, "agents/strategy-reviewer.md.template", ctx)
        (output_dir / "agents" / "strategy-reviewer.md").write_text(sr_content, encoding="utf-8")
        print(f"  Generated agents/strategy-reviewer.md")

    # 4c. Exec update generator (if enabled)
    if agents_cfg.get("exec_update_generator"):
        eu_content = render_template(env, "agents/exec-update-generator.md.template", ctx)
        (output_dir / "agents" / "exec-update-generator.md").write_text(eu_content, encoding="utf-8")
        print(f"  Generated agents/exec-update-generator.md")

    # 4d. Retrospective agent (if enabled)
    if agents_cfg.get("retrospective"):
        retro_content = render_template(env, "agents/retrospective.md.template", ctx)
        (output_dir / "agents" / "retrospective.md").write_text(retro_content, encoding="utf-8")
        print(f"  Generated agents/retrospective.md")

    # 5. Memory directory — create if it doesn't exist
    memory_dir = PROJECT_ROOT / "memory"
    for subdir in ["decisions", "feedback", "weekly-plans", "strategy-reviews", "exec-updates", "knowledge-snapshots", "learning-log"]:
        (memory_dir / subdir).mkdir(parents=True, exist_ok=True)
    print(f"  Memory directory ready at {memory_dir}")

    # 6. Skills — copy from skills/ to output/skills/
    skills_src = PROJECT_ROOT / "skills"
    templates_dir = PROJECT_ROOT / "templates"

    if skills_cfg.get("prd_writer", True):
        skill = "prd-writer"
        if (skills_src / skill).exists():
            shutil.copytree(skills_src / skill, output_dir / "skills" / skill, dirs_exist_ok=True)
            print(f"  Copied skills/{skill}/")

    if skills_cfg.get("working_backwards", True):
        skill = "working-backwards"
        if (skills_src / skill).exists():
            shutil.copytree(skills_src / skill, output_dir / "skills" / skill, dirs_exist_ok=True)
            print(f"  Copied skills/{skill}/")

    if skills_cfg.get("pptx_creator", True):
        skill = "pptx-creator"
        if (skills_src / skill).exists():
            shutil.copytree(skills_src / skill, output_dir / "skills" / skill, dirs_exist_ok=True)
            print(f"  Copied skills/{skill}/")

    SKILL_MAP = {
        "strategy_connector": "strategy-connector",
        "exec_communicator": "exec-communicator",
        "experiment_designer": "experiment-designer",
        "launch_readiness": "launch-readiness",
        "launch_post": "launch-post",
        "one_pager": "one-pager",
        "stakeholder_update": "stakeholder-update",
        "meeting_to_actions": "meeting-to-actions",
        "experiment_writeup": "experiment-writeup",
        "brainstorming": "brainstorming",
        "writing_clearly": "writing-clearly",
        "decision_logger": "decision-logger",
        "what_if": "what-if",
        "knowledge_updater": "knowledge-updater",
        "continual_learning": "continual-learning",
    }
    for cfg_key, folder_name in SKILL_MAP.items():
        if skills_cfg.get(cfg_key, False) and (skills_src / folder_name).exists():
            shutil.copytree(skills_src / folder_name, output_dir / "skills" / folder_name, dirs_exist_ok=True)
            print(f"  Copied skills/{folder_name}/")

    # Action-item-prioritizer: generate from template (has goals/VIPs)
    if skills_cfg.get("action_item_prioritizer", True):
        ap_dir = output_dir / "skills" / "action-item-prioritizer"
        ap_dir.mkdir(parents=True, exist_ok=True)
        ap_tpl = templates_dir / "skills" / "action-item-prioritizer" / "SKILL.md.template"
        if ap_tpl.exists():
            env_ap = Environment(
                loader=FileSystemLoader(templates_dir / "skills" / "action-item-prioritizer"),
                trim_blocks=True,
                lstrip_blocks=True,
            )
            content = env_ap.get_template("SKILL.md.template").render(ctx)
            (ap_dir / "SKILL.md").write_text(content, encoding="utf-8")
            print(f"  Generated skills/action-item-prioritizer/SKILL.md")

    print(f"\nOutput written to: {output_dir}")

    # Always generate MCP config when tools are selected (project-level .mcp.json)
    generate_mcp_config(cfg)

    if mode == "output_only":
        print("\nNext: Copy or symlink from output/ to your Claude Code directory, or open this workspace in Claude Code as-is.")
        return

    # Always deploy generated agents/skills into project's .claude/ directory
    project_claude = PROJECT_ROOT / ".claude"
    project_agents = project_claude / "agents"
    project_skills = project_claude / "skills"
    project_agents.mkdir(parents=True, exist_ok=True)
    project_skills.mkdir(parents=True, exist_ok=True)

    def deploy_files(src: Path, dst_dir: Path, link: bool):
        for f in src.iterdir():
            if f.is_file():
                target = dst_dir / f.name
                if target.exists() or target.is_symlink():
                    target.unlink()
                if link:
                    target.symlink_to(f.resolve())
                else:
                    shutil.copy2(f, target)

    def deploy_skills(src_skills: Path, dst_skills: Path, link: bool):
        for skill_dir in src_skills.iterdir():
            if skill_dir.is_dir():
                dst = dst_skills / skill_dir.name
                if dst.exists() or dst.is_symlink():
                    if dst.is_symlink():
                        dst.unlink()
                    else:
                        shutil.rmtree(dst)
                if link:
                    dst.symlink_to(skill_dir.resolve())
                else:
                    shutil.copytree(skill_dir, dst)

    # Deploy to project's own .claude/ (always)
    deploy_files(output_dir / "agents", project_agents, link=False)
    deploy_skills(output_dir / "skills", project_skills, link=False)
    print(f"\nDeployed to project .claude/ (agents + skills)")

    # Optionally deploy to user-level ~/.claude/ for cross-project availability
    if mode in ("copy", "symlink"):
        user_agents = claude_path / "agents"
        user_skills = claude_path / "skills"
        user_agents.mkdir(parents=True, exist_ok=True)
        user_skills.mkdir(parents=True, exist_ok=True)

        link = (mode == "symlink")
        deploy_files(output_dir / "agents", user_agents, link=link)
        deploy_skills(output_dir / "skills", user_skills, link=link)
        print(f"Also deployed to {claude_path} (mode={mode})")

    print("Done. Open this repo in Claude Code — CLAUDE.md, .claude/agents/, .claude/skills/, and .mcp.json will load automatically.")


if __name__ == "__main__":
    main()
