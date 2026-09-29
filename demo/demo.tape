Output demo/demo.gif

Set Shell bash
Set FontSize 16
Set Width 1000
Set Height 620
Set Theme "Dracula"
Set TypingSpeed 30ms

Type "sed -n '84,86p' SKILL.md"
Enter
Sleep 2s

Type "python3 scripts/estimate_cost.py --task --model opus-5-5 --effort high"
Enter
Sleep 800ms
Type "python3 scripts/estimate_cost.py --task --model sonnet-5-5 --effort low"
Enter
Sleep 1.5s

Type "python3 scripts/quota_state.sh"
Enter
Sleep 1.5s

Type "python3 scripts/refresh_models.py --offline"
Enter
Sleep 2s

Type "uv run --with pytest pytest -q"
Enter
Sleep 3s
