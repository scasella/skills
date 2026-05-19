---
name: modal
description: >
  Alias for `modal-router`. Use when the user says `$modal`, mentions Modal
  work broadly, or asks for GPU, sandbox, training, fine-tuning, CUDA
  validation, isolated execution, or remote compute through Modal. Immediately
  load and follow `modal-router`, then use the child skill selected by that
  router.
metadata:
  short-description: Route $modal to $modal-router
---

# Modal Alias

`$modal` routes to `$modal-router`.

When this skill activates:

1. Load `/Users/scasella/.codex/skills/modal/SKILL.md` (`modal-router`).
2. Follow the Modal Router primitive-selection table.
3. Load only the referenced child skill needed for the chosen primitive:
   `modal-basic-skills`, `modal-gpu`, `modal-gpu-dev`, or
   `modal-gpu-experiment`.
4. Do not launch Modal work from this alias alone.
