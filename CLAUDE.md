# CLAUDE.md

Standing rules for this project (file organizer; see problem.md for requirements).

- Python 3, standard library only. No new dependencies without asking.
- Requirements live in problem.md (R1–R6); spec.md maps each to the implementation. Update spec.md whenever behavior changes.
- Never modify or delete a user's original files — copy only (R5).
- Every requirement needs a test in test_organizer.py, named `test_rN_*`. All tests must pass before committing.
- Run tests: `python -m unittest -v`
- Errors go to stderr with a helpful message and a nonzero exit code; no tracebacks for expected failures.
- Commit in small, focused steps with clear messages.
