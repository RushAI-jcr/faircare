# FairCareAI Release Checklist

Use this checklist before publishing a tagged release to ensure package quality, reproducibility, and governance artifacts are ready.

## 1) Versioning and Metadata

- [ ] Update version in `pyproject.toml`
- [ ] Update version in `CITATION.cff` (if changed)
- [ ] Update `CHANGELOG.md` with release notes
- [ ] Confirm repository URLs in metadata are correct

## 2) Local Quality Gates

```bash
python -m pip install -e ".[all]"
python -m playwright install chromium
python -m ruff check .
python -m mypy src
python -m pytest
```

- [ ] Lint passes
- [ ] Type checks pass
- [ ] Test suite passes

## 3) End-to-End Artifact Verification

Run a synthetic-data workflow and verify all outputs:

- [ ] Data scientist HTML report
- [ ] Governance HTML report
- [ ] Data scientist PDF report
- [ ] Governance PDF report
- [ ] Governance PPTX deck
- [ ] PNG bundle export (`.zip`)
- [ ] CHAI model card XML export
- [ ] CHAI model card JSON export
- [ ] RAIC Checkpoint 1 checklist JSON export
- [ ] Reproducibility bundle JSON export

## 4) Visual Quality Gate

For generated HTML/PNG/PPTX artifacts:

- [ ] No text overlap
- [ ] No clipping at chart/table boundaries
- [ ] Readable minimum font sizes (>=12px chart text, >=12pt slides)
- [ ] No blank/failed image exports

## 5) Packaging and Publishing Readiness

```bash
uv build
uv pip install twine
uv run twine check dist/*
```

- [ ] Build succeeds for sdist and wheel
- [ ] `twine check` passes

## 6) Tag and Publish

- [ ] Create annotated release tag (e.g., `v0.2.0`)
- [ ] Push branch + tag
- [ ] Publish GitHub Release notes
- [ ] Verify CI + publish workflow completion

## 7) Post-Release Validation

- [ ] Install from PyPI in clean environment
- [ ] Run smoke audit and generate one report
- [ ] Confirm docs links and badges resolve
- [ ] Announce release notes to users
