import json
import re

notebook_path = 'd:/code/DATATHON/notebooks/02_forecasting.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] != 'code':
        continue
    source = ''.join(cell['source'])
    
    # 1. Add imports
    if 'import lightgbm as lgb' in source and 'from prophet import Prophet' not in source:
        new_imports = """
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from prophet import Prophet
"""
        source = source.replace('import lightgbm as lgb', 'import lightgbm as lgb\n' + new_imports)
        
    # 2. train_and_evaluate
    if 'def train_and_evaluate(df_train, target, feature_cols, n_splits=5):' in source:
        source = """class EnsembleForecaster:
    def __init__(self, target, feature_cols, date_col='Date', n_splits=5, seed=42):
        self.target = target
        self.feature_cols = feature_cols
        self.date_col = date_col
        self.n_splits = n_splits
        self.seed = seed
        
        self.lgb_base = lgb.LGBMRegressor(
            objective='regression', metric='mae',
            num_leaves=127, learning_rate=0.05,
            feature_fraction=0.8, bagging_fraction=0.8, bagging_freq=5,
            min_child_samples=20, reg_alpha=0.1, reg_lambda=0.1,
            n_estimators=1000, random_state=self.seed, verbose=-1
        )
        
        self.lgb_quant = lgb.LGBMRegressor(
            objective='quantile', alpha=0.5, metric='mae',
            num_leaves=127, learning_rate=0.05,
            feature_fraction=0.8, bagging_fraction=0.8, bagging_freq=5,
            min_child_samples=20, reg_alpha=0.1, reg_lambda=0.1,
            n_estimators=1000, random_state=self.seed, verbose=-1
        )
        
        self.ridge = Pipeline([
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler()),
            ('model', Ridge(alpha=1.0, random_state=self.seed))
        ])
        
        self.prophet_model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)

    def fit(self, df_train, df_val=None):
        X_tr = df_train[self.feature_cols].values
        y_tr = df_train[self.target].values
        
        print(f"Training {self.target} Ensemble...")
        if df_val is not None:
            X_val = df_val[self.feature_cols].values
            y_val = df_val[self.target].values
            self.lgb_base.fit(X_tr, y_tr, eval_set=[(X_val, y_val)], callbacks=[lgb.early_stopping(50, verbose=False), lgb.log_evaluation(-1)])
            self.lgb_quant.fit(X_tr, y_tr, eval_set=[(X_val, y_val)], callbacks=[lgb.early_stopping(50, verbose=False), lgb.log_evaluation(-1)])
        else:
            self.lgb_base.fit(X_tr, y_tr, callbacks=[lgb.log_evaluation(-1)])
            self.lgb_quant.fit(X_tr, y_tr, callbacks=[lgb.log_evaluation(-1)])
            
        self.ridge.fit(X_tr, y_tr)
        
        prophet_df = pd.DataFrame({
            'ds': df_train[self.date_col],
            'y': df_train[self.target]
        })
        import logging
        logger = logging.getLogger('cmdstanpy')
        logger.addHandler(logging.NullHandler())
        logger.propagate = False
        logger.setLevel(logging.CRITICAL)
        self.prophet_model.fit(prophet_df)
        print(f"Finished training {self.target} Ensemble.")
        
    def predict(self, df_test):
        X_te = df_test[self.feature_cols].values
        
        p_lgb = self.lgb_base.predict(X_te)
        p_quant = self.lgb_quant.predict(X_te)
        p_ridge = self.ridge.predict(X_te)
        
        prophet_test = pd.DataFrame({'ds': df_test[self.date_col].values})
        p_prophet = self.prophet_model.predict(prophet_test)['yhat'].values
        
        return (p_lgb + p_quant + p_ridge + p_prophet) / 4.0

def train_and_evaluate(df_train, target, feature_cols, n_splits=5):
    model = EnsembleForecaster(target, feature_cols, n_splits=n_splits)
    model.fit(df_train)
    return model, {}"""

    # 3. OOT val
    if 'val_rev_pred  = rev_model.predict(df_val[FEATURE_COLS])' in source:
        source = source.replace('val_rev_pred  = rev_model.predict(df_val[FEATURE_COLS])', 'val_rev_pred  = rev_model.predict(df_val)')
        source = source.replace('val_cogs_pred = cogs_model.predict(df_val[FEATURE_COLS])', 'val_cogs_pred = cogs_model.predict(df_val)')
        
    # 4. SHAP
    if 'explainer   = shap.TreeExplainer(rev_model)' in source:
        source = source.replace('explainer   = shap.TreeExplainer(rev_model)', 'explainer   = shap.TreeExplainer(rev_model.lgb_base)')
        
    # 5. Retrain final model
    if 'lgb_params_final =' in source and 'final_rev_model  = lgb.LGBMRegressor' in source:
        source = re.sub(
            r'lgb_params_final = \{.*?print\(\'Final models trained on full history \(2013 → 2022\)\.\'\)',
            "final_rev_model = EnsembleForecaster('Revenue', FEATURE_COLS)\nfinal_cogs_model = EnsembleForecaster('COGS', FEATURE_COLS)\n\nfinal_rev_model.fit(full_train_clean)\nfinal_cogs_model.fit(full_train_clean)\nprint('Final models trained on full history (2013 → 2022).')",
            source,
            flags=re.DOTALL
        )
        
    # 6. Predict recursive
    if 'X_row = pd.DataFrame([feat])[FEATURE_COLS]' in source:
        source = source.replace('X_row = pd.DataFrame([feat])[FEATURE_COLS]', "feat['Date'] = row['Date']\n    X_row = pd.DataFrame([feat])")

    lines = source.split('\n')
    cell['source'] = [line + '\n' for line in lines[:-1]] + [lines[-1]] if lines else []

with open('d:/code/DATATHON/notebooks/02_forecasting.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook updated successfully.")
