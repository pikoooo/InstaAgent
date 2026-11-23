# InstaAgent production brief

## Goal

Research 5–6 currently performing Instagram reels in health and wellness, use the findings to develop original podcast-style reels featuring the user's virtual influencer, and produce a stitched final video after approval.

## Workflow

1. Research recent reels, recording links, creators, dates, views and available account baselines. Rank candidates using relative performance where evidence permits; label missing data and avoid claiming a definitive trend ranking from an incomplete sample. Save references and attribution. Download reference videos when an authorized, supported method is available; do not assume every reel is downloadable.
2. Select an idea and verify health claims against reliable, current primary or public-health sources. Write original scripts in the influencer's voice, drawing on the structural lessons rather than copying source videos. Divide each script into coherent 10–15 second production segments.
3. Prepare a storyboard and visual references showing the influencer at a podcast microphone, with shot descriptions, dialogue, continuity details, and sources for claims.
4. Pause for the user's approval of the script and visuals. Changes after approval require review before generating affected segments.
5. Generate the approved video segments with an available video provider, preserving the influencer's appearance, voice, setting and vertical framing. Review each clip for speech, continuity and factual accuracy; regenerate or flag failures.
6. Stitch accepted clips in order, check audio and transitions, and deliver the final video and source references. Publishing requires a separate explicit instruction.

## Information to establish

- Influencer name, voice characteristics and permitted use.
- Health topics and creative boundaries.
- Whether 5–6 research references should result in one video or one video per topic, and the desired finished length.
- Instagram access and a supported way to save reference videos; a video-generation provider and account; and an available stitching tool.

## Influencer references

- Appearance and podcast setting: `/Users/puneetkapoor/Documents/2. Health and wellness/Virtual influrncer face + Voice/Our Virtual Influencer.png`.
- User-provided voice reference video: `/Users/puneetkapoor/Documents/2. Health and wellness/Virtual influrncer face + Voice/2.mp4`. Voice and provider compatibility still need to be assessed.

## Audience and language

The primary audience is in India. Scripts should use a natural mix of Hindi and English, guided by the user's reference video. The first sleep pilot was drafted in English before this direction was supplied and needs revision after the user's review. The user will provide detailed feedback; wait for explicit approval of both script and visuals before generating video.

## Scene-writing example

User's sample and comments: `/Users/puneetkapoor/Documents/2. Health and wellness/Gut Health Video/Video Script Sample For AI Training.txt`. Nine example scene outputs are in the same folder. The sample names the presenter Aryana.

- One finished video covers the relevant points together. Divide scenes primarily by spoken dialogue length for the approximately 10-second model limit, even when one point needs multiple scenes. Keep the podcast setting continuous unless a creative change is approved.
- The user's scene 3 is the preferred pacing example (about 28 space-delimited words); scene 1 (about 34) fitted but sounded a little fast, and scene 2 (about 25) left a pause. Word counts are only rough guides: language, pronunciation and pauses affect actual duration. Allow buffer and review outputs for cut-off dialogue. The user gave no pacing verdict on the remaining scenes.
- Write conversational Roman-script Hindi mixed naturally with English, address the viewer respectfully, open with relatable symptoms or a question, offer reassurance, and explain numbered points with familiar Indian examples. Develop an explanation across multiple scenes when needed, and close with a balanced takeaway.
- Each scene prompt states setting, camera when useful, action and exact dialogue. Use restrained gestures, expressions, camera moves and relevant B-roll or text overlays; the presenter remains the main character. Prepare a character-and-setting reference image in pre-production for approval alongside the script; clothing and room can vary.
- Extract the source's relevant points comprehensively, distinguish satire from usable claims, and verify health claims before writing. Preserve the user's point-to-scene distinction. Do not assume every sample health claim has been independently verified.

## Current implementation status

Instagram research and writing skills are installed. This document describes the intended workflow; it is not an automated pipeline. At initial inspection Google Flow and Windsor Instagram tools were not exposed in the session, OpenArt video tools were exposed but not verified for this project, and `ffmpeg` was not on the shell path.
