# InstaAgent

InstaAgent is a workspace for producing Indian health and wellness podcast reels with Aryana. Ask Codex: “Use InstaAgent to research one health reel and prepare a video.” The workflow is defined in [.agents/skills/ig-producer/SKILL.md](.agents/skills/ig-producer/SKILL.md).

The agent researches and attributes references, develops a sourced Hinglish script and visual, pauses for approval, produces one Flow video per scene, reviews the clips and stitches them. Research and Flow interaction are agent-guided tasks; this is not an unattended background service. Publishing requires a separate instruction.

The user’s preferences, reference asset locations and sample are recorded in [instagram/production-brief.md](instagram/production-brief.md). Each source concept should have its own production folder and finished video. The first test clip is in `instagram/flow-output/`.

## Production records

The assistant can use the local helper to record a review package and assemble its clips:

```bash
PY=.tools/instaagent-venv/bin/python
TOOL=.agents/skills/ig-producer/scripts/production.py
"$PY" "$TOOL" prepare instagram/runs/example --script /absolute/path/to/storyboard.md --visual /absolute/path/to/reference.png --source /absolute/path/to/source-notes.md --scenes 8
"$PY" "$TOOL" status instagram/runs/example
# Only after the user explicitly approves the complete package:
"$PY" "$TOOL" approve instagram/runs/example
"$PY" "$TOOL" add-clip instagram/runs/example --scene 1 --file /absolute/path/to/scene-1.mp4
# Add every remaining reviewed scene in the same way.
"$PY" "$TOOL" stitch instagram/runs/example
```

The approval record fingerprints the review files and scene count. If they change, `check`, `add-clip`, and `stitch` stop until the revised package is approved. The helper is a local workflow aid, not a security boundary: Google Flow itself is external and can be operated outside it. The assistant must honor the approval checkpoint. Clips must contain audio and are normalized to 1080×1920, 30 fps, H.264/AAC before joining; inspect the output after export.

The virtual environment contains `imageio-ffmpeg`; recreate it with `python3 -m venv .tools/instaagent-venv` and `.tools/instaagent-venv/bin/pip install imageio-ffmpeg` if needed.

## Current integration limits

- The installed unofficial Flow MCP can read projects and download assets. Local additions `flow_agent_options`, `flow_agent_prepare`, `flow_agent_confirm`, and `flow_agent_reject` target Flow's current Agent interface. One live test successfully attached an image, prepared and confirmed a 30-credit quote, waited for a new video and downloaded a 10-second 720×1280 clip with audio. A prior attempt failed when its browser closed too early; the confirmation path now waits for a new media tile, and an unconfirmed submission must be checked in Flow before retrying. This single test does not establish reliability for all videos. Quotes exist only within the same running MCP server process; reopening the server invalidates them. The original composer controls still may not work. Flow UI changes, account sign-in and credit availability can interrupt production.
- The test used a described voice. Flow did not accept the supplied MP4 as a direct voice input, and the upload picker did not accept the extracted WAV in that interaction. Matching Aryana’s reference voice remains unresolved.
- Trending-reel research needs live access and available metrics; the workflow must label missing baselines and cannot guarantee a definitive ranking. Instagram login, where needed, is performed by the user.
- Review and quality checks require an agent with access to the actual generated clips. The helper cannot assess speech, lip sync, factual accuracy or edit quality.
