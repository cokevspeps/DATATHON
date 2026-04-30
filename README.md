# Datathon 2026 — The Gridbreakers

## Cấu trúc thư mục

```
DATATHON/
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
│   ├── sales.csv
│   ├── sample_submission.csv
│   ├── shipments.csv
│   └── web_traffic.csv
│
├── notebooks/
│   ├── 00_mcq.ipynb          # MCQ
│   ├── 01_eda.ipynb          # EDA & Visualization
│   ├── 02_forecasting.ipynb  # Sales Forecasting
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
