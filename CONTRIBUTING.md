# Contributing to Project Quiver

General Arrow contribution guidelines live in the
[Contributing Guide](https://www.arrowair.com/docs/contributing/intro) on the
Arrow website. This page covers the practical, repo-specific parts.

## Getting the repository

The repository carries large STEP and flight-log files; a shallow clone is
much faster and is all you need for development:

```sh
git clone --depth 1 https://github.com/Arrow-air/project-quiver.git
```

## Working on the CAD assembly

The mechanical design is a [build123d](https://github.com/gumyr/build123d)
Python package in [`src/quiver/`](src/quiver/) (see its README for the BOM
structure). Requires Python 3.10+:

```sh
python -m venv .venv && source .venv/bin/activate
pip install -e "./src[dev]" -c src/constraints.txt

python -m quiver.assembly            # export the full drone as STEP
python -m quiver.assembly --show     # open in the ocp-vscode 3D viewer
python -m pytest src/tests/          # run the assembly smoke tests
```

CI builds the assembly and runs these tests on every pull request that
touches `src/`. If a deliberate design change shifts the assembly's
bounding box or part count, update the baselines in
`src/tests/test_assembly.py` in the same commit.

Adding a vendor STEP file? Run it through
`src/tools/simplify_step.py` **before** the first commit — committed
files stay in git history forever, so bloat cannot be removed later.

## Designing attachments

The drone has three quick-release payload interfaces (bottom, left,
right). Start by copying the template package at
[`src/quiver/attachments/designs/example_plate/`](src/quiver/attachments/designs/example_plate/)
and see the
[attachment requirements](task-grant-bounty/equipment/attachment/0002-detailed_attachment_requirement_for_bounty/information-note.md).

## Electronics and manufacturing

- KiCad sources for the four custom boards: [`src/pcb/`](src/pcb/)
- Fabrication notes and file conventions: [`src/manufacturing/`](src/manufacturing/)
- 3D-print part list: [`src/printing/`](src/printing/)

## Conventions

- Commits follow [Conventional Commits](https://www.conventionalcommits.org)
  (`feat:`, `fix:`, `docs:`, ...) — enforced by commitlint in CI.
- Formatting and spelling are checked by `make test` (requires Docker);
  `make help` lists the individual checks.
- Files marked "DO NOT EDIT" (Makefile, `.make/`, `sanity_checks.yml`, lint
  configs) are provisioned by Terraform from
  [Arrow-air/tf-github](https://github.com/Arrow-air/tf-github) — change them
  there, not here.

## Questions

Join the [Arrow Discord](https://discord.gg/arrow) — engineering call notes
are on the [wiki](https://github.com/Arrow-air/project-quiver/wiki).
