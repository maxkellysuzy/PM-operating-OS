# LinkedIn Post — PM Operating System

---

## Post (copy below the line)

I kept re-explaining our strategy to AI. Every new session — "here's our segments, here's what we deprioritized last quarter." Like onboarding a new hire every morning.

So we built something. Then open-sourced it.

**PM Operating System** — a repo you clone into Cursor that gives your AI full PM context, once. Strategy, segments, metrics, decisions. It connects your LLM and IDE to the systems you already work in — Slack, Jira, Drive, Figma, Databricks — and pulls context from them. That context makes every action contextual. No prompting your goals, your segments, your last decision. The AI already knows.

It has 15+ PM skills baked in: PRDs, working backwards, launch posts, exec updates, weekly planning.

The real shift is shared context across the team. Everyone's AI works from the same strategy, same priorities, same framing.

Under the hood, the repo builds a **context graph** — strategy, segments, metrics, decisions, feedback, and plans all linked together. Every artifact you create adds a node. Every decision you log adds an edge. The graph is what lets the AI reason across your product, not just within a single prompt.

What that looks like in practice:

1. Director drops a strategy doc into the knowledge layer. An agent derives key metrics. A subagent builds the Databricks dashboard. Strategy → metrics → dashboard — same graph, no re-typing.

2. I say "write a PRD for X." The AI already has our segments, positioning, and strategic pillars from the graph. I edit and push — not rewrite from scratch.

3. Monday: "plan my week." The agent reads my goals, quarterly priorities, and last 24 hours of Slack. Out comes a daily plan — P0s, P1s, P2s. Tuesday: "plan my day" — it reshuffles based on what actually happened. The graph keeps it grounded in real commitments.

Each example feeds the next. Strategy shapes the PRD. The PRD informs the plan. Decisions logged this quarter shape next quarter's review. It compounds.

Clone the repo, open in Cursor, say "onboard." A few questions later you're set up — knowledge layer, skills, agents, rules. MCPs are optional.

Here's what the repo looks like:

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

github.com/Sach1ng/PM-operating-OS

#ProductManagement #AI #Cursor #OpenSource
