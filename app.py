import streamlit as st
from supabase import create_client, Client
from fpdf import FPDF
import urllib.parse
import datetime
import os

# --- DATABASE CONNECTION (HARDCODED) ---
SUPABASE_URL = "https://vnkykcvkaglvtciaxzaa.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZua3lrY3ZrYWdsdnRjaWF4emFhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODcyMzUyNTEsImV4cCI6MjEwMjgxMTI1MX0.1_0R39KMFJiZ7ouErrWnpHqXKhUxLO--uFe6TgMnEWI"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- PDF GENERATOR (A4 LETTERHEAD) ---
class PDF(FPDF):
    def header(self):
        # CLASSICAL EDGE-TO-EDGE DESIGN
        # Solid classic dark green bar touching the top edges
        self.set_fill_color(24, 69, 36) 
        self.rect(0, 0, 210, 10, 'F') 
        
        self.ln(12)
        
        # Firm Name (Classic Times Font, bold and large)
        self.set_font('Times', 'B', 22)
        self.set_text_color(24, 69, 36)
        self.cell(0, 10, 'BABA BHAI BHAWA SINGH JI BIOMASS PELLET PLANT', 0, 1, 'C')
        
        # Address
        self.set_font('Times', '', 11)
        self.set_text_color(50, 50, 50)
        self.cell(0, 6, 'Kot Dharam Chand Kalan Road, Tarn Taran, Punjab, 143301', 0, 1, 'C')
        
        # GSTIN & Partner Details
        self.set_font('Times', 'B', 11)
        self.set_text_color(30, 30, 30)
        self.cell(0, 6, 'GSTIN: 03ABGFB5093F1ZO  |  Partner: Chamkaur Singh  |  Mob: +91 98722 73941', 0, 1, 'C')
        
        # Elegant Classical Double Underline
        self.set_draw_color(24, 69, 36)
        self.set_line_width(0.7)
        self.line(10, 45, 200, 45)
        self.set_line_width(0.2)
        self.line(10, 46.5, 200, 46.5)
        
        self.ln(12) # Space before table

    def footer(self):
        self.set_y(-25)
        
        # Subtle footer divider line
        self.set_draw_color(180, 180, 180)
        self.set_line_width(0.2)
        self.line(10, 275, 200, 275)
        
        self.set_font('Times', 'I', 9)
        self.set_text_color(128, 128, 128)
        
        # Page Number (Aligned Left)
        self.cell(50, 10, f'Page {self.page_no()}', 0, 0, 'L')
        
        # Branding (Aligned Bottom Right)
        self.set_x(125)
        self.cell(50, 10, "Software designed by", 0, 0, 'R')
        
        if os.path.exists("bani_logo.jpeg"):
            self.image("bani_logo.jpeg", x=177, y=273, w=22)

def create_quotation_pdf(client_name, date, qty, rate, transport, tax_type, total, ref_no):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Times", size=12) # Match classical font for body
    pdf.set_text_color(0, 0, 0)
    
    # Body Header
    pdf.cell(100, 8, txt=f"Ref No: {ref_no}", ln=0, align='L')
    pdf.cell(90, 8, txt=f"Date: {date}", ln=1, align='R')
    
    pdf.set_font("Times", 'B', 12)
    pdf.cell(200, 8, txt=f"Quotation For: {client_name}", ln=True, align='L')
    pdf.ln(6)
    
    # Table Header
    pdf.set_fill_color(240, 245, 240) 
    pdf.cell(90, 10, 'Description', 1, 0, 'C', 1)
    pdf.cell(30, 10, 'Qty (MT)', 1, 0, 'C', 1)
    pdf.cell(35, 10, 'Rate (Rs)', 1, 0, 'C', 1)
    pdf.cell(35, 10, 'Amount (Rs)', 1, 1, 'C', 1)
    
    # Table Data
    pdf.set_font("Times", '', 12)
    base_amount = qty * rate
    pdf.cell(90, 10, 'Eco-Friendly Biomass Pellets', 1, 0, 'L')
    pdf.cell(30, 10, f"{qty:,.2f}", 1, 0, 'C')
    pdf.cell(35, 10, f"{rate:,.2f}", 1, 0, 'C')
    pdf.cell(35, 10, f"{base_amount:,.2f}", 1, 1, 'R')
    
    pdf.cell(155, 10, 'Transportation Cost', 1, 0, 'R')
    pdf.cell(35, 10, f"{transport:,.2f}", 1, 1, 'R')
    
    tax_amount = (base_amount + transport) * 0.05
    pdf.cell(155, 10, f'GST ({tax_type} - 5%)', 1, 0, 'R')
    pdf.cell(35, 10, f"{tax_amount:,.2f}", 1, 1, 'R')
    
    pdf.set_font("Times", 'B', 13)
    pdf.cell(155, 10, 'TOTAL AMOUNT', 1, 0, 'R', 1)
    pdf.cell(35, 10, f"{total:,.2f}", 1, 1, 'R', 1)
    
    pdf.ln(15)
    
    # Terms & Conditions
    pdf.set_font("Times", 'I', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, txt="* Terms and conditions apply.", ln=True, align='L')
    
    pdf.ln(15)
    
    # Signatory
    pdf.set_font("Times", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(190, 10, txt="Authorized Signatory", ln=True, align='R')
    pdf.set_font("Times", '', 11)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(190, 5, txt="For Baba Bhai Bhawa Singh Ji Biomass Pellet Plant", ln=True, align='R')
    
    return pdf.output(dest='S').encode('latin1')


# --- UI LOGO HELPER FUNCS ---
def display_ui_branding():
    st.markdown("<p style='text-align: center; color: gray; font-size: 13px; margin-bottom: 5px;'>Software designed by</p>", unsafe_allow_html=True)
    if os.path.exists("bani_logo.jpeg"):
        cols = st.columns([1, 2, 1])
        with cols[1]:
            st.image("bani_logo.jpeg", use_container_width=True)

def display_sidebar_branding():
    st.sidebar.markdown("---")
    st.sidebar.markdown("<p style='text-align: center; color: gray; font-size: 13px; margin-bottom: 5px;'>Software designed by</p>", unsafe_allow_html=True)
    if os.path.exists("bani_logo.jpeg"):
        st.sidebar.image("bani_logo.jpeg", use_container_width=True)


# --- AUTHENTICATION ---
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None

if st.session_state['user_role'] is None:
    st.title("Login")
    role = st.selectbox("Select Role", ["Staff", "Admin"])
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if role == "Admin" and password == "admin123":
            st.session_state['user_role'] = "Admin"
            st.rerun()
        elif role == "Staff" and password == "staff123":
            st.session_state['user_role'] = "Staff"
            st.rerun()
        else:
            st.error("Invalid Password")
            
    # Login Page Branding
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    display_ui_branding()

else:
    # --- MAIN APPLICATION DASHBOARD ---
    st.sidebar.title(f"Welcome, {st.session_state['user_role']}")
    menu = st.sidebar.radio("Navigation", ["Issue Quotation", "Quotation Records"])
    
    if st.sidebar.button("Logout"):
        st.session_state['user_role'] = None
        st.rerun()
        
    # Working Page Sidebar Branding
    display_sidebar_branding()

    if menu == "Issue Quotation":
        st.title("Issue New Quotation")
        
        with st.form("quote_form"):
            col1, col2 = st.columns(2)
            client_name = col1.text_input("Client/Company Name")
            client_mobile = col2.text_input("Client WhatsApp Number (with country code, e.g., 919876543210)")
            
            col3, col4 = st.columns(2)
            qty = col3.number_input("Quantity (MT)", min_value=1.0, value=10.0)
            rate = col4.number_input("Rate per MT (Rs)", min_value=0.0, value=5000.0)
            
            transport = st.number_input("Transportation Cost (Rs)", min_value=0.0, value=1000.0)
            tax_type = st.selectbox("Tax Type", ["CGST/SGST", "IGST"])
            
            submit = st.form_submit_button("Generate Quotation")
            
        if submit:
            base = (qty * rate) + transport
            tax = base * 0.05
            total = base + tax
            
            response = supabase.table("quotations").insert({
                "client_name": client_name,
                "client_mobile": client_mobile,
                "quantity_mt": qty,
                "rate_per_mt": rate,
                "transportation_cost": transport,
                "tax_type": tax_type,
                "total_amount": total,
                "issued_by": st.session_state['user_role']
            }).execute()
            
            st.success("Quotation Saved Successfully!")
            
            new_record = response.data[0]
            ref_no = f"BBSP-{new_record['id'][:6].upper()}"
            
            pdf_bytes = create_quotation_pdf(
                client_name, 
                datetime.date.today().strftime("%d-%b-%Y"), 
                qty, rate, transport, tax_type, total, 
                ref_no
            )
            
            wa_link = ""
            if client_mobile:
                msg = urllib.parse.quote(f"Hello {client_name}, your quotation ({ref_no}) for {qty}MT of Biomass Pellets is Rs. {total:,.2f}. Please find the document attached.")
                wa_link = f"https://wa.me/{client_mobile}?text={msg}"
            
            # Save variables into session state so they survive the "Print" rerun
            st.session_state['last_pdf'] = pdf_bytes
            st.session_state['last_filename'] = f"{ref_no}_{client_name}.pdf"
            st.session_state['last_wa'] = wa_link
            st.session_state['last_client'] = client_name

        # Render action buttons outside the form submit logic using Memory (Session State)
        if 'last_pdf' in st.session_state:
            st.markdown("---")
            st.write(f"**Actions for latest quotation: {st.session_state['last_client']}**")
            
            st.download_button(
                label="📄 Download / Print A4 Quotation",
                data=st.session_state['last_pdf'],
                file_name=st.session_state['last_filename'],
                mime="application/pdf"
            )
            
            if st.session_state['last_wa']:
                st.markdown(f"[📱 Send WhatsApp Message to Client]({st.session_state['last_wa']})")

    elif menu == "Quotation Records":
        st.title("Quotation History")
        
        response = supabase.table("quotations").select("*").order("created_at", desc=True).execute()
        records = response.data
        
        for record in records:
            record_date = record['created_at'][:10] if record.get('created_at') else "Unknown Date"
            ref_no = f"BBSP-{record['id'][:6].upper()}"
            
            with st.expander(f"{record_date} | {ref_no} | {record['client_name']} - Rs.{record['total_amount']:,.2f}"):
                st.write(f"**Quantity:** {record['quantity_mt']} MT | **Rate:** Rs.{record['rate_per_mt']}/MT")
                st.write(f"**Issued By:** {record['issued_by']}")
                
                col_a, col_b = st.columns(2)
                
                pdf_bytes = create_quotation_pdf(
                    record['client_name'], 
                    record_date, 
                    record['quantity_mt'], 
                    record['rate_per_mt'], 
                    record['transportation_cost'], 
                    record['tax_type'], 
                    record['total_amount'],
                    ref_no
                )
                col_a.download_button(
                    label="📄 Reprint PDF",
                    data=pdf_bytes,
                    file_name=f"{ref_no}_{record['client_name']}_Reprint.pdf",
                    mime="application/pdf",
                    key=f"dl_{record['id']}"
                )
                
                if st.session_state['user_role'] == "Admin":
                    if col_b.button("🗑️ Delete Record", key=f"del_{record['id']}"):
                        supabase.table("quotations").delete().eq("id", record['id']).execute()
                        st.success("Record deleted. Please refresh the page.")
                        st.rerun()
