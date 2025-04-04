import pandas as pd
import streamlit as st
import plotly.express as px
import os

# Set page configuration
st.set_page_config(
    page_title="Index Details",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Modern CSS
st.markdown("""
<style>
    /* Advanced Color Palette */
    :root {
        --primary: #6b21a8; /* Deep Purple */
        --primary-light: #a855f7;
        --secondary: #d4a017; /* Warm Gold */
        --accent: #14b8a6; /* Teal */
        --background: #f0f4f8; /* Soft Blue-Gray */
        --card: rgba(255, 255, 255, 0.9);
        --text: #1e293b; /* Dark Slate */
        --text-light: #64748b;
        --success: #10b981;
        --danger: #ef4444;
        --warning: #f59e0b;
        --border: rgba(100, 116, 139, 0.2);
        --glass-bg: rgba(255, 255, 255, 0.15);
        --gradient: linear-gradient(135deg, #6b21a8, #d4a017, #14b8a6);
        --glow: 0 0 15px rgba(107, 33, 168, 0.3);
    }

    /* Dark Mode Colors */
    [data-theme="dark"] {
        --primary: #a855f7;
        --primary-light: #d8b4fe;
        --secondary: #facc15;
        --accent: #2dd4bf;
        --background: #111827;
        --card: rgba(30, 41, 59, 0.9);
        --text: #f9fafb;
        --text-light: #9ca3af;
        --border: rgba(148, 163, 184, 0.2);
        --glass-bg: rgba(30, 41, 59, 0.5);
        --gradient: linear-gradient(135deg, #a855f7, #facc15, #2dd4bf);
        --glow: 0 0 15px rgba(168, 85, 247, 0.3);
    }

    /* Base Styles */
    .stApp {
        background: var(--background);
        color: var(--text);
        font-family: 'Poppins', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        transition: all 0.4s ease-in-out;
        backdrop-filter: blur(10px);
    }

    /* Index Card */
    .index-card {
        background: var(--glass-bg);
        border-radius: 15px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        border: 1px solid var(--border);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08), var(--glow);
        backdrop-filter: blur(5px);
        transition: all 0.4s ease;
    }

    .index-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12), 0 0 20px rgba(107, 33, 168, 0.4);
    }

    .index-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: var(--text);
        margin-bottom: 0.6rem;
        background: var(--gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .price-container {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.6rem;
    }

    .current-price {
        font-size: 1.9rem;
        font-weight: 700;
        color: var(--text);
        letter-spacing: -0.02em;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    .price-change {
        font-size: 0.95rem;
        font-weight: 600;
        padding: 0.45rem 0.9rem;
        border-radius: 25px;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    }

    .price-change.positive {
        background: rgba(16, 185, 129, 0.2);
        color: var(--success);
    }

    .price-change.negative {
        background: rgba(239, 68, 68, 0.2);
        color: var(--danger);
    }

    .price-change:hover {
        transform: scale(1.1) rotate(2deg);
    }

    /* Description Card */
    .description-card {
        background: var(--glass-bg);
        border-radius: 15px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        border: 1px solid var(--border);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08), var(--glow);
        backdrop-filter: blur(5px);
    }

    .description-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text);
        margin-bottom: 0.6rem;
        background: var(--gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .description-content {
        font-size: 0.9rem;
        color: var(--text-light);
        line-height: 1.6;
    }

    /* Metrics Grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 0.75rem;
        margin: 1.25rem 0;
    }

    .metric-card {
        background: var(--glass-bg);
        padding: 0.9rem;
        border-radius: 12px;
        border: 1px solid var(--border);
        text-align: center;
        transition: all 0.4s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06), var(--glow);
        backdrop-filter: blur(5px);
    }

    .metric-card:hover {
        background: var(--gradient);
        color: white;
        transform: translateY(-4px) scale(1.05);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12), 0 0 15px rgba(107, 33, 168, 0.5);
    }

    .metric-label {
        font-size: 0.8rem;
        color: var(--text-light);
        margin-bottom: 0.4rem;
        transition: color 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .metric-card:hover .metric-label {
        color: rgba(255, 255, 255, 0.9);
    }

    .metric-value {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--text);
    }

    .metric-card:hover .metric-value {
        color: white;
    }

    /* Chart Container */
    .chart-container {
        background: var(--glass-bg);
        border-radius: 15px;
        padding: 1.25rem;
        margin: 1.25rem 0;
        border: 1px solid var(--border);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08), var(--glow);
        backdrop-filter: blur(5px);
    }

    .chart-title {
        font-size: 1.6rem;
        font-weight: 600;
        color: var(--text);
        margin-bottom: 1rem;
        background: var(--gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Toggle Buttons */
    .toggle-container {
        display: flex;
        gap: 0.6rem;
        margin-bottom: 1rem;
        justify-content: flex-end;
    }

    .stButton>button {
        padding: 0.5rem 1.1rem;
        border-radius: 8px;
        background: var(--gradient);
        color: white;
        border: none;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        transition: all 0.4s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1), var(--glow);
        position: relative;
        overflow: hidden;
    }

    .stButton>button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15), 0 0 20px rgba(107, 33, 168, 0.5);
    }

    .stButton>button::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s ease, height 0.6s ease;
    }

    .stButton>button:hover::after {
        width: 200px;
        height: 200px;
    }

    /* Back Button */
    .stButton>button[key="back_main"] {
        background: var(--secondary);
        color: white;
        padding: 0.5rem 1.1rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.85rem;
        transition: all 0.4s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1), 0 0 15px rgba(212, 160, 23, 0.3);
    }

    .stButton>button[key="back_main"]:hover {
        background: var(--primary-light);
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15), 0 0 20px rgba(168, 85, 247, 0.5);
    }

    /* Responsive Adjustments */
    @media (max-width: 768px) {
        .index-title {
            font-size: 1.5rem;
        }
        .current-price {
            font-size: 1.6rem;
        }
        .price-change {
            font-size: 0.8rem;
            padding: 0.35rem 0.7rem;
        }
        .metrics-grid {
            grid-template-columns: 1fr;
        }
        .chart-title {
            font-size: 1.3rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Define indices data
indices = {
    "NIFTY 50": {"description": "NIFTY 50 is the benchmark index of the National Stock Exchange of India, representing the top 50 companies."},
    "NIFTY 100": {"description": "NIFTY 100 includes the top 100 companies by market capitalization listed on the NSE."},
    "NIFTY BANK": {"description": "NIFTY BANK tracks the performance of the most liquid and large capitalized banking stocks."}
}

# Load data function
@st.cache_data
def load_data():
    try:
        base_path = r"C:\Users\Srujan KV\Desktop\Srujan Zenshastra\WEEK 7\Indian stockk dashboard"
        index_week = pd.read_csv(os.path.join(base_path, 'index_week.csv'))
        index_week.columns = index_week.columns.str.strip()
        index_week['Date'] = pd.to_datetime(index_week['Date'])
        index_week['Close'] = index_week['Close'].astype(str).str.replace(',', '').astype(float)

        index_month = pd.read_csv(os.path.join(base_path, 'index_month.csv'))
        index_month.columns = index_month.columns.str.strip()
        index_month['Date'] = pd.to_datetime(index_month['Date'])
        index_month['Close'] = index_month['Close'].astype(str).str.replace(',', '').astype(float)

        index_data = pd.read_csv(os.path.join(base_path, 'index_data.csv'))
        index_data.columns = [col.strip() for col in index_data.columns]

        return index_week, index_month, index_data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None, None

# Get index data function
def get_index_data(index_name):
    try:
        index_week, index_month, index_data = load_data()
        if any(data is None for data in [index_week, index_month, index_data]):
            return None

        weekly_perf = index_week[index_week['Index Name'].str.strip() == index_name].sort_values('Date')
        monthly_perf = index_month[index_month['Index Name'].str.strip() == index_name].sort_values('Date')
        
        index_row = index_data[index_data['SYMBOL'].str.strip() == index_name].iloc[0]
        ltp = float(str(index_row['LTP']).replace(',', ''))
        change = float(str(index_row['CHNG']).replace(',', ''))
        percent_change = float(str(index_row['%CHNG']).replace(',', ''))
        week_52_high = float(str(index_row['52W H']).replace(',', ''))
        week_52_low = float(str(index_row['52W L']).replace(',', ''))
        value = float(str(index_row['VALUE (₹ Crores)']).replace(',', ''))
        
        return {
            'weekly_performance': weekly_perf,
            'monthly_performance': monthly_perf,
            'ltp': ltp,
            'change': change,
            'percent_change': percent_change,
            '52_week_high': week_52_high,
            '52_week_low': week_52_low,
            'value': value
        }
    except Exception as e:
        st.error(f"Error processing index data: {str(e)}")
        return None

# Function to display index card
def display_index_card(index_name, index_data):
    try:
        ltp_display = f"₹{index_data['ltp']:,.2f}"
        percent_display = f"{'+' if index_data['percent_change'] >= 0 else ''}{index_data['percent_change']:.2f}%"
        change_class = 'positive' if index_data['percent_change'] >= 0 else 'negative'
        change_icon = '▼' if index_data['percent_change'] < 0 else '▲'
    except Exception as e:
        st.error(f"Error preparing index data: {e}")
        return

    html_content = f"""
    <div class="index-card">
        <div class="index-title">{index_name}</div>
        <div class="price-container">
            <div class="current-price">{ltp_display}</div>
            <div class="price-change {change_class}">
                {percent_display} {change_icon} ({index_data['change']:+.2f})
            </div>
        </div>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

def main():
    index_name = st.session_state.get('selected_index', None)
    
    if not index_name:
        st.error("No index selected. Please return to the dashboard and select an index.")
        if st.button("Back to Dashboard", key="back_error"):
            st.switch_page("home.py")
        return
    
    if index_name not in indices:
        st.error(f"Index {index_name} not found in the database.")
        if st.button("Back to Dashboard", key="back_not_found"):
            st.switch_page("home.py")
        return
    
    index_data = get_index_data(index_name)
    if index_data is None:
        st.error("Error loading index data. Please try again.")
        if st.button("Back to Dashboard", key="back_error_data"):
            st.switch_page("home.py")
        return

    display_index_card(index_name, index_data)
    
    st.markdown(f"""
    <div class="description-card">
        <div class="description-title">Index Overview</div>
        <div class="description-content">{indices[index_name]['description']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-label">52-Week High</div>
            <div class="metric-value">₹{index_data['52_week_high']:,.2f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">52-Week Low</div>
            <div class="metric-value">₹{index_data['52_week_low']:,.2f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Value (₹ Cr)</div>
            <div class="metric-value">₹{index_data['value']:,.2f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container"><div class="chart-title">Price History</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
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
        data = index_data['weekly_performance']
        title = "Weekly Performance"
    else:
        data = index_data['monthly_performance']
        title = "Monthly Performance"
    
    if not data.empty and not data['Close'].isna().all():
        fig = px.line(data, x='Date', y='Close',
                     title=f"{index_name} - {title}",
                     template="plotly_white" if not st.session_state.get('dark_mode', False) else "plotly_dark")
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Date",
            yaxis_title="Index Value",
            hovermode='x unified',
            showlegend=False,
            margin=dict(t=50, r=20, b=40, l=60),
            title_font_size=18,
            title_x=0.5,
            font=dict(family="Poppins", size=12),
            xaxis=dict(gridcolor='rgba(100, 116, 139, 0.1)'),
            yaxis=dict(gridcolor='rgba(100, 116, 139, 0.1)')
        )
        
        fig.update_traces(
            line_color='#6b21a8',
            line_width=2.5,
            hovertemplate='₹%{y:,.2f}<extra></extra>',
            mode='lines+markers',
            marker=dict(size=6, color='#6b21a8')
        )
        
        with col1:
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(f"No {title.lower()} data available for {index_name}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("← Back to Dashboard", key="back_main"):
        st.switch_page("home.py")

if __name__ == "__main__":
    main()
