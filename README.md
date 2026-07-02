# Cookie Cats A/B Test: Does the Level Gate Placement Affect Retention?

## Business Question

Cookie Cats is a mobile puzzle game where players hit a "gate" that forces a
short wait (or in-app purchase) to continue. This test compares moving that
gate from **level 30** to **level 40**, and asks: does delaying the gate
change how many players come back the next day, and a week later?

This matters because gate placement is a trade-off. Move it later, and
players get more uninterrupted early-game momentum — but the studio also
delays the point where friction (and monetization) kicks in. The wrong
choice either bleeds players early or leaves revenue on the table.

## Data

- **Source:** [Mobile Games A/B Testing — Cookie Cats](https://www.kaggle.com/datasets/mursideyarkin/mobile-games-ab-testing-cookie-cats) (Kaggle)
- **Unit of randomization:** individual player (`userid`)
- **Groups:** `gate_30` (control) vs `gate_40` (treatment)
- **Sample size:** 90,189 players total
- **Metrics:**
  - `sum_gamerounds` — total rounds played in the first 14 days
  - `retention_1` — returned 1 day after install (bool)
  - `retention_7` — returned 7 days after install (bool)

## Method

1. **Sample Ratio Mismatch (SRM) check** — confirmed the control/treatment
   split matches the expected ~50/50 randomization before trusting any
   downstream result (chi-square goodness-of-fit test).
2. **Power analysis** — since this data was already collected, power was
   assessed retroactively: given the actual sample size per group and the
   observed baseline rate, what's the smallest effect this test could
   reliably have detected?
3. **Retention analysis** — two-proportion z-tests on `retention_1` and
   `retention_7`, with 95% confidence intervals on the difference, not just
   p-values.
4. **Engagement analysis** — `sum_gamerounds` is heavily right-skewed (one
   extreme outlier present), so the mean was compared using bootstrap
   confidence intervals and cross-checked with a Mann-Whitney U test rather
   than relying on a t-test alone.
5. **Effect sizes** reported alongside significance (Cohen's d for the
   continuous metric, relative lift for the proportions) — statistical
   significance alone doesn't tell you if an effect is big enough to act on.

## Results

> Fill in after running `notebook.ipynb` — keep the structure, replace the
> placeholders.

**Sample Ratio Mismatch check:** [PASS/FAIL] — χ² = X.XX, p = X.XX
(expected ~50/50 split; observed control n = XX,XXX / treatment n = XX,XXX)

**Power analysis:** With n ≈ XX,XXX per group and a baseline retention_1
rate of XX.X%, this test had 80% power to detect an absolute difference of
at least X.X percentage points.

| Metric                | Control (gate_30) | Treatment (gate_40) | Abs. difference | 95% CI     | p-value | Significant? |
| --------------------- | ----------------- | ------------------- | --------------- | ---------- | ------- | ------------ |
| retention_1           | XX.X%             | XX.X%               | X.X pp          | [X.X, X.X] | 0.XXX   | Yes/No       |
| retention_7           | XX.X%             | XX.X%               | X.X pp          | [X.X, X.X] | 0.XXX   | Yes/No       |
| sum_gamerounds (mean) | XX.X              | XX.X                | X.X             | [X.X, X.X] | 0.XXX   | Yes/No       |

![Retention by group](figures/retention_comparison.png)

## Recommendation

> One paragraph, plain English, no hedging where the data doesn't call for
> it. State which gate to ship and why, referencing both statistical and
> practical significance (e.g. "retention_7 was significantly higher under
> gate_30, and the effect size — while small — was consistent across both
> retention windows, so I'd recommend keeping the gate at level 30 rather
> than moving it to 40").

## Limitations

- This is an **observational retrospective** on a completed test, not a
  live experiment — power analysis here checks whether the sample size
  achieved was sufficient, not whether the test was designed with a target
  MDE in mind up front.
- `sum_gamerounds` has extreme outliers (one player logged an
  implausibly high round count); results are reported both with and
  without this point removed to show it doesn't change the conclusion.
- No segmentation by platform, geography, or install cohort — an
  aggregate effect can mask heterogeneous effects in subgroups.
- Retention is measured as a binary same-day/week flag, not
  session depth or long-term LTV, so this doesn't speak to monetization
  impact directly.

## Repo Structure

```
ab-test-analysis/
├── README.md
├── notebook.ipynb
├── data/
├── src/
│   ├── power_analysis.py
│   └── stats_tests.py
├── requirements.txt
└── figures/
```

## Running This

```bash
pip install -r requirements.txt
jupyter notebook notebook.ipynb
```
