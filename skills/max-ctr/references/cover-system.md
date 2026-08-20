# Cover System

## 1. Intent and source hierarchy

Choose the truth model before making a cover.

### Source-footage mode

1. Source video frames are the truth for faces, clothing, body shape, action, and architecture.
2. User screenshots identify a shot range and desired composition.
3. Generated drafts are layout proposals, not replacement photography.

Discard any generated layer that changes facial structure, skin texture, gaze, teeth, glasses, or hairline.

### Generated-editorial mode

1. The approved brief defines the destination, story cue, protagonist, tone, and target ratio.
2. The copy manifest defines the exact visible title and emphasis.
3. An approved cover becomes the visual truth for later ratio adaptations.

Do not infer that a destination/seeding account is based on the creator's biography. Use the creator's location, school, or persona only when the brief makes it relevant.

## 2. Title contract

Maintain two independent title roles:

| Field | Job | Typical behavior |
| --- | --- | --- |
| `cover_title` | Win the click | Short, emotional, curiosity-led; may omit location if the visual is unmistakable |
| `publish_title` | Win search and recommendation | Includes the exact destination/topic and communicates the content payoff |

For every cover, record:

- exact `cover_title` characters and punctuation;
- approved line breaks;
- accent words and colors;
- `publish_title` and searchable destination;
- platform, ratio, and dimensions.

Never use a publish title as the visible cover title merely because it is present in the same row. A cover can be visually correct while its publish metadata is wrong, or vice versa; validate both separately.

When a content system uses Chinese field names, map by role rather than column position:

| Conceptual role | Common field labels | Acceptance rule |
| --- | --- | --- |
| `cover_title` | 封面标题、画面标题 | Must match the text rendered inside the approved cover |
| `publish_title` | 文案标题、发布标题 | Must contain required search terms such as the destination |
| `ai_reference` | AI 参考图、草稿图 | May preserve exploration, but must not drive active gallery/voting covers |
| `final_cover` | 最终封面、定稿图 | The only active visual source for downstream surfaces |

## 3. Precise frame and subject selection

For footage, search roughly ±1 second around a screenshot; widen only when movement or a cut requires it. Extract at 8–12 fps for the first pass, then inspect the strongest moment frame-by-frame.

Score candidates in this order:

1. Eyes open and gaze intentional.
2. Face sharpness and low motion blur.
3. Natural mouth shape and expression.
4. Clean subject separation and no awkward crop at joints.
5. Room for the title inside the intended crop.
6. Recognizable destination/story cue and useful color contrast.

For multiple people, reject both a perfect foreground face with a visibly weak second face and a crop that cannot preserve both identities.

For generated editorial covers, use the brief-specified protagonist. Maintain continuity when a series requires it, but do not let persona consistency overpower destination recognition or the story hook.

## 4. Two-layer safe-zone model

Treat every cross-platform cover as two layers:

- **Master / bleed layer:** preserves the full composition and absorbs platform cropping.
- **Crop / core layer:** contains the title, faces, essential hands/props, and recognizable story cue.

### Landscape

- Master: 16:9, typically 1920×1080.
- Centered 4:3 crop at full height: 1440×1080.
- Default side bleed: 240 px on each side.
- Default core bounds: `x=240…1680`, `y=0…1080`.

The crop may be biased left or right to preserve a subject. Review the actual bias rather than assuming a centered crop.

### Portrait

- Master: 9:16, typically 1080×1920.
- Centered 3:4 crop at full width: 1080×1440.
- Default top/bottom bleed: 240 px each.
- Default core bounds: `x=0…1080`, `y=240…1680`.

If the deliverable is already 1080×1440, it is a native 3:4 cover. Do not add artificial margins or treat it as an incidental crop.

## 5. Cover families

### Single-frame 16:9 or 4:3

Use one strong scene with an immediate human reaction or destination cue. Create variants by changing the narrative angle, not by randomly moving the same title:

1. Character-led: expression dominates; title supports the reaction.
2. Scene-led: architecture or destination reads immediately; title occupies negative space.
3. Story-led: image contains a question, contradiction, before/after, or payoff cue.

### Native single-frame 3:4

Design for the feed thumbnail from the start:

- keep the headline readable at small size;
- use the upper half for the primary read, while respecting platform UI occlusion;
- let the person and destination cue share the frame rather than forcing everything into the center;
- preserve approved art direction when converting from landscape, using crop bias, recomposition, or background extension;
- avoid a landscape image pasted into a portrait canvas.

### Three-strip 3:4

Use three edge-to-edge bands with no white gutters. Build rhythm between intimacy, context, and payoff. Keep the primary title in the middle band; supporting top/bottom copy stays lighter and less dominant.

Useful sequences include direct gaze → action → destination reveal, or detail → human reaction → wide scene.

## 6. Typography adaptation

When typography is approved, preserve:

- font family and weight;
- italic angle and width proportions;
- color assignment, outline, and shadow language;
- headline/subheadline hierarchy.

Adapt only:

- x/y position;
- line break and alignment;
- scale within the established hierarchy;
- overlap order with the subject;
- perspective placement when it follows architecture;
- background extension or crop bias required by a new ratio.

Never horizontally compress a typeface. Let a head overlap a non-critical glyph edge to create depth, but never cover eyes or an essential expression.

## 7. CTR validation

Review at both feed-thumbnail size and 100%:

1. First read: can the hook be understood in under one second?
2. Second read: is the destination, contradiction, or payoff legible?
3. Human read: is the expression crisp, natural, and relevant?
4. Copy read: does visible text match the exact `cover_title` character-for-character?
5. Crop read: do faces, title keywords, and story cues survive likely crops?
6. Series read: does this belong to the account without making every topic about the creator?

OCR can flag discrepancies but cannot replace visual inspection, especially for stylized Chinese text, punctuation, line breaks, or highlighted characters.

## 8. Final-asset and backfill QA

Use separate states for `draft`, `ai_reference`, and `final_cover`. A version suffix or familiar filename is not proof that an attachment contains the approved image.

When backfilling a gallery, voting table, or publishing system:

1. Upload the approved final visual to `final_cover`.
2. Point downstream lookups and card covers to `final_cover`, not `ai_reference`.
3. Treat attachment upload as append-by-default until proven otherwise.
4. With authorization, remove or archive stale attachments after the new final upload succeeds.
5. Read the record back and confirm exactly which attachment is active.
6. Download or preview the stored image and compare its visible text with the copy manifest.
7. Verify gallery, voting, and publishing surfaces independently.

When a downstream system copies the file and creates a new attachment token, compare the visual or content hash rather than requiring the token to match.

Do not report success after checking only metadata. The pixels visible to the user are the acceptance surface.

## 9. Delivery contract

For an exploratory request, deliver the requested materially different variants. Once a variant is approved, stop expanding the solution and package:

- final cover(s) in requested ratios;
- matching clean frames when available;
- safe-zone previews for cross-platform masters;
- a manifest with filename, final/draft status, exact cover title, publish title, destination, ratio, dimensions, source timestamp(s) or generation brief, content hash when available, and crop bias.

Final checks:

- faces are clean and sharp;
- visible title exactly matches the approved cover title;
- publish title contains required search terms;
- no title keyword crosses the crop boundary;
- no font is squeezed or silently replaced;
- no unintended white gaps or margins appear;
- overlays and platform labels are not baked into finals;
- no stale draft is presented as the active final;
- filenames distinguish master, crop, clean frame, check preview, draft, and final.
