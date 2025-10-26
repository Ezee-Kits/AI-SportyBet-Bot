# ⚡ SportyBet AutoTrader — Full AI Betting Automation for Mobile (Termux + Pyppeteer)

## 🧠 Overview
**SportyBet AutoTrader** is a **complete Python automation system** that automatically:
- Scrapes football matches from **SportyBet**
- Matches predictions from **six professional tipster sites**
- Calculates **value bets** using **Kelly Criterion**
- Automatically **places bets** on SportyBet  
All of this runs **completely on mobile** using **Termux** — no laptop or desktop needed!

This project was developed by **Ezee Kits**, and I’ve made a **detailed step-by-step video tutorial** on my **[YouTube Channel (Ezee Kits)](https://www.youtube.com/@Ezee_Kits)** explaining:
- How to install Python and required libraries on Termux  
- How to set up SportyBet automation  
- How to make it run safely and efficiently on any Android device  

---

## 🎯 What It Does
The bot automates your SportyBet workflow by combining:
1. **Data extraction** from prediction sites:
   - Forebet  
   - Statarea  
   - Betclan  
   - FootballSuperTips  
   - AccumulatorTips  
   - Prematips  
2. **Probability matching** using fuzzy similarity (difflib)
3. **Value detection** using a custom formula from `Main_Calc.py`
4. **Kelly Criterion-based bet sizing**
5. **Automatic bet placement** on SportyBet via **Pyppeteer**
6. **CSV logging** of all daily data and bets placed

This is not a scraper — it’s a **self-learning, data-driven, full-stack betting automation system** that works 24/7.

---

## ⚙️ Setup (Termux Installation Guide)
Follow these steps carefully — everything runs directly on **Android**.

### 📱 Step 1: Install Termux
Download and install **Termux** from F-Droid or GitHub (avoid Play Store version).

### 📦 Step 2: Install Python and Core Tools
Run the following commands:
```bash
pkg update && pkg upgrade -y
pkg install python git -y
```

### 🧩 Step 3: Install Required Libraries
```bash
pip install pyppeteer pandas numpy asyncio
```

If `pyppeteer` fails, try:
```bash
pip install pyppeteer==2.0.0
```

### ⚡ Step 4: Install Chromium for Termux
```bash
pkg install chromium -y
```

---

## 🧮 Step 5: Clone the Project
```bash
git clone https://github.com/yourusername/SportyBet-AutoTrader.git
cd SportyBet-AutoTrader
```

---

## 🔐 Step 6: Login to SportyBet
Before running, make sure:
- You are **logged in to your SportyBet account** on the cloned Chrome profile.
- You have an **active bankroll** and have tested manual betting once.

---

## ▶️ Step 7: Run the Script
```bash
python GAMING.py
```

The script will open **SportyBet** in Chromium and prompt:
```
PRESS ENTER AFTER LOGGING IN AND SETTING UP THE PAGE TO AUTOMATE...
```
After pressing Enter, it will start scanning matches and automatically:
- Match games with prediction data
- Calculate value edges
- Place bets when criteria are met

---

## 💸 Output Example
Example terminal output when automation runs:

```
CURRENTLY ON SPORTY NUMBER >>>> 5 ON 3
2025-10-19 16:00 Arsenal vs Chelsea
==================== MATCHED DATA ======================
HOME EDGE : 12.45 %  @ 1.85 WITH ACCU : 58 %
PLACED BET ON >>>>> (HOME EDGE : 12.45 %  @ 1.85 WITH ACCU : 58 % )

OVER 2.5 EDGE : 14.9 %  @ 2.10 WITH ACCU : 61 %
PLACED BET ON >>>>> (OVER 2.5 EDGE : 14.9 %  @ 2.10 WITH ACCU : 61 % )
```

CSV files like `Data.csv` will be saved automatically in:
```
/storage/emulated/0/CSV FILES/YYYY-MM-DD Files/
```

---

## ⚗️ How It Works (Step-by-Step)

1. **Collects predictions** from 6 different data sources  
2. **Compares home and away team names** using fuzzy similarity (≥57%)  
3. **Finds overlapping match data** across multiple prediction websites  
4. **Applies Kelly Criterion formula** to calculate optimal bet size  
5. **Uses Pyppeteer** to open SportyBet and navigate through live games  
6. **Automatically clicks odds, places bets, and confirms** via simulated mouse actions  
7. **Logs every bet** for future analysis  

---

## 🧠 Value Betting + Kelly Criterion
The Kelly Criterion formula determines the percentage of bankroll to wager:

```
Kelly % = (bp - q) / b
```

Where:
- `b` = decimal odds - 1  
- `p` = win probability  
- `q` = 1 - p  

The script calculates the **edge** and **optimal stake** automatically, making it behave like a professional quantitative bettor.

---

## 🔍 Example Use Case

**Scenario:**
You want to bet automatically every weekend on SportyBet using AI-driven odds and predictions.

**Bot will:**
- Load all matches
- Compare 6 sources
- Find high-confidence picks (e.g., Over 2.5, Home Win)
- Place bets automatically if **Edge ≥ 10%** and **Accuracy ≥ 55–60%**

This works great for:
- Daily betting strategies  
- Data-backed bankroll management  
- Automated testing of prediction models  

---

## ⚙️ Tech Stack
| Component | Description |
|------------|--------------|
| **Language** | Python 3.10+ |
| **Automation Engine** | Pyppeteer |
| **Environment** | Termux (Android) |
| **Browser** | Chromium |
| **Data Processing** | Pandas, NumPy |
| **String Matching** | difflib |
| **Math Calculation** | Kelly Criterion (`Main_Calc.py`) |
| **File Storage** | CSV auto-logging |
| **Libraries Used** | asyncio, os, pandas, numpy, difflib, datetime |

---

## 📱 Mobile Advantage
Unlike typical PC automation setups, **SportyBet AutoTrader** runs completely on **Android**.  
This means you can:
- Run 24/7 automated bets on your phone  
- Save power and bandwidth  
- Carry your AI betting system anywhere  

---

## 📊 Output Data Example (CSV)
```
DATE,TIME,HOME TEAM,AWAY TEAM,MARKET,ODDS,EDGE(%),STAKE(₦)
2025-10-19,15:00,Arsenal,Chelsea,HOME WIN,1.85,12.4,10
2025-10-19,17:30,Barcelona,Sevilla,OVER 2.5,2.10,14.9,15
```

---

## 🎥 Full Video Tutorial
I’ve made a **complete walkthrough video** showing:
- How to install and configure everything on Termux  
- How to set up SportyBet for automation  
- How to safely manage bankroll and logs  

👉 **Watch it on YouTube:** [Ezee Kits Channel](https://www.youtube.com/@Ezee_Kits)  
Don’t forget to **Subscribe, Like, and Comment** ❤️

---

## 👨‍💻 Author
**Ezee Kits (Peter)**  
🎓 Electrical and Electronics Engineer | 🇳🇬 Nigeria  
💡 Passionate about Automation, AI, and Data Science  
📧 **Email:** ezeekits@gmail.com  
📺 **YouTube:** [Ezee Kits](https://www.youtube.com/@Ezee_Kits)

---

## 📜 License
**MIT License**

This project is free and open-source for educational and research purposes.  
You may modify or distribute it with proper credit to the author.


**GitHub Short Description (SEO Optimized):**
> Full SportyBet automation system for Android (Termux) using Pyppeteer. Automatically finds value bets, applies Kelly Criterion, and places bets in real-time. Fully explained on Ezee Kits YouTube channel.

