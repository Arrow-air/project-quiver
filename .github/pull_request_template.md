<!-- Conventional-commit style title, e.g. "feat: add lidar mount attachment" -->

## What & why

## Checklist

- [ ] CAD changes: `python -m pytest src/tests/` passes (update baselines in
      `src/tests/test_assembly.py` if the design deliberately changed)
- [ ] New vendor STEP files were run through `src/tools/simplify_step.py`
      before committing
- [ ] Docs/links updated where paths changed
