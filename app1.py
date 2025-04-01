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
    initial_sidebar_state="collapsed"
)

# Custom styling with improved design
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #5642FA;
        --secondary-color: #2B2B2B;
        --accent-color: #FF5252;
        --light-gray: #F5F7FA;
        --text-color: #2B2B2B;
        --success-color: #4CAF50;
        --warning-color: #FFC107;
        --info-color: #2196F3;
    }
    
    /* Global styles */
    body {
        font-family: 'Inter', sans-serif;
        color: var(--text-color);
        background-color: var(--light-gray);
    }
    
    .stApp {
        background-color: var(--light-gray);
    }
    
    /* Header styling */
    .header {
        text-align: center;
        margin-bottom: 30px;
        color: var(--primary-color);
        font-weight: 700;
        font-size: 2.5rem;
        padding: 20px 0;
        border-bottom: 2px solid #EEF2F6;
    }
    
    .subheader {
        color: var(--secondary-color);
        font-weight: 600;
        border-left: 4px solid var(--primary-color);
        padding-left: 10px;
        margin: 20px 0;
    }
    
    /* Stock card styling */
    .stock-card {
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        margin-bottom: 24px;
        background-color: white;
        transition: all 0.3s ease;
        border: 1px solid #EEF2F6;
        cursor: pointer;
    }
    
    .stock-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(86, 66, 250, 0.15);
        border-color: var(--primary-color);
    }
    
    .title {
        font-size: 22px;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 5px;
    }
    
    .company {
        color: #6B7280;
        font-size: 14px;
        margin-bottom: 16px;
        font-weight: 500;
    }
    
    .metrics {
        display: flex;
        justify-content: space-between;
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px solid #EEF2F6;
    }
    
    .metric {
        display: inline-block;
        font-size: 14px;
        color: #6B7280;
    }
    
    .metric-value {
        font-weight: 600;
        color: var(--secondary-color);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px 4px 0 0;
        padding: 10px 16px;
        background-color: #EEF2F6;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-color) !important;
        color: white !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: white;
        color: var(--primary-color);
        border: 1px solid var(--primary-color);
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 500;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: var(--primary-color);
        color: white;
    }
    
    /* Chart container */
    .chart-container {
        background-color: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 24px;
    }
    
    /* Metric styling */
    .metric-card {
        background-color: white;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        text-align: center;
    }
    
    .metric-label {
        font-size: 14px;
        color: #6B7280;
        margin-bottom: 8px;
    }
    
    .metric-number {
        font-size: 24px;
        font-weight: 700;
    }
    
    /* Section styling */
    .section {
        background-color: white;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Responsive fixes */
    @media screen and (max-width: 768px) {
        .header {
            font-size: 1.8rem;
        }
        .stock-card {
            padding: 16px;
        }
        .title {
            font-size: 18px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Define stock categories and sample stocks
stocks = {
    "Sector": {
        "Tech": [
            {"symbol": "INFY", "company": "Infosys Ltd.", "description": "Infosys is a global leader in next-generation digital services and consulting."},
            {"symbol": "TECHM", "company": "Tech Mahindra Ltd.", "description": "Tech Mahindra provides IT services and solutions across industries."}
        ],
        "Finance": [
            {"symbol": "HDFCBANK", "company": "HDFC Bank Ltd.", "description": "HDFC Bank is one of India's premier banking institutions."},
            {"symbol": "IDFCFIRSTB", "company": "IDFC First Bank Ltd.", "description": "IDFC First Bank offers banking and financial services with a focus on retail and business banking."}
        ]
    },
    "Market-cap": {
        "Large-cap": [
            {"symbol": "INFY", "company": "Infosys Ltd.", "description": "Infosys is a global leader in next-generation digital services and consulting."},
            {"symbol": "HDFCBANK", "company": "HDFC Bank Ltd.", "description": "HDFC Bank is one of India's premier banking institutions."}
        ],
        "Mid-cap": [
            {"symbol": "TECHM", "company": "Tech Mahindra Ltd.", "description": "Tech Mahindra provides IT services and solutions across industries."}
        ],
        "Small-cap": [
            {"symbol": "IDFCFIRSTB", "company": "IDFC First Bank Ltd.", "description": "IDFC First Bank offers banking and financial services with a focus on retail and business banking."}
        ]
    }
}

# Load and preprocess data
@st.cache_data
def load_data():
    base_path = r"C:\Users\Srujan KV\Desktop\Srujan Zenshastra\WEEK 7\Indian stockk dashboard"
    
    # Load weekly data
    weekly_data = pd.read_csv(os.path.join(base_path, 'etf_week.csv'))
    weekly_data.columns = weekly_data.columns.str.strip()
    required_columns = ['Date', 'Symbol', 'Close Price']
    if not all(col in weekly_data.columns for col in required_columns):
        st.error(f"Error: Required columns missing in etf_week.csv. Found: {weekly_data.columns.tolist()}")
        raise KeyError("Missing required columns in etf_week.csv")
    weekly_data = weekly_data[required_columns]
    weekly_data['Date'] = pd.to_datetime(weekly_data['Date'])
    weekly_data['Close Price'] = weekly_data['Close Price'].astype(str).str.replace(',', '').astype(float)

    # Load monthly data
    monthly_data = pd.read_csv(os.path.join(base_path, 'etf_month.csv'))
    monthly_data.columns = monthly_data.columns.str.strip()
    if not all(col in monthly_data.columns for col in required_columns):
        st.error(f"Error: Required columns missing in etf_month.csv. Found: {monthly_data.columns.tolist()}")
        raise KeyError("Missing required columns in etf_month.csv")
    monthly_data = monthly_data[required_columns]
    monthly_data['Date'] = pd.to_datetime(monthly_data['Date'])
    monthly_data['Close Price'] = monthly_data['Close Price'].astype(str).str.replace(',', '').astype(float)

    # Load 52-week high-low data
    high_low_data = pd.read_csv(os.path.join(base_path, '52W-high-low.csv'))
    high_low_data.columns = high_low_data.columns.str.strip()
    if 'SYMBOL' not in high_low_data.columns or 'Adjusted 52_Week_High' not in high_low_data.columns or 'Adjusted 52_Week_Low' not in high_low_data.columns:
        st.error(f"Error: Required columns missing in 52W-high-low.csv. Found: {high_low_data.columns.tolist()}")
        raise KeyError("Missing required columns in 52W-high-low.csv")

    # Load P/E data
    pe_data = pd.read_csv(os.path.join(base_path, 'PE.csv'))
    pe_data.columns = pe_data.columns.str.strip()
    if 'SYMBOL' not in pe_data.columns or 'ADJUSTED P/E' not in pe_data.columns:
        st.error(f"Error: Required columns missing in PE.csv. Found: {pe_data.columns.tolist()}")
        raise KeyError("Missing required columns in PE.csv")

    return weekly_data, monthly_data, high_low_data, pe_data

# Load data
try:
    weekly_data, monthly_data, high_low_data, pe_data = load_data()
except FileNotFoundError as e:
    st.error(f"Error: {e}. Please ensure all CSV files are present in the specified directory.")
    st.stop()

# Get stock data function
def get_stock_data(symbol):
    symbol = symbol.strip().upper()  # Normalize symbol
    
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
    
    # Random generation only for yield and market cap
    yield_value = round(random.uniform(1, 5), 2)
    
    if symbol in ["INFY", "HDFCBANK"]:
        market_cap = "₹" + str(round(random.uniform(100000, 500000), 2)) + " Cr"
    elif symbol == "TECHM":
        market_cap = "₹" + str(round(random.uniform(10000, 50000), 2)) + " Cr"
    elif symbol == "IDFCFIRSTB":
        market_cap = "₹" + str(round(random.uniform(1000, 5000), 2)) + " Cr"
    else:
        market_cap = "N/A"
    
    # Calculate some additional metrics
    if not weekly_perf.empty:
        current_price = weekly_perf['Close Price'].iloc[-1] if not weekly_perf.empty else 0
        prev_price = weekly_perf['Close Price'].iloc[0] if not weekly_perf.empty and len(weekly_perf) > 1 else current_price
        weekly_change = ((current_price - prev_price) / prev_price) * 100 if prev_price != 0 else 0
    else:
        current_price = 0
        weekly_change = 0
    
    return {
        'weekly_performance': weekly_perf,
        'monthly_performance': monthly_perf,
        '52_week_high': week_52_high,
        '52_week_low': week_52_low,
        'pe_ratio': pe,
        'yield': yield_value,
        'market_cap': market_cap,
        'current_price': current_price,
        'weekly_change': weekly_change
    }

# Create a visually improved stock card
def create_stock_card(symbol, company, stock_data, key):
    pe_ratio = stock_data['pe_ratio']
    yield_value = stock_data['yield']
    weekly_change = stock_data['weekly_change']
    change_color = "#4CAF50" if weekly_change >= 0 else "#FF5252"
    change_icon = "↑" if weekly_change >= 0 else "↓"
    
    card_html = f"""
    <div class="stock-card">
        <div class="title">{symbol}</div>
        <div class="company">{company}</div>
        <div style="margin-top: 10px; font-size: 18px; font-weight: 600;">
            ₹{stock_data['current_price']:.2f} 
            <span style="color: {change_color}; font-size: 14px; margin-left: 8px;">
                {change_icon} {abs(weekly_change):.2f}%
            </span>
        </div>
        <div class="metrics">
            <div class="metric">P/E: <span class="metric-value">{pe_ratio}</span></div>
            <div class="metric">Yield: <span class="metric-value">{yield_value}%</span></div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    
    button_label = "View Details"
    return st.button(button_label, key=key)

# Function to display detailed stock view
def show_stock_details(symbol, stock_info):
    st.markdown(f"""
    <div class="section">
        <h2 style="color: var(--primary-color); margin-bottom: 8px;">
            {symbol} - {stock_info['company']}
        </h2>
        <p style="color: #6B7280; margin-bottom: 24px;">
            {stock_info['description']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    stock_data = get_stock_data(symbol)
    
    # Show current price and weekly change
    col_price1, col_price2 = st.columns([1, 3])
    with col_price1:
        st.markdown(f"""
        <div style="background-color: white; border-radius: 12px; padding: 20px; text-align: center;">
            <div style="color: #6B7280; font-size: 14px;">Current Price</div>
            <div style="font-size: 26px; font-weight: 700; margin: 10px 0;">
                ₹{stock_data['current_price']:.2f}
            </div>
            <div style="color: {'#4CAF50' if stock_data['weekly_change'] >= 0 else '#FF5252'}; font-weight: 600;">
                {'↑' if stock_data['weekly_change'] >= 0 else '↓'} {abs(stock_data['weekly_change']):.2f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_price2:
        # Quick summary metrics
        cols = st.columns(4)
        metrics = [
            {"label": "P/E Ratio", "value": stock_data['pe_ratio']},
            {"label": "Yield", "value": f"{stock_data['yield']}%"},
            {"label": "52W High", "value": stock_data['52_week_high']},
            {"label": "52W Low", "value": stock_data['52_week_low']}
        ]
        
        for i, metric in enumerate(metrics):
            with cols[i]:
                st.markdown(f"""
                <div style="background-color: white; border-radius: 8px; padding: 10px; text-align: center; height: 100%;">
                    <div style="color: #6B7280; font-size: 12px;">{metric['label']}</div>
                    <div style="font-size: 16px; font-weight: 600; margin-top: 5px;">{metric['value']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Performance charts
    st.markdown("""
    <div class="subheader">Performance Analysis</div>
    """, unsafe_allow_html=True)
    
    perf_tab1, perf_tab2 = st.tabs(["1-Week Performance", "1-Month Performance"])
    
    with perf_tab1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        weekly_perf = stock_data['weekly_performance'].copy()
        if not weekly_perf.empty and not weekly_perf['Close Price'].isna().all():
            fig = px.line(weekly_perf, x='Date', y='Close Price', title=f"{symbol} - 1-Week Performance")
            y_min = min(weekly_perf['Close Price'].dropna())
            y_max = max(weekly_perf['Close Price'].dropna())
            y_min = y_min - (y_min % 50)
            y_max = y_max + (50 - y_max % 50) if y_max % 50 != 0 else y_max
            
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Price (₹)",
                yaxis=dict(range=[y_min, y_max], dtick=50),
                xaxis=dict(tickmode='auto', nticks=5),
                hovermode="x unified",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif"),
                margin=dict(l=0, r=0, t=40, b=0)
            )
            
            fig.update_traces(line=dict(color='#5642FA', width=3))
            
            # Add area under the curve with gradient fill
            fig.update_traces(fill='tozeroy', fillcolor='rgba(86, 66, 250, 0.1)')
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"No weekly performance data available for {symbol}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with perf_tab2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        monthly_perf = stock_data['monthly_performance'].copy()
        if not monthly_perf.empty and not monthly_perf['Close Price'].isna().all():
            fig = px.line(monthly_perf, x='Date', y='Close Price', title=f"{symbol} - 1-Month Performance")
            y_min = min(monthly_perf['Close Price'].dropna())
            y_max = max(monthly_perf['Close Price'].dropna())
            y_min = y_min - (y_min % 50)
            y_max = y_max + (50 - y_max % 50) if y_max % 50 != 0 else y_max
            
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Price (₹)",
                yaxis=dict(range=[y_min, y_max], dtick=50),
                xaxis=dict(tickmode='auto', nticks=5),
                hovermode="x unified",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif"),
                margin=dict(l=0, r=0, t=40, b=0)
            )
            
            fig.update_traces(line=dict(color='#5642FA', width=3))
            
            # Add area under the curve with gradient fill
            fig.update_traces(fill='tozeroy', fillcolor='rgba(86, 66, 250, 0.1)')
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"No monthly performance data available for {symbol}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional Details Section
    st.markdown("""
    <div class="subheader">Financial Overview</div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section">', unsafe_allow_html=True)
    
    # Create more organized financial metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <h4 style="font-size: 18px; margin-bottom: 16px;">Key Metrics</h4>
        """, unsafe_allow_html=True)
        metrics_data = {
            "P/E Ratio": stock_data['pe_ratio'],
            "Yield": f"{stock_data['yield']}%",
            "Market Cap": stock_data['market_cap']
        }
        
        for label, value in metrics_data.items():
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #EEF2F6;">
                <div style="color: #6B7280;">{label}</div>
                <div style="font-weight: 600;">{value}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <h4 style="font-size: 18px; margin-bottom: 16px;">Price Range</h4>
        """, unsafe_allow_html=True)
        
        # Create a visual price range indicator
        high = stock_data['52_week_high']
        low = stock_data['52_week_low']
        current = stock_data['current_price']
        
        if isinstance(high, (int, float)) and isinstance(low, (int, float)) and isinstance(current, (int, float)):
            range_total = high - low
            if range_total > 0:
                position = ((current - low) / range_total) * 100
                position = max(0, min(100, position))  # Ensure position is between 0 and 100
                
                st.markdown(f"""
                <div style="margin-top: 20px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <div style="font-size: 14px;">₹{low}</div>
                        <div style="font-size: 14px;">₹{high}</div>
                    </div>
                    <div style="height: 6px; background-color: #EEF2F6; border-radius: 3px; position: relative;">
                        <div style="position: absolute; left: {position}%; transform: translateX(-50%); width: 12px; height: 12px; background-color: #5642FA; border-radius: 50%; top: -3px;"></div>
                    </div>
                    <div style="text-align: center; margin-top: 16px;">
                        <div style="color: #6B7280; font-size: 14px;">Current</div>
                        <div style="font-weight: 600; font-size: 18px;">₹{current:.2f}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Insufficient data to display price range")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Add a link to go back
    st.markdown("""
    <div style="text-align: center; margin-top: 30px;">
        <a href="#" style="color: #5642FA; text-decoration: none; font-weight: 500;">← Back to Dashboard</a>
    </div>
    """, unsafe_allow_html=True)

# Main app
def main():
    st.markdown("<h1 class='header'>Indian Stock Analysis Dashboard</h1>", unsafe_allow_html=True)
    
    # Improved tabs with custom styling
    tab1, tab2 = st.tabs(["🏢 Sector-wise", "💰 Market-cap wise"])
    
    with tab1:
        st.markdown("<div class='subheader'>Sector-wise Stocks</div>", unsafe_allow_html=True)
        
        for sector, stock_list in stocks["Sector"].items():
            st.markdown(f"<h3 style='margin-top: 20px; margin-bottom: 16px; font-size: 20px;'>{sector}</h3>", unsafe_allow_html=True)
            cols = st.columns(len(stock_list))
            
            for i, stock_info in enumerate(stock_list):
                symbol = stock_info["symbol"]
                company = stock_info["company"]
                stock_data = get_stock_data(symbol)
                
                with cols[i]:
                    if create_stock_card(symbol, company, stock_data, f"btn_{symbol}_{sector}"):
                        show_stock_details(symbol, stock_info)
    
    with tab2:
        st.markdown("<div class='subheader'>Market-cap wise Stocks</div>", unsafe_allow_html=True)
        
        for cap, stock_list in stocks["Market-cap"].items():
            st.markdown(f"<h3 style='margin-top: 20px; margin-bottom: 16px; font-size: 20px;'>{cap}</h3>", unsafe_allow_html=True)
            cols = st.columns(len(stock_list))
            
            for i, stock_info in enumerate(stock_list):
                symbol = stock_info["symbol"]
                company = stock_info["company"]
                stock_data = get_stock_data(symbol)
                
                with cols[i]:
                    if create_stock_card(symbol, company, stock_data, f"btn_cap_{symbol}_{cap}"):
                        show_stock_details(symbol, stock_info)
    
    # Add footer
    st.markdown("""
    <div style="text-align: center; padding: 20px; color: #6B7280; margin-top: 30px; border-top: 1px solid #EEF2F6;">
        <p>Indian Stock Analysis Dashboard © 2025</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()