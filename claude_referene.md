# CLAUDE.md Best Practices

**Core Purpose**
`CLAUDE.md` serves as **the onboarding handbook for your project**. It transforms Claude Code from a general-purpose AI assistant into a specialized development tool that understands your team's specific context, conventions, and constraints. Properly tuned, it can drastically reduce unnecessary output, stop hallucinated fixes, and save you tokens on repetitive tasks.

**Token Efficiency & The Input/Output Trade-off**
Every word Claude generates costs tokens. By default, Claude includes unsolicited suggestions, flattering preamble ("Sure!", "Great question!"), and restates questions—all of which add zero value.

* **The Trade-off:** Loading a `CLAUDE.md` file consumes *input* tokens on every single message. The cost savings come purely from reducing *output* verbosity.
* **When to use it:** It is highly effective for persistent sessions, high-volume automation pipelines, and repetitive structured tasks. In these scenarios, an optimized `CLAUDE.md` can reduce word count by over 60%.
* **When to avoid it:** Do not use heavy `CLAUDE.md` rules for single short queries, casual one-off use, or fresh sessions per task, as the persistent input token cost will outweigh the output savings.

**File Hierarchy and Scope**
Claude Code utilizes a **layered loading model**, meaning multiple `CLAUDE.md` files compose and take effect simultaneously.

* **User-Level (`~/.claude/CLAUDE.md`)**: Best for global personal preferences, such as tone, format, and avoiding sycophantic chatter.
* **Project-Level (`./CLAUDE.md`)**: Shared via version control to dictate default repository behavior and project-specific constraints (e.g., "never modify `/config`").
* **Local Project-Level (`CLAUDE.local.md`)**: Ideal for private, uncommitted notes.
* **Subdirectory Level**: These files are only loaded when Claude Code actually reads content from that specific folder. Keep task-specific rules here to prevent bloating the root file.

**Loading Rules and Conflict Resolution**

* **The Nearest-Scope Principle**: When multiple files conflict, the rule closest to the active task and narrowest in scope takes priority.
* **Override Rule**: User instructions *always* win. If you explicitly ask for a verbose explanation in the chat, Claude will ignore brevity rules in the file.

**What to Include (and How to Write It)**

* **Target Specific Failures:** Generic rules ("be concise", "pay attention to code quality") are far less effective than targeting actual failure modes. For example, if Claude fails on pipelines, write: "when a step fails, stop immediately and report the full error with traceback before attempting any fix".
* **Communicate Intent**: Explain *why* rules exist. Instead of just "do not modify `src/generated/`", state that they are auto-generated from an OpenAPI schema, pointing the AI to the true source of truth.
* **High-Impact Fixes to Include:** Enforce that Claude must read files before writing, run tests before declaring a task "done", read unchanged files only once, and prefer targeted edits over large file rewrites.

**Continuous Evolution & Workflow Profiles**

* **Start Lean:** Use `/init` to generate a draft, but aggressively delete generic information so it doesn't waste the context window.
* **Use Versioned Profiles:** Depending on the project, you might adopt specific tool budgets:
  * *v5 Strategy*: For complex multi-step workflows with detailed agent protocols (50 tool calls).
  * *v6 Strategy*: For faster execution with strict "done means done" rules (no polishing passing code).
  * *v8 Strategy*: Ultra-lean for cost-sensitive pipelines (20 tool calls).
* **Automate Retrospectives**: Run `/reflection` at the end of sessions to have Claude summarize stable lessons and add them to the file. Periodically run `/insights` to analyze long-term usage history and formally record recurring habits.
* **Split as You Grow**: Keep the main file disciplined. Use `@imports` to split out complex, detailed workflows into separate files.

**Security Warning**

* **Never put API keys, passwords, tokens, or other secrets in `CLAUDE.md`**, as this file is typically tracked in version control.

***

### Comprehensive References

Here is the updated list of references, drawing from both the official guides and the `claude-token-efficient` repository:

* [*The Complete Guide to Claude Code: CLAUDE.md* by zhaozhiming](https://ai.gopubby.com/the-complete-guide-to-claude-code-claude-md-743d4cbac757?gi=ed78fdd60759#bypass)
* [*drona23/claude-token-efficient*](https://github.com/drona23/claude-token-efficient)
* *How to Write a Good CLAUDE.md File*
* *Writing a good CLAUDE.md*
* *Understanding CLAUDE.md Loading in Large Monorepos*
* *Manage Claude's memory*
* *AGENTS.md*
*   [TurboDocx: CLAUDE.md Best Practices](https://www.turbodocx.com/blog/how-to-write-claude-md-best-practices)
*   [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice)
*   [GitHub Gist: AGENTS.md Guidelines](https://gist.github.com/jerdaw/3917eab775d3e4bbcf37928101fbc3db)
*   [egghead.io: CLAUDE.md Initialization and Best Practices in Claude Code](https://egghead.io/claude-md-initialization-and-best-practices-in-claude-code~jae0x)
* *Anthropic Docs - Reduce Hallucinations*
* *PromptHub - "Three Prompt Engineering Methods to Reduce Hallucinations"*
* *DEV Community - "7 Ways to Cut Your Claude Code Token Usage"*
* *Medium - "Stop Wasting Tokens: Optimize Claude Code Context by 60%"*
### Official Claude Code Documentation
*   [Best Practices](https://code.claude.com/docs/en/best-practices)
*   [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)
*   [Common workflows](https://code.claude.com/docs/en/common-workflows)
*   [Extend Claude Code (Skills, Hooks, MCP, etc.)](https://code.claude.com/docs/en/features-overview)
