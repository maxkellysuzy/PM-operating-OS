# LinkedIn Post — PM Operating System

---

## Post (copy below the line)

I kept re-explaining our strategy to AI. Every new chat, every new session — "here's our segments, here are our goals, here's what we deprioritized last quarter." It felt like onboarding a new hire every morning.

So we built something for ourselves. Then open-sourced it.

**PM Operating System** is a repo you clone into Cursor that gives the LLM your full PM context — once. Strategy, segments, metrics, decisions. It connects to where you already work (Slack, Jira, Drive, Figma, Databricks) and has PM skills baked in: PRDs, working backwards, launch posts, exec updates, strategy reviews.

The real shift is shared context across the team. Everyone's AI works from the same strategy, same priorities, same framing.

Under the hood, the repo builds a **context graph** — strategy, segments, metrics, decisions, feedback, and plans all linked together. Every artifact you create adds a node. Every decision you log adds an edge. The graph is what lets the AI reason across your product, not just within a single prompt.

Three examples of the context graph in action:

1. Our director wrote the strategy doc and dropped it into the knowledge layer — one node. From there, an agent derived the key metrics — another node, linked to strategy. An analytics subagent took those metrics and built the dashboard, querying Databricks and formatting the views. Strategy → metrics → dashboard, three nodes, same graph, no re-typing.

2. When I write a PRD, the AI already has the strategy, segments, and positioning from the graph. I say "write a PRD for X" and it drafts with the right framing — because the PRD skill traverses the same context graph the strategy lives in. I edit and push, not rewrite from scratch.

3. Every Monday I say "plan my week." The agent walks the context graph — reads my goals, quarterly priorities, last week's decisions — then pulls my last 24 hours of Slack to see what's live. It produces a daily plan: P0s, P1s, P2s, with time blocks. Tuesday morning I say "plan my day" and it reshuffles based on what actually happened — new Slack threads, shifted priorities, completed work. The graph keeps the plan grounded in real commitments, not stale to-do lists.

Each example builds on the same graph. The strategy doc feeds the PRD. The PRD informs the weekly plan. Decisions logged this quarter shape next quarter's strategy review. It compounds.

It's not magic. It's just context, structured as a graph, loaded consistently.

We open-sourced the whole thing. Clone the repo, open in Cursor, say "onboard." A few questions later you have rules, skills, agents, and a knowledge layer configured for your product. Tool connections (MCPs) are optional and come last — add them when you're ready.

Here's the structure (see snapshot below):

```
PM-operating-OS/
├── AGENTS.md          # AI identity & persistent context
├── ONBOARDING.md      # Say "onboard" and go
├── knowledge/         # Strategy, segments, metrics, decisions
├── skills/            # PRDs, launch posts, working backwards, 15+ more
├── agents/            # Autonomous PM agents
├── memory/            # Context graph — compounds over time
└── templates/         # Ready-to-use scaffolding
```

If you're a PM using AI and tired of re-explaining context, this might save you real time.

Repo: github.com/Sach1ng/PM-operating-OS

#ProductManagement #AI #Cursor #OpenSource
