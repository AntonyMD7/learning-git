# Exercise 01 — Your First Safe Branch

**Goal:** make one small change, inspect it, commit it, and publish the branch without touching `main` directly.

## 1. Confirm your starting point

```bash
git status
git branch --show-current
```

Expected: Git identifies the current branch and shows whether the working tree is clean.

## 2. Create a practice branch

```bash
git switch -c practice/first-note
```

Verify:

```bash
git branch --show-current
```

Expected:

```text
practice/first-note
```

## 3. Create a harmless practice file

```bash
printf "One thing I learned about Git today.\n" > what-i-learned.md
```

Now inspect rather than immediately committing:

```bash
git status
git diff -- what-i-learned.md
```

## 4. Stage deliberately

```bash
git add what-i-learned.md
git diff --staged
```

You should see only the file/change you intended to include.

## 5. Commit

```bash
git commit -m "practice: add first learning note"
```

Inspect the result:

```bash
git status
git log --oneline --decorate -3
```

## 6. Publish the branch

```bash
git push -u origin practice/first-note
```

Open a pull request on GitHub. Before merging, use the **Files changed** tab and confirm that only `what-i-learned.md` is present.

## Recovery drills

Do these only in a disposable practice clone.

### Unstage without deleting your edit

```bash
git restore --staged what-i-learned.md
```

### Discard an unstaged practice edit

```bash
git restore what-i-learned.md
```

Do not practice `git reset --hard` or force-push on important repositories.

## Evidence of completion

You can consider this exercise complete when you can show:

- the practice branch name;
- a clean `git status` after the commit;
- the commit in `git log --oneline`;
- the branch on GitHub;
- a pull request whose diff contains only the intended practice file.

The purpose of the evidence is not bureaucracy: it proves you understand what changed and where it went.
