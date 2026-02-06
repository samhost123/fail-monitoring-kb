"""
Settlement Fails Data Simulator
Generates 20,000 realistic settlement fails for dashboard demonstration.
Based on the Equity Settlements Dashboard Design specification.

Enhanced with full SSI, client, product, and MTM data.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# =============================================================================
# REFERENCE DATA
# =============================================================================

# Coverage Desks with realistic distribution
COVERAGE_DESKS = {
    'Prime Brokerage': 0.35,
    'Institutional': 0.45,
    'Retail': 0.20
}

# Client Tiers
CLIENT_TIERS = {
    'Platinum': 0.05,
    'Gold': 0.15,
    'Silver': 0.35,
    'Bronze': 0.45
}

# Fail Direction
FAIL_DIRECTIONS = {
    'FTD': 0.55,  # Fail to Deliver
    'FTR': 0.45   # Fail to Receive
}

# Trade Types (for Reg SHO classification)
TRADE_TYPES = {
    'Long Sale': 0.50,
    'Short Sale': 0.25,
    'Market Making': 0.08,
    'Buy': 0.17
}

# Product Types
PRODUCT_TYPES = {
    'Equity': 0.70,
    'Fixed Income': 0.30
}

# Equity Subtypes
EQUITY_SUBTYPES = {
    'Common Stock': 0.65,
    'ETF': 0.20,
    'ADR': 0.08,
    'Preferred Stock': 0.04,
    'REIT': 0.03
}

# Fixed Income Subtypes
FI_SUBTYPES = {
    'Corporate Bond': 0.40,
    'Treasury': 0.25,
    'Municipal Bond': 0.15,
    'Agency Bond': 0.12,
    'MBS/ABS': 0.08
}

# Exception Categories with SWIFT codes
EXCEPTION_TAXONOMY = {
    'Inventory Shortage': {
        'weight': 0.35,
        'codes': ['LACK', 'LALO', 'MINO'],
        'dtc_codes': ['004', '005', '006'],
        'owner': 'Stock Loan / Inventory Mgmt',
        'description': 'Insufficient securities position'
    },
    'SSI Mismatch': {
        'weight': 0.25,
        'codes': ['DEPT', 'ICUS', 'SAFE', 'IEXE'],
        'dtc_codes': ['070', '071', '072'],
        'owner': 'Data Management / Client Service',
        'description': 'Settlement instruction discrepancy'
    },
    'Trade Discrepancy': {
        'weight': 0.20,
        'codes': ['DDEA', 'DQUA', 'DDAT', 'IIND', 'PODU'],
        'dtc_codes': ['056', '057', '058'],
        'owner': 'Middle Office / Sales Support',
        'description': 'Trade details mismatch'
    },
    'Counterparty Issue': {
        'weight': 0.12,
        'codes': ['DKNY', 'LATE', 'ADEA'],
        'dtc_codes': ['041', '042', '087'],
        'owner': 'Counterparty Relationship Mgmt',
        'description': 'Counterparty behavioral issue'
    },
    'Cash/Credit': {
        'weight': 0.08,
        'codes': ['MONY', 'CMON', 'CLAC'],
        'dtc_codes': ['054', '055'],
        'owner': 'Treasury / Credit Risk',
        'description': 'Insufficient funds or credit'
    }
}

# SWIFT Reason Code Descriptions
SWIFT_CODE_DESCRIPTIONS = {
    'LACK': 'Lack of securities',
    'LALO': 'Securities loaned out',
    'MINO': 'Minimum settlement amount not reached',
    'DEPT': 'Place of settlement mismatch',
    'ICUS': 'Receiving/delivering custodian mismatch',
    'SAFE': 'Safekeeping account mismatch',
    'IEXE': 'Instructing party mismatch',
    'DDEA': 'Deal price mismatch',
    'DQUA': 'Quantity mismatch',
    'DDAT': 'Settlement date mismatch',
    'IIND': 'Missing common reference',
    'PODU': 'Possible duplicate instruction',
    'DKNY': 'Counterparty does not know trade',
    'LATE': 'Instruction received late',
    'ADEA': 'Account servicer deadline missed',
    'MONY': 'Insufficient money',
    'CMON': 'Awaiting money from counterparty',
    'CLAC': 'Counterparty lacks funds'
}

# =============================================================================
# COUNTERPARTIES & CUSTODIANS
# =============================================================================

CUSTODIANS = [
    {'name': 'State Street', 'bic': 'SBOSUS33XXX', 'dtc_participant': '0997'},
    {'name': 'BNY Mellon', 'bic': 'IABORBBR', 'dtc_participant': '0901'},
    {'name': 'JP Morgan', 'bic': 'CHASUS33XXX', 'dtc_participant': '0902'},
    {'name': 'Northern Trust', 'bic': 'CNORUS44XXX', 'dtc_participant': '2669'},
    {'name': 'Citi', 'bic': 'CITIUS33XXX', 'dtc_participant': '0908'},
    {'name': 'HSBC', 'bic': 'MRMDUS33XXX', 'dtc_participant': '0158'},
    {'name': 'Brown Brothers Harriman', 'bic': 'BBHCUS33XXX', 'dtc_participant': '0443'},
    {'name': 'US Bank', 'bic': 'UABORBBR', 'dtc_participant': '0357'},
]

PB_COUNTERPARTIES = [
    {'name': 'Goldman Sachs PB', 'bic': 'GOLDUS33XXX', 'dtc_participant': '0005'},
    {'name': 'Morgan Stanley PB', 'bic': 'MABORBBR', 'dtc_participant': '0050'},
    {'name': 'JP Morgan PB', 'bic': 'CHASUS33PBX', 'dtc_participant': '0352'},
    {'name': 'Barclays PB', 'bic': 'BABORBBR', 'dtc_participant': '0229'},
    {'name': 'UBS PB', 'bic': 'UBSWUS33XXX', 'dtc_participant': '0642'},
    {'name': 'Deutsche Bank PB', 'bic': 'DEUTUS33XXX', 'dtc_participant': '0355'},
    {'name': 'BofA Securities', 'bic': 'BABORBBR', 'dtc_participant': '0161'},
]

RETAIL_BROKERS = [
    {'name': 'Schwab', 'bic': 'SCHBUS33XXX', 'dtc_participant': '0164'},
    {'name': 'Fidelity', 'bic': 'FIDEUS33XXX', 'dtc_participant': '0226'},
    {'name': 'TD Ameritrade', 'bic': 'TDAMXXXX', 'dtc_participant': '0188'},
    {'name': 'E*TRADE', 'bic': 'ETRDUS33XXX', 'dtc_participant': '0385'},
    {'name': 'Robinhood', 'bic': 'ROBHUS33XXX', 'dtc_participant': '6769'},
    {'name': 'Interactive Brokers', 'bic': 'IBKRUS33XXX', 'dtc_participant': '0534'},
]

# =============================================================================
# SECURITIES DATABASE
# =============================================================================

EQUITY_SECURITIES = [
    # Large Cap - Easy to Borrow
    {'cusip': '037833100', 'isin': 'US0378331005', 'sedol': '2046251', 'symbol': 'AAPL',
     'name': 'Apple Inc', 'price_range': (170, 195), 'htb': False, 'sector': 'Technology',
     'exchange': 'NASDAQ', 'country': 'US', 'currency': 'USD', 'subtype': 'Common Stock'},
    {'cusip': '594918104', 'isin': 'US5949181045', 'sedol': '2588173', 'symbol': 'MSFT',
     'name': 'Microsoft Corp', 'price_range': (380, 420), 'htb': False, 'sector': 'Technology',
     'exchange': 'NASDAQ', 'country': 'US', 'currency': 'USD', 'subtype': 'Common Stock'},
    {'cusip': '02079K305', 'isin': 'US02079K3059', 'sedol': 'BYVY8G0', 'symbol': 'GOOGL',
     'name': 'Alphabet Inc', 'price_range': (140, 165), 'htb': False, 'sector': 'Technology',
     'exchange': 'NASDAQ', 'country': 'US', 'currency': 'USD', 'subtype': 'Common Stock'},
    {'cusip': '023135106', 'isin': 'US0231351067', 'sedol': '2000019', 'symbol': 'AMZN',
     'name': 'Amazon.com Inc', 'price_range': (175, 195), 'htb': False, 'sector': 'Consumer Discretionary',
     'exchange': 'NASDAQ', 'country': 'US', 'currency': 'USD', 'subtype': 'Common Stock'},
    {'cusip': '67066G104', 'isin': 'US67066G1040', 'sedol': '2379504', 'symbol': 'NVDA',
     'name': 'NVIDIA Corp', 'price_range': (800, 950), 'htb': False, 'sector': 'Technology',
     'exchange': 'NASDAQ', 'country': 'US', 'currency': 'USD', 'subtype': 'Common Stock'},
    {'cusip': '88160R101', 'isin': 'US88160R1014', 'sedol': 'B616C79', 'symbol': 'TSLA',
     'name': 'Tesla Inc', 'price_range': (240, 280), 'htb': False, 'sector': 'Consumer Discretionary',
     'exchange': 'NASDAQ', 'country': 'US', 'currency': 'USD', 'subtype': 'Common Stock'},
    {'cusip': '30303M102', 'isin': 'US30303M1027', 'sedol': 'B7TL820', 'symbol': 'META',
     'name': 'Meta Platforms', 'price_range': (480, 550), 'htb': False, 'sector': 'Technology',
     'exchange': 'NASDAQ', 'country': 'US', 'currency': 'USD', 'subtype': 'Common Stock'},
    {'cusip': '46625H100', 'isin': 'US46625H1005', 'sedol': '2190385', 'symbol': 'JPM',
     'name': 'JPMorgan Chase', 'price_range': (190, 220), 'htb': False, 'sector': 'Financials',
     'exchange': 'NYSE', 'country': 'US', 'currency': 'USD', 'subtype': 'Common Stock'},
    {'cusip': '91324P102', 'isin': 'US91324P1021', 'sedol': '2917766', 'symbol': 'UNH',
     'name': 'UnitedHealth Group', 'price_range': (520, 580), 'htb': False, 'sector': 'Healthcare',
     'exchange': 'NYSE', 'country': 'US', 'currency': 'USD', 'subtype': 'Common Stock'},
    {'cusip': '478160104', 'isin': 'US4781601046', 'sedol': '2475833', 'symbol': 'JNJ',
     'name': 'Johnson & Johnson', 'price_range': (155, 175), 'htb': False, 'sector': 'Healthcare',
     'exchange': 'NYSE', 'country': 'US', 'currency': 'USD', 'subtype': 'Common Stock'},
    # ETFs
    {'cusip': '464287200', 'isin': 'US4642872000', 'sedol': '2840215', 'symbol': 'IWM',
     'name': 'iShares Russell 2000 ETF', 'price_range': (195, 220), 'htb': False, 'sector': 'ETF',
     'exchange': 'NYSE', 'country': 'US', 'currency': 'USD', 'subtype': 'ETF'},
    {'cusip': '78462F103', 'isin': 'US78462F1030', 'sedol': '2840216', 'symbol': 'SPY',
     'name': 'SPDR S&P 500 ETF', 'price_range': (480, 520), 'htb': False, 'sector': 'ETF',
     'exchange': 'NYSE', 'country': 'US', 'currency': 'USD', 'subtype': 'ETF'},
    {'cusip': '46090E103', 'isin': 'US46090E1038', 'sedol': 'BYY8XS5', 'symbol': 'QQQ',
     'name': 'Invesco QQQ Trust', 'price_range': (420, 470), 'htb': False, 'sector': 'ETF',
     'exchange': 'NASDAQ', 'country': 'US', 'currency': 'USD', 'subtype': 'ETF'},
    # ADRs
    {'cusip': '88579Y101', 'isin': 'US88579Y1010', 'sedol': 'B5B2106', 'symbol': 'BABA',
     'name': 'Alibaba Group ADR', 'price_range': (75, 95), 'htb': False, 'sector': 'Consumer Discretionary',
     'exchange': 'NYSE', 'country': 'CN', 'currency': 'USD', 'subtype': 'ADR'},
    {'cusip': '90138F102', 'isin': 'US90138F1021', 'sedol': 'BYY8Y18', 'symbol': 'TSM',
     'name': 'Taiwan Semiconductor ADR', 'price_range': (140, 180), 'htb': False, 'sector': 'Technology',
     'exchange': 'NYSE', 'country': 'TW', 'currency': 'USD', 'subtype': 'ADR'},
    # Hard to Borrow (HTB) - Meme stocks, heavily shorted
    {'cusip': '36467W109', 'isin': 'US36467W1099', 'sedol': '2326754', 'symbol': 'GME',
     'name': 'GameStop Corp', 'price_range': (15, 30), 'htb': True, 'sector': 'Consumer Discretionary',
     'exchange': 'NYSE', 'country': 'US', 'currency': 'USD', 'subtype': 'Common Stock'},
    {'cusip': '00165C104', 'isin': 'US00165C1045', 'sedol': 'BYV2WK4', 'symbol': 'AMC',
     'name': 'AMC Entertainment', 'price_range': (4, 8), 'htb': True, 'sector': 'Consumer Discretionary',
     'exchange': 'NYSE', 'country': 'US', 'currency': 'USD', 'subtype': 'Common Stock'},
    {'cusip': '75886F107', 'isin': 'US75886F1075', 'sedol': 'BMWXLX6', 'symbol': 'RBLX',
     'name': 'Roblox Corp', 'price_range': (38, 52), 'htb': True, 'sector': 'Technology',
     'exchange': 'NYSE', 'country': 'US', 'currency': 'USD', 'subtype': 'Common Stock'},
    {'cusip': '824348106', 'isin': 'US8243481061', 'sedol': 'B17TH16', 'symbol': 'SHAK',
     'name': 'Shake Shack', 'price_range': (85, 110), 'htb': True, 'sector': 'Consumer Discretionary',
     'exchange': 'NYSE', 'country': 'US', 'currency': 'USD', 'subtype': 'Common Stock'},
    # REITs
    {'cusip': '756109104', 'isin': 'US7561091049', 'sedol': '2724193', 'symbol': 'O',
     'name': 'Realty Income Corp', 'price_range': (52, 62), 'htb': False, 'sector': 'Real Estate',
     'exchange': 'NYSE', 'country': 'US', 'currency': 'USD', 'subtype': 'REIT'},
    # Preferred Stock
    {'cusip': '06051GHF2', 'isin': 'US06051GHF28', 'sedol': 'BM9BQV9', 'symbol': 'BAC-PL',
     'name': 'Bank of America Preferred L', 'price_range': (23, 27), 'htb': False, 'sector': 'Financials',
     'exchange': 'NYSE', 'country': 'US', 'currency': 'USD', 'subtype': 'Preferred Stock'},
]

FI_SECURITIES = [
    # Corporate Bonds
    {'cusip': '037833CU2', 'isin': 'US037833CU26', 'symbol': 'AAPL 2.40 05/03/23',
     'name': 'Apple Inc 2.40% 2030', 'price_range': (95, 102), 'htb': False, 'sector': 'Technology',
     'coupon': 2.40, 'maturity': '2030-05-03', 'rating': 'AA+', 'subtype': 'Corporate Bond', 'currency': 'USD'},
    {'cusip': '594918BW3', 'isin': 'US594918BW39', 'symbol': 'MSFT 2.525 06/01/50',
     'name': 'Microsoft Corp 2.525% 2050', 'price_range': (75, 85), 'htb': False, 'sector': 'Technology',
     'coupon': 2.525, 'maturity': '2050-06-01', 'rating': 'AAA', 'subtype': 'Corporate Bond', 'currency': 'USD'},
    {'cusip': '46625HJY5', 'isin': 'US46625HJY53', 'symbol': 'JPM 4.125 12/15/26',
     'name': 'JPMorgan Chase 4.125% 2026', 'price_range': (98, 103), 'htb': False, 'sector': 'Financials',
     'coupon': 4.125, 'maturity': '2026-12-15', 'rating': 'A-', 'subtype': 'Corporate Bond', 'currency': 'USD'},
    {'cusip': '172967KK5', 'isin': 'US172967KK57', 'symbol': 'C 3.887 10/10/24',
     'name': 'Citigroup 3.887% 2028', 'price_range': (94, 100), 'htb': False, 'sector': 'Financials',
     'coupon': 3.887, 'maturity': '2028-10-10', 'rating': 'BBB+', 'subtype': 'Corporate Bond', 'currency': 'USD'},
    # Treasuries
    {'cusip': '912810TM0', 'isin': 'US912810TM08', 'symbol': 'T 4.5 02/15/36',
     'name': 'US Treasury 4.5% 2036', 'price_range': (102, 108), 'htb': False, 'sector': 'Government',
     'coupon': 4.5, 'maturity': '2036-02-15', 'rating': 'AAA', 'subtype': 'Treasury', 'currency': 'USD'},
    {'cusip': '91282CJL0', 'isin': 'US91282CJL00', 'symbol': 'T 4.25 11/15/34',
     'name': 'US Treasury 4.25% 2034', 'price_range': (98, 105), 'htb': False, 'sector': 'Government',
     'coupon': 4.25, 'maturity': '2034-11-15', 'rating': 'AAA', 'subtype': 'Treasury', 'currency': 'USD'},
    {'cusip': '912810RZ3', 'isin': 'US912810RZ30', 'symbol': 'T 2.875 05/15/52',
     'name': 'US Treasury 2.875% 2052', 'price_range': (68, 78), 'htb': False, 'sector': 'Government',
     'coupon': 2.875, 'maturity': '2052-05-15', 'rating': 'AAA', 'subtype': 'Treasury', 'currency': 'USD'},
    # Municipal Bonds
    {'cusip': '64966QFJ9', 'isin': 'US64966QFJ94', 'symbol': 'NYC GO 5.0 03/01/35',
     'name': 'New York City GO 5.0% 2035', 'price_range': (105, 112), 'htb': False, 'sector': 'Municipal',
     'coupon': 5.0, 'maturity': '2035-03-01', 'rating': 'AA', 'subtype': 'Municipal Bond', 'currency': 'USD'},
    {'cusip': '13063DAD2', 'isin': 'US13063DAD21', 'symbol': 'CA GO 4.0 04/01/38',
     'name': 'California State GO 4.0% 2038', 'price_range': (95, 103), 'htb': False, 'sector': 'Municipal',
     'coupon': 4.0, 'maturity': '2038-04-01', 'rating': 'AA-', 'subtype': 'Municipal Bond', 'currency': 'USD'},
    # Agency Bonds
    {'cusip': '3135G0V34', 'isin': 'US3135G0V340', 'symbol': 'FNMA 2.625 09/06/24',
     'name': 'Fannie Mae 2.625% 2029', 'price_range': (94, 99), 'htb': False, 'sector': 'Agency',
     'coupon': 2.625, 'maturity': '2029-09-06', 'rating': 'AA+', 'subtype': 'Agency Bond', 'currency': 'USD'},
    {'cusip': '3130A2UW2', 'isin': 'US3130A2UW25', 'symbol': 'FHLB 3.25 11/16/28',
     'name': 'Federal Home Loan Bank 3.25% 2028', 'price_range': (96, 101), 'htb': False, 'sector': 'Agency',
     'coupon': 3.25, 'maturity': '2028-11-16', 'rating': 'AA+', 'subtype': 'Agency Bond', 'currency': 'USD'},
]

# =============================================================================
# CLIENT DATABASE
# =============================================================================

CLIENTS = {
    'Platinum': [
        {'name': 'Citadel Advisors', 'lei': '549300DZ0RXVLF15VZ23', 'account': 'CITA-001', 'rm': 'Sarah Chen', 'rm_phone': '+1-212-555-1001'},
        {'name': 'Millennium Management', 'lei': '549300ZSHL5TFME4CF84', 'account': 'MILL-001', 'rm': 'James Wilson', 'rm_phone': '+1-212-555-1002'},
        {'name': 'Point72 Asset Mgmt', 'lei': '549300QN9CVHXD2XZX15', 'account': 'PT72-001', 'rm': 'Sarah Chen', 'rm_phone': '+1-212-555-1001'},
        {'name': 'Two Sigma Investments', 'lei': '549300DRQQI6VXKMKT09', 'account': 'TWOS-001', 'rm': 'Michael Brown', 'rm_phone': '+1-212-555-1003'},
        {'name': 'DE Shaw & Co', 'lei': '549300WR4GQBZ4QN7T17', 'account': 'DESH-001', 'rm': 'Michael Brown', 'rm_phone': '+1-212-555-1003'},
        {'name': 'Renaissance Technologies', 'lei': '549300WOIFUSNYH0FL22', 'account': 'RENT-001', 'rm': 'Emily Rodriguez', 'rm_phone': '+1-212-555-1004'},
        {'name': 'Bridgewater Associates', 'lei': '549300IPG1VXWQJ41T18', 'account': 'BRID-001', 'rm': 'Emily Rodriguez', 'rm_phone': '+1-212-555-1004'},
        {'name': 'AQR Capital', 'lei': '549300P38TF6ND8GN420', 'account': 'AQRC-001', 'rm': 'James Wilson', 'rm_phone': '+1-212-555-1002'},
    ],
    'Gold': [
        {'name': 'Viking Global', 'lei': '549300K4RPYML8LZLN14', 'account': 'VIKG-001', 'rm': 'David Kim', 'rm_phone': '+1-212-555-2001'},
        {'name': 'Lone Pine Capital', 'lei': '549300TPSVXCB0FWXP86', 'account': 'LONE-001', 'rm': 'David Kim', 'rm_phone': '+1-212-555-2001'},
        {'name': 'Tiger Global', 'lei': '549300X2BSCVQ0SPMQ47', 'account': 'TIGR-001', 'rm': 'Lisa Park', 'rm_phone': '+1-212-555-2002'},
        {'name': 'Coatue Management', 'lei': '549300DMXJ7BZ5F4SV95', 'account': 'COAT-001', 'rm': 'Lisa Park', 'rm_phone': '+1-212-555-2002'},
        {'name': 'Third Point LLC', 'lei': '549300YWGME6LBV34J65', 'account': 'THRD-001', 'rm': 'Robert Martinez', 'rm_phone': '+1-212-555-2003'},
        {'name': 'Elliott Management', 'lei': '549300GHQVM86R3X5L14', 'account': 'ELLI-001', 'rm': 'Robert Martinez', 'rm_phone': '+1-212-555-2003'},
        {'name': 'Baupost Group', 'lei': '549300BVXG5TQMU6ZL08', 'account': 'BAUP-001', 'rm': 'Jennifer Lee', 'rm_phone': '+1-212-555-2004'},
        {'name': 'Pershing Square', 'lei': '549300PJMK9QHVLVD321', 'account': 'PERS-001', 'rm': 'Jennifer Lee', 'rm_phone': '+1-212-555-2004'},
        {'name': 'ValueAct Capital', 'lei': '549300RSXH4LP2VQ3M98', 'account': 'VALU-001', 'rm': 'David Kim', 'rm_phone': '+1-212-555-2001'},
        {'name': 'Jana Partners', 'lei': '549300QWFVDZ7KQJF893', 'account': 'JANA-001', 'rm': 'Lisa Park', 'rm_phone': '+1-212-555-2002'},
    ],
    'Silver': [
        {'name': 'Capital Group', 'lei': '549300FKHWKPTLV5GQ15', 'account': 'CAPG-001', 'rm': 'Team Alpha', 'rm_phone': '+1-212-555-3001'},
        {'name': 'Fidelity Investments', 'lei': '549300FMRL6YKPC1XN43', 'account': 'FIDE-001', 'rm': 'Team Alpha', 'rm_phone': '+1-212-555-3001'},
        {'name': 'Vanguard Group', 'lei': '549300JQT6YLT4QWJS35', 'account': 'VANG-001', 'rm': 'Team Beta', 'rm_phone': '+1-212-555-3002'},
        {'name': 'BlackRock', 'lei': '549300LRIF3NWCU26A80', 'account': 'BLKR-001', 'rm': 'Team Beta', 'rm_phone': '+1-212-555-3002'},
        {'name': 'T Rowe Price', 'lei': '549300PSZ78SGGRK3T08', 'account': 'TROW-001', 'rm': 'Team Gamma', 'rm_phone': '+1-212-555-3003'},
        {'name': 'Wellington Management', 'lei': '549300ZH4NHJBMJQ7N43', 'account': 'WELL-001', 'rm': 'Team Gamma', 'rm_phone': '+1-212-555-3003'},
        {'name': 'PIMCO', 'lei': '549300CPMJ1J4LMVZQ15', 'account': 'PIMC-001', 'rm': 'Team Delta', 'rm_phone': '+1-212-555-3004'},
        {'name': 'Invesco', 'lei': '549300GH65RVGX5UCP37', 'account': 'INVE-001', 'rm': 'Team Delta', 'rm_phone': '+1-212-555-3004'},
        {'name': 'Franklin Templeton', 'lei': '549300VM8GFL6NGXLR19', 'account': 'FRAN-001', 'rm': 'Team Alpha', 'rm_phone': '+1-212-555-3001'},
        {'name': 'MFS Investment', 'lei': '549300GHKL9RNX7FJL51', 'account': 'MFSI-001', 'rm': 'Team Beta', 'rm_phone': '+1-212-555-3002'},
        {'name': 'Nuveen', 'lei': '549300LMRV7KQN1GVL58', 'account': 'NUVE-001', 'rm': 'Team Gamma', 'rm_phone': '+1-212-555-3003'},
        {'name': 'American Century', 'lei': '549300HJVBMLPQJD4N13', 'account': 'AMCN-001', 'rm': 'Team Delta', 'rm_phone': '+1-212-555-3004'},
    ],
    'Bronze': [
        {'name': 'Regional Bank Trust A', 'lei': '549300AAAAAAAAAAA001', 'account': 'RBTA-001', 'rm': 'Operations Desk', 'rm_phone': '+1-212-555-4000'},
        {'name': 'Regional Bank Trust B', 'lei': '549300AAAAAAAAAAA002', 'account': 'RBTB-001', 'rm': 'Operations Desk', 'rm_phone': '+1-212-555-4000'},
        {'name': 'Small Cap Fund I', 'lei': '549300AAAAAAAAAAA003', 'account': 'SCFI-001', 'rm': 'Operations Desk', 'rm_phone': '+1-212-555-4000'},
        {'name': 'Small Cap Fund II', 'lei': '549300AAAAAAAAAAA004', 'account': 'SCF2-001', 'rm': 'Operations Desk', 'rm_phone': '+1-212-555-4000'},
        {'name': 'Pension Fund Alpha', 'lei': '549300AAAAAAAAAAA005', 'account': 'PENA-001', 'rm': 'Operations Desk', 'rm_phone': '+1-212-555-4000'},
        {'name': 'Pension Fund Beta', 'lei': '549300AAAAAAAAAAA006', 'account': 'PENB-001', 'rm': 'Operations Desk', 'rm_phone': '+1-212-555-4000'},
        {'name': 'Insurance Portfolio A', 'lei': '549300AAAAAAAAAAA007', 'account': 'INSA-001', 'rm': 'Operations Desk', 'rm_phone': '+1-212-555-4000'},
        {'name': 'Insurance Portfolio B', 'lei': '549300AAAAAAAAAAA008', 'account': 'INSB-001', 'rm': 'Operations Desk', 'rm_phone': '+1-212-555-4000'},
        {'name': 'Family Office X', 'lei': '549300AAAAAAAAAAA009', 'account': 'FAMX-001', 'rm': 'Operations Desk', 'rm_phone': '+1-212-555-4000'},
        {'name': 'Family Office Y', 'lei': '549300AAAAAAAAAAA010', 'account': 'FAMY-001', 'rm': 'Operations Desk', 'rm_phone': '+1-212-555-4000'},
        {'name': 'Endowment Fund 1', 'lei': '549300AAAAAAAAAAA011', 'account': 'END1-001', 'rm': 'Operations Desk', 'rm_phone': '+1-212-555-4000'},
        {'name': 'Endowment Fund 2', 'lei': '549300AAAAAAAAAAA012', 'account': 'END2-001', 'rm': 'Operations Desk', 'rm_phone': '+1-212-555-4000'},
        {'name': 'Municipal Fund A', 'lei': '549300AAAAAAAAAAA013', 'account': 'MUNA-001', 'rm': 'Operations Desk', 'rm_phone': '+1-212-555-4000'},
        {'name': 'Municipal Fund B', 'lei': '549300AAAAAAAAAAA014', 'account': 'MUNB-001', 'rm': 'Operations Desk', 'rm_phone': '+1-212-555-4000'},
        {'name': 'Credit Union Trust', 'lei': '549300AAAAAAAAAAA015', 'account': 'CRUT-001', 'rm': 'Operations Desk', 'rm_phone': '+1-212-555-4000'},
        {'name': 'Community Bank', 'lei': '549300AAAAAAAAAAA016', 'account': 'COMB-001', 'rm': 'Operations Desk', 'rm_phone': '+1-212-555-4000'},
    ]
}

# Place of Settlement codes
PSET_CODES = {
    'US': 'DTCYUS33XXX',  # DTC
    'UK': 'CABORBBR',     # CREST
    'EU': 'ECLABORB',     # Euroclear
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def weighted_choice(choices_dict):
    """Select from dict where values are weights."""
    items = list(choices_dict.keys())
    weights = list(choices_dict.values())
    return random.choices(items, weights=weights, k=1)[0]


def generate_trade_id():
    """Generate realistic trade ID."""
    prefix = random.choice(['TRD', 'EQT', 'SET', 'CNS', 'OTC'])
    return f"{prefix}-{random.randint(10000000, 99999999)}"


def generate_cns_control():
    """Generate CNS control number."""
    return f"CNS{random.randint(100000000, 999999999)}"


def generate_broker_ref():
    """Generate broker reference."""
    prefix = random.choice(['BR', 'EX', 'OR'])
    return f"{prefix}{random.randint(1000000, 9999999)}"


def generate_swift_ref():
    """Generate SWIFT message reference."""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=16))


def generate_safekeeping_account():
    """Generate safekeeping account number."""
    return f"{random.randint(10000, 99999)}-{random.randint(1000, 9999)}"


# =============================================================================
# MAIN GENERATOR
# =============================================================================

def generate_fails(n_fails=20000, base_date=None):
    """
    Generate n settlement fails with realistic distributions and full data.
    """
    if base_date is None:
        base_date = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

    fails = []

    for i in range(n_fails):
        # =====================================================================
        # BASIC IDENTIFIERS
        # =====================================================================
        trade_id = generate_trade_id()
        cns_control_number = generate_cns_control()
        broker_reference = generate_broker_ref()
        swift_reference = generate_swift_ref()

        # =====================================================================
        # PRODUCT TYPE & SECURITY
        # =====================================================================
        product_type = weighted_choice(PRODUCT_TYPES)

        if product_type == 'Equity':
            security = random.choice(EQUITY_SECURITIES)
            subtype = security.get('subtype', weighted_choice(EQUITY_SUBTYPES))
        else:
            security = random.choice(FI_SECURITIES)
            subtype = security.get('subtype', weighted_choice(FI_SUBTYPES))

        # =====================================================================
        # COVERAGE DESK
        # =====================================================================
        desk = weighted_choice(COVERAGE_DESKS)

        # Client Tier (Platinum clients more likely in PB)
        if desk == 'Prime Brokerage':
            tier_weights = {'Platinum': 0.15, 'Gold': 0.30, 'Silver': 0.35, 'Bronze': 0.20}
        elif desk == 'Institutional':
            tier_weights = {'Platinum': 0.05, 'Gold': 0.15, 'Silver': 0.40, 'Bronze': 0.40}
        else:  # Retail
            tier_weights = {'Platinum': 0.01, 'Gold': 0.04, 'Silver': 0.25, 'Bronze': 0.70}

        client_tier = weighted_choice(tier_weights)
        client = random.choice(CLIENTS[client_tier])

        # =====================================================================
        # COUNTERPARTY / CUSTODIAN
        # =====================================================================
        if desk == 'Prime Brokerage':
            counterparty = random.choice(PB_COUNTERPARTIES)
        elif desk == 'Institutional':
            counterparty = random.choice(CUSTODIANS)
        else:
            counterparty = random.choice(RETAIL_BROKERS)

        # =====================================================================
        # TRADE DETAILS
        # =====================================================================
        direction = weighted_choice(FAIL_DIRECTIONS)
        trade_type = weighted_choice(TRADE_TYPES)

        # Pricing
        trade_price = round(random.uniform(*security['price_range']), 4)
        # Current market price (for MTM) - slight variation from trade price
        price_change_pct = random.uniform(-0.05, 0.05)  # +/- 5%
        current_price = round(trade_price * (1 + price_change_pct), 4)

        # Quantity - varies by desk and product
        if desk == 'Prime Brokerage':
            if product_type == 'Equity':
                quantity = random.randint(1000, 100000)
            else:
                quantity = random.randint(100000, 5000000)  # FI in face value
        elif desk == 'Institutional':
            if product_type == 'Equity':
                quantity = random.randint(500, 50000)
            else:
                quantity = random.randint(50000, 2000000)
        else:
            if product_type == 'Equity':
                quantity = random.randint(10, 5000)
            else:
                quantity = random.randint(1000, 100000)

        # Value calculations
        trade_value = round(quantity * trade_price, 2)
        market_value = round(quantity * current_price, 2)

        # MTM (Mark to Market) - unrealized P&L
        if direction == 'FTD':  # We owe - price up is bad
            mtm_pnl = round(trade_value - market_value, 2)
        else:  # FTR - We're owed - price up is good
            mtm_pnl = round(market_value - trade_value, 2)

        # =====================================================================
        # DATES & AGING
        # =====================================================================
        age_weights = {
            1: 0.45, 2: 0.20, 3: 0.12, 4: 0.08, 5: 0.06, 6: 0.04, 7: 0.02,
            **{d: 0.003 for d in range(8, 35)},
            **{d: 0.0005 for d in range(35, 45)}
        }
        age_days = weighted_choice(age_weights)

        settlement_date = base_date - timedelta(days=age_days)
        trade_date = settlement_date - timedelta(days=1)

        # Aging bucket
        if age_days <= 1:
            aging_bucket = 'T+1 (Fresh)'
        elif age_days <= 4:
            aging_bucket = 'T+2 to T+4 (Warning)'
        elif age_days <= 34:
            aging_bucket = 'T+5 to T+34 (Aged)'
        else:
            aging_bucket = 'T+35+ (Deemed-to-Own)'

        # =====================================================================
        # EXCEPTION CATEGORY & REASON CODES
        # =====================================================================
        exception_category = weighted_choice({k: v['weight'] for k, v in EXCEPTION_TAXONOMY.items()})
        exception_info = EXCEPTION_TAXONOMY[exception_category]
        reason_code = random.choice(exception_info['codes'])
        dtc_reason_code = random.choice(exception_info['dtc_codes'])
        reason_description = SWIFT_CODE_DESCRIPTIONS.get(reason_code, 'Unknown')
        operational_owner = exception_info['owner']

        # =====================================================================
        # SSI (STANDING SETTLEMENT INSTRUCTIONS)
        # =====================================================================
        # Our side SSI
        our_agent_bic = 'OURFIRMUS3XXX'
        our_safekeeping_account = generate_safekeeping_account()
        our_dtc_participant = '0999'

        # Counterparty SSI
        cpty_agent_bic = counterparty['bic']
        cpty_safekeeping_account = generate_safekeeping_account()
        cpty_dtc_participant = counterparty['dtc_participant']

        # Place of Settlement
        pset = PSET_CODES['US']

        # SSI Mismatch details (if applicable)
        if exception_category == 'SSI Mismatch':
            ssi_mismatch_field = random.choice(['Agent BIC', 'Safekeeping Account', 'PSET', 'Account Number'])
            ssi_expected = f"Expected: {our_agent_bic}" if ssi_mismatch_field == 'Agent BIC' else f"Expected: {our_safekeeping_account}"
            ssi_received = f"Received: {cpty_agent_bic}X" if ssi_mismatch_field == 'Agent BIC' else f"Received: {cpty_safekeeping_account}X"
        else:
            ssi_mismatch_field = None
            ssi_expected = None
            ssi_received = None

        # =====================================================================
        # CNS & REGULATORY FLAGS
        # =====================================================================
        if desk == 'Prime Brokerage':
            is_cns = random.random() > 0.3
        else:
            is_cns = random.random() > 0.1

        is_htb = security.get('htb', False)
        if exception_category == 'Inventory Shortage' and not is_htb:
            is_htb = random.random() < 0.15

        is_threshold_security = is_htb and random.random() < 0.3

        # Reg SHO calculations
        if direction == 'FTD':
            if trade_type == 'Short Sale':
                closeout_deadline = 3
            elif trade_type == 'Market Making':
                closeout_deadline = 6
            else:
                closeout_deadline = 5
            days_to_closeout = closeout_deadline - age_days
            is_reg_sho_at_risk = days_to_closeout <= 1 and age_days >= (closeout_deadline - 1)
        else:
            closeout_deadline = None
            days_to_closeout = None
            is_reg_sho_at_risk = False

        # =====================================================================
        # PRIORITY SCORE
        # =====================================================================
        priority_score = 0
        if client_tier == 'Platinum':
            priority_score += 40
        elif client_tier == 'Gold':
            priority_score += 25
        elif client_tier == 'Silver':
            priority_score += 10
        if is_reg_sho_at_risk:
            priority_score += 50
        if is_htb:
            priority_score += 15
        if trade_value > 10_000_000:
            priority_score += 30
        elif trade_value > 1_000_000:
            priority_score += 20
        elif trade_value > 500_000:
            priority_score += 10
        if age_days > 3:
            priority_score += age_days * 2
        if abs(mtm_pnl) > 100_000:
            priority_score += 15

        # =====================================================================
        # BUILD RECORD
        # =====================================================================
        fail = {
            # Identifiers
            'trade_id': trade_id,
            'cns_control_number': cns_control_number,
            'broker_reference': broker_reference,
            'swift_reference': swift_reference,

            # Dates
            'trade_date': trade_date.strftime('%Y-%m-%d'),
            'settlement_date': settlement_date.strftime('%Y-%m-%d'),
            'age_days': age_days,
            'aging_bucket': aging_bucket,

            # Product
            'product_type': product_type,
            'product_subtype': subtype,
            'cusip': security['cusip'],
            'isin': security.get('isin', ''),
            'sedol': security.get('sedol', ''),
            'symbol': security['symbol'],
            'security_name': security['name'],
            'sector': security.get('sector', ''),
            'exchange': security.get('exchange', ''),
            'currency': security.get('currency', 'USD'),

            # Quantity & Pricing
            'quantity': quantity,
            'trade_price': trade_price,
            'current_price': current_price,
            'trade_value': trade_value,
            'market_value': market_value,
            'mtm_pnl': mtm_pnl,

            # Trade Classification
            'direction': direction,
            'trade_type': trade_type,
            'desk': desk,

            # Client
            'client_name': client['name'],
            'client_lei': client['lei'],
            'client_account': client['account'],
            'client_tier': client_tier,
            'relationship_manager': client['rm'],
            'rm_phone': client['rm_phone'],

            # Counterparty
            'counterparty_name': counterparty['name'],
            'counterparty_bic': counterparty['bic'],
            'counterparty_dtc_participant': counterparty['dtc_participant'],

            # SSI - Our Side
            'our_agent_bic': our_agent_bic,
            'our_safekeeping_account': our_safekeeping_account,
            'our_dtc_participant': our_dtc_participant,

            # SSI - Counterparty Side
            'cpty_agent_bic': cpty_agent_bic,
            'cpty_safekeeping_account': cpty_safekeeping_account,
            'cpty_dtc_participant': cpty_dtc_participant,

            # SSI - Common
            'pset': pset,
            'ssi_mismatch_field': ssi_mismatch_field,
            'ssi_expected': ssi_expected,
            'ssi_received': ssi_received,

            # Exception Details
            'exception_category': exception_category,
            'swift_reason_code': reason_code,
            'dtc_reason_code': dtc_reason_code,
            'reason_description': reason_description,
            'operational_owner': operational_owner,

            # Settlement Flags
            'is_cns': is_cns,
            'settlement_type': 'CNS' if is_cns else 'Trade-for-Trade',

            # Inventory & Reg SHO
            'is_htb': is_htb,
            'borrowability': 'HTB' if is_htb else 'ETB',
            'is_threshold_security': is_threshold_security,
            'is_reg_sho_at_risk': is_reg_sho_at_risk,
            'closeout_deadline_days': closeout_deadline,
            'days_to_closeout': days_to_closeout,

            # Priority
            'priority_score': priority_score,
        }

        fails.append(fail)

    df = pd.DataFrame(fails)
    df = df.sort_values('priority_score', ascending=False).reset_index(drop=True)

    return df


def generate_summary_stats(df):
    """Generate summary statistics for the executive ribbon."""
    stats = {
        'total_fails': len(df),
        'total_trade_value': df['trade_value'].sum(),
        'total_market_value': df['market_value'].sum(),
        'total_mtm_pnl': df['mtm_pnl'].sum(),

        # Direction
        'ftd_count': len(df[df['direction'] == 'FTD']),
        'ftd_value': df[df['direction'] == 'FTD']['trade_value'].sum(),
        'ftr_count': len(df[df['direction'] == 'FTR']),
        'ftr_value': df[df['direction'] == 'FTR']['trade_value'].sum(),

        # Product Type
        'equity_count': len(df[df['product_type'] == 'Equity']),
        'equity_value': df[df['product_type'] == 'Equity']['trade_value'].sum(),
        'fi_count': len(df[df['product_type'] == 'Fixed Income']),
        'fi_value': df[df['product_type'] == 'Fixed Income']['trade_value'].sum(),

        # Reg SHO
        'reg_sho_at_risk_count': len(df[df['is_reg_sho_at_risk']]),
        'reg_sho_at_risk_value': df[df['is_reg_sho_at_risk']]['trade_value'].sum(),

        # HTB
        'htb_count': len(df[df['is_htb']]),
        'htb_value': df[df['is_htb']]['trade_value'].sum(),

        # Priority Clients
        'platinum_fails': len(df[df['client_tier'] == 'Platinum']),
        'platinum_value': df[df['client_tier'] == 'Platinum']['trade_value'].sum(),
    }

    return stats


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("Generating 20,000 settlement fails with full data model...")
    df = generate_fails(20000)

    print(f"\n{'='*60}")
    print(f"GENERATED {len(df):,} FAILS")
    print(f"{'='*60}")

    print(f"\n📊 VALUE SUMMARY:")
    print(f"   Total Trade Value:  ${df['trade_value'].sum():,.2f}")
    print(f"   Total Market Value: ${df['market_value'].sum():,.2f}")
    print(f"   Total MTM P&L:      ${df['mtm_pnl'].sum():,.2f}")

    print(f"\n📈 BY DIRECTION:")
    print(df.groupby('direction')[['trade_value', 'mtm_pnl']].agg(['count', 'sum']).to_string())

    print(f"\n🏢 BY DESK:")
    print(df.groupby('desk')['trade_value'].agg(['count', 'sum']).to_string())

    print(f"\n📦 BY PRODUCT TYPE:")
    print(df.groupby('product_type')['trade_value'].agg(['count', 'sum']).to_string())

    print(f"\n⚠️  BY EXCEPTION CATEGORY:")
    print(df.groupby('exception_category')['trade_value'].agg(['count', 'sum']).to_string())

    print(f"\n🚨 REG SHO AT RISK:")
    print(f"   {len(df[df['is_reg_sho_at_risk']]):,} fails, ${df[df['is_reg_sho_at_risk']]['trade_value'].sum():,.2f}")

    print(f"\n📋 SAMPLE RECORD (First Fail):")
    first = df.iloc[0]
    print(f"   Trade ID:        {first['trade_id']}")
    print(f"   Security:        {first['symbol']} - {first['security_name']}")
    print(f"   Product:         {first['product_type']} / {first['product_subtype']}")
    print(f"   Direction:       {first['direction']}")
    print(f"   Quantity:        {first['quantity']:,}")
    print(f"   Trade Price:     ${first['trade_price']:,.4f}")
    print(f"   Current Price:   ${first['current_price']:,.4f}")
    print(f"   Trade Value:     ${first['trade_value']:,.2f}")
    print(f"   MTM P&L:         ${first['mtm_pnl']:,.2f}")
    print(f"   Client:          {first['client_name']} ({first['client_tier']})")
    print(f"   Counterparty:    {first['counterparty_name']}")
    print(f"   Exception:       {first['exception_category']} - {first['swift_reason_code']}")
    print(f"   Cpty BIC:        {first['cpty_agent_bic']}")
    print(f"   PSET:            {first['pset']}")

    # Save to CSV
    df.to_csv('/tmp/sample_fails_full.csv', index=False)
    print(f"\n✅ Full dataset saved to /tmp/sample_fails_full.csv")
    print(f"   Columns: {len(df.columns)}")
