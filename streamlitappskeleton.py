import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sandvik Proposal App", layout="wide")
st.title("Sandvik Proposal Generator")

# --- memory ---
for key in ["project_data", "proposal_pdf", "vendor_files", "ranking"]:
    if key not in st.session_state:
        st.session_state[key] = None

# --- sidebar ---
with st.sidebar:
    st.header("Settings")
    st.caption("Model and scoring options will go here.")

# --- three jobs ---
tab1, tab2, tab3 = st.tabs(["1. Create Proposal", "2. Upload Vendors", "3. Compare"])

with tab1:
    st.header("Create a proposal")
    with st.form("project_form"):
        name = st.text_input("Project name")
        weeks = st.number_input("Duration (weeks)", min_value=1, value=26)
        budget = st.number_input("Budget (USD)", min_value=0, value=480000, step=10000)
        if st.form_submit_button("Save project"):
            st.session_state.project_data = {
                "project_name": name, "duration_weeks": weeks, "budget_usd": budget,
            }
            st.success("Saved.")
    if st.session_state.project_data:
        st.json(st.session_state.project_data)
        # (Day 5: a "Generate PDF" button that calls Claude goes here)

with tab2:
    st.header("Upload vendor proposals")
    files = st.file_uploader("Vendor PDFs", type=["pdf"], accept_multiple_files=True)
    if files:
        st.session_state.vendor_files = [{"name": f.name, "bytes": f.read()} for f in files]
        st.success(f"{len(files)} file(s) uploaded.")
        for f in st.session_state.vendor_files:
            st.write(f"📄 {f['name']}")

with tab3:
    st.header("Compare & recommend")
    
    # Check prerequisites
    if not st.session_state.project_data:
        st.info("ℹ️ Fill in the project details in Tab 1 first.")
    elif not st.session_state.vendor_files:
        st.info("ℹ️ Upload vendor PDFs in Tab 2 first.")
    else:
        # We have both project data and vendor files — ready to analyze
        if st.button("Analyze & rank vendors"):
            with st.status("Analyzing vendors...", expanded=True) as status:
                st.write("Extracting vendor details from PDFs...")
                
                # Day 12: Replace this with real Claude extraction
                # For now, this is a placeholder
                extracted = []
                for vendor_file in st.session_state.vendor_files:
                    # extracted_dict = call_claude_extract(vendor_file["bytes"])
                    # extracted.append(extracted_dict)
                    extracted.append({
                        "vendor": vendor_file["name"],
                        "price_usd": 500000,  # placeholder
                        "timeline_weeks": 26,  # placeholder
                    })
                
                st.write("Scoring...")
                df = pd.DataFrame(extracted)
                df["score"] = 50.0  # placeholder
                ranked = df.sort_values("score", ascending=False)
                
                status.update(label="Done", state="complete")
            
            st.session_state.ranking = ranked
        
        # Show the ranking if it exists
        if st.session_state.ranking is not None:
            st.subheader("Final ranking")
            st.dataframe(st.session_state.ranking)