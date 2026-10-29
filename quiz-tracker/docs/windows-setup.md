# Windows and GitHub workflow

## Existing directory and inspection

Use PowerShell in the existing folder:

```powershell
Set-Location 'C:\Users\MRKni\OneDrive\ares-tracking-system'
Get-ChildItem -Force
git status
git remote -v
git branch --show-current
git log --oneline -5
```

Read root control/handoff documents and `quiz-tracker/AGENTS.md`/`STATUS.md` before changes. Verify origin is `https://github.com/markknit/ares-tracking-system.git` (or its equivalent SSH URL). Never initialize a replacement repository, reset existing work, or overwrite local files.

At bootstrap this folder was empty, not a checkout, and cloning failed because Git could not reach GitHub. Foundation documents were prepared locally afterward. To recover, clone the existing remote into a separate empty staging folder once connectivity works, inspect it, and compare its content against these documents before copying `quiz-tracker/` into that checkout. Do not clone over this now-populated folder. Reconcile the final working-folder location explicitly before continuing.

Recovery completed on 2026-10-28: the staging clone contained only the original LICENSE. Its Git metadata and LICENSE were moved into the original requested folder after inspection, with all 11 foundation files verified unchanged during transfer. The working checkout remains `C:\Users\MRKni\OneDrive\ares-tracking-system` on `main`. The recovery procedure above is historical; do not repeat it for this established checkout.

## Normal update and review (verified checkout only)

```powershell
git fetch origin
git status --short --branch
git log --oneline origin/main..HEAD
git log --oneline HEAD..origin/main
git pull --ff-only
```

Pull only after reviewing local modifications and divergence; do not discard work to make it succeed. Stage explicit project paths and review before committing:

```powershell
git add -- quiz-tracker
git diff --cached --check
git diff --cached
git commit -m 'docs(quiz): initialize two-track quiz system'
git log -1 --format=fuller
git status --short --branch
```

The foundation must remain local until the remote is verified and the commit reviewed. Once push is authorized, verify origin again, fetch, inspect divergence, and use `git push origin main` for the reviewed foundation commit. Never force-push.

## Separate worktrees after foundation review

Create these from a verified checkout after its foundation commit is available. Prefer active worktrees outside OneDrive:

```powershell
New-Item -ItemType Directory -Force 'C:\Users\MRKni\source\ares-worktrees'
git worktree add -b quiz/track-a 'C:\Users\MRKni\source\ares-worktrees\quiz-track-a' main
git worktree add -b quiz/track-b 'C:\Users\MRKni\source\ares-worktrees\quiz-track-b' main
git worktree list
```

Use one Codex session per worktree with that directory as cwd. Each session reads project rules/status and verifies branch before edits. Do not run two sessions against the same working tree. Respect path ownership; coordinate shared-contract edits and review them with both tracks.

## Review and merge

From the integration checkout, inspect `git diff main...quiz/track-a` and `git log main..quiz/track-a`, run that milestone's checks, and confirm gates. Merge reviewed work with `git merge --no-ff quiz/track-a`; repeat for Track B only after its separate review. If conflicts occur, inspect and reconcile deliberately, then rerun applicable checks. Record approvals and outcomes in status/decision documents. Push reviewed commits only when authorized.

OneDrive synchronization is not Git coordination or backup verification. Do not edit a synchronized checkout simultaneously on different computers. Let synchronization settle before changing machines; inspect Git state on arrival. Worktrees share the primary checkout's Git metadata, so retaining it under OneDrive still exposes metadata to synchronization: never run concurrent Git operations across synchronized replicas. For sustained Android work, consider a reviewed move of the full clone outside OneDrive as well. Exclude build outputs from commits when build tooling is introduced. Do not move/delete a registered worktree manually.
