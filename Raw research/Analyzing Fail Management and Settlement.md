# **Fail Management and Mitigation Strategies in US Equity Settlement: A Comprehensive Analysis of Financial Operations and Risk Control**

The infrastructure governing the settlement of United States equity markets is a deterministic, high-velocity environment where the primary objective is the mitigation of systemic risk through the precise synchronization of ownership transfer and capital exchange. Within this ecosystem, the occurrence of a "fail to deliver" (FTD) or a "fail to receive" (FTR) constitutes a fundamental disruption to the expected trade lifecycle, creating ripples of credit risk, liquidity stress, and regulatory liability that extend far beyond the original counterparties. Consequently, fail management is not merely a back-office operational utility but a critical component of financial resource management, directly influencing a broker-dealer’s net capital standing, margin requirements, and intraday liquidity profile.1  
This analysis provides an exhaustive technical examination of Part V of the settlement workflow—Fail Management and Mitigation Strategies. It explores the operational mechanics of the Continuous Net Settlement (CNS) system's fail processing, the financial engineering behind mitigation tools like Partial Settlement and the Stock Borrow Program (SBP), and the rigorous regulatory penalties imposed by the Securities and Exchange Commission (SEC) under Regulation SHO and Rule 15c3-1. Furthermore, it integrates recent structural changes, including the 2025 revision of the CNS Fails Charge and the industry-wide transition to a T+1 settlement cycle, which have collectively compressed the temporal buffer available for exception management and heightened the cost of settlement inefficiency.3

## **I. The Operational Physics of Settlement Failure**

To comprehend the strategies employed to mitigate failure, one must first dissect the environment in which these failures occur. The primary engine of US equity settlement is the Continuous Net Settlement (CNS) system operated by the National Securities Clearing Corporation (NSCC). CNS is an automated accounting system that fundamentally alters the legal and operational nature of a securities transaction through the process of novation.1

### **The Mechanism of Novation and Netting**

At the point of trade validation, typically on T+0, the NSCC interposes itself as the central counterparty (CCP) to every eligible transaction. Through novation, the bilateral contract between a buying member and a selling member is severed and replaced by two distinct contracts: the NSCC becomes the buyer to every seller and the seller to every buyer.1 This legal transformation is the bedrock of the fail management framework because it centralizes liability. A member’s failure to deliver securities is a failure to the CCP, not to the original counterparty. This ensures that the systemic risk is contained and managed through the CCP's aggregate risk waterfall rather than propagating through a bilateral contagion chain.7  
The "Continuous" aspect of CNS refers to the perpetual netting of obligations. Unlike a trade-for-trade system where each transaction settles independently, CNS reduces all obligations for a specific CUSIP (security identifier) into a single net long (receive) or net short (deliver) position per member per day. Crucially, this netting process includes not only the new trades settling that day ("Settling Trades") but also any unsettled positions from previous days ("Closing Positions"). Therefore, a fail to deliver on settlement date (S) is not a static event; the system automatically rolls the failed position forward, netting it against the member's activity for S+1.1

### **The Lifecycle of a Failed Position**

The transition of a trade from a "pending" status to a confirmed "fail" involves a specific sequence of algorithmic checks and accounting entries. Understanding this lifecycle is essential for operations professionals ("FinOps") who must intervene at specific nodes to prevent the crystallization of capital charges.

1. **The Night Cycle Allocation (S-1 Evening):** The settlement process begins in the evening prior to the settlement date. The CNS system attempts to satisfy delivery obligations by sweeping the member's "General Free" account at The Depository Trust Company (DTC). If the member has sufficient shares, they are debited, and the delivery is effectively made to the NSCC. This is the primary window for "passive" settlement, where inventory is automatically utilized.1  
2. **The Day Cycle Allocation (Settlement Date):** If the Night Cycle fails to secure the necessary inventory (resulting in a "short" position at the start of S), the obligation moves to the Day Cycle. As the member receives securities throughout the day—whether from other settlements, stock loan returns, or deposits—the CNS system continuously attempts to "recycle" or re-process the open short position. It acts as a dynamic queue, grabbing inventory the moment it becomes available.1  
3. **End-of-Day Fail Establishment:** If, by the close of the securities processing day (typically 3:00 PM ET for value), the short position remains unsatisfied, the position is formally marked as a "CNS Fail to Deliver." At this specific boundary, the operational problem transforms into a financial liability. The fail is recorded on the member's "CNS Settlement Activity Statement," and the timeline for regulatory penalties (Reg SHO close-outs) and capital deductions (Rule 15c3-1) commences.1

The following table details the operational states of a transaction as it progresses toward failure:

| Settlement Phase | Operational State | Systemic Action | FinOps Implication |
| :---- | :---- | :---- | :---- |
| **T+0 (Trade Date)** | Trade Recording | UTC Matching / Novation | Initial Margin (VaR) calculated on net position. |
| **S-1 (Night Cycle)** | Inventory Sweep | CNS Night Allocation | Inventory in "General Free" is swept; SBP utilized if applicable. |
| **S (Day Cycle)** | Recycling | Continuous Netting | System attempts to source shares from incoming receives. |
| **S (Market Close)** | Fail Established | Mark-to-Market | Fails Charge accrual begins; "Age" counter set to Day 1\. |
| **S+1 (Morning)** | Reg SHO Close-Out | Mandatory Borrow/Buy | Firms must source inventory by market open to avoid penalty. |
| **S+5 (Aged Fail)** | Capital Deduction | 15c3-1 Charge Applied | "Aged Fail" deduction reduces Net Capital; potential leverage impact. |

1

## **II. Mitigation Strategy A: Partial Settlement Functionality**

The complexity of modern trading volumes necessitates automated solutions to prevent settlement gridlock. One of the most effective structural enhancements to the US settlement system has been the introduction and refinement of Partial Settlement Functionality. This mechanism addresses the "all-or-none" constraint that historically exacerbated fail rates.1

### **The "All-or-None" Bottleneck**

In a legacy settlement environment, delivery instructions were often binary. If a broker-dealer had an obligation to deliver 100,000 shares of a security but only held 90,000 shares in their DTC account, the entire transaction would fail. This rigidity created a cascading effect: because the receiving broker did not receive the 90,000 shares available, they, in turn, might lack the inventory to satisfy a downstream obligation to a third party. This phenomenon, known as a "daisy chain" failure, artificially inflated the volume and value of settlement fails across the street.10

### **Operational Mechanics of Partial Settlement**

Partial Settlement functionality allows the settlement engine to accept and process the portion of a delivery obligation that *is* supported by available inventory. Using the previous example, the system would identify the 90,000 shares in the deliverer's account, debit those shares, credit the receiver, and reduce the outstanding CNS obligation to 10,000 shares. The remaining 10,000 share obligation is then retained in the recycling queue for future attempts.1  
This process relies on a sophisticated set of user-defined profiles and system defaults:

* **Inventory Management System (IMS) Profiles:** Members configure their IMS profiles to determine how their inventory is utilized. A "Green" profile generally authorizes the automatic release of shares for settlement as soon as they become available, facilitating partials. A "Yellow" or "Red" profile might require manual intervention, potentially inhibiting the flow of partial deliveries.1  
* **Receiver Authorized Delivery (RAD):** While the deliverer must have inventory, the receiver must also be willing to accept a partial delivery. RAD limits allow members to set thresholds for the value or quantity of securities they will automatically accept. Systemic enhancements have increasingly automated the acceptance of partials to ensure that "stuck" inventory is moved whenever possible, provided it does not breach the receiver's risk management controls (such as the Net Debit Cap).1

### **Financial Operations Impact: Capital and Liquidity**

For the financial operations professional, partial settlement is a potent tool for balance sheet optimization. The benefits extend beyond simple operational throughput:

1. **Reduction of Capital Charges:** Under SEC Rule 15c3-1, broker-dealers must take a capital charge on "aged" fails to deliver (typically those outstanding 5 business days or longer). By allowing a trade to partially settle, the firm reduces the *notional value* of the fail. Instead of taking a capital charge on a $1 million failed trade, the firm might only face a charge on a $100,000 residual balance. This preservation of Net Capital is critical for maintaining the firm’s leverage and trading capacity.12  
2. **Liquidity Velocity:** In a T+1 environment, liquidity is premium. Partial settlement ensures that the receiving firm gets immediate possession of the available shares. These shares can then be used to satisfy that firm's own delivery obligations, effectively "unblocking" the daisy chain and reducing the aggregate level of fails in the market.5  
3. **Lower Borrowing Costs:** When a firm must borrow securities to cover a fail (to comply with Reg SHO), they pay a fee based on the quantity borrowed. Partial settlement reduces the quantity required to be borrowed, thereby directly lowering the "cost of carry" associated with the failed position.10

## **III. Mitigation Strategy B: The NSCC Stock Borrow Program (SBP)**

While partial settlement manages inventory that a firm *has*, the NSCC Stock Borrow Program (SBP) is designed to address inventory that a firm *lacks*. It is an automated facility that allows the CCP to borrow shares from members with excess inventory to satisfy the delivery needs of other members, thereby prioritizing the completion of settlement.1

### **SBP Operational Workflow**

The SBP operates primarily during the CNS Night Cycle. It is a voluntary program where members can instruct the NSCC (via specific functional codes in their IMS) that certain securities in their DTC account are available for lending.1

1. **Identification of Need:** During the night cycle allocation, the CNS algorithm identifies situations where the aggregate shares delivered by short members are insufficient to satisfy the aggregate needs of long members (receivers).  
2. **Sourcing Inventory:** The system scans the pool of securities designated as available for the SBP by potential lenders.  
3. **Automated Borrow:** If the shares are available, the NSCC automatically borrows them from the lender. The shares are debited from the lender’s account and credited to the CNS account, which then allocates them to the waiting long members.1  
4. **Collateralization:** To secure the loan, the NSCC credits the lending member’s settlement account with cash collateral equivalent to the full market value of the borrowed securities. This cash acts as a risk mitigant for the lender.8

### **The "Cure" vs. "Liability" Distinction**

A critical nuance for financial operations is understanding that the SBP does *not* cure the fail of the original short member. It creates a disconnect between the delivery and the obligation:

* **The Receiver:** Gets their shares and considers the trade settled.  
* **The Lender:** Loses possession of the shares but holds cash collateral and earns interest (the rebate rate).  
* **The Failing Member:** *Remains in a fail-to-deliver position.* The NSCC has satisfied the receiver, but the original failing member now owes the shares to the NSCC to repay the borrow. The fail persists on the books of the failing member, and they continue to accrue Fails Charges and face potential regulatory penalties.18

### **Financial Implications and Decline in Usage**

From a FinOps perspective, the SBP transforms a securities holding into a cash equivalent. The lender receives cash collateral which allows them to earn the "rebate rate"—effectively the interest paid on the cash. If the rebate rate is lower than the Federal Funds rate (which is typical for hard-to-borrow stocks), the difference represents the fee paid by the borrower.17  
However, reliance on the SBP has waned significantly, with usage dropping by nearly 95% since the mid-2000s.8 This decline is driven by the rise of more efficient, bilateral securities lending markets and, more recently, the introduction of SFT Clearing services. Modern FinOps desks often prefer to manage their lending activity explicitly rather than through the passive, automated sweep of the SBP, allowing for better rate negotiation and counterparty risk management.8

## **IV. The Evolution of Liquidity: SFT Clearing**

Recognizing the limitations of the legacy SBP and the capital constraints of bilateral lending, the NSCC introduced the Securities Financing Transaction (SFT) Clearing service. This represents the next generation of fail mitigation and liquidity management.21

### **Central Clearing of Stock Loans**

Unlike the SBP, which is an automated utility for curing CNS fails, SFT Clearing is a platform for the central clearing of overnight borrow and loan transactions. It allows members to submit bilateral securities lending transactions to the NSCC for novation. Once novated, the NSCC becomes the counterparty to both the borrower and the lender, just as it does for cash trades.23

### **Capital Efficiency and Balance Sheet Netting**

The primary driver for SFT Clearing adoption is capital efficiency. In a bilateral stock loan, a broker-dealer must hold capital against the counterparty credit risk of the borrower. By novating the trade to the NSCC:

* **Risk Weighting:** The exposure is transferred to a Qualifying Central Counterparty (QCCP), which generally attracts a significantly lower risk weighting (e.g., 2%) under Basel III capital rules compared to a bilateral counterparty.3  
* **Balance Sheet Netting:** SFTs cleared through the NSCC can be netted on the balance sheet. If a firm borrows 100 shares of IBM and lends 100 shares of IBM through the CCP, these positions can offset, reducing the gross size of the balance sheet. This is critical for banks constrained by the Supplementary Leverage Ratio (SLR).22  
* **SCCL Exemption:** Transactions cleared through a QCCP are often exempt from Single Counterparty Credit Limits (SCCL), allowing firms to execute larger volumes of financing transactions without breaching regulatory concentration limits.21

For the operations desk, SFT Clearing provides a standardized, automated mechanism to source inventory for potential fails or to finance long positions, effectively acting as a "preventative" fail management strategy that is far more capital-efficient than the reactive measures of the past.

## **V. Financial Operations: The Cost of Failing**

When mitigation strategies fail and a position remains open, the financial machinery of the settlement system imposes direct costs. These costs are designed to be punitive, incentivizing members to resolve fails quickly to minimize market risk. The two primary financial levers are the CNS Fails Charge and the Margin Requirement Differential (MRD).

### **The CNS Fails Charge: A Regime Change (2025)**

The CNS Fails Charge is a daily fee assessed on the market value of unsettled positions. Historically, this charge was calculated based on the member's credit rating (CRRM). However, effective December 2025, the NSCC implemented a radical restructuring of this fee under filing **SR-NSCC-2025-013**.3  
The new methodology shifts the focus from the *member's* creditworthiness to the *position's* duration risk. It acknowledges that a fail that persists for weeks poses a unique market risk regardless of whether the failing firm is a AAA-rated bank or a smaller broker-dealer.  
The structural changes include:

1. **Removal of Long Position Charges:** The NSCC discontinued the Fails Charge on "Long Positions" (fails to receive). This recognizes that a receiving member has limited control over whether their counterparty delivers, and penalizing the victim of a fail was operationally inequitable.3  
2. **Duration-Based Penalties:** The charge for Short Positions (fails to deliver) is now determined by a tiered schedule based on the "age" of the fail. The penalty escalates aggressively to discourage chronic failure.

**CNS Fails Charge Schedule (Effective Dec 15, 2025):**

| Age of Fail (Business Days) | Charge Percentage (of Market Value) | Strategic Implication |
| :---- | :---- | :---- |
| **1 to 4 Days** | 5% | Accommodates operational friction (e.g., physical certs). |
| **5 to 10 Days** | 15% | Escalation signal; fail is becoming "aged." |
| **11 to 20 Days** | 20% | High penalty; approximates cost of hard borrow. |
| **Over 20 Days** | 100% | Punitive; effectively requires full cash collateralization. |

4  
This 100% charge for fails exceeding 20 days is a draconian measure designed to force a "buy-in" or settlement. It effectively eliminates any economic incentive a firm might have to maintain a fail (e.g., if the cost of borrowing the stock was higher than the previous fails charge).4

### **The Margin Requirement Differential (MRD)**

While the Fails Charge looks at the *current* state of fails, the Margin Requirement Differential (MRD) looks at the *velocity* of risk in a member's portfolio. It addresses the "coverage gap" that exists between the moment a trade is guaranteed (trade date) and the moment margin is collected (settlement morning).28  
The MRD is calculated daily and added to the Clearing Fund requirement. It assesses the day-over-day fluctuation in a member's portfolio risk. Specifically, it looks at the positive changes in the **Start of Day (SOD) Volatility** and **Mark-to-Market (MTM)** components over a historical 100-day look-back period.28  
The mathematical derivation for the volatility component of the MRD ($MRD\_V$) is:

$$MRD\_V(t) \= \\sum\_{i=0}^n \\theta\_i \\times \\max\\{V(t-i, SOD) \- V(t-(i+1), SOD), 0\\}$$  
Where:

* $V(t-i, SOD)$ is the Start of Day volatility charge for day $t-i$.  
* $\\theta\_i$ is a weighting decay factor (typically 0.97).  
* The $\\max\\{..., 0\\}$ function ensures that only *increases* in volatility risk are penalized. If a portfolio becomes less risky day-over-day, the MRD contribution for that day is zero, not negative.28

This calculation ensures that a member who is rapidly increasing their risk exposure (which often precedes settlement difficulties) must pre-fund that risk. For the FinOps team, an increasing MRD is a leading indicator of portfolio stress and a signal to investigate trading activity for potential concentration or volatility risks.28

## **VI. Regulatory Capital Impact: SEC Rule 15c3-1**

Beyond the fees charged by the CCP, the most significant financial consequence of a settlement fail is the impact on a broker-dealer’s regulatory capital. SEC Rule 15c3-1, the "Net Capital Rule," mandates that firms maintain liquid assets sufficient to satisfy all obligations to customers and creditors. Fails to deliver are treated as unsecured receivables, which are not "good" assets for capital purposes.31

### **The "Aged Fail" Deduction**

Under Rule 15c3-1(c)(2)(ix), a broker-dealer must apply a deduction (a "charge") to their net worth for any fail to deliver that remains outstanding for a specified period. This is known as the "Aged Fail Deduction".12

* **Timeline:** The deduction applies to contracts outstanding **5 business days or longer** (21 business days for municipal securities).  
* **Calculation:** The deduction is based on the "haircut" that would apply to the security if it were held in the firm’s proprietary inventory (e.g., 15% for most equities).  
* **Formula:**  
  * **Base Deduction:** The standard haircut amount.  
  * **Plus:** Any excess of the contract price over the current market value (unrealized loss).  
  * **Minus:** Any excess of the current market value over the contract price (unrealized gain), limited to the amount of the haircut.12

**Example:**  
If a firm has a fail to deliver of $100,000 in a stock with a 15% haircut:

* **Scenario A (Market Flat):** Deduction \= $15,000 (15% of $100k).  
* **Scenario B (Stock Price Rises to $110,000):** The firm owes stock that is now more expensive. Deduction \= $16,500 (15% of $110k) \+ $10,000 (Loss) \= $26,500.  
* **Scenario C (Stock Price Falls to $90,000):** The firm owes stock that is cheaper. Deduction \= $13,500 (15% of $90k) \- $10,000 (Gain) \= $3,500.

This dynamic aligns the capital penalty with the market risk of the failed position. For FinOps teams, monitoring "Aged Fails" is a daily priority. A spike in aged fails can rapidly deplete excess net capital, potentially triggering reporting violations or forcing a cessation of business operations.33

### **Impact on Aggregate Indebtedness**

Fails to receive also impact the capital computation. Specifically, fails to receive that are allocated to a customer's long position (i.e., the customer bought the stock, but the street hasn't delivered it yet) are generally *excluded* from Aggregate Indebtedness (AI). This exclusion prevents the firm from being penalized for the street's failure to perform. However, credit balances in customer accounts related to short sales where the firm has failed to deliver must be carefully tracked, as they are included in AI, potentially worsening the firm's Net Capital Ratio.35

## **VII. Regulatory Enforcement: Regulation SHO**

Superimposed over the operational and financial mechanics is the legal framework of Regulation SHO. Enacted to curb abusive short selling, Reg SHO imposes strict "close-out" requirements that override standard settlement flexibility.

### **Rule 204: The Close-Out Mandate**

Rule 204 is the primary enforcement mechanism for settlement discipline. It requires that any participant of a registered clearing agency must deliver securities by the settlement date. If a fail occurs, the participant must take affirmative action to close out the position by purchasing or borrowing securities of like kind and quantity.1  
The deadlines are rigid and depend on the nature of the trade:

1. **Short Sale Fails:** Must be closed out by the beginning of regular trading hours on **S+1** (the settlement day following the settlement date).  
2. **Long Sale Fails:** If the seller owns the shares (but failed to deliver due to logistics), the close-out deadline is extended to **S+3** (three settlement days after settlement date).  
3. **Market Maker Exemption:** Fails attributable to bona fide market making also enjoy the **S+3** extension, protecting the liquidity provision function.1

### **The "Penalty Box"**

Failure to comply with Rule 204 results in the "Penalty Box" (Pre-Borrow Requirement). If a participant fails to close out an FTD by the required deadline, the participant (and any broker-dealer for which it clears) is prohibited from accepting *any* short sale order in that security from any customer, or effecting a short sale for its own account, unless it has first **borrowed** or entered into a bona fide arrangement to borrow the security.1  
This removes the ability to rely on a "locate" (a reasonable belief of availability) and forces a "hard borrow," significantly increasing transaction costs and friction. For active trading desks, entering the Penalty Box is a catastrophic operational failure that halts short-selling strategies in the affected security.1

### **Threshold Securities (Rule 203\)**

Rule 203 creates a public "shame list" for securities with chronic settlement problems. A security becomes a "Threshold Security" if it has an aggregate FTD position of 10,000 shares or more, and that position represents at least 0.5% of the issuer's total shares outstanding, for five consecutive settlement days.1  
If a fail in a Threshold Security persists for **13 consecutive settlement days**, Rule 203(b)(3) mandates an immediate, mandatory close-out. While Rule 204 usually forces action much sooner (T+1/T+3), the Threshold list serves as a backstop for persistent fails that might otherwise evade daily close-out logic (e.g., through "rolling" positions).1

## **VIII. Exception Processing and the Obligation Warehouse**

Not all fails occur within the pristine netting of CNS. A significant volume of fails resides in the bilateral world or requires manual intervention due to trade discrepancies.

### **Reclaims vs. Recalls**

Operational precision requires distinguishing between these two exception types:

* **Reclaims (Reclamations):** These are essentially "returns" of a delivery. If a member receives a delivery they do not recognize (DK) or that has the wrong quantity/money, they "reclaim" it. Systemically, this is treated as a *new* delivery instruction back to the sender. It must pass the sender's RAD limits to settle. This is an error correction mechanism.1  
* **Recalls:** These are contractual demands related to stock loans. A lender issues a recall to demand the return of loaned securities (usually to vote a proxy or sell the shares). A recall is not a settlement error; it is a notification of an impending buy-in if the shares are not returned within the standard cycle (typically T+1 or T+2).1

### **The Obligation Warehouse (OW)**

For ex-clearing trades and non-CNS securities, the Obligation Warehouse (OW) serves as the central repository. The OW tracks bilateral obligations, performs real-time matching, and handles "RECAPS" (Reconfirmation and Pricing Service).  
A vital feature of the OW is its "Rescue" mechanism. The system scans its database of bilateral fails daily. If a security that was previously ineligible for CNS becomes eligible (e.g., due to a corporate action lifting a chill), the OW automatically sends the obligation to the CNS Accounting Operation. This "rescues" the fail from the risky bilateral environment and places it under the safety of the CCP's netting and guarantee, significantly increasing the probability of settlement.1

## **IX. Strategic Outlook: Fail Management in the T+1 Era**

The transition to a T+1 settlement cycle in May 2024 has fundamentally compressed the timeline for fail management. The removal of 24 hours of processing time means that decisions previously made on T+1 must now be made on T+0.5

### **The 10:45 PM Cutoff**

Operational workflows now revolve around the **10:45 PM ET** cutoff on Trade Date (T+0). This is the deadline for submitting exemptions to the CNS Night Cycle. If a firm fails to exempt a position by this time, the CNS system may automatically sweep inventory that was intended for a specific client or segregation requirement, creating a "seg deficit" violation.1  
This compression forces firms to adopt "Match to Instruct" workflows, where the affirmation of a trade automatically generates the settlement instruction. The era of manual "DK" processing is effectively over; reliance on automated tools like the DTCC Exception Manager is now a prerequisite for operational compliance.5

## **X. Conclusion**

Fail management in US equity settlement is a discipline defined by the intersection of algorithmic determinism and regulatory rigidity. The CNS system, with its netting and recycling logic, provides the machinery for efficiency, while the Stock Borrow Program and Partial Settlement functionality serve as vital pressure release valves. However, the costs of malfunction are severe. The 2025 overhaul of the CNS Fails Charge—imposing 100% penalties on aged fails—and the capital deductions mandated by Rule 15c3-1 transform operational delays into direct hits on a firm's profitability and solvency. In the T+1 environment, the "FinOps" function has evolved from a back-office support role to a frontline risk management capability, where the ability to automate inventory allocation and preemptively resolve exceptions is the primary defense against systemic and financial liability.

#### **Works cited**

1. Equity Settlement Workflow and Decision Tree  
2. NATIONAL SECURITIES CLEARING CORPORATION \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/Globals/PDFs/2023/September/30/NSCC-Self-Assessment-Q3](https://www.dtcc.com/Globals/PDFs/2023/September/30/NSCC-Self-Assessment-Q3)  
3. Self-Regulatory Organizations; National Securities Clearing Corporation; Order Approving of Proposed Rule Change To Amend the CNS Fails Charge in the NSCC Rules \- Federal Register, accessed on February 3, 2026, [https://www.federalregister.gov/documents/2025/12/01/2025-21645/self-regulatory-organizations-national-securities-clearing-corporation-order-approving-of-proposed](https://www.federalregister.gov/documents/2025/12/01/2025-21645/self-regulatory-organizations-national-securities-clearing-corporation-order-approving-of-proposed)  
4. SR 2025 \- \* 013 \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/Globals/PDFs/2025/September/05/SR-NSCC-2025-013](https://www.dtcc.com/Globals/PDFs/2025/September/05/SR-NSCC-2025-013)  
5. Proposed Rule: Shortening the Securities Transaction Settlement Cycle \- SEC.gov, accessed on February 3, 2026, [https://www.sec.gov/files/rules/proposed/2022/34-94196.pdf](https://www.sec.gov/files/rules/proposed/2022/34-94196.pdf)  
6. Efficient Netting & Settlement with CNS \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/clearing-and-settlement-services/equities-clearing-services/cns](https://www.dtcc.com/clearing-and-settlement-services/equities-clearing-services/cns)  
7. Order Approving of Proposed Rule Change to Amend the CNS Fails Charge in the NSCC Rules \- SEC.gov, accessed on February 3, 2026, [https://www.sec.gov/files/rules/sro/nscc/2025/34-104270.pdf](https://www.sec.gov/files/rules/sro/nscc/2025/34-104270.pdf)  
8. Federal Register/Vol. 78, No. 249/Friday, December 27, 2013/Notices \- GovInfo, accessed on February 3, 2026, [https://www.govinfo.gov/content/pkg/FR-2013-12-27/pdf/2013-30936.pdf](https://www.govinfo.gov/content/pkg/FR-2013-12-27/pdf/2013-30936.pdf)  
9. ACCELERATED SETTLEMENT (T+1) \- State Street, accessed on February 3, 2026, [https://www.statestreet.com/web/insights/articles/documents/t1-functional-changes.pdf](https://www.statestreet.com/web/insights/articles/documents/t1-functional-changes.pdf)  
10. Settlement Enhancements: Partial Settlement \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/-/media/Files/Downloads/Transformation/Partial-Settlement.pdf](https://www.dtcc.com/-/media/Files/Downloads/Transformation/Partial-Settlement.pdf)  
11. Settlement Service Guide \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/globals/pdfs/2018/february/27/service-guide-settlement](https://www.dtcc.com/globals/pdfs/2018/february/27/service-guide-settlement)  
12. FINRA \- SEA Rule 15c3-1 (a), accessed on February 3, 2026, [https://www.finra.org/sites/default/files/SEA.Rule\_.15c3-1.Interpretations.pdf](https://www.finra.org/sites/default/files/SEA.Rule_.15c3-1.Interpretations.pdf)  
13. Equities Clearing & Settlement Transformation-Functional Change Document \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/-/media/Files/Downloads/Transformation/Functional-Change-Document.pdf](https://www.dtcc.com/-/media/Files/Downloads/Transformation/Functional-Change-Document.pdf)  
14. Self-Regulatory Organizations; National Securities Clearing Corporation; Notice of Filing of Proposed Rule Change To Modify the Amended and Restated Stock Options and Futures Settlement Agreement and Make Certain Revisions to the NSCC Rules \- Federal Register, accessed on February 3, 2026, [https://www.federalregister.gov/documents/2023/08/30/2023-18670/self-regulatory-organizations-national-securities-clearing-corporation-notice-of-filing-of-proposed](https://www.federalregister.gov/documents/2023/08/30/2023-18670/self-regulatory-organizations-national-securities-clearing-corporation-notice-of-filing-of-proposed)  
15. NSCC IOSCO Disclosure Framework \- Bank for International Settlements, accessed on February 3, 2026, [https://www.bis.org/publ/cpss20\_usnscc.pdf](https://www.bis.org/publ/cpss20_usnscc.pdf)  
16. Self-Regulatory Organizations; National Securities Clearing Corporation; Notice of Filing of Proposed Rule Change To Discontinue its Stock Borrow Program \- Federal Register, accessed on February 3, 2026, [https://www.federalregister.gov/documents/2013/12/27/2013-30936/self-regulatory-organizations-national-securities-clearing-corporation-notice-of-filing-of-proposed](https://www.federalregister.gov/documents/2013/12/27/2013-30936/self-regulatory-organizations-national-securities-clearing-corporation-notice-of-filing-of-proposed)  
17. Securities Lending Primer \- NAIC, accessed on February 3, 2026, [https://content.naic.org/sites/default/files/capital-markets-primer-securities-lending.pdf](https://content.naic.org/sites/default/files/capital-markets-primer-securities-lending.pdf)  
18. The Stock Borrow Program \- SEC.gov, accessed on February 3, 2026, [https://www.sec.gov/files/rules/proposed/s72404/s72404-14.pdf](https://www.sec.gov/files/rules/proposed/s72404/s72404-14.pdf)  
19. GAO-09-318R Securities and Exchange Commission: Oversight of U.S. Equities Market Clearing Agencies, accessed on February 3, 2026, [https://www.gao.gov/pdf/product/new-items-d09318r](https://www.gao.gov/pdf/product/new-items-d09318r)  
20. S\&P Securities Lending Index Series Methodology, accessed on February 3, 2026, [https://www.spglobal.com/spdji/en/documents/methodologies/methodology-sp-securities-lending.pdf](https://www.spglobal.com/spdji/en/documents/methodologies/methodology-sp-securities-lending.pdf)  
21. Securities Financing Transaction (SFT) Clearing \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/clearing-and-settlement-services/equities-clearing-services/sft](https://www.dtcc.com/clearing-and-settlement-services/equities-clearing-services/sft)  
22. Securities Financing Transactions (SFT) Clearing Frequently Asked Questions (FAQs) \- DTCC Learning Center, accessed on February 3, 2026, [https://dtcclearning.com/helpfiles/ec/sft-faq/Content/Resources/Attachments/sft\_clearing\_faq.pdf](https://dtcclearning.com/helpfiles/ec/sft-faq/Content/Resources/Attachments/sft_clearing_faq.pdf)  
23. Self-Regulatory Organizations; National Securities Clearing Corporation; Notice of Filing and Immediate Effectiveness of Proposed Rule Change To Modify Addendum A (Fee Structure) \- Federal Register, accessed on February 3, 2026, [https://www.federalregister.gov/documents/2024/12/23/2024-30527/self-regulatory-organizations-national-securities-clearing-corporation-notice-of-filing-and](https://www.federalregister.gov/documents/2024/12/23/2024-30527/self-regulatory-organizations-national-securities-clearing-corporation-notice-of-filing-and)  
24. Securities Financing Transaction (SFT) Clearing \- DTCC Learning Center, accessed on February 3, 2026, [https://dtcclearning.com/products-and-services/equities-clearing/sft-clearing.html](https://dtcclearning.com/products-and-services/equities-clearing/sft-clearing.html)  
25. Self-Regulatory Organizations; National Securities Clearing Corporation; Order Approving Proposed Rule Change To Introduce Central Clearing for Securities Financing Transaction Clearing Service \- Federal Register, accessed on February 3, 2026, [https://www.federalregister.gov/documents/2022/06/06/2022-12009/self-regulatory-organizations-national-securities-clearing-corporation-order-approving-proposed-rule](https://www.federalregister.gov/documents/2022/06/06/2022-12009/self-regulatory-organizations-national-securities-clearing-corporation-order-approving-proposed-rule)  
26. Self-Regulatory Organizations; National Securities Clearing Corporation; Notice of Filing of Proposed Rule Change To Amend the CNS Fails Charge in the NSCC Rules \- Federal Register, accessed on February 3, 2026, [https://www.federalregister.gov/documents/2025/09/16/2025-17815/self-regulatory-organizations-national-securities-clearing-corporation-notice-of-filing-of-proposed](https://www.federalregister.gov/documents/2025/09/16/2025-17815/self-regulatory-organizations-national-securities-clearing-corporation-notice-of-filing-of-proposed)  
27. Important Notice National Securities Clearing Corporation \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/-/media/Files/pdf/2025/12/1/a9687.pdf](https://www.dtcc.com/-/media/Files/pdf/2025/12/1/a9687.pdf)  
28. NSCC Risk Margin Component Guide \- DTCC Learning Center, accessed on February 3, 2026, [https://dtcclearning.com/documents/equities-clearing/nscc-risk-management/risk-management-nscc/3992-nscc-risk-margin-component-guide.html](https://dtcclearning.com/documents/equities-clearing/nscc-risk-management/risk-management-nscc/3992-nscc-risk-margin-component-guide.html)  
29. Order Approving Proposed Rule Change to Adopt Intraday Volatility Charge and Eliminate Intraday Backtesting Charge \- SEC.gov, accessed on February 3, 2026, [https://www.sec.gov/files/rules/sro/nscc/2023/34-97129.pdf](https://www.sec.gov/files/rules/sro/nscc/2023/34-97129.pdf)  
30. Self-Regulatory Organizations; National Securities Clearing Corporation; Notice of Filing of Advance Notice To Accelerate Its Trade Guaranty, Add New Clearing Fund Components, Enhance Its Intraday Risk Management, Provide for Loss Allocation of “Off-the-Market Transactions,” and Make Other Changes \- Federal Register, accessed on February 3, 2026, [https://www.federalregister.gov/documents/2016/11/30/2016-28771/self-regulatory-organizations-national-securities-clearing-corporation-notice-of-filing-of-advance](https://www.federalregister.gov/documents/2016/11/30/2016-28771/self-regulatory-organizations-national-securities-clearing-corporation-notice-of-filing-of-advance)  
31. Key. SEC Financial Responsibility Rules, accessed on February 3, 2026, [https://www.sec.gov/about/offices/oia/oia\_market/key\_rules.pdf](https://www.sec.gov/about/offices/oia/oia_market/key_rules.pdf)  
32. Financial Responsibility and the Net Capital Rule \- AWS, accessed on February 3, 2026, [https://sep-media.s3.us-west-2.amazonaws.com/series/27/samples/sample\_Series27.pdf](https://sep-media.s3.us-west-2.amazonaws.com/series/27/samples/sample_Series27.pdf)  
33. Net Capital | FINRA.org, accessed on February 3, 2026, [https://www.finra.org/rules-guidance/guidance/reports/2021-finras-examination-and-risk-monitoring-program/net-capital](https://www.finra.org/rules-guidance/guidance/reports/2021-finras-examination-and-risk-monitoring-program/net-capital)  
34. SEA Rule 15c3-1 and Related Interpretations | FINRA.org, accessed on February 3, 2026, [https://www.finra.org/rules-guidance/guidance/interpretations-financial-operational-rules/sea-rule-15c3-1-and-related-interpretations](https://www.finra.org/rules-guidance/guidance/interpretations-financial-operational-rules/sea-rule-15c3-1-and-related-interpretations)  
35. NET CAPITAL REQUIREMENTS FOR BROKERS OR DEALERS SEA Rule 15c3-1 \- FINRA, accessed on February 3, 2026, [https://www.finra.org/sites/default/files/InterpretationsFOR/p037763.pdf](https://www.finra.org/sites/default/files/InterpretationsFOR/p037763.pdf)  
36. SEA Rule 15c3-3 and Related Interpretations | FINRA.org, accessed on February 3, 2026, [https://www.finra.org/rules-guidance/guidance/interpretations-financial-operational-rules/sea-rule-15c3-3-and-related-interpretations](https://www.finra.org/rules-guidance/guidance/interpretations-financial-operational-rules/sea-rule-15c3-3-and-related-interpretations)  
37. Page 3 of 45 \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/Globals/PDFs/2021/July/27/SR-NSCC-2021-011](https://www.dtcc.com/Globals/PDFs/2021/July/27/SR-NSCC-2021-011)  
38. Page 3 of 83 \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/Globals/PDFs/2022/June/24/SR-NSCC-2022-009](https://www.dtcc.com/Globals/PDFs/2022/June/24/SR-NSCC-2022-009)  
39. Self-Regulatory Organizations; The Options Clearing Corporation; Notice of Filing of Proposed Rule Change, as Modified by Partial Amendment No. 1, by The Options Clearing Corporation Concerning Its Stock Loan Programs \- Federal Register, accessed on February 3, 2026, [https://www.federalregister.gov/documents/2024/09/10/2024-20329/self-regulatory-organizations-the-options-clearing-corporation-notice-of-filing-of-proposed-rule](https://www.federalregister.gov/documents/2024/09/10/2024-20329/self-regulatory-organizations-the-options-clearing-corporation-notice-of-filing-of-proposed-rule)