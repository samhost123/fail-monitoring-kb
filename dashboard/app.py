"""
Equity Settlement Fails Dashboard
Executive Command & Control Interface for T+1 Settlement Operations

Interactive drill-down: Direction → Category → Fails → Detail
Views: Home | Counterparty Exposure | FTD/FTR Pairing | Reg SHO Center
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

from data_simulator import generate_fails, generate_summary_stats

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="Settlement Fails Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS
# =============================================================================
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }

    /* Clickable cards */
    .metric-card {
        background-color: #1e2130;
        border: 1px solid #2d3250;
        border-radius: 10px;
        padding: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        border-color: #4ecdc4;
        transform: translateY(-2px);
    }

    /* Breadcrumb */
    .breadcrumb {
        background-color: #1e2130;
        padding: 10px 20px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .breadcrumb a {
        color: #4ecdc4;
        text-decoration: none;
    }

    /* Section headers */
    .section-header {
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 15px;
        padding-bottom: 5px;
        border-bottom: 2px solid #3d4663;
    }

    /* Alert colors */
    .critical { color: #ff4444; }
    .warning { color: #ffaa00; }
    .success { color: #4ecdc4; }

    /* Hide default */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Make buttons look clickable */
    .stButton > button {
        width: 100%;
        background-color: #1e2130;
        border: 1px solid #3d4663;
        color: white;
    }
    .stButton > button:hover {
        border-color: #4ecdc4;
        background-color: #2d3250;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# DATA LOADING
# =============================================================================
@st.cache_data
def load_data():
    df = generate_fails(20000)
    stats = generate_summary_stats(df)
    return df, stats


# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================
def init_session_state():
    """Initialize navigation state."""
    if 'nav_level' not in st.session_state:
        st.session_state.nav_level = 'home'  # home, direction, category, fails, detail
    if 'selected_direction' not in st.session_state:
        st.session_state.selected_direction = None
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = None
    if 'selected_subcategory' not in st.session_state:
        st.session_state.selected_subcategory = None
    if 'selected_trade_id' not in st.session_state:
        st.session_state.selected_trade_id = None
    if 'main_view' not in st.session_state:
        st.session_state.main_view = 'home'  # home, counterparty, pairing, regsho


def navigate_to(level, direction=None, category=None, subcategory=None, trade_id=None):
    """Navigate to a specific level."""
    st.session_state.nav_level = level
    if direction is not None:
        st.session_state.selected_direction = direction
    if category is not None:
        st.session_state.selected_category = category
    if subcategory is not None:
        st.session_state.selected_subcategory = subcategory
    if trade_id is not None:
        st.session_state.selected_trade_id = trade_id


def go_home():
    st.session_state.nav_level = 'home'
    st.session_state.selected_direction = None
    st.session_state.selected_category = None
    st.session_state.selected_subcategory = None
    st.session_state.selected_trade_id = None


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def format_currency(value, prefix="$", suffix=""):
    if abs(value) >= 1_000_000_000:
        return f"{prefix}{value/1_000_000_000:.1f}B{suffix}"
    elif abs(value) >= 1_000_000:
        return f"{prefix}{value/1_000_000:.1f}M{suffix}"
    elif abs(value) >= 1_000:
        return f"{prefix}{value/1_000:.1f}K{suffix}"
    else:
        return f"{prefix}{value:,.0f}{suffix}"


# =============================================================================
# BREADCRUMB NAVIGATION
# =============================================================================
def render_breadcrumb():
    """Render clickable breadcrumb navigation."""
    breadcrumb_parts = ["🏠 Home"]

    if st.session_state.selected_direction:
        breadcrumb_parts.append(f"📊 {st.session_state.selected_direction}")
    if st.session_state.selected_category:
        breadcrumb_parts.append(f"📁 {st.session_state.selected_category}")
    if st.session_state.selected_subcategory:
        breadcrumb_parts.append(f"📋 {st.session_state.selected_subcategory}")
    if st.session_state.selected_trade_id:
        breadcrumb_parts.append(f"📄 {st.session_state.selected_trade_id}")

    cols = st.columns(len(breadcrumb_parts) + 1)

    for i, part in enumerate(breadcrumb_parts):
        with cols[i]:
            if i == 0:
                if st.button(part, key=f"bc_{i}", use_container_width=True):
                    go_home()
                    st.rerun()
            elif i == 1 and st.session_state.selected_direction:
                if st.button(part, key=f"bc_{i}", use_container_width=True):
                    navigate_to('direction', direction=st.session_state.selected_direction)
                    st.session_state.selected_category = None
                    st.session_state.selected_subcategory = None
                    st.session_state.selected_trade_id = None
                    st.rerun()
            elif i == 2 and st.session_state.selected_category:
                if st.button(part, key=f"bc_{i}", use_container_width=True):
                    navigate_to('category')
                    st.session_state.selected_subcategory = None
                    st.session_state.selected_trade_id = None
                    st.rerun()
            elif i == 3 and st.session_state.selected_subcategory:
                if st.button(part, key=f"bc_{i}", use_container_width=True):
                    navigate_to('fails')
                    st.session_state.selected_trade_id = None
                    st.rerun()
            else:
                st.button(part, key=f"bc_{i}", disabled=True, use_container_width=True)


# =============================================================================
# VIEW: HOME (Executive Summary)
# =============================================================================
def render_home(df, stats):
    """Render the home view with clickable direction cards."""

    st.markdown("# 📊 Settlement Fails Dashboard")
    st.markdown(f"**Start of Day (SOD) Fail Report** | {datetime.now().strftime('%B %d, %Y %H:%M')} ET")
    st.divider()

    # Executive Summary KPIs
    st.markdown('<p class="section-header">Executive Summary</p>', unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Total Fail Exposure", format_currency(stats['total_trade_value']), f"{stats['total_fails']:,} trades")
    with k2:
        st.metric("🚨 Reg SHO At Risk", format_currency(stats['reg_sho_at_risk_value']),
                  f"{stats['reg_sho_at_risk_count']} at deadline", delta_color="inverse")
    with k3:
        st.metric("Affirmation Rate", "94.7%", "-0.8% vs target", delta_color="inverse")
    with k4:
        cash_impact = stats['ftr_value'] - stats['ftd_value']
        st.metric("Net Cash Impact", format_currency(cash_impact),
                  "Funding required" if cash_impact < 0 else "Surplus")

    st.divider()

    # CLICKABLE DIRECTION CARDS
    st.markdown('<p class="section-header">👆 Click to Drill Down by Direction</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔴 Fails to Deliver (FTD)")
        st.markdown(f"**{format_currency(stats['ftd_value'])}** | {stats['ftd_count']:,} trades")
        st.markdown("*Regulatory focus - Rule 204 exposure*")

        # Breakdown preview
        ftd_df = df[df['direction'] == 'FTD']
        ftd_by_cat = ftd_df.groupby('exception_category')['trade_value'].sum().sort_values(ascending=False)
        for cat, val in ftd_by_cat.head(3).items():
            st.markdown(f"- {cat}: {format_currency(val)}")

        if st.button("🔍 Explore FTD Fails →", key="btn_ftd", use_container_width=True, type="primary"):
            navigate_to('direction', direction='FTD')
            st.rerun()

    with col2:
        st.markdown("### 🟢 Fails to Receive (FTR)")
        st.markdown(f"**{format_currency(stats['ftr_value'])}** | {stats['ftr_count']:,} trades")
        st.markdown("*Credit risk - Counterparty exposure*")

        # Breakdown preview
        ftr_df = df[df['direction'] == 'FTR']
        ftr_by_cat = ftr_df.groupby('exception_category')['trade_value'].sum().sort_values(ascending=False)
        for cat, val in ftr_by_cat.head(3).items():
            st.markdown(f"- {cat}: {format_currency(val)}")

        if st.button("🔍 Explore FTR Fails →", key="btn_ftr", use_container_width=True, type="primary"):
            navigate_to('direction', direction='FTR')
            st.rerun()

    st.divider()

    # Additional summary charts
    st.markdown('<p class="section-header">Overview</p>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### By Desk")
        desk_data = df.groupby('desk')['trade_value'].sum().reset_index()
        fig = px.pie(desk_data, values='trade_value', names='desk',
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(height=300, margin=dict(t=20, b=20, l=20, r=20),
                         paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("#### By Product Type")
        prod_data = df.groupby('product_type')['trade_value'].sum().reset_index()
        fig = px.pie(prod_data, values='trade_value', names='product_type',
                     color_discrete_sequence=['#4ecdc4', '#ff6b6b'])
        fig.update_layout(height=300, margin=dict(t=20, b=20, l=20, r=20),
                         paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# VIEW: DIRECTION (FTD or FTR breakdown)
# =============================================================================
def render_direction_view(df):
    """Show breakdown of selected direction with clickable categories."""

    direction = st.session_state.selected_direction
    filtered_df = df[df['direction'] == direction]

    direction_label = "Fails to Deliver (FTD)" if direction == "FTD" else "Fails to Receive (FTR)"
    direction_icon = "🔴" if direction == "FTD" else "🟢"

    st.markdown(f"# {direction_icon} {direction_label}")
    st.markdown(f"**Total: {format_currency(filtered_df['trade_value'].sum())}** | {len(filtered_df):,} trades")

    if direction == "FTD":
        reg_sho = filtered_df[filtered_df['is_reg_sho_at_risk']]
        if len(reg_sho) > 0:
            st.error(f"🚨 **{len(reg_sho)} trades at Reg SHO deadline** - {format_currency(reg_sho['trade_value'].sum())} exposure")

    st.divider()

    # Category selection
    st.markdown('<p class="section-header">👆 Click a Category to Drill Down</p>', unsafe_allow_html=True)

    category_type = st.radio(
        "Group by:",
        ["Exception Category", "Counterparty", "Desk", "Client Tier", "Aging Bucket", "Product Type"],
        horizontal=True,
        key="category_type"
    )

    # Map selection to column
    category_col_map = {
        "Exception Category": "exception_category",
        "Counterparty": "counterparty_name",
        "Desk": "desk",
        "Client Tier": "client_tier",
        "Aging Bucket": "aging_bucket",
        "Product Type": "product_type"
    }
    category_col = category_col_map[category_type]

    # Calculate aggregates
    cat_data = filtered_df.groupby(category_col).agg({
        'trade_value': 'sum',
        'trade_id': 'count',
        'mtm_pnl': 'sum'
    }).reset_index()
    cat_data.columns = ['Category', 'Value', 'Count', 'MTM']
    cat_data = cat_data.sort_values('Value', ascending=False)

    # Display as clickable cards
    cols = st.columns(min(len(cat_data), 4))

    for i, (_, row) in enumerate(cat_data.iterrows()):
        col_idx = i % 4
        with cols[col_idx]:
            st.markdown(f"### {row['Category']}")
            st.markdown(f"**{format_currency(row['Value'])}**")
            st.markdown(f"{int(row['Count']):,} trades | MTM: {format_currency(row['MTM'])}")

            if st.button(f"View Fails →", key=f"cat_{i}", use_container_width=True):
                navigate_to('category', category=category_type, subcategory=row['Category'])
                st.rerun()

        # New row every 4 items
        if (i + 1) % 4 == 0 and i + 1 < len(cat_data):
            cols = st.columns(min(len(cat_data) - i - 1, 4))

    st.divider()

    # Visualization
    st.markdown("#### Distribution")
    fig = px.bar(cat_data, x='Category', y='Value', color='Category',
                 text=[format_currency(v) for v in cat_data['Value']],
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_traces(textposition='outside')
    fig.update_layout(height=400, showlegend=False,
                     paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# VIEW: CATEGORY (List of fails in selected category)
# =============================================================================
def render_category_view(df):
    """Show list of fails in selected category with click-to-detail."""

    direction = st.session_state.selected_direction
    category_type = st.session_state.selected_category
    subcategory = st.session_state.selected_subcategory

    # Map category type to column
    category_col_map = {
        "Exception Category": "exception_category",
        "Counterparty": "counterparty_name",
        "Desk": "desk",
        "Client Tier": "client_tier",
        "Aging Bucket": "aging_bucket",
        "Product Type": "product_type"
    }
    category_col = category_col_map.get(category_type, "exception_category")

    # Filter data
    filtered_df = df[df['direction'] == direction]
    filtered_df = filtered_df[filtered_df[category_col] == subcategory]
    filtered_df = filtered_df.sort_values('priority_score', ascending=False)

    st.markdown(f"# 📋 {subcategory}")
    st.markdown(f"**{direction}** | {format_currency(filtered_df['trade_value'].sum())} | {len(filtered_df):,} trades")

    # Highlight critical items
    critical_count = len(filtered_df[filtered_df['is_reg_sho_at_risk']])
    htb_count = len(filtered_df[filtered_df['is_htb']])
    platinum_count = len(filtered_df[filtered_df['client_tier'] == 'Platinum'])

    if critical_count > 0 or htb_count > 0 or platinum_count > 0:
        alert_cols = st.columns(3)
        with alert_cols[0]:
            if critical_count > 0:
                st.error(f"🚨 {critical_count} Reg SHO at risk")
        with alert_cols[1]:
            if htb_count > 0:
                st.warning(f"⚠️ {htb_count} Hard to Borrow")
        with alert_cols[2]:
            if platinum_count > 0:
                st.info(f"⭐ {platinum_count} Platinum clients")

    st.divider()

    # Filter controls
    st.markdown('<p class="section-header">Filter Fails</p>', unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    with f1:
        show_reg_sho = st.checkbox("Only Reg SHO at risk", key="filter_regsho")
    with f2:
        show_htb = st.checkbox("Only Hard to Borrow", key="filter_htb")
    with f3:
        show_platinum = st.checkbox("Only Platinum clients", key="filter_platinum")

    display_df = filtered_df.copy()
    if show_reg_sho:
        display_df = display_df[display_df['is_reg_sho_at_risk']]
    if show_htb:
        display_df = display_df[display_df['is_htb']]
    if show_platinum:
        display_df = display_df[display_df['client_tier'] == 'Platinum']

    st.markdown(f"**Showing {len(display_df):,} fails** (sorted by priority)")

    st.divider()

    # CLICKABLE FAIL LIST
    st.markdown('<p class="section-header">👆 Click a Fail to View Details</p>', unsafe_allow_html=True)

    # Show top 50 as clickable items
    for i, (_, row) in enumerate(display_df.head(50).iterrows()):
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])

        # Priority indicator
        priority_icon = "🔴" if row['is_reg_sho_at_risk'] else ("🟡" if row['is_htb'] else "⚪")
        tier_icon = "⭐" if row['client_tier'] == 'Platinum' else ("🥇" if row['client_tier'] == 'Gold' else "")

        with col1:
            st.markdown(f"**{priority_icon} {row['trade_id']}**")
            st.caption(f"{row['symbol']} | {row['security_name'][:25]}...")

        with col2:
            st.markdown(f"**{format_currency(row['trade_value'])}**")
            st.caption(f"{row['quantity']:,} @ ${row['trade_price']:.2f}")

        with col3:
            st.markdown(f"**{tier_icon} {row['client_name'][:20]}**")
            st.caption(f"{row['client_tier']} | {row['counterparty_name'][:15]}")

        with col4:
            st.markdown(f"**{row['swift_reason_code']}**")
            st.caption(f"Age: {row['age_days']}d | {row['aging_bucket'][:10]}")

        with col5:
            if st.button("View →", key=f"fail_{i}", use_container_width=True):
                navigate_to('detail', trade_id=row['trade_id'])
                st.rerun()

        st.markdown("---")


# =============================================================================
# VIEW: DETAIL (Single fail complete details)
# =============================================================================
def render_detail_view(df):
    """Show complete details for a single fail."""

    trade_id = st.session_state.selected_trade_id
    trade = df[df['trade_id'] == trade_id].iloc[0]

    # Header with key info
    priority_icon = "🔴" if trade['is_reg_sho_at_risk'] else ("🟡" if trade['is_htb'] else "🟢")

    st.markdown(f"# {priority_icon} Trade Detail: {trade_id}")

    # Alert banner if critical
    if trade['is_reg_sho_at_risk']:
        st.error(f"🚨 **REG SHO AT RISK** - Closeout deadline in {trade['days_to_closeout']} days!")
    if trade['is_htb']:
        st.warning(f"⚠️ **HARD TO BORROW** - Check Stock Loan availability")
    if trade['client_tier'] == 'Platinum':
        st.info(f"⭐ **PLATINUM CLIENT** - Priority handling required | RM: {trade['relationship_manager']} ({trade['rm_phone']})")

    st.divider()

    # Main details in 3 columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📄 Trade Information")
        st.markdown(f"""
        | Field | Value |
        |-------|-------|
        | **Trade ID** | `{trade['trade_id']}` |
        | **CNS Control** | `{trade['cns_control_number']}` |
        | **Broker Ref** | `{trade['broker_reference']}` |
        | **SWIFT Ref** | `{trade['swift_reference']}` |
        | **Trade Date** | {trade['trade_date']} |
        | **Settlement Date** | {trade['settlement_date']} |
        | **Age** | **{trade['age_days']} days** |
        | **Aging Bucket** | {trade['aging_bucket']} |
        """)

        st.markdown("### 📈 Security")
        st.markdown(f"""
        | Field | Value |
        |-------|-------|
        | **Symbol** | **{trade['symbol']}** |
        | **Name** | {trade['security_name']} |
        | **CUSIP** | `{trade['cusip']}` |
        | **ISIN** | `{trade['isin']}` |
        | **SEDOL** | `{trade['sedol']}` |
        | **Product** | {trade['product_type']} |
        | **Subtype** | {trade['product_subtype']} |
        | **Sector** | {trade['sector']} |
        | **Exchange** | {trade['exchange']} |
        """)

    with col2:
        st.markdown("### 💰 Quantity & Value")

        # Visual value display
        st.metric("Trade Value", f"${trade['trade_value']:,.2f}")
        st.metric("Market Value", f"${trade['market_value']:,.2f}")

        mtm_color = "green" if trade['mtm_pnl'] >= 0 else "red"
        st.metric("MTM P&L", f"${trade['mtm_pnl']:,.2f}",
                  delta=f"{'Gain' if trade['mtm_pnl'] >= 0 else 'Loss'}")

        st.markdown(f"""
        | Field | Value |
        |-------|-------|
        | **Quantity** | **{trade['quantity']:,}** |
        | **Trade Price** | ${trade['trade_price']:,.4f} |
        | **Current Price** | ${trade['current_price']:,.4f} |
        | **Currency** | {trade['currency']} |
        """)

        st.markdown("### 🏷️ Classification")
        st.markdown(f"""
        | Field | Value |
        |-------|-------|
        | **Direction** | **{trade['direction']}** |
        | **Trade Type** | {trade['trade_type']} |
        | **Settlement Type** | {trade['settlement_type']} |
        | **CNS** | {'Yes' if trade['is_cns'] else 'No'} |
        | **Borrowability** | **{trade['borrowability']}** |
        | **Threshold Security** | {'⚠️ Yes' if trade['is_threshold_security'] else 'No'} |
        """)

    with col3:
        st.markdown("### 👤 Client")
        st.markdown(f"""
        | Field | Value |
        |-------|-------|
        | **Name** | **{trade['client_name']}** |
        | **Tier** | **{trade['client_tier']}** {'⭐' if trade['client_tier'] == 'Platinum' else ''} |
        | **Account** | `{trade['client_account']}` |
        | **LEI** | `{trade['client_lei']}` |
        | **RM** | {trade['relationship_manager']} |
        | **RM Phone** | **{trade['rm_phone']}** |
        """)

        st.markdown("### 🏦 Counterparty")
        st.markdown(f"""
        | Field | Value |
        |-------|-------|
        | **Name** | **{trade['counterparty_name']}** |
        | **BIC** | `{trade['counterparty_bic']}` |
        | **DTC Participant** | `{trade['counterparty_dtc_participant']}` |
        """)

        st.markdown("### ⚠️ Exception")
        st.markdown(f"""
        | Field | Value |
        |-------|-------|
        | **Category** | **{trade['exception_category']}** |
        | **SWIFT Code** | `{trade['swift_reason_code']}` |
        | **DTC Code** | `{trade['dtc_reason_code']}` |
        | **Description** | {trade['reason_description']} |
        | **Owner** | **{trade['operational_owner']}** |
        """)

    st.divider()

    # SSI DETAILS
    st.markdown("### 🔗 Settlement Instructions (SSI)")

    ssi1, ssi2 = st.columns(2)

    with ssi1:
        st.markdown("#### Our Side")
        st.markdown(f"""
        | Field | Value |
        |-------|-------|
        | **Agent BIC** | `{trade['our_agent_bic']}` |
        | **Safekeeping Account** | `{trade['our_safekeeping_account']}` |
        | **DTC Participant** | `{trade['our_dtc_participant']}` |
        | **PSET** | `{trade['pset']}` |
        """)

    with ssi2:
        st.markdown("#### Counterparty Side")
        st.markdown(f"""
        | Field | Value |
        |-------|-------|
        | **Agent BIC** | `{trade['cpty_agent_bic']}` |
        | **Safekeeping Account** | `{trade['cpty_safekeeping_account']}` |
        | **DTC Participant** | `{trade['cpty_dtc_participant']}` |
        """)

    # SSI Mismatch alert
    if trade['ssi_mismatch_field']:
        st.error(f"""
        ### 🚫 SSI Mismatch Detected

        **Field:** {trade['ssi_mismatch_field']}

        - {trade['ssi_expected']}
        - {trade['ssi_received']}

        **Action Required:** Contact Data Management to update SSI database
        """)

    st.divider()

    # Reg SHO Details (if FTD)
    if trade['direction'] == 'FTD' and trade['closeout_deadline_days']:
        st.markdown("### 📋 Regulation SHO Status")

        reg1, reg2, reg3 = st.columns(3)
        with reg1:
            st.metric("Trade Type", trade['trade_type'])
        with reg2:
            st.metric("Closeout Deadline", f"T+{trade['closeout_deadline_days']}")
        with reg3:
            days_left = trade['days_to_closeout'] if trade['days_to_closeout'] else 'N/A'
            st.metric("Days Remaining", days_left,
                     delta="URGENT" if trade['is_reg_sho_at_risk'] else None,
                     delta_color="inverse")

        if trade['is_reg_sho_at_risk']:
            st.error("""
            **⚠️ IMMEDIATE ACTION REQUIRED**

            This fail is at or past the Reg SHO closeout deadline. Failure to close out will result in:
            - Pre-borrow penalty (restriction on short sales)
            - Potential regulatory reporting
            - Increased capital charges

            **Recommended Actions:**
            1. Check Stock Loan for borrow availability
            2. Initiate buy-in if borrow unavailable
            3. Escalate to compliance
            """)


# =============================================================================
# VIEW: COUNTERPARTY EXPOSURE
# =============================================================================
def render_counterparty_view(df):
    """Show exposure aggregated by counterparty."""

    st.markdown("# 🏦 Counterparty Exposure Analysis")
    st.markdown("Aggregate fail exposure by counterparty - identify concentration risk")
    st.divider()

    # Direction filter
    direction_filter = st.radio(
        "View:", ["All Fails", "FTD Only", "FTR Only"],
        horizontal=True, key="cpty_direction"
    )

    filtered_df = df.copy()
    if direction_filter == "FTD Only":
        filtered_df = filtered_df[filtered_df['direction'] == 'FTD']
    elif direction_filter == "FTR Only":
        filtered_df = filtered_df[filtered_df['direction'] == 'FTR']

    # Aggregate by counterparty
    cpty_agg = filtered_df.groupby('counterparty_name').agg({
        'trade_value': 'sum',
        'trade_id': 'count',
        'mtm_pnl': 'sum',
        'is_reg_sho_at_risk': 'sum',
        'age_days': 'mean'
    }).reset_index()
    cpty_agg.columns = ['Counterparty', 'Exposure', 'Fail Count', 'MTM P&L', 'Reg SHO At Risk', 'Avg Age']
    cpty_agg = cpty_agg.sort_values('Exposure', ascending=False)

    # Summary KPIs
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Counterparties with Fails", len(cpty_agg))
    with k2:
        top_exposure = cpty_agg.iloc[0]['Exposure'] if len(cpty_agg) > 0 else 0
        st.metric("Largest Exposure", format_currency(top_exposure))
    with k3:
        concentration = (cpty_agg.head(5)['Exposure'].sum() / cpty_agg['Exposure'].sum() * 100) if len(cpty_agg) > 0 else 0
        st.metric("Top 5 Concentration", f"{concentration:.1f}%")
    with k4:
        high_risk = len(cpty_agg[cpty_agg['Reg SHO At Risk'] > 0])
        st.metric("With Reg SHO Risk", high_risk)

    st.divider()

    # Two column layout
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown("### Top Counterparties by Exposure")

        # Treemap visualization
        fig = px.treemap(
            cpty_agg.head(20),
            path=['Counterparty'],
            values='Exposure',
            color='MTM P&L',
            color_continuous_scale=['#ff4444', '#ffaa00', '#4ecdc4'],
            color_continuous_midpoint=0
        )
        fig.update_layout(height=400, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Exposure Distribution")

        fig = px.pie(
            cpty_agg.head(10),
            values='Exposure',
            names='Counterparty',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(height=400, margin=dict(t=20, b=20, l=20, r=20),
                         paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Detailed table with drill-down
    st.markdown("### 👆 Click a Counterparty to View Fails")

    for i, (_, row) in enumerate(cpty_agg.head(15).iterrows()):
        c1, c2, c3, c4, c5, c6 = st.columns([2.5, 1.5, 1, 1, 1, 0.8])

        risk_icon = "🔴" if row['Reg SHO At Risk'] > 0 else "🟢"

        with c1:
            st.markdown(f"**{risk_icon} {row['Counterparty']}**")
        with c2:
            st.markdown(f"**{format_currency(row['Exposure'])}**")
        with c3:
            st.markdown(f"{int(row['Fail Count']):,} fails")
        with c4:
            mtm_color = "🟢" if row['MTM P&L'] >= 0 else "🔴"
            st.markdown(f"{mtm_color} {format_currency(row['MTM P&L'])}")
        with c5:
            st.markdown(f"{row['Avg Age']:.1f} days avg")
        with c6:
            if st.button("View →", key=f"cpty_{i}"):
                st.session_state.main_view = 'home'
                st.session_state.selected_direction = None
                st.session_state.selected_category = "Counterparty"
                st.session_state.selected_subcategory = row['Counterparty']
                st.session_state.nav_level = 'category'
                st.rerun()

        st.markdown("---")


# =============================================================================
# VIEW: FTD/FTR PAIRING
# =============================================================================
def render_pairing_view(df):
    """Show FTD/FTR pairing opportunities for netting."""

    st.markdown("# 🔄 FTD/FTR Pairing Analysis")
    st.markdown("Identify offsetting positions for potential netting and exposure reduction")
    st.divider()

    # Find potential pairs (same security, opposite direction)
    ftd_df = df[df['direction'] == 'FTD'].copy()
    ftr_df = df[df['direction'] == 'FTR'].copy()

    # Group by security for pairing
    ftd_by_security = ftd_df.groupby(['cusip', 'symbol', 'security_name']).agg({
        'quantity': 'sum',
        'trade_value': 'sum',
        'trade_id': 'count'
    }).reset_index()
    ftd_by_security.columns = ['CUSIP', 'Symbol', 'Security', 'FTD Qty', 'FTD Value', 'FTD Count']

    ftr_by_security = ftr_df.groupby(['cusip', 'symbol', 'security_name']).agg({
        'quantity': 'sum',
        'trade_value': 'sum',
        'trade_id': 'count'
    }).reset_index()
    ftr_by_security.columns = ['CUSIP', 'Symbol', 'Security', 'FTR Qty', 'FTR Value', 'FTR Count']

    # Merge to find overlaps
    pairs = ftd_by_security.merge(ftr_by_security, on=['CUSIP', 'Symbol', 'Security'], how='inner')

    # Calculate netting potential
    pairs['Nettable Qty'] = pairs.apply(lambda x: min(x['FTD Qty'], x['FTR Qty']), axis=1)
    pairs['Nettable Value'] = pairs.apply(
        lambda x: min(x['FTD Value'], x['FTR Value']), axis=1
    )
    pairs['Net Position'] = pairs['FTD Qty'] - pairs['FTR Qty']
    pairs['Net Exposure'] = pairs['FTD Value'] - pairs['FTR Value']
    pairs = pairs.sort_values('Nettable Value', ascending=False)

    # Summary KPIs
    total_nettable = pairs['Nettable Value'].sum()
    total_ftd = ftd_df['trade_value'].sum()
    total_ftr = ftr_df['trade_value'].sum()

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Securities with Pairs", len(pairs))
    with k2:
        st.metric("Total Nettable Exposure", format_currency(total_nettable))
    with k3:
        pct_nettable = (total_nettable / total_ftd * 100) if total_ftd > 0 else 0
        st.metric("% FTD Nettable", f"{pct_nettable:.1f}%")
    with k4:
        reduction_benefit = total_nettable * 2  # Both sides benefit
        st.metric("Gross Exposure Reduction", format_currency(reduction_benefit))

    if total_nettable > 0:
        st.success(f"💡 **Netting Opportunity:** Offsetting these {len(pairs)} securities could reduce gross exposure by {format_currency(reduction_benefit)}")

    st.divider()

    # Visualization
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### FTD vs FTR by Security")

        if len(pairs) > 0:
            fig = go.Figure()
            top_pairs = pairs.head(10)

            fig.add_trace(go.Bar(
                name='FTD',
                x=top_pairs['Symbol'],
                y=top_pairs['FTD Value'],
                marker_color='#ff6b6b'
            ))
            fig.add_trace(go.Bar(
                name='FTR',
                x=top_pairs['Symbol'],
                y=top_pairs['FTR Value'],
                marker_color='#4ecdc4'
            ))

            fig.update_layout(
                barmode='group',
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="h", yanchor="bottom", y=1.02)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No matching securities found between FTD and FTR")

    with col2:
        st.markdown("### Net Position Distribution")

        if len(pairs) > 0:
            fig = px.scatter(
                pairs.head(20),
                x='FTD Value',
                y='FTR Value',
                size='Nettable Value',
                color='Net Exposure',
                hover_name='Symbol',
                color_continuous_scale=['#4ecdc4', '#ffaa00', '#ff6b6b'],
                color_continuous_midpoint=0
            )
            fig.add_trace(go.Scatter(
                x=[0, max(pairs['FTD Value'].max(), pairs['FTR Value'].max())],
                y=[0, max(pairs['FTD Value'].max(), pairs['FTR Value'].max())],
                mode='lines',
                line=dict(dash='dash', color='gray'),
                name='Perfect Balance'
            ))
            fig.update_layout(
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Pairing Table
    st.markdown("### Pairing Opportunities (sorted by nettable value)")

    for i, (_, row) in enumerate(pairs.head(20).iterrows()):
        net_icon = "⚖️" if abs(row['Net Position']) < 100 else ("📈" if row['Net Position'] > 0 else "📉")

        c1, c2, c3, c4, c5, c6 = st.columns([2, 1.5, 1.5, 1.5, 1.5, 1])

        with c1:
            st.markdown(f"**{row['Symbol']}**")
            st.caption(row['Security'][:30] + "..." if len(row['Security']) > 30 else row['Security'])
        with c2:
            st.markdown(f"🔴 FTD: **{format_currency(row['FTD Value'])}**")
            st.caption(f"{int(row['FTD Qty']):,} shares | {int(row['FTD Count'])} fails")
        with c3:
            st.markdown(f"🟢 FTR: **{format_currency(row['FTR Value'])}**")
            st.caption(f"{int(row['FTR Qty']):,} shares | {int(row['FTR Count'])} fails")
        with c4:
            st.markdown(f"✅ Nettable: **{format_currency(row['Nettable Value'])}**")
            st.caption(f"{int(row['Nettable Qty']):,} shares")
        with c5:
            st.markdown(f"{net_icon} Net: **{format_currency(row['Net Exposure'])}**")
            direction = "FTD heavy" if row['Net Exposure'] > 0 else "FTR heavy"
            st.caption(direction if abs(row['Net Exposure']) > 1000 else "Balanced")
        with c6:
            if st.button("Details", key=f"pair_{i}"):
                # Could drill into this security
                pass

        st.markdown("---")


# =============================================================================
# VIEW: REG SHO COMMAND CENTER
# =============================================================================
def render_regsho_view(df):
    """Dedicated Reg SHO compliance dashboard."""

    st.markdown("# ⚠️ Reg SHO Command Center")
    st.markdown("Rule 204 Compliance Monitoring - Focus on Closeout Deadlines")
    st.divider()

    # Filter to FTDs only (Reg SHO applies to fails to deliver)
    ftd_df = df[df['direction'] == 'FTD'].copy()

    # Categorize by closeout status
    at_risk = ftd_df[ftd_df['is_reg_sho_at_risk']]
    approaching = ftd_df[(ftd_df['days_to_closeout'] > 0) & (ftd_df['days_to_closeout'] <= 2) & (~ftd_df['is_reg_sho_at_risk'])]
    threshold_securities = ftd_df[ftd_df['is_threshold_security']]
    htb = ftd_df[ftd_df['is_htb']]

    # Alert Banner
    if len(at_risk) > 0:
        st.error(f"""
        🚨 **CRITICAL: {len(at_risk)} FAILS AT OR PAST CLOSEOUT DEADLINE**

        Total Exposure: **{format_currency(at_risk['trade_value'].sum())}** | Immediate action required
        """)

    # Summary KPIs
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("🔴 At Deadline", len(at_risk), format_currency(at_risk['trade_value'].sum()))
    with k2:
        st.metric("🟡 Approaching (≤2 days)", len(approaching), format_currency(approaching['trade_value'].sum()))
    with k3:
        st.metric("⚠️ Threshold Securities", len(threshold_securities), format_currency(threshold_securities['trade_value'].sum()))
    with k4:
        st.metric("📍 Hard to Borrow", len(htb), format_currency(htb['trade_value'].sum()))

    st.divider()

    # Closeout Timeline
    st.markdown("### 📅 Closeout Timeline")

    # Group by days to closeout
    timeline = ftd_df[ftd_df['days_to_closeout'].notna()].groupby('days_to_closeout').agg({
        'trade_value': 'sum',
        'trade_id': 'count'
    }).reset_index()
    timeline.columns = ['Days to Closeout', 'Value', 'Count']
    timeline = timeline.sort_values('Days to Closeout')

    # Color code bars
    def get_color(days):
        if days <= 0:
            return '#ff4444'
        elif days <= 2:
            return '#ffaa00'
        else:
            return '#4ecdc4'

    if len(timeline) > 0:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=timeline['Days to Closeout'],
            y=timeline['Value'],
            marker_color=[get_color(d) for d in timeline['Days to Closeout']],
            text=[format_currency(v) for v in timeline['Value']],
            textposition='outside'
        ))
        fig.update_layout(
            height=300,
            xaxis_title="Days to Closeout Deadline",
            yaxis_title="Exposure ($)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        fig.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="DEADLINE")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Two-column layout for at-risk details
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔴 At/Past Deadline - IMMEDIATE ACTION")

        if len(at_risk) == 0:
            st.success("✅ No fails currently at or past closeout deadline")
        else:
            for i, (_, row) in enumerate(at_risk.sort_values('trade_value', ascending=False).head(10).iterrows()):
                htb_flag = "📍" if row['is_htb'] else ""

                st.markdown(f"""
                **{row['symbol']}** {htb_flag} | {format_currency(row['trade_value'])}
                - {row['quantity']:,} shares | Age: {row['age_days']} days
                - Client: {row['client_name'][:25]} ({row['client_tier']})
                - Owner: **{row['operational_owner']}**
                """)

                c1, c2 = st.columns(2)
                with c1:
                    if st.button("View Details", key=f"risk_{i}"):
                        st.session_state.main_view = 'home'
                        st.session_state.selected_trade_id = row['trade_id']
                        st.session_state.nav_level = 'detail'
                        st.rerun()
                with c2:
                    st.button("Initiate Buy-In", key=f"buyin_{i}", type="secondary")

                st.markdown("---")

    with col2:
        st.markdown("### 🟡 Approaching Deadline (1-2 days)")

        if len(approaching) == 0:
            st.info("No fails approaching deadline in next 2 days")
        else:
            for i, (_, row) in enumerate(approaching.sort_values('days_to_closeout').head(10).iterrows()):
                urgency = "⚡" if row['days_to_closeout'] == 1 else "⏰"

                st.markdown(f"""
                {urgency} **{row['symbol']}** | {format_currency(row['trade_value'])} | **{int(row['days_to_closeout'])} day(s) left**
                - {row['quantity']:,} shares | Borrowability: {row['borrowability']}
                - Client: {row['client_name'][:25]}
                """)

                if st.button("View", key=f"approach_{i}"):
                    st.session_state.main_view = 'home'
                    st.session_state.selected_trade_id = row['trade_id']
                    st.session_state.nav_level = 'detail'
                    st.rerun()

                st.markdown("---")

    st.divider()

    # Threshold Security Analysis
    st.markdown("### ⚠️ Threshold Securities")
    st.caption("Securities on SEC Threshold List - heightened regulatory scrutiny")

    if len(threshold_securities) == 0:
        st.success("✅ No fails in threshold securities")
    else:
        thresh_by_sec = threshold_securities.groupby(['symbol', 'security_name']).agg({
            'trade_value': 'sum',
            'trade_id': 'count',
            'quantity': 'sum'
        }).reset_index().sort_values('trade_value', ascending=False)

        for i, (_, row) in enumerate(thresh_by_sec.head(10).iterrows()):
            st.markdown(f"**{row['symbol']}** - {row['security_name'][:40]}")
            st.markdown(f"Exposure: {format_currency(row['trade_value'])} | {int(row['trade_id'])} fails | {int(row['quantity']):,} shares")
            st.markdown("---")


# =============================================================================
# SIDEBAR NAVIGATION
# =============================================================================
def render_sidebar(stats):
    """Render sidebar navigation."""

    st.sidebar.markdown("## 📊 Navigation")
    st.sidebar.divider()

    if st.sidebar.button("🏠 **Home Dashboard**", use_container_width=True,
                         type="primary" if st.session_state.main_view == 'home' else "secondary"):
        st.session_state.main_view = 'home'
        go_home()
        st.rerun()

    if st.sidebar.button("🏦 **Counterparty Exposure**", use_container_width=True,
                         type="primary" if st.session_state.main_view == 'counterparty' else "secondary"):
        st.session_state.main_view = 'counterparty'
        go_home()
        st.rerun()

    if st.sidebar.button("🔄 **FTD/FTR Pairing**", use_container_width=True,
                         type="primary" if st.session_state.main_view == 'pairing' else "secondary"):
        st.session_state.main_view = 'pairing'
        go_home()
        st.rerun()

    if st.sidebar.button("⚠️ **Reg SHO Center**", use_container_width=True,
                         type="primary" if st.session_state.main_view == 'regsho' else "secondary"):
        st.session_state.main_view = 'regsho'
        go_home()
        st.rerun()

    st.sidebar.divider()

    # Quick Stats
    st.sidebar.markdown("### Quick Stats")
    st.sidebar.metric("Total Exposure", format_currency(stats['total_trade_value']))
    st.sidebar.metric("Reg SHO At Risk", stats['reg_sho_at_risk_count'])
    st.sidebar.metric("Total Fails", f"{stats['total_fails']:,}")

    st.sidebar.divider()
    st.sidebar.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")


# =============================================================================
# MAIN APP
# =============================================================================
def main():
    init_session_state()
    df, stats = load_data()

    # Render sidebar navigation
    render_sidebar(stats)

    # Main content based on view selection
    if st.session_state.main_view == 'counterparty':
        render_counterparty_view(df)

    elif st.session_state.main_view == 'pairing':
        render_pairing_view(df)

    elif st.session_state.main_view == 'regsho':
        render_regsho_view(df)

    else:  # 'home' view with drill-down
        # Render breadcrumb navigation
        render_breadcrumb()
        st.divider()

        # Route to appropriate view based on navigation level
        if st.session_state.nav_level == 'home' or st.session_state.selected_direction is None:
            render_home(df, stats)

        elif st.session_state.selected_trade_id is not None:
            render_detail_view(df)

        elif st.session_state.selected_subcategory is not None:
            render_category_view(df)

        elif st.session_state.selected_direction is not None:
            render_direction_view(df)


if __name__ == "__main__":
    main()
