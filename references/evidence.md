# Evidence list

Every source key used anywhere in this skill's references, in one place,
fetched 2026-09-29 and 2026-09-30 unless a source has its own date. When
`scripts/refresh_models.py` reports a STALE banner, re-fetch the sources
below that feed references/models.md first, since prices and benchmark
numbers move the most.

## Contents

- [Model pricing and benchmarks](#model-pricing-and-benchmarks)
- [Effort and reasoning docs](#effort-and-reasoning-docs)
- [Quota and pricing pages](#quota-and-pricing-pages)
- [Community sources](#community-sources)
- [Skill authoring and competitors](#skill-authoring-and-competitors)
- [Known gaps in this evidence base](#known-gaps-in-this-evidence-base)

## Model pricing and benchmarks

- S1. platform.claude.com/docs/en/models/overview
- S2. platform.claude.com/docs/en/about-claude/pricing
- S3. platform.claude.com/docs/en/models/{opus-5-5,fable-5-1,sonnet-5-5,haiku-4-5}/overview
- S4. anthropic.com/claude-opus-5-5 (2026-09-22)
- S5. anthropic.com/claude-fable-and-mythos-5-1 (2026-09-01)
- S6. anthropic.com/claude-sonnet-5-5 (2026-09-28)
- S7. developers.openai.com/api/docs/models (plus /gpt-6-astra, /gpt-6-sol)
- S8. developers.openai.com/api/docs/pricing
- S9. developers.openai.com/api/docs/guides/reasoning
- S10. ai.google.dev/gemini-api/docs/pricing
- S11. ai.google.dev/gemini-api/docs/thinking
- S12. blog.google, 3.8 Flash launch post (2026-09-02)
- S13. artificialanalysis.ai/leaderboards/models and model pages
- S14. arena.ai/leaderboard/text (data as of 2026-09-25)
- S15. swebench.com
- S16. labs.scale.com/leaderboard/swe_bench_pro_public
- S17. aider.chat/docs/leaderboards/
- S18. openrouter.ai/rankings (week to 2026-09-28) and openrouter.ai/api/v1/models
- S19. Hugging Face model cards: Qwen/Qwen3.8-27B, zai-org/GLM-5.3, deepseek-ai/DeepSeek-V4.1-Flash, moonshotai/Kimi-K3, kimi.ai/blog/kimi-k3, dev.meta.ai/models/muse-spark
- S38. deepmind.google/models/gemini/flash

## Effort and reasoning docs

- S20. simonwillison.net, 2026/Sep/22 "opus-and-sol-and-luna," Sep/28 "claude-sonnet-5-5," Sep/27 "2026-in-llms-so-far," Sep/21 "jev"
- S21. code.claude.com/docs/en/model-config (re-fetched live 2026-09-30 for this build)
- S22. platform.claude.com/docs/en/build-with-claude/effort
- S23. platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence
- S24. platform.claude.com prompting guides for opus-5-5, sonnet-5-5, fable-5-1
- S25. learn.chatgpt.com/docs: config-reference (re-fetched live 2026-09-30), models, model-selection, pricing, agent-configuration/speed
- S26. geminicli.com/docs: quota-and-pricing, cli/model (re-fetched live 2026-09-30), cli/model-routing, cli/generation-settings
- S28. opencode.ai/docs/models

## Quota and pricing pages

- S29. claude.com/pricing, claude.com/pricing/max, support.claude.com articles 11049741, 12429409, 9797557, 17007452, 11647753
- S30. code.claude.com/docs/en/{costs,errors,interactive-mode,sub-agents,best-practices}
- S27. cursor.com/docs models, account/pricing, context/max-mode, cursor.com/pricing
- S34. gemini.google/subscriptions

## Community sources

- S31. claude.com/blog/claude-model-and-effort-level-in-claude-code (2026-07-07)
- S32. Hacker News items: 49401549 (2026-08-22), 49881850, 49874728 (2026-09-28), 49850798 (2026-09-25), 49465304 (2026-08-27), 49097780 (2026-07-29)
- S33. github.com/abhishekray07/claude-meter
- S37. mchromiak.github.io, "Typed Decision Models" post (2026-09-17). Github.com/yibie/laya-jev-lab

## Skill authoring and competitors

- S35. agentskills.io/specification (re-fetched live 2026-09-30) and platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices (re-fetched live 2026-09-30)
- S36. Competitor repositories: musistudio/claude-code-router, workweave/router, kerpopule/hermes-jev-skills, modu-ai/moai-adk, EchoBird, hussi9/skill-router, senda-labs/DQIII8, Rishav1996/model-router, frankchu91/coding-agent-router, AndrewStifora/model-grade, marcoaiwithfefe-hub/effort-pick, obra/superpowers, mattpocock/skills, DietrichGebert/ponytail, garrytan/gstack, JuliusBrussee/caveman

## Known gaps in this evidence base

- openai.com and help.openai.com returned 403 during research. ChatGPT
  plan prices are not independently confirmed, only Codex's own
  "estimated messages per window" table (S25).
- Reddit was blocked during research. Community routing evidence leans on
  Hacker News and Simon Willison instead.
- Terminal-Bench, ARC Prize, and LMArena WebDev leaderboard pages are
  client-rendered and were not scraped. Only vendor-quoted Terminal-Bench
  numbers appear here.
- The Gemini CLI settings.json and env var precedence in
  references/effort-controls.md come from the original research pass
  (S11, S26), not the live 2026-09-30 fetch of geminicli.com/docs/cli/model,
  because that page's rendered content did not include those sections at
  fetch time. The `/model` command and `--model` flag syntax in this file
  is confirmed live.
