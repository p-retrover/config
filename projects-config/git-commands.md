# Git commands cheatsheet

1. this creates a private repo and pushes the current git repo. (make sure you have gh)

```bash
gh repo create my-cv --private --source=. --remote=origin --push
```

2. delete a repo using gh

first run this to list all repositories under your account

```bash
gh repo list
```

By default, gh does not enable repository deletion for safety. Run this command first to authorize the scope

```bash
gh auth refresh -s delete_repo
```

Choose one of the following commands depending on how you want to confirm the deletion:

- Delete with interactive confirmation. Run `gh repo delete owner/repo` (or simply `gh repo delete` if you are inside the local repository folder). You will be prompted to type the full repository name to confirm.
- Delete immediately without prompts. Pass the `--yes` flag along with the explicit repository name:

```bash
gh repo delete owner/repo --yes
```

> Note: For safety, `--yes` is ignored if you do not specify the `owner/repo` name

3. if you accidentally deleted a branch, or a bad rebase, or want to recover lost commit (```bash git reset --hard ```) it's like your undo button.

```bash
git reflog

# then to go to a particular commit
git reset --hard HEAD@{index}

# if you see an entry in the reflog, but aren't sure, take a peek
git show HEAD@{index}

# if you want one specific commit from the reflog history to be applied to current branch , rather than moving your whole history back, use cherry-pick
git cherry-pick <commit-hash>
```
