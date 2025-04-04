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

# Enhanced Modern CSS (without dark mode)
st.markdown("""
<style>
    /* Modern Color Palette */
    :root {
        --primary: #4f46e5; /* Indigo */
        --primary-light: #818cf8;
        --secondary: #6b7280; /* Gray */
        --accent: #14b8a6; /* Teal */
        --background: #f9fafb; /* Light Gray */
        --card: #ffffff;
        --text: #111827; /* Dark Gray */
        --text-light: #6b7280;
        --success: #10b981;
        --danger: #ef4444;
        --warning: #f59e0b;
        --border: #e5e7eb;
    }

    /* Base Styles */
    .stApp {
        background-color: var(--background);
        color: var(--text);
        font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        transition: all 0.3s ease;
    }

    /* Dashboard Header */
    .dashboard-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        padding: 2.5rem 1rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
    }

    .dashboard-title {
        font-size: 2.75rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.025em;
    }

    .dashboard-subtitle {
        font-size: 1.25rem;
        opacity: 0.85;
    }

    /* Stock Card */
    .stock-card {
        background: var(--card);
        border-radius: 12px;
        padding: 1.75rem;
        margin: 1rem 0;
        border: 1px solid var(--border);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    .stock-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
    }

    .stock-symbol {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 0.5rem;
    }

    .stock-company {
        font-size: 0.95rem;
        color: var(--text-light);
        margin-bottom: 1rem;
    }

    .stock-price {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 0.75rem;
    }

    .price-change {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.95rem;
    }

    .price-change.positive {
        background: rgba(16, 185, 129, 0.15);
        color: var(--success);
    }

    .price-change.negative {
        background: rgba(239, 68, 68, 0.15);
        color: var(--danger);
    }

    /* Metrics */
    .metrics-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-top: 1.25rem;
    }

    .metric {
        background: var(--background);
        padding: 0.75rem;
        border-radius: 8px;
        text-align: center;
        transition: background 0.2s ease;
    }

    .metric:hover {
        background: var(--border);
    }

    .metric-label {
        font-size: 0.85rem;
        color: var(--text-light);
        margin-bottom: 0.25rem;
    }

    .metric-value {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text);
    }

    /* Section Headers */
    .section-header {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text);
        margin: 2.5rem 0 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid var(--primary);
        display: inline-block;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: var(--card);
        border-radius: 10px;
        padding: 0.85rem 1.75rem;
        color: var(--text);
        border: 1px solid var(--border);
        transition: all 0.2s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: var(--primary-light);
        color: white;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: var(--primary);
        color: white;
        border-color: var(--primary);
    }

    /* Sidebar */
    .sidebar .sidebar-content {
        background: var(--card);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    .filter-section {
        margin-bottom: 2rem;
    }

    .filter-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text);
        margin-bottom: 1rem;
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        padding: 0.85rem;
        border-radius: 10px;
        background: var(--primary);
        color: white;
        border: none;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        background: var(--primary-light);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Define stock data with updated stocks
stocks = {
    "Sector": {
        "Tech": [
            {"symbol": "INFY", "company": "Infosys Ltd.", "description": "Infosys is a global leader in next-generation digital services and consulting."},
            {"symbol": "TCS", "company": "Tata Consultancy Services Ltd.", "description": "TCS is a leading global IT services, consulting, and business solutions organization."},
            {"symbol": "COFORGE", "company": "Coforge Ltd.", "description": "Coforge is a global IT solutions organization providing digital services."},
            {"symbol": "MASTEK", "company": "Mastek Ltd.", "description": "Mastek provides enterprise technology solutions and digital transformation services."}
        ],
        "Finance": [
            {"symbol": "HDFCBANK", "company": "HDFC Bank Ltd.", "description": "HDFC Bank is one of India's premier banking institutions."},
            {"symbol": "SBIN", "company": "State Bank of India", "description": "SBI is India's largest public sector bank providing comprehensive banking services."},
            {"symbol": "IDFCFIRSTB", "company": "IDFC First Bank Ltd.", "description": "IDFC First Bank offers banking and financial services with a focus on retail and business banking."},
            {"symbol": "DCBBANK", "company": "DCB Bank Ltd.", "description": "DCB Bank provides banking services to individuals and businesses in India."}
        ],
        "Energy": [
            {"symbol": "TATAPOWER", "company": "Tata Power Company Ltd.", "description": "Tata Power is one of India's largest integrated power companies."},
            {"symbol": "ADANIGREEN", "company": "Adani Green Energy Ltd.", "description": "Adani Green is a leading renewable energy company in India."},
            {"symbol": "NHPC", "company": "NHPC Ltd.", "description": "NHPC is a major hydropower generation company in India."},
            {"symbol": "RELINFRA", "company": "Reliance Infrastructure Ltd.", "description": "Reliance Infra is involved in power generation, transmission, and distribution."}
        ],
        "Consumer": [
            {"symbol": "HINDUNILVR", "company": "Hindustan Unilever Ltd.", "description": "Hindustan Unilever is a leading consumer goods company in India."},
            {"symbol": "ITC", "company": "ITC Ltd.", "description": "ITC is a diversified conglomerate with a strong presence in FMCG."},
            {"symbol": "BAJAJELEC", "company": "Bajaj Electricals Ltd.", "description": "Bajaj Electricals is a consumer electrical equipment manufacturing company."},
            {"symbol": "VOLTAS", "company": "Voltas Ltd.", "description": "Voltas is a leading air conditioning and engineering services company."}
        ]
    },
    "Market-cap": {
        "Large-cap": [],
        "Mid-cap": [],
        "Small-cap": []
    }
}

# Define indices data
indices = {
    "NIFTY 50": {"description": "NIFTY 50 is the benchmark index of the National Stock Exchange of India, representing the top 50 companies."},
    "NIFTY 100": {"description": "NIFTY 100 includes the top 100 companies by market capitalization listed on the NSE."},
    "NIFTY BANK": {"description": "NIFTY BANK tracks the performance of the most liquid and large capitalized banking stocks."}
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

    index_data = pd.read_csv(os.path.join(base_path, 'index_data.csv'))
    index_data.columns = [col.strip() for col in index_data.columns]

    return weekly_data, monthly_data, high_low_data, pe_data, traded_data, index_data

try:
    weekly_data, monthly_data, high_low_data, pe_data, traded_data, index_data = load_data()
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

# Get index data function
def get_index_data(index_name):
    try:
        if index_data.empty:
            st.warning(f"index_data.csv is empty!")
            return {
                'ltp': "N/A",
                'change': "N/A",
                'percent_change': "N/A",
                '52_week_high': "N/A",
                '52_week_low': "N/A",
                'value': "N/A"
            }

        required_columns = ['SYMBOL', 'LTP', 'CHNG', '%CHNG', '52W H', '52W L', 'VALUE (₹ Crores)']
        missing_columns = [col for col in required_columns if col not in index_data.columns]
        if missing_columns:
            st.warning(f"Missing columns in index_data.csv: {missing_columns}")
            return {
                'ltp': "N/A",
                'change': "N/A",
                'percent_change': "N/A",
                '52_week_high': "N/A",
                '52_week_low': "N/A",
                'value': "N/A"
            }

        if index_name not in index_data['SYMBOL'].str.strip().values:
            st.warning(f"Index '{index_name}' not found in index_data.csv. Available indices: {list(index_data['SYMBOL'].str.strip().unique())}")
            return {
                'ltp': "N/A",
                'change': "N/A",
                'percent_change': "N/A",
                '52_week_high': "N/A",
                '52_week_low': "N/A",
                'value': "N/A"
            }

        index_row = index_data[index_data['SYMBOL'].str.strip() == index_name].iloc[0]
        ltp = float(str(index_row['LTP']).replace(',', ''))
        change = float(str(index_row['CHNG']).replace(',', ''))
        percent_change = float(str(index_row['%CHNG']).replace(',', ''))
        week_52_high = float(str(index_row['52W H']).replace(',', ''))
        week_52_low = float(str(index_row['52W L']).replace(',', ''))
        value = float(str(index_row['VALUE (₹ Crores)']).replace(',', ''))
        return {
            'ltp': ltp,
            'change': change,
            'percent_change': percent_change,
            '52_week_high': week_52_high,
            '52_week_low': week_52_low,
            'value': value
        }
    except (IndexError, ValueError) as e:
        st.warning(f"Error processing data for index '{index_name}': {str(e)}")
        return {
            'ltp': "N/A",
            'change': "N/A",
            'percent_change': "N/A",
            '52_week_high': "N/A",
            '52_week_low': "N/A",
            'value': "N/A"
        }

# Function to populate market-cap categories dynamically
def populate_market_cap_stocks():
    stocks["Market-cap"]["Large-cap"].clear()
    stocks["Market-cap"]["Mid-cap"].clear()
    stocks["Market-cap"]["Small-cap"].clear()
    
    all_stocks = []
    for sector in stocks["Sector"].values():
        all_stocks.extend(sector)
    
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

def main():
    # Dashboard Header
    st.markdown("""
    <div class="dashboard-header">
        <div class="dashboard-title">Indian Stock Analysis Dashboard</div>
        <div class="dashboard-subtitle">Real-time Insights for Smart Investing</div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar Controls
    with st.sidebar:
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.title("Controls")
        
        st.markdown('<div class="filter-title">Filters</div>', unsafe_allow_html=True)
        sector_filter = st.multiselect(
            "Sectors",
            options=list(stocks["Sector"].keys()),
            default=list(stocks["Sector"].keys())
        )
        
        market_cap_filter = st.multiselect(
            "Market Cap",
            options=list(stocks["Market-cap"].keys()),
            default=list(stocks["Market-cap"].keys())
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Market Overview Section
    st.markdown('<div class="section-header">Market Overview</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, (index_name, index_info) in enumerate(indices.items()):
        index_data = get_index_data(index_name)
        with cols[i]:
            if isinstance(index_data['percent_change'], (int, float)):
                change_class = "positive" if index_data['percent_change'] > 0 else "negative"
                triangle = "▲" if index_data['percent_change'] > 0 else "▼"
                percent_display = f"{index_data['percent_change']:+.2f}"
                change_display = f"{index_data['change']:+.2f}"
            else:
                change_class = "negative"
                triangle = "—"
                percent_display = "N/A"
                change_display = "N/A"
            
            ltp_display = f"₹{index_data['ltp']:,.2f}" if isinstance(index_data['ltp'], (int, float)) else "N/A"
            
            st.markdown(f"""
            <div class="stock-card">
                <div class="stock-symbol">{index_name}</div>
                <div class="stock-price">{ltp_display}</div>
                <div class="price-change {change_class}">
                    {triangle} {percent_display}% ({change_display})
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View Details", key=f"index_{index_name}"):
                st.session_state['selected_index'] = index_name
                st.switch_page("pages/index_details.py")

    # Main Content Tabs
    tab1, tab2 = st.tabs(["Sector-wise", "Market-cap wise"])
    
    with tab1:
        st.markdown('<div class="section-header">Sector-wise Stocks</div>', unsafe_allow_html=True)
        for sector in sector_filter:
            st.subheader(sector)
            cols = st.columns(2)
            for i, stock_info in enumerate(stocks["Sector"][sector]):
                symbol = stock_info["symbol"]
                company = stock_info["company"]
                stock_data = get_stock_data(symbol)
                
                with cols[i % 2]:
                    change_class = "positive" if stock_data['percent_change'] > 0 else "negative"
                    triangle = "▲" if stock_data['percent_change'] > 0 else "▼"
                    
                    st.markdown(f"""
                    <div class="stock-card">
                        <div class="stock-symbol">{symbol}</div>
                        <div class="stock-company">{company}</div>
                        <div class="stock-price">₹{stock_data['ltp']:,.2f}</div>
                        <div class="price-change {change_class}">
                            {triangle} {stock_data['percent_change']:+.2f}%
                        </div>
                        <div class="metrics-container">
                            <div class="metric">
                                <div class="metric-label">P/E</div>
                                <div class="metric-value">{stock_data['pe_ratio']}</div>
                            </div>
                            <div class="metric">
                                <div class="metric-label">Yield</div>
                                <div class="metric-value">{stock_data['yield']}%</div>
                            </div>
                            <div class="metric">
                                <div class="metric-label">Category</div>
                                <div class="metric-value">{stock_data['market_cap_class']}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("View Details", key=f"btn_{symbol}_{sector}"):
                        st.session_state['selected_symbol'] = symbol
                        st.switch_page("pages/stock_details.py")
    
    with tab2:
        st.markdown('<div class="section-header">Market-cap wise Stocks</div>', unsafe_allow_html=True)
        populate_market_cap_stocks()
        
        for cap in market_cap_filter:
            st.subheader(cap)
            if stocks["Market-cap"][cap]:
                cols = st.columns(2)
                for i, stock_info in enumerate(stocks["Market-cap"][cap]):
                    symbol = stock_info["symbol"]
                    company = stock_info["company"]
                    stock_data = get_stock_data(symbol)
                    
                    with cols[i % 2]:
                        change_class = "positive" if stock_data['percent_change'] > 0 else "negative"
                        triangle = "▲" if stock_data['percent_change'] > 0 else "▼"
                        
                        st.markdown(f"""
                        <div class="stock-card">
                            <div class="stock-symbol">{symbol}</div>
                            <div class="stock-company">{company}</div>
                            <div class="stock-price">₹{stock_data['ltp']:,.2f}</div>
                            <div class="price-change {change_class}">
                                {triangle} {stock_data['percent_change']:+.2f}%
                            </div>
                            <div class="metrics-container">
                                <div class="metric">
                                    <div class="metric-label">P/E</div>
                                    <div class="metric-value">{stock_data['pe_ratio']}</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-label">Yield</div>
                                    <div class="metric-value">{stock_data['yield']}%</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-label">Market Cap</div>
                                    <div class="metric-value">{stock_data['market_cap']}</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("View Details", key=f"btn_cap_{symbol}_{cap}"):
                            st.session_state['selected_symbol'] = symbol
                            st.switch_page("pages/stock_details.py")
            else:
                st.info(f"No stocks available in {cap} category.")

if __name__ == "__main__":
    main()
