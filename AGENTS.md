# InstaAgent

- Use the matching Instagram skill in `.agents/skills/`. Run each Python helper from its skill folder or invoke it by its full path. Resolve shared resources such as `ig-reel/hooks.json` from `.agents/skills/`.
- Read `instagram/voice.md` for the creator's voice, audience, and approved claims. Shared plans, logs, and swipe files belong in `instagram/`, relative to this workspace.
- For a live profile check or content audit, use the `instagram` Windsor.ai MCP server. Check `get_connectors` for a connected Instagram account, then retrieve the account's available profile or post metrics. If the account is missing, use `get_connector_connect_info` for `instagram` to get the connection link. Use exports or screenshots for fields the connector does not provide.
- Instagram skills produce drafts. Publishing, commenting, and sending messages require a separate, explicit user instruction.
- For the end-to-end health and wellness reel production workflow, use `.agents/skills/ig-producer/SKILL.md`. The user reviews and approves the script and visual reference before generation; approval of a single scene does not approve all scenes.
