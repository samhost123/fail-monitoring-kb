# **Operational Dynamics of US Equity Settlement Exception Processing: A Technical Analysis of Reclaims, Recalls, and Buy-Ins**

## **Systemic Architecture of Settlement Exceptions**

The settlement of equity transactions in the United States capital markets is governed by a highly sophisticated, multi-tiered infrastructure designed to ensure the prompt and accurate exchange of ownership and funds.1 At the core of this ecosystem sits the Depository Trust & Clearing Corporation (DTCC) and its subsidiaries, the National Securities Clearing Corporation (NSCC) and The Depository Trust Company (DTC). While the Continuous Net Settlement (CNS) system provides the primary engine for clearing and settling street-side equity trades through netting and novation, the systemic integrity of the market is ultimately defined by its ability to manage departures from the standard workflow.1 These departures, categorized as exception processing, encompass reclaims, recalls, and buy-ins.  
In the contemporary regulatory environment, particularly following the transition to a trade date plus one business day (T+1) settlement cycle in May 2024, the management of these exceptions has shifted from a back-office administrative task to a front-line risk management imperative.3 The reduction of the settlement window by 24 hours has compressed the time available for operational remediation by approximately 83%, forcing market participants to adopt real-time resolution strategies for failed obligations.5  
The architecture of exception processing is built upon the interaction between the NSCC’s netting engine and the DTC’s inventory locations. When a trade fails to settle on the scheduled settlement date (SD), it does not merely disappear; it enters a specialized lifecycle governed by strict algorithmic logic (CNS), rigorous inventory controls (Inventory Management System or IMS), and unforgiving regulatory deadlines (Regulation SHO).1 The effective management of this lifecycle distinguishes solvent, capital-efficient firms from those plagued by operational drag and regulatory penalties.

### **The CNS Accounting Operation and Fail Management**

To understand exception processing, one must first grasp the "continuous" nature of the CNS system. Unlike a window settlement system where trades must settle on a specific day or fail bilaterally, CNS automatically rolls failing positions forward.1 A "fail to deliver" today becomes part of the opening short position for tomorrow's netting cycle. This structure reduces the volume of securities movements required, as a member with equal buying and selling activity in the same security may end the day "flat," requiring no physical movement of shares despite significant trading volume.1  
However, this continuity creates a risk: the accumulation of aged fails. A fail represents a credit risk to the Central Counterparty (CCP) and a market risk to the receiving member. To mitigate this, the NSCC employs a sophisticated accounting operation divided into Night and Day cycles, each with specific allocation logic designed to prioritize the resolution of exceptions.1

#### **The Night Cycle Allocation Logic**

The processing day effectively begins on the evening preceding the settlement date (S-1). The Night Cycle is designed to maximize settlement volume by utilizing available inventory before the market opens.1

* **Timing and Scope:** The cycle typically processes approximately 50 percent of CNS transactions. It begins in the evening (approx. 11:30 PM ET in T+1) and utilizes the "Closing Positions" from the prior day netted against the new "Settling Trades".6  
* **Inventory Sourcing:** The system checks the delivering member's designated sub-accounts at DTC. If shares are available in the "General Free" account and are not otherwise exempted via IMS, they are debited from the member and credited to the NSCC's central CNS account.1  
* **Exception Handling:** Crucially, the Night Cycle allows for specific "Standing Priority Requests" and "Priority Overrides." A member anticipating a buy-in or a critical client delivery can manipulate these settings to ensure their long position is satisfied first during this batch process.1

#### **The Day Cycle and Dynamic Settlement**

Positions that remain open after the Night Cycle—due to insufficient inventory or specific exemption instructions—are recycled into the Day Cycle on the settlement date.1

* **Dynamic Processing:** As members receive securities throughout the day (from other settlements, stock loan returns, or new deposits), these shares become available for CNS allocation. The system continuously attempts to satisfy open short obligations.1  
* **Settlement Optimization:** Recent enhancements include algorithms that hold certain transactions to process them in batches, maximizing the total number of items settled rather than processing strictly one-by-one. This is particularly relevant for "partial settlements," where the system settles the portion of the obligation supported by inventory to reduce the aggregate fail value.1

### **Inventory Management System (IMS) Profiles**

The Inventory Management System (IMS) acts as the staging area and control panel for settlement.1 It allows members to dictate the rules under which their securities inventory is utilized. In the context of exception processing, IMS profiles are the primary tool for managing the flow of assets to prevent accidental deliveries that might exacerbate a fail or violate a segregation requirement.

| Profile Type | Operational Behavior | Strategic Application in Exception Management |
| :---- | :---- | :---- |
| **Green Profile** | **High Automation:** The system attempts to process deliveries immediately as they become due, provided there is sufficient position and risk controls are satisfied. | Used for standard, low-risk transactions where speed and STP (Straight-Through Processing) are the priority. In T+1, this is the default for most prime brokerage flows to ensure 9:00 PM affirmation deadlines are met. |
| **Yellow Profile** | **Conditional Automation:** The system processes deliveries only in a specific order authorized by the participant. It may "reserve" positions for deliveries that are pending due to receiver controls. | Critical for managing intraday liquidity or inventory scarcity. A firm might use this to ensure a "Buy-In" obligation is satisfied before a general street-side delivery. |
| **Red Profile** | **Manual Intervention:** The system *does not* process deliveries automatically. Transactions are queued and require an explicit "release" instruction. | Reserved for high-value transactions, sensitive counterparties, or reclaims where the risk of error is high. This profile prevents "flight" of assets that are subject to a recall or segregation order. |

1  
The strategic manipulation of these profiles allows operations teams to "defend" their inventory. For example, if a firm receives a stock loan recall (an exception), they may switch the relevant security to a "Red Profile" or set a "Global Lock" to prevent those shares from being delivered out to satisfy a routine CNS obligation, ensuring they remain available to satisfy the recall.1

## **The Reclaim: Operational Correction and Liability Reversal**

A reclaim, or reclamation, is the systemic return of a delivery (Deliver Order or Payment Order) received by a participant.1 It is distinct from a trade cancellation, which typically occurs before settlement. A reclaim is a post-settlement reversal intended to correct an error in the original delivery, such as an incorrect quantity, the wrong security, or a delivery that the receiver does not recognize ("Don't Know" or DK).1  
From a strict operational perspective, the DTC treats a reclaim as a **new delivery**.1 This has profound risk management implications: the return of the shares must pass through the same Receiver Authorized Delivery (RAD) controls and Net Debit Cap checks as the original transaction. If the original deliverer (now the receiver of the reclaim) acts in bad faith or lacks the credit cap to accept the return, the reclaim can fail, leaving the erroneous shares stuck with the original receiver.9

### **The Reclaim Reason Codes: A Taxonomy of Errors**

The efficiency of the reclaim process relies on the accurate use of **Reason Codes**. These codes signal to the counterparty and the settlement system exactly why the delivery is being rejected. In the high-speed T+1 environment, selecting the correct code is vital for automated matching and reconciliation.11  
The following table details the primary reason codes utilized in daily financial operations for reclaims:

| Code | Classification | Description | Operational Consequence |
| :---- | :---- | :---- | :---- |
| **41** | **DK (Don't Know)** | The receiver does not recognize the trade or the counterparty. | Often indicates an affirmation failure or a missing SSI (Standing Settlement Instruction). Requires immediate investigation by the middle office. |
| **42** | **Wrong Quantity** | The delivered share count does not match the trade confirmation. | The receiver typically reclaims the *entire* delivery, forcing the deliverer to re-book and re-deliver the correct amount. Partial reclaims (Code 45\) are also possible but complex. |
| **43** | **Wrong Security** | The CUSIP delivered differs from the trade blotter. | High risk. Receiving the wrong CUSIP can contaminate the receiver's inventory, potentially leading to segregation violations if not caught immediately via RAD. |
| **44** | **Wrong Money** | The settlement value (cash amount) is incorrect. | Common in DVP (Delivery Versus Payment) trades. The securities are correct, but the payment amount is disputed. |
| **45** | **Partial Reclaim** | Returning only a portion of the received shares. | Used when an over-delivery occurs (e.g., received 1,000 shares on a trade for 500). |
| **87** | **Reorganization** | Related to corporate action adjustments. | Often used when a delivery occurs on a security that has undergone a mandatory reorganization (e.g., merger or reverse split) and the deliverer sent the "old" shares. |
| **88** | **Distribution** | Related to dividend or interest payment discrepancies. | Used to reclaim funds related to erroneous dividend allocations. |

9

### **Receiver Authorized Delivery (RAD) and Reclaims**

The interaction between reclaims and the **Receiver Authorized Delivery (RAD)** system is a critical control point. RAD is designed to prevent "dumping"—the practice of delivering securities to a counterparty without their prior knowledge, potentially causing them to breach their collateral limits.1

1. **Matched Reclaims:** If the DTC system can systemically link the reclaim to a specific original transaction that occurred earlier that same day, it is processed as a **"Matched Reclaim"**.14 Crucially, matched reclaims are generally **exempt from RAD limits** for the original deliverer.15 This means the original deliverer *cannot* block the return of the shares via RAD. The system forces the return, ensuring that a firm cannot make an erroneous delivery and then refuse to take it back.  
2. **Unmatched Reclaims:** If the reclaim cannot be linked to a specific transaction (e.g., if the original trade settled on a previous day or the data fields do not align perfectly), it is treated as an unmatched delivery. These *are* subject to RAD.14 This creates a risk where the original deliverer receives the reclaim in their RAD queue and must manually approve it. If they refuse (DK the reclaim), the two firms enter a bilateral dispute while the shares remain in limbo.

### **Reclaim Modernization: Decoupling and Simplification**

Historically, the DTC attempted to strictly "link" every reclaim to an original transaction processed within the preceding 60 business days.16 However, recent initiatives in settlement simplification are moving away from this rigid systemic linking. The DTC has announced plans (targeting Q3 2027\) to decommission the strict linking capability.16  
**Implication:** Future reclaims will rely more heavily on the information provided by the client (such as the original transaction reference number inserted in the reclaim message) rather than a depository-level validation link. This shifts the burden of reconciliation to the participants' internal systems but allows for greater flexibility in processing returns for trades that may have complex histories (e.g., shaped deliveries or partial settlements).16

## **Securities Lending Recalls: Liquidity Mechanics in T+1**

While reclaims correct errors, **Recalls** are the exercise of a contractual right within the securities lending market. In a typical stock loan transaction, a lender (beneficial owner) transfers securities to a borrower (often a broker-dealer covering a short sale) in exchange for collateral.17 The lender retains the right to "recall" the loan at any time, demanding the return of the securities.19  
In the T+1 environment, the recall process has become a critical choke point for liquidity. The compression of the settlement cycle means that a borrower has significantly less time to source shares to satisfy a recall.3

### **The Operational Workflow of a Recall**

The recall lifecycle is governed by the Master Securities Lending Agreement (MSLA), but its execution relies on the messaging infrastructure provided by DTCC's **SMART/Track**.20

1. **Initiation:** The lender determines a need for the shares (usually to sell them or to vote in a proxy meeting). They generate a Recall Notice.  
2. **Transmission:** The notice is transmitted via **SMART/Track for Stock Loan Recalls**. This service acts as a centralized hub, routing ISO 15022/20022 messages between counterparties.20 This creates an immutable audit trail of the recall issuance time, which is critical for determining regulatory compliance.  
3. **The "Bona Fide" Deadline:** To ensure the borrower can return the shares by settlement date (SD), the industry best practice under T+1 is to issue the recall by **11:59 PM ET on the trade date (T)**.3  
   * *Old Standard (T+2):* Recalls could often be issued by 3:00 PM on T+1.  
   * *New Standard (T+1):* The 11:59 PM T cutoff allows the borrower the full T+1 day to source inventory (borrow elsewhere or buy in the market) to meet the delivery.3

### **Regulation SHO and the "Deemed to Own" Requirement**

The recall workflow is directly tied to **Regulation SHO Rule 200(g)**, which governs how broker-dealers must mark sell orders ("long" or "short").22

* **Long Sale Marking:** A broker can only mark a sale as "long" if the seller owns the security and the broker reasonably expects that the security will be in their physical possession or control by the settlement date.23  
* **The Recall Link:** If the shares are currently out on loan, the seller is still "deemed to own" them, provided they issue a **"bona fide" recall**.1  
* **The T+1 Nuance:** For the recall to be "bona fide" under T+1, it must be issued such that the borrower is contractually obligated to return the shares within the standard settlement cycle. If a lender sells shares and *fails* to issue the recall by the 11:59 PM T deadline, they may not be able to rely on the "long" marking provision, potentially forcing them to treat the trade as a short sale (which requires a "locate") or facing a failure to deliver.21

### **Proxy Voting and the "Empty Voting" Risk**

A significant driver of recall volume is corporate governance. Institutional investors have a fiduciary duty to vote their shares in material corporate actions.19 However, shares on loan cannot be voted by the lender; the voting right follows the share to the borrower (and often subsequently to the ultimate buyer).  
This dynamic creates "empty voting" risk (where a borrower votes shares they have no economic interest in) and forces lenders to recall shares ahead of the **Record Date**. The new Form N-PX reporting requirements, effective July 2024, require funds to publicly disclose the number of shares they voted versus the number they had on loan and *chose not to recall*.19 This transparency is expected to increase the volume of recalls around proxy seasons, placing further stress on the settlement infrastructure.

## **Buy-Ins: The Regulatory and Operational End-Game**

When the standard settlement process fails—netting doesn't cover the obligation, reclaims are rejected, and recalls are dishonored—the industry turns to its final enforcement mechanism: the **Buy-In**.1 A buy-in allows a receiving member (the buyer) to purchase the failing securities in the open market and charge the cost difference to the failing counterparty.1  
There are two distinct buy-in regimes in the US market: **NSCC Rule 11** (for CNS trades) and **FINRA Rule 11810** (for ex-clearing trades).1

### **NSCC Rule 11: The CNS Buy-In Workflow**

In the CNS system, the NSCC is the Central Counterparty (CCP). Therefore, a member failing to receive shares is technically failing to receive them from the NSCC, not a specific trading partner. The CNS Buy-In process is designed to prioritize allocation rather than immediately force a market execution.1

#### **1\. Submission of Buy-In Intent**

The process begins when a Long Member (waiting for shares) submits a **"Buy-In Intent"** to the NSCC via the SMART/Track system.1 This notice alerts the CCP that the member demands delivery.

#### **2\. Priority Group 2 Elevation**

Upon receipt of the Buy-In Intent, the NSCC's accounting algorithm elevates the member's long position to **Priority Group 2**.1

* **Priority Group 1:** Corporate Actions (Reorg sub-accounts).  
* **Priority Group 2:** Buy-Ins (Expiring Intents).  
* **Priority Group 3:** Member Requests (General settlement).

This elevation ensures that any shares coming into the CNS system (from any member's deliveries) are allocated to the Buy-In position *before* they are used to satisfy general settlement obligations. This "queue jumping" is the system's primary method of resolving the fail without external market action.1

#### **3\. The Retransmittal Notice**

If the Priority Group 2 allocation fails to satisfy the obligation by the specified time, the NSCC issues a **CNS Retransmittal Notice**.1

* **Targeting the Oldest Fail:** The NSCC identifies the member(s) with the *oldest* short positions in that security.  
* **Passing the Liability:** The Retransmittal Notice effectively passes the buy-in liability from the NSCC to those specific failing members.1  
* **Timing:** For "Buy-In Retransmittal Notices" (where the submitting member is passing on a buy-in they received externally), the execution clock is accelerated. The buy-in can be executed as early as **3:00 PM ET on N+1** (where N is the submission day).27

#### **4\. Execution and Financial Settlement**

If the shares are still not delivered by the deadline, the originator executes the buy-in in the open market.

* **Buy-In Premium:** If the execution price is higher than the original contract price (a "buy-in premium"), the difference is debited from the failing member's settlement account and credited to the originator.28  
* **Money Settlement:** These debits and credits flow through the daily CNS money settlement process, netting against the member's other obligations.1

### **FINRA Rule 11810: The Bilateral Buy-In**

For trades settled outside of CNS (ex-clearing, balance orders, or physical settlements), the process is governed by FINRA Rule 11810\.1 This is a manual, bilateral process.

* **Notice Requirement:** The buyer must send a written notice to the seller no later than **12:00 noon ET**, two business days prior to the proposed execution date.8  
* **Transit Protections:** A key feature of Rule 11810 is the protection for securities in transit. If the seller can provide evidence (e.g., certificate numbers, transfer agent receipts) that the securities are **in transit** or **in transfer**, the buyer *must* extend the execution date, typically by **seven calendar days**.8  
* **Liability Notice:** For securities subject to corporate actions (like voluntary tenders), the receiving member may send a "Liability Notice." This informs the failing seller that they will be held liable for any lost value if the shares are not delivered in time to participate in the offer.30

### **Regulation SHO Rule 204: The Mandatory Close-Out**

Distinct from the operational buy-in rules of NSCC and FINRA, **Regulation SHO Rule 204** imposes a federal mandate to close out fails to deliver (FTDs) to prevent abusive "naked" short selling.1

* **The Clock:**  
  * **Short Sales:** Must be closed out by the beginning of regular trading hours on **T+1** (Settlement \+ 1).1  
  * **Long Sales:** Must be closed out by the beginning of regular trading hours on **T+3** (Settlement \+ 3).1  
  * **Market Makers:** Fails attributable to bona fide market making are granted the extended **T+3** timeline.1  
* **The Penalty Box:** Failure to comply results in the "Penalty Box" (Rule 204(b)). The firm is banned from shorting that security unless it pre-borrows the shares (a "hard borrow") until the fail is cured.1 This is a severe operational constraint that destroys the economics of market making for that security.

## **The Bilateral Ecosystem and Obligation Warehouse**

While CNS captures the majority of volume, a significant number of trades—such as complex ex-clearing transactions, non-CNS eligible global securities, and aged fails—live in the bilateral world. Historically, managing these fails was a manual nightmare of paper "DK" notices and phone calls.1  
The **Obligation Warehouse (OW)** service was introduced to automate this bilateral landscape. It serves as a central repository for ex-clearing obligations, performing three critical functions:

1. **Storage and Maintenance:** OW tracks open obligations, automatically adjusting them for mandatory corporate actions (e.g., stock splits, mergers) so that the liability remains accurate over time.1  
2. **RECAPS (Reconfirmation and Pricing Service):** The OW periodically runs the RECAPS cycle, which re-prices open fails to the current market value. This reduces counterparty credit risk by marking the fail to market and settling the cash difference, leaving only the flat security obligation outstanding.1  
3. **The CNS Eligibility Scan:** Perhaps its most vital function is the daily scan. If a security stored in the OW suddenly becomes CNS-eligible (e.g., a restriction is lifted), the OW automatically "flips" the obligation into the CNS Accounting Operation.1 This mechanism "rescues" trades from the bilateral world, moving them into the novated, guaranteed environment of the CCP, thereby significantly reducing systemic risk.33

## **T+1 Operational Impact and Future Resilience**

The shift to T+1 has removed the "operational slack" that previously allowed firms to resolve exceptions manually. With the affirmation deadline moved to 9:00 PM on Trade Date (T) and the Night Cycle starting at 11:30 PM, the margin for error is effectively zero.6

### **The Cost of Failure**

The financial penalties for exception mismanagement have escalated. The NSCC has revised the **CNS Fails Charge** to be increasingly punitive based on the **duration** of the fail rather than just the member's credit rating.35 Furthermore, the removal of the fails charge credit for long positions aligns the penalty strictly with the failing deliverer, removing any "offset" benefit for firms that are net flat but failing on both sides.36  
Operationally, a trade that fails to affirm by 9:00 PM T and subsequently fails settlement incurs:

* **Night Delivery Order (NDO) Fees:** Significantly higher than CNS allocation fees.6  
* **Cost of Carry:** The interest expense of financing unsettled positions.  
* **Regulatory Risk:** Exposure to Reg SHO Penalty Box restrictions.

### **Automation: The Only Path Forward**

To survive in this environment, firms are adopting "Match-to-Instruct" (M2i) workflows. By integrating systems like CTM and ALERT, trades are automatically enriched with SSIs and affirmed immediately upon matching, bypassing manual intervention entirely.38 This "upstream" resolution of exceptions—fixing the data before it ever reaches the DTC—is the defining characteristic of the modern, resilient financial operation.  
In conclusion, exception processing in the US equity market is no longer a remedial back-office function. It is a complex, high-stakes discipline involving the synchronization of contractual rights (Recalls), systemic corrections (Reclaims), and regulatory enforcement (Buy-Ins). Mastery of these workflows—specifically the interaction between IMS profiles, RAD thresholds, and CNS priority groups—is the primary determinant of operational alpha in the T+1 era.

## **Daily Settlement Operations Checklist (T+1 Context)**

To ensure compliance and operational resilience, the following daily checklist serves as a guide for settlement operations analysts managing the exception lifecycle.

### **Trade Date (T) \- The "Golden Hours"**

* **7:00 PM ET:** Deadline for Buy-Side Allocations. Ensure all institutional allocations are received to allow time for affirmation.40  
* **8:00 PM ET:** **Reclaim Risk Assessment.** Review any reclaims received during the day (Reason Codes 41/42/43). Ensure valid reclaims are processed and invalid ones are rejected before EOD systems close.11  
* **9:00 PM ET:** **Affirmation Cutoff.** The critical deadline. Verify that all eligible institutional trades are affirmed in TradeSuite ID/CTM. Unaffirmed trades after this time will likely fail CNS netting and require costly bilateral Delivery Orders.21  
* **10:45 PM ET:** **CNS Exemption Deadline.** Final check of IMS profiles. Ensure "Fully Paid" customer securities are exempted from CNS delivery to prevent segregation violations (Rule 15c3-3).1  
* **11:30 PM ET:** **Night Delivery Order (NDO) Cutoff.** Last chance to input manual deliveries for the Night Cycle.6  
* **11:59 PM ET:** **Stock Loan Recall Deadline.** Issue all recalls via SMART/Track to establish "bona fide" status for T+1 return requirements.3

### **Settlement Date (S / T+1) \- The Resolution Phase**

* **2:00 AM ET:** **CNS Reporting.** Review the *CNS Settlement Activity Statement*. Identify positions that failed the Night Cycle. These are the priority targets for the Day Cycle.1  
* **8:00 AM \- 1:30 PM ET:** **Day Cycle & Returns.** Monitor incoming stock loan returns. As inventory arrives, ensure IMS "Green" profiles release shares to satisfy CNS short obligations.1  
* **12:00 PM ET:** **Buy-In Notice Deadline (Ex-Clearing).** For bilateral trades (FINRA Rule 11810), ensure buy-in notices are delivered by noon for execution two days later.8  
* **3:00 PM ET:** **Recall Execution Window.** Assess if recalled securities have been returned. If not, evaluate counterparty exposure and prepare for potential buy-in initiation.21  
* **3:10 PM ET:** **NSCC Buy-In Execution.** The window opens to execute buy-ins for Retransmittal Notices (N+1 execution).27  
* **3:20 PM ET:** **Day Delivery Order (DDO) Cutoff.** Final deadline for valuing deliveries in the current settlement day.6  
* **3:45 PM ET:** **Money Settlement.** Final reconciliation of net debits/credits with the settling bank.1

### **Post-Settlement (S+1 and Beyond)**

* **Reg SHO Close-Outs:** Identify any Short Sale fails that were not resolved on S. These *must* be borrowed or bought-in by market open on S+1 (T+2) to avoid the Penalty Box.1  
* **OW Maintenance:** Check the Obligation Warehouse for any ex-clearing fails that need to be re-priced (RECAPS) or that have flipped to CNS eligibility.1

#### **Works cited**

1. Equity Settlement Workflow and Decision Tree  
2. Efficient Netting & Settlement with CNS \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/clearing-and-settlement-services/equities-clearing-services/cns](https://www.dtcc.com/clearing-and-settlement-services/equities-clearing-services/cns)  
3. T+1 settlement cycle booklet \- ISDA.org, accessed on February 3, 2026, [https://www.isda.org/a/fFwgE/T1-Settlement-Cycle-Booklet.pdf](https://www.isda.org/a/fFwgE/T1-Settlement-Cycle-Booklet.pdf)  
4. JP Morgan US T+1 Securities Settlement – Frequently Asked Questions: Markets Clients, accessed on February 3, 2026, [https://www.jpmorgan.com/insights/securities-services/regulatory-solutions/us-t-plus-1securities-services-markets-faq](https://www.jpmorgan.com/insights/securities-services/regulatory-solutions/us-t-plus-1securities-services-markets-faq)  
5. T+1 Settlement Overview \- The Investment Association, accessed on February 3, 2026, [https://www.theia.org/sites/default/files/2024-11/IA%20T%2B1%20Settlement%20Overview.pdf](https://www.theia.org/sites/default/files/2024-11/IA%20T%2B1%20Settlement%20Overview.pdf)  
6. Trade Settlement: Know Your T+1 Blind Spots \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/dtcc-connection/articles/2024/april/29/trade-settlement-know-your-t1-blind-spots](https://www.dtcc.com/dtcc-connection/articles/2024/april/29/trade-settlement-know-your-t1-blind-spots)  
7. T+1 Settlement Timelines \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/-/media/Files/PDFs/T2/T1Timelinesv1824.pdf](https://www.dtcc.com/-/media/Files/PDFs/T2/T1Timelinesv1824.pdf)  
8. 11810\. Buy-In Procedures and Requirements | FINRA.org, accessed on February 3, 2026, [https://www.finra.org/rules-guidance/rulebooks/finra-rules/11810](https://www.finra.org/rules-guidance/rulebooks/finra-rules/11810)  
9. Settlement Service Guide \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/globals/pdfs/2018/february/27/service-guide-settlement](https://www.dtcc.com/globals/pdfs/2018/february/27/service-guide-settlement)  
10. DTC Settlement Service Guide \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/-/media/Files/Downloads/Operational-Resilience/DTC-Settlement-Service-Guide.pdf](https://www.dtcc.com/-/media/Files/Downloads/Operational-Resilience/DTC-Settlement-Service-Guide.pdf)  
11. Memo Segregation \- Exhibit 5, accessed on February 3, 2026, [https://www.sec.gov/files/rules/sro/dtc/2017/34-81099-ex5.pdf](https://www.sec.gov/files/rules/sro/dtc/2017/34-81099-ex5.pdf)  
12. Redemptions Service Guide \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/-/media/Files/Downloads/legal/service-guides/Redemptions.pdf](https://www.dtcc.com/-/media/Files/Downloads/legal/service-guides/Redemptions.pdf)  
13. dtc corporate actions \- user guide: iso 20022 messaging for distributions entitlements and allocations, accessed on February 3, 2026, [https://www.dtcc.com/-/media/Files/Downloads/issues/Corporate-Actions-Transformation/ISO\_20022\_EntAlloc\_UG.pdf](https://www.dtcc.com/-/media/Files/Downloads/issues/Corporate-Actions-Transformation/ISO_20022_EntAlloc_UG.pdf)  
14. DTC Settlement Service Guide \- Exhibit 5, accessed on February 3, 2026, [https://www.sec.gov/files/rules/sro/dtc/2014/34-73443-ex5.pdf](https://www.sec.gov/files/rules/sro/dtc/2014/34-73443-ex5.pdf)  
15. DTC \- Exhibit 5, accessed on February 3, 2026, [https://www.sec.gov/files/rules/sro/dtc/2013/34-69666-ex5.pdf](https://www.sec.gov/files/rules/sro/dtc/2013/34-69666-ex5.pdf)  
16. Reclaims \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/-/media/Files/Downloads/Transformation/Reclaims.pdf](https://www.dtcc.com/-/media/Files/Downloads/Transformation/Reclaims.pdf)  
17. Getting Income from Fully Paid Securities Lending \- Charles Schwab, accessed on February 3, 2026, [https://www.schwab.com/learn/story/earning-extra-income-with-securities-lending](https://www.schwab.com/learn/story/earning-extra-income-with-securities-lending)  
18. What Is Securities Lending? \- State Street Global Advisors, accessed on February 3, 2026, [https://www.ssga.com/library-content/assets/pdf/emea/resources/spdr-what-is-securities-lending.pdf](https://www.ssga.com/library-content/assets/pdf/emea/resources/spdr-what-is-securities-lending.pdf)  
19. Loan Recalls & the T+1 Countdown: Can Securities Lenders Adapt?, accessed on February 3, 2026, [https://csfme.org/loan-recalls-the-t1-countdown-can-securities-lenders-adapt/](https://csfme.org/loan-recalls-the-t1-countdown-can-securities-lenders-adapt/)  
20. Stock Loan Recall Messaging | DTCC SMART/Track Services, accessed on February 3, 2026, [https://www.dtcc.com/clearing-and-settlement-services/settlement/stock-loan-recalls](https://www.dtcc.com/clearing-and-settlement-services/settlement/stock-loan-recalls)  
21. T+1 SECURITIES SETTLEMENT INDUSTRY IMPLEMENTATION PLAYBOOK \- Investment Company Institute, accessed on February 3, 2026, [https://www.ici.org/files/2022/22-ppr-t1-playbook.pdf](https://www.ici.org/files/2022/22-ppr-t1-playbook.pdf)  
22. Accelerating the US Securities Settlement Cycle to T+1 \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/-/media/Files/PDFs/T2/Accelerating-the-US-Securities-Settlement-Cycle-to-T1-December-1-2021.pdf](https://www.dtcc.com/-/media/Files/PDFs/T2/Accelerating-the-US-Securities-Settlement-Cycle-to-T1-December-1-2021.pdf)  
23. Key Points About Regulation SHO \- SEC.gov, accessed on February 3, 2026, [https://www.sec.gov/investor/pubs/regsho.htm](https://www.sec.gov/investor/pubs/regsho.htm)  
24. SMART/Track Services \- DTCC Learning Center, accessed on February 3, 2026, [https://dtcclearning.com/products-and-services/settlement/smarttrack-services.html](https://dtcclearning.com/products-and-services/settlement/smarttrack-services.html)  
25. Self-Regulatory Organizations; National Securities Clearing Corporation; Order Approving Proposed Rule Change Relating To Buy-Ins in Its Continuous Net Settlement System \- Federal Register, accessed on February 3, 2026, [https://www.federalregister.gov/documents/2006/03/28/E6-4433/self-regulatory-organizations-national-securities-clearing-corporation-order-approving-proposed-rule](https://www.federalregister.gov/documents/2006/03/28/E6-4433/self-regulatory-organizations-national-securities-clearing-corporation-order-approving-proposed-rule)  
26. Self-Regulatory Organizations; National Securities Clearing Corporation; Notice of Filing and Immediate Effectiveness of a Proposed Rule Change To Clarify the Rules That Describe the Buy-In Process \- Federal Register, accessed on February 3, 2026, [https://www.federalregister.gov/documents/2018/09/27/2018-20997/self-regulatory-organizations-national-securities-clearing-corporation-notice-of-filing-and](https://www.federalregister.gov/documents/2018/09/27/2018-20997/self-regulatory-organizations-national-securities-clearing-corporation-notice-of-filing-and)  
27. Order Approving Proposed Rule Change Relating To Buy-Ins in Its Continuous Net Settlement System; Rel. No. 34-53528, File No. SR \- SEC.gov, accessed on February 3, 2026, [https://www.sec.gov/files/rules/sro/nscc/34-53528.pdf](https://www.sec.gov/files/rules/sro/nscc/34-53528.pdf)  
28. The ICMA Buy-in Rules, accessed on February 3, 2026, [https://www.icmagroup.org/assets/ICMA\_Buy-in-Rules\_Webinar\_September-2023.pdf](https://www.icmagroup.org/assets/ICMA_Buy-in-Rules_Webinar_September-2023.pdf)  
29. Principles and operations of the Buy-in process \- | European Securities and Markets Authority, accessed on February 3, 2026, [https://www.esma.europa.eu/sites/default/files/dacsi\_15-1119\_consresp\_esma\_rts\_on\_csdr\_operation\_of\_buy-in\_process\_v\_2.1\_6aug\_1.pdf](https://www.esma.europa.eu/sites/default/files/dacsi_15-1119_consresp_esma_rts_on_csdr_operation_of_buy-in_process_v_2.1_6aug_1.pdf)  
30. SEC Approves Amendments to NASD Rule 11810(i) to Mandate the Use of the Automated Liability Notification System of a Registered Clearing Agency \- FINRA, accessed on February 3, 2026, [https://www.finra.org/rules-guidance/notices/08-06](https://www.finra.org/rules-guidance/notices/08-06)  
31. Regulatory Notice 17-19 \- FINRA, accessed on February 3, 2026, [https://www.finra.org/sites/default/files/notice\_doc\_file\_ref/Regulatory-Notice-17-19.pdf](https://www.finra.org/sites/default/files/notice_doc_file_ref/Regulatory-Notice-17-19.pdf)  
32. ACCELERATED SETTLEMENT (T+1) \- State Street, accessed on February 3, 2026, [https://www.statestreet.com/web/insights/articles/documents/t1-functional-changes.pdf](https://www.statestreet.com/web/insights/articles/documents/t1-functional-changes.pdf)  
33. Securities Transaction Settlement Cycle \- Federal Register, accessed on February 3, 2026, [https://www.federalregister.gov/documents/2017/03/29/2017-06037/securities-transaction-settlement-cycle](https://www.federalregister.gov/documents/2017/03/29/2017-06037/securities-transaction-settlement-cycle)  
34. ACCELERATED SETTLEMENT (T+1) \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/-/media/Files/PDFs/T2/T1-Functional-Changes.pdf](https://www.dtcc.com/-/media/Files/PDFs/T2/T1-Functional-Changes.pdf)  
35. Self-Regulatory Organizations; National Securities Clearing Corporation; Order Approving of Proposed Rule Change To Amend the CNS Fails Charge in the NSCC Rules \- Federal Register, accessed on February 3, 2026, [https://www.federalregister.gov/documents/2025/12/01/2025-21645/self-regulatory-organizations-national-securities-clearing-corporation-order-approving-of-proposed](https://www.federalregister.gov/documents/2025/12/01/2025-21645/self-regulatory-organizations-national-securities-clearing-corporation-order-approving-of-proposed)  
36. SR 2025 \- \* 013 \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/Globals/PDFs/2025/September/05/SR-NSCC-2025-013](https://www.dtcc.com/Globals/PDFs/2025/September/05/SR-NSCC-2025-013)  
37. Order Approving of Proposed Rule Change to Amend the CNS Fails Charge in the NSCC Rules \- SEC.gov, accessed on February 3, 2026, [https://www.sec.gov/files/rules/sro/nscc/2025/34-104270.pdf](https://www.sec.gov/files/rules/sro/nscc/2025/34-104270.pdf)  
38. CTM —Match to Instruct Workflow \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/-/media/Files/Downloads/Institutional-Trade-Processing/Central-Trade-Manager/M2i-Factsheet.pdf](https://www.dtcc.com/-/media/Files/Downloads/Institutional-Trade-Processing/Central-Trade-Manager/M2i-Factsheet.pdf)  
39. DTCC's Match-to-Instruct workflow: Vital for T+1 trade settlement in the US \- ION Group, accessed on February 3, 2026, [https://iongroup.com/blog/markets/dtccs-match-to-instruct-workflow-vital-for-t1-trade-settlement-in-the-us/](https://iongroup.com/blog/markets/dtccs-match-to-instruct-workflow-vital-for-t1-trade-settlement-in-the-us/)  
40. Trade Affirmations: Key Questions Answered as T+1 Approaches \- DTCC, accessed on February 3, 2026, [https://www.dtcc.com/dtcc-connection/articles/2024/april/23/trade-affirmations-key-questions-answered-as-t1-approaches](https://www.dtcc.com/dtcc-connection/articles/2024/april/23/trade-affirmations-key-questions-answered-as-t1-approaches)