# Dispatch

> A task manager for AI agents — queue work, track progress, and review results across multiple models.

![Dark UI screenshot](https://img.shields.io/badge/status-prototype-blue?style=flat-square) ![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

---

## What is Dispatch?

Dispatch is a clean, dark-themed interface for managing tasks that are executed by AI agents. Instead of manually doing work yourself, you describe what needs to be done, assign it to an AI agent, and track its progress in real time.

Built for teams and individuals who delegate research, writing, code review, data processing, and other knowledge work to models like Claude, GPT-4o, and others.

---

## Features

- **Task queue** — create tasks and assign them to any AI agent
- **Live status tracking** — Running, Reviewing, Queued, Done, and Failed states with animated indicators
- **Multi-agent support** — works across Claude, GPT-4o, DeepL, AutoGPT, and more
- **Progress bars** — see how far along each agent is in real time
- **Agent logs** — inspect what the agent did, step by step
- **Priority levels** — High, Medium, Low with color-coded indicators
- **Responsive design** — full desktop layout with sidebar + table, and a native-feeling mobile view

---

## Getting Started

This is currently a static HTML prototype. Open `index.html` in any browser.

```bash
git clone https://github.com/dannol/dispatch.git
cd dispatch
open index.html
```

No build step, no dependencies.

---

## Roadmap

- [ ] New task modal with agent selector
- [ ] Real API integration (Claude, OpenAI)
- [ ] Persistent task storage
- [ ] Webhook support for task completion callbacks
- [ ] Team/workspace sharing
- [ ] Mobile app

---

## Design

Inspired by the clean dark aesthetic of tools like Craft and Linear. Built with vanilla HTML, CSS, and JS — no frameworks.

---

## License

MIT
