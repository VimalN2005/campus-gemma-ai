"""CampusGemma AI: The Zero-Cost Student Side-Hustle & Technical Coaching Studio.

Built for Hacktoberfest 2026 Week 2 ('Side Hustle') using Google Gemma 2 Open Weights
and OpenTelemetry GenAI Observability.
"""

import streamlit as st
from core.engine import CampusGemmaEngine
from core.telemetry import get_recent_spans, init_telemetry

init_telemetry()

st.set_page_config(
    page_title="CampusGemma AI | Side Hustle Studio",
    page_icon="💼",
    layout="wide",
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F3F4F6;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
        border-left: 4px solid #3B82F6;
    }
    .profit-badge {
        background-color: #ECFDF5;
        color: #065F46;
        padding: 10px 14px;
        border-radius: 8px;
        border-left: 4px solid #10B981;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=500&auto=format&fit=crop&q=60", caption="IIIT Bhopal Student Side-Hustle Hub")
    st.title("⚙️ Gemma 2 Settings")
    api_key = st.text_input("Groq API Key (Optional)", type="password", help="Leave blank to run in zero-config offline mode")
    mode = st.radio("Inference Provider", ["Groq Cloud (gemma2-9b-it)", "Local Ollama (localhost:11434)", "Built-in Offline Demo"])

    use_ollama = "Ollama" in mode
    engine = CampusGemmaEngine(api_key=api_key, use_local_ollama=use_ollama)

    st.markdown("---")
    st.markdown("### 🏆 Hacktoberfest Week 2")
    st.markdown("- **Theme:** Side Hustle 💼")
    st.markdown("- **Featured Track:** Best Use of Gemma")
    st.markdown("- **Observability:** OpenTelemetry GenAI")
    st.markdown("- **Builder:** Vimal Sahani (IIIT Bhopal)")

st.markdown('<div class="main-header">💼 CampusGemma AI: Student Side-Hustle Studio</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Turn messy client messages into high-converting freelance proposals, scope-of-work contracts, and paid technical coaching — with $0.00 API overhead via Google Gemma 2.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="profit-badge">💡 <strong>Why Open Weights Make This Side-Hustle Profitable:</strong> Running Google Gemma 2 locally or on open endpoints keeps client NDA briefs 100% private on your laptop and eliminates $20+/month proprietary API subscriptions—meaning 100% of every student freelance gig stays in your pocket.</div>',
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💼 Freelance SOW & Contract Shield",
    "💳 Milestone Invoice & Payment Studio",
    "🎯 Paid Mock-Interview Coaching",
    "🔬 Client Code & Security Auditor",
    "📊 OpenTelemetry & Unit Economics",
])

# ----------------- TAB 1: FREELANCE PROPOSAL & SOW GENERATOR -----------------
with tab1:
    st.subheader("Turn Messy WhatsApp / Upwork Client Briefs into Ready-to-Sign Proposals")
    col1, col2 = st.columns([3, 1])
    with col1:
        preset_choice = st.selectbox(
            "Quick Demo Presets:",
            [
                "Custom Client Brief",
                "Preset: Local Bakery & Cafe Online Ordering Backend",
                "Preset: Freelance React & Tailwind Portfolio Website",
                "Preset: Student Club Event Ticketing & QR Portal",
            ]
        )
        if preset_choice == "Preset: Local Bakery & Cafe Online Ordering Backend":
            default_brief = (
                "Hi! I run a local bakery and book cafe in Bhopal. Right now we take custom cake orders over WhatsApp "
                "and track everything in a messy Excel sheet. Half the time we miss delivery slots or forget advance payments. "
                "Can you build us a fast order booking backend with invoice PDFs and an admin dashboard?"
            )
        elif preset_choice == "Preset: Freelance React & Tailwind Portfolio Website":
            default_brief = (
                "Hey Vimal, I need a high-converting personal portfolio website for my consulting business. "
                "Need 4 pages: Home, Case Studies, Services, Contact with email integration. "
                "Must be fully responsive, dark mode, under 1s load time, and deployed on Vercel."
            )
        elif preset_choice == "Preset: Student Club Event Ticketing & QR Portal":
            default_brief = (
                "Our college coding society is organizing an inter-college hackathon with 500+ participants. "
                "We need a registration portal that accepts UPI payments, verifies transactions, "
                "and automatically generates unique QR entry passes sent to students' emails."
            )
        else:
            default_brief = ""

        client_brief = st.text_area("Paste Raw Client Requirement / Message:", value=default_brief, height=130, placeholder="Paste your client's email, Upwork job, or WhatsApp brief here...")
    with col2:
        hourly_rate = st.number_input("Your Hourly Rate ($ USD)", min_value=10.0, max_value=150.0, value=25.0, step=5.0)
        st.caption("Automatically calculates milestone quotes & anti-scope-creep clauses.")

    if st.button("⚡ Generate Statement of Work (SOW) & Pricing Quote", use_container_width=True):
        if not client_brief.strip():
            st.warning("Please paste a client requirement or pick a preset above.")
        else:
            with st.spinner("Google Gemma 2 structuring SOW, milestones, and recording OpenTelemetry trace..."):
                st.session_state["proposal"] = engine.generate_freelance_proposal(
                    client_brief=client_brief, hourly_rate_usd=hourly_rate
                )

    if "proposal" in st.session_state:
        prop = st.session_state["proposal"]
        st.success(f"💰 **Estimated Project Quote:** {prop.get('total_estimated_cost')}")
        st.markdown(f"### 📋 Executive Pitch\n{prop.get('executive_summary')}")

        st.markdown("### 🗓️ Engineering Milestones & Deliverable Schedule")
        for m in prop.get("milestones", []):
            st.markdown(f"- ✅ {m}")

        col_a, col_b = st.columns(2)
        with col_a:
            st.info(f"**🛡️ Anti-Scope-Creep Clause:**\n\n{prop.get('scope_boundaries')}")
        with col_b:
            st.warning(f"**🏗️ Recommended Tech Stack:**\n\n{prop.get('tech_stack_recommendation')}")

        # Exportable SOW Document
        milestones_formatted = "\n".join([f"- {m}" for m in prop.get("milestones", [])])
        sow_document = f"""# 📄 STATEMENT OF WORK (SOW) & FREELANCE CONTRACT

**Project:** Custom Engineering & Software Development
**Prepared By:** Campus Freelance Engineer
**Target Hourly Rate:** ${hourly_rate}/hr
**Total Estimated Investment:** {prop.get('total_estimated_cost')}

---

## 1. Executive Summary
{prop.get('executive_summary')}

## 2. Engineering Milestones & Deliverables
{milestones_formatted}

## 3. Recommended Architecture
{prop.get('tech_stack_recommendation')}

## 4. Scope-Creep Protection & Legal Boundaries
{prop.get('scope_boundaries')}

---

### Acceptance & Authorization
By signing below, the client agrees to the milestones, payment terms, and scope boundaries outlined above:

**Client Signature:** ___________________________  **Date:** _______________  
**Developer Signature:** ________________________  **Date:** _______________  
"""
        st.download_button(
            label="📥 Download Formal SOW Agreement (.md)",
            data=sow_document,
            file_name="CampusGemma_Freelance_SOW.md",
            mime="text/markdown",
            use_container_width=True
        )

# ----------------- TAB 2: MILESTONE INVOICE & PAYMENT STUDIO -----------------
with tab2:
    st.subheader("Generate Professional Client Invoices & Payment Requests in Seconds")
    st.caption("Protect your cash flow: convert completed engineering milestones into itemized commercial invoices with direct settlement instructions.")

    inv_c1, inv_c2 = st.columns(2)
    with inv_c1:
        client_name = st.text_input("Client / Business Name:", value="Aman Verma (FinEdge Labs)")
        project_title = st.text_input("Project Engagement:", value="E-Commerce Ordering Portal & FastAPI Backend")
    with inv_c2:
        milestone_billed = st.selectbox(
            "Milestone to Bill:",
            [
                "Milestone 1: Database Schema & Authentication API Delivery",
                "Milestone 2: Real-time Order Webhook & Invoice Engine",
                "Milestone 3: Final Security Review, Pytest Suite & Cloud Deployment",
                "Milestone 4: Post-Launch Support & Performance Tuning",
            ]
        )
        col_amt, col_upi = st.columns(2)
        with col_amt:
            milestone_amount = st.number_input("Milestone Amount ($ USD):", min_value=10.0, max_value=2000.0, value=120.0, step=10.0)
        with col_upi:
            payment_handle = st.text_input("Your UPI / PayPal Handle:", value="vimalsahani@upi")

    if st.button("💳 Generate Itemized Commercial Invoice", use_container_width=True):
        with st.spinner("Google Gemma 2 generating itemized invoice & recording OpenTelemetry trace..."):
            st.session_state["invoice"] = engine.generate_client_invoice(
                client_name=client_name,
                project_title=project_title,
                milestone_name=milestone_billed,
                amount_usd=milestone_amount,
                payment_id=payment_handle
            )

    if "invoice" in st.session_state:
        inv = st.session_state["invoice"]
        st.success(f"🧾 **Invoice {inv.get('invoice_number')} Generated Successfully!**")

        st.markdown(f"### 📋 Invoice Summary")
        m1, m2, m3 = st.columns(3)
        m1.metric("Invoice #", inv.get("invoice_number", "INV-2026-101"))
        m2.metric("Due Date", inv.get("due_date", "Net 7 Days"))
        m3.metric("Total Payable", inv.get("total_amount_usd", f"${milestone_amount:.2f} USD"))

        st.markdown(f"**Billed To:** `{inv.get('client_name')}` | **Project:** `{inv.get('project_title')}`")
        st.markdown(f"**Milestone Scope:** `{inv.get('milestone_name')}`")

        st.markdown("#### 📦 Itemized Deliverables:")
        for item in inv.get("line_items", []):
            st.markdown(f"- 💵 {item}")

        st.info(f"**🏦 Payment Instructions:** {inv.get('payment_instructions')}")
        st.caption(f"**Legal Terms:** {inv.get('payment_terms')}")

        line_items_formatted = "\n".join([f"- {it}" for it in inv.get("line_items", [])])
        invoice_doc = f"""# 🧾 COMMERCIAL FREELANCE INVOICE

**Invoice Number:** {inv.get('invoice_number')}
**Date of Issue:** {inv.get('issue_date')}
**Payment Terms:** {inv.get('due_date')}

---

### BILL TO:
**Client:** {inv.get('client_name')}
**Project:** {inv.get('project_title')}
**Scope Billed:** {inv.get('milestone_name')}

---

### ITEMIZED DELIVERABLES & CHARGES:
{line_items_formatted}

---

### TOTAL PAYABLE: **{inv.get('total_amount_usd')}**

### PAYMENT METHOD:
{inv.get('payment_instructions')}

### TERMS & CONDITIONS:
{inv.get('payment_terms')}

---
*Generated by CampusGemma AI — Zero-Cost Open-Source Freelance Studio.*
"""
        st.download_button(
            label="📥 Download Commercial Invoice (.md)",
            data=invoice_doc,
            file_name=f"{inv.get('invoice_number', 'Invoice')}.md",
            mime="text/markdown",
            use_container_width=True
        )

# ----------------- TAB 3: PAID MOCK INTERVIEW COACHING -----------------
with tab3:
    st.subheader("Campus Placement Coaching Side-Hustle Studio")
    st.caption("Host structured 1-on-1 mock technical interviews for juniors and generate instant grading rubrics.")
    col1, col2 = st.columns([2, 1])
    with col1:
        topic = st.selectbox("Interview Domain", [
            "Distributed Systems (Consensus, Raft, CAP Theorem)",
            "Operating Systems & Concurrency (Mutex, Deadlocks, Virtual Memory)",
            "Database Internals (B+ Trees, WAL, Isolation Levels)",
            "High-Throughput Networking (TCP/IP, Epoll, Socket Multiplexing)",
            "Advanced Data Structures (Segment Trees, Disjoint Set Union)",
        ])
    with col2:
        difficulty = st.select_slider("Target Role Level", options=["Intern", "Junior SDE", "Systems / Senior SDE"], value="Junior SDE")

    if st.button("🚀 Generate Interview Problem", use_container_width=True):
        with st.spinner("Google Gemma 2 generating scenario & tracing OpenTelemetry span..."):
            st.session_state["current_q"] = engine.generate_interview_question(topic=topic, difficulty=difficulty)

    if "current_q" in st.session_state:
        q = st.session_state["current_q"]
        st.info(f"**Scenario:** {q.get('problem')}")

        with st.expander("🔍 Key Concepts Evaluated"):
            for c in q.get("concepts", []):
                st.markdown(f"- {c}")

        with st.expander("💡 View Coaching Hint"):
            st.write(q.get("hint"))

        candidate_ans = st.text_area("Candidate Answer / Notes:", height=130, placeholder="Type the student's response to generate a structured grading report...")

        if st.button("📝 Generate Paid Session Scorecard"):
            if not candidate_ans.strip():
                st.warning("Please enter candidate notes before grading.")
            else:
                with st.spinner("Gemma 2 grading response..."):
                    eval_res = engine.evaluate_candidate_answer(question=q.get("problem", ""), candidate_answer=candidate_ans)
                    st.session_state["eval_res"] = eval_res

        if "eval_res" in st.session_state:
            eval_res = st.session_state["eval_res"]
            st.success(f"**Session Score: {eval_res.get('score', 'N/A')} / 10**")
            st.markdown(f"**Strengths:** {eval_res.get('strengths')}")
            st.markdown(f"**Actionable Gaps:** {eval_res.get('critique')}")
            st.info(f"**Reference Solution:** {eval_res.get('exemplar')}")

            scorecard_md = f"""# 🎯 1-ON-1 TECHNICAL MOCK INTERVIEW SCORECARD

**Topic:** {topic}
**Difficulty Level:** {difficulty}
**Candidate Final Score:** {eval_res.get('score', 'N/A')} / 10

---

## 1. Problem Scenario
{q.get('problem', '')}

## 2. Key Strengths Demonstrated
{eval_res.get('strengths', '')}

## 3. Areas for Improvement & Technical Gaps
{eval_res.get('critique', '')}

## 4. Benchmark Reference Solution
{eval_res.get('exemplar', '')}

---
*Mentorship session conducted via CampusGemma AI with OpenTelemetry tracing.*
"""
            st.download_button(
                label="📥 Download Mentorship Scorecard (.md)",
                data=scorecard_md,
                file_name="Interview_Scorecard.md",
                mime="text/markdown",
                use_container_width=True
            )

# ----------------- TAB 4: CLIENT CODE AUDITOR -----------------
with tab4:
    st.subheader("Rapid Code Audit & Bottleneck Report Generator")
    lang = st.selectbox("Language", ["cpp", "python", "go", "c"])
    sample_code = """// Example: Lock-free ring buffer snippet
#include <atomic>
#include <vector>

template <typename T, size_t Cap>
class RingBuffer {
    std::atomic<size_t> head_{0};
    std::atomic<size_t> tail_{0};
    T buffer_[Cap];
public:
    bool push(const T& val) {
        size_t current_tail = tail_.load(std::memory_order_relaxed);
        if ((current_tail + 1) % Cap == head_.load(std::memory_order_acquire))
            return false;
        buffer_[current_tail] = val;
        tail_.store((current_tail + 1) % Cap, std::memory_order_release);
        return true;
    }
};"""
    code_input = st.text_area("Paste Client or Lab Code:", value=sample_code, height=200)

    if st.button("🔬 Generate Technical Audit Report", use_container_width=True):
        with st.spinner("Auditing code with Google Gemma 2..."):
            st.session_state["audit_res"] = engine.explain_lab_code(code=code_input, language=lang)

    if "audit_res" in st.session_state:
        res = st.session_state["audit_res"]
        st.markdown(f"### 📋 Executive Summary\n{res.get('summary')}")
        st.markdown(f"### 🧠 Memory & Concurrency Analysis\n{res.get('memory_breakdown')}")
        st.markdown(f"### ⏱️ Algorithmic Complexity\n{res.get('complexity')}")
        st.warning(f"### ⚠️ Risk & Deadlock Audit\n{res.get('pitfalls')}")

        audit_md = f"""# 🔬 TECHNICAL CODE AUDIT & SECURITY REPORT

**Language:** {lang.upper()}
**Audit Engine:** Google Gemma 2 (`gemma2-9b-it`)

---

## 1. Executive Summary
{res.get('summary', '')}

## 2. Memory & Concurrency Architecture
{res.get('memory_breakdown', '')}

## 3. Algorithmic Complexity
{res.get('complexity', '')}

## 4. Identified Vulnerabilities & Pitfalls
{res.get('pitfalls', '')}

---
*Generated by CampusGemma AI Client Security Auditor.*
"""
        st.download_button(
            label="📥 Download Audit Report (.md)",
            data=audit_md,
            file_name="Code_Audit_Report.md",
            mime="text/markdown",
            use_container_width=True
        )

# ----------------- TAB 5: OPENTELEMETRY & UNIT ECONOMICS -----------------
with tab5:
    st.subheader("OpenTelemetry GenAI Observability & Side-Hustle Unit Economics")
    st.caption("Live trace spans proving why open-weight models (Google Gemma 2) keep side-hustle profit margins at 100%.")

    spans = get_recent_spans()
    c1, c2, c3 = st.columns(3)
    c1.metric("Recorded GenAI Spans", len(spans))
    c2.metric("Gemma 2 Inference Cost", "$0.00 USD", delta="100% Profit Margin")
    c3.metric("Proprietary API Cost Saved", f"${round(len(spans) * 0.045, 3)} USD", delta="Saved via Open Weights")

    if not spans:
        st.info("No inference spans recorded yet. Generate a Freelance Proposal or Interview Scenario to inspect live OpenTelemetry traces.")
    else:
        for s in reversed(spans):
            with st.container():
                st.markdown(f"""
                <div class="metric-card">
                    <strong>Span Name:</strong> <code>{s['name']}</code> | 
                    <strong>Duration:</strong> {s['duration_ms']} ms | 
                    <strong>Status:</strong> {s['status']} <br>
                    <small>Trace ID: <code>{s['trace_id']}</code> | Span ID: <code>{s['span_id']}</code></small>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("Inspect OpenTelemetry GenAI Attributes"):
                    st.json(s["attributes"])
