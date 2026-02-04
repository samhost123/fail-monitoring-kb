# Glossary

## Settlement Infrastructure

| Term | Definition | See Also |
|------|------------|----------|
| **CNS** | Continuous Net Settlement - NSCC's core netting and novation system | [[cns-system]] |
| **DTC** | Depository Trust Company - central securities depository | [[ims-profiles]] |
| **NSCC** | National Securities Clearing Corporation - central counterparty | [[cns-system]] |
| **IMS** | Inventory Management System - DTC's delivery sequencing system | [[ims-profiles]] |
| **OW** | Obligation Warehouse - bilateral settlement repository | [[obligation-warehouse]] |
| **CCP** | Central Counterparty - guarantor of novated trades | [[novation]] |
| **ATP** | Account Transaction Processor - DTC core processing | [[ims-profiles]] |

## Settlement Mechanics

| Term | Definition | See Also |
|------|------------|----------|
| **Novation** | Legal transformation of bilateral trade into CCP-guaranteed obligations | [[novation]] |
| **Netting** | Reduction of gross obligations to net (98% typical) | [[netting]] |
| **Night Cycle** | S-1 evening allocation (~11:30 PM ET, 50% volume) | [[night-cycle]] |
| **Day Cycle** | Settlement date continuous allocation | [[day-cycle]] |
| **T+1** | Trade date plus one business day (standard settlement) | [[t1-critical-deadlines]] |
| **DVP** | Delivery vs Payment - securities only on cash receipt | |
| **RVP** | Receive vs Payment - cash only on securities receipt | |
| **Partial Settlement** | Intraday partial delivery functionality | [[partial-settlement]] |
| **STP** | Straight-Through Processing ($0.37 cost) | |

## Fails

| Term | Definition | See Also |
|------|------------|----------|
| **Fail** | Trade that did not settle on expected settlement date | [[fail-lifecycle]] |
| **FTD** | Fail-to-Deliver - seller's failure to deliver securities | [[fail-to-deliver]] |
| **FTR** | Fail-to-Receive - buyer's failure to receive securities | [[fail-to-receive]] |
| **Aging** | Number of days a fail has been outstanding | [[prioritization-logic]] |
| **Offset** | Matching a receive fail against a deliver fail | [[offset-matching]] |
| **CNS Fails Charge** | Duration-based penalty (5%→15%→20%→100%) | [[cns-fails-charge]] |
| **Aged Fail** | Fail triggering Rule 15c3-1 capital deduction (S+5+) | [[aged-fail-deductions]] |

## CNS System

| Term | Definition | See Also |
|------|------------|----------|
| **Priority Groups** | CNS allocation hierarchy: 1=Corp Actions, 2=Buy-Ins, 3=Member Requests, 4=General | [[priority-groups]] |
| **Stock Borrow Program** | SBP - NSCC's securities lending facility | [[stock-borrow-program]] |
| **Retransmittal Notice** | Notification to oldest short in buy-in process | [[buy-in-mechanics]] |
| **CNS Position** | Net settlement obligation with NSCC | [[cns-system]] |

## IMS System

| Term | Definition | See Also |
|------|------------|----------|
| **IMS Profile** | Automation level: Green (high), Yellow (conditional), Red (manual) | [[ims-profiles]] |
| **Collateral Monitor** | CM - solvency calculation with haircuts | [[collateral-monitor]] |
| **Net Debit Cap** | NDC - liquidity limit ($2.15B individual, $2.85B family) | [[net-debit-cap]] |
| **Look-Ahead** | 2-minute gridlock resolution mini-netting | [[look-ahead-process]] |
| **SPP** | Settlement Progress Payment - intraday Fedwire liquidity valve | [[settlement-progress-payment]] |
| **RAD** | Receiver Authorized Delivery - delivery threshold controls | [[rad-thresholds]] |

## Obligation Warehouse

| Term | Definition | See Also |
|------|------------|----------|
| **Ex-Clearing** | Trades settled outside CNS (bilateral) | [[obligation-warehouse]] |
| **RECAPS** | Reconfirmation and Pricing Service - mark-to-market cycle | [[recaps]] |
| **CNS Eligibility Scan** | Daily check to "rescue" eligible OW trades to CNS | [[cns-eligibility-scan]] |
| **DK** | Don't Know - counterparty doesn't recognize trade | [[dk-processing]] |
| **Balance Order** | Adjustment entry in OW | [[obligation-warehouse]] |

## Regulation SHO

| Term | Definition | See Also |
|------|------------|----------|
| **Reg SHO** | SEC regulation governing short sales and close-outs | [[reg-sho-rule-204]] |
| **Rule 200** | Order marking requirements (Long/Short/Short Exempt) | |
| **Rule 203** | Locate requirement and threshold securities | [[threshold-securities]] |
| **Rule 204** | Mandatory close-out deadlines | [[reg-sho-rule-204]] |
| **Threshold Security** | Security with significant FTD positions (13-day close-out) | [[threshold-securities]] |
| **Penalty Box** | Pre-borrow restriction from close-out failure | [[penalty-box]] |
| **Locate** | Reasonable grounds to believe shares available for borrow | |
| **Pre-Borrow** | Actual borrow before short sale (Penalty Box requirement) | [[penalty-box]] |
| **Deemed to Own** | Rule 200(g) provision for bona fide recalls | [[recalls]] |
| **HTB** | Hard-to-Borrow - securities with high locate/borrow costs | |

## Close-Out Deadlines

| Term | Definition | See Also |
|------|------------|----------|
| **S+1** | Settlement date + 1 (short sale close-out) | [[close-out-matrix]] |
| **S+3** | Settlement date + 3 (long sale/market maker close-out) | [[close-out-matrix]] |
| **S+5** | Settlement date + 5 (capital deduction begins) | [[aged-fail-deductions]] |
| **S+13** | Settlement date + 13 (threshold mandatory purchase) | [[threshold-securities]] |
| **S+21** | Settlement date + 21 (100% capital deduction) | [[aged-fail-deductions]] |

## Rule 15c3-1 (Net Capital)

| Term | Definition | See Also |
|------|------------|----------|
| **Rule 15c3-1** | SEC Net Capital Rule - broker-dealer capital requirements | [[aged-fail-deductions]] |
| **Haircut** | Capital deduction percentage for aged fails | [[aged-fail-deductions]] |
| **Excess Net Capital** | Capital above minimum requirement | |

## Buy-Ins

| Term | Definition | See Also |
|------|------------|----------|
| **Buy-In** | Forced purchase to close fail position | [[buy-in-mechanics]] |
| **NSCC Rule 11** | CNS buy-in procedure | [[buy-in-mechanics]] |
| **FINRA Rule 11810** | Bilateral buy-in procedure (2-day notice) | [[buy-in-mechanics]] |
| **Buy-In Intent** | Notice elevating position to Priority Group 2 | [[buy-in-mechanics]] |

## Exceptions

| Term | Definition | See Also |
|------|------------|----------|
| **Reclaim** | Reversal of erroneous delivery | [[reclaims]] |
| **Recall** | Request to return borrowed securities | [[recalls]] |
| **Reason Code** | DTC code explaining reclaim/rejection (41-88) | [[dtc-reason-codes]] |
| **Matched Reclaim** | Reclaim with counterparty acknowledgment (RAD exempt) | [[reclaims]] |

## Prioritization

| Term | Definition | See Also |
|------|------------|----------|
| **Priority Score** | Weighted urgency calculation | [[prioritization-logic]] |
| **Escalation** | Routing to senior operations or compliance | [[escalation-paths]] |
| **Triage** | Initial fail assessment and queue assignment | [[new-fail-triage]] |

## Business Terms

| Term | Definition | See Also |
|------|------------|----------|
| **Counterparty** | The other party to a trade | |
| **CUSIP** | Committee on Uniform Securities Identification Procedures - security ID | |
| **Position** | Net quantity held in a security | |
| **Correspondent** | Client broker we clear for | |
| **Mark-to-Market** | Daily revaluation to current price | [[recaps]] |
| **Settlement Finality** | Irrevocable completion of settlement | [[cns-system]] |
