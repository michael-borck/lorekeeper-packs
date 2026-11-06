# Lorekeeper pack store policy

Status: first-party and reviewed packs. This repo is the submission queue.

## Scope

A pack is a small, self-contained course with lessons and optional compiled Ink
stories. It is not a replacement for a full unit, an LMS course or assessed
material.

## What a pack may contain

- original or properly licensed text, images and Ink stories
- exercises whose tests run in the Lorekeeper sandbox
- a complete manifest with id, title, version, author and licence

## What a pack must not contain

- personal data, student work, marks, exam answers or staff-only material
- malware, remote scripts, trackers or network calls from exercise tests
- copied material without permission
- content that is discriminatory, harassing or unsafe for the intended audience

## Safety model

- Every published pack is signed with the Lorekeeper Ed25519 key.
- `lorekeeper verify-store` checks every pack hash and signature before deploy.
- Exercise tests run in a sandboxed iframe with a nonce CSP.
- The sandbox cannot reach the parent page, local storage or the network.
- The learner chooses to add a pack; nothing installs automatically.

## Review

1. CI validates the pack shape, size, stories and metadata.
2. A human reviews rights, privacy, accuracy, accessibility and tone.
3. The exercises are run in the sandbox.
4. The pack is signed and published through the store build.
5. The reviewer, date and version are recorded.

## Key handling

The private signing key is never in this repository or in CI logs. Public keys
live in the Lorekeeper player. Rotation and compromise procedure is documented
in the engine repository. If a key is compromised, remove it from the trusted
list, re-sign every pack and publish a new player build.

## Corrections and takedown

A pack can be removed from the catalogue by deleting its entry and pack file,
rebuilding the store and redeploying. Installed local copies are not remotely
deleted. Corrections ship as a new version.
