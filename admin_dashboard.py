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
    
    st.markdown("""
    <div style="padding: 10px 0 15px 0;">
        <div style="font-family: 'Share Tech Mono', monospace; font-size: 13px; color: #ff00ff; letter-spacing: 3px;">
            // PRIVILEGED TELEMETRY // ROOT_CONSOLE //
        </div>
        <h2 style="font-family: 'Orbitron', monospace; font-size: 2.2rem; color: #ffffff; letter-spacing: 2.5px; margin: 4px 0 0 0;">
            ⚙️ SYSTEM TELEMETRY &amp; UPLOAD CONTROLS
        </h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    # Top controls
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.markdown("""
        <div style="font-family: 'Orbitron', monospace; font-size: 1.15rem; color: #00d4ff; letter-spacing: 1px;">
            📊 TELEMETRY OVERVIEW
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("🚪 LOGOUT ROOT", use_container_width=True):
            from auth import logout
            logout()
    
    # System Control Toggle
    st.markdown("""
    <div style="font-family: 'Orbitron', monospace; font-size: 1.15rem; color: #00ff88; letter-spacing: 1px; margin-top: 15px;">
        ⚙️ CLOUD STORAGE PIPELINE (NO MORE UPPY)
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
        <div style="background: rgba(255, 51, 102, 0.08); border-left: 4px solid #ff3366; padding: 12px 16px; margin: 10px 0; font-family: 'Share Tech Mono', monospace; font-size: 13px; color: #ff3366; box-shadow: 0 0 12px rgba(255, 51, 102, 0.2);">
            ⚠️ <strong>NO MORE UPPY PROTOCOL ENGAGED:</strong><br>
            S3 cloud storage pipeline is offline. Resumes can still be analyzed in volatile memory, but persistent uploads to AWS S3 are blocked to conserve budget.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: rgba(0, 255, 136, 0.08); border-left: 4px solid #00ff88; padding: 12px 16px; margin: 10px 0; font-family: 'Share Tech Mono', monospace; font-size: 13px; color: #00ff88; box-shadow: 0 0 12px rgba(0, 255, 136, 0.2);">
            ✅ <strong>S3 UPLOADS ENGAGED:</strong> Resumes are automatically persisted to AWS S3 encrypted bucket.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Time range selector
    st.markdown("""
    <div style="font-family: 'Orbitron', monospace; font-size: 1.15rem; color: #00d4ff; letter-spacing: 1px; margin-bottom: 8px;">
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
    <div style="font-family: 'Orbitron', monospace; font-size: 1.15rem; color: #ffffff; letter-spacing: 1.5px; margin-top: 15px; margin-bottom: 12px;">
        📈 KEY TELEMETRY COEFFICIENTS
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="score-label">Total Ingestions</div>', unsafe_allow_html=True)
        st.metric(
            "",
            stats['total_uploads'],
            delta=f"+{stats['recent_uploads']}" if stats['recent_uploads'] > 0 else None
        )
    
    with col2:
        avg_score = stats['average_score']
        st.markdown('<div class="score-label">Avg Vector Match</div>', unsafe_allow_html=True)
        st.metric(
            "",
            f"{avg_score:.1f}%" if avg_score else "N/A"
        )
    
    with col3:
        total_size_mb = stats['total_size_mb']
        st.markdown('<div class="score-label">Vault Storage</div>', unsafe_allow_html=True)
        st.metric(
            "",
            f"{total_size_mb:.2f} MB"
        )
    
    with col4:
        st.markdown('<div class="score-label">Active Node Users</div>', unsafe_allow_html=True)
        st.metric(
            "",
            stats['unique_users']
        )
    
    st.markdown("---")
    
    # Upload timeline chart
    st.markdown("""
    <div style="font-family: 'Orbitron', monospace; font-size: 1.15rem; color: #00d4ff; letter-spacing: 1px; margin-bottom: 12px;">
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
        
        # Create chart with Cyberpunk theme
        fig, ax = plt.subplots(figsize=(12, 5))
        fig.patch.set_facecolor('#0a0a0f')
        ax.set_facecolor('#0a0a0f')
        
        x_indices = list(range(len(upload_counts)))
        ax.bar(
            x_indices,
            upload_counts.values,
            color="#00ff88",
            edgecolor="#00ff88",
            linewidth=1.2,
            alpha=0.85
        )
        
        tick_labels = [p.strftime(tick_fmt) for p in upload_counts.index]
        ax.set_xticks(x_indices)
        ax.set_xticklabels(
            tick_labels,
            rotation=35 if len(upload_counts) > 6 else 0,
            ha='right' if len(upload_counts) > 6 else 'center',
            color='#00d4ff',
            fontweight='bold',
            fontsize=9
        )
        
        ax.set_xlabel(xlabel, color='#6b7280', fontsize=10)
        ax.set_ylabel('INGESTIONS COUNT', color='#6b7280', fontsize=10)
        ax.tick_params(colors='#6b7280')
        ax.grid(axis='y', alpha=0.25, color='#2a2a3a', linestyle='--')
        
        # Style spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#2a2a3a')
        ax.spines['bottom'].set_color('#2a2a3a')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    else:
        st.info("No uploads recorded in selected telemetry window.")
    
    st.markdown("---")
    
    # Recent uploads table
    st.markdown("### 📋 Recent Uploads")
    
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
        st.markdown("### 🔍 View Individual Resume")
        
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
                **Filename:** {resume['filename']}  
                **Upload Date:** {pd.to_datetime(resume['uploaded_at']).strftime('%Y-%m-%d %H:%M:%S')}  
                **File Size:** {file_sz / 1024:.1f} KB  
                **Match Score:** {score_str} (if analyzed)  
                **User:** {user_str}
                """)
            
            with col2:
                if st.button("🔗 Open S3 URL", use_container_width=True):
                    st.markdown(f"[Open in new tab]({resume['s3_url']})")
                
                if st.button("📥 Download PDF", use_container_width=True):
                    st.markdown(f"[Download]({resume['s3_url']})")
    
    else:
        st.info("No uploads found")


def render_admin_stats_widget():
    """Render a compact admin stats widget for sidebar with Cyberpunk styling"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="font-family: 'Orbitron', monospace; font-size: 13px; color: #00d4ff; letter-spacing: 1.5px; margin-bottom: 8px;">
        // ROOT TELEMETRY MINI-HUD
    </div>
    """, unsafe_allow_html=True)
    
    stats = get_upload_stats(start_time=datetime.now() - timedelta(days=1))
    
    st.sidebar.metric("Today's Ingestions", stats['recent_uploads'])
    st.sidebar.metric("Total Vault Ingestions", stats['total_uploads'])
    
    # Upload status indicator
    settings = get_system_settings()
    if settings.get('uploads_enabled', True):
        st.sidebar.markdown("""
        <div style="font-family: 'Share Tech Mono', monospace; font-size: 12px; color: #00ff88; border: 1px solid #00ff88; padding: 6px 10px; margin-top: 8px; box-shadow: 0 0 8px rgba(0, 255, 136, 0.3);">
            [✓ PIPELINE ACTIVE] S3: ON
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
        <div style="font-family: 'Share Tech Mono', monospace; font-size: 12px; color: #ff3366; border: 1px solid #ff3366; padding: 6px 10px; margin-top: 8px; box-shadow: 0 0 8px rgba(255, 51, 102, 0.3);">
            [🔒 NO MORE UPPY] S3: OFF
        </div>
        """, unsafe_allow_html=True)