# Datathon 2026 — The Gridbreakers

## Cấu trúc thư mục

```
datathon2026/
├── data/
│   ├── customers.csv
│   ├── geography.csv
│   ├── inventory.csv
│   ├── order_items.csv
│   ├── orders.csv
│   ├── payments.csv
│   ├── products.csv
│   ├── promotions.csv
│   ├── returns.csv
│   ├── reviews.csv
│   ├── sales.csv             # Train: 2012-07-04 → 2022-12-31
│   ├── sample_submission.csv # Test: 2023-01-01 → 2024-07-01
│   ├── shipments.csv
│   └── web_traffic.csv
│
├── notebooks/
│   ├── 00_mcq.ipynb          # MCQ
│   ├── 01_eda.ipynb          # EDA & Visualization
│   ├── 02_forecasting.ipynb  # Sales Forecasting Model
│   └── baseline.ipynb
│
├── outputs/
│   └── submission.csv
│
├── reports/
│
├── README.md
│
└── requirements.txt
```

## Hướng dẫn chạy

```bash

pip install -r requirements.txt

jupyter notebook notebooks/00_mcq.ipynb
jupyter notebook notebooks/01_eda.ipynb
jupyter notebook notebooks/02_forecasting.ipynb
```

## Nộp bài

- **Kaggle**: https://www.kaggle.com/competitions/datathon-2026-round-1
- **File nộp**: `outputs/submission.csv` (548 dòng, đúng thứ tự `sample_submission.csv`)
- **Report**: NeurIPS template, tối đa 4 trang, đặt trong `reports/`
