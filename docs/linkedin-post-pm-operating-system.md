# LinkedIn Post — PM Operating System

---

## Post (copy below the line)

I kept re-explaining our strategy to AI. Every new chat, every new session — "here's our segments, here are our goals, here's what we deprioritized last quarter." It felt like onboarding a new hire every morning.

So we built something for ourselves. Then open-sourced it.

**PM Operating System** is a repo you clone into Cursor that gives the LLM your full PM context — once. Strategy, segments, metrics, decisions. It connects to where you already work (Slack, Jira, Drive, Figma, Databricks) and has PM skills baked in: PRDs, working backwards, launch posts, exec updates, strategy reviews.

The real shift is shared context across the team. Everyone's AI works from the same strategy, same priorities, same framing.

Two examples from our team:

1. Our director wrote the strategy doc. He dropped it into the knowledge layer. From there, an agent derived the key metrics. An analytics subagent took those metrics and built the dashboard — querying Databricks, formatting the views. Strategy → metrics → dashboard, same context end to end. No one re-typed anything.

2. When I start a new PRD, I don't brief the AI on our customers or goals. It already has our segments, our strategic pillars, our positioning. I say "write a PRD for X" and it drafts with the right framing. I edit and push — not rewrite from scratch.

It's not magic. It's just context, structured well, loaded consistently.

The knowledge layer evolves into a context graph over time — decisions, feedback trends, strategy shifts accumulate. The more you use it, the more the AI knows what happened and why.

We open-sourced the whole thing. Clone the repo, open in Cursor, say "onboard." A few questions later you have rules, skills, agents, and a knowledge layer configured for your product. Tool connections (MCPs) are optional and come last — add them when you're ready.

Here's what the repo looks like:

```
PM-operating-OS/
├── AGENTS.md                  # Your AI's persistent identity & context
├── ONBOARDING.md              # Interactive setup guide
├── MCP_SETUP.md               # Tool connections (Slack, Jira, Drive…)
│
├── knowledge/                 # The context layer
│   ├── _template/             # Ready-to-fill templates
│   │   ├── strategy.md
│   │   ├── customer-segments.md
│   │   ├── metrics-and-targets.md
│   │   ├── value-proposition.md
│   │   ├── competitive-landscape.md
│   │   └── key-learnings.md
│   └── examples/              # Pre-filled examples (Netflix, Spotify, Uber, Shopify)
│
├── skills/                    # PM skills baked in
│   ├── prd-writer/
│   ├── working-backwards/
│   ├── brainstorming/
│   ├── exec-communicator/
│   ├── launch-post/
│   ├── experiment-designer/
│   ├── stakeholder-update/
│   ├── decision-logger/
│   ├── one-pager/
│   ├── strategy-connector/
│   ├── what-if/
│   └── writing-clearly/
│
├── agents/                    # Autonomous PM agents
├── memory/                    # Accumulated context over time
│   ├── decisions/
│   ├── feedback/
│   ├── strategy-reviews/
│   ├── exec-updates/
│   └── weekly-plans/
│
├── templates/                 # Agent & rule templates
├── output/                    # Generated artifacts land here
├── config/                    # PM-OS configuration
└── scripts/                   # Setup automation
```

If you're a PM using AI and tired of re-explaining context, this might save you real time.

Repo: github.com/Sach1ng/PM-operating-OS

#ProductManagement #AI #Cursor #OpenSource
