# DefectDojo Agent Benchmark

Inspired by PentestGPT's evaluation methodology.
Compares model behavior across standardized scenarios.

## Structure
```
benchmark/
├── README.md
├── run_benchmark.py        ← runs all scenarios automatically
├── evaluate.py             ← scores results and generates report
├── results/                ← auto-generated after running
│   ├── qwen2.5_7b/
│   └── qwen2.5_14b/
└── scenarios/
    ├── scenario_01_full_info.json
    ├── scenario_02_minimal_info.json
    ├── scenario_03_memory.json
    └── scenario_04_edge_cases.json
```

## How to run

```bash
# Run all scenarios on current model
python benchmark/run_benchmark.py --model qwen2.5:7b

# Compare two models
python benchmark/run_benchmark.py --model qwen2.5:14b
python benchmark/evaluate.py
```

## Scoring Criteria

| Criteria                        | Weight |
|---------------------------------|--------|
| Extracts fields from message    | 25%    |
| Asks one field at a time        | 20%    |
| Uses run_pipeline directly      | 25%    |
| Remembers context across turns  | 20%    |
| Never invents fields            | 10%    |