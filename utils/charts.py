import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import datetime
from typing import Optional

def plot_category_distribution(df: pd.DataFrame) -> Optional[go.Figure]:
    """Generates a Plotly Donut Chart for medicine category distribution."""
    if df.empty:
        return None
        
    cat_counts = df["Category"].value_counts().reset_index()
    cat_counts.columns = ["Category", "Count"]
    
    fig = px.pie(
        cat_counts, 
        values="Count", 
        names="Category", 
        hole=0.4,
        color_discrete_sequence=["#0d9488", "#0f766e", "#14b8a6", "#2dd4bf", "#5eead4", "#99f6e4", "#ccfbf1", "#115e59", "#134e4a", "#042f2e"],
        title="Medicine Category Distribution"
    )
    
    fig.update_traces(
        textposition='outside',
        textinfo='percent+label',
        domain=dict(x=[0.15, 0.85], y=[0.15, 0.85])
    )
    fig.update_layout(
        margin=dict(t=40, b=0, l=0, r=0),
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Outfit, sans-serif", size=12)
    )
    return fig

def plot_stock_by_category(df: pd.DataFrame) -> Optional[go.Figure]:
    """Generates a Plotly Bar Chart showing stock levels per category."""
    if df.empty:
        return None
        
    stock_df = df.groupby("Category")["Quantity"].sum().reset_index()
    stock_df = stock_df.sort_values(by="Quantity", ascending=True)
    
    fig = px.bar(
        stock_df, 
        x="Quantity", 
        y="Category", 
        orientation="h",
        color="Quantity",
        color_continuous_scale="Teal",
        title="Stock Volume by Category",
        labels={"Quantity": "Total Stock Qty"}
    )
    
    fig.update_layout(
        margin=dict(t=40, b=10, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Outfit, sans-serif", size=12),
        coloraxis_showscale=False
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(200,200,200,0.2)")
    fig.update_yaxes(showgrid=False)
    return fig

def plot_sales_trend(df_sales: pd.DataFrame) -> Optional[go.Figure]:
    """Generates an Area/Line Chart of daily sales trends over the past 30 days."""
    if df_sales.empty:
        return None
        
    # Group by Sale Date
    trend = df_sales.groupby("Sale Date")["Total Amount"].sum().reset_index()
    trend["Sale Date"] = pd.to_datetime(trend["Sale Date"])
    trend = trend.sort_values(by="Sale Date")
    
    fig = px.area(
        trend, 
        x="Sale Date", 
        y="Total Amount",
        color_discrete_sequence=["#0d9488"],
        title="Daily Sales & Revenue Trend",
        labels={"Total Amount": "Revenue (₹)"}
    )
    
    fig.update_traces(
        line=dict(width=3, color='#0d9488'),
        fillcolor='rgba(13, 148, 136, 0.15)'
    )
    
    fig.update_layout(
        margin=dict(t=40, b=10, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Outfit, sans-serif", size=12)
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(200,200,200,0.2)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(200,200,200,0.2)")
    return fig

def plot_top_selling(df_sales: pd.DataFrame) -> Optional[go.Figure]:
    """Generates a vertical bar chart of top selling medicines."""
    if df_sales.empty:
        return None
        
    summary = df_sales.groupby("Medicine Name")["Quantity Sold"].sum().reset_index()
    summary = summary.sort_values(by="Quantity Sold", ascending=False).head(7)
    
    fig = px.bar(
        summary, 
        x="Quantity Sold", 
        y="Medicine Name",
        orientation="h",
        color="Quantity Sold",
        color_continuous_scale="Viridis",
        title="Top Selling Medicines (Units Sold)"
    )
    
    fig.update_layout(
        margin=dict(t=40, b=10, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Outfit, sans-serif", size=12),
        coloraxis_showscale=False
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(200,200,200,0.2)")
    fig.update_yaxes(autorange="reversed")
    return fig

def plot_expiry_status_pie(df_meds: pd.DataFrame) -> Optional[go.Figure]:
    """Plots a beautiful pie chart showing the status of medicine expiry."""
    if df_meds.empty:
        return None
        
    today = datetime.date(2026, 7, 10)
    
    statuses = []
    for idx, row in df_meds.iterrows():
        try:
            exp_date = datetime.datetime.strptime(str(row["Expiry Date"]), "%Y-%m-%d").date()
            if exp_date < today:
                statuses.append("Expired")
            elif (exp_date - today).days <= 30:
                statuses.append("Expiring Soon (<30 Days)")
            else:
                statuses.append("Normal / Safe")
        except Exception:
            statuses.append("Unknown")
            
    status_df = pd.Series(statuses).value_counts().reset_index()
    status_df.columns = ["Status", "Count"]
    
    # Custom color map
    color_map = {
        "Expired": "#ef4444",
        "Expiring Soon (<30 Days)": "#f59e0b",
        "Normal / Safe": "#10b981",
        "Unknown": "#94a3b8"
    }
    
    fig = px.pie(
        status_df, 
        values="Count", 
        names="Status",
        color="Status",
        color_discrete_map=color_map,
        hole=0.4,
        title="Inventory Expiry Status Analysis"
    )
    
    fig.update_traces(
        textposition='outside',
        textinfo='percent+label',
        domain=dict(x=[0.15, 0.85], y=[0.15, 0.85])
    )
    
    fig.update_layout(
        margin=dict(t=40, b=0, l=0, r=0),
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Outfit, sans-serif", size=12)
    )
    return fig

def plot_low_stock_chart(df_meds: pd.DataFrame) -> Optional[go.Figure]:
    """Plots a bar chart highlighting inventory items with low stock level."""
    if df_meds.empty:
        return None
        
    low_stock_df = df_meds[df_meds["Quantity"] < 20].sort_values(by="Quantity")
    if low_stock_df.empty:
        return None
        
    fig = px.bar(
        low_stock_df.head(10), 
        x="Medicine Name", 
        y="Quantity",
        color="Quantity",
        color_continuous_scale="Reds_r",
        title="Critical Stock Status (Top 10 Low Stock Items)",
        labels={"Quantity": "Stock Quantity"}
    )
    
    fig.add_hline(y=20, line_dash="dash", line_color="orange", annotation_text="Low Stock Threshold (20)")
    
    fig.update_layout(
        margin=dict(t=40, b=10, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Outfit, sans-serif", size=12),
        coloraxis_showscale=False
    )
    fig.update_yaxes(showgrid=True, gridcolor="rgba(200,200,200,0.2)")
    return fig
