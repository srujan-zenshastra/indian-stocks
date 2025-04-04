import pandas as pd
import streamlit as st
import plotly.express as px
import os
import random

# Set page configuration
st.set_page_config(
    page_title="Stock Details",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS for modern UI
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
    }

    /* Modern Card Design */
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

    /* Typography */
    .stock-title {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .stock-subtitle {
        font-size: 1.1rem;
        color: var(--text-light);
        margin-bottom: 1.5rem;
    }

    /* Price Display */
    .price-container {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .current-price {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text);
    }

    .price-change {
        font-size: 1.2rem;
        font-weight: 600;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }

    .price-change.positive {
        background: rgba(34, 197, 94, 0.1);
        color: var(--success);
    }

    .price-change.negative {
        background: rgba(239, 68, 68, 0.1);
        color: var(--danger);
    }

    /* Metrics Grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }

    .metric-card {
        background: var(--card);
        padding: 1rem;
        border-radius: 0.75rem;
        border: 1px solid var(--border);
    }

    .metric-label {
        font-size: 0.875rem;
        color: var(--text-light);
        margin-bottom: 0.25rem;
    }

    .metric-value {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text);
    }

    /* Chart Container */
    .chart-container {
        background: var(--card);
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid var(--border);
    }

    /* Toggle Buttons */
    .toggle-container {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }

    .toggle-button {
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        border: 1px solid var(--border);
        background: var(--card);
        color: var(--text);
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .toggle-button:hover {
        background: var(--primary-light);
        color: white;
    }

    .toggle-button.active {
        background: var(--primary);
        color: white;
        border-color: var(--primary);
    }

    /* Back Button */
    .back-button {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        background: var(--primary);
        color: white;
        text-decoration: none;
        transition: all 0.2s ease;
        margin-top: 1.5rem;
    }

    .back-button:hover {
        background: var(--primary-light);
        transform: translateY(-1px);
    }

    /* Description Card */
    .description-card {
        background: var(--card);
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid var(--border);
    }

    .description-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text);
        margin-bottom: 1rem;
    }

    .description-content {
        color: var(--text-light);
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# Define stock data
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
    }
}

# Load data function
@st.cache_data
def load_data():
    try:
        weekly_data = pd.read_csv('etf_week.csv')
        weekly_data.columns = weekly_data.columns.str.strip()
        weekly_data = weekly_data[['Date', 'Symbol', 'Close Price']]
        weekly_data['Date'] = pd.to_datetime(weekly_data['Date'])
        weekly_data['Close Price'] = weekly_data['Close Price'].astype(str).str.replace(',', '').astype(float)

        monthly_data = pd.read_csv('etf_month.csv')
        monthly_data.columns = monthly_data.columns.str.strip()
        monthly_data = monthly_data[['Date', 'Symbol', 'Close Price']]
        monthly_data['Date'] = pd.to_datetime(monthly_data['Date'])
        monthly_data['Close Price'] = monthly_data['Close Price'].astype(str).str.replace(',', '').astype(float)

        high_low_data = pd.read_csv('52W-high-low.csv')
        high_low_data.columns = high_low_data.columns.str.strip()

        pe_data = pd.read_csv('PE.csv')
        pe_data.columns = pe_data.columns.str.strip()

        traded_data = pd.read_csv('StocksTraded.csv')
        traded_data.columns = traded_data.columns.str.strip()

        return weekly_data, monthly_data, high_low_data, pe_data, traded_data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None, None, None, None

# Get stock data function
def get_stock_data(symbol):
    try:
        weekly_data, monthly_data, high_low_data, pe_data, traded_data = load_data()
        if any(data is None for data in [weekly_data, monthly_data, high_low_data, pe_data, traded_data]):
            return None

        symbol = symbol.strip().upper()
        weekly_perf = weekly_data[weekly_data['Symbol'].str.strip().str.upper() == symbol].sort_values('Date')
        monthly_perf = monthly_data[monthly_data['Symbol'].str.strip().str.upper() == symbol].sort_values('Date')
        
        try:
            high_low = high_low_data[high_low_data['SYMBOL'].str.strip().str.upper() == symbol].iloc[0]
            week_52_high = float(str(high_low['Adjusted 52_Week_High']).replace(',', ''))
            week_52_low = float(str(high_low['Adjusted 52_Week_Low']).replace(',', ''))
        except (IndexError, ValueError):
            week_52_high = 0
            week_52_low = 0
        
        try:
            pe = float(pe_data[pe_data['SYMBOL'].str.strip().str.upper() == symbol].iloc[0]['ADJUSTED P/E'])
        except (IndexError, ValueError):
            pe = 0
        
        yield_value = round(random.uniform(1, 5), 2)
        
        try:
            traded = traded_data[traded_data['Symbol'].str.strip().str.upper() == symbol].iloc[0]
            ltp = float(str(traded['LTP']).replace(',', ''))
            percent_change = float(str(traded['%chng']).replace(',', ''))
            market_cap_value = float(str(traded['Mkt Cap (₹ Crores)']).replace(',', ''))
            market_cap = f"₹{market_cap_value:,.2f} Cr"
            
            if market_cap_value > 50000:
                market_cap_class = "Large-cap"
            elif 16000 <= market_cap_value <= 50000:
                market_cap_class = "Mid-cap"
            else:
                market_cap_class = "Small-cap"
        except (IndexError, ValueError):
            ltp = 0
            percent_change = 0
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
    except Exception as e:
        st.error(f"Error processing stock data: {str(e)}")
        return None

# Function to display stock card
def display_stock_card(symbol, stock_info, stock_data):
    try:
        ltp = stock_data.get('ltp', 'N/A')
        ltp_display = f"₹{ltp:,.2f}" if isinstance(ltp, (int, float)) else str(ltp)
        
        percent_change = stock_data.get('percent_change', 'N/A')
        if isinstance(percent_change, (int, float)):
            percent_display = f"{'+' if percent_change >= 0 else ''}{percent_change:.2f}%"
            change_class = 'positive' if percent_change >= 0 else 'negative'
            change_icon = '▲' if percent_change >= 0 else '▼'
        else:
            percent_display = str(percent_change)
            change_class = 'negative'
            change_icon = '—'
        
        company_name = stock_info.get('company', 'Unknown Company')
    except Exception as e:
        st.error(f"Error preparing stock data: {e}")
        return

    html_content = f"""
    <div class="stock-card">
        <div class="stock-title">
            {symbol}
            <div style="font-size: 1.2rem; color: var(--text-light); display: inline;"> • </div>
            <div style="font-size: 1.2rem; color: var(--text-light); display: inline;">{company_name}</div>
        </div>
        <div class="price-container">
            <div class="current-price">{ltp_display}</div>
            <div class="price-change {change_class}">
                {percent_display} {change_icon}
            </div>
        </div>
    </div>
    """

    try:
        st.markdown(html_content, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error rendering stock card: {e}")

def main():
    symbol = st.session_state.get('selected_symbol', None)
    
    if not symbol:
        st.error("No stock symbol provided. Please return to the dashboard and select a stock.")
        if st.button("Back to Dashboard", key="back_error"):
            st.switch_page("home.py")
        return
    
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
        if st.button("Back to Dashboard", key="back_not_found"):
            st.switch_page("home.py")
        return
    
    stock_data = get_stock_data(symbol)
    if stock_data is None:
        st.error("Error loading stock data. Please try again.")
        if st.button("Back to Dashboard", key="back_error_data"):
            st.switch_page("home.py")
        return

    display_stock_card(symbol, stock_info, stock_data)
    
    st.markdown(f"""
    <div class="description-card">
        <div class="description-title">Company Overview</div>
        <div class="description-content">{stock_info['description']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-label">P/E Ratio</div>
            <div class="metric-value">{stock_data['pe_ratio']:.2f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">52-Week High</div>
            <div class="metric-value">₹{stock_data['52_week_high']:,.2f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">52-Week Low</div>
            <div class="metric-value">₹{stock_data['52_week_low']:,.2f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Yield</div>
            <div class="metric-value">{stock_data['yield']:.2f}%</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Market Cap</div>
            <div class="metric-value">{stock_data['market_cap']}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Category</div>
            <div class="metric-value">{stock_data['market_cap_class']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="chart-container">
        <h2 style="margin-bottom: 1rem;">Price History</h2>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    with col2:
        st.markdown('<div class="toggle-container">', unsafe_allow_html=True)
        weekly = st.button("1W", key="weekly", help="Show weekly data")
        monthly = st.button("1M", key="monthly", help="Show monthly data")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if 'chart_view' not in st.session_state:
        st.session_state['chart_view'] = 'weekly'
    
    if weekly:
        st.session_state['chart_view'] = 'weekly'
    if monthly:
        st.session_state['chart_view'] = 'monthly'
    
    if st.session_state['chart_view'] == 'weekly':
        data = stock_data['weekly_performance']
        title = "Weekly Performance"
    else:
        data = stock_data['monthly_performance']
        title = "Monthly Performance"
    
    if not data.empty and not data['Close Price'].isna().all():
        fig = px.line(data, x='Date', y='Close Price',
                     title=f"{symbol} - {title}",
                     template="plotly_white" if not st.session_state.get('dark_mode', False) else "plotly_dark")
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Date",
            yaxis_title="Price (₹)",
            hovermode='x unified',
            showlegend=False,
            margin=dict(t=30, r=10, b=30, l=60)
        )
        
        fig.update_traces(
            line_color='#2563eb',
            line_width=2,
            hovertemplate='₹%{y:,.2f}<extra></extra>'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(f"No {title.lower()} data available for {symbol}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("← Back to Dashboard", key="back_main"):
        st.switch_page("home.py")

if __name__ == "__main__":
    main()
