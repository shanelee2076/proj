# 📊 Product Analysis Dashboard

A Streamlit dashboard that analyzes product-level sales data to surface:

- 🏆 **Best-Selling Categories** — ranked by units sold or revenue
- 💰 **Most Profitable Products** — top N products by profit
- 📉 **Loss-Making Products** — products currently sold at a loss

Includes sample data out of the box, plus the ability to upload your own CSV.

---

## 1. Project structure

```
product-analysis-dashboard/
├── app.py                     # Main Streamlit app
├── generate_sample_data.py    # Script that creates the sample dataset
├── data/
│   └── sample_sales_data.csv  # Sample product sales data
├── requirements.txt           # Python dependencies
├── .gitignore
└── README.md
```

## 2. Run it locally

```bash
# 1. Clone your repo (after you've pushed it to GitHub)
git clone https://github.com/<your-username>/product-analysis-dashboard.git
cd product-analysis-dashboard

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## 3. Push this project to GitHub

```bash
cd product-analysis-dashboard
git init
git add .
git commit -m "Initial commit: Product Analysis Dashboard"
git branch -M main
git remote add origin https://github.com/<your-username>/product-analysis-dashboard.git
git push -u origin main
```

## 4. Deploy on Streamlit Community Cloud (free)

1. Go to **https://share.streamlit.io** and sign in with GitHub.
2. Click **"New app"**.
3. Select:
   - **Repository:** `<your-username>/product-analysis-dashboard`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **Deploy**. Streamlit will install `requirements.txt` and launch the app.
5. You'll get a public URL like:
   `https://<your-username>-product-analysis-dashboard.streamlit.app`

Any future `git push` to `main` will auto-redeploy the app.

## 5. Using your own data

Instead of the bundled sample data, use the sidebar to **"Upload my own CSV"**.
Your CSV should ideally contain these columns:

| Column          | Required | Notes                                      |
|-----------------|----------|---------------------------------------------|
| Product_Name    | Yes      | Name of the product                        |
| Category        | Yes      | Product category                           |
| Units_Sold      | Yes      | Number of units sold                       |
| Cost_Price      | Yes      | Cost price per unit                        |
| Selling_Price   | Yes      | Selling price per unit                     |
| Revenue         | Optional | Auto-computed as `Selling_Price × Units_Sold` if missing |
| Total_Cost      | Optional | Auto-computed as `Cost_Price × Units_Sold` if missing |
| Profit          | Optional | Auto-computed as `Revenue − Total_Cost` if missing |

## 6. Regenerating the sample dataset

```bash
python generate_sample_data.py
```

This overwrites `data/sample_sales_data.csv` with a new randomized dataset
(deliberately includes some loss-making products for demo purposes).

---

### Tech stack
- [Streamlit](https://streamlit.io/) — UI & app framework
- [Pandas](https://pandas.pydata.org/) — data wrangling
- [Plotly](https://plotly.com/python/) — interactive charts
