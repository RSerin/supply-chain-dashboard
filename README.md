[readme.md](https://github.com/user-attachments/files/28490082/readme.md)
# supply-chain-dashboard
Supply chain key performance indicator (KPI) dashboard tracking revenue, regional delivery statuses, shipping delays, and category-level supplier risks across 180K global order records. Made by R. Serin.
My Supply Chain Data Project
By: R. Serin
Tools Used: Python, Excel, Power BI, and an emulation of SAP

 What is this project?
I wanted to see what it's actually like to handle a massive corporate data dump, so I built an end-to-end data project using a global supply chain dataset with over **180,000 rows** of order records. 

My goal was to take this raw data, clean it up using code (python), emulate it as an export from a SAP system, and build a dashboard that a manager could actually use to fix shipping problems.

---

 What I Did (STEPS):

 Step 1: Clean the Data with Python
The raw data was way too big and messy to drop straight into Excel, so I used **Python** to do the heavy lifting. I wrote a script called `analyze.py` that cleaned up missing information, fixed date formats, and broke the massive file down into smaller, clean summary sheets (like category and regional breakdowns).

 Step 2: Set up the SAP Simulation in Excel
To make this look like a real corporate environment, I brought the data into Excel and built a sheet that mimics a real **SAP inventory report (MM60)**. 
 I renamed the column headers to match actual SAP database terms, like using **Material Group** for categories and **WRBTR USD** for local currency revenue.
 I built a Pivot Table to calculate the average late-delivery risk for each product group.
 I added conditional formatting so that any product category with a late-delivery rate higher than **50%** automatically highlights in bright red.

 Step 3: Build the Power BI Dashboard
Finally, I pulled the clean files into Power BI to make an interactive dashboard for leadership. I built 5 main visuals:
1. KPI Cards: Show at a glance that the overall average shipping delay is 0.57 days.
2. Sales by Category: A bar chart proving that "Fishing" gear is the biggest money maker (hitting nearly $7M).
3. Delay Timeline: A line chart showing a massive spike where shipping times crashed and burned in 2018.
4. Regional Breakdown: A stacked bar chart separating on-time vs. late shipments for every global territory.
5.*Supplier Risk Matrix: A simple table summarizing exactly which categories are the riskiest to keep in stock.

---

 Summary:
After looking at the finished dashboard, I found some massive problems in this supply chain:
 The Shipping Crisis: A staggering 54.83% of all global orders are arriving late. That means more than half of the business's shipments are failing.
 The 2018 Bottleneck: Shipping delays suddenly spiked worse than ever in 2018, which means something went seriously wrong in the warehouses that year.
 The Financial Risk: Because "Fishing" makes up almost $7 million of total sales, fixing the shipping issues in that specific category needs to be priority number one.

---

 How to Check Out My Work:
1. Run python analyze.py in your terminal to see the data processing script run.
2. Open SAP_Inventory_Report.xlsx in Excel to see the red-highlighted Pivot Tables.
3. Open the Power BI file to click around the active dashboard layout.
