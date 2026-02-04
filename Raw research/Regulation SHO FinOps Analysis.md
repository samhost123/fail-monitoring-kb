# **Operationalizing Regulation SHO: A Comprehensive Financial and Settlement Analysis in the T+1 Era**

## **Executive Summary: The Convergence of Regulation and Financial Operations**

The landscape of United States equity settlement is defined by a rigid regulatory architecture designed to ensure the prompt and accurate exchange of ownership. At the heart of this architecture lies Regulation SHO, a set of rules established by the Securities and Exchange Commission (SEC) to address failures to deliver (FTDs) and curb abusive short selling practices. While often categorized as a compliance obligation, Regulation SHO functions as a primary driver of Financial Operations (FinOps) strategy, dictating capital allocation, liquidity management, and daily operational workflows.  
With the industry's transition to a T+1 settlement cycle in May 2024, the operational buffers that previously allowed for the manual resolution of settlement exceptions have evaporated. The "Part 3" framework of the settlement lifecycle—specifically the imperative of close-outs under Rule 204 and the management of Threshold Securities under Rule 203—has evolved from a regulatory backstop into a real-time operational constraint. For the modern broker-dealer, the cost of a settlement fail is no longer just a regulatory risk; it is a quantifiable financial liability, manifesting through Continuous Net Settlement (CNS) fails charges, increased margin requirements, and punitive Net Capital deductions.  
This report provides an exhaustive analysis of Regulation SHO through the lens of FinOps and day-to-day settlement mechanics. It dissects the operational timelines of Rule 204, the economic consequences of the "penalty box," the intricate accounting of the CNS system, and the capital implications of aged fails under SEC Rule 15c3-1. By integrating regulatory mandates with operational reality, this document serves as a foundational text for understanding the financial engineering required to maintain settlement integrity in the modern market.

## **I. The Regulatory Architecture of Delivery: Genesis and Evolution of Regulation SHO**

To understand the current FinOps pressures surrounding settlement, one must first deconstruct the regulatory evolution that transformed the "fail to deliver" from a market nuisance into a critical compliance violation. Regulation SHO was adopted in 2005 to update short sale regulation, but its most significant operational components—the "hard" close-out requirement—emerged from the liquidity crises of 2008\.

### **The Shift from Rule 204T to Permanent Rule 204**

The contemporary settlement discipline regime is rooted in the transition from temporary Rule 204T to the permanent Rule 204 in July 2009\. Prior to this shift, the regulatory framework allowed for greater flexibility in managing fails, particularly for market makers and in non-threshold securities. The financial crisis, however, exposed the systemic risks associated with "naked" short selling—the practice of selling securities without borrowing them—which could artificially depress stock prices and destabilize financial institutions.  
In response, the SEC implemented Rule 204 to impose a strict "close-out" requirement on *all* equity securities, regardless of their status as threshold securities. This shift fundamentally altered the operational relationship between the broker-dealer and the National Securities Clearing Corporation (NSCC). It moved the industry from a "locate-centric" model, where the primary check was at the time of trade, to a "delivery-centric" model, where the failure to deliver triggers immediate and non-negotiable market action.  
For FinOps teams, this evolution effectively monetized the settlement timeline. Every hour past the settlement date now carries an increasing probability of forced market action (buy-ins), borrowing costs, and regulatory penalties. The permanent nature of Rule 204 institutionalized the concept that settlement finality is not just a goal but a requirement for continued market participation.

### **The Scope of Regulation SHO in Daily Operations**

Regulation SHO is not a monolithic rule; it is a tripartite framework that intersects with different stages of the trade lifecycle:

1. **Rule 200 (Marking):** Dictates how orders are characterized (Long, Short, Short Exempt) at the point of entry. FinOps systems must ensure that these markers are accurate, as they determine the downstream logic for close-outs and capital charges.  
2. **Rule 203 (Locate and Threshold):** Governs the sourcing of inventory prior to trade (the "locate") and the management of persistent fails in "Threshold Securities." This rule imposes the 13-day mandatory close-out, creating a "hard stop" for aged fails.  
3. **Rule 204 (Close-Out):** The operational engine of the regulation, mandating the T+1 (now S+1) and S+3 close-out timelines for short and long sales, respectively.

The interaction between these rules creates a complex decision matrix for operations managers. A fail is not simply a "fail"; it is a specific *type* of fail (short vs. long, market maker vs. proprietary) that triggers a specific sequence of regulatory and financial obligations.

## **II. Rule 204: The Operational Mechanics of the Hard Close-Out**

Rule 204 constitutes the primary operational constraint for settlement teams. It mandates that a participant of a registered clearing agency must deliver securities by the settlement date. If a delivery failure occurs, the rule imposes a mandatory "close-out" requirement that overrides normal trading discretion.

### **The Anatomy of the Close-Out Timeline**

The FinOps workflow for Rule 204 is governed by strict chronological deadlines relative to the settlement date (S). With the compression to T+1, these deadlines have become extremely tight, requiring automated "sweeps" of fail positions and rapid decision-making by stock loan and trading desks.

#### **1\. The Short Sale Fail (S+1 Deadline)**

The most aggressive timeline applies to fails resulting from short sales. The regulation assumes that a short seller should have secured a borrow *prior* to execution (the locate). Therefore, a failure to deliver on settlement date is treated as a potential "naked" short.

* **The Mandate:** The participant must close out the fail position by purchasing or borrowing securities of like kind and quantity.  
* **The Deadline:** This action must occur by **no later than the beginning of regular trading hours** (9:30 AM ET) on the settlement day following the settlement date.  
* **T+1 Operational Flow:**  
  * **Trade Date (T):** Execution.  
  * **Settlement Date (S/T+1):** The trade fails to settle in the CNS night or day cycle.  
  * **Close-Out Date (S+1/T+2):** The firm must execute a buy-in or secure a borrow before market open.

This S+1 deadline creates a "morning scramble" for operations teams. If the CNS night cycle (which runs the evening of S) fails to allocate shares, the firm has only a few hours before the market opens on S+1 to resolve the deficit.

#### **2\. The Long Sale Fail (S+3 Deadline)**

Fails resulting from long sales are treated with slightly more leniency, acknowledging that they often stem from operational friction (e.g., delay in retrieving physical certificates, restricted stock legends) rather than manipulative intent.

* **The Mandate:** The participant must close out the fail by purchasing or borrowing securities.  
* **The Deadline:** By the beginning of regular trading hours on the **third consecutive settlement day** following the settlement date.  
* **Operational Note:** While the timeline is longer, the financial liability (capital charges) continues to accrue. FinOps teams must weigh the cost of borrowing stock to cure the fail earlier against the risk of waiting for the S+3 deadline.

#### **3\. The Market Maker Exception (S+3 Deadline)**

Rule 204(a)(3) provides an exception for fails attributable to "bona fide market making" activities.

* **The Mandate:** Similar to the long sale timeline, market makers have until the beginning of regular trading hours on the third consecutive settlement day following the settlement date to close out.  
* **FinOps Constraint:** To rely on this exception, the firm must be able to demonstrate that the fail was a direct result of bona fide market making. This requires robust tagging in the order management system (OMS) to differentiate market making flow from speculative proprietary trading. If a fail is misclassified, the firm risks violating the S+1 deadline for short sales, leading to "penalty box" restrictions.

| Transaction Type | Fail Cause | Close-Out Deadline (Relative to Settlement) | Permitted Resolution |
| :---- | :---- | :---- | :---- |
| **Short Sale** | Lack of Inventory / Failed Borrow | S+1 (Market Open) | Purchase or Borrow |
| **Long Sale** | Operational Delay / Physical Certs | S+3 (Market Open) | Purchase or Borrow |
| **Market Maker** | Bona Fide Market Making Activity | S+3 (Market Open) | Purchase or Borrow |
| **Deemed to Own** | Rule 144 / Restricted Securities | T+35 (Calendar Days) | Purchase Only |

### **The "Cleared and Settled" Requirement**

A critical nuance of Rule 204 that impacts FinOps is the requirement that the close-out action must result in a "cleared and settled" trade. It is not enough to simply execute a buy order; the shares from that buy order must actually be delivered to the clearing agency.

* **Implication:** If a firm executes a buy-in to close out a fail, and that buy-in trade *also* fails to settle, the firm has not satisfied Rule 204\. This recursive risk forces FinOps teams to prioritize buy-ins with reliable counterparties or to utilize "Guaranteed Delivery" mechanisms where available.

### **ETF Conversion and Operational Relief**

Operational guidance has evolved to address specific instrument types. For example, firms may use Exchange Traded Fund (ETF) conversion activity to meet the purchase requirement of Rule 204 under certain circumstances (detailed in a 2017 SEC No-Action Letter). This allows a firm to create or redeem ETF units to satisfy a delivery obligation, providing a liquidity valve for market makers dealing with hard-to-borrow component stocks. However, this relief is strictly limited to ETFs and does not extend to American Depositary Receipt (ADR) conversions.

## **III. The Penalty Box: Operational Friction and Economic Costs**

The most feared operational consequence of Regulation SHO is the "Penalty Box"—the restriction imposed under Rule 204(b) for failing to comply with the close-out requirements. This is not merely a fine; it is a functional blockade on a firm's ability to trade a specific security.

### **The Mechanics of the Pre-Borrow Restriction**

If a participant fails to close out a fail position by the required deadline, Rule 204(b) mandates:

* The participant (and any broker-dealer for which it clears) may not accept a short sale order in the equity security from another person, or effect a short sale in the equity security for its own account.  
* **Unless:** The participant has first **borrowed** or entered into a **bona fide arrangement to borrow** the security.

This shifts the requirement from a "locate" (reasonable belief) to a "pre-borrow" (hard confirmation).

### **Operational Impact on Day-to-Day Trading**

For a high-frequency trading desk or a prime brokerage client, the pre-borrow requirement introduces significant latency and friction:

1. **Execution Delay:** Standard short sales are executed in milliseconds based on automated locate lists. A pre-borrow requires the stock loan desk to physically secure the shares before the order can be routed. This delay often negates the alpha of the trade.  
2. **Systemic Blocks:** Order Management Systems (OMS) must be configured to automatically reject short orders in "penalty box" securities unless a special "pre-borrow" flag is attached. This requires continuous synchronization between the settlement system (which identifies the penalty) and the trading engine.  
3. **Client Impact:** If a clearing firm enters the penalty box due to the actions of one client, *all* clients clearing through that firm may be subject to the pre-borrow restriction for that security. This creates significant reputational risk and can lead to clients migrating to other clearing firms.

### **The Economic Cost of the Pre-Borrow**

The financial difference between a "locate" and a "pre-borrow" is substantial and directly impacts the profitability of the FinOps function:

* **Locate Cost:** Often nominal or zero for "Easy-to-Borrow" (ETB) securities. The firm simply tags the order against an available inventory list.  
* **Pre-Borrow Cost:** Requires the firm to enter into a stock loan contract immediately. This incurs:  
  * **Borrow Fees:** The annualized interest rate charged on the collateral (or the fee paid for non-cash collateral). For "Hard-to-Borrow" (HTB) stocks, this can range from 10% to over 100% APR.  
  * **Execution Fees:** Many prime brokers and stock loan conduits charge a per-ticket fee (e.g., $20 \- $50) for processing manual pre-borrows.  
  * **Cost of Carry:** The firm must post collateral (typically 102% of the market value) immediately, tying up liquidity that could be deployed elsewhere.  
  * **Utilization Risk:** If the firm pre-borrows stock but the trader decides not to execute the short sale (or the price moves away), the firm is still liable for the borrowing fees and the cost of returning the unused stock.

## **IV. The Financial Operations of Settlement: CNS, Margin, and Liquidity**

Beyond the specific mandates of Reg SHO, the day-to-day settlement process is governed by the financial architecture of the National Securities Clearing Corporation (NSCC). A settlement fail is a liability on the balance sheet of the broker-dealer, and the NSCC manages this risk through a sophisticated regime of charges and margin requirements.

### **The Continuous Net Settlement (CNS) System**

CNS is the primary engine for clearing equity trades. It nets all obligations for a specific CUSIP into a single long or short position per member per day. This "netting" is the first line of defense against fails, as it reduces the total number of physical movements required.

* **Novation:** Through novation, the NSCC becomes the counterparty to every trade. This guarantees the trade, meaning that if Member A fails to deliver to Member B, the NSCC is still obligated to deliver to Member B (assuming Member B is long in the net).  
* **Accounting Cycles:** FinOps teams must manage inventory across two distinct cycles:  
  1. **Night Cycle:** Processes \~50% of volume. Uses exemptions and priority groups to allocate shares available in DTC accounts.  
  2. **Day Cycle:** Continuously attempts to settle remaining open positions as new inventory arrives (e.g., from stock loan returns or incoming deliveries).

### **The CNS Fails Charge: The Cost of Liquidity**

To discourage members from using the CNS system as a cheap financing facility (i.e., failing to deliver because it's cheaper than borrowing), the NSCC imposes a "CNS Fails Charge."

* **Historical Model:** Previously, this charge was calculated based on the member's credit rating (CRRM). Lower-rated members paid higher penalties.  
* **New "Aging" Methodology (2025):** The methodology has shifted to focus on the **duration** of the fail. The charge is now calculated by multiplying the Current Market Value (CMV) of the fail by a percentage that escalates the longer the fail remains open.  
  * *Strategic Implication:* FinOps managers must prioritize the resolution of the *oldest* fails to minimize this expense. A fail that ages past S+1 becomes progressively more expensive, creating a nonlinear cost curve.  
  * **Removal of Long Position Charge:** The new rules discontinued the charge on "Long Positions" (failed receives), correctly identifying that the receiving member is the victim, not the perpetrator, of the fail.

### **Margin Requirements and the Clearing Fund**

A fail-to-deliver increases the firm's contribution to the NSCC Clearing Fund. This is a direct drain on the firm's working capital.

1. **Mark-to-Market (MtM):** Fails are marked to market daily. If the price of the security rises, the failing member (who is short) must post additional cash collateral to cover the difference between the contract price and the current market price.  
   * *FinOps Risk:* In a "short squeeze," the price of the failing security can skyrocket. The MtM debits can drain the firm's liquidity reserves, potentially triggering a net capital crisis (as seen in the GameStop event).  
2. **Value-at-Risk (VaR):** The NSCC uses a VaR model to calculate the potential future exposure of the portfolio. Open fails increase the volatility profile of the portfolio, leading to higher VaR charges.  
3. **Margin Requirement Differential (MRD):** A charge to cover the risk of price fluctuations between the calculation of the margin and the actual liquidation of the position.

| Financial Component | FinOps Impact of a Fail |
| :---- | :---- |
| **CNS Fails Charge** | Direct expense; escalates with the age of the fail. |
| **Mark-to-Market** | Liquidity drain; requires daily cash posting if stock price rises. |
| **VaR Margin** | Increases collateral requirement; reduces free capital. |
| **Corporate Actions** | Liability for missed dividends or voting rights; manual claims processing. |

## **V. Regulatory Capital: Rule 15c3-1 and the Cost of Aged Fails**

While NSCC charges are operational costs, SEC Rule 15c3-1 (the Net Capital Rule) poses an existential threat to the broker-dealer. This rule requires firms to maintain a minimum level of liquid capital to protect investors. Settlement fails directly attack this liquidity buffer through "Aged Fail" deductions.

### **The "Aged Fail" Haircut**

Under Rule 15c3-1, a fail-to-deliver is considered a receivable (an asset). However, because the counterparty has failed to pay (delivery versus payment), this asset is viewed as risky.

* **The Clock:** The regulatory clock for capital deductions starts on the settlement date.  
* **S+5 Deduction:** For most equity securities, if a fail remains outstanding for **5 business days** (S+5), the firm must apply a "haircut" (deduction) to its Net Worth.  
* **Calculation:** The deduction is typically equal to the haircut percentage applicable to the underlying security (e.g., 15% for most equities) applied to the market value of the fail.  
* **Mark-to-Market Loss:** Additionally, if the market value of the security exceeds the contract price (the firm is losing money on the short), 100% of that unrealized loss is deducted immediately.

### **FinOps Strategy: Moment-to-Moment Compliance**

FinOps teams must demonstrate "moment-to-moment" compliance with the Net Capital Rule. This means that if a massive fail occurs intraday that would breach the capital requirement, the firm must cease operations or infuse capital immediately.

* **T+1 Pressure:** In the T+1 environment, the window between S+1 (Reg SHO deadline) and S+5 (Capital deduction) is compressed. However, the S+1 mandatory close-out under Rule 204 is designed to prevent fails from ever reaching the S+5 "aged" status.  
* **The Regulatory Cliff:** If a firm fails to close out under Rule 204 (S+1) *and* fails to resolve the position by S+5, it faces a "double jeopardy": operational restrictions from Reg SHO (Penalty Box) and capital degradation from Rule 15c3-1.

### **Municipal Securities Nuance**

For municipal securities brokers' brokers, the timeline is extended. The deduction applies to fails outstanding for **21 business days** or longer. The deduction is 1% of the contract value, plus any excess of the contract price over market value. This reflects the lower liquidity and settlement nuances of the municipal bond market compared to equities.

## **VI. Threshold Securities and Rule 203: Managing Systemic Persistence**

While Rule 204 handles the daily flow of fails, Rule 203(b)(3) addresses "Threshold Securities"—those issues where fails have become a persistent, systemic problem.

### **Identifying Threshold Securities**

A security becomes a "Threshold Security" if:

1. There is an aggregate fail-to-deliver position of 10,000 shares or more.  
2. This fail position equals at least 0.5% of the issuer's total shares outstanding.  
3. These conditions persist for **five consecutive settlement days**.

FinOps teams must download the daily Threshold Lists from SROs (e.g., NASDAQ, NYSE) and cross-reference them with their internal "Hard-to-Borrow" lists.

### **The 13-Day Mandatory Close-Out**

Rule 203 imposes a definitive backstop for threshold securities. If a participant has a fail-to-deliver position in a threshold security for **13 consecutive settlement days**, the participant must immediately close out the position by purchasing shares of like kind and quantity.

* **No Borrowing:** Unlike Rule 204, which allows borrowing to close out, Rule 203 strictly requires a **purchase**. This is to force a reduction in the "phantom" supply of shares.  
* **Trading Restriction:** Until the position is closed out, the participant may not accept any short sale orders in that security without a pre-borrow.

### **Operational Workflow for Threshold Management**

1. **Daily Screening:** Automated scan of the SRO Threshold List against the firm's open fail positions.  
2. **Aging Analysis:** Tracking the "age" of fails in threshold securities. Alerts are typically set at Day 10 to give the stock loan desk 72 hours to source the buy-in.  
3. **Buy-In Execution:** On Day 13, if the fail persists, the OMS automatically generates a "Buy-In" order. This order is marked for guaranteed delivery if possible.  
4. **Cooling Off:** A security is removed from the list only after it fails to meet the threshold criteria for five consecutive settlement days.

## **VII. Operational Strategies: Buy-Ins, Stock Borrow, and Reclaims**

To navigate this minefield of regulations and costs, FinOps teams utilize a suite of operational mitigation strategies.

### **1\. The Stock Borrow Program (SBP)**

The most efficient way to prevent a CNS fail is to utilize the NSCC's Stock Borrow Program.

* **Mechanism:** Members with excess inventory (long positions) can enroll in the SBP. During the night cycle, the NSCC algorithms can "borrow" these shares to satisfy the delivery obligations of failing members.  
* **Benefit:** The failing member effectively "borrows" the stock from the CCP rather than failing to the street. This masks the fail from the receiving counterparty, preserving settlement finality.  
* **FinOps Cost:** The failing member pays a fee for this service, but it avoids the "Penalty Box" and potential buy-ins.

### **2\. Partial Settlement**

Historically, settlement was binary: you delivered all shares or none. The introduction of **Partial Settlement** allows the system to settle whatever portion of the obligation is supported by inventory.

* **Example:** Obligation to deliver 1,000 shares; inventory is 600 shares.  
* **Result:** 600 shares settle; 400 shares fail.  
* **Impact:** This reduces the *value* of the fail, which lowers the CNS Fails Charge and the Net Capital deduction. It maximizes the velocity of collateral through the system.

### **3\. Reclaims vs. Recalls**

* **Reclaim:** Used to correct a delivery error (e.g., wrong CUSIP). This is an operational reversal. In T+1, the window for reclaims is extremely narrow; they typically must be processed on the same day as the erroneous delivery.  
* **Recall:** A lender demands the return of loaned securities (usually to vote proxies or sell the shares). In T+1, the **Recall Timeline** is critical. If a lender sells shares that are out on loan, they must issue a recall *immediately*. The borrower has until the settlement date of the sale (S+1) to return the shares. If they fail, the lender will fail on their sale, triggering a Rule 204 obligation.

### **4\. Buy-In Execution: NSCC vs. Bilateral**

When automated mitigation fails, the firm must execute a buy-in.

* **NSCC Buy-In (Rule 11):** For CNS-eligible securities. The long member submits a "Buy-In Intent." This elevates their priority in the allocation algorithm (Priority Group 2), essentially allowing them to "jump the queue" for incoming shares. If shares are still not received, the NSCC transmits the buy-in liability to the member with the oldest short position.  
* **FINRA Buy-In (Rule 11810):** For ex-clearing (bilateral) trades. This is a manual process requiring written notice delivered to the seller by 12:00 noon ET, two business days before the proposed execution. In the T+1 world, this "T-2" notice period is operationally challenging, often effectively extending the resolution timeline beyond the T+1 settlement goal.

## **VIII. The Economic Calculus of Fails: A FinOps Decision Matrix**

Operations managers make real-time decisions based on the "Cost of Carry" for a fail. The decision to Borrow, Buy-In, or Fail is a mathematical calculation.

### **The Cost Equation**

$Cost\_{Fail} \= (Charge\_{CNS}) \+ (Cost\_{Capital}) \+ (Risk\_{PenaltyBox}) \+ (Margin\_{MRD})$  
vs.  
$Cost\_{Borrow} \= (Rate\_{StockLoan} \\times Price\_{Share}) \+ (Fee\_{Ticket})$

### **Decision Logic**

1. **High-Cost Borrow (HTB):** If the stock borrow rate is 50% APR, the daily cost of borrowing is high. A firm might be tempted to fail if the CNS penalty is lower. However, Rule 204 *prohibits* intentional failing. The "Penalty Box" risk (inability to trade) usually outweighs the borrow cost.  
2. **Low-Cost Borrow (GC):** For General Collateral stocks (rates \< 0.5%), there is no economic rationale to fail. Automation should aggressively borrow to cover.  
3. **Illiquid Securities:** If no borrow is available and the stock is illiquid, the firm must execute a buy-in. The FinOps team must calculate the "market impact" of the buy-in—driving the price up against themselves—versus the regulatory risk of the fail.

## **IX. Future Outlook: T+0 and the End of the Buffer**

The transition to T+1 is likely a stepping stone to **T+0 (Same-Day Settlement)**. In a T+0 environment, the distinction between "Trade" and "Settlement" vanishes.

* **Real-Time Gross Settlement (RTGS):** The netting benefits of CNS would be diminished, requiring firms to hold significantly higher liquidity buffers.  
* **Instant Reg SHO:** The "locate" and "delivery" would happen simultaneously. A failure to locate would result in an immediate trade failure, not a T+1 fail-to-deliver.  
* **Blockchain/DLT:** Distributed Ledger Technology could automate the "penalty box" logic via smart contracts, instantly disabling a wallet's ability to sell short upon a delivery failure.

## **Conclusion**

Operationalizing Regulation SHO in a T+1 environment requires a fundamental shift in the role of Financial Operations. FinOps is no longer a back-office function of recording and reporting; it is a front-line risk management discipline. The integration of Rule 204's hard deadlines, the punitive economics of the CNS Fails Charge, and the capital strictures of Rule 15c3-1 creates an environment where settlement efficiency is directly correlated with firm profitability.  
For the modern broker-dealer, the "Part 3" mandate—the imperative of close-outs—is the metronome of daily operations. Success requires a synthesis of automated inventory management, predictive capital planning, and a rigorous adherence to the regulatory timeline. In the unforgiving arithmetic of T+1, a fail is not just an error; it is an expensive liability that the modern market infrastructure is designed to punish with increasing severity.

## **Appendix: Structured Data and Operational Reference**

### **Table 1: Consolidated FinOps Deadlines and Capital Impacts**

| Event / Status | Regulatory Deadline | Operational Action Required | Financial Impact |
| :---- | :---- | :---- | :---- |
| **Short Sale Fail** | S+1 (Market Open) | Purchase or Borrow (Rule 204\) | CNS Fails Charge initiates. |
| **Long Sale Fail** | S+3 (Market Open) | Purchase or Borrow (Rule 204\) | Accrued interest claims; CNS charges escalate. |
| **Market Maker Fail** | S+3 (Market Open) | Purchase or Borrow (Rule 204\) | Validation of "Bona Fide" status required. |
| **Aged Fail (Capital)** | S+5 | Net Capital Deduction (Rule 15c3-1) | 15% Haircut \+ 100% of Unrealized Loss. |
| **Threshold Fail** | S+13 | Mandatory Buy-In (Rule 203\) | Buy-in at market price; loss of trading privilege. |
| **Muni Broker Fail** | S+21 | Net Capital Deduction (Rule 15c3-1) | 1% of Contract Value deduction. |
| **Rule 144 Fail** | T+35 (Calendar) | Mandatory Close-out | Long-term capital drag. |

### **Table 2: CNS Fails Charge Methodology Comparison**

| Feature | Old Methodology | New Methodology (2025) | FinOps Implication |
| :---- | :---- | :---- | :---- |
| **Basis of Charge** | Member Credit Rating (CRRM) | Age of Fail (Duration) | Incentivizes speed of resolution over member status. |
| **Long Positions** | Charge applied to failed receives | Charge discontinued | Relief for receiving members; focuses penalty on failing delivering members. |
| **Rate Structure** | Fixed % based on rating (e.g., 5-20%) | Escalating % based on days open | "Old" fails become exponentially expensive. |
| **Calculation** | $CMV \\times CRRM Rate$ | $CMV \\times Aging Factor$ | Requires daily tracking of fail vintage. |

### **Table 3: Buy-In Mechanism Comparison**

| Feature | NSCC Rule 11 (CNS) | FINRA Rule 11810 (Ex-Clearing) |
| :---- | :---- | :---- |
| **Scope** | CNS-eligible securities | Bilateral / Ex-clearing trades |
| **Trigger** | "Buy-In Intent" Notice | Written Notice to Counterparty |
| **Notice Period** | 1 Business Day (Retransmittal) | 2 Business Days (T-2 by Noon) |
| **Execution** | NSCC allocates priority; Member executes if fail persists | Buying member executes in open market |
| **Liability** | Passed to oldest short position holder | Direct counterparty liability |
| **T+1 Impact** | Highly efficient; automated allocation | Operationally difficult due to 2-day notice requirement |

