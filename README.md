README - SOP_GA_PSO

# SOP_GA_PSO

[![Build](https://github.com/CellaIoana/SOP_GA_PSO/actions/workflows/build.yml/badge.svg)](https://github.com/CellaIoana/SOP_GA_PSO/actions/workflows/build.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Issues](https://img.shields.io/github/issues/CellaIoana/SOP_GA_PSO)](https://github.com/CellaIoana/SOP_GA_PSO/issues)
[![Last Commit](https://img.shields.io/github/last-commit/CellaIoana/SOP_GA_PSO)](https://github.com/CellaIoana/SOP_GA_PSO/commits/main)
[![Repo Size](https://img.shields.io/github/repo-size/CellaIoana/SOP_GA_PSO)](https://github.com/CellaIoana/SOP_GA_PSO)

> Solving the **Sequential Ordering Problem (SOP)** with **Genetic Algorithm (GA)** and **Particle Swarm Optimization (PSO)**.  
> Includes a clean parser for **TSPLIB-SOP** files and side‑by‑side comparisons on **ESC07**, **ESC25**, and **ESC78**.

---

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Results (ESC07/ESC25/ESC78)](#results-esc07-esc25-esc78)
- [Reproducibility Notes](#reproducibility-notes)
- [Author](#author)
- [Cite & Acknowledgments](#cite--acknowledgments)
- [License](#license)

## Overview

This project implements and compares two metaheuristics for SOP:
- **GA on cost matrix** with order crossover (OX), tournament selection, swap mutation, and elitism
- **PSO in permutation space** using swap‑sequence velocities: inertia, cognitive and social components

A lightweight **TSPLIB-SOP parser** loads:
- node count (`DIMENSION`)
- cost matrix (`EDGE_WEIGHT_SECTION`)
- precedence constraints (`PRECEDENCE_SECTION`)

## Project Structure

```
.
├─ comparare.py           # GA vs PSO comparison and plots
├─ genetic_algorithm.py   # GA version on graph (toy)
├─ pso_algorithm.py       # PSO version on graph (toy)
├─ genetic_matrix.py      # GA on cost matrix (TSPLIB-scale)
├─ pso_matrix.py          # PSO on cost matrix (TSPLIB-scale)
├─ instance_parser.py     # TSPLIB-SOP parser
├─ sop_instances/         # ESC07.sop, ESC25.sop, ESC78.sop
├─ requirements.txt
├─ LICENSE
└─ .github/workflows/build.yml
```

## Installation

```bash
# 1) (optional, recommended) create venv
python -m venv .venv

# Windows
.\.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

# 2) install deps
pip install -r requirements.txt
```

## How to Run

### A) Quick local toy instance
```bash
python comparare.py
```
This runs GA & PSO on a small in‑code graph and shows the comparative fitness plot.

### B) TSPLIB‑SOP instances (ESC07/ESC25/ESC78)
Ensure the `.sop` files are in `sop_instances/` and run:
```bash
python comparare.py
```
You'll get:
- a plot per instance (GA vs PSO fitness over generations)
- best cost found by each algorithm in console output

## Results (ESC07/ESC25/ESC78)

Fill with your final numbers after running `comparare.py`.

| Instance | GA — Best Cost | PSO — Best Cost | Notes |
|---|---:|---:|---|
| ESC07 | -3 | -3 | both reach optimum on small instance |
| ESC25 | … | … | fill after run |
| ESC78 | … | … | fill after run |

**Example plot (ESC07):**  
Add a screenshot to `assets/` and embed it:  
`![ESC07](assets/esc07_plot.png)`

## Reproducibility Notes

- For stable runs, set a seed at the top of `comparare.py`:
  ```python
  import random; random.seed(42)
  ```
- Suggested starting params for larger instances:
  - GA: `population_size=100`, `generations=300`
  - PSO: `num_particles=100`, `generations=300`, `w=0.4`, `c1=1.5`, `c2=1.5`
- Infeasible permutations (precedence violated) receive `inf` cost.

## Author

**Cella Ioana** — [github.com/CellaIoana](https://github.com/CellaIoana)

## Cite & Acknowledgments

- TSPLIB95 — SOP instances (ESC07/25/78), Heidelberg University.

**BibTeX:**
```bibtex
@misc{SOP_GA_PSO,
  author       = {Cella Ioana},
  title        = {SOP\_GA\_PSO: Genetic Algorithm vs Particle Swarm Optimization for the Sequential Ordering Problem},
  year         = {2025},
  howpublished = {\url{https://github.com/CellaIoana/SOP_GA_PSO}}
}
```

## License

This project is released under the **MIT License** — see **[LICENSE](LICENSE)**.
