README.md - SOP_GA_PSO
# SOP_GA_PSO

> Solving the Sequential Ordering Problem (SOP) using Genetic Algorithm (GA) and Particle Swarm Optimization (PSO)

This project implements and compares GA and PSO for SOP instances from TSPLIB, including ESC07, ESC25, and ESC78.

## 📁 Project Structure

- `genetic_matrix.py` – Genetic Algorithm on cost matrix
- `pso_matrix.py` – Particle Swarm Optimization on matrix
- `instance_parser.py` – Parser for .sop TSPLIB format
- `comparare.py` – Runs and compares GA vs PSO
- `sop_instances/` – Contains `.sop` test files

## 🚀 How to Run

```bash
python comparare.py
```

You’ll see a plot comparing GA vs PSO and the best costs.

## 📊 Example Output

- GA → Best cost: `-3`
- PSO → Best cost: `-3`

## 📦 Dependencies

See `requirements.txt`.

## 📄 License

MIT – see LICENSE file.
