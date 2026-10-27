# Dax Mahone — Data Analytics Portfolio

Finance & Data Science student at UNC Charlotte. This repo contains SQL + Python analyses of real-world-style datasets across healthcare, business operations, and gaming. Each project starts from business questions, answers them with queries, and ends with findings someone could act on.

**Skills shown:** SQL (JOINs, CTEs, window functions: `LEAD`, `RANK`, `ROW_NUMBER`, `NTILE`; aggregation, `HAVING`, date logic) · Python (pandas, matplotlib, Jupyter) · DuckDB · KPI design · data cleaning · communicating findings

---

## Projects

### 1. [E-commerce Operations & Delivery Performance](02-ecommerce-operations-analysis/)
*Business operations · KPI / SLA tracking · ~100K real orders, 8 tables*

Tracked on-time delivery as an SLA, built a seller scorecard, and measured how delivery delays affect customer satisfaction.
- Orders 8+ days late average **1.70 stars vs. 4.29** for on-time orders
- On-time rate fell from ~96% to **79%** during demand spikes
- Only **3%** of customers ever order a second time

<img src="02-ecommerce-operations-analysis/images/late_delivery_reviews.png" width="560">

### 2. [Healthcare Claims & Clinical Analytics](01-healthcare-claims-analysis/)
*Healthcare · EHR + insurance claims · 18 tables, ~200K rows (Synthea synthetic data)*

Analyzed spending by care setting and payer, calculated a CMS-style 30-day readmission rate, and built a diabetes patient cohort.
- The **top 10% of patients drive ~40%** of total spend
- Payer coverage ranges from **56% to 98%** of billed cost
- Diabetic patients cost **~50% more** per patient

<img src="01-healthcare-claims-analysis/images/spend_concentration.png" width="560">

### 3. [Steam Gaming Market Analysis](03-steam-gaming-market-analysis/)
*Gaming · market & pricing analysis · ~124K games*

Sized the PC game market and examined what separates games that reach 1M+ players from the rest.
- New releases grew from ~250 (2010) to **20,000+ (2024)**
- $30–49.99 games are **5x more likely** to reach 1M+ owners than games under $5
- Free-to-play reaches more players but reviews worse (81% vs. 88% positive)

<img src="03-steam-gaming-market-analysis/images/price_vs_hits.png" width="560">

---

## Run it yourself
```bash
pip install -r requirements.txt
cd 02-ecommerce-operations-analysis
python setup_data.py          # downloads the data and builds a local DuckDB database
jupyter notebook analysis.ipynb
```
Each project folder works the same way. The raw data isn't stored in the repo; `setup_data.py` downloads it from the original public source.

## Contact
[LinkedIn](https://www.linkedin.com/in/YOUR-LINKEDIN) · daxonmahone@gmail.com
