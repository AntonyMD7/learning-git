# Start Here

Welcome. This repository is a **practice lab**, not a test. You are expected to make small changes, inspect them, commit them on a branch, and learn how to recover safely.

## Before you begin

You need Git and a GitHub account. You do **not** need to know command-line Git already.

Use a disposable clone or fork for practice. Never paste passwords, API keys, private keys, `.env` contents, medical/private records, or other confidential data into this repository.

## Your first 10 minutes

1. Clone the repository.
2. Run `git status`.
3. Read the **mental model** in `README.md`.
4. Create a practice branch:

   ```bash
   git switch -c practice/my-first-branch
   ```

5. Verify the branch:

   ```bash
   git branch --show-current
   git status
   ```

6. Continue with `exercises/01-first-branch.md`.

## Stop conditions

Stop and inspect before continuing if:

- Git says you have a merge conflict;
- you are on `main` when you expected a practice branch;
- `git status` shows files you did not intend to change;
- a command contains `--force`, `reset --hard`, or deletes files/history;
- GitHub asks you to publish information that should remain private.

## Three views

**Beginner:** follow the numbered exercise and use the explanation under each command.

**Intermediate:** inspect `git status`, `git diff`, and `git log` before/after every exercise.

**Engineer:** review the repository history, CI checks, branch graph, and exact object IDs to understand how the same actions are represented internally.

## Finished the first exercise?

Return to the README and continue through the remaining labs. The goal is not memorizing commands; it is learning a workflow where you can always answer:

- What branch am I on?
- What changed?
- What is staged?
- What will the next command do?
- Can I recover if I am wrong?
