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

# Initialize session state for dark mode if not exists
if 'dark_mode' not in st.session_state:
    st.session_state['dark_mode'] = False

# Enhanced Custom CSS for modern UI with dynamic theme switching
st.markdown("""
<style>
    /* Modern Color Palette */
    :root {
        --primary: #2563eb;
        --primary-light: #3b82f6;
        --secondary: #64748b;
        --accent: #0ea5e9;
        --background: #f8fafc;
        --card: #ffffff;
        --text: #1e293b;
        --text-light: #64748b;
        --success: #22c55e;
        --danger: #ef4444;
        --warning: #f59e0b;
        --border: #e2e8f0;
    }

    /* Dark Mode Colors */
    [data-theme="dark"] {
        --primary: #3b82f6;
        --primary-light: #60a5fa;
        --secondary: #94a3b8;
        --accent: #0ea5e9;
        --background: #0f172a;
        --card: #1e293b;
        --text: #f8fafc;
        --text-light: #cbd5e1;
        --border: #334155;
    }

    /* Apply theme to Streamlit elements */
    .stApp {
        background-color: var(--background);
        color: var(--text);
    }

    .stMarkdown, .stText {
        color: var(--text);
    }

    /* General Layout */
    .main {
        background: var(--background);
        color: var(--text);
        font-family: 'Inter', sans-serif;
        padding: 2rem;
    }

    /* Dashboard Header */
    .dashboard-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        border-radius: 1rem;
        color: white;
    }

    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .dashboard-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
    }

    /* Modern Stock Card */
    .stock-card {
        background: var(--card);
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid var(--border);
        transition: all 0.3s ease;
    }

    .stock-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    /* Stock Card Content */
    .stock-symbol {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 0.25rem;
    }

    .stock-company {
        font-size: 0.875rem;
        color: var(--text-light);
        margin-bottom: 1rem;
    }

    .stock-price {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 0.5rem;
    }

    .price-change {
        display: inline-flex;
        align-items: center;
        padding: 0.375rem 0.75rem;
        border-radius: 0.5rem;
        font-weight: 600;
        font-size: 0.875rem;
        margin-bottom: 1rem;
    }

    .price-change.positive {
        background: rgba(34, 197, 94, 0.1);
        color: var(--success);
    }

    .price-change.negative {
        background: rgba(239, 68, 68, 0.1);
        color: var(--danger);
    }

    /* Metrics Display */
    .metrics-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.75rem;
        margin-top: 1rem;
    }

    .metric {
        background: var(--background);
        padding: 0.75rem;
        border-radius: 0.5rem;
        text-align: center;
    }

    .metric-label {
        font-size: 0.75rem;
        color: var(--text-light);
        margin-bottom: 0.25rem;
    }

    .metric-value {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text);
    }

    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text);
        margin: 2rem 0 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--border);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        margin-bottom: 1rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: var(--card);
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        color: var(--text);
        border: 1px solid var(--border);
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

    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background: var(--card);
        padding: 1.5rem;
        border-radius: 1rem;
    }

    /* Filter Controls */
    .filter-section {
        margin-bottom: 1.5rem;
    }

    .filter-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text);
        margin-bottom: 0.75rem;
    }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        padding: 0.75rem;
        border-radius: 0.5rem;
        background: var(--primary);
        color: white;
        border: none;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        background: var(--primary-light);
        transform: translateY(-1px);
    }
</style>

<script>
    // Function to set theme
    function setTheme(isDark) {
        document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
    }

    // Initialize theme
    setTheme(window.localStorage.getItem('dark_mode') === 'true');

    // Watch for theme changes
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === 'attributes' && mutation.attributeName === 'data-theme') {
                const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
                window.localStorage.setItem('dark_mode', isDark);
            }
        });
    });

    observer.observe(document.documentElement, { attributes: true });
</script>
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

def main():
    # Dashboard Header
    st.markdown("""
    <div class="dashboard-header">
        <div class="dashboard-title">Indian Stock Analysis Dashboard</div>
        <div class="dashboard-subtitle">Real-time market insights and analysis</div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar Controls
    with st.sidebar:
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.title("Dashboard Controls")
        
        # Dark Mode Toggle
        dark_mode = st.toggle("Dark Mode", help="Toggle dark mode theme")
        if dark_mode:
            st.markdown('<script>document.documentElement.setAttribute("data-theme", "dark")</script>', unsafe_allow_html=True)
            st.session_state['dark_mode'] = True
        else:
            st.markdown('<script>document.documentElement.setAttribute("data-theme", "light")</script>', unsafe_allow_html=True)
            st.session_state['dark_mode'] = False
        
        # Filters
        st.markdown('<div class="filter-title">Filters</div>', unsafe_allow_html=True)
        sector_filter = st.multiselect(
            "Select Sectors",
            options=stocks["Sector"].keys(),
            default=list(stocks["Sector"].keys())
        )
        
        market_cap_filter = st.multiselect(
            "Select Market Cap",
            options=stocks["Market-cap"].keys(),
            default=list(stocks["Market-cap"].keys())
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Main Content
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
        populate_market_cap_stocks()  # Update market cap classifications
        
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
                st.info(f"No stocks available in {cap} category based on current data.")

if __name__ == "__main__":
    main()
