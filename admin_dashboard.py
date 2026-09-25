"""
Admin Dashboard
Bauhaus Design System Implementation
Statistics, upload history, and system controls with constructivist aesthetic
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
    """Render the admin dashboard with Bauhaus constructivist aesthetic"""
    
    st.markdown("""
    <div style="padding: 20px 0 16px 0; border-bottom: 4px solid #121212; margin-bottom: 24px;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
            <div class="circle-shape" style="width: 20px; height: 20px; background: #D02020; border: 2px solid #121212;"></div>
            <div style="width: 18px; height: 18px; background: #1040C0; border: 2px solid #121212;"></div>
            <div style="width: 18px; height: 18px; background: #F0C020; border: 2px solid #121212; transform: rotate(45deg);"></div>
            <span style="font-family: 'Outfit', sans-serif; font-size: 13px; font-weight: 800; color: #121212; letter-spacing: 2.5px; text-transform: uppercase;">
                ROOT TELEMETRY // SYSTEM ADMIN
            </span>
        </div>
        <h1 style="font-size: 3.2rem; color: #121212; letter-spacing: -1px; margin: 0; font-weight: 900; line-height: 1;">
            ADMINISTRATIVE CONSOLE
        </h1>
        <div style="font-family: 'Outfit', sans-serif; font-size: 13px; font-weight: 600; color: #555555; text-transform: uppercase; letter-spacing: 1px; margin-top: 6px;">
            Cloud Ingestion Pipeline, Performance Indices &amp; Resume Archive
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Top controls
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.markdown("""
        <div style="font-family: 'Outfit', sans-serif; font-size: 1.25rem; font-weight: 900; color: #121212; text-transform: uppercase; letter-spacing: 0.5px;">
            ■ TELEMETRY OVERVIEW
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("🚪 LOGOUT ROOT", use_container_width=True):
            from auth import logout
            logout()
    
    # System Control Toggle
    st.markdown("""
    <div style="font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 800; color: #121212; letter-spacing: 0.5px; margin-top: 20px; text-transform: uppercase;">
        ● CLOUD STORAGE INGESTION PIPELINE
    </div>
    """, unsafe_allow_html=True)
    
    settings = get_system_settings()
    uploads_enabled = settings.get('uploads_enabled', True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        new_upload_status = st.toggle(
            "🔓 S3 PDF INGESTION ACTIVE" if uploads_enabled else "🔒 S3 INGESTION BLOCKED [NO MORE UPPY]",
            value=uploads_enabled,
            help="Toggle to enable/disable user PDF uploads to S3 bucket to control cloud cost."
        )
    
    with col2:
        if new_upload_status != uploads_enabled:
            update_system_settings('uploads_enabled', new_upload_status)
            st.success("✅ PROTOCOL UPDATED")
            st.rerun()
    
    if not new_upload_status:
        st.markdown("""
        <div style="background: #F0C020; border: 4px solid #121212; box-shadow: 4px 4px 0px 0px #121212; padding: 14px 18px; margin: 12px 0; font-family: 'Outfit', sans-serif; font-size: 13px; font-weight: 700; color: #121212;">
            ▲ <strong>NO MORE UPPY PROTOCOL ENGAGED:</strong><br>
            S3 cloud storage pipeline is offline. Resumes can still be analyzed in volatile memory, but persistent uploads to AWS S3 are blocked to conserve budget.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #FFFFFF; border: 4px solid #121212; border-left: 12px solid #1040C0; box-shadow: 4px 4px 0px 0px #121212; padding: 14px 18px; margin: 12px 0; font-family: 'Outfit', sans-serif; font-size: 13px; font-weight: 600; color: #121212;">
            ■ <strong>S3 UPLOADS ENGAGED:</strong> Resumes are automatically persisted to AWS S3 encrypted bucket.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Time range selector
    st.markdown("""
    <div style="font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 900; color: #121212; letter-spacing: 0.5px; margin-bottom: 8px; text-transform: uppercase;">
        📅 TELEMETRY WINDOW SELECTION
    </div>
    """, unsafe_allow_html=True)
    
    time_range = st.selectbox(
        "Select time range",
        ["Last Hour", "Last Day", "Last Week", "Last Month", "Last Year", "All Time"],
        index=2,
        label_visibility="collapsed"
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
    st.markdown("""
    <div style="font-family: 'Outfit', sans-serif; font-size: 1.25rem; font-weight: 900; color: #121212; letter-spacing: 0.5px; margin-top: 20px; margin-bottom: 14px; text-transform: uppercase;">
        📈 KEY TELEMETRY INDICES
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: #FFFFFF; border: 4px solid #121212; box-shadow: 4px 4px 0px 0px #121212; padding: 14px 18px;">
            <div class="score-label">Total Uploads</div>
        """, unsafe_allow_html=True)
        st.metric(
            "",
            stats['total_uploads'],
            delta=f"+{stats['recent_uploads']}" if stats['recent_uploads'] > 0 else None
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        avg_score = stats['average_score']
        st.markdown("""
        <div style="background: #FFFFFF; border: 4px solid #121212; box-shadow: 4px 4px 0px 0px #121212; padding: 14px 18px;">
            <div class="score-label">Avg Match Score</div>
        """, unsafe_allow_html=True)
        st.metric(
            "",
            f"{avg_score:.1f}%" if avg_score else "N/A"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        total_size_mb = stats['total_size_mb']
        st.markdown("""
        <div style="background: #FFFFFF; border: 4px solid #121212; box-shadow: 4px 4px 0px 0px #121212; padding: 14px 18px;">
            <div class="score-label">Vault Storage</div>
        """, unsafe_allow_html=True)
        st.metric(
            "",
            f"{total_size_mb:.2f} MB"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: #FFFFFF; border: 4px solid #121212; box-shadow: 4px 4px 0px 0px #121212; padding: 14px 18px;">
            <div class="score-label">Active Users</div>
        """, unsafe_allow_html=True)
        st.metric(
            "",
            stats['unique_users']
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Upload timeline chart
    st.markdown("""
    <div style="font-family: 'Outfit', sans-serif; font-size: 1.25rem; font-weight: 900; color: #121212; letter-spacing: 0.5px; margin-bottom: 12px; text-transform: uppercase;">
        📊 INGESTION VELOCITY TIMELINE
    </div>
    """, unsafe_allow_html=True)
    
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
            df['period'] = pd.to_datetime(df['timestamp']).dt.floor('h')
            xlabel = "TIME CHANNEL (HOURLY)"
            tick_fmt = '%H:%M'
        elif time_range == "Last Week":
            df['period'] = pd.to_datetime(df['timestamp']).dt.floor('d')
            xlabel = "TIME CHANNEL (DAILY)"
            tick_fmt = '%a %d'
        else:
            df['period'] = pd.to_datetime(df['timestamp']).dt.floor('d')
            xlabel = "DATE CHANNEL"
            tick_fmt = '%b %d'
        
        upload_counts = df.groupby('period').size()
        
        # Create chart with Bauhaus theme
        fig, ax = plt.subplots(figsize=(12, 5))
        fig.patch.set_facecolor('#F0F0F0')
        ax.set_facecolor('#FFFFFF')
        
        x_indices = list(range(len(upload_counts)))
        ax.bar(
            x_indices,
            upload_counts.values,
            color="#1040C0",
            edgecolor="#121212",
            linewidth=2,
            alpha=1.0
        )
        
        tick_labels = [p.strftime(tick_fmt) for p in upload_counts.index]
        ax.set_xticks(x_indices)
        ax.set_xticklabels(
            tick_labels,
            rotation=35 if len(upload_counts) > 6 else 0,
            ha='right' if len(upload_counts) > 6 else 'center',
            color='#121212',
            fontweight='heavy',
            fontsize=9.5
        )
        
        ax.set_xlabel(xlabel, color='#121212', fontsize=11, fontweight='heavy')
        ax.set_ylabel('INGESTIONS COUNT', color='#121212', fontsize=11, fontweight='heavy')
        ax.tick_params(colors='#121212', width=2)
        ax.grid(axis='y', alpha=0.18, color='#121212', linestyle='--')
        
        # Style spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#121212')
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['bottom'].set_color('#121212')
        ax.spines['bottom'].set_linewidth(2.5)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    else:
        st.info("No uploads recorded in selected telemetry window.")
    
    st.markdown("---")
    
    # Recent uploads table
    st.markdown("""
    <div style="font-family: 'Outfit', sans-serif; font-size: 1.25rem; font-weight: 900; color: #121212; letter-spacing: 0.5px; margin-bottom: 12px; text-transform: uppercase;">
        📋 RECENT UPLOADS ARCHIVE
    </div>
    """, unsafe_allow_html=True)
    
    if resumes:
        # Create table data
        table_data = []
        for r in resumes[:50]:  # Show last 50
            score_val = r.get('match_score')
            file_sz = r.get('file_size') or 0
            table_data.append({
                'Filename': r['filename'][:30] + '...' if len(r['filename']) > 30 else r['filename'],
                'Score': f"{score_val:.1f}%" if score_val is not None else "N/A",
                'Size': f"{file_sz / 1024:.1f} KB",
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
        st.markdown("""
        <div style="font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 800; color: #121212; letter-spacing: 0.5px; margin-top: 20px; margin-bottom: 8px; text-transform: uppercase;">
            🔍 VIEW ARTIFACT DETAILS
        </div>
        """, unsafe_allow_html=True)
        
        selected_resume = st.selectbox(
            "Select a resume to view",
            options=range(len(resumes)),
            format_func=lambda i: f"{resumes[i]['filename']} - {pd.to_datetime(resumes[i]['uploaded_at']).strftime('%Y-%m-%d %H:%M')}"
        )
        
        if selected_resume is not None:
            resume = resumes[selected_resume]
            file_sz = resume.get('file_size') or 0
            score_val = resume.get('match_score')
            score_str = f"{score_val:.1f}%" if score_val is not None else "N/A"
            user_str = resume.get('user_email') or 'Anonymous'
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div style="background: #FFFFFF; border: 3px solid #121212; box-shadow: 4px 4px 0px 0px #121212; padding: 16px;">
                    <strong>Filename:</strong> {resume['filename']}<br>
                    <strong>Upload Date:</strong> {pd.to_datetime(resume['uploaded_at']).strftime('%Y-%m-%d %H:%M:%S')}<br>
                    <strong>File Size:</strong> {file_sz / 1024:.1f} KB<br>
                    <strong>Match Score:</strong> {score_str}<br>
                    <strong>User:</strong> {user_str}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("🔗 Open S3 URL", use_container_width=True):
                    st.markdown(f"[Open in new tab]({resume['s3_url']})")
                
                if st.button("📥 Download PDF", use_container_width=True):
                    st.markdown(f"[Download]({resume['s3_url']})")
    
    else:
        st.info("No uploads found")


def render_admin_stats_widget():
    """Render a compact admin stats widget for sidebar with Bauhaus styling"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="font-family: 'Outfit', sans-serif; font-size: 13px; font-weight: 900; color: #121212; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px;">
        ROOT TELEMETRY WIDGET
    </div>
    """, unsafe_allow_html=True)
    
    stats = get_upload_stats(start_time=datetime.now() - timedelta(days=1))
    
    st.sidebar.metric("Today's Ingestions", stats['recent_uploads'])
    st.sidebar.metric("Total Ingestions", stats['total_uploads'])
    
    # Upload status indicator
    settings = get_system_settings()
    if settings.get('uploads_enabled', True):
        st.sidebar.markdown("""
        <div style="font-family: 'Outfit', sans-serif; font-size: 12px; font-weight: 800; color: #FFFFFF; background: #1040C0; border: 2px solid #121212; box-shadow: 2px 2px 0px 0px #121212; padding: 6px 10px; margin-top: 8px; text-transform: uppercase;">
            ● PIPELINE ACTIVE // S3: ON
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
        <div style="font-family: 'Outfit', sans-serif; font-size: 12px; font-weight: 800; color: #121212; background: #F0C020; border: 2px solid #121212; box-shadow: 2px 2px 0px 0px #121212; padding: 6px 10px; margin-top: 8px; text-transform: uppercase;">
            ▲ NO MORE UPPY // S3: OFF
        </div>
        """, unsafe_allow_html=True)