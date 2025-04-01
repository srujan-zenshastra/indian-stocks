import pandas as pd
import streamlit as st
import plotly.express as px
import os
import random

# Set page configuration
st.set_page_config(
    page_title="Stock Details",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for stock details page
st.markdown("""
<style>
    /* General Styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
    }
    
    /* Dark Mode */
    [data-theme="dark"] .main {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
    }
    
    /* Typography */
    .details-ltp {
        font-size: 24px;
        font-weight: 700;
        color: #2c3e50;
        display: inline-block;
        margin-right: 20px;
    }
    .details-change {
        font-size: 16px;
        font-weight: 600;
        display: inline-block;
    }
    .change-positive {
        color: #27ae60;
    }
    .change-negative {
        color: #c0392b;
    }
    .metric {
        font-size: 14px;
        color: #34495e;
        margin: 5px 0;
    }
    .metric-value {
        font-weight: 600;
        color: #2980b9;
    }
    [data-theme="dark"] .details-ltp {
        color: #ecf0f1;
    }
    [data-theme="dark"] .metric {
        color: #ecf0f1;
    }
    [data-theme="dark"] .metric-value {
        color: #3498db;
    }
    
    /* Toggle Button Styling */
    .toggle-container {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 10px;
    }
    .toggle-container button {
        margin-left: 8px !important;
        border-radius: 5px !important;
        padding: 5px 10px !important;
    }
    .stButton>button:hover {
        background-color: #e0e0e0;
    }
    .stButton>button:focus {
        background-color: #3498db;
        color: white;
    }
    
    /* Fix for horizontal button alignment */
    .button-row {
        display: flex;
        justify-content: flex-end;
        gap: 10px;
    }
    .button-row > div {
        margin: 0 !important;
    }
    .button-row button {
        margin: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Define stock data (same as in Home.py)
stocks = {
    "Sector": {
        "Tech": [
            {"symbol": "INFY", "company": "Infosys Ltd.", "description": "Infosys is a global leader in next-generation digital services and consulting. It empowers businesses with agile digital solutions. The company operates across multiple industries worldwide."},
            {"symbol": "TCS", "company": "Tata Consultancy Services Ltd.", "description": "TCS is a leading global IT services, consulting, and business solutions organization. Part of the Tata Group, it serves clients worldwide. It specializes in digital transformation and IT services."},
            {"symbol": "COFORGE", "company": "Coforge Ltd.", "description": "Coforge is a global IT solutions organization providing digital services. It focuses on innovative technology transformations. The company caters to various sectors including finance and travel."},
            {"symbol": "MASTEK", "company": "Mastek Ltd.", "description": "Mastek provides enterprise technology solutions and digital transformation services. It caters to various industries globally. The company is known for its agile and innovative approach."}
        ],
        "Finance": [
            {"symbol": "HDFCBANK", "company": "HDFC Bank Ltd.", "description": "HDFC Bank is one of India's premier banking institutions. It offers a wide range of financial products and services. The bank is known for its robust digital banking platform."},
            {"symbol": "SBIN", "company": "State Bank of India", "description": "SBI is India's largest public sector bank providing comprehensive banking services. It has a vast network across the country. The bank serves millions of customers daily."},
            {"symbol": "IDFCFIRSTB", "company": "IDFC First Bank Ltd.", "description": "IDFC First Bank offers banking and financial services with a focus on retail and business banking. It aims for customer-centric growth. The bank emphasizes sustainable banking practices."},
            {"symbol": "DCBBANK", "company": "DCB Bank Ltd.", "description": "DCB Bank provides banking services to individuals and businesses in India. It focuses on personalized financial solutions. The bank operates a growing network of branches."}
        ],
        "Energy": [
            {"symbol": "TATAPOWER", "company": "Tata Power Company Ltd.", "description": "Tata Power is one of India's largest integrated power companies. It operates in generation, transmission, and distribution. The company is part of the Tata Group."},
            {"symbol": "ADANIGREEN", "company": "Adani Green Energy Ltd.", "description": "Adani Green is a leading renewable energy company in India. It focuses on sustainable solar and wind power projects. The company aims to expand green energy capacity."},
            {"symbol": "NHPC", "company": "NHPC Ltd.", "description": "NHPC is a major hydropower generation company in India. It develops and operates hydroelectric projects nationwide. The company contributes significantly to India's power sector."},
            {"symbol": "RELINFRA", "company": "Reliance Infrastructure Ltd.", "description": "Reliance Infra is involved in power generation, transmission, and distribution. It also undertakes infrastructure projects. The company is part of the Reliance Group."}
        ],
        "Consumer": [
            {"symbol": "HINDUNILVR", "company": "Hindustan Unilever Ltd.", "description": "Hindustan Unilever is a leading consumer goods company in India. It offers a wide range of FMCG products. The company is known for its strong brand portfolio."},
            {"symbol": "ITC", "company": "ITC Ltd.", "description": "ITC is a diversified conglomerate with a strong presence in FMCG. It also operates in hotels and agribusiness. The company is a major player in India's consumer market."},
            {"symbol": "BAJAJELEC", "company": "Bajaj Electricals Ltd.", "description": "Bajaj Electricals is a consumer electrical equipment manufacturing company. It specializes in appliances and lighting. The company has a strong presence in India."},
            {"symbol": "VOLTAS", "company": "Voltas Ltd.", "description": "Voltas is a leading air conditioning and engineering services company. It is part of the Tata Group. The company excels in cooling solutions and projects."}
        ]
    }
}

# Load data function
@st.cache_data
def load_data():
    base_path = r"C:\Users\Srujan KV\Desktop\Srujan Zenshastra\WEEK 7\Indian stockk dashboard"
    weekly_data = pd.read_csv(os.path.join(base_path, 'etf_week.csv'))
    weekly_data.columns = weekly_data.columns.str.strip()
    weekly_data = weekly_data[['Date', 'Symbol', 'Close Price']]
    weekly_data['Date'] = pd.to_datetime(weekly_data['Date'])
    weekly_data['Close Price'] = weekly_data['Close Price'].astype(str).str.replace(',', '').astype(float)

    monthly_data = pd.read_csv(os.path.join(base_path, 'etf_month.csv'))
    monthly_data.columns = monthly_data.columns.str.strip()
    monthly_data = monthly_data[['Date', 'Symbol', 'Close Price']]
    monthly_data['Date'] = pd.to_datetime(monthly_data['Date'])
    monthly_data['Close Price'] = monthly_data['Close Price'].astype(str).str.replace(',', '').astype(float)

    high_low_data = pd.read_csv(os.path.join(base_path, '52W-high-low.csv'))
    high_low_data.columns = high_low_data.columns.str.strip()

    pe_data = pd.read_csv(os.path.join(base_path, 'PE.csv'))
    pe_data.columns = pe_data.columns.str.strip()

    traded_data = pd.read_csv(os.path.join(base_path, 'StocksTraded.csv'))
    traded_data.columns = traded_data.columns.str.strip()

    return weekly_data, monthly_data, high_low_data, pe_data, traded_data

try:
    weekly_data, monthly_data, high_low_data, pe_data, traded_data = load_data()
except FileNotFoundError as e:
    st.error(f"Error: {e}. Please ensure all CSV files are present in the specified directory.")
    st.stop()

# Get stock data function
def get_stock_data(symbol):
    symbol = symbol.strip().upper()
    weekly_perf = weekly_data[weekly_data['Symbol'].str.strip().str.upper() == symbol].sort_values('Date')
    monthly_perf = monthly_data[monthly_data['Symbol'].str.strip().str.upper() == symbol].sort_values('Date')
    
    try:
        high_low = high_low_data[high_low_data['SYMBOL'].str.strip().str.upper() == symbol].iloc[0]
        week_52_high = float(high_low['Adjusted 52_Week_High'])
        week_52_low = float(high_low['Adjusted 52_Week_Low'])
    except IndexError:
        week_52_high = "N/A"
        week_52_low = "N/A"
    
    try:
        pe = float(pe_data[pe_data['SYMBOL'].str.strip().str.upper() == symbol].iloc[0]['ADJUSTED P/E'])
    except IndexError:
        pe = "N/A"
    
    yield_value = round(random.uniform(1, 5), 2)
    
    try:
        traded = traded_data[traded_data['Symbol'].str.strip().str.upper() == symbol].iloc[0]
        ltp = float(traded['LTP'])
        percent_change = float(traded['%chng'])
        market_cap_value = float(traded['Mkt Cap (₹ Crores)'])
        market_cap = f"₹{market_cap_value:,.2f} Cr"
        
        # Classify market cap with new thresholds
        if market_cap_value > 50000:
            market_cap_class = "Large-cap"
        elif 16000 <= market_cap_value <= 50000:
            market_cap_class = "Mid-cap"
        else:
            market_cap_class = "Small-cap"
    except IndexError:
        ltp = "N/A"
        percent_change = "N/A"
        market_cap = "N/A"
        market_cap_class = "N/A"
    
    return {
        'weekly_performance': weekly_perf,
        'monthly_performance': monthly_perf,
        '52_week_high': week_52_high,
        '52_week_low': week_52_low,
        'pe_ratio': pe,
        'yield': yield_value,
        'market_cap': market_cap,
        'market_cap_class': market_cap_class,
        'ltp': ltp,
        'percent_change': percent_change
    }

# Main function for stock details page
def main():
    # Get the symbol from session state
    symbol = st.session_state.get('selected_symbol', None)
    
    if not symbol:
        st.error("No stock symbol provided. Please return to the dashboard and select a stock.")
        if st.button("Back to Dashboard"):
            st.switch_page("Home.py")
        return
    
    # Find stock info
    stock_info = None
    for sector in stocks["Sector"].values():
        for stock in sector:
            if stock["symbol"] == symbol:
                stock_info = stock
                break
        if stock_info:
            break
    
    if not stock_info:
        st.error(f"Stock {symbol} not found in the database.")
        if st.button("Back to Dashboard"):
            st.switch_page("Home.py")
        return
    
    # Stock Details
    st.subheader(f"{symbol} - {stock_info['company']}")
    
    stock_data = get_stock_data(symbol)
    
    # LTP and Percent Change (simple layout)
    change_class = "change-positive" if stock_data['percent_change'] != "N/A" and stock_data['percent_change'] > 0 else "change-negative"
    triangle = "▲" if stock_data['percent_change'] != "N/A" and stock_data['percent_change'] > 0 else "▼"
    details_header_html = f"""
    <div>
        <span class="details-ltp">₹{stock_data['ltp']}</span>
        <span class="details-change {change_class}">{triangle} {stock_data['percent_change']}%</span>
    </div>
    """
    st.markdown(details_header_html, unsafe_allow_html=True)
    
    # Stock Description
    st.markdown(f"**Description:** {stock_info['description']}")
    
    # Price Chart Section
    st.markdown("### Price Chart")
    
    # Toggle for Weekly/Monthly Data (positioned at top-right)
    if 'chart_view' not in st.session_state:
        st.session_state['chart_view'] = 'weekly'
    
    # Use a container with columns to position the toggle buttons horizontally
    col1, col2 = st.columns([5, 1])
    
    with col2:
        # Apply custom HTML/CSS for button alignment
        st.markdown('<div class="button-row">', unsafe_allow_html=True)
        left_col, right_col = st.columns(2)
        with left_col:
            weekly_button = st.button("1W")
        with right_col:
            monthly_button = st.button("1M")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if weekly_button:
            st.session_state['chart_view'] = 'weekly'
        if monthly_button:
            st.session_state['chart_view'] = 'monthly'
    
    # Display the selected chart
    if st.session_state['chart_view'] == 'weekly':
        # Weekly Performance Graph
        weekly_perf = stock_data['weekly_performance'].copy()
        if not weekly_perf.empty and not weekly_perf['Close Price'].isna().all():
            min_price = weekly_perf['Close Price'].min()
            max_price = weekly_perf['Close Price'].max()
            # Set Y-axis range to start below the minimum price
            y_axis_range = [min_price * 0.95, max_price * 1.05]  # 5% buffer below min and above max
            
            fig_weekly = px.line(weekly_perf, x='Date', y='Close Price', title=f"{symbol} - Weekly Performance",
                                 template="plotly_white" if not st.session_state.get('dark_mode', False) else "plotly_dark")
            fig_weekly.update_layout(
                xaxis_title="Date",
                yaxis_title="Price (₹)",
                yaxis=dict(range=y_axis_range, tickformat=".2f"),
                xaxis=dict(tickmode='auto', nticks=5, tickformat="%d %b %Y"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=50)  # Adjust top margin to prevent overlap with toggle
            )
            st.plotly_chart(fig_weekly, use_container_width=True)
        else:
            st.info(f"No weekly performance data available for {symbol}")
    
    else:
        # Monthly Performance Graph
        monthly_perf = stock_data['monthly_performance'].copy()
        if not monthly_perf.empty and not monthly_perf['Close Price'].isna().all():
            min_price = monthly_perf['Close Price'].min()
            max_price = monthly_perf['Close Price'].max()
            # Set Y-axis range to start below the minimum price
            y_axis_range = [min_price * 0.95, max_price * 1.05]  # 5% buffer below min and above max
            
            fig_monthly = px.line(monthly_perf, x='Date', y='Close Price', title=f"{symbol} - Monthly Performance",
                                  template="plotly_white" if not st.session_state.get('dark_mode', False) else "plotly_dark")
            fig_monthly.update_layout(
                xaxis_title="Date",
                yaxis_title="Price (₹)",
                yaxis=dict(range=y_axis_range, tickformat=".2f"),
                xaxis=dict(tickmode='auto', nticks=5, tickformat="%d %b %Y"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=50)  # Adjust top margin to prevent overlap with toggle
            )
            st.plotly_chart(fig_monthly, use_container_width=True)
        else:
            st.info(f"No monthly performance data available for {symbol}")
    
    # Company Overview Section
    st.subheader("Company Overview")
    cols = st.columns(3)
    with cols[0]:
        st.metric("P/E Ratio", stock_data['pe_ratio'])
    with cols[1]:
        st.metric("52-Week High", stock_data['52_week_high'])
    with cols[2]:
        st.metric("52-Week Low", stock_data['52_week_low'])
    
    cols = st.columns(3)
    with cols[0]:
        st.metric("Yield", f"{stock_data['yield']}%")
    with cols[1]:
        st.metric("Market Cap", stock_data['market_cap'])
    with cols[2]:
        st.metric("Market Cap Class", stock_data['market_cap_class'])
    
    # Back to Dashboard Button
    if st.button("Back to Dashboard"):
        st.switch_page("Home.py")

if __name__ == "__main__":
    main()