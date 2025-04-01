import pandas as pd
import streamlit as st
import plotly.express as px
import os
import random

# Set page configuration
st.set_page_config(
    page_title="Indian Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* General Styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
    }
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background: #2c3e50;
        color: white;
    }
    
    /* Stock Card Styling */
    .stock-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border-left: 5px solid #3498db;
    }
    .stock-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    /* Typography */
    .title {
        font-size: 20px;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 2px;
    }
    .company {
        color: #7f8c8d;
        font-size: 14px;
        margin-bottom: 10px;
    }
    .ltp {
        font-size: 24px;
        font-weight: 700;
        color: #2c3e50;
        margin: 5px 0;
    }
    .change-container {
        display: flex;
        align-items: center;
        margin: 5px 0;
    }
    .change {
        font-size: 16px;
        font-weight: 600;
        margin-right: 5px;
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
    
    /* Header */
    .header {
        text-align: center;
        color: #2c3e50;
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 30px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        background-color: #ecf0f1;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        margin-right: 5px;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #3498db;
        color: white;
    }
    
    /* Dark Mode */
    [data-theme="dark"] .main {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
    }
    [data-theme="dark"] .stock-card {
        background: #34495e;
        color: white;
    }
    [data-theme="dark"] .title {
        color: #ecf0f1;
    }
    [data-theme="dark"] .company {
        color: #bdc3c7;
    }
    [data-theme="dark"] .ltp {
        color: #ecf0f1;
    }
    [data-theme="dark"] .metric {
        color: #ecf0f1;
    }
    [data-theme="dark"] .metric-value {
        color: #3498db;
    }
    [data-theme="dark"] .header {
        color: #ecf0f1;
    }
</style>
""", unsafe_allow_html=True)

# Define stock data with updated stocks
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
    },
    "Market-cap": {
        "Large-cap": [],
        "Mid-cap": [],
        "Small-cap": []
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

# Function to populate market-cap categories dynamically
def populate_market_cap_stocks():
    # Clear existing market-cap lists
    stocks["Market-cap"]["Large-cap"].clear()
    stocks["Market-cap"]["Mid-cap"].clear()
    stocks["Market-cap"]["Small-cap"].clear()
    
    # Collect all stocks from Sector dictionary
    all_stocks = []
    for sector in stocks["Sector"].values():
        all_stocks.extend(sector)
    
    # Classify each stock based on market cap
    for stock_info in all_stocks:
        symbol = stock_info["symbol"]
        stock_data = get_stock_data(symbol)
        market_cap_class = stock_data['market_cap_class']
        
        if market_cap_class == "Large-cap":
            stocks["Market-cap"]["Large-cap"].append(stock_info)
        elif market_cap_class == "Mid-cap":
            stocks["Market-cap"]["Mid-cap"].append(stock_info)
        elif market_cap_class == "Small-cap":
            stocks["Market-cap"]["Small-cap"].append(stock_info)

# Sidebar
with st.sidebar:
    st.title("Dashboard Controls")
    dark_mode = st.toggle("Dark Mode")
    if dark_mode:
        st.markdown('<style>body {background-color: #2c3e50; color: white;}</style>', unsafe_allow_html=True)
        st.markdown('<script>document.documentElement.setAttribute("data-theme", "dark")</script>', unsafe_allow_html=True)
        st.session_state['dark_mode'] = True
    else:
        st.markdown('<script>document.documentElement.setAttribute("data-theme", "light")</script>', unsafe_allow_html=True)
        st.session_state['dark_mode'] = False
    
    st.subheader("Filters")
    sector_filter = st.multiselect("Select Sectors", options=stocks["Sector"].keys(), default=list(stocks["Sector"].keys()))
    market_cap_filter = st.multiselect("Select Market Cap", options=stocks["Market-cap"].keys(), default=list(stocks["Market-cap"].keys()))

# Main app
def main():
    # Populate market-cap stocks dynamically
    populate_market_cap_stocks()
    
    st.markdown("<h1 class='header'>Indian Stock Analysis Dashboard</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Sector-wise", "Market-cap wise"])
    
    with tab1:
        st.header("Sector-wise Stocks")
        for sector in sector_filter:
            st.subheader(sector)
            cols = st.columns(2)
            for i, stock_info in enumerate(stocks["Sector"][sector]):
                symbol = stock_info["symbol"]
                company = stock_info["company"]
                stock_data = get_stock_data(symbol)
                
                with cols[i % 2]:
                    change_class = "change-positive" if stock_data['percent_change'] != "N/A" and stock_data['percent_change'] > 0 else "change-negative"
                    triangle = "▲" if stock_data['percent_change'] != "N/A" and stock_data['percent_change'] > 0 else "▼"
                    card_html = f"""
                    <div class="stock-card">
                        <div class="title">{symbol}</div>
                        <div class="company">{company}</div>
                        <div class="ltp">₹{stock_data['ltp']}</div>
                        <div class="change-container">
                            <span class="change {change_class}">{triangle} {stock_data['percent_change']}%</span>
                        </div>
                        <div class="metric">P/E: <span class="metric-value">{stock_data['pe_ratio']}</span></div>
                        <div class="metric">Yield: <span class="metric-value">{stock_data['yield']}%</span></div>
                        <div class="metric">Market Cap: <span class="metric-value">{stock_data['market_cap_class']}</span></div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
                    if st.button(f"Details", key=f"btn_{symbol}_{sector}"):
                        st.session_state['selected_symbol'] = symbol
                        st.switch_page("pages/stock_details.py")
    
    with tab2:
        st.header("Market-cap wise Stocks")
        for cap in market_cap_filter:
            st.subheader(cap)
            if stocks["Market-cap"][cap]:  # Check if there are stocks in this category
                cols = st.columns(min(2, len(stocks["Market-cap"][cap])))
                for i, stock_info in enumerate(stocks["Market-cap"][cap]):
                    symbol = stock_info["symbol"]
                    company = stock_info["company"]
                    stock_data = get_stock_data(symbol)
                    
                    with cols[i % len(cols)]:
                        change_class = "change-positive" if stock_data['percent_change'] != "N/A" and stock_data['percent_change'] > 0 else "change-negative"
                        triangle = "▲" if stock_data['percent_change'] != "N/A" and stock_data['percent_change'] > 0 else "▼"
                        card_html = f"""
                        <div class="stock-card">
                            <div class="title">{symbol}</div>
                            <div class="company">{company}</div>
                            <div class="ltp">₹{stock_data['ltp']}</div>
                            <div class="change-container">
                                <span class="change {change_class}">{triangle} {stock_data['percent_change']}%</span>
                            </div>
                            <div class="metric">P/E: <span class="metric-value">{stock_data['pe_ratio']}</span></div>
                            <div class="metric">Yield: <span class="metric-value">{stock_data['yield']}%</span></div>
                            <div class="metric">Market Cap: <span class="metric-value">{stock_data['market_cap_class']}</span></div>
                        </div>
                        """
                        st.markdown(card_html, unsafe_allow_html=True)
                        if st.button(f"Details", key=f"btn_cap_{symbol}_{cap}"):
                            st.session_state['selected_symbol'] = symbol
                            st.switch_page("pages/stock_details.py")
            else:
                st.info(f"No stocks available in {cap} category based on current data.")

if __name__ == "__main__":
    main()