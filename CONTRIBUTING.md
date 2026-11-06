# Contributing a pack

## Before you start

- Read [POLICY.md](POLICY.md).
- Use content you own or have permission to publish.
- Keep the pack small: text courses and compiled Ink stories, no student data.
- Do not include a private API key, personal contact details or student work.

## Build

From the Lorekeeper engine:

```bash
python3 -m lorekeeper pack <course> --out /tmp/<pack-id>/pack.json
```

If you are starting from an existing course, check that the course slug in the
pack is unique. The validator rejects collisions with other submissions.

## Submission files

```text
submissions/<pack-id>/
  pack.json
  submission.json
```

`submission.json`:

```json
{
  "packId": "my-pack",
  "title": "My Pack",
  "author": "Your name",
  "contact": "you@example.com",
  "licence": "CC BY 4.0",
  "version": "1.0.0",
  "description": "One or two sentences.",
  "changes": "What is in this version.",
  "status": "submitted"
}
```

## Validate

```bash
python3 scripts/validate_pack.py
```

## Pull request

Use the pull request template, include a short reviewer note, and say whether
this is a new pack or a new version.
