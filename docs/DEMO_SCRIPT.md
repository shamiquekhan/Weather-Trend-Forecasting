#  2-Minute Demo Video Script & Recording Guide

## Script Outline (Exactly 2 Minutes)

Use this script to guide your screen-share demo. **Bold times** are hard checkpoints for pacing.

---

## **[0:00–0:15] OPENING (15 seconds)**

### Script:
"Hi, I'm [Your Full Name]. This is my submission for the PM Accelerator AI Engineer Internship Assessment. I've built a comprehensive weather trend forecasting project that combines multiple time-series models, spatial analysis, and interactive visualizations. Let me walk you through what's included."

### What to Show:
- Your face (quick, professional greeting)
- Briefly show your desktop/environment

**Checkpoint: 0:15** ⏱

---

## **[0:15–0:40] REPOSITORY STRUCTURE (25 seconds)**

### Script:
"Let me start by showing the GitHub repository structure. You'll see I've organized the project into modular components: data ingestion with a dedicated `src/` folder, numbered Jupyter notebooks following a logical workflow, and a reports directory with all visualizations and deliverables. The README documents everything needed to reproduce the analysis."

### What to Show:
- **Open GitHub repo** (in browser or terminal)
- **Scroll through folder structure:**
  ```
   data/ (with README)
   notebooks/ (01_cleaning, 02_eda_basic, ..., 06_unique_analyses)
   src/ (data_loader.py, eda_utils.py, models.py)
   reports/figures/ (generated plots)
   README.md (scroll down briefly to show mission statement + setup)
   requirements.txt
   dashboard.py
  ```
- **Do NOT** spend time reading line-by-line

**Checkpoint: 0:40** ⏱

---

## **[0:40–1:10] KEY VISUALIZATIONS (30 seconds)**

### Script:
"Now let me show some of the key findings from the analysis. First, here's a global temperature trend over time showing clear seasonal patterns. This choropleth map reveals average temperatures by country — notice the tropical regions in red and arctic zones in blue. This anomaly detection chart highlights unusual weather events I detected using Isolation Forest. And this correlation matrix shows relationships between temperature, humidity, wind speed, and other features."

### What to Show (in this order):
1. **Global temperature trend** (plotly interactive line chart)
   - Mouse over to show interactivity
   - 5 seconds

2. **Choropleth map** (country-level temperatures)
   - Show color gradient
   - 5 seconds

3. **Anomaly detection scatter** (with highlighted anomalies)
   - Point out red X markers
   - 5 seconds

4. **Correlation heatmap** (static image)
   - Highlight strong correlations (dark red/green)
   - 5 seconds

5. **Precipitation chart** (top cities by rainfall)
   - Brief glance
   - 5 seconds

**Keep transitions smooth — use Alt+Tab or browser tabs pre-opened**

**Checkpoint: 1:10** ⏱

---

## **[1:10–1:40] MODEL COMPARISON & RESULTS (30 seconds)**

### Script:
"I trained multiple forecasting models: ARIMA, Prophet, and XGBoost, plus an ensemble that stacks their predictions. The ensemble achieved the best performance with an MAE of 2.05°C. You can see in this comparison table that the ensemble outperforms individual models by 3–5% in RMSE. The SHAP feature importance plot shows that lag-1 and lag-7 features are the strongest predictors of temperature, which aligns with weather's autocorrelated nature."

### What to Show:
1. **Model comparison bar chart** (MAE/RMSE by model)
   - Highlight ensemble as the winner
   - 10 seconds

2. **Model metrics table**
   - Point to ensemble row (best MAE/RMSE/R²)
   - 5 seconds

3. **SHAP feature importance plot**
   - Explain top 3–4 features
   - 10 seconds

4. **Forecast plot for one city** (Prophet or ARIMA)
   - Show actual vs predicted
   - Show confidence intervals
   - 5 seconds

**Checkpoint: 1:40** ⏱

---

## **[1:40–2:00] CLOSING (20 seconds)**

### Script:
"The modular code design makes it easy to add new models or extend the analysis. The project demonstrates end-to-end machine learning from data cleaning through model ensemble and interpretation. All code includes type hints and docstrings for reproducibility. I've hosted a Dash dashboard for interactive exploration [optional: quick 5-sec demo] and documented everything in the README. The dataset is from Kaggle's Global Weather Repository, and this work aligns perfectly with PM Accelerator's mission: empowering AI professionals through real-world projects. Thanks for reviewing my submission."

### What to Show:
1. **Quick code snippet** (in VS Code or notebook)
   - Show function with type hints + docstring
   - 5 seconds

2. **Dash dashboard** (optional)
   - Show interactive dropdown + charts
   - 5 seconds

3. **README final section** (mission + author info)
   - 5 seconds

4. **Brief closing screen** (your name + thank you)
   - 5 seconds

**Checkpoint: 2:00** ⏱

---

##  Recording Setup

### Option 1: Loom (Recommended for Ease)
1. Go to [loom.com](https://loom.com)
2. Click **"Start Recording"**
3. Select **"Chrome Tab"** (to record browser) or **"Entire Screen"** (to show VS Code + browser)
4. Allow microphone access
5. Click **"Start Recording"**
6. Narrate as you follow the script above
7. Click **"Stop"** when done
8. Click **"Share"** and copy public link (anyone can view)
9. Save link to `demo/demo_link.txt` or include in README

### Option 2: OBS Studio (Free Desktop Tool)
1. Install [obsproject.com](https://obsproject.com)
2. Create a **Scene** with:
   - **Display Capture** (source: your monitor)
   - **Audio Input** (source: your microphone)
3. Click **"Start Recording"**
4. Follow script, narrate
5. Click **"Stop Recording"** when done
6. Upload MP4 to **YouTube (unlisted)** or **Google Drive**
7. Share link

### Option 3: Google Meet (Simple & Free)
1. Start a **Google Meet**
2. Click **"Start recording"** (red circle button)
3. Share screen
4. Follow script
5. Click **"Stop recording"**
6. Google Drive will receive MP4 automatically
7. Share via link

---

##  Pre-Recording Checklist

- [ ] Close all unnecessary browser tabs (only keep GitHub, visualizations, code)
- [ ] Disable notifications (macOS: Focus Mode, Windows: Focus Assist)
- [ ] Zoom to 125% or 150% (so text is readable in video)
- [ ] Test microphone (Loom: do test rec, OBS: check levels)
- [ ] Print this script and place next to monitor
- [ ] Have all visualizations/notebooks open in separate tabs before recording
- [ ] Cursor speed set to normal (not too fast)
- [ ] Fresh cup of water nearby 

---

##  Narration Tips

 **DO:**
- Speak clearly and at a natural pace (not rushed)
- Use the script as a **guide**, not a word-for-word mandate
- Show enthusiasm about the project
- Point out interesting findings ("Notice the red anomalies here...")
- Pause briefly when transitioning between visuals

 **DON'T:**
- Read the script robotically
- Go over 2 minutes (hard cutoff)
- Show/discuss sensitive info (personal credentials, keys)
- Use filler words ("um", "uh") — pause instead
- Show code for more than 3 seconds without explaining it

---

##  Editing (Optional)

If using OBS/Google Meet, you can edit in:
- **DaVinci Resolve** (free video editor)
- **CapCut** (free, easy for beginners)
- **Shotcut** (free, open-source)

Basic edits:
- Trim opening/closing silence
- Speed up file browser navigation (1.5x speed)
- Add title card with your name

---

##  Sharing the Link

After recording:

1. **Loom:**
   - Copy share link (public)
   - Paste into `demo/demo_link.txt`

2. **YouTube:**
   - Upload as **Unlisted** (not Private)
   - Copy YouTube URL
   - Share in README or submission form

3. **Google Drive:**
   - Right-click file → **Share**
   - Set to **"Anyone with link can view"**
   - Copy share link

**Test the link 24 hours before submission** to ensure it still works!

---

##  Demo Link Format

Create `demo/demo_link.txt` with:
```
 DEMO VIDEO LINK
==================

Title: Weather Trend Forecasting — PM Accelerator Assessment
Duration: 2 minutes
Recorded: [Date]
Link: https://www.loom.com/share/... (or YouTube/Drive URL)

Platform: Loom | YouTube | Google Drive
Access: Public | Anyone with link can view
```

---

##  Checklist: Post-Recording

- [ ] Video is at least 1:30 and at most 2:00
- [ ] Audio is clear (test by listening once)
- [ ] All screens are readable (no blurry text)
- [ ] Transitions between tabs are smooth
- [ ] Link is public/shareable
- [ ] Link works when tested from incognito browser
- [ ] Link is saved in repo (`demo/demo_link.txt` + README)

---

##  Going Live

**48 hours before submission deadline:**
- [ ] Record final demo video
- [ ] Test link works
- [ ] Share link in README
- [ ] Commit to GitHub
- [ ] Do a final repo review

**You're ready! **

---

**Template Created:** May 15, 2026  
**For:** PM Accelerator AI Engineer Internship Assessment
