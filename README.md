# FWM Simulator

Rb double-lambda Four-Wave Mixing (FWM) simulator.

## Overview

This project provides tools for simulating and analyzing Four-Wave Mixing phenomena in Rubidium atoms using a double-lambda configuration.

## Installation

Install the project and its dependencies using Poetry:

```bash
poetry install
```

## Usage

The simulator provides a command-line interface with several subcommands:

### Help

```bash
fwm-sim --help
```

### Simulate

Run a Four-Wave Mixing simulation:

```bash
fwm-sim simulate --config config.json --output results/
```

### Plot

Visualize simulation results:

```bash
fwm-sim plot --input results/output.h5 --plot-type interactive
```

### Export

Export simulation results to various formats:

```bash
fwm-sim export --input results/output.h5 --output data.csv --format csv
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

Format code with Black:

```bash
black src/ tests/
```

### Linting

Lint code with Ruff:

```bash
ruff check src/ tests/
```

## Project Structure

```
.
├── src/
│   └── fwm_sim/          # Main package
│       ├── __init__.py
│       └── cli.py        # Command-line interface
├── tests/                # Test suite
│   ├── __init__.py
│   └── test_basic.py
├── pyproject.toml        # Project configuration
└── README.md
```

## License

TBD

## Contributors

FWM Sim Team
