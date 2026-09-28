# Agile board and role agents

Board: [AssetForge Project #3](https://github.com/users/vitaliybilyak25/projects/3)

Agents live in this repository under `.claude/agents/`. The Project is the board. You (the human) are the Product Owner.

## Project fields

Project #3 has **Sprint** (iteration), **Status**, **Priority**, **Size**, and **Kind** (Epic/Story).

- Use **Sprint** as the sprint. Filter views with `@current` / `@next`.
- Roll unfinished work to the next sprint from a view grouped by Sprint.
- Do not invent a second sprint tracker.

## Labels

| Label | Meaning |
|---|---|
| `needs-refinement` | Missing story, AC, or ready checklist |
| `ready` | PO approved; a developer or tester may be assigned |
| `blocked` | Waiting on a dependency or decision |
| `agent:ba` | Business Analyst should refine |
| `agent:dev` | Developer (default Copilot / Cursor) should implement |
| `agent:qa` | Tester should verify or add tests |

## Ready checklist

An issue is `ready` only when all of these are true:

- [ ] User story in As a / I want / So that
- [ ] In scope and out of scope listed
- [ ] Testable acceptance criteria
- [ ] Dependencies and risks named
- [ ] Epic link present on the issue (parent field or body reference)
- [ ] If the story contains a worked example against a named external schema or API, the example has been verified against the source
- [ ] PO (human) approved the cut

## Board status rules

When an issue receives the `ready` label, the Scrum Master or Product Owner agent **must** immediately set its board **Status** to `Ready`. Do not leave `ready`-labelled issues in `Backlog`.

| Label state | Board Status |
|---|---|
| `needs-refinement` | Backlog |
| `ready` | Ready |
| In progress (picked up) | In Progress |
| PO reviewing | In Review |
| Accepted | Done |

All sprint issues must be **assigned** to a team member when the sprint starts.

## Handoff

```
BA or PO draft → you approve → label ready + set Status Ready + assign → developer or tester picks up
```

No agent assigns another agent without your trigger. No agent reorders the backlog or accepts a sprint.

## Ceremonies (human-triggered)

- **Planning:** Scrum facilitator reads current and next Sprint, proposes a sprint goal and a cut line; you confirm.
- **Refinement:** BA takes `needs-refinement` issues and writes AC back onto the issue.
- **Standup:** Facilitator posts Yesterday / Today / Blockers on the sprint issue you name.
- **Review / Retro:** Tester plus facilitator summarize merged PRs and one process change; you accept.

## Role scope

| Role | May do | Must not do |
|---|---|---|
| Product Owner (you) | Prioritize, accept sprint, accept increment | — |
| Product Owner agent | Draft stories, AC, MoSCoW options | Reorder backlog or accept a sprint |
| Business Analyst | Briefs, AC, RICE, process maps | Write production code |
| Scrum Master | Ceremony notes, blocker list, board hygiene | Invent scope or assign work |
| Developer | Implement one ready issue, open a PR | Merge to main or expand scope |
| Tester | Tests, AC verification, review comments | Change product behavior to make tests pass |
