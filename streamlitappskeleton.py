import streamlit as st
from anthropic import AnthropicFoundry
from fpdf import FPDF

# ============================================================
# PAGE SETUP
# ============================================================
st.set_page_config(page_title="Sandvik Proposal App", layout="wide")
st.title("Sandvik Proposal Generator")

# ============================================================
# INITIALIZE SESSION STATE
# ============================================================
for key in ["project_data", "proposal_text", "proposal_pdf", "vendor_files", "ranking"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ============================================================
# HELPER: convert text to PDF bytes
# ============================================================
def proposal_to_pdf_bytes(project_name: str, body_text: str) -> bytes:
    safe_title = project_name.encode("latin-1", errors="replace").decode("latin-1")
    safe_body = body_text.encode("latin-1", errors="replace").decode("latin-1")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(25, 25, 25)

    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "Sandvik Project Proposal", align="C")
    pdf.ln(14)

    # Project name
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, safe_title, align="C")
    pdf.ln(12)

    # Body
    pdf.set_font("Helvetica", "", 11)
    for line in safe_body.split("\n"):
        stripped = line.strip()
        if stripped == "":
            pdf.ln(3)
        else:
            words = stripped.split(" ")
            safe_words = [w[:80] for w in words]
            safe_line = " ".join(safe_words)
            try:
                pdf.multi_cell(0, 6, safe_line)
            except Exception:
                pass

    out = pdf.output()
    return bytes(out) if not isinstance(out, bytes) else out

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.header("Settings")
    st.caption("Model: Claude Sonnet 4.6 (via Azure Foundry)")

# ============================================================
# THREE TABS
# ============================================================
tab1, tab2, tab3 = st.tabs(["1. Create Proposal", "2. Upload Vendors", "3. Compare"])

# ============================================================
# TAB 1: CREATE PROPOSAL
# ============================================================
with tab1:
    st.header("Create a proposal")

    with st.form("project_form"):
        name = st.text_input("Project name")
        weeks = st.number_input("Duration (weeks)", min_value=1, value=26)
        budget = st.number_input("Budget (USD)", min_value=0, value=480000, step=10000)
        start = st.text_area("Starting state", height=80)
        end = st.text_area("End state", height=80)
        submitted = st.form_submit_button("Save project")

    if submitted and name:
        st.session_state.project_data = {
            "project_name": name,
            "duration_weeks": weeks,
            "budget_usd": budget,
            "start_state": start,
            "end_state": end,
        }
        st.session_state.proposal_text = None
        st.session_state.proposal_pdf = None
        st.success("Project saved!")

    if st.session_state.project_data:
        st.json(st.session_state.project_data)

        if st.button("Generate Proposal"):
            with st.spinner("Claude is writing your proposal..."):
                base_url = st.secrets["AZURE_FOUNDRY_BASE_URL"]
                api_key = st.secrets["AZURE_FOUNDRY_API_KEY"]
                deployment = st.secrets["AZURE_FOUNDRY_DEPLOYMENT"]

                client = AnthropicFoundry(api_key=api_key, base_url=base_url)
                p = st.session_state.project_data

                prompt = f"""
Generate a professional Sandvik project proposal based on this information.
Use plain text only. No markdown, no bullet points with special characters,
no em-dashes, no smart quotes. Use regular hyphens and straight quotes only.

Project Name: {p['project_name']}
Duration: {p['duration_weeks']} weeks
Budget: ${p['budget_usd']:,}
Starting State: {p['start_state']}
End State: {p['end_state']}

Write a formal proposal with these sections:
1. Executive Summary
2. Project Scope
3. Timeline and Milestones
4. Budget Breakdown
5. Risk Assessment
6. Team and Resources

Make it professional and ready to send to stakeholders.End the proposal with a professional closing statement on its own line.
"""

                message = client.messages.create(
                    model=deployment,
                    max_tokens=4000,
                    messages=[{"role": "user", "content": prompt}]
                )

                # Save the text
                st.session_state.proposal_text = message.content[0].text

                # Convert to PDF and save bytes
                st.session_state.proposal_pdf = proposal_to_pdf_bytes(
                    p["project_name"],
                    st.session_state.proposal_text,
                )

            st.success("Proposal generated!")

        # Show proposal text
        if st.session_state.proposal_text:
            st.subheader("Your proposal")
            st.write(st.session_state.proposal_text)

        # Show download button
        if st.session_state.proposal_pdf:
            st.download_button(
                label="⬇️ Download proposal as PDF",
                data=st.session_state.proposal_pdf,
                file_name="sandvik_proposal.pdf",
                mime="application/pdf",
            )
        else:
            # DEBUG: tell us why the button isn't showing
            if st.session_state.proposal_text:
                st.warning("PDF generation failed silently. Check the error above.")

# ============================================================
# TAB 2: UPLOAD VENDORS
# ============================================================
with tab2:
    st.header("Upload vendor proposals")
    files = st.file_uploader("Vendor PDFs", type=["pdf"], accept_multiple_files=True)
    if files:
        st.session_state.vendor_files = [
            {"name": f.name, "bytes": f.read()} for f in files
        ]
        st.success(f"{len(files)} file(s) uploaded.")
        for f in st.session_state.vendor_files:
            st.write(f"📄 {f['name']}")

# ============================================================
# TAB 3: COMPARE
# ============================================================
with tab3:
    st.header("Compare & recommend")
    st.info("This tab will compare vendors once we wire up extraction (Day 12).")
