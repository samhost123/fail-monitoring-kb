# **The Mechanics of US Equity Settlement: A Comprehensive Technical Analysis of the Lifecycle Decision Tree, Financial Operations, and T+1 Settlement Architecture**

## **I. Introduction: The Deterministic Settlement Machine**

The infrastructure governing the United States equity markets functions as a deterministic machine, a sophisticated ecosystem defined by algorithmic netting, rigorous inventory logistics, and unforgiving regulatory enforcement. At the core of this environment lies the Depository Trust & Clearing Corporation (DTCC) and its subsidiaries, the National Securities Clearing Corporation (NSCC) and The Depository Trust Company (DTC). While often perceived as a singular back-office utility, the settlement process is, in reality, a complex decision tree of continuous netting, allocation logic, and exception management.1  
For the modern broker-dealer, settlement is no longer a passive post-trade administrative function. It has evolved into a critical discipline of Financial Operations (FinOps), where the optimization of capital, liquidity, and inventory directly impacts the firm's profitability and regulatory standing. The transition to a T+1 settlement cycle in May 2024 has further compressed this lifecycle, removing the historical 24-hour buffer used for remediation and forcing firms to adopt near-real-time operational workflows.2  
This report provides an exhaustive analysis of the settlement lifecycle, specifically mapped to the "Settlement Lifecycle Decision Tree" (Part VII of the referenced documentation). It dissects the operational flow from trade comparison through to finality or failure, overlaying the financial implications of every decision node. By examining the interplay between Continuous Net Settlement (CNS), the Obligation Warehouse (OW), and Regulation SHO, this analysis illuminates the "plumbing" that safeguards the US capital markets and defines the daily responsibilities of the Financial and Operations Principal (FINOP).

### **The Strategic Imperative of Settlement FinOps**

In the context of equity settlement, FinOps transcends the traditional definition of cost management. It encompasses the holistic management of:

* **Regulatory Capital (SEC Rule 15c3-1):** Minimizing deductions for aged fails and non-marketable assets.4  
* **Liquidity Risk:** Managing intraday net debit caps and collateral requirements at the CCP.5  
* **Margin Efficiency:** Optimizing portfolio composition to reduce Clearing Fund deposits.6  
* **Operational Cost:** Reducing the friction of manual exceptions, buy-ins, and penalty charges.7

The following analysis follows the sequential logic of the Settlement Lifecycle Decision Tree, exploring the operational and financial nuances of each critical node.

## ---

**II. Node 1: Trade Comparison and the CNS Eligibility Decision**

The settlement lifecycle initiates at **Node 1: Trade Comparison & Recording**. At this stage, trade data from exchanges, Alternative Trading Systems (ATS), and Qualified Special Representatives (QSRs) is ingested by the NSCC’s Universal Trade Capture (UTC) system.8 The system performs a binary classification that dictates the subsequent settlement path: Is the security and the specific transaction eligible for Continuous Net Settlement (CNS)?

### **The Logic of CNS Eligibility**

CNS eligibility is the primary gatekeeper of settlement efficiency. To be eligible, a security must be CUSIP-based, denominated in US dollars, and eligible for book-entry transfer at DTC.10 The operational implication of this classification is profound.

* **CNS Eligible:** The trade enters the netting engine. The NSCC becomes the counterparty through novation, guaranteeing the trade and netting it against all other activity.1  
* **Non-CNS Eligible:** The trade is directed to the Obligation Warehouse (OW) or processed as a Balance Order. These trades remain bilateral liabilities, meaning the counterparty risk stays with the trading partners, and settlement requires gross movement of shares and cash.1

### **FinOps Implications of Node 1**

From a FinOps perspective, Node 1 represents a divergence in capital treatment and margin calculation.

1. **Novation and Risk Weighting:** CNS trades, by virtue of the NSCC guarantee, attract favorable capital treatment compared to bilateral receivables. The counterparty risk is substituted with the credit risk of the CCP, which is strictly regulated and highly capitalized.2  
2. **Margin Offsets:** In the CNS environment, a long position in Security A can offset the margin requirement of a short position in Security B (portfolio margining). In a non-CNS environment (Node 8), such offsets are generally unavailable, leading to higher gross margin requirements and trapped liquidity.13  
3. **Balance Sheet Impact:** Bilateral trades (Non-CNS) often result in "gross" payables and receivables on the broker-dealer's balance sheet, inflating the balance sheet size and potentially impacting leverage ratios. CNS trades net down to a single line item per CUSIP, significantly compressing the balance sheet.1

### **Operational Workflow: The T+1 Compression**

In the T+1 environment, the timeline for Node 1 is severely compressed. The cutoff for trade matching and affirmation has moved to 9:00 PM ET on Trade Date (T).14 Trades not affirmed by this deadline may not be automatically introduced to the CNS Night Cycle, forcing them into day-cycle processing or bilateral settlement, increasing the risk of failure.16

## ---

**III. Node 2: The CNS Netting and Accounting Engine**

If the decision at Node 1 is affirmative, the transaction proceeds to **Node 2: CNS Netting & Accounting**. This is the engine of market efficiency, transforming thousands of discrete trade obligations into a streamlined net position.

### **The Mechanics of Multilateral Netting**

CNS netting logic is continuous. It does not merely net today's trades against each other; it nets today's "Settling Trades" against the "Closing Positions" (unsettled fails) from the previous day.1

* **Settling Trades:** New activity from T scheduled for settlement on T+1.  
* **Closing Positions:** The net fail position carried over from T-1 (yesterday’s settlement date).

This creates a rolling net obligation. A broker-dealer who fails to deliver 100 shares on Monday and buys 100 shares on Tuesday will effectively be "flat" on Wednesday morning. The system automatically extinguishes the fail with the new receive, requiring no physical movement of securities.1 This "netting effect" is the single largest contributor to liquidity efficiency in the US markets, reducing the value of securities requiring settlement by over 98% on an average day.19

### **FinOps Analysis: The Mark-to-Market (MTM) Component**

While securities are netted, the financial risk is managed through daily Mark-to-Market (MTM) accounting.

* **Debits and Credits:** Every night, CNS calculates the difference between the contract price of the trade and the current market price (CMP).  
* **Risk Mitigation:** If a member has a fail-to-deliver (short) position and the stock price rises, the system debits the member’s cash account for the difference. This ensures that the counterparty (NSCC) is protected against the replacement cost of the securities.6  
* **Liquidity Management:** The FINOP must ensure sufficient liquidity in the settlement account to meet these MTM calls, which can be substantial during periods of high volatility. Unlike the delivery of securities, which can wait for the algorithm, MTM cash payments are hard deadlines.20

### **Operational Control: The Exemption Logic**

At Node 2, operations teams must make critical decisions regarding **Exemptions**. Firms often hold inventory that is segregated for customer protection (Rule 15c3-3) or intended for other purposes (e.g., stock loan returns). To prevent CNS from automatically grabbing these shares, firms apply "Exemption" instructions.1

* **Level 1 Exemption:** A standing instruction to withhold specific shares.  
* **Level 2 Exemption:** A dynamic instruction (now largely decommissioned/modified for T+1).22  
* **T+1 Impact:** The cutoff for submitting these exemptions has moved to **10:45 PM ET on T**.14 Missing this window risks the inadvertent delivery of customer securities, a severe regulatory violation that requires immediate "recall" and potential capital charges.

## ---

**IV. Node 3: The Night Cycle Allocation (S-1 Evening)**

The actual movement of securities begins at **Node 3: Night Cycle Allocation**. In the compressed T+1 lifecycle, this cycle typically commences around 11:30 PM ET on T (the night before settlement).1

### **Allocation Algorithm and Priority Groups**

The central question at Node 3 is: "Who gets the shares?" NSCC employs a strict, algorithmic hierarchy to allocate limited inventory among receiving members. This is not a random distribution; it is a prioritized queue designed to protect system stability.1  
**The Priority Hierarchy:**

1. **Priority Group 1 (Corporate Actions & Reorgs):** Allocations to members with "CNS Reorganization Sub-Accounts" are prioritized to ensure shareholders can participate in tender offers or voluntary actions.1  
2. **Priority Group 2 (Buy-Ins):** Members who have submitted a "Buy-In Intent" (Node 7 logic) jump to this level. The system prioritizes filling these distinct "aged" fails to prevent market execution of a buy-in.1  
3. **Priority Group 3 (Settling Trades):** The general pool of settling trades. Within this group, the algorithm sorts by **Age of Position** (oldest fails first). If ages are identical, it uses a **Random Number** generator to ensure fairness.1

### **The Stock Borrow Program (SBP)**

A critical FinOps tool active at Node 3 is the **NSCC Stock Borrow Program (SBP)**.

* **Function:** Members with excess inventory can lend shares to the NSCC to cover temporary shortfalls in the system.1  
* **FinOps Benefit:** The lending member earns interest on the cash collateral provided by NSCC.  
* **Settlement Benefit:** The borrowing allows NSCC to complete deliveries to long members who might otherwise fail to receive, reducing systemic friction.1  
* **Limitation:** NSCC will not borrow shares to cover a member's short position if that member is on the "Watch List" or if borrowing would create "wrong-way risk" (e.g., borrowing a bank's own stock).25

**Outcome of Node 3:**

* **YES (Inventory Available):** Shares are debited from the short member and credited to the long member. The trade settles.  
* **NO (Inventory Unavailable):** The position remains open and transitions to **Node 4**.

## ---

**V. Node 4: The Day Cycle Allocation (Settlement Date)**

Trades that fail to settle during the Night Cycle roll into **Node 4: Day Cycle Allocation**. This cycle runs continuously throughout the settlement day (SD), attempting to recycle inventory as it becomes available.1

### **Dynamic Settlement Processing**

The Day Cycle is highly dynamic. As members receive shares from other transactions (e.g., a stock loan return or a separate purchase), those shares are immediately swept by the CNS algorithm to satisfy open short obligations, subject to the member's profile controls.1

### **Optimization: Partial Settlement**

A pivotal efficiency mechanism at Node 4 is **Partial Settlement**.

* **Mechanism:** If a member owes 1,000 shares but only has 400 available, the system will settle the 400 shares and leave a fail obligation of 600\.1  
* **FinOps Impact:** This dramatically reduces the *value* of outstanding fails. Since capital charges and penalties are often based on the notional value of the fail, settling 40% of the obligation directly reduces the regulatory capital burden.25 It also provides the receiving member with 400 shares they can reuse for their own deliveries, increasing the "velocity" of collateral in the system.

### **Cash Reconciliation and Finality**

Throughout Node 4, the **Cash Reconciliation Statement** is updated in real-time. Operations teams must monitor this statement to determine their net funding requirement.5

* **Net-Net Settlement:** At the end of the day (approx. 3:45 PM ET), DTC/NSCC aggregates all activity into a single final figure.13  
* **Settlement Progress Payments (SPP):** If a firm's activity creates a debit balance exceeding its cap, the Treasury/FinOps desk must issue an SPP via Fedwire to release the hold on transactions.27 Failure to fund this obligation halts the firm's processing and can trigger a default event.

## ---

**VI. Node 5: Fail Management and Financial Penalties**

If the Day Cycle concludes without delivery, the transaction formally becomes a "Fail to Deliver" (FTD) at **Node 5**. This status triggers a cascade of financial and regulatory consequences.

### **The CNS Fails Charge (2025/2026 Methodology)**

The cost of failing is not merely reputational; it is an explicit expense line item. NSCC assesses a **CNS Fails Charge** to discourage persistent fails. Recent rule filings (SR-NSCC-2025-013) have overhauled this methodology to be more punitive regarding duration.28  
**New Calculation Logic:**

1. **Removal of CRRM:** The charge is no longer based on the member's credit rating. It is purely position-based.30  
2. **Duration Multiplier:** The penalty rate escalates based on the age of the fail.  
   * **Days 1-5:** A baseline charge (e.g., 5% annualized cost of carry).29  
   * **Days 6-20:** An escalated charge to reflect increased replacement risk.30  
   * **Day 21+:** A punitive charge (potentially 100% of the market value) to force closure.31  
3. **Scope:** The charge applies *only* to fails-to-deliver (shorts), acknowledging that members have limited control over fails-to-receive (longs).32

**FinOps Takeaway:** The "cost of carry" for a fail is no longer just the borrowing cost; it now includes an escalating exchange fee. Operations managers must prioritize closing out fails *before* they hit the Day 6 or Day 21 multipliers to protect the firm's P\&L.

### **Net Capital (Rule 15c3-1) Implications**

Simultaneously, the FINOP must adjust the firm's Net Capital computation.4

* **Aged Fails Deduction:** Generally, a broker-dealer must deduct from its net worth the market value of any fail-to-deliver that is outstanding for 5 business days or longer (or 21 days for municipal securities).33  
* **Mark-to-Market Impact:** For CNS fails, because they are marked-to-market daily, the "contract price" is effectively reset. However, if the market value moves against the firm intraday, the FINOP must ensure sufficient "moment-to-moment" capital is available.34

## ---

**VII. Node 6: Mandatory Close-Out (Regulation SHO Rule 204\)**

**Node 6** is the regulatory backstop. Regulation SHO Rule 204 mandates that fails cannot persist indefinitely. This is a non-negotiable compliance node.1

### **The T+1 Close-Out Matrix**

Under T+1 settlement, the windows for action are compressed.

* **Short Sales:** If a short sale fails on Settlement Date (SD), the firm must borrow or purchase securities to close out the position by the **beginning of trading hours on SD+1** (which is T+2).1  
* **Long Sales:** If a long sale fails (seller owns shares but failed to deliver, e.g., lost certificate), the close-out deadline is **SD+3** (T+4).1  
* **Market Makers:** Bona fide market making activity also has an extended close-out window of **SD+3**.1

### **The "Penalty Box" (Rule 204(b))**

If the firm fails to close out the position by the deadline, it enters the "Penalty Box."

* **Restriction:** The firm (and any broker-dealer clearing for it) is prohibited from executing *any* short sale in that security without a **pre-borrow** arrangement.1  
* **Operational Drag:** This removes the efficiency of the "locate" process. Pre-borrowing requires a firm confirmation of shares *before* the trade, which adds cost, slows down trading, and can severely impact high-frequency or algorithmic trading strategies.37

## ---

**VIII. Node 7: Voluntary Buy-In Mechanics (NSCC Rule 11\)**

While Node 6 is a *regulatory* obligation on the seller, **Node 7** is a *contractual right* of the buyer. The **Voluntary Buy-In** is the mechanism by which a receiving member forces the system to prioritize their delivery.

### **The Strategic Value of the Buy-In Intent**

In a netted system, a "long" member doesn't know *who* is failing to them; they only know NSCC owes them shares. To escalate this, they submit a **Buy-In Intent**.1  
**Operational Steps:**

1. **Submission:** The long member submits the Intent to NSCC.  
2. **Priority Jump:** This action elevates the member's long position to **Priority Group 2** in the CNS Night Cycle.1 They are now ahead of all other banks waiting for shares.  
3. **Retransmittal (The Liability Pass):** If the Night Cycle does not yield shares, NSCC identifies the member with the **oldest short position** in that CUSIP. NSCC sends a **Buy-In Retransmittal Notice** to that failing member.1  
   * *Crucial Detail:* This transforms the generic CNS obligation into a specific liability. The identified short member is now "on the hook" for the buy-in execution risk.1

### **Execution and Financial Settlement**

If the shares are still not delivered by the expiration of the Buy-In Notice (typically N+2):

* **Execution:** The originator (buyer) goes into the open market and purchases the shares ("Buy-In Execution").1  
* **Cost Allocation:** The buyer submits the execution price to NSCC. If the buy-in price is higher than the CNS contract price, the difference is debited from the failing member (the one who received the Retransmittal Notice) and credited to the buyer.39

**FinOps Strategy:** Smart operational teams monitor their "Age of Fails" closely. If a firm has the oldest short position in the street, they are the target for *all* incoming buy-in retransmittals. Firms will often prioritize covering their oldest shorts first to avoid being "tagged" with this buy-in liability.38

## ---

**IX. Node 8: The Obligation Warehouse (OW) and Ex-Clearing**

Not all trades fit into the efficient CNS machine. **Node 8** handles the messy reality of **Ex-Clearing** trades via the Obligation Warehouse (OW).1

### **Bilateral Liability vs. CCP Guarantee**

The defining characteristic of OW is that it is **non-guaranteed**. NSCC does not novate these trades. The OW acts as a ledger and matching engine, but the counterparty risk remains with the trading partners.1

### **Managing "DKs" and RECAPS**

One of the greatest operational risks in ex-clearing is the **"DK" (Don't Know)** trade—where one side recognizes a trade and the other does not. OW automates the comparison of these trades.42  
**RECAPS (Reconfirmation and Pricing Service):**

* **Function:** Periodically, OW runs a RECAPS cycle. It takes open, aged fails and re-prices them to the current market value.1  
* **FinOps Benefit:** By marking the fail to market and settling the cash difference, the credit exposure between the two firms is reset to zero (temporarily). This allows firms to reduce the capital charges associated with unsecured receivables.12  
* **CNS "Rescue":** OW performs a daily scan. If an ex-clearing obligation involves a security that becomes CNS-eligible, OW sends it to Node 2 (CNS), effectively "rescuing" it from the risky bilateral world and placing it under the NSCC guarantee.12

## ---

**X. FinOps Best Practices: Daily Settlement Checklist**

To navigate this decision tree effectively, particularly under T+1, FinOps and Operations teams must adhere to a rigorous daily schedule.

| Time (ET) | Operational Action | Decision Node Impact | FinOps Impact |
| :---- | :---- | :---- | :---- |
| **8:30 AM** | Review **Cash Reconciliation Statement**. Estimate net funding needs. | Node 4 | Determine intraday liquidity requirements (SPP). |
| **9:00 AM** | Monitor **Rule 204 Close-Outs**. Execute buy-ins for T+2 shorts. | Node 6 | Avoid "Penalty Box" restrictions. |
| **11:00 AM** | Review **OW DK items**. Contact counterparties for mismatches. | Node 8 | Reduce capital charges on unmatched trades. |
| **1:30 PM** | Deadline for **Corporate Bond (CMU)** matching for T+1. | Node 1 | Ensure bond trades enter netting. |
| **3:00 PM** | Deadline for **Voluntary Buy-In Execution** submission. | Node 7 | Finalize execution price for charge-back. |
| **3:45 PM** | **Final Settlement Figures** posted. Initiate Fedwire funding if net debit. | Node 4 | Avoid default/systemic block. |
| **6:00 PM** | Assess **Net Capital (15c3-1)** position based on aged fails. | Node 5 | Ensure regulatory capital compliance. |
| **9:00 PM** | **Affirmation Cutoff** for T trade date institutional trades. | Node 1 | Maximize STP; ensure trade makes Night Cycle. |
| **10:45 PM** | **CNS Exemption Cutoff**. Final inventory protection. | Node 2/3 | Protect fully-paid customer securities. |
| **11:30 PM** | **Night Cycle** begins. | Node 3 | Start of T+1 settlement flow. |

## **XI. Conclusion: The FinOps Frontier**

The "Settlement Lifecycle Decision Tree" is not merely a map of securities movements; it is a map of financial liability. Every node represents a choice between efficiency and risk.

* **Node 2 (Netting)** maximizes liquidity.  
* **Node 5 (Fails)** incurs penalty charges.  
* **Node 6 (Reg SHO)** risks trading authority.  
* **Node 7 (Buy-In)** enforces market discipline.

For the FinOps professional, the transition to T+1 has shifted the focus from "post-trade processing" to "real-time inventory orchestration." The ability to navigate these nodes—leveraging IMS profiles, managing fail ages to avoid escalators, and utilizing the Stock Borrow Program—determines the operational alpha of the firm. In a market defined by velocity, the efficiency of the back office is now a front-line competitive advantage.

### **List of Tables**

1. **Table 1: Comparison of Settlement Modes (CNS vs. Bilateral/OW)**  
2. **Table 2: IMS Profile Logic and Strategic Use Cases**  
3. **Table 3: CNS Fails Charge Escalation Matrix (2025/2026 Rules)**  
4. **Table 4: Mandatory Close-Out Timelines (Reg SHO Rule 204\)**  
5. **Table 5: Daily FinOps Settlement Schedule (T+1)**

## ---

**Detailed Component Analysis**

### **Table 1: Comparison of Settlement Modes (CNS vs. Bilateral/OW)**

| Feature | Continuous Net Settlement (CNS) (Node 2\) | Obligation Warehouse (OW) / Bilateral (Node 8\) |
| :---- | :---- | :---- |
| **Counterparty** | NSCC (Central Counterparty).1 | The trading partner (Broker-to-Broker).12 |
| **Guarantee** | Yes (Trade Guarantee attached).11 | No (Non-Guaranteed).41 |
| **Settlement Mechanics** | Net Long / Net Short per CUSIP.1 | Gross delivery per trade instruction.1 |
| **Balance Sheet** | Netted (Low Impact).1 | Gross Payables/Receivables (High Impact).1 |
| **Mark-to-Market** | Daily Cash Settlement of MTM.24 | Periodic via RECAPS cycle.43 |
| **Exception Mgmt** | Automated (Stock Borrow, Partials).1 | Manual / Semi-Automated (DKs, Phone calls).44 |
| **Buy-In Rules** | NSCC Rule 11 (Retransmittal/Priority).1 | FINRA Rule 11810 (Direct Notice).45 |

### **Table 2: IMS Profile Logic and Strategic Use Cases**

| Profile Type | Operational Behavior | Strategic FinOps Use Case |
| :---- | :---- | :---- |
| **Green** | **High Automation:** Deliveries process immediately if inventory exists and risk caps are met.1 | Used for high-volume, low-value flow where speed and STP are prioritized to reduce operational overhead. |
| **Yellow** | **Conditional:** Deliveries are sequenced. Positions may be "reserved" pending authorization.1 | Used to manage "scarcity." If a firm has 100 shares and owes 100 to Client A and 100 to the Street, Yellow profile allows the firm to prioritize Client A manually. |
| **Red** | **Manual:** Transactions queued; explicit release required.1 | Used for high-value risk items or when a firm is close to its Net Debit Cap and must strictly control cash outflows/inflows. |

### **Table 3: CNS Fails Charge Escalation Matrix (Proposed 2025/2026 Rules)**

| Fail Duration (Days) | Charge Basis | FinOps Implication |
| :---- | :---- | :---- |
| **1 \- 5 Days** | Low % of Market Value (e.g., 5%).29 | Cost of doing business; focus on operational clean-up. |
| **6 \- 20 Days** | Escalating % of Market Value.30 | Warning zone. The cost of the fail begins to exceed the cost of borrowing stock. FinOps should push for a borrow. |
| **21+ Days** | **100% of Market Value** (Proposed).31 | Critical P\&L hit. Indicates "impaired liquidity." The penalty forces the firm to execute a buy-in or borrow at any price. |

### **Table 4: Mandatory Close-Out Timelines (Reg SHO Rule 204 in T+1)**

| Transaction Type | Close-Out Deadline | Action Required |
| :---- | :---- | :---- |
| **Short Sale Fail** | Market Open **SD+1** (T+2).1 | Borrow or Buy shares. |
| **Long Sale Fail** | Market Open **SD+3** (T+4).1 | Buy shares (unless operational delay proven). |
| **Market Maker** | Market Open **SD+3** (T+4).1 | Borrow or Buy shares. |
| **Penalty for Non-Compliance** | Immediate "Penalty Box".1 | Restriction on short sales without pre-borrow. |

## ---

**Works Cited**

* 1  
  User Document: "Equity Settlement Workflow and Decision Tree".  
* 19  
  DTCC: "Efficient Netting & Settlement with CNS".  
* 27  
  DTCC: "Understanding Settlement".  
* 2  
  ISDA: "T+1 Settlement Cycle Booklet".  
* 13  
  DTCC: "Settlement Service Guide" (General).  
* 6  
  DTCC Learning: "NSCC Risk Margin Component Guide" (Fails Charge).  
* 28  
  DTCC Rule Filing: SR-NSCC-2025-013 (Fails Charge Methodology).  
* 32  
  DTCC Important Notice: "Fails Charge Enhancements".  
* 10  
  Federal Register: "Amendments to Regulation SHO".  
* 18  
  DTCC: "NSCC Rules & Procedures" (Netting).  
* 46  
  Cornell Law: "17 CFR § 240.15c3-1" (Net Capital).  
* 25  
  DTCC: "Settlement Enhancements: Partial Settlement".  
* 2  
  SEC: "The Stock Borrow Program".  
* 25  
  Federal Register: "Stock Borrow Program Risk Enhancements".  
* 13  
  DTCC: "NSCC Risk Margin Component Guide".  
* 45  
  FINRA: "Rule 11810 Buying-In".  
* 6  
  FINRA: "Rule 11810 Buy-In Procedures".  
* 47  
  Federal Register: "Order Approving Fails Charge".  
* 14  
  DTCC: "T+1 Functional Changes" (Affirmation Timelines).  
* 2  
  ISDA: "T+1 Settlement Cycle Booklet" (Recalls).  
* 48  
  ICI: "T+1 Playbook" (ETF/CNS Timelines).  
* 12  
  DTCC: "Obligation Warehouse Service".  
* 43  
  DTCC: "Year 2026 Obligation Warehouse RECAPS Schedule".  
* 8  
  FINRA: "Books and Records Requirements".  
* 22  
  State Street: "T+1 Functional Changes".  
* 23  
  ECB: "T+1 Overview" (Night Cycle Timings).  
* 48  
  ICI: "T+1 Playbook".  
* 13  
  DTCC: "Settlement Service Guide".  
* 46  
  Cornell Law: "17 CFR § 240.15c3-1".  
* 29  
  SEC: "Proposed Rule Change CNS Fails Charge".  
* 31  
  SEC: "SR-NSCC-2025-013".  
* 4  
  SEC: "Key Rules" (Net Capital).  
* 33  
  Florida OFR: "Rule 15c3-1" (Municipal Fails).  
* 12  
  DTCC: "OW for Real-time Matching".  
* 49  
  SIX Group: "Settlement Fails".  
* 7  
  DTCC: "Impact of Fails Infographic".  
* 50  
  SWIFT: "Settlement Fails".  
* 6  
  DTCC: "Risk Margin Component Guide" (MTM).  
* 32  
  DTCC: "Important Notice a9687".  
* 30  
  Federal Register: "SR-NSCC-2025-013".  
* 34  
  FINRA: "SEA Rule 15c3-1 Interpretations".  
* 4  
  SEC: "Key Rules".  
* 51  
  DTCC: "Ask the Expert: Same Day Settlement".  
* 47  
  Federal Register: "SR-NSCC-2025-013".  
* 11  
  DTCC: "NSCC Disclosure Framework".  
* 13  
  DTCC: "Settlement Service Guide".  
* 34  
  FINRA: "Interpretations 15c3-1".  
* 51  
  DTCC: "Ask the Expert".  
* 31  
  SEC: "SR-NSCC-2025-013" (Buy-In Process).  
* 52  
  DTCC: "SR-NSCC-2025-011" (ACATS).  
* 39  
  Federal Register: "Clarify Buy-In Rules".  
* 24  
  DTCC: "CNS System" (Buy-In Priority).  
* 38  
  SEC: "SR-NSCC-2018-007" (Retransmittal).  
* 53  
  Federal Register: "SR-NSCC-2018-007" (Retransmittal Notice).  
* 17  
  Investopedia: "Continuous Net Settlement".  
* 24  
  DTCC: "CNS System".  
* 5  
  SEC: "SR-NSCC-2014-04" (Cash Reconciliation).  
* 20  
  Microsoft: "Dynamics 365 Settlement".  
* 54  
  DTCC: "Inventory Management System".  
* 3  
  UBS: "T+1 Settlement".  
* 33  
  Florida OFR: "Rule 15c3-1".  
* 55  
  FINRA: "Interpretations 15c3-1".  
* 56  
  FINRA: "Regulatory Oversight Report" (Rule 204).  
* 57  
  Harvard Law: "SEC Short Sale Rules".  
* 35  
  Cornell Law: "Rule 204 Close-out".  
* 37  
  Oyster LLC: "Reg SHO Compliance".  
* 36  
  SEC: "Key Points About Reg SHO".  
* 12  
  DTCC: "Obligation Warehouse".  
* 9  
  DTCC: "Functional Change Document" (UTC).  
* 2  
  ISDA: "T+1 Settlement Cycle".  
* 41  
  DTCC Learning: "Obligation Warehouse Overview".  
* 44  
  DTCC: "Managing Risks of Ex-Clearing".  
* 42  
  DTCC Learning: "OW Users" (DKs).  
* 58  
  Federal Register: "SR-NSCC-2024-002".  
* 14  
  DTCC: "T+1 Functional Changes".  
* 2  
  ISDA: "T+1 Settlement Cycle".  
* 24  
  DTCC: "CNS System".  
* 59  
  Interactive Brokers: "CNS Glossary".  
* 5  
  SEC: "SR-NSCC-2014-04" (Accounting Summary).  
* 60  
  AFME: "US T+1 Settlement FAQs".  
* 34  
  FINRA: "Interpretations 15c3-1".  
* 55  
  FINRA: "Interpretations 15c3-1" (CNS Balances).  
* 61  
  ECFR: "Rule 15c3-1".  
* 30  
  Federal Register: "SR-NSCC-2025-013" (Fails Charge Risk).  
* 31  
  SEC: "SR-NSCC-2025-013" (100% Charge).  
* 26  
  DTCC: "NSCC Rules".  
* 39  
  Federal Register: "SR-NSCC-2018-007".  
* 24  
  DTCC: "CNS System" (Liability).  
* 62  
  ICMA: "Buy-in Rules Webinar".  
* 14  
  DTCC: "T+1 Functional Changes".  
* 48  
  ICI: "T+1 Playbook".  
* 26  
  DTCC: "NSCC Rules" (Cash Recon).  
* 22  
  State Street: "T+1 Functional Changes".  
* 21  
  SEC: "SR-NSCC-2005-15" (Stock Borrow/Partials).  
* 3  
  UBS: "T+1 Settlement".  
* 16  
  PostTrade360: "T+1 Challenges".  
* 30  
  Federal Register: "SR-NSCC-2025-013".  
* 52  
  DTCC: "SR-NSCC-2025-011".  
* 5  
  SEC: "SR-NSCC-2014-04".  
* 33  
  Florida OFR: "Rule 15c3-1".  
* 55  
  FINRA: "Interpretations 15c3-1".  
* 52  
  DTCC: "SR-NSCC-2025-011".  
* 63  
  Jefferies: "Reg SHO Policy".  
* 25  
  FINRA: "Understanding Settlement".  
* 27  
  DTCC: "Understanding Settlement".  
* 27  
  DTCC: "Understanding Settlement".  
* 64  
  DTCC Learning: "CNS".  
* 65  
  SEC: "Proposed Rule T+1".  
* 40  
  FINRA: "Rule 11810".  
* 66  
  BBH: "T+1 FAQ".  
* 15  
  DTCC: "Trade Settlement Blind Spots".

#### **Works cited**

1. Equity Settlement Workflow and Decision Tree  
2. T+1 settlement cycle booklet \- ISDA.org, accessed on February 3, 2026, [https://www.isda.org/a/fFwgE/T1-Settlement-Cycle-Booklet.pdf](https://www.isda.org/a/fFwgE/T1-Settlement-Cycle-Booklet.pdf)  
3. North America T+1 Settlement \- UBS, accessed on February 3, 2026, [https://www.ubs.com/global/en/investment-bank/regulatory-directory/na-t1/about.html](https://www.ubs.com/global/en/investment-bank/regulatory-directory/na-t1/about.html)  
4. Key. SEC Financial Responsibility Rules, accessed on February 3, 2026, [https://www.sec.gov/about/offices/oia/oia\_market/key\_rules.pdf](https://www.sec.gov/about/offices/oia/oia_market/key_rules.pdf)  
5. Exhibit 5 \- SEC.gov, accessed on February 3, 2026, [https://www.sec.gov/files/rules/sro/nscc/2014/34-71725-ex5.pdf](https://www.sec.gov/files/rules/sro/nscc/2014/34-71725-ex5.pdf)  
6. NSCC Risk Margin Component Guide \- DTCC Learning Center, accessed on February 3, 2026, [https://dtcclearning.com/documents/equities-clearing/nscc-risk-management/risk-management-nscc/3992-nscc-risk-margin-component-guide.html](https://dtcclearning.com/documents/equities-clearing/nscc-risk-management/risk-management-nscc/3992-nscc-risk-margin-component-guide.html)  
7. hidden impact: \- the real cost of trade fails \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/itp-hub/dist/downloads/Impact\_of\_fails\_Infographic\_2020.pdf](https://www.dtcc.com/itp-hub/dist/downloads/Impact_of_fails_Infographic_2020.pdf)  
8. Books and Records Requirements Checklist for Broker-Dealers \- FINRA, accessed on February 3, 2026, [https://www.finra.org/sites/default/files/2022-02/Books-and-Records-Requirements-Checklist-for-Broker-Dealers.pdf](https://www.finra.org/sites/default/files/2022-02/Books-and-Records-Requirements-Checklist-for-Broker-Dealers.pdf)  
9. Equities Clearing & Settlement Transformation-Functional Change Document \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/-/media/Files/Downloads/Transformation/Functional-Change-Document.pdf](https://www.dtcc.com/-/media/Files/Downloads/Transformation/Functional-Change-Document.pdf)  
10. NSCC IOSCO Disclosure Framework \- Bank for International Settlements, accessed on February 3, 2026, [https://www.bis.org/publ/cpss20\_usnscc.pdf](https://www.bis.org/publ/cpss20_usnscc.pdf)  
11. NATIONAL SECURITIES CLEARING CORPORATION \- Disclosure Framework for Covered Clearing Agencies and Financial Market Infrastructures \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/-/media/Files/Downloads/legal/policy-and-compliance/NSCC\_Disclosure\_Framework.pdf](https://www.dtcc.com/-/media/Files/Downloads/legal/policy-and-compliance/NSCC_Disclosure_Framework.pdf)  
12. Obligation Warehouse (OW) for Real-time Matching \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/clearing-and-settlement-services/equities-clearing-services/ow](https://www.dtcc.com/clearing-and-settlement-services/equities-clearing-services/ow)  
13. Settlement Service Guide \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/globals/pdfs/2018/february/27/service-guide-settlement](https://www.dtcc.com/globals/pdfs/2018/february/27/service-guide-settlement)  
14. ACCELERATED SETTLEMENT (T+1) \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/-/media/Files/PDFs/T2/T1-Functional-Changes.pdf](https://www.dtcc.com/-/media/Files/PDFs/T2/T1-Functional-Changes.pdf)  
15. Trade Settlement: Know Your T+1 Blind Spots \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/dtcc-connection/articles/2024/april/29/trade-settlement-know-your-t1-blind-spots](https://www.dtcc.com/dtcc-connection/articles/2024/april/29/trade-settlement-know-your-t1-blind-spots)  
16. FinOps explores T+1 challenges for fund managers | PostTrade 360°, accessed on February 3, 2026, [https://posttrade360.com/news/fund-ops/finops-explores-t1-challenges-for-fund-managers/](https://posttrade360.com/news/fund-ops/finops-explores-t1-challenges-for-fund-managers/)  
17. Continuous Net Settlement (CNS): Overview, Advantages, Example \- Investopedia, accessed on February 3, 2026, [https://www.investopedia.com/terms/c/cns.asp](https://www.investopedia.com/terms/c/cns.asp)  
18. SECURITIES AND EXCHANGE COMMISSION WASHINGTON, D.C. 20549 Form 19b-4 Description Contact Information Signature \- Options Clearing Corporation, accessed on February 3, 2026, [https://www.theocc.com/getmedia/e09d82f0-45a9-4eed-9970-867f3dedaf17/SR-OCC-2023-801-Amendment-2.pdf](https://www.theocc.com/getmedia/e09d82f0-45a9-4eed-9970-867f3dedaf17/SR-OCC-2023-801-Amendment-2.pdf)  
19. Fundamentals of the Securities Trade Lifecycle \- Informa Connect, accessed on February 3, 2026, [https://informaconnect.com/fundamentals-of-the-securities-trade-lifecycle/](https://informaconnect.com/fundamentals-of-the-securities-trade-lifecycle/)  
20. Configure settlement \- Finance | Dynamics 365 \- Microsoft Learn, accessed on February 3, 2026, [https://learn.microsoft.com/en-us/dynamics365/finance/cash-bank-management/configure-settlement](https://learn.microsoft.com/en-us/dynamics365/finance/cash-bank-management/configure-settlement)  
21. SECURITIES AND EXCHANGE COMMISSION \- SEC.gov, accessed on February 3, 2026, [https://www.sec.gov/files/rules/sro/nscc/34-50026.pdf](https://www.sec.gov/files/rules/sro/nscc/34-50026.pdf)  
22. ACCELERATED SETTLEMENT (T+1) \- State Street, accessed on February 3, 2026, [https://www.statestreet.com/web/insights/articles/documents/t1-functional-changes.pdf](https://www.statestreet.com/web/insights/articles/documents/t1-functional-changes.pdf)  
23. item 2 T+1 Overview, accessed on February 3, 2026, [https://www.ecb.europa.eu/paym/groups/pdf/omg/2023/230620/item\_2\_T\_1\_Overview.pdf](https://www.ecb.europa.eu/paym/groups/pdf/omg/2023/230620/item_2_T_1_Overview.pdf)  
24. Efficient Netting & Settlement with CNS \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/clearing-and-settlement-services/equities-clearing-services/cns](https://www.dtcc.com/clearing-and-settlement-services/equities-clearing-services/cns)  
25. Understanding Settlement Cycles: What Does T+1 Mean for You? | FINRA.org, accessed on February 3, 2026, [https://www.finra.org/investors/insights/understanding-settlement-cycles](https://www.finra.org/investors/insights/understanding-settlement-cycles)  
26. NATIONAL SECURITIES CLEARING CORPORATION RULES & PROCEDURES \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/\~/media/files/downloads/legal/rules/nscc\_rules.pdf](https://www.dtcc.com/~/media/files/downloads/legal/rules/nscc_rules.pdf)  
27. Understanding the DTCC Subsidiaries Settlement Process, accessed on February 3, 2026, [https://www.dtcc.com/understanding-settlement/index.html](https://www.dtcc.com/understanding-settlement/index.html)  
28. SR 2025 \- \* 013 \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/Globals/PDFs/2025/September/05/SR-NSCC-2025-013](https://www.dtcc.com/Globals/PDFs/2025/September/05/SR-NSCC-2025-013)  
29. Order Approving of Proposed Rule Change to Amend the CNS Fails Charge in the NSCC Rules \- SEC.gov, accessed on February 3, 2026, [https://www.sec.gov/files/rules/sro/nscc/2025/34-104270.pdf](https://www.sec.gov/files/rules/sro/nscc/2025/34-104270.pdf)  
30. Self-Regulatory Organizations; National Securities Clearing Corporation; Notice of Filing of Proposed Rule Change To Amend the CNS Fails Charge in the NSCC Rules \- Federal Register, accessed on February 3, 2026, [https://www.federalregister.gov/documents/2025/09/16/2025-17815/self-regulatory-organizations-national-securities-clearing-corporation-notice-of-filing-of-proposed](https://www.federalregister.gov/documents/2025/09/16/2025-17815/self-regulatory-organizations-national-securities-clearing-corporation-notice-of-filing-of-proposed)  
31. Notice of Filing of Proposed Rule Change to Amend the CNS Fails Charge in the NSCC Rules \- SEC.gov, accessed on February 3, 2026, [https://www.sec.gov/files/rules/sro/nscc/2025/34-103952.pdf](https://www.sec.gov/files/rules/sro/nscc/2025/34-103952.pdf)  
32. Important Notice National Securities Clearing Corporation \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/-/media/Files/pdf/2025/12/1/a9687.pdf](https://www.dtcc.com/-/media/Files/pdf/2025/12/1/a9687.pdf)  
33. 240.15c3-1 Net capital requirements for brokers or dealers. \- Office of Financial Regulation, accessed on February 3, 2026, [https://flofr.gov/docs/default-source/documents/69w-200-00258.pdf?sfvrsn=6ba6748c\_1](https://flofr.gov/docs/default-source/documents/69w-200-00258.pdf?sfvrsn=6ba6748c_1)  
34. SEA Rule 15c3-1 and Related Interpretations | FINRA.org, accessed on February 3, 2026, [https://www.finra.org/rules-guidance/guidance/interpretations-financial-operational-rules/sea-rule-15c3-1-and-related-interpretations](https://www.finra.org/rules-guidance/guidance/interpretations-financial-operational-rules/sea-rule-15c3-1-and-related-interpretations)  
35. 17 CFR § 242.204 \- Close-out requirement. \- Cornell Law School, accessed on February 3, 2026, [https://www.law.cornell.edu/cfr/text/17/242.204](https://www.law.cornell.edu/cfr/text/17/242.204)  
36. Key Points About Regulation SHO \- SEC.gov, accessed on February 3, 2026, [https://www.sec.gov/investor/pubs/regsho.htm](https://www.sec.gov/investor/pubs/regsho.htm)  
37. The Essentials \- Reg SHO Compliance | Oyster Consulting, accessed on February 3, 2026, [https://www.oysterllc.com/what-we-think/the-essentials-reg-sho-compliance/](https://www.oysterllc.com/what-we-think/the-essentials-reg-sho-compliance/)  
38. Exhibit 5 \- SEC.gov, accessed on February 3, 2026, [https://www.sec.gov/files/rules/sro/nscc/2018/34-84259-ex5.pdf](https://www.sec.gov/files/rules/sro/nscc/2018/34-84259-ex5.pdf)  
39. Self-Regulatory Organizations; National Securities Clearing Corporation; Notice of Filing and Immediate Effectiveness of a Proposed Rule Change To Clarify the Rules That Describe the Buy-In Process \- Federal Register, accessed on February 3, 2026, [https://www.federalregister.gov/documents/2018/09/27/2018-20997/self-regulatory-organizations-national-securities-clearing-corporation-notice-of-filing-and](https://www.federalregister.gov/documents/2018/09/27/2018-20997/self-regulatory-organizations-national-securities-clearing-corporation-notice-of-filing-and)  
40. 11810\. Buy-In Procedures and Requirements | FINRA.org, accessed on February 3, 2026, [https://www.finra.org/rules-guidance/rulebooks/finra-rules/11810](https://www.finra.org/rules-guidance/rulebooks/finra-rules/11810)  
41. Obligation Warehouse Overview \- DTCC Learning Center, accessed on February 3, 2026, [https://dtcclearning.com/products-and-services/equities-clearing/obligation-warehouse/1765-ow-overview/8542-ow-overview.html](https://dtcclearning.com/products-and-services/equities-clearing/obligation-warehouse/1765-ow-overview/8542-ow-overview.html)  
42. Obligation Warehouse Users \- DTCC Learning Center, accessed on February 3, 2026, [https://dtcclearning.com/products-and-services/equities-clearing/obligation-warehouse/ow-users.html](https://dtcclearning.com/products-and-services/equities-clearing/obligation-warehouse/ow-users.html)  
43. Important Notice National Securities Clearing Corporation \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/-/media/Files/pdf/2025/11/17/a9676.pdf](https://www.dtcc.com/-/media/Files/pdf/2025/11/17/a9676.pdf)  
44. Transforming the Processing of Fails & Other Open Obligations \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/-/media/Files/Downloads/Bylined-Articles/SCosgrove\_Fails\_Obligations.pdf](https://www.dtcc.com/-/media/Files/Downloads/Bylined-Articles/SCosgrove_Fails_Obligations.pdf)  
45. Securities Transactions Settlement \- SEC.gov, accessed on February 3, 2026, [https://www.sec.gov/rules-regulations/2004/03/securities-transactions-settlement](https://www.sec.gov/rules-regulations/2004/03/securities-transactions-settlement)  
46. 17 CFR § 240.15c3-1 \- Net capital requirements for brokers or dealers., accessed on February 3, 2026, [https://www.law.cornell.edu/cfr/text/17/240.15c3-1](https://www.law.cornell.edu/cfr/text/17/240.15c3-1)  
47. Self-Regulatory Organizations; National Securities Clearing Corporation; Order Approving of Proposed Rule Change To Amend the CNS Fails Charge in the NSCC Rules \- Federal Register, accessed on February 3, 2026, [https://www.federalregister.gov/documents/2025/12/01/2025-21645/self-regulatory-organizations-national-securities-clearing-corporation-order-approving-of-proposed](https://www.federalregister.gov/documents/2025/12/01/2025-21645/self-regulatory-organizations-national-securities-clearing-corporation-order-approving-of-proposed)  
48. T+1 SECURITIES SETTLEMENT INDUSTRY IMPLEMENTATION PLAYBOOK \- Investment Company Institute, accessed on February 3, 2026, [https://www.ici.org/files/2022/22-ppr-t1-playbook.pdf](https://www.ici.org/files/2022/22-ppr-t1-playbook.pdf)  
49. Settlement Fails \- SIX Group, accessed on February 3, 2026, [https://www.six-group.com/en/blog/settlement-fails.html](https://www.six-group.com/en/blog/settlement-fails.html)  
50. Settlement fails: Getting to the root of the problem \- Swift, accessed on February 3, 2026, [https://www.swift.com/news-events/news/settlement-fails-getting-root-problem](https://www.swift.com/news-events/news/settlement-fails-getting-root-problem)  
51. How Same-Day Settlement Works at DTCC, accessed on February 3, 2026, [https://www.dtcc.com/dtcc-connection/articles/2021/april/19/ask-the-expert-same-day-every-day-how-same-day-settlement-works-at-dtcc](https://www.dtcc.com/dtcc-connection/articles/2021/april/19/ask-the-expert-same-day-every-day-how-same-day-settlement-works-at-dtcc)  
52. SR-NSCC-2025-011 \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/-/media/Files/Downloads/legal/rule-filings/2025/NSCC/SR-NSCC-2025-011.pdf](https://www.dtcc.com/-/media/Files/Downloads/legal/rule-filings/2025/NSCC/SR-NSCC-2025-011.pdf)  
53. Federal Register/Vol. 83, No. 188/Thursday, September 27, 2018/Notices \- GovInfo, accessed on February 3, 2026, [https://www.govinfo.gov/content/pkg/FR-2018-09-27/pdf/2018-20997.pdf](https://www.govinfo.gov/content/pkg/FR-2018-09-27/pdf/2018-20997.pdf)  
54. Inventory Management System (IMS) \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/clearing-and-settlement-services/settlement/inventory-management-system](https://www.dtcc.com/clearing-and-settlement-services/settlement/inventory-management-system)  
55. FINRA \- SEA Rule 15c3-1 (a), accessed on February 3, 2026, [https://www.finra.org/sites/default/files/SEA.Rule\_.15c3-1.Interpretations.pdf](https://www.finra.org/sites/default/files/SEA.Rule_.15c3-1.Interpretations.pdf)  
56. Regulation SHO – Bona Fide Market Making and Close-Out Requirements | FINRA.org, accessed on February 3, 2026, [https://www.finra.org/rules-guidance/guidance/reports/2025-finra-annual-regulatory-oversight-report/regulation-sho](https://www.finra.org/rules-guidance/guidance/reports/2025-finra-annual-regulatory-oversight-report/regulation-sho)  
57. SEC Announces Short Sale Rule Changes and Initiatives, accessed on February 3, 2026, [https://corpgov.law.harvard.edu/2009/08/09/sec-announces-short-sale-rule-changes-and-initiatives/](https://corpgov.law.harvard.edu/2009/08/09/sec-announces-short-sale-rule-changes-and-initiatives/)  
58. Self-Regulatory Organizations; National Securities Clearing Corporation; Order Approving of Proposed Rule Change To Accommodate a Shorter Standard Settlement Cycle and Make Other Changes \- Federal Register, accessed on February 3, 2026, [https://www.federalregister.gov/documents/2024/05/08/2024-10001/self-regulatory-organizations-national-securities-clearing-corporation-order-approving-of-proposed](https://www.federalregister.gov/documents/2024/05/08/2024-10001/self-regulatory-organizations-national-securities-clearing-corporation-order-approving-of-proposed)  
59. Continuous Net Settlement (CNS) | IBKR Glossary, accessed on February 3, 2026, [https://www.interactivebrokers.com/campus/glossary-terms/continuous-net-settlement-cns/](https://www.interactivebrokers.com/campus/glossary-terms/continuous-net-settlement-cns/)  
60. US T+1 Settlement \- FAQs \- AFME, accessed on February 3, 2026, [https://www.afme.eu/publications/position-papers/us-tplus1-settlement-faqs/](https://www.afme.eu/publications/position-papers/us-tplus1-settlement-faqs/)  
61. 17 CFR 240.15c3-1 \-- Net capital requirements for brokers or dealers. \- eCFR, accessed on February 3, 2026, [https://www.ecfr.gov/current/title-17/chapter-II/part-240/subpart-A/subject-group-ECFR541343e5c1fa459/section-240.15c3-1](https://www.ecfr.gov/current/title-17/chapter-II/part-240/subpart-A/subject-group-ECFR541343e5c1fa459/section-240.15c3-1)  
62. The ICMA Buy-in Rules, accessed on February 3, 2026, [https://www.icmagroup.org/assets/ICMA\_Buy-in-Rules\_Webinar\_September-2023.pdf](https://www.icmagroup.org/assets/ICMA_Buy-in-Rules_Webinar_September-2023.pdf)  
63. SEC Rule 204 of Regulation SHO \- Jefferies, accessed on February 3, 2026, [https://www.jefferies.com/CMSFiles/Jefferies.com/Files/Policies/regsho.pdf](https://www.jefferies.com/CMSFiles/Jefferies.com/Files/Policies/regsho.pdf)  
64. CNS® \- DTCC Learning Center, accessed on February 3, 2026, [https://dtcclearning.com/products-and-services/equities-clearing/cns.html](https://dtcclearning.com/products-and-services/equities-clearing/cns.html)  
65. Proposed Rule: Shortening the Securities Transaction Settlement Cycle \- SEC.gov, accessed on February 3, 2026, [https://www.sec.gov/files/rules/proposed/2022/34-94196.pdf](https://www.sec.gov/files/rules/proposed/2022/34-94196.pdf)  
66. T+1 FAQ \- Brown Brothers Harriman, accessed on February 3, 2026, [https://www.bbh.com/us/en/insights/investor-services-insights/t-1-faq.html](https://www.bbh.com/us/en/insights/investor-services-insights/t-1-faq.html)