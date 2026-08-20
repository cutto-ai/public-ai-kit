---
name: max-ctr
description: "Maximize click-through rate for video and social covers built from source footage, approved screenshots, or generated editorial visuals. Separate click-driving cover titles from searchable publish titles; protect real identities; design native 16:9, 4:3, and 3:4 covers; preserve approved typography during reflow; and verify the actual final image across galleries, voting tables, and publishing records. Use for high-CTR covers, CTR optimization, 视频封面、逐帧选封面、封面标题/文案标题、AI 生图封面、城市种草、小红书 3:4、横竖版适配、三帧竖排、多平台安全区、封面回填、版本验收或封面批量方案。"
---

# Max CTR

Turn footage or an approved visual brief into a high-CTR, publish-ready cover system. Treat the rendered pixels—not filenames, prompts, or attachment tokens—as the final truth.

## Read First

Read [references/cover-system.md](references/cover-system.md) before selecting frames, generating visuals, laying out text, or backfilling a content system. It defines title roles, visual-truth modes, safe zones, cover families, and final-asset QA.

Use the bundled overlays only for cross-platform crop checks:

- `assets/landscape-16x9-to-4x3-safe-zone-overlay.svg`
- `assets/portrait-9x16-to-3x4-safe-zone-overlay.svg`

## Workflow

### 1. Lock the brief and title contract

Confirm the account objective, audience, destination/topic, seasonal hook, protagonist, target platform, and required ratio. Do not infer that the account is autobiographical or make the creator's city/persona the default unless the brief says so.

Create an exact copy manifest before rendering:

- `cover_title`: short curiosity hook optimized for the click;
- `publish_title`: search/recommendation title optimized for platform discovery;
- `destination`: exact searchable city, school, landmark, or region;
- `line_breaks`, `accent_words`, and punctuation for the cover;
- `ratio` and final pixel dimensions.

For destination or seeding accounts, put the exact destination in `publish_title`. The cover may omit it when the image already communicates place and a shorter hook is stronger. Never swap `cover_title` and `publish_title`, and never silently rewrite approved cover copy.

### 2. Lock the visual truth

Choose one mode and keep its truth boundary explicit:

- **Source-footage mode:** treat screenshots as time-range clues. Locate the shot, run `scripts/extract-frame-window.sh`, compare adjacent frames at 80–150 ms intervals, and record the chosen timestamp. Preserve real faces, clothing, body shape, and architecture from the frame.
- **Generated-editorial mode:** treat the approved art direction, destination cues, protagonist specification, and exact cover-title manifest as truth. Generate or extend the scene as needed, but inspect geographic cues and rendered text. Do not turn a generic travel/seeding account into a personal biography.
- **Approved-cover reflow:** when the user approves the design and asks only for another ratio, preserve the subject, scene, type system, colors, and exact title. Recompose or extend background only as required by the new canvas.

Never rebuild a usable real face with image generation. If identity changes, return to the source frame or approved portrait layer.

### 3. Build the requested cover families

Produce families before polishing isolated variants:

- **Single-frame landscape:** use a 16:9 master with a validated 4:3 crop, or design a native 4:3 cover when that is the actual deliverable.
- **Single-frame portrait:** design natively at 3:4 for feed-first platforms such as Xiaohongshu. Reflow the approved composition; do not merely squeeze or center-crop a landscape cover.
- **Three-strip portrait:** stack three horizontal frames edge-to-edge in 3:4. Use the middle band for the primary title and keep supporting copy subordinate.

Keep approved font family, weight, italic angle, outline/shadow language, and color assignment unchanged. Solve fit with position, line breaks, scale within the established hierarchy, subject overlap, crop bias, or background extension—not font distortion.

### 4. Validate the actual image

Inspect every candidate at thumbnail size and at 100%:

1. Compare visible text character-for-character with `cover_title`, including punctuation, line breaks, and highlighted words.
2. Confirm the destination/story cue, protagonist expression, and title hierarchy survive the intended crop.
3. Confirm ratio and pixel dimensions.
4. Use OCR only as an aid; visual inspection of the pixels is mandatory.
5. Reject stale copy, mixed versions, malformed faces, ambiguous geography, or a technically correct filename containing the wrong picture.

Do not report a cover as correct based only on its filename, version suffix, record value, or file token.

### 5. Backfill and verify downstream surfaces

Treat one explicitly named `final_cover` asset as the source of truth. Keep drafts and AI references separate from final delivery.

When writing to a content system:

1. Map `cover_title`, `publish_title`, and `final_cover` to separate fields.
2. Make galleries, voting views, and publishing records reference `final_cover`, not a draft/AI-reference field.
3. Remember that attachment uploads may append. After a successful upload, archive or remove stale attachments only when authorized, then read the record back.
4. Download or visually inspect the stored attachment and verify the rendered title—not just metadata.
5. Confirm every downstream lookup resolves to the same final visual.

When a downstream system copies an attachment and issues a new token, compare pixels or a content hash instead of requiring token equality.

### 6. Package the result

Before approval, provide materially different variants only when exploration is requested. After approval, stop generating variants and package the approved system:

- final covers with ratio/version names;
- matching clean frames when available;
- crop-check previews for cross-platform masters;
- a manifest containing exact cover title, publish title, filename, ratio, dimensions, source timestamp(s) or generation brief, content hash when available, and final status.

Keep earlier drafts clearly labeled as drafts; never let them appear as the active final cover.

## Non-negotiables

- Preserve real identities from source assets.
- Never swap click-oriented cover copy with search-oriented publish copy.
- Validate the text visible inside the image, not just the surrounding record fields.
- Do not distort typography to force it into a safe zone.
- Do not treat a safe zone as a reason to shrink everything toward the center.
- Do not cover eyes or an essential expression.
- When only relocation or ratio adaptation is requested, change only layout-required properties.
- Distinguish masters, crops, clean frames, drafts, and finals in filenames and records.
- Do not call the task complete until the final asset and every requested downstream surface are visually consistent.
