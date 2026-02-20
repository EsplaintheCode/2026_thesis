# 2026_thesis

Data Science & Statistics Thesis written with [Quarto](https://quarto.org).

## Project Structure

```
2026_thesis/
├── data/
│   ├── raw/                        # Raw, unprocessed data files
│   └── clean/                      # Cleaned and processed data files
├── graphs/                         # Generated graphs and visualisations
├── notebooks/
│   ├── exploratory_analysis/       # EDA scripts and notebooks
│   └── feature_engineering/        # Feature engineering scripts and notebooks
├── chapters/
│   ├── exploratory_analysis.qmd    # EDA chapter
│   ├── feature_engineering.qmd     # Feature engineering chapter
│   └── results.qmd                 # Results and discussion chapter
├── docs/                           # Rendered Quarto output (generated)
├── _quarto.yml                     # Quarto project configuration
├── index.qmd                       # Thesis title page / preface
└── references.bib                  # Bibliography
```

## Getting Started

1. Install [Quarto](https://quarto.org/docs/get-started/).
2. Place raw data files in `data/raw/`.
3. Add analysis scripts to `notebooks/exploratory_analysis/` and `notebooks/feature_engineering/`.
4. Edit the chapter `.qmd` files in `chapters/` to write up your thesis.
5. Render the thesis with:

```bash
quarto render
```

The rendered output will be placed in `docs/`.
