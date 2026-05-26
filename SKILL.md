---
name: audio-transcript-polish
description: Use when the user provides an audio recording and wants transcription plus an AI-polished稿件. Produces two versions, a verbatim transcript and an optimized稿, detects whether there are multiple speakers, labels speakers only when needed, and creates copy-friendly text/HTML outputs.
---

# Audio Transcript Polish

## Goal

Turn an audio file into two deliverables:

- **逐字稿**: direct transcription, preserving meaning, oral phrasing, repetitions, and obvious pauses as much as useful.
- **AI优化稿**: a polished稿件 based on speech, semantics, intent, behavior, and emotion; remove redundancy, merge repeated ideas, fix order, and make it ready to use.

Both versions should support easy copy. Prefer generating a two-column HTML page with copy buttons plus `.txt` files.

## Output Rules

### Speaker labels

- If the recording has **one speaker**, do **not** add `A：` or any speaker label. Output the text directly.
- If the recording has **more than one speaker**, label speakers as `A：`, `B：`, `C：`... in both 逐字稿 and AI优化稿.
- For multiple speakers, preserve turn order and merge adjacent segments from the same speaker when it improves readability.
- Do not write header lines such as `逐字稿` or `AI优化稿` inside the copyable text content. The page/UI section title can show those labels, but the copied text should start directly with the transcript body.

### Verbatim transcript

- Keep the original wording and oral structure close to the audio.
- Lightly correct obvious ASR errors when context is unambiguous, especially names of known concepts, repeated misheard terms, and homophones.
- Do not over-polish the verbatim version into article prose.
- For single-speaker audio, paragraphs can be split by semantic pauses; for multi-speaker audio, split by speaker turn.

### AI优化稿

- Remove filler, stutters, false starts, and repetitive fragments.
- Merge repeated ideas and reorder only when it improves clarity without changing intent.
- Preserve emotionally meaningful nuance and interpersonal stance.
- For self-media or口播 content, shape it into a publishable script with a clear opening, main argument, personal example, takeaway, and call to action where appropriate.
- For conversations, shape it into a clean dialogue or meeting-style summary while preserving `A/B/C` speaker ownership.

## Recommended Workflow

1. Inspect the audio path and duration with local tools such as `afinfo`.
2. Transcribe with the best available local ASR, commonly `faster-whisper`.
3. Use the faster speaker path:
   - If the content is clearly single-speaker口播, do only a quick sampled speaker check or skip full diarization when evidence is strong.
   - If sampled speaker detection suggests multiple speakers, run full speaker embedding/diarization.
   - Full diarization is only worth the time for likely multi-speaker recordings.
4. Clean obvious ASR errors using context.
5. Generate:
   - `<basename>_逐字稿.txt`
   - `<basename>_AI优化稿.txt`
   - `<basename>_转录结果.html`
6. Verify the copied text does not begin with version headers and that single-speaker outputs have no `A：` label.

## Speed Strategy

- Cache models and intermediate artifacts in the workspace when processing multiple recordings.
- Use `small` ASR model for quick drafts unless the user asks for maximum accuracy or the audio is difficult.
- For long audio:
  - Save transcript JSON incrementally.
  - Skip full speaker diarization for obvious single-speaker recordings.
  - Use sampled speaker embeddings first; run full embeddings only if the smaller cluster is meaningful and separation is strong.
- Good conservative rule: if sampled 2-speaker clustering creates one tiny cluster or a weak score, treat as single speaker.

## HTML Copy Page

Use `scripts/make_copy_page.py` when useful. It creates a simple two-column page with:

- page title
- transcript textarea
- optimized稿 textarea
- copy buttons for each version

The textareas should contain only the copyable body text, with no internal `逐字稿` / `AI优化稿` heading.

## Common Corrections

Apply only when context supports it:

- `Web Coding`, `外部扣垫`, `外部可以` -> `Vibe Coding`
- `射线` -> `设限`
- `继续学习` -> `机器学习`
- `生的学习` -> `深度学习`
- `提琴`, `提醒` -> `提亲`
- `彩底` -> `彩礼`
- `减力` in job-search context -> `简历`

Keep a small local replacement map per audio instead of making risky global corrections.
