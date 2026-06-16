"""
TTB AI Alcohol Label Verification Engine - Presentation Layer Portal
Renders the Streamlit user interface for real-time COLA compliance auditing.
Integrates with centralized configuration controls and system logging sinks.
"""

import os
import sys
from pathlib import Path
import streamlit as st

# Ingest centralized configuration architectures
try:
    from config import AppConfig, logger
except ImportError as e:
    print(f"CRITICAL: Failed to load core configuration context in UI layer. Error: {e}")
    sys.exit(1)

from processor import analyze_label
from main import evaluate_compliance

# Enforce system configuration rules on the presentation view
ALLOWED_TYPES = [ext.replace('.', '') for ext in AppConfig.ALLOWED_EXTENSIONS]

st.set_page_config(
    page_title="TTB Label Verification Portal",
    page_icon="🏛️",
    layout="wide"
)

st.title("🏛️ TTB AI-Powered Alcohol Label Verification")
st.markdown("### COLA Modernization Framework • Human-in-the-Loop Governance Engine")
st.write("Upload a front-facing label asset (PDF or Image) to execute real-time extraction and compliance rule verification.")

# Sidebar Operational Telemetry Matrix
st.sidebar.header("System Status")
st.sidebar.info(f"Runtime Architecture: **CPU Fallback Mode**")
st.sidebar.success(f"Operational Mode: **{AppConfig.ENV.upper()}**")

# File Ingestion Ingress Layer
uploaded_file = st.file_uploader("Choose a label file...", type=ALLOWED_TYPES)

if uploaded_file is not None:
    # Force an explicit, absolute path topology right next to this script
    temp_path = str(Path(__file__).resolve().parent / uploaded_file.name)
    
    # Trace user action in centralized log stream
    logger.info(f"Presentation Layer: Ingestion cycle initiated by client for asset -> '{uploaded_file.name}'")
    
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"Successfully ingested: `{uploaded_file.name}`")
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Asset Processing View")
        if uploaded_file.name.lower().endswith('.pdf'):
            st.warning("📄 PDF Vector Asset Ingested. Displaying processing confirmation below.")
            st.info("The backend `pdf2image` driver is actively extracting Page [0] for computer vision mapping.")
        else:
            st.image(temp_path, caption="Ingested Target Label Layout", use_container_width=True)

    with col2:
        st.subheader("Pipeline Analysis & Compliance Report")
        with st.spinner("Executing Machine Vision Mapping and Governance Rules..."):
            try:
                logger.info(f"Pipeline Ingress: Dispatching '{uploaded_file.name}' to extraction engine.")
                structured_ocr_data = analyze_label(temp_path)
                
                logger.info("Pipeline Processing: Extraction complete. Evaluating business rules context.")
                report = evaluate_compliance(structured_ocr_data)
                status = report["status"]
                
                # Render Audit Boundaries Based on Result Context
                if status == "PASSED":
                    st.success(f"### FINAL AUDIT STATUS: {status}")
                    logger.info(f"Audit Resolution: Asset '{uploaded_file.name}' evaluated as COMPLIANT.")
                elif status == "NEEDS_HUMAN_REVIEW":
                    st.warning(f"### FINAL AUDIT STATUS: {status}")
                    logger.warning(f"Audit Resolution: Asset '{uploaded_file.name}' routed to Human-in-the-Loop exception queue.")
                else:
                    st.error(f"### FINAL AUDIT STATUS: {status}")
                    logger.error(f"Audit Resolution: Asset '{uploaded_file.name}' flagged with non-compliant operational deviations.")

                st.markdown("#### **Extracted Targets Matrix**")
                for field, value in report["extracted_fields"].items():
                    clean_label = field.replace('_', ' ').title()
                    st.markdown(f"**{clean_label}:** `{value if value else 'Not Detected'}`")

                if report["flags"]:
                    st.markdown("#### **Pipeline System Logs**")
                    for flag in report["flags"]:
                        st.markdown(f"⚠️ `{flag}`")

            except Exception as e:
                st.error(f"Execution Error within pipeline: {str(e)}")
                logger.error(f"Pipeline Ingress Error: Failed to execute extraction pipeline on asset '{uploaded_file.name}'. Context: {str(e)}")
            finally:
                # Guaranteed cleanup of transient storage files to prevent caching bloat
                if os.path.exists(temp_path):
                    os.remove(temp_path)