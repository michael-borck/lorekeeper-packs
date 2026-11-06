# Lorekeeper packs

Submissions for the [Lorekeeper](https://lorekeeper.borck.education/) pack store.

This repo is the public review queue. A merged submission is not live
immediately: the maintainer reviews it, signs the pack with the Lorekeeper key,
rebuilds the catalogue and deploys it to the store.

## Submit a pack

1. Build a pack with the engine:

   ```bash
   python3 -m lorekeeper pack <course> --out path/to/pack.json
   ```

2. Create a folder under `submissions/<pack-id>/` containing:

   ```text
   submissions/<pack-id>/pack.json
   submissions/<pack-id>/submission.json
   ```

3. Fill in `submission.json` (see `templates/submission.json`).

4. Run the validator:

   ```bash
   python3 scripts/validate_pack.py
   ```

5. Open a pull request. CI runs the same validator.

## What happens next

- The maintainer checks the pack against the [store policy](POLICY.md).
- The pack is signed with the private Lorekeeper key and added to the static
  catalogue.
- The live catalogue is rebuilt and deployed separately. A merged PR is not a
  live pack until that deploy completes.
- Corrections ship as a new pack version.

## Pack format

A pack is one or more courses plus their compiled Ink stories. See
[`POLICY.md`](POLICY.md) and the example under `submissions/pocket-incidents/`.

## Safety

Exercise tests run in a sandboxed iframe with no parent access, no local storage
and no network. Packs are signed before publication. The sandbox is a safety
layer, not a substitute for review.

## Licence

Each pack declares its own licence in `submission.json` and in the pack
manifest. You must have the right to publish the content.
