"""
🚴 Bike Store Dashboard - Streamlit Application
================================================

A comprehensive analytics dashboard for Bike Store database
with sales analysis, customer insights, and inventory management.

"""

import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="🚴 Bike Store Dashboard",
    page_icon="🚴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================

st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-row {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 10px;
        border-bottom: 3px solid #1f77b4;
    }
    h2 {
        color: #2ca02c;
        margin-top: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# DATABASE CONNECTION
# ============================================================================

@st.cache_resource
def get_connection():
    """
    Create and cache database connection
    """
    try:

        conn = psycopg2.connect(
            host="postgres",
            database="your_database",
            user="your_user",
            password="your_password"
        )
       
        return conn
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        st.stop()

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data(query, params=None):
    """
    Load data from database with caching
    """
    conn = get_connection()
    try:
        df = pd.read_sql(query, conn, params=params)
        return df
    except Exception as e:
        st.error(f"❌ Query failed: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def get_key_metrics():
    """
    Get key business metrics
    """
    query = """
    SELECT 
        COUNT(DISTINCT o.order_id) as total_orders,
        COUNT(DISTINCT o.customer_id) as total_customers,
        COUNT(DISTINCT p.product_id) as total_products,
        ROUND(SUM(ot.quantity * ot.list_price * (1 - ot.discount))::numeric, 2) as total_revenue
    FROM orders o
    LEFT JOIN order_items ot ON o.order_id = ot.order_id
    LEFT JOIN products p ON ot.product_id = p.product_id
    WHERE o.order_status = 4
    """
    df = load_data(query)
    return df.iloc[0] if not df.empty else {}

@st.cache_data(ttl=300)
def get_sales_by_category():
    """
    Get sales by product category
    """
    query = """
    SELECT 
        c.category_name,
        SUM(ot.quantity) as total_quantity,
        ROUND(SUM(ot.quantity * ot.list_price * (1 - ot.discount))::numeric, 2) as total_sales
    FROM order_items ot
    JOIN products p ON ot.product_id = p.product_id
    JOIN categories c ON p.category_id = c.category_id
    JOIN orders o ON ot.order_id = o.order_id
    WHERE o.order_status = 4
    GROUP BY c.category_name
    ORDER BY total_sales DESC
    """
    return load_data(query)

@st.cache_data(ttl=300)
def get_top_products(limit=10):
    """
    Get top-selling products
    """
    query = f"""
    SELECT 
        p.product_name,
        b.brand_name,
        c.category_name,
        SUM(ot.quantity) as units_sold,
        ROUND(SUM(ot.quantity * ot.list_price * (1 - ot.discount))::numeric, 2) as revenue
    FROM order_items ot
    JOIN products p ON ot.product_id = p.product_id
    JOIN brands b ON p.brand_id = b.brand_id
    JOIN categories c ON p.category_id = c.category_id
    JOIN orders o ON ot.order_id = o.order_id
    WHERE o.order_status = 4
    GROUP BY p.product_name, b.brand_name, c.category_name
    ORDER BY revenue DESC
    LIMIT {limit}
    """
    return load_data(query)

@st.cache_data(ttl=300)
def get_top_customers(limit=10):
    """
    Get top customers by spending
    """
    query = f"""
    SELECT 
        c.customer_id,
        c.first_name || ' ' || c.last_name as customer_name,
        c.email,
        c.city,
        c.state,
        COUNT(DISTINCT o.order_id) as total_orders,
        ROUND(SUM(ot.quantity * ot.list_price * (1 - ot.discount))::numeric, 2) as total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items ot ON o.order_id = ot.order_id
    WHERE o.order_status = 4
    GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.city, c.state
    ORDER BY total_spent DESC
    LIMIT {limit}
    """
    return load_data(query)

@st.cache_data(ttl=300)
def get_sales_by_store():
    """
    Get sales by store
    """
    query = """
    SELECT 
        s.store_name,
        s.city,
        s.state,
        COUNT(DISTINCT o.order_id) as total_orders,
        SUM(ot.quantity) as units_sold,
        ROUND(SUM(ot.quantity * ot.list_price * (1 - ot.discount))::numeric, 2) as revenue
    FROM stores s
    JOIN orders o ON s.store_id = o.store_id
    JOIN order_items ot ON o.order_id = ot.order_id
    WHERE o.order_status = 4
    GROUP BY s.store_name, s.city, s.state
    ORDER BY revenue DESC
    """
    return load_data(query)

@st.cache_data(ttl=300)
def get_sales_trend():
    """
    Get daily sales trend
    """
    query = """
    SELECT 
        o.order_date::DATE as order_date,
        COUNT(DISTINCT o.order_id) as num_orders,
        SUM(ot.quantity) as units_sold,
        ROUND(SUM(ot.quantity * ot.list_price * (1 - ot.discount))::numeric, 2) as daily_revenue
    FROM orders o
    JOIN order_items ot ON o.order_id = ot.order_id
    WHERE o.order_status = 4
    GROUP BY o.order_date::DATE
    ORDER BY o.order_date::DATE
    """
    return load_data(query)

@st.cache_data(ttl=300)
def get_inventory_status():
    """
    Get inventory status by store
    """
    query = """
    SELECT 
        st.store_name,
        p.product_name,
        c.category_name,
        s.quantity,
        CASE 
            WHEN s.quantity = 0 THEN 'Out of Stock'
            WHEN s.quantity < 10 THEN 'Low Stock'
            ELSE 'In Stock'
        END as status
    FROM stocks s
    JOIN stores st ON s.store_id = st.store_id
    JOIN products p ON s.product_id = p.product_id
    JOIN categories c ON p.category_id = c.category_id
    ORDER BY s.quantity ASC, st.store_name
    """
    return load_data(query)

@st.cache_data(ttl=300)
def get_order_status_distribution():
    """
    Get order status distribution
    """
    query = """
    SELECT 
        CASE order_status
            WHEN 1 THEN 'Pending'
            WHEN 2 THEN 'Processing'
            WHEN 3 THEN 'Rejected'
            WHEN 4 THEN 'Completed'
            ELSE 'Unknown'
        END as status_name,
        COUNT(*) as count
    FROM orders
    GROUP BY order_status
    ORDER BY order_status
    """
    return load_data(query)

@st.cache_data(ttl=300)
def get_brand_performance():
    """
    Get brand performance metrics
    """
    query = """
    SELECT 
        b.brand_name,
        COUNT(DISTINCT p.product_id) as num_products,
        SUM(ot.quantity) as units_sold,
        ROUND(AVG(p.list_price)::numeric, 2) as avg_price,
        ROUND(SUM(ot.quantity * ot.list_price * (1 - ot.discount))::numeric, 2) as revenue
    FROM brands b
    JOIN products p ON b.brand_id = p.brand_id
    LEFT JOIN order_items ot ON p.product_id = ot.product_id
    LEFT JOIN orders o ON ot.order_id = o.order_id
    WHERE o.order_status = 4 OR o.order_status IS NULL
    GROUP BY b.brand_name
    ORDER BY revenue DESC
    """
    return load_data(query)

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

st.sidebar.title("🚴 Bike Store")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["📊 Overview", "💰 Sales Analysis", "👥 Customers", "📦 Products", "🏪 Stores", "📈 Trends", "⚙️ Settings"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.info("""
    **About**
    
    This dashboard provides comprehensive analytics
    for Bike Store operations including sales,
    customers, inventory, and trends.
    
    Data is updated every 5 minutes.
""")

# ============================================================================
# PAGE: OVERVIEW
# ============================================================================

if page == "📊 Overview":
    st.title("📊 Bike Store Dashboard - Overview")
    st.markdown("### Key Performance Indicators")
    
    # Load key metrics
    metrics = get_key_metrics()
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💵 Total Revenue",
            value=f"${metrics.get('total_revenue', 0):,.2f}",
            delta="YTD"
        )
    
    with col2:
        st.metric(
            label="📦 Total Orders",
            value=f"{metrics.get('total_orders', 0):,}",
            delta="Completed"
        )
    
    with col3:
        st.metric(
            label="👥 Total Customers",
            value=f"{metrics.get('total_customers', 0):,}",
            delta="Active"
        )
    
    with col4:
        st.metric(
            label="🏷️ Total Products",
            value=f"{metrics.get('total_products', 0):,}",
            delta="In Catalog"
        )
    
    st.markdown("---")
    
    # Row 1: Sales by Category and Top Products
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Sales by Category")
        df_category = get_sales_by_category()
        
        if not df_category.empty:
            fig = px.pie(
                df_category,
                values='total_sales',
                names='category_name',
                title='Revenue Distribution by Category',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No category data available")
    
    with col2:
        st.subheader("🏆 Top 5 Products")
        df_products = get_top_products(5)
        
        if not df_products.empty:
            fig = px.bar(
                df_products,
                x='revenue',
                y='product_name',
                orientation='h',
                title='Top Products by Revenue',
                labels={'revenue': 'Revenue ($)', 'product_name': 'Product'},
                color='revenue',
                color_continuous_scale='Blues'
            )
            fig.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No product data available")
    
    st.markdown("---")
    
    # Row 2: Order Status and Store Performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Order Status Distribution")
        df_status = get_order_status_distribution()
        
        if not df_status.empty:
            fig = px.bar(
                df_status,
                x='status_name',
                y='count',
                title='Orders by Status',
                labels={'count': 'Number of Orders', 'status_name': 'Status'},
                color='status_name',
                color_discrete_map={
                    'Completed': '#2ca02c',
                    'Processing': '#ff7f0e',
                    'Pending': '#1f77b4',
                    'Rejected': '#d62728'
                }
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No order status data available")
    
    with col2:
        st.subheader("🏪 Store Performance")
        df_stores = get_sales_by_store()
        
        if not df_stores.empty:
            fig = px.bar(
                df_stores,
                x='store_name',
                y='revenue',
                title='Revenue by Store',
                labels={'revenue': 'Revenue ($)', 'store_name': 'Store'},
                color='revenue',
                color_continuous_scale='Greens'
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No store data available")

# ============================================================================
# PAGE: SALES ANALYSIS
# ============================================================================

elif page == "💰 Sales Analysis":
    st.title("💰 Sales Analysis")
    
    # Sales trend
    st.subheader("📈 Sales Trend Over Time")
    df_trend = get_sales_trend()
    
    if not df_trend.empty:
        # Create figure with secondary y-axis
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_trend['order_date'],
            y=df_trend['daily_revenue'],
            name='Revenue',
            line=dict(color='#1f77b4', width=2),
            fill='tozeroy'
        ))
        
        fig.update_layout(
            title='Daily Revenue Trend',
            xaxis_title='Date',
            yaxis_title='Revenue ($)',
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_daily = df_trend['daily_revenue'].mean()
            st.metric("Avg Daily Revenue", f"${avg_daily:,.2f}")
        
        with col2:
            max_daily = df_trend['daily_revenue'].max()
            st.metric("Max Daily Revenue", f"${max_daily:,.2f}")
        
        with col3:
            total_orders = df_trend['num_orders'].sum()
            st.metric("Total Orders", f"{total_orders:,}")
        
        with col4:
            avg_order_value = df_trend['daily_revenue'].sum() / df_trend['num_orders'].sum()
            st.metric("Avg Order Value", f"${avg_order_value:,.2f}")
    else:
        st.info("No sales trend data available")
    
    st.markdown("---")
    
    # Sales by category detailed
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Detailed Category Analysis")
        df_category = get_sales_by_category()
        
        if not df_category.empty:
            fig = px.bar(
                df_category,
                x='category_name',
                y=['total_quantity', 'total_sales'],
                title='Category Performance: Units vs Revenue',
                labels={'value': 'Amount', 'category_name': 'Category'},
                barmode='group'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No category data available")
    
    with col2:
        st.subheader("📋 Category Table")
        if not df_category.empty:
            st.dataframe(
                df_category.style.format({
                    'total_quantity': '{:,.0f}',
                    'total_sales': '${:,.2f}'
                }),
                height=400
            )
    
    st.markdown("---")
    
    # Brand performance
    st.subheader("🏷️ Brand Performance Analysis")
    df_brands = get_brand_performance()
    
    if not df_brands.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.scatter(
                df_brands,
                x='units_sold',
                y='revenue',
                size='num_products',
                color='brand_name',
                title='Brand Performance: Units Sold vs Revenue',
                labels={
                    'units_sold': 'Units Sold',
                    'revenue': 'Revenue ($)',
                    'brand_name': 'Brand'
                },
                hover_data=['avg_price']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            top_brands = df_brands.nlargest(10, 'revenue')
            fig = px.bar(
                top_brands,
                x='brand_name',
                y='revenue',
                title='Top 10 Brands by Revenue',
                color='revenue',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(showlegend=False, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        # Brand table
        st.subheader("📊 Brand Details")
        st.dataframe(
            df_brands.style.format({
                'num_products': '{:,.0f}',
                'units_sold': '{:,.0f}',
                'avg_price': '${:,.2f}',
                'revenue': '${:,.2f}'
            }),
            use_container_width=True
        )
    else:
        st.info("No brand data available")

# ============================================================================
# PAGE: CUSTOMERS
# ============================================================================

elif page == "👥 Customers":
    st.title("👥 Customer Analysis")
    
    # Top customers
    st.subheader("🏆 Top Customers by Spending")
    
    limit = st.slider("Number of customers to show", 5, 50, 10)
    df_customers = get_top_customers(limit)
    
    if not df_customers.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.bar(
                df_customers,
                x='customer_name',
                y='total_spent',
                title=f'Top {limit} Customers by Total Spending',
                labels={'total_spent': 'Total Spent ($)', 'customer_name': 'Customer'},
                color='total_spent',
                color_continuous_scale='RdYlGn',
                hover_data=['total_orders', 'city', 'state']
            )
            fig.update_layout(xaxis_tickangle=-45, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.metric(
                "Total Customers",
                f"{len(df_customers):,}"
            )
            st.metric(
                "Avg Spending",
                f"${df_customers['total_spent'].mean():,.2f}"
            )
            st.metric(
                "Total Revenue",
                f"${df_customers['total_spent'].sum():,.2f}"
            )
        
        # Customer details table
        st.subheader("📋 Customer Details")
        st.dataframe(
            df_customers.style.format({
                'total_orders': '{:,.0f}',
                'total_spent': '${:,.2f}'
            }),
            use_container_width=True
        )
        
        # Download button
        csv = df_customers.to_csv(index=False)
        st.download_button(
            label="📥 Download Customer Data (CSV)",
            data=csv,
            file_name=f"top_customers_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No customer data available")
    
    st.markdown("---")
    
    # Customer geographic distribution
    st.subheader("🗺️ Customer Geographic Distribution")
    
    if not df_customers.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # By state
            state_data = df_customers.groupby('state').agg({
                'customer_id': 'count',
                'total_spent': 'sum'
            }).reset_index()
            state_data.columns = ['state', 'num_customers', 'total_revenue']
            
            fig = px.bar(
                state_data,
                x='state',
                y='num_customers',
                title='Customers by State',
                labels={'num_customers': 'Number of Customers', 'state': 'State'},
                color='total_revenue',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # By city
            city_data = df_customers.groupby('city').agg({
                'customer_id': 'count',
                'total_spent': 'sum'
            }).reset_index().nlargest(10, 'customer_id')
            city_data.columns = ['city', 'num_customers', 'total_revenue']
            
            fig = px.bar(
                city_data,
                x='city',
                y='num_customers',
                title='Top 10 Cities by Customer Count',
                labels={'num_customers': 'Number of Customers', 'city': 'City'},
                color='total_revenue',
                color_continuous_scale='Greens'
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE: PRODUCTS
# ============================================================================

elif page == "📦 Products":
    st.title("📦 Product Analysis")
    
    # Top products
    st.subheader("🏆 Top Performing Products")
    
    limit = st.slider("Number of products to show", 5, 50, 10)
    df_products = get_top_products(limit)
    
    if not df_products.empty:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            fig = px.scatter(
                df_products,
                x='units_sold',
                y='revenue',
                size='revenue',
                color='category_name',
                hover_name='product_name',
                title=f'Top {limit} Products: Units Sold vs Revenue',
                labels={
                    'units_sold': 'Units Sold',
                    'revenue': 'Revenue ($)',
                    'category_name': 'Category'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            total_units = df_products['units_sold'].sum()
            total_revenue = df_products['revenue'].sum()
            
            st.metric("Total Units Sold", f"{total_units:,.0f}")
            st.metric("Total Revenue", f"${total_revenue:,.2f}")
            st.metric("Avg Revenue/Product", f"${total_revenue/len(df_products):,.2f}")
        
        # Product table
        st.subheader("📋 Product Details")
        st.dataframe(
            df_products.style.format({
                'units_sold': '{:,.0f}',
                'revenue': '${:,.2f}'
            }),
            use_container_width=True
        )
    else:
        st.info("No product data available")
    
    st.markdown("---")
    
    # Inventory status
    st.subheader("📊 Inventory Status")
    df_inventory = get_inventory_status()
    
    if not df_inventory.empty:
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            selected_store = st.selectbox(
                "Select Store",
                ["All Stores"] + sorted(df_inventory['store_name'].unique().tolist())
            )
        
        with col2:
            selected_status = st.selectbox(
                "Select Status",
                ["All Status", "Out of Stock", "Low Stock", "In Stock"]
            )
        
        # Apply filters
        df_filtered = df_inventory.copy()
        
        if selected_store != "All Stores":
            df_filtered = df_filtered[df_filtered['store_name'] == selected_store]
        
        if selected_status != "All Status":
            df_filtered = df_filtered[df_filtered['status'] == selected_status]
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            out_of_stock = len(df_filtered[df_filtered['status'] == 'Out of Stock'])
            st.metric("⚠️ Out of Stock", out_of_stock)
        
        with col2:
            low_stock = len(df_filtered[df_filtered['status'] == 'Low Stock'])
            st.metric("⚡ Low Stock", low_stock)
        
        with col3:
            in_stock = len(df_filtered[df_filtered['status'] == 'In Stock'])
            st.metric("✅ In Stock", in_stock)
        
        # Inventory chart
        status_counts = df_filtered['status'].value_counts().reset_index()
        status_counts.columns = ['status', 'count']
        
        fig = px.pie(
            status_counts,
            values='count',
            names='status',
            title='Inventory Status Distribution',
            color='status',
            color_discrete_map={
                'Out of Stock': '#d62728',
                'Low Stock': '#ff7f0e',
                'In Stock': '#2ca02c'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Inventory table
        st.subheader("📋 Inventory Details")
        st.dataframe(
            df_filtered.style.apply(
                lambda x: ['background-color: #ffcccc' if v == 'Out of Stock' 
                          else 'background-color: #ffffcc' if v == 'Low Stock'
                          else '' for v in x],
                subset=['status']
            ),
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📥 Download Inventory Data (CSV)",
            data=csv,
            file_name=f"inventory_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No inventory data available")

# ============================================================================
# PAGE: STORES
# ============================================================================

elif page == "🏪 Stores":
    st.title("🏪 Store Performance")
    
    df_stores = get_sales_by_store()
    
    if not df_stores.empty:
        # Store metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Stores", len(df_stores))
        
        with col2:
            st.metric("Total Revenue", f"${df_stores['revenue'].sum():,.2f}")
        
        with col3:
            st.metric("Avg Revenue/Store", f"${df_stores['revenue'].mean():,.2f}")
        
        st.markdown("---")
        
        # Store comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💰 Revenue by Store")
            fig = px.bar(
                df_stores,
                x='store_name',
                y='revenue',
                color='revenue',
                title='Store Revenue Comparison',
                labels={'revenue': 'Revenue ($)', 'store_name': 'Store'},
                color_continuous_scale='Blues'
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📦 Units Sold by Store")
            fig = px.bar(
                df_stores,
                x='store_name',
                y='units_sold',
                color='units_sold',
                title='Units Sold Comparison',
                labels={'units_sold': 'Units Sold', 'store_name': 'Store'},
                color_continuous_scale='Greens'
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # Store details
        st.subheader("📊 Store Performance Details")
        
        # Add calculated columns
        df_stores['avg_order_value'] = df_stores['revenue'] / df_stores['total_orders']
        df_stores['avg_units_per_order'] = df_stores['units_sold'] / df_stores['total_orders']
        
        st.dataframe(
            df_stores.style.format({
                'total_orders': '{:,.0f}',
                'units_sold': '{:,.0f}',
                'revenue': '${:,.2f}',
                'avg_order_value': '${:,.2f}',
                'avg_units_per_order': '{:.1f}'
            }),
            use_container_width=True
        )
        
        # Store location map (if coordinates available)
        st.subheader("🗺️ Store Locations")
        st.info("Store location: " + ", ".join(df_stores.apply(lambda x: f"{x['store_name']} ({x['city']}, {x['state']})", axis=1).tolist()))
    else:
        st.info("No store data available")

# ============================================================================
# PAGE: TRENDS
# ============================================================================

elif page == "📈 Trends":
    st.title("📈 Sales Trends & Forecasting")
    
    df_trend = get_sales_trend()
    
    if not df_trend.empty:
        # Time range selector
        st.subheader("📅 Select Time Range")
        
        min_date = df_trend['order_date'].min()
        max_date = df_trend['order_date'].max()
        
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
        
        with col2:
            end_date = st.date_input("End Date", max_date, min_value=min_date, max_value=max_date)
        
        # Filter data
        mask = (df_trend['order_date'] >= pd.to_datetime(start_date)) & (df_trend['order_date'] <= pd.to_datetime(end_date))
        df_filtered = df_trend[mask].copy()
        
        if not df_filtered.empty:
            # Revenue trend
            st.subheader("💰 Revenue Trend")
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df_filtered['order_date'],
                y=df_filtered['daily_revenue'],
                mode='lines+markers',
                name='Daily Revenue',
                line=dict(color='#1f77b4', width=2),
                fill='tozeroy'
            ))
            
            # Add moving average
            df_filtered['ma_7'] = df_filtered['daily_revenue'].rolling(window=7, min_periods=1).mean()
            
            fig.add_trace(go.Scatter(
                x=df_filtered['order_date'],
                y=df_filtered['ma_7'],
                mode='lines',
                name='7-Day Moving Average',
                line=dict(color='#ff7f0e', width=2, dash='dash')
            ))
            
            fig.update_layout(
                title='Daily Revenue with 7-Day Moving Average',
                xaxis_title='Date',
                yaxis_title='Revenue ($)',
                hovermode='x unified',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Orders trend
            st.subheader("📦 Orders Trend")
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=df_filtered['order_date'],
                y=df_filtered['num_orders'],
                name='Daily Orders',
                marker_color='#2ca02c'
            ))
            
            fig.update_layout(
                title='Daily Order Count',
                xaxis_title='Date',
                yaxis_title='Number of Orders',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_revenue = df_filtered['daily_revenue'].sum()
                st.metric("Total Revenue", f"${total_revenue:,.2f}")
            
            with col2:
                avg_daily_revenue = df_filtered['daily_revenue'].mean()
                st.metric("Avg Daily Revenue", f"${avg_daily_revenue:,.2f}")
            
            with col3:
                total_orders = df_filtered['num_orders'].sum()
                st.metric("Total Orders", f"{total_orders:,}")
            
            with col4:
                avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
                st.metric("Avg Order Value", f"${avg_order_value:,.2f}")
            
            # Growth analysis
            st.markdown("---")
            st.subheader("📊 Growth Analysis")
            
            if len(df_filtered) > 1:
                # Calculate growth metrics
                first_week_revenue = df_filtered.head(7)['daily_revenue'].sum()
                last_week_revenue = df_filtered.tail(7)['daily_revenue'].sum()
                
                if first_week_revenue > 0:
                    growth_rate = ((last_week_revenue - first_week_revenue) / first_week_revenue) * 100
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("First Week Revenue", f"${first_week_revenue:,.2f}")
                    
                    with col2:
                        st.metric("Last Week Revenue", f"${last_week_revenue:,.2f}")
                    
                    with col3:
                        st.metric("Growth Rate", f"{growth_rate:+.1f}%", delta=f"{growth_rate:+.1f}%")
        else:
            st.warning("No data available for selected date range")
    else:
        st.info("No trend data available")

# ============================================================================
# PAGE: SETTINGS
# ============================================================================

elif page == "⚙️ Settings":
    st.title("⚙️ Settings & Configuration")
    
    st.subheader("🔌 Database Connection")
    
    # Show connection info (without password)
    st.info("""
        **Current Connection:**
        - Host: localhost
        - Database: datacamp
        - User: datacamp
        - Status: ✅ Connected
    """)
    
    # Test connection button
    if st.button("🔄 Test Connection"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            cur.close()
            st.success(f"✅ Connection successful!\n\nPostgreSQL version: {version}")
        except Exception as e:
            st.error(f"❌ Connection failed: {e}")
    
    st.markdown("---")
    
    # Cache management
    st.subheader("💾 Cache Management")
    
    st.info("""
        Data is cached for 5 minutes to improve performance.
        Clear cache if you want to see the most recent data.
    """)
    
    if st.button("🗑️ Clear Cache"):
        st.cache_data.clear()
        st.success("✅ Cache cleared successfully!")
        st.rerun()
    
    st.markdown("---")
    
    # Display settings
    st.subheader("🎨 Display Settings")
    
    theme = st.radio("Theme", ["Light", "Dark"], index=0)
    
    if theme == "Dark":
        st.info("Dark theme will be applied in the next version")
    
    st.markdown("---")
    
    # Data export
    st.subheader("📥 Data Export")
    
    st.info("""
        Export options are available on individual pages.
        Navigate to the desired page and use the download buttons.
    """)
    
    st.markdown("---")
    
    # About
    st.subheader("ℹ️ About")
    
    st.markdown("""
        **Bike Store Dashboard v1.0**
        
        Created with:
        - Streamlit
        - PostgreSQL
        - Plotly
        - Pandas
        
        For support or feature requests, please contact your administrator.
        
        © 2025 Bike Store Analytics
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <p>🚴 Bike Store Dashboard | Last updated: {} | Data refreshes every 5 minutes</p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    unsafe_allow_html=True
)
