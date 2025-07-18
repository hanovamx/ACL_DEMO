import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import random

# Page configuration
st.set_page_config(
    page_title="ACL Mexico | Business Intelligence Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide sidebar completely
st.markdown("""
<style>
    .stSidebar {
        display: none;
    }
    div[data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Corporate ACL Mexico CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&family=Noto+Sans:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Noto Sans', sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    .corporate-header {
        background: linear-gradient(135deg, #002D72 0%, #0072CE 100%);
        color: white;
        padding: 2rem 3rem;
        border-radius: 0;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 4px 20px rgba(0, 45, 114, 0.3);
    }
    
    .company-logo {
        font-family: 'Montserrat', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .company-tagline {
        font-family: 'Montserrat', sans-serif;
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    .company-info {
        font-family: 'Noto Sans', sans-serif;
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.8);
        margin: 1rem 0 0 0;
        line-height: 1.4;
    }
    
    .filters-container {
        background: white;
        border: 2px solid #0072CE;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(0, 114, 206, 0.1);
    }
    
    .filters-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 1.3rem;
        font-weight: 600;
        color: #002D72;
        margin: 0 0 1rem 0;
        border-bottom: 2px solid #0072CE;
        padding-bottom: 0.5rem;
    }
    
    .section-container {
        background: white;
        border-radius: 16px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 6px 25px rgba(0, 45, 114, 0.08);
        border: 1px solid rgba(0, 114, 206, 0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 2px solid #e2e8f0;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 45, 114, 0.05);
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(0, 45, 114, 0.15);
        border-color: #0072CE;
    }
    
    .metric-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        color: #002D72;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-family: 'Montserrat', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #002D72;
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    
    .metric-unit {
        font-size: 1.3rem;
        color: #0072CE;
        font-weight: 600;
    }
    
    .status-excellent {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-color: #10b981;
    }
    .status-excellent .metric-value { color: #047857; }
    
    .status-good {
        background: linear-gradient(135deg, #fefce8 0%, #fef3c7 100%);
        border-color: #f59e0b;
    }
    .status-good .metric-value { color: #d97706; }
    
    .status-warning {
        background: linear-gradient(135deg, #fff7ed 0%, #fed7aa 100%);
        border-color: #ea580c;
    }
    .status-warning .metric-value { color: #c2410c; }
    
    .status-critical {
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
        border-color: #ef4444;
    }
    .status-critical .metric-value { color: #dc2626; }
    
    .section-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #002D72;
        margin: 0 0 2rem 0;
        padding-bottom: 1rem;
        border-bottom: 4px solid #0072CE;
        position: relative;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -4px;
        left: 0;
        width: 60px;
        height: 4px;
        background: #002D72;
    }
    
    .subsection-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #002D72;
        margin: 2.5rem 0 1.5rem 0;
        display: flex;
        align-items: center;
    }
    
    .subsection-title::before {
        content: '';
        width: 4px;
        height: 24px;
        background: #0072CE;
        margin-right: 1rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: linear-gradient(135deg, #002D72 0%, #0072CE 100%);
        border-radius: 20px;
        padding: 8px;
        border: none;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 65px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 600;
        font-family: 'Montserrat', sans-serif;
        font-size: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #002D72 !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
        border: 1px solid #0072CE !important;
        font-weight: 700;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-1px);
    }
    
    .executive-summary {
        background: linear-gradient(135deg, #002D72 0%, #0072CE 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 8px 30px rgba(0, 45, 114, 0.3);
    }
    
    .executive-summary h3 {
        margin: 0 0 1rem 0;
        font-size: 2rem;
        font-weight: 700;
        font-family: 'Montserrat', sans-serif;
    }
    
    .executive-summary p {
        margin: 0;
        font-size: 1.1rem;
        opacity: 0.9;
        font-family: 'Noto Sans', sans-serif;
    }
    
    .stSelectbox > div > div {
        background: white;
        border: 2px solid #0072CE;
        border-radius: 12px;
        font-family: 'Noto Sans', sans-serif;
        color: #002D72;
        font-weight: 500;
    }
    
    .stSelectbox > div > div:focus {
        border-color: #002D72;
        box-shadow: 0 0 0 3px rgba(0, 114, 206, 0.1);
    }
    
    .stMultiSelect > div > div {
        background: white;
        border: 2px solid #0072CE;
        border-radius: 12px;
        font-family: 'Noto Sans', sans-serif;
    }
    
    .filter-label {
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        color: #002D72;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .kpi-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        font-family: 'Montserrat', sans-serif;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 0.2rem;
    }
    
    .badge-excellent {
        background: #d1fae5;
        color: #047857;
        border: 2px solid #10b981;
    }
    
    .badge-good {
        background: #fef3c7;
        color: #d97706;
        border: 2px solid #f59e0b;
    }
    
    .badge-warning {
        background: #fed7aa;
        color: #c2410c;
        border: 2px solid #ea580c;
    }
    
    .badge-critical {
        background: #fecaca;
        color: #dc2626;
        border: 2px solid #ef4444;
    }
    
    .footer-corporate {
        background: linear-gradient(135deg, #002D72 0%, #0072CE 100%);
        color: white;
        text-align: center;
        padding: 3rem 2rem;
        border-radius: 20px;
        margin: 3rem 0 0 0;
        font-family: 'Noto Sans', sans-serif;
    }
    
    .footer-corporate .company-name {
        font-family: 'Montserrat', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .footer-corporate .company-details {
        opacity: 0.9;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .footer-corporate .website {
        font-weight: 600;
        color: #fbbf24;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_operation_data():
    """Load real operation data from demo Excel"""
    operation_df = pd.read_excel("ACL_KPI_DEMO.xlsx", sheet_name="OPERATION")
    
    # Calculate SLA metrics
    operation_df['Processing_Days'] = (operation_df['Empty In'] - operation_df['CC Date']).dt.days
    operation_df['SLA_Status'] = operation_df['Processing_Days'].apply(
        lambda x: 'On Time' if x <= 2 else 'Late' if x > 2 else 'No Data'
    )
    operation_df['SLA_Category'] = operation_df['Processing_Days'].apply(
        lambda x: 'Excellent' if x <= 1 else 'Good' if x <= 2 else 'Warning' if x <= 5 else 'Critical'
    )
    
    # Add month for filtering
    operation_df['Month'] = operation_df['CC Date'].dt.strftime('%Y-%m')
    operation_df['Week'] = operation_df['CC Date'].dt.strftime('%Y-W%U')
    
    return operation_df

@st.cache_data
def generate_admin_demo_data():
    """Generate realistic admin demo data as described by user"""
    
    # Employee names (Mexican/Spanish names for ACL Mexico)
    employees = [
        'Ana García Herrera', 'Carlos Ruiz López', 'María López Vega', 'José Hernández Silva', 
        'Laura Martín Torres', 'Diego Torres Morales', 'Carmen Silva Jiménez', 'Roberto Vega Castro',
        'Elena Morales Ramírez', 'Juan Castillo Mendoza'
    ]
    
    # Departments for ACL Mexico
    departments = {
        'Ana García Herrera': 'Operaciones', 'Carlos Ruiz López': 'Administración',
        'María López Vega': 'Logística', 'José Hernández Silva': 'Operaciones',
        'Laura Martín Torres': 'Administración', 'Diego Torres Morales': 'Logística',
        'Carmen Silva Jiménez': 'Administración', 'Roberto Vega Castro': 'Operaciones',
        'Elena Morales Ramírez': 'Logística', 'Juan Castillo Mendoza': 'Administración'
    }
    
    # KPIs from the Excel file
    kpis = [
        'Asistencia', 'Puntualidad', 'Comunicación efectiva', 'Cumplimiento de tareas',
        'Feedback con clientes', 'Colaboración entre áreas', 'Entrega de reportes financieros',
        'Conciliación de pagos', 'Actualización de CRM', 'Validación de facturas', 'Soporte a dirección'
    ]
    
    kpi_types = {
        'Asistencia': '%', 'Puntualidad': '%', 'Comunicación efectiva': 'Checkbox',
        'Cumplimiento de tareas': '%', 'Feedback con clientes': 'On time',
        'Colaboración entre áreas': 'Checkbox', 'Entrega de reportes financieros': 'On time',
        'Conciliación de pagos': 'On time', 'Actualización de CRM': 'Checkbox',
        'Validación de facturas': 'On time', 'Soporte a dirección': 'Checkbox'
    }
    
    # Generate weeks
    weeks = [f'2024-W{i:02d}' for i in range(27, 31)]  # Last 4 weeks of current period
    
    data = []
    for employee in employees:
        department = departments[employee]
        for week in weeks:
            for kpi in kpis:
                kpi_type = kpi_types[kpi]
                
                if kpi_type == '%':
                    # Random percentage between 70-100%
                    value = random.randint(70, 100)
                    status = 'Excellent' if value >= 95 else 'Good' if value >= 85 else 'Warning' if value >= 75 else 'Critical'
                elif kpi_type == 'Checkbox':
                    # True/False
                    value = random.choice([True, False])
                    status = 'Excellent' if value else 'Critical'
                elif kpi_type == 'On time':
                    # On time/Late
                    value = random.choice(['On Time', 'Late'])
                    status = 'Excellent' if value == 'On Time' else 'Critical'
                
                data.append({
                    'Employee': employee,
                    'Department': department,
                    'Week': week,
                    'KPI': kpi,
                    'Type': kpi_type,
                    'Value': value,
                    'Status': status
                })
    
    return pd.DataFrame(data)

def create_metric_card(title, value, unit="", status="primary"):
    """Create professional metric card with ACL styling"""
    status_class = f"metric-card status-{status}"
    
    st.markdown(f"""
    <div class="{status_class}">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}<span class="metric-unit">{unit}</span></div>
    </div>
    """, unsafe_allow_html=True)

def apply_filters(df, filters):
    """Apply multiple filters to dataframe"""
    filtered_df = df.copy()
    
    for filter_name, filter_values in filters.items():
        if filter_values and filter_name in filtered_df.columns:
            if isinstance(filter_values, list) and filter_values:
                filtered_df = filtered_df[filtered_df[filter_name].isin(filter_values)]
            elif filter_values != "Todos":
                filtered_df = filtered_df[filtered_df[filter_name] == filter_values]
    
    return filtered_df

def main():
    # Corporate Header
    st.markdown("""
    <div class="corporate-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 class="company-logo">ACL MEXICO</h1>
                <p class="company-tagline">Air Container Logistics Mexico</p>
                <p class="company-info">
                    Oficinas: Apodaca, N.L. & Silao, Gto. • 
                    Forwarding, Almacenamiento & Logística Cross-Border<br> 
                    Filial de Air Container Logistics (Corea del Sur)
                </p>
            </div>
            <div style="text-align: right; font-size: 3rem; opacity: 0.3;">
                🏢
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    operation_df = load_operation_data()
    admin_df = generate_admin_demo_data()
    
    # Advanced Filters Section
    st.markdown("""
    <div class="filters-container">
        <h3 class="filters-title">🔍 Filtros Avanzados de Análisis</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Create filter columns
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
    
    with filter_col1:
        st.markdown('<p class="filter-label">📅 Período</p>', unsafe_allow_html=True)
        period_filter = st.selectbox(
            "Período",
            options=['Todos', 'Última semana', 'Último mes', 'Trimestre actual'],
            label_visibility="collapsed"
        )
        
        st.markdown('<p class="filter-label">👥 Empleado</p>', unsafe_allow_html=True)
        employee_filter = st.multiselect(
            "Empleados",
            options=admin_df['Employee'].unique(),
            label_visibility="collapsed",
            placeholder="Seleccionar empleados..."
        )
    
    with filter_col2:
        st.markdown('<p class="filter-label">🏢 Departamento</p>', unsafe_allow_html=True)
        department_filter = st.multiselect(
            "Departamentos",
            options=admin_df['Department'].unique(),
            label_visibility="collapsed",
            placeholder="Seleccionar departamentos..."
        )
        
        st.markdown('<p class="filter-label">🚚 Transportista</p>', unsafe_allow_html=True)
        trucker_filter = st.multiselect(
            "Transportistas",
            options=operation_df['Trucker'].unique(),
            label_visibility="collapsed",
            placeholder="Seleccionar transportistas..."
        )
    
    with filter_col3:
        st.markdown('<p class="filter-label">📦 Cliente/Consignatario</p>', unsafe_allow_html=True)
        consignee_filter = st.multiselect(
            "Consignatarios",
            options=operation_df['CONSIGNEE'].unique(),
            label_visibility="collapsed",
            placeholder="Seleccionar consignatarios..."
        )
        
        st.markdown('<p class="filter-label">🏭 Shipper</p>', unsafe_allow_html=True)
        shipper_filter = st.multiselect(
            "Shippers",
            options=operation_df['SHIPPER'].unique(),
            label_visibility="collapsed",
            placeholder="Seleccionar shippers..."
        )
    
    with filter_col4:
        st.markdown('<p class="filter-label">📊 Estado SLA</p>', unsafe_allow_html=True)
        sla_filter = st.selectbox(
            "Estado SLA",
            options=['Todos', 'On Time', 'Late'],
            label_visibility="collapsed"
        )
        
        st.markdown('<p class="filter-label">⚠️ Nivel de Riesgo</p>', unsafe_allow_html=True)
        risk_filter = st.selectbox(
            "Nivel de Riesgo",
            options=['Todos', 'Excellent', 'Good', 'Warning', 'Critical'],
            label_visibility="collapsed"
        )
    
    # Apply filters to data
    operation_filters = {}
    if trucker_filter:
        operation_filters['Trucker'] = trucker_filter
    if consignee_filter:
        operation_filters['CONSIGNEE'] = consignee_filter
    if shipper_filter:
        operation_filters['SHIPPER'] = shipper_filter
    if sla_filter != 'Todos':
        operation_filters['SLA_Status'] = sla_filter
    
    admin_filters = {}
    if employee_filter:
        admin_filters['Employee'] = employee_filter
    if department_filter:
        admin_filters['Department'] = department_filter
    
    # Filter data
    filtered_operation_df = apply_filters(operation_df, operation_filters)
    filtered_admin_df = apply_filters(admin_df, admin_filters)
    
    # Executive Summary
    st.markdown("""
    <div class="executive-summary">
        <h3>📊 Dashboard Ejecutivo de Rendimiento</h3>
        <p>Monitoreo integral de operaciones y desempeño administrativo en tiempo real</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_ops = len(filtered_operation_df)
        create_metric_card("Operaciones", total_ops, status="primary")
    
    with col2:
        if len(filtered_operation_df) > 0:
            sla_compliance = len(filtered_operation_df[filtered_operation_df['SLA_Status'] == 'On Time']) / len(filtered_operation_df) * 100
        else:
            sla_compliance = 0
        status = "excellent" if sla_compliance >= 80 else "good" if sla_compliance >= 70 else "warning" if sla_compliance >= 60 else "critical"
        create_metric_card("SLA Compliance", f"{sla_compliance:.1f}", "%", status)
    
    with col3:
        if len(filtered_operation_df) > 0:
            avg_processing = filtered_operation_df['Processing_Days'].mean()
        else:
            avg_processing = 0
        status = "excellent" if avg_processing <= 2 else "good" if avg_processing <= 3 else "warning" if avg_processing <= 5 else "critical"
        create_metric_card("Tiempo Promedio", f"{avg_processing:.1f}", " días", status)
    
    with col4:
        if len(filtered_admin_df) > 0:
            admin_performance = len(filtered_admin_df[filtered_admin_df['Status'].isin(['Excellent', 'Good'])]) / len(filtered_admin_df) * 100
        else:
            admin_performance = 0
        status = "excellent" if admin_performance >= 85 else "good" if admin_performance >= 75 else "warning" if admin_performance >= 65 else "critical"
        create_metric_card("Rendimiento Staff", f"{admin_performance:.1f}", "%", status)
    
    # Tabs for detailed analysis
    tab1, tab2, tab3 = st.tabs([
        "🚚 Análisis Operativo", 
        "👥 Rendimiento del Personal", 
        "📈 Reportes Ejecutivos"
    ])
    
    # TAB 1: Operations Analysis
    with tab1:
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">🚚 Análisis Operativo Detallado</h2>', unsafe_allow_html=True)
        
        if len(filtered_operation_df) == 0:
            st.warning("No hay datos que coincidan con los filtros seleccionados.")
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        # Operational metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            on_time_ops = len(filtered_operation_df[filtered_operation_df['SLA_Status'] == 'On Time'])
            create_metric_card("Operaciones a Tiempo", on_time_ops, status="excellent")
        
        with col2:
            late_ops = len(filtered_operation_df[filtered_operation_df['SLA_Status'] == 'Late'])
            create_metric_card("Operaciones Retrasadas", late_ops, status="critical")
        
        with col3:
            critical_ops = len(filtered_operation_df[filtered_operation_df['Processing_Days'] > 5])
            create_metric_card("Casos Críticos (>5 días)", critical_ops, status="warning")
        
        # SLA Performance Chart
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<h3 class="subsection-title">Estado de Cumplimiento SLA</h3>', unsafe_allow_html=True)
            sla_counts = filtered_operation_df['SLA_Status'].value_counts()
            
            if not sla_counts.empty:
                fig_sla = px.pie(
                    values=sla_counts.values,
                    names=sla_counts.index,
                    color_discrete_map={
                        'On Time': '#10b981',
                        'Late': '#ef4444'
                    },
                    hole=0.5
                )
                fig_sla.update_layout(
                    font=dict(family="Montserrat", size=12),
                    height=400,
                    showlegend=True,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                fig_sla.update_traces(textposition='inside', textinfo='percent+label', textfont_size=14)
                st.plotly_chart(fig_sla, use_container_width=True)
        
        with col2:
            st.markdown('<h3 class="subsection-title">Distribución de Tiempos</h3>', unsafe_allow_html=True)
            
            fig_hist = px.histogram(
                filtered_operation_df,
                x='Processing_Days',
                nbins=12,
                color_discrete_sequence=['#0072CE']
            )
            fig_hist.add_vline(x=2, line_dash="dash", line_color="#ef4444", line_width=3,
                              annotation_text="SLA: 2 días", annotation_position="top right")
            fig_hist.update_layout(
                font=dict(family="Montserrat", size=12),
                height=400,
                xaxis_title="Días de Procesamiento",
                yaxis_title="Número de Operaciones",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        # Trucker Performance Analysis
        st.markdown('<h3 class="subsection-title">Análisis de Rendimiento por Transportista</h3>', unsafe_allow_html=True)
        
        trucker_stats = filtered_operation_df.groupby('Trucker').agg({
            'SLA_Status': lambda x: (x == 'On Time').sum(),
            'Processing_Days': ['count', 'mean']
        }).round(1)
        
        trucker_stats.columns = ['On_Time_Count', 'Total_Operations', 'Avg_Days']
        trucker_stats['Compliance_Rate'] = (trucker_stats['On_Time_Count'] / trucker_stats['Total_Operations'] * 100).round(1)
        trucker_stats = trucker_stats.reset_index()
        
        if not trucker_stats.empty:
            # Trucker performance chart
            fig_trucker = px.bar(
                trucker_stats,
                x='Trucker',
                y='Compliance_Rate',
                color='Compliance_Rate',
                color_continuous_scale=['#ef4444', '#f59e0b', '#10b981'],
                range_color=[0, 100],
                text='Compliance_Rate'
            )
            fig_trucker.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_trucker.update_layout(
                font=dict(family="Montserrat", size=12),
                height=400,
                xaxis_title="Transportista",
                yaxis_title="Tasa de Cumplimiento (%)",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig_trucker, use_container_width=True)
        
        # Detailed operations table
        st.markdown('<h3 class="subsection-title">Registro Detallado de Operaciones</h3>', unsafe_allow_html=True)
        
        # Add status badges to the dataframe for display
        display_df = filtered_operation_df[['SHIPPER', 'CONSIGNEE', 'Trucker', 'CC Date', 'Empty In', 'Processing_Days', 'SLA_Status']].copy()
        display_df['CC Date'] = display_df['CC Date'].dt.strftime('%Y-%m-%d')
        display_df['Empty In'] = display_df['Empty In'].dt.strftime('%Y-%m-%d')
        
        st.dataframe(
            display_df,
            use_container_width=True,
            height=400,
            column_config={
                "SLA_Status": st.column_config.TextColumn(
                    "Estado SLA",
                    help="Estado de cumplimiento del SLA"
                ),
                "Processing_Days": st.column_config.NumberColumn(
                    "Días Procesamiento",
                    help="Días transcurridos entre CC Date y Empty In"
                )
            }
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TAB 2: Administrative Performance
    with tab2:
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">👥 Rendimiento del Personal ACL Mexico</h2>', unsafe_allow_html=True)
        
        if len(filtered_admin_df) == 0:
            st.warning("No hay datos administrativos que coincidan con los filtros seleccionados.")
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        # Week selector
        col1, col2 = st.columns([1, 3])
        with col1:
            available_weeks = filtered_admin_df['Week'].unique()
            selected_week = st.selectbox("📅 Seleccionar Semana", available_weeks)
        
        week_data = filtered_admin_df[filtered_admin_df['Week'] == selected_week]
        
        # Employee performance summary
        employee_summary = week_data.groupby(['Employee', 'Department']).agg({
            'Status': lambda x: (x.isin(['Excellent', 'Good'])).sum() / len(x) * 100
        }).round(1).reset_index()
        employee_summary.columns = ['Employee', 'Department', 'Performance_Score']
        employee_summary = employee_summary.sort_values('Performance_Score', ascending=False)
        
        # Department summary
        dept_summary = week_data.groupby('Department').agg({
            'Status': lambda x: (x.isin(['Excellent', 'Good'])).sum() / len(x) * 100
        }).round(1).reset_index()
        dept_summary.columns = ['Department', 'Performance_Score']
        
        # Top performers
        st.markdown('<h3 class="subsection-title">🏆 Ranking de Rendimiento Semanal</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Performance ranking by employee
            fig_ranking = px.bar(
                employee_summary.head(10),
                x='Performance_Score',
                y='Employee',
                orientation='h',
                color='Department',
                color_discrete_map={
                    'Operaciones': '#0072CE',
                    'Administración': '#002D72',
                    'Logística': '#10b981'
                }
            )
            fig_ranking.update_layout(
                font=dict(family="Montserrat", size=11),
                height=500,
                xaxis_title="Puntuación de Rendimiento (%)",
                yaxis_title="Empleado",
                yaxis={'categoryorder': 'total ascending'},
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(title="Departamento")
            )
            st.plotly_chart(fig_ranking, use_container_width=True)
        
        with col2:
            # Department performance
            fig_dept = px.bar(
                dept_summary,
                x='Department',
                y='Performance_Score',
                color='Performance_Score',
                color_continuous_scale=['#ef4444', '#f59e0b', '#10b981'],
                range_color=[0, 100],
                text='Performance_Score'
            )
            fig_dept.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_dept.update_layout(
                font=dict(family="Montserrat", size=12),
                height=500,
                xaxis_title="Departamento",
                yaxis_title="Rendimiento Promedio (%)",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig_dept, use_container_width=True)
        
        # KPI Performance Matrix
        st.markdown('<h3 class="subsection-title">📊 Matriz de Rendimiento por KPI</h3>', unsafe_allow_html=True)
        
        # Create pivot table for KPI performance
        kpi_matrix = week_data.pivot_table(
            index=['Employee', 'Department'],
            columns='KPI',
            values='Value',
            aggfunc='first'
        ).fillna('N/A')
        
        # Format the data for better display
        formatted_matrix = kpi_matrix.copy()
        for col in formatted_matrix.columns:
            kpi_type = week_data[week_data['KPI'] == col]['Type'].iloc[0] if not week_data[week_data['KPI'] == col].empty else 'Unknown'
            if kpi_type == '%':
                formatted_matrix[col] = formatted_matrix[col].apply(lambda x: f"{x}%" if pd.notna(x) and x != 'N/A' else 'N/A')
            elif kpi_type == 'Checkbox':
                formatted_matrix[col] = formatted_matrix[col].apply(lambda x: "✅" if x is True else "❌" if x is False else 'N/A')
            elif kpi_type == 'On time':
                formatted_matrix[col] = formatted_matrix[col].apply(lambda x: "🟢" if x == 'On Time' else "🔴" if x == 'Late' else 'N/A')
        
        st.dataframe(
            formatted_matrix,
            use_container_width=True,
            height=400
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TAB 3: Executive Reports
    with tab3:
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">📈 Reportes Ejecutivos ACL Mexico</h2>', unsafe_allow_html=True)
        
        # Key Performance Indicators Summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_employees = filtered_admin_df['Employee'].nunique() if len(filtered_admin_df) > 0 else 0
            create_metric_card("Personal Total", total_employees, status="primary")
        
        with col2:
            if len(filtered_admin_df) > 0:
                employee_summary_all = filtered_admin_df.groupby('Employee').agg({
                    'Status': lambda x: (x.isin(['Excellent', 'Good'])).sum() / len(x) * 100
                }).round(1).reset_index()
                excellent_employees = len(employee_summary_all[employee_summary_all['Status'] > 90])
            else:
                excellent_employees = 0
            create_metric_card("Personal Destacado", excellent_employees, status="excellent")
        
        with col3:
            if len(filtered_operation_df) > 0:
                avg_sla_compliance = filtered_operation_df.groupby('Trucker')['SLA_Status'].apply(lambda x: (x == 'On Time').mean() * 100).mean()
            else:
                avg_sla_compliance = 0
            status = "excellent" if avg_sla_compliance >= 80 else "good" if avg_sla_compliance >= 70 else "warning"
            create_metric_card("SLA Global", f"{avg_sla_compliance:.1f}", "%", status)
        
        with col4:
            if len(filtered_operation_df) > 0:
                critical_issues = len(filtered_operation_df[filtered_operation_df['Processing_Days'] > 7])
            else:
                critical_issues = 0
            status = "excellent" if critical_issues == 0 else "warning" if critical_issues < 3 else "critical"
            create_metric_card("Casos Críticos", critical_issues, status=status)
        
        # Company Performance Overview
        st.markdown('<h3 class="subsection-title">🏢 Panorama General ACL Mexico</h3>', unsafe_allow_html=True)
        
        summary_col1, summary_col2 = st.columns(2)
        
        with summary_col1:
            st.markdown(f"""
            **🎯 Indicadores Clave de Rendimiento:**
            - **Cumplimiento SLA operativo**: {sla_compliance:.1f}%
            - **Rendimiento administrativo general**: {admin_performance:.1f}%
            - **Personal con rendimiento excelente**: {excellent_employees}
            - **Operaciones procesadas a tiempo**: {on_time_ops}
            - **Tiempo promedio de procesamiento**: {avg_processing:.1f} días
            """)
        
        with summary_col2:
            if len(filtered_operation_df) > 0:
                best_trucker = trucker_stats.loc[trucker_stats['Compliance_Rate'].idxmax(), 'Trucker'] if not trucker_stats.empty else 'N/A'
                worst_trucker = trucker_stats.loc[trucker_stats['Compliance_Rate'].idxmin(), 'Trucker'] if not trucker_stats.empty else 'N/A'
            else:
                best_trucker = worst_trucker = 'N/A'
                
            st.markdown(f"""
            **⚠️ Áreas de Oportunidad:**
            - **Casos críticos en operaciones**: {critical_ops}
            - **Transportista más eficiente**: {best_trucker}
            - **Transportista que requiere apoyo**: {worst_trucker}
            - **Personal que requiere atención**: {len(employee_summary_all[employee_summary_all['Status'] < 70]) if len(filtered_admin_df) > 0 else 0}
            """)
        
        # Filter Summary
        st.markdown('<h3 class="subsection-title">🔍 Resumen de Filtros Aplicados</h3>', unsafe_allow_html=True)
        
        filter_summary = []
        if employee_filter:
            filter_summary.append(f"**Empleados**: {', '.join(employee_filter[:3])}{'...' if len(employee_filter) > 3 else ''}")
        if department_filter:
            filter_summary.append(f"**Departamentos**: {', '.join(department_filter)}")
        if trucker_filter:
            filter_summary.append(f"**Transportistas**: {', '.join(trucker_filter)}")
        if consignee_filter:
            filter_summary.append(f"**Consignatarios**: {', '.join(consignee_filter[:2])}{'...' if len(consignee_filter) > 2 else ''}")
        if sla_filter != 'Todos':
            filter_summary.append(f"**Estado SLA**: {sla_filter}")
        
        if filter_summary:
            st.markdown("**Filtros activos:**")
            for filter_item in filter_summary:
                st.markdown(f"- {filter_item}")
        else:
            st.info("No hay filtros aplicados. Mostrando todos los datos disponibles.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Corporate Footer
    st.markdown("""
    <div class="footer-corporate">
        <div class="company-name">ACL MEXICO</div>
        <div class="company-details">
            <strong>Air Container Logistics Mexico</strong><br>
            Apodaca, Nuevo León • Silao, Guanajuato<br>
            Forwarding • Almacenamiento • Logística Cross-Border<br>
            Filial de Air Container Logistics (Corea del Sur)<br>
            <span class="website">www.aclcargo.com</span>
        </div>
        <div style="font-size: 0.9rem; opacity: 0.8;">
            Dashboard de Business Intelligence • Datos en tiempo real • Confidencial
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
