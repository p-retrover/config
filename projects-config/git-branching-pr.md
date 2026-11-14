# Git Branching & Pull Request Testing Cheat Sheet

## 1. Creating & Managing Local Branches

* **Create and switch to a new branch (modern):**
  ```bash
  git switch -c <branch-name>
  ```
* **Create and switch to a new branch (classic):**
  ```bash
  git checkout -b <branch-name>
  ```
* **Create a branch without switching to it:**
  ```bash
  git branch <branch-name>
  ```
* **Switch to an existing branch:**
  ```bash
  git switch <branch-name>
  ```
* **Create a branch from a specific starting branch or commit:**
  ```bash
  git checkout -b <new-branch> <base-branch>
  ```
* **Push a new local branch to a remote repository:**
  ```bash
  git push -u origin <branch-name>
  ```
* **Delete a local branch (force delete):**
  ```bash
  git branch -D <branch-name>
  ```

---

## 2. Checking a Single Pull Request (Without Merging into `main`)

### Using Standard Git (Works for Forks & Same-Repo PRs)
1. **Fetch the PR into a new local branch:**
   ```bash
   git fetch origin pull/<ID>/head:<local-branch-name>
   ```
   *(Note: For GitLab, use `merge-requests/<ID>/head:<local-branch-name>`)*
2. **Switch to the fetched PR branch:**
   ```bash
   git switch <local-branch-name>
   ```
3. **Clean up when finished:**
   ```bash
   git switch main
   git branch -D <local-branch-name>
   ```

### Using GitHub CLI (Fastest for GitHub)
* **Fetch and switch to the PR in one step:**
  ```bash
  gh pr checkout <ID>
  ```

### If the PR Branch is in the Same Repository
1. **Update remote branch references:**
   ```bash
   git fetch origin
   ```
2. **Switch to the PR branch:**
   ```bash
   git switch <pr-branch-name>
   ```

---

## 3. Testing Multiple Pull Requests

### Option A: Test PRs One by One
1. **Fetch each PR into its own separate branch:**
   ```bash
   git fetch origin pull/42/head:pr-42
   git fetch origin pull/43/head:pr-43
   ```
2. **Switch between them as needed:**
   ```bash
   git switch pr-42
   git switch pr-43
   ```
3. **Delete all temporary branches when done:**
   ```bash
   git switch main
   git branch -D pr-42 pr-43
   ```

### Option B: Combine Multiple PRs in a Sandbox Branch
1. **Create a temporary testing branch from `main`:**
   ```bash
   git checkout -b test-multiple-prs main
   ```
2. **Fetch the PRs locally without switching:**
   ```bash
   git fetch origin pull/42/head:pr-42
   git fetch origin pull/43/head:pr-43
   ```
3. **Merge the PR branches into your sandbox:**
   ```bash
   git merge pr-42
   git merge pr-43
   ```
4. **Abort a merge if conflicts get too messy:**
   ```bash
   git merge --abort
   ```
5. **Clean up everything when done:**
   ```bash
   git switch main
   git branch -D test-multiple-prs pr-42 pr-43
   ```

---

## 4. Troubleshooting Common Fetch Errors

### Error: `fatal: refusing to fetch into branch 'refs/heads/<branch>' checked out at ...`
Git prevents fetching into a branch that is currently active in your terminal.

* **Fix 1 — Switch off the branch before fetching:**
  ```bash
  git switch main
  git fetch origin pull/<ID>/head:<branch>
  ```
* **Fix 2 — Fetch into a different, unused branch name:**
  ```bash
  git fetch origin pull/<ID>/head:<new-branch-name>
  git switch <new-branch-name>
  ```
* **Fix 3 — Update an existing PR branch you are already on:**
  ```bash
  git pull origin pull/<ID>/head
  ```
