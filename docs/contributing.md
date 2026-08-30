# Contributing

Documentation changes should be proposed through a focused branch or pull request. Explain the user problem, identify the affected API or workflow, and keep examples free of secrets and real customer data.

## Content changes

Use Markdown under `docs/`, update `smartgen.yml` when adding or renaming a page, and keep navigation labels concise. Prefer a short explanatory paragraph followed by a table or example where that improves clarity.

## API changes

When a Worker route changes, update the endpoint inventory, request and response examples, error behavior, data model, and changelog together. Confirm that examples use placeholders and that the documented authorization matches the implementation.

## Validation

Run:

```bash
smartgen-docs build
```

Then review the generated site for broken links, missing assets, incorrect code fences, and mobile navigation problems. The repository workflow performs a clean build before deployment.

## Review expectations

A reviewer should check factual alignment with the current Worker, secret hygiene, security language, and whether a proposed workflow accidentally turns a review-first operation into an automatic data mutation. Keep changes reversible and document migration or rotation steps when configuration names change.
