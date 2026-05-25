#  QUICK START GUIDE

## Your Complete Weather Forecasting Project — Ready to Build

This folder contains everything you need to win the PM Accelerator AI Engineer Internship assessment. Here's how to get started **right now**.

---

##  What's Here?

| File | Purpose |
|------|---------|
| `BUILD_GUIDE.md` | ** START HERE** — Complete step-by-step implementation guide |
| `README.md` | Your GitHub repository template (copy to your repo) |
| `requirements.txt` | Python dependencies (for `pip install -r requirements.txt`) |
| `environment.yml` | Conda environment file (alternative to pip) |
| `SUBMISSION_CHECKLIST.md` | Verify everything before final submission |
| `DEMO_SCRIPT.md` | 2-minute video script + recording guide |
| `src/data_loader.py` | Production-grade data cleaning utilities |
| `src/eda_utils.py` | Reusable visualization helpers |
| **This file** | Quick orientation (you're reading it) |

---

##  5-Minute Setup

### Step 1: Create GitHub Repository
```bash
# Go to github.com → New Repository
# Name: weather-trend-forecasting
# Description: Global weather forecasting using ARIMA, Prophet, XGBoost & ensemble
# Public: 
# Initialize with README:  (you'll add your own)
```

### Step 2: Clone & Set Up Local
```bash
git clone https://github.com/YOUR_USERNAME/weather-trend-forecasting.git
cd weather-trend-forecasting

# Create folders
mkdir -p data notebooks reports/figures src demo tests

# Copy files from this guide into your repo
# (Python files go in src/, notebooks go in notebooks/, etc.)
```

### Step 3: Install Dependencies
```bash
# Option A: pip
pip install -r requirements.txt

# Option B: conda
conda env create -f environment.yml
conda activate weather-forecast
```

### Step 4: Download Dataset
```bash
# Go to: https://www.kaggle.com/datasets/nelgiriyewithana/global-weather-repository
# Download manually, or use Kaggle CLI:
pip install kaggle
# (Set up API key at ~/.kaggle/kaggle.json)
kaggle datasets download -d nelgiriyewithana/global-weather-repository --unzip -p data/
```

### Step 5: Open & Start Building
```bash
jupyter notebook
# Then open notebooks/01_data_cleaning.ipynb and follow BUILD_GUIDE.md
```

**⏱ Total time: 5 minutes. You're ready!**

---

##  Recommended Workflow

Follow these notebooks **in order**:

1. **`01_data_cleaning.ipynb`** (2 hours)
   - Load data using `src/data_loader.py`
   - Clean, preprocess, engineer features
   - Save `data/weather_cleaned.csv`

2. **`02_eda_basic.ipynb`** (1.5 hours)
   - Temperature trends, precipitation patterns
   - Correlation matrix, seasonal analysis
   - Use `src/eda_utils.py` for plotting

3. **`03_eda_advanced.ipynb`** (1 hour)
   - Anomaly detection (PyOD)
   - Visualize anomalies
   - Seasonal decomposition

4. **`04_modeling_basic.ipynb`** (2 hours)
   - Select one city (London recommended)
   - Fit ARIMA with auto_arima
   - Evaluate & plot

5. **`05_modeling_advanced.ipynb`** (3 hours)
   - Prophet model
   - XGBoost with lag features
   - Ensemble stacking
   - Model comparison table

6. **`06_unique_analyses.ipynb`** (2 hours)
   - Climate patterns (continental trends)
   - Environmental impact (AQI vs weather)
   - SHAP feature importance
   - Spatial visualizations (Folium, Choropleth)

**Total: ~11–12 hours of focused work**

---

##  Minimum Viable Submission (Basic Track)

If you're short on time, **at minimum** deliver:

 Notebooks 1–4 (data cleaning, basic EDA, ARIMA)  
 Model metrics (MAE, RMSE, R²)  
 2 visualizations (temperature trend + precipitation)  
 GitHub README  
 2-minute demo video  

**Estimated time: 6 hours**

---

##  Full Advanced Submission (Recommended)

 All notebooks (1–6)  
 3+ forecasting models + ensemble  
 5+ unique visualizations  
 SHAP feature importance  
 Spatial analysis (Folium + Choropleth)  
 Dash dashboard  
 Production code (type hints, docstrings, modular design)  

**Estimated time: 15–18 hours**

---

##  Code Template Usage

### Data Loading (from `src/data_loader.py`)
```python
from src.data_loader import load_data, clean_weather_data

df = load_data("data/GlobalWeatherRepository.csv")
df_clean = clean_weather_data(df)
df_clean.to_csv("data/weather_cleaned.csv", index=False)
```

### Visualization Helpers (from `src/eda_utils.py`)
```python
from src.eda_utils import plot_temperature_trends, plot_correlation_matrix

plot_temperature_trends(df_clean, save_path="reports/figures/temp_trends.html")
plot_correlation_matrix(df_clean, save_path="reports/figures/corr.png")
```

---

##  Before You Start

- [ ] Python 3.11+ installed (`python --version`)
- [ ] Git installed and configured (`git config --list`)
- [ ] Kaggle account created (for dataset)
- [ ] GitHub account ready (for repo)
- [ ] Text editor / IDE open (VS Code recommended)
- [ ] 15–20 hours blocked on calendar

---

##  Stuck? Here's What to Do

| Problem | Solution |
|---------|----------|
| Kaggle dataset not downloading | Manual download from browser, save to `data/` folder |
| `ModuleNotFoundError` (pandas, etc.) | Run `pip install -r requirements.txt` again |
| Notebook kernel won't start | Restart Jupyter kernel (Kernel → Restart) |
| Code running slowly | Reduce dataset size (`df.sample(10000)` for testing) |
| Visualization not showing | Add `plt.show()` or save to file |
| Prophet installation fails | Use `pip install pystan==2.19.1.1` first, then `pip install prophet` |

---

##  Demo Video Tips

- **Record after everything is built** (use DEMO_SCRIPT.md)
- **Keep it to 2 minutes exactly**
- **Use Loom** (easiest, free, shareable link)
- **Test link before submitting** (try incognito browser)

---

##  Final Submission Checklist

**One week before deadline, run through SUBMISSION_CHECKLIST.md** to verify:

- [ ] All code pushed to GitHub
- [ ] README explains setup
- [ ] Demo video link works
- [ ] `requirements.txt` is accurate
- [ ] PM Accelerator mission is mentioned
- [ ] Visualizations are saved

---

##  Key Concepts to Understand

Before diving in, make sure you're comfortable with:

- **Time-series forecasting** (ARIMA, seasonality, trend)
- **Feature engineering** (lag features, rolling statistics)
- **Train/test splits** (80/20 for time-series)
- **Model metrics** (MAE, RMSE, R², MAPE)
- **Ensemble methods** (combining predictions)
- **Anomaly detection** (statistical outliers)

**Resources:**
- [Statsmodels ARIMA Guide](https://www.statsmodels.org/stable/tsa.html)
- [Prophet Documentation](https://facebook.github.io/prophet/)
- [XGBoost Time Series](https://xgboost.readthedocs.io/)
- [SHAP Interpretability](https://shap.readthedocs.io/)

---

##  You've Got This!

This is a **sizable project**, but it's **100% doable** in 15–18 hours. The BUILD_GUIDE walks you through every step. The code templates get you started fast. And the checklist ensures nothing is missed.

**Start with Step 1 (GitHub repo), then follow the workflow above. Good luck! **

---

##  Questions?

- Check BUILD_GUIDE.md for detailed explanations
- Review SUBMISSION_CHECKLIST.md for requirements
- See DEMO_SCRIPT.md for recording guidance
- Test using code in src/ folder (working examples)

---

**Build date:** May 15, 2026  
**For:** PM Accelerator AI Engineer Internship Assessment  
**Status:** Ready to implement 
