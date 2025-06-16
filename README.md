# Project Quiver

[![GitHub Issues](https://img.shields.io/github/issues/Arrow-air/project-quiver)](https://github.com/Arrow-air/project-quiver/issues)
[![GitHub Stars](https://img.shields.io/github/stars/Arrow-air/project-quiver)](https://github.com/Arrow-air/project-quiver/stargazers)

**Project Quiver** is an open-source UAV initiative developed under the Arrow Air DAO. It aims to design and build scalable, modular drone systems for real-world utility. This repository hosts the core documentation, source code, engineering plans, and governance artifacts for the Quiver development lifecycle.

---

## 📁 Repository Structure

| Path                        | Description                                                      |
| --------------------------- | ---------------------------------------------------------------- |
| `.github/`                  | GitHub configuration files (workflows, templates, etc.)          |
| `.make/`                    | Build automation and infrastructure setup files                  |
| `docs/`                     | Project documentation, reports, and specifications               |
| `src/`                      | Source code for the project (core logic, scripts, tooling, etc.) |
| `task-grant-bounty/`        | DAO-related tasks, grants, and bounty tracking                   |
| `.commitlintrc.yml`         | Commit linting configuration                                     |
| `.cspell.config.yaml`       | Code spell-checker config                                        |
| `.cspell.project-words.txt` | Custom vocabulary list for spell-checking                        |
| `.editorconfig`             | Editor formatting guidelines                                     |
| `.gitignore`                | Git ignore rules                                                 |
| `.terraform_init`           | Terraform bootstrap or infrastructure provisioning script        |
| `Makefile`                  | Automation entrypoint for builds, tests, or provisioning         |
| `CONTRIBUTING.md`           | Guidelines for contributing to the project                       |
| `README.md`                 | You're here! Project overview and instructions                   |

---

## 🚀 Getting Started

### Prerequisites

To work with this repository, ensure you have:

* Git and Make installed
* Terraform (if provisioning infrastructure)
* Any language/toolchain dependencies required by files in `src/`

### Basic Usage

Clone the repository:

```bash
git clone https://github.com/Arrow-air/project-quiver.git
cd project-quiver
```

Run any available automation (if defined in `Makefile`):

```bash
make help
# or specific targets like:
# make setup
# make test
```

> 📌 *Note: specific Makefile targets or Terraform steps may depend on internal conventions — consult `Makefile` and `.terraform_init` directly for more.*

---

## 📄 Documentation

All project-level documentation is located in the [`docs/`](docs/) folder. Key resources may include:

* Engineering reports
* Payload specifications
* Interface definitions
* Phase planning and reviews

Refer to filenames inside that folder for phase-specific progress (e.g., `PT1-Engineering-Report.md`).

---

## 🛠 Development

Code lives in the [`src/`](src/) directory and is under active development. To contribute:

1. Read [`CONTRIBUTING.md`](CONTRIBUTING.md)
2. Create a feature or fix branch
3. Make changes following commit lint rules
4. Submit a pull request

Linting and spellchecking are supported via:

* `.commitlintrc.yml` (commit message linting)
* `.cspell.*` (spell checking configuration and dictionary)

---

## 💬 Governance

The `task-grant-bounty/` folder contains grant tracking, bounty records, and governance-related files tied to DAO or Arrow Air proposals.

This may include:

* Deliverables for funded tasks
* Contributor reward tracking
* Proposal status notes

---

## 📌 Notes

* Infrastructure or deployment components may be tied to Terraform (`.terraform_init`)
* No compiled binaries or builds are stored in this repo — it is source and spec focused
* GitHub Actions or CI logic may reside in `.github/` if workflows are configured

---

## 🤝 Contributing

We welcome contributors! To get involved:

1. Fork the repository
2. Read the [CONTRIBUTING.md](CONTRIBUTING.md)
3. Open an issue or pull request

Please ensure your contributions follow the repo's formatting, linting, and conduct guidelines.

---

## 📝 License

This project is open-source

