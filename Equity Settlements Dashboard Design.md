# **Operational Intelligence in the T+1 Era: A Comprehensive Framework for US Equity Settlement Dashboards**

## **1\. Introduction: The Strategic Imperative of Settlement Visualization**

The transition of the United States equity markets to a T+1 settlement cycle on May 28, 2024, marked a watershed moment in the history of financial market infrastructure.1 This structural compression of the post-trade lifecycle has fundamentally altered the operational cadence of settlement teams across the industry. In the previous T+2 environment, operations managers operated with a comfortable "recovery buffer"—a 24-hour window where trade discrepancies, inventory shortages, and standing settlement instruction (SSI) mismatches could be identified and remediated before causing a definitive settlement failure.1 Under the T+1 regime, this buffer has effectively evaporated. The time between trade execution and the final exchange of assets has been halved, forcing firms to adopt a posture of "pre-settlement" vigilance rather than post-trade reaction.4  
For an Operations Manager overseeing a US Equity Settlements team, the Start of Day (SOD) fail report is no longer merely a retrospective administrative list of transactions that did not settle. In the current regulatory and economic climate, the SOD fail report represents a live inventory of capital at risk, regulatory exposure under SEC Rule 204, and potential reputational damage.6 The sheer velocity of the modern market, combined with the punitive nature of buy-in regimes and the cost of intraday liquidity, demands a shift from static reporting to dynamic, real-time visualization.  
This report outlines a comprehensive architectural framework for a "Best-in-Class" Operations Manager Dashboard. This dashboard is designed not just to display data but to serve as a command-and-control interface that enables rapid decision-making. By synthesizing data from disparate sources—clearing houses (NSCC/DTCC), custodians, internal sub-ledgers, and counterparty communications—the dashboard provides a multi-dimensional view of settlement health.8 It is structured to allow an immediate assessment of high-level KPIs while facilitating a frictionless "drill-down" into the underlying causes of failure, categorized by coverage desk, directionality (receives vs. deliveries), and exception taxonomy.9  
The objective of this document is to provide an exhaustive specification for such a dashboard, detailing the operational logic, regulatory requirements, and data visualization strategies necessary to manage a US equity settlements desk in a T+1 environment. It explores the nuances of managing failures across different business lines—from high-touch Prime Brokerage relationships to high-volume Institutional flows—and articulates how to translate raw settlement data into actionable operational intelligence.

## **2\. The Regulatory and Operational Landscape**

To design an effective dashboard, one must first understand the complex regulatory and operational constraints that define "success" and "failure" in US equity settlements. The dashboard’s logic must be hard-wired to these constraints, alerting the manager not just to *what* has failed, but *why* it matters specifically in the context of current rules.

### **2.1 The T+1 Compression and Affirmation Deadlines**

The move to T+1 was driven by the Securities and Exchange Commission (SEC) to reduce credit, market, and liquidity risks.1 By shortening the settlement cycle, the industry reduces the number of unsettled trades outstanding at any given moment, thereby lowering the exposure of clearing members to the default of a counterparty. However, this risk reduction at the systemic level translates to increased operational pressure at the firm level.11  
A critical component of T+1 compliance is the "Same-Day Affirmation" requirement. Under the new framework, trades must be affirmed—meaning the details are agreed upon by both the investment manager and the broker-dealer—by 9:00 PM ET on the trade date (T).12 This deadline is a crucial checkpoint for the dashboard. Trades affirmed by this cutoff flow automatically into the Depository Trust Company (DTC) for settlement processing. Trades affirmed late require manual intervention, effectively creating "exception" workflows before the settlement date even arrives.14  
Therefore, the Operations Manager’s dashboard cannot solely look at *fails* (which happen on S, or Settlement Date); it must also look upstream at *affirmation rates* on T-Day. A low affirmation rate is a leading indicator of tomorrow’s fails. The dashboard must visualize this "Affirmation Gap"—the delta between executed trades and affirmed trades—in real-time as the 9:00 PM deadline approaches.15

### **2.2 SEC Regulation SHO and Rule 204**

The most significant regulatory constraint governing US equity settlement fails is SEC Regulation SHO, specifically Rule 204\.6 Enacted to curb abusive "naked" short selling, Rule 204 imposes strict close-out requirements on participants of registered clearing agencies (like the NSCC).  
Rule 204 mandates that if a firm has a "fail to deliver" position at the clearing agency in any equity security, it must immediately borrow or purchase securities to close out the fail. The timelines are rigid and non-negotiable, making them the primary driver of "Critical Alerts" on the dashboard.7

* **Short Sales:** If the fail resulted from a short sale, the firm must close out the position by the beginning of regular trading hours on the settlement day following the settlement date (T+3).6  
* **Long Sales:** If the fail resulted from a long sale (where the seller owns the stock but failed to deliver), the firm has until the beginning of regular trading hours on the third settlement day following the settlement date (T+5).6  
* **Market Making:** Bona fide market making activities have an extended deadline of T+6.7  
* **Deemed-to-Own:** For securities deemed to be owned but subject to processing delays (e.g., Rule 144 restricted stock), the close-out period extends to T+35.7

The implications for the dashboard are profound. A fail is not just a fail; it is a ticking clock. The dashboard must automatically classify every fail to deliver based on the underlying trade type (Short vs. Long) and calculate the "Time to Close-Out." A fail to deliver resulting from a short sale that is currently at T+2 is an urgent operational emergency that requires immediate attention from the buy-in desk, whereas a T+2 fail from a long sale may have a different priority level. The dashboard must visually distinguish these regulatory cliffs to prevent the firm from incurring the "pre-borrow penalty," which restricts the firm’s ability to execute short sales without a pre-confirmed borrow.6

### **2.3 The Continuous Net Settlement (CNS) System**

The vast majority of US equity trades settle through the NSCC’s Continuous Net Settlement (CNS) system.19 In CNS, the clearing house becomes the central counterparty (CCP) for every trade—the buyer to every seller and the seller to every buyer. This netting process significantly reduces the volume of physical settlements.  
However, the dashboard must distinguish between **CNS Fails** and **Non-CNS (Trade-for-Trade)** Fails.

* **CNS Fails:** These are net obligations to the NSCC. A failure here affects the firm’s standing with the central clearer and can trigger Rule 204 obligations.  
* **Non-CNS Fails:** These are bilateral fails with specific counterparties (often used for complex prime brokerage trades or specific institutional settlements). These fails carry direct counterparty credit risk and relationship risk but may be managed differently than CNS obligations.20

The dashboard must provide a toggle or a split view to allow the manager to see the "Net" position (what is owed to NSCC) versus the "Gross" position (the underlying client trades that make up that net obligation). Operations managers often struggle when a net delivery obligation to CNS is caused by a single client failing to deliver shares to the broker. The dashboard must bridge this gap, linking the specific client fail (Gross) to the street-side obligation (Net).19

## **3\. Strategic Dashboard Design Principles**

Before detailing the specific widgets and views, it is essential to establish the design philosophy. An Operations Dashboard is a tool for cognitive offloading—it should perform the heavy lifting of data synthesis so the manager can focus on decision execution.10

### **3.1 The "Medallion" Data Architecture**

To ensure the dashboard is fast, accurate, and drillable, the underlying data strategy should follow a "Medallion" architecture.22 While this is a data engineering concept, it directly impacts the *view* the manager sees:

* **Bronze Layer (The Raw Intake):** This is the granular, unpolished data. It includes every individual SWIFT MT548 message, every line item from the DTCC output file, and every raw inventory record. The dashboard allows access to this layer only when the manager drills down to the lowest level (e.g., "Show me the raw reject message from BNY Mellon").  
* **Silver Layer (The Normalized Logic):** This layer cleans and standardizes the data. For instance, Custodian A might report a fail as "Lack of Secs," while Custodian B reports it as "LACK." The Silver layer maps both to a standardized dashboard category: **"Inventory Shortage."** This ensures the dashboard view is consistent regardless of the underlying counterparty or custodian.  
* **Gold Layer (The Executive View):** This is the aggregated, high-level intelligence. It calculates the KPIs: "Total Exposure," "Affirmation Rate," "Rule 204 At-Risk Count." The top-level dashboard view is exclusively populated by Gold Layer data to ensure instant load times and clarity.22

### **3.2 Visual Hierarchy and "Preattentive" Attributes**

The dashboard design must leverage preattentive attributes—color, size, and position—to guide the eye to the most critical information immediately.9

* **Color as Meaning:** Red should be reserved exclusively for "Action Required / Regulatory Risk." Amber for "Warning / Approaching Deadline." Green for "On Track." Neutral colors (greys, blues) should be used for contextual data (e.g., volume trends) to avoid "alert fatigue".9  
* **Z-Pattern Layout:** The most critical information (SOD High-Level KPIs) should be at the top left and center. The breakdown by desk/coverage should follow in the middle. The detailed list of exceptions should be at the bottom, accessible via interaction.

### **3.3 The "3-Click" Rule**

The dashboard must be designed so that an operations manager can get from the highest-level aggregate metric (e.g., "$500M Total Fails") to the specific phone number of the counterparty causing the fail in no more than three clicks.

1. **Click 1:** Select the "Inventory Shortage" bar in the breakdown chart. (Filters the view to only inventory fails).  
2. **Click 2:** Select the "Prime Brokerage" desk slice. (Filters to PB trades).  
3. **Click 3:** Click on the specific CUSIP/Trade ID in the grid. (Opens the Trade Detail card with contact info).

## **4\. Dashboard Component 1: The Executive Intake Ribbon (Start of Day)**

The top section of the dashboard is the "Intake Ribbon." This is the first thing the manager sees at 8:00 AM. It answers the question: *"How bad is it today, and where is the fire?"*  
This ribbon consists of a series of "Big Number" tiles (Scorecards), each accompanied by a small trend line (sparkline) showing the metric over the last 5 days.

### **4.1 Metric 1: Total Gross Fail Value & Count**

* **Display:** **$452.5M** (1,240 Trades)  
* **Context:** Split by **Fails to Receive (FTR)** vs. **Fails to Deliver (FTD)**.  
* **Relevance:** This provides the headline exposure number. A spike here indicates a systemic issue or a major market event.25  
* **Sparkline:** 5-day trend. An upward trend suggests deteriorating operational quality.

### **4.2 Metric 2: Net Regulation SHO Exposure**

* **Display:** **$12.5M** (3 Trades at T+3 Risk)  
* **Color:** Dynamic. If count \> 0 for T+3 (Short) or T+5 (Long), this tile turns **RED**.  
* **Relevance:** This is the "Regulatory Panic Button." It highlights the subset of FTDs that are approaching the mandatory close-out deadline under Rule 204\. It filters out the "noise" of T+1 fails to focus on the "hard" constraints.6

### **4.3 Metric 3: Yesterday’s Affirmation Rate (T-Day Final)**

* **Display:** **96.2%**  
* **Target:** \>95% (Industry Best Practice for T+1).12  
* **Relevance:** A leading indicator. If this number drops below 90%, the manager knows that the *intraday* team will be swamped with exceptions today, likely leading to settlement fails tomorrow. This allows for proactive resource allocation (e.g., moving staff from other tasks to exception management).12

### **4.4 Metric 4: Intraday Liquidity Requirement**

* **Display:** **\-$45M** (Net Funding Needed)  
* **Calculation:** (Total Fails to Receive Value) \- (Total Fails to Deliver Value, adjusted for haircuts/borrowability).  
* **Relevance:** In a T+1 world, liquidity is expensive. This metric tells the manager how much cash the Treasury desk needs to deploy to cover the settlement gaps. If the firm is failing to receive $100M in cash but must deliver $145M in securities, there is a funding mismatch that must be financed.26

### **Table 5: Executive Intake Ribbon Specification**

| Metric Name | Data Source | Calculation Logic | Alert Threshold (Default) | Visual Indicator |
| :---- | :---- | :---- | :---- | :---- |
| **Gross Fail Value** | Sub-ledger / CNS | Sum(Abs(FTD)) \+ Sum(Abs(FTR)) | \> Avg \+ 2σ (Standard Deviations) | Trend Arrow (↑/↓) |
| **Reg SHO At-Risk** | Reg SHO Reporting Engine | Count of FTDs where (Type=Short AND Age\>=T+2) OR (Type=Long AND Age\>=T+4) | \> 0 | Flashing Red Border |
| **Affirmation Rate** | DTCC ITP / Omgeo | (Affirmed Trades / Total Executed Trades) | \< 95% | Amber Background |
| **Cash Impact** | Treasury System | Net Settlement Obligation \+ FTR Impact | \> Daily Limit | Red Text |

## **5\. Dashboard Component 2: The Fails Matrix (Coverage and Directionality)**

Below the ribbon lies the analytical core of the dashboard: The Fails Matrix. This section allows the manager to slice the aggregate data to identify *who* is responsible. The user query specifically requested views by "coverage, receives, deliveries."

### **5.1 The Coverage Heatmap**

* **Visualization:** A Treemap or Heatmap.  
* **Dimensions:** Size of box \= Value of Fails. Color of box \= Fail Count or Age.  
* **Segments:** The view is segmented by **Desk** or **Business Unit**.

#### **5.1.1 Prime Brokerage (PB)**

* **Characteristics:** High value, complex strategies (long/short equity), high sensitivity to client relationships.  
* **Fail Drivers:** Often driven by "Locates" (short selling inventory) or "Recalls" (securities lending).28  
* **Dashboard Specifics:** The PB section of the heatmap must distinguish between "Arranged Financing" fails and standard DVP fails.

#### **5.1.2 Institutional / Custody**

* **Characteristics:** High volume, lower variance. Dealing with pension funds, mutual funds.  
* **Fail Drivers:** SSI mismatches, late instructions from the investment manager.30  
* **Dashboard Specifics:** Requires grouping by **Custodian** (e.g., State Street, BNY Mellon, JP Morgan). This highlights if a specific custodian is having a systemic issue (e.g., "Why are all our BNY trades failing today?").

#### **5.1.3 Retail / Wealth Management**

* **Characteristics:** Smaller individual sizes, massive volume.  
* **Fail Drivers:** Inventory segregation issues, customer margin accounts.  
* **Dashboard Specifics:** Focus on "Pattern Fails"—is a specific branch or retail product generating the errors?

### **5.2 The Directionality Split: Receives vs. Deliveries**

* **Visualization:** A "Butterfly Chart" (or Tornado Chart).  
* **Left Side (Receives \- FTR):** Represents money failing to come in or securities failing to arrive.  
  * *Operational Focus:* Credit risk monitoring. Why hasn't the counterparty delivered? Is it an inventory issue on their side, or did we not pay them (DK)?  
* **Right Side (Deliveries \- FTD):** Represents the firm failing to deliver to the street.  
  * *Operational Focus:* Inventory management and Regulation SHO compliance. This is the side that triggers penalties and buy-ins.

This visual split allows the manager to instantly see if the desk is "Long Fails" (waiting on others) or "Short Fails" (unable to perform). A balanced chart is typical; a lopsided chart indicates a specific process breakdown (e.g., "We are failing to deliver everywhere—is our inventory system down?").

### **5.3 Client Tiering View (The "White Glove" Filter)**

Adhering to the "Gold/Silver/Bronze" service model, the dashboard should allow filtering the Fails Matrix by Client Tier.31

* **Platinum Clients:** The dashboard should highlight fails impacting top-tier clients (e.g., major hedge funds) with a special icon (e.g., a star). Operations managers often need to "hand-hold" these settlements to preserve commercial relationships. A fail of $1M for a Platinum client might be more urgent than a fail of $10M for a Bronze client due to the relationship sensitivity.

## **6\. Dashboard Component 3: The Exception Engine (Root Cause Analysis)**

The user requested an easy way to "dig into the underlying fail data." This is achieved through the **Exception Taxonomy Widget**. This section categorizes fails not by *who* (desk) but by *why* (Root Cause).  
To make this effective, the dashboard must ingest and normalize **SWIFT MT548** (Settlement Status and Processing Advice) messages and **DTCC Reason Codes**.20

### **6.1 The Taxonomy Hierarchy (Drill-Down Paths)**

The dashboard should group the thousands of potential error codes into 4-5 actionable buckets. Clicking on a bucket reveals the granular codes.

#### **Bucket A: Instructional Mismatches (Data Integrity)**

* *Concept:* The buyer and seller disagree on the terms of the trade.  
* *SWIFT Codes:*  
  * **DDEA (Deal Price):** The price on the instruction doesn't match the counterparty.34  
  * **DQUA (Quantity):** Disagreement on share count.  
  * **IIND (Common Reference):** The unique trade ID is missing or mismatched.  
  * **PODU (Possible Duplicate):** The system thinks this trade was already processed.34  
* *Operational Action:* Requires the Middle Office or Trade Support Group to verify the trade ticket.

#### **Bucket B: Standing Settlement Instructions (SSI)**

* *Concept:* The trade details are correct, but the "Where" is wrong.  
* *SWIFT Codes:*  
  * **DEPT (Place of Settlement):** Wrong PSET (Place of Settlement) BIC.33  
  * **ICUS (Receiving/Delivering Custodian):** Wrong custodian details.  
  * **SAFE (Safekeeping Account):** Wrong account number at the custodian.  
* *Context:* SSI mismatches are a leading cause of fails, often due to manual database errors or stale data.35  
* *Operational Action:* Update the ALERT database or internal static data repository.

#### **Bucket C: Inventory & Liquidity (The "Real" Fails)**

* *Concept:* The data is fine, but the assets aren't there.  
* *SWIFT Codes:*  
  * **LACK (Lack of Securities):** The most common code for FTDs. The seller doesn't have the stock.33  
  * **LALO (Loaned Out):** The securities are out on loan. Requires a recall.  
  * **MONY / CMON (Insufficient Money):** The buyer doesn't have the cash.33  
* *Operational Action:* Notify Stock Loan desk for recalls; notify Treasury for cash funding.

#### **Bucket D: Counterparty Status (DK & Late)**

* *Concept:* Behavioral issues with the counterparty.  
* *Codes:*  
  * **DK ("Don't Know"):** The counterparty claims they have no record of the trade.38  
  * **LATE:** Instruction received after the cut-off.  
  * **ADEA (Account Servicer Deadline Missed):** Too late for the custodian to process today.33

### **6.2 Visualization of the Taxonomy**

* **Widget:** A Horizontal Bar Chart.  
* **Interaction:** Clicking "Instructional Mismatches" expands the bar to show the split between Price, Quantity, and SSI.  
* **Insight:** If "Price Mismatch" spikes, it suggests a systemic issue with a specific feed (e.g., "Did the Bloomberg feed break?"). If "LACK" is high, it suggests a liquidity/inventory crisis.

### **Table 6: Mapping Dashboard Categories to Underlying Reason Codes**

| Dashboard Category | SWIFT Reason Codes (MT548) | DTCC Reason Codes | Operational Owner |
| :---- | :---- | :---- | :---- |
| **Inventory Shortage** | LACK, LALO, MINO | 004 (Net Reason) | Stock Loan / Inventory Mgmt |
| **Cash / Credit** | MONY, CMON, CLAC | 054 (Liquidity) | Treasury / Credit Risk |
| **SSI / Reference** | DEPT, ICUS, IEXE, SAFE | 070 (Bad Instructions) | Data Management / Client Service |
| **Trade Discrepancy** | DDEA, DQUA, DDAT, IIND | 056 (Unmatched) | Middle Office / Sales Support |
| **Counterparty Logic** | DKNY, LATE, ADEA | 057 (DK) | Counterparty Relationship Mgmt |

## **7\. Component 4: Inventory Management and Aging**

Managing "Lack of Securities" (LACK) requires a dedicated view, especially given the Rule 204 constraints.

### **7.1 The Aging Buckets (Inventory View)**

The dashboard must visualize fails by their "Age"—how many days they have been failing. This is directly tied to the T+1/T+3/T+5 regulatory clocks.

* **Bucket 1 (T+1):** "Fresh Fails." High volume, usually operational/admin noise.  
* **Bucket 2 (T+2 to T+4):** "Warning Zone." These are hardening fails. For Short Sales, these are already past the Rule 204 deadline (requiring immediate buy-in). For Long sales, they are approaching the cliff.  
* **Bucket 3 (T+5 to T+34):** "Capital Intensive." These fails likely incur increased capital charges and require daily explanations to compliance.  
* **Bucket 4 (T+35+):** "Deemed-to-Own / Restricted." Long-tail fails often related to physical certificates or complex legal transfers.7

### **7.2 Integration with Securities Lending**

For every fail flagged as "Inventory Shortage," the dashboard should pull in data from the Securities Lending system.

* **Indicator:** "Availability."  
* **Logic:** Is this security "Easy to Borrow" (ETB) or "Hard to Borrow" (HTB)?  
* **Visual:** If a fail is $10M and the stock is HTB (Hard to Borrow), the dashboard should highlight this with a **Critical Inventory Icon**. This tells the manager: "You can't just borrow this to fix it; you might need to go to the open market or force a buy-in".25

## **8\. Component 5: Intraday Dynamics and Liquidity Monitoring**

The "SOD" view is static. The dashboard needs a "Live Mode" for intraday management.

### **8.1 Real-Time Settlement Progress**

* **Visualization:** An "Area Chart" or "Burn-Down Chart."  
* **X-Axis:** Time (08:00 AM to 06:00 PM).  
* **Y-Axis:** % of Value Settled.  
* **Data:** Compares "Today's Settlement Trajectory" (Solid Line) vs. "30-Day Average" (Dotted Line).  
* **Insight:** If the solid line is lagging significantly below the dotted line at 1:00 PM, the manager knows there is a bottleneck (e.g., Fedwire delay, DTCC system slowness, or a major counterparty holding up payments).40

### **8.2 RAD (Receiver Authorized Delivery) Queue**

* **Widget:** A "Counter" or "List View."  
* **Context:** Large deliveries often sit in the "RAD" queue at DTCC waiting for the counterparty to manually click "Approve".42  
* **Action:** If a large trade is stuck in RAD, the operations team needs to call the counterparty and ask them to "push the button." The dashboard identifies these high-value "stuck" items instantly.

### **8.3 Intraday Liquidity Forecasting**

* **Widget:** "Cash Ladder."  
* **Logic:** Projects the cash balance at the end of the day based on *expected* settlements vs. *confirmed* settlements.  
* **Insight:** Helps the manager answer the Treasury desk's question: "Can we release this $500M payment, or are we waiting for incoming funds?".26

## **9\. Operational Workflows and Automation**

The ultimate goal of the dashboard is to facilitate action. The design should support "Actionable Intelligence" where the data grid is not just a display, but a control surface.

### **9.1 Contextual Action Menus**

Right-clicking on a fail in the dashboard should bring up a context menu with options derived from the Reason Code:

* **If Reason \= SSI Mismatch:** \-\> "Generate SSI Query Email to Client" (Pre-populated with trade details).  
* **If Reason \= LACK:** \-\> "Check Stock Loan Availability" (API call to Lending system).  
* **If Reason \= DK:** \-\> "Send Trade Confirmation Proof" (Attaches the Omgeo CTM confirm).

### **9.2 The "Rule 204 Buy-In" Workflow**

For fails hitting the Reg SHO deadline (e.g., Short Sale at T+3 market open), the dashboard should feature a "Buy-In Prep" button.

* **Function:** Aggregates the failing position, calculates the quantity required to close out, and formats a standardized "Buy-In Notice" or execution order for the trading desk. This reduces the manual risk of calculating the wrong buy-in quantity.6

## **10\. Technical Architecture and Data Governance**

Building this dashboard requires a robust technical foundation.

### **10.1 Data Lineage and Integration**

* **Ingestion:** Real-time listeners for SWIFT (MQ Series) and File Watchers for DTCC/NSCC output files (MRO, CNS).  
* **Storage:** A high-performance time-series database (e.g., KDB+ or InfluxDB) is ideal for the intraday metrics, while a relational database (PostgreSQL/Oracle) serves the static trade data.44  
* **API Layer:** A REST API layer that serves the "Gold Layer" metrics to the front-end (Tableau, PowerBI, or Custom React App).

### **10.2 Role-Based Access Control (RBAC)**

* **Manager View:** Sees everything, financial values, and client names.  
* **Analyst View:** Sees only their coverage desk (e.g., "PB Analyst" sees only PB fails).  
* **Compliance View:** Read-only access to the Reg SHO/Rule 204 metrics for independent verification.45

## **11\. Conclusion**

The transition to T+1 has removed the margin for error in US equity settlements. The "one-day cushion" that operations teams relied upon for decades is gone. In this environment, the Operations Manager Dashboard is not a luxury; it is a critical piece of risk management infrastructure.  
By implementing the framework detailed in this report—focusing on the "Intake Ribbon" for immediate situational awareness, the "Fails Matrix" for directional analysis, and the "Exception Engine" for root cause remediation—firms can transform their settlement operations. The shift is from "cleanup" to "control." The dashboard enables the manager to visualize the invisible operational risks—the Affirmation Gap, the Intraday Liquidity Drag, and the Rule 204 Regulatory Cliff—and act upon them before they crystallize into financial losses or regulatory sanctions.  
In the T+1 era, the best settlement is the one you don't have to think about. But for the ones that fail, this dashboard ensures they are managed with precision, speed, and intelligence.

#### **Works cited**

1. Understanding Settlement Cycles: What Does T+1 Mean for You? | FINRA.org, accessed on February 5, 2026, [https://www.finra.org/investors/insights/understanding-settlement-cycles](https://www.finra.org/investors/insights/understanding-settlement-cycles)  
2. T+1 Settlement \- KPMG International, accessed on February 5, 2026, [https://kpmg.com/xx/en/our-insights/regulatory-insights/t-plus-1-settlement.html](https://kpmg.com/xx/en/our-insights/regulatory-insights/t-plus-1-settlement.html)  
3. JP Morgan US T+1 Securities Settlement – Frequently Asked Questions: Markets Clients, accessed on February 5, 2026, [https://www.jpmorgan.com/insights/securities-services/regulatory-solutions/us-t-plus-1securities-services-markets-faq](https://www.jpmorgan.com/insights/securities-services/regulatory-solutions/us-t-plus-1securities-services-markets-faq)  
4. T+1 Settlement: All You Need to Know | J.P. Morgan, accessed on February 5, 2026, [https://www.jpmorgan.com/insights/securities-services/regulatory-solutions/t-plus-1](https://www.jpmorgan.com/insights/securities-services/regulatory-solutions/t-plus-1)  
5. Supporting a global shortened settlement cycle \- Euroclear, accessed on February 5, 2026, [https://www.euroclear.com/newsandinsights/en/Format/Whitepapers-Reports/supporting-a-global-shortened-settlement-cycle.html](https://www.euroclear.com/newsandinsights/en/Format/Whitepapers-Reports/supporting-a-global-shortened-settlement-cycle.html)  
6. SEC Rule 204 of Regulation SHO \- Jefferies, accessed on February 5, 2026, [https://www.jefferies.com/CMSFiles/Jefferies.com/Files/Policies/regsho.pdf](https://www.jefferies.com/CMSFiles/Jefferies.com/Files/Policies/regsho.pdf)  
7. SEC ADOPTS FINAL RULE 204 OF REGULATION SHO TO REDUCE FAILS TO DELIVER, accessed on February 5, 2026, [https://www.willkie.com/publications/2009/08/sec-adopts-final-rule-204-of-regulation-sho-to-r\_\_](https://www.willkie.com/publications/2009/08/sec-adopts-final-rule-204-of-regulation-sho-to-r__)  
8. Understanding the DTCC Subsidiaries Settlement Process, accessed on February 5, 2026, [https://www.dtcc.com/understanding-settlement/index.html](https://www.dtcc.com/understanding-settlement/index.html)  
9. 8 Best Practices for Dashboard Design with Excellent Examples \- Sigma Computing, accessed on February 5, 2026, [https://www.sigmacomputing.com/blog/best-practices-dashboard-design-examples](https://www.sigmacomputing.com/blog/best-practices-dashboard-design-examples)  
10. 20 Operational Dashboard Best Practices: Beginner's Guide \- Xenia.Team, accessed on February 5, 2026, [https://www.xenia.team/articles/operational-dashboard-best-practices](https://www.xenia.team/articles/operational-dashboard-best-practices)  
11. Shortening the US Equities Settlement Cycle \- DTCC, accessed on February 5, 2026, [https://www.dtcc.com/ust1](https://www.dtcc.com/ust1)  
12. SIFMA, ICI, and DTCC Release “T+1 After Action Report” Industry Coordination Led to Successful Transition, Reducing Risk and Costs in the System, accessed on February 5, 2026, [https://www.sifma.org/news/press-releases/sifma-ici-and-dtcc-release-t1-after-action-report-industry-coordination-led-to-successful-transition-reducing-risk-and-costs-in-the-system](https://www.sifma.org/news/press-releases/sifma-ici-and-dtcc-release-t1-after-action-report-industry-coordination-led-to-successful-transition-reducing-risk-and-costs-in-the-system)  
13. Trade Affirmations: Key Questions Answered as T+1 Approaches \- DTCC, accessed on February 5, 2026, [https://www.dtcc.com/dtcc-connection/articles/2024/april/23/trade-affirmations-key-questions-answered-as-t1-approaches](https://www.dtcc.com/dtcc-connection/articles/2024/april/23/trade-affirmations-key-questions-answered-as-t1-approaches)  
14. Navigating T+1 settlement: Agility and resilience in finance \- HCLTech, accessed on February 5, 2026, [https://www.hcltech.com/blogs/post-tplus1-go-live-reduction-in-trade-settlement-cycle-calls-for-agility-and-resilience](https://www.hcltech.com/blogs/post-tplus1-go-live-reduction-in-trade-settlement-cycle-calls-for-agility-and-resilience)  
15. US T+1, affirmation, and the settlement cycle \- BNP Paribas Securities Services, accessed on February 5, 2026, [https://securities.cib.bnpparibas/us-t1-trade-affirmation-settlement/](https://securities.cib.bnpparibas/us-t1-trade-affirmation-settlement/)  
16. 17 CFR § 242.204 \- Close-out requirement. \- Cornell Law School, accessed on February 5, 2026, [https://www.law.cornell.edu/cfr/text/17/242.204](https://www.law.cornell.edu/cfr/text/17/242.204)  
17. Division of Market Regulation \- SEC.gov, accessed on February 5, 2026, [https://www.sec.gov/rules-regulations/staff-guidance/trading-markets-frequently-asked-questions-8](https://www.sec.gov/rules-regulations/staff-guidance/trading-markets-frequently-asked-questions-8)  
18. Key Points About Regulation SHO \- SEC.gov, accessed on February 5, 2026, [https://www.sec.gov/investor/pubs/regsho.htm](https://www.sec.gov/investor/pubs/regsho.htm)  
19. Fails-to-Deliver Data \- SEC.gov, accessed on February 5, 2026, [https://www.sec.gov/data-research/sec-markets-data/fails-deliver-data](https://www.sec.gov/data-research/sec-markets-data/fails-deliver-data)  
20. T1 Net Reason Codes \- DTCC, accessed on February 5, 2026, [https://www.dtcc.com/ust1/-/media/Files/PDFs/T2/NetReasonCodes.pdf](https://www.dtcc.com/ust1/-/media/Files/PDFs/T2/NetReasonCodes.pdf)  
21. Beyond Pretty Charts: Creating Actionable Financial Dashboards That Drive Decisions, accessed on February 5, 2026, [https://corporatefinanceinstitute.com/resources/fpa/financial-dashboards-that-drive-decisions/](https://corporatefinanceinstitute.com/resources/fpa/financial-dashboards-that-drive-decisions/)  
22. Medallion Architecture: A Layered Data Optimization Model \- Information Week, accessed on February 5, 2026, [https://www.informationweek.com/machine-learning-ai/medallion-architecture-a-layered-data-optimization-model](https://www.informationweek.com/machine-learning-ai/medallion-architecture-a-layered-data-optimization-model)  
23. Bronze, Silver, and Gold Data Layers \- The Agile Brand Guide®, accessed on February 5, 2026, [https://agilebrandguide.com/wiki/data/bronze-silver-and-gold-data-layers/](https://agilebrandguide.com/wiki/data/bronze-silver-and-gold-data-layers/)  
24. Understanding the Three Layers of Medallion Architecture \- ER/Studio, accessed on February 5, 2026, [https://erstudio.com/blog/understanding-the-three-layers-of-medallion-architecture/](https://erstudio.com/blog/understanding-the-three-layers-of-medallion-architecture/)  
25. Measuring Settlement Fails \- Liberty Street Economics \- Federal Reserve Bank of New York, accessed on February 5, 2026, [https://libertystreeteconomics.newyorkfed.org/2014/09/measuring-settlement-fails/](https://libertystreeteconomics.newyorkfed.org/2014/09/measuring-settlement-fails/)  
26. Real-Time Intraday Liquidity Management Solution \- Baton Systems, accessed on February 5, 2026, [https://batonsystems.com/solutions/real-time-intraday-liquidity-management-solution/](https://batonsystems.com/solutions/real-time-intraday-liquidity-management-solution/)  
27. Monitoring tools for intraday liquidity management \- Bank for International Settlements, accessed on February 5, 2026, [https://www.bis.org/publ/bcbs248.pdf](https://www.bis.org/publ/bcbs248.pdf)  
28. Understanding Prime Brokers: Services and Importance for Hedge Funds \- Investopedia, accessed on February 5, 2026, [https://www.investopedia.com/articles/professionals/110415/role-prime-broker.asp](https://www.investopedia.com/articles/professionals/110415/role-prime-broker.asp)  
29. Prime Services | Goldman Sachs, accessed on February 5, 2026, [https://www.goldmansachs.com/what-we-do/ficc-and-equities/prime-services](https://www.goldmansachs.com/what-we-do/ficc-and-equities/prime-services)  
30. The Difference Between a Prime Broker and a Custodian | GIS UK, accessed on February 5, 2026, [https://www.gisukltd.com/news/news\_details/the-difference-between-a-prime-broker-and-a-custodian\_45](https://www.gisukltd.com/news/news_details/the-difference-between-a-prime-broker-and-a-custodian_45)  
31. How to bring the best of the bank to corporates: Ideas for coverage models \- McKinsey, accessed on February 5, 2026, [https://www.mckinsey.com/industries/financial-services/our-insights/how-to-bring-the-best-of-the-bank-to-corporates-ideas-for-coverage-models](https://www.mckinsey.com/industries/financial-services/our-insights/how-to-bring-the-best-of-the-bank-to-corporates-ideas-for-coverage-models)  
32. Transaction Reason \- DTCC, accessed on February 5, 2026, [https://www.dtcc.com/-/media/Files/Downloads/Investment-Product-Services/Insurance-and-Retirement-Services/Participant-Support-Services/Standard-Usage/Licensing-and-Appointments/18300Status-Reason-Codes.xls](https://www.dtcc.com/-/media/Files/Downloads/Investment-Product-Services/Insurance-and-Retirement-Services/Participant-Support-Services/Standard-Usage/Licensing-and-Appointments/18300Status-Reason-Codes.xls)  
33. MT548: (84) Field 24B: Reason Code \- ISO 20022, accessed on February 5, 2026, [https://www.iso20022.org/15022/uhb/mt548-84-field-24b.htm](https://www.iso20022.org/15022/uhb/mt548-84-field-24b.htm)  
34. MT548: (12) Field 24B: Reason Code \- ISO 20022, accessed on February 5, 2026, [https://www.iso20022.org/15022/uhb/mt548-12-field-24b.htm](https://www.iso20022.org/15022/uhb/mt548-12-field-24b.htm)  
35. Sharing of Standard Settlement Instructions (SSIs) \- FMSB, accessed on February 5, 2026, [https://fmsb.com/wp-content/uploads/2025/01/20241128\_FMSB-Standard-for-Sharing-of-Standard-Settlement-Instructions-SSIs\_FINAL.pdf](https://fmsb.com/wp-content/uploads/2025/01/20241128_FMSB-Standard-for-Sharing-of-Standard-Settlement-Instructions-SSIs_FINAL.pdf)  
36. Market Practice for the Communication of Standing Settlement Instructions | ISITC, accessed on February 5, 2026, [https://isitc.org/wp-content/uploads/Standing-Settlement-Instruction-Market-Practice.pdf](https://isitc.org/wp-content/uploads/Standing-Settlement-Instruction-Market-Practice.pdf)  
37. iso 15022 messages \- Euronext, accessed on February 5, 2026, [https://www.euronext.com/sites/default/files/2024-12/Layouts%20ISO%2015022%20Messages-Specifications.pdf](https://www.euronext.com/sites/default/files/2024-12/Layouts%20ISO%2015022%20Messages-Specifications.pdf)  
38. Custody Services | Comptroller's Handbook \- OCC.gov, accessed on February 5, 2026, [https://www.occ.gov/publications-and-resources/publications/comptrollers-handbook/files/custody-services/pub-ch-custody-services.pdf](https://www.occ.gov/publications-and-resources/publications/comptrollers-handbook/files/custody-services/pub-ch-custody-services.pdf)  
39. T+1 SECURITIES SETTLEMENT INDUSTRY IMPLEMENTATION PLAYBOOK \- DTCC, accessed on February 5, 2026, [https://www.dtcc.com/-/media/Files/PDFs/T2/T1-Industry-Implementation-Playbook.pdf](https://www.dtcc.com/-/media/Files/PDFs/T2/T1-Industry-Implementation-Playbook.pdf)  
40. Intraday chart examples using Highcharts, accessed on February 5, 2026, [https://www.highcharts.com/blog/tutorials/intraday-chart-examples-using-highcharts/](https://www.highcharts.com/blog/tutorials/intraday-chart-examples-using-highcharts/)  
41. Top 10 Intraday Chart Patterns: Every Traders Should Know \- StockGro, accessed on February 5, 2026, [https://www.stockgro.club/blogs/intraday-trading/intraday-chart-patterns/](https://www.stockgro.club/blogs/intraday-trading/intraday-chart-patterns/)  
42. DTC Settlement Service Guide \- Exhibit 5, accessed on February 5, 2026, [https://www.sec.gov/files/rules/sro/dtc/2014/34-73443-ex5.pdf](https://www.sec.gov/files/rules/sro/dtc/2014/34-73443-ex5.pdf)  
43. Navigating cash and treasury: 4\. Establish intraday liquidity monitoring capabilities \# en, accessed on February 5, 2026, [https://www.infor.com/blog/navigating-cash-and-treasury-4-establish-intraday-liquidity-monitoring-capabilities](https://www.infor.com/blog/navigating-cash-and-treasury-4-establish-intraday-liquidity-monitoring-capabilities)  
44. 2 High Availability and Data Protection – Getting From Requirements to Architecture \- Oracle Help Center, accessed on February 5, 2026, [https://docs.oracle.com/en/database/oracle/oracle-database/23/haovw/ha-requirements-architecture.html](https://docs.oracle.com/en/database/oracle/oracle-database/23/haovw/ha-requirements-architecture.html)  
45. Compliance Programs of Investment Companies and Investment Advisers \- SEC.gov, accessed on February 5, 2026, [https://www.sec.gov/rules-regulations/2003/12/compliance-programs-investment-companies-investment-advisers](https://www.sec.gov/rules-regulations/2003/12/compliance-programs-investment-companies-investment-advisers)  
46. Leveraging SEC Rule 204-2 as a foundation for compliance \- Global Relay, accessed on February 5, 2026, [https://www.globalrelay.com/resources/the-compliance-hub/rules-and-regulations/recordkeeping-sec-rule-204/](https://www.globalrelay.com/resources/the-compliance-hub/rules-and-regulations/recordkeeping-sec-rule-204/)