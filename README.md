# Learning Git — A Practical Beginner Lab

A small, hands-on repository for learning Git and GitHub by doing the work yourself: creating commits, branching safely, resolving mistakes, and opening pull requests.

## Who this is for

This lab is aimed at people who are new to Git or who have used GitHub mainly through a web interface and want a clearer mental model of what happens locally and remotely.

## What you will learn

By the end of the lab you should be able to:

- explain the difference between Git and GitHub;
- clone a repository and inspect its state;
- create and switch branches;
- stage and commit changes deliberately;
- compare local and remote history;
- push a branch without changing `main` directly;
- open and review a pull request;
- recover from common mistakes without deleting work.

## The mental model

Think of the workflow as four layers:

1. **Working tree** — files you are editing now.
2. **Staging area** — the exact changes selected for the next commit.
3. **Local repository** — commits stored on your computer.
4. **Remote repository** — the shared GitHub copy, usually named `origin`.

A normal safe workflow is:

```text
edit -> git status -> git add -> git commit -> git push -> pull request
```

## Lab 1 — Clone and inspect

```bash
git clone https://github.com/AntonyMD7/learning-git.git
cd learning-git
git status
git remote -v
git log --oneline --decorate -5
```

Before changing anything, get into the habit of running `git status`.

## Lab 2 — Create a branch

```bash
git switch -c practice/first-change
```

Verify where you are:

```bash
git branch --show-current
git status
```

Avoid doing practice work directly on `main`.

## Lab 3 — Make a commit

Create a small file:

```bash
printf "My first Git practice note.\n" > practice-note.txt
```

Inspect the change:

```bash
git status
git diff
```

Stage and commit it:

```bash
git add practice-note.txt
git diff --staged
git commit -m "practice: add first Git note"
```

A useful habit is to inspect both the unstaged and staged diff before committing.

## Lab 4 — Push safely

```bash
git push -u origin practice/first-change
```

The `-u` records the upstream branch so future `git push` and `git pull` commands know which remote branch belongs to your local branch.

Then open a pull request on GitHub instead of merging straight into `main`.

## Lab 5 — Update your branch from main

```bash
git switch main
git pull --ff-only
git switch practice/first-change
git merge main
```

`--ff-only` prevents Git from quietly creating a merge commit while you are simply updating your local `main`.

## Lab 6 — Recover from common mistakes

### You changed a file but have not staged it

Discard only that file's uncommitted changes:

```bash
git restore path/to/file
```

### You staged the wrong file

Keep the file changes but remove it from the staging area:

```bash
git restore --staged path/to/file
```

### You want to inspect an older commit

```bash
git log --oneline
git show <commit-sha>
```

Do not use `git reset --hard`, force-push, or history rewriting until you understand exactly what will be lost.

## Everyday command reference

```bash
git status                  # What changed?
git diff                    # What is unstaged?
git diff --staged           # What will be committed?
git branch --show-current   # Which branch am I on?
git log --oneline -10       # Recent history
git switch -c NAME          # Create and enter a branch
git add FILE                # Stage a specific file
git commit -m "message"     # Create a commit
git push -u origin NAME     # Publish a new branch
git fetch origin            # Refresh remote references
git pull --ff-only          # Safely update the current branch when possible
```

## Practice challenges

1. Create a branch named `practice/readme-note`.
2. Add one sentence to a new file named `what-i-learned.md`.
3. Inspect the diff before staging it.
4. Commit with a descriptive message.
5. Push the branch.
6. Open a pull request.
7. Review the Files changed tab before merging.
8. Delete the practice branch after the pull request is merged.

## Safety rules for beginners

- Check `git status` before and after important operations.
- Work on branches instead of directly on `main`.
- Commit small, understandable changes.
- Never commit passwords, API keys, private keys, `.env` files, or personal confidential data.
- Do not copy terminal commands you do not understand into an important repository.
- Prefer reversible commands while learning.

## Suggested progression

After completing this repository, move on to pull-request review, merge conflicts, tags/releases, GitHub Actions, and collaborative branch protection.

## Contributing

This repository is intended to remain beginner-friendly. Improvements should favor clear explanations, safe commands, reproducible exercises, and small pull requests.