# DSN Mart Sales Prediction — DSN AI Bootcamp 2026 Qualification Hackathon

Predicts `total_sales` for a given product at a given store. Evaluated by RMSE (lower is better).

## Requirements

```
pandas
numpy
matplotlib
seaborn
scikit-learn
```

## Data

Place these three files in the **same folder as the notebook**:

- `train.csv`
- `test.csv`
- `sample_submission.csv`

## How to run

Run all cells top to bottom. No configuration needed — paths, model, and
hyperparameter search are all self-contained in the notebook.

**Output:** `submission.csv`, written to the same folder, ready to upload.

## Approach

1. **Clean** inconsistent category labels — casing (`Dairy`/`dairy`/`DAIRY`)
   and, for `fat_content`, abbreviation variants (`LF`, `reg`, etc.) mapped
   to their full labels.
2. **Impute missing values** — `product_weight_kg` by product-level median,
   `store_size` by store-level mode, both with a global fallback.
3. **Engineer features** — price relative to category/store/format
   averages, a cleaned shelf-visibility measure (treating `0` as missing),
   price-per-kg, and a binned store-age feature.
4. **Encode** remaining categoricals with one-hot encoding.
5. **Tune** a `RandomForestRegressor`'s regularization (`max_depth`,
   `min_samples_leaf`, `max_features`) with a grid search, validated with
   5-fold cross-validation.
6. **Train** the tuned model on the full training set and predict on test.

## Notes

- Random seed fixed at 42 throughout for reproducibility.
- Feature importances for the final model are plotted at the end of the
  notebook.
- Price/category/store aggregates are computed over train+test combined
  (not leakage of the target — those columns are known for every test row,
  it just gives more stable averages).
