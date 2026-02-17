"""
Admin Dashboard
Statistics, upload history, and system controls
"""

import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from database import (
    get_all_resumes,
    get_resumes_by_timeframe,
    get_upload_stats,
    get_system_settings,
    update_system_settings
)
import pandas as pd


def render_admin_dashboard():
    """Render the admin dashboard"""
    
    st.markdown("## 👨‍💼 Admin Dashboard")
    st.markdown("---")
    
    # Top controls
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.markdown("### 📊 System Overview")
    
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            from auth import logout
            logout()
    
    # System Control Toggle
    st.markdown("### ⚙️ System Controls")
    
    settings = get_system_settings()
    uploads_enabled = settings.get('uploads_enabled', True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        new_upload_status = st.toggle(
            "🔓 Allow PDF Uploads" if uploads_enabled else "🔒 PDF Uploads Disabled",
            value=uploads_enabled,
            help="Toggle to enable/disable user PDF uploads to S3"
        )
    
    with col2:
        if new_upload_status != uploads_enabled:
            update_system_settings('uploads_enabled', new_upload_status)
            st.success("✅ Updated!")
            st.rerun()
    
    if not new_upload_status:
        st.warning(
            "⚠️ **No More Uppy Mode Active**\n\n"
            "Users cannot upload PDFs to S3. They can still analyze uploaded files, "
            "but new uploads will be blocked to save costs."
        )
    else:
        st.info("✅ Users can upload PDFs to S3 bucket")
    
    st.markdown("---")
    
    # Time range selector
    st.markdown("### 📅 Statistics Period")
    
    time_range = st.selectbox(
        "Select time range",
        ["Last Hour", "Last Day", "Last Week", "Last Month", "Last Year", "All Time"],
        index=2
    )
    
    # Get data based on time range
    if time_range == "Last Hour":
        start_time = datetime.now() - timedelta(hours=1)
    elif time_range == "Last Day":
        start_time = datetime.now() - timedelta(days=1)
    elif time_range == "Last Week":
        start_time = datetime.now() - timedelta(weeks=1)
    elif time_range == "Last Month":
        start_time = datetime.now() - timedelta(days=30)
    elif time_range == "Last Year":
        start_time = datetime.now() - timedelta(days=365)
    else:  # All Time
        start_time = None
    
    # Get statistics
    stats = get_upload_stats(start_time)
    resumes = get_resumes_by_timeframe(start_time)
    
    # Display key metrics
    st.markdown("### 📈 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Uploads",
            stats['total_uploads'],
            delta=f"+{stats['recent_uploads']}" if stats['recent_uploads'] > 0 else None
        )
    
    with col2:
        avg_score = stats['average_score']
        st.metric(
            "Avg Match Score",
            f"{avg_score:.1f}%" if avg_score else "N/A"
        )
    
    with col3:
        total_size_mb = stats['total_size_mb']
        st.metric(
            "Total Storage",
            f"{total_size_mb:.2f} MB"
        )
    
    with col4:
        st.metric(
            "Active Users",
            stats['unique_users']
        )
    
    st.markdown("---")
    
    # Upload timeline chart
    st.markdown("### 📊 Upload Timeline")
    
    if resumes:
        # Create DataFrame
        df = pd.DataFrame([
            {
                'timestamp': r['uploaded_at'],
                'score': r['match_score'] or 0,
                'filename': r['filename']
            }
            for r in resumes
        ])
        
        # Group by hour/day based on time range
        if time_range in ["Last Hour", "Last Day"]:
            df['period'] = pd.to_datetime(df['timestamp']).dt.floor('H')
            xlabel = "Hour"
        elif time_range == "Last Week":
            df['period'] = pd.to_datetime(df['timestamp']).dt.floor('D')
            xlabel = "Day"
        else:
            df['period'] = pd.to_datetime(df['timestamp']).dt.floor('D')
            xlabel = "Date"
        
        upload_counts = df.groupby('period').size()
        
        # Create chart
        fig, ax = plt.subplots(figsize=(12, 5))
        fig.patch.set_facecolor('#1a1a1a')
        ax.set_facecolor('#1a1a1a')
        
        ax.bar(
            range(len(upload_counts)),
            upload_counts.values,
            color='#00D4AA',
            alpha=0.8
        )
        
        ax.set_xlabel(xlabel, color='#a0a0a0', fontsize=11)
        ax.set_ylabel('Uploads', color='#a0a0a0', fontsize=11)
        ax.tick_params(colors='#a0a0a0')
        ax.grid(axis='y', alpha=0.2, color='#404040', linestyle='--')
        
        # Style spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#404040')
        ax.spines['bottom'].set_color('#404040')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    else:
        st.info("No uploads in selected time range")
    
    st.markdown("---")
    
    # Recent uploads table
    st.markdown("### 📋 Recent Uploads")
    
    if resumes:
        # Create table data
        table_data = []
        for r in resumes[:50]:  # Show last 50
            table_data.append({
                'Filename': r['filename'][:30] + '...' if len(r['filename']) > 30 else r['filename'],
                'Score': f"{r['match_score']:.1f}%" if r['match_score'] else "N/A",
                'Size': f"{r['file_size'] / 1024:.1f} KB",
                'Uploaded': pd.to_datetime(r['uploaded_at']).strftime('%Y-%m-%d %H:%M'),
                'User': (r.get('user_email') or 'Anonymous')[:20],
                'URL': r['s3_url']
            })
        
        df_table = pd.DataFrame(table_data)
        
        # Display table
        st.dataframe(
            df_table,
            use_container_width=True,
            hide_index=True
        )
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Export CSV", use_container_width=True):
                csv = df_table.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    csv,
                    "resume_uploads.csv",
                    "text/csv",
                    use_container_width=True
                )
        
        # View/Download individual resumes
        st.markdown("### 🔍 View Individual Resume")
        
        selected_resume = st.selectbox(
            "Select a resume to view",
            options=range(len(resumes)),
            format_func=lambda i: f"{resumes[i]['filename']} - {pd.to_datetime(resumes[i]['uploaded_at']).strftime('%Y-%m-%d %H:%M')}"
        )
        
        if selected_resume is not None:
            resume = resumes[selected_resume]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Filename:** {resume['filename']}  
                **Upload Date:** {pd.to_datetime(resume['uploaded_at']).strftime('%Y-%m-%d %H:%M:%S')}  
                **File Size:** {resume['file_size'] / 1024:.1f} KB  
                **Match Score:** {resume['match_score']:.1f}% (if analyzed)  
                **User:** {resume.get('user_email', 'Anonymous')}
                """)
            
            with col2:
                if st.button("🔗 Open S3 URL", use_container_width=True):
                    st.markdown(f"[Open in new tab]({resume['s3_url']})")
                
                if st.button("📥 Download PDF", use_container_width=True):
                    st.markdown(f"[Download]({resume['s3_url']})")
    
    else:
        st.info("No uploads found")


def render_admin_stats_widget():
    """Render a compact admin stats widget for sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Quick Stats")
    
    stats = get_upload_stats(start_time=datetime.now() - timedelta(days=1))
    
    st.sidebar.metric("Today's Uploads", stats['recent_uploads'])
    st.sidebar.metric("Total Uploads", stats['total_uploads'])
    
    # Upload status indicator
    settings = get_system_settings()
    if settings.get('uploads_enabled', True):
        st.sidebar.success("🔓 Uploads: ON")
    else:
        st.sidebar.error("🔒 Uploads: OFF")