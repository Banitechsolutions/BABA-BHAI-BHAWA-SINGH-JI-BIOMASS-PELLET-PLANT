import streamlit as st
from supabase import create_client, Client
from fpdf import FPDF
import base64
import urllib.parse
import datetime

# --- DATABASE CONNECTION ---
# Configure these in Streamlit Cloud -> Advanced Settings -> Secrets
# st.secrets["SUPABASE_URL"] and st.secrets["SUPABASE_KEY"]
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "your-supabase-url")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "your-supabase-key")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- PDF GENERATOR (A4 LETTERHEAD) ---
class PDF(FPDF):
    def header(self):
        # Forest Green Header Block for Eco-Friendly Biomass Theme
        self.set_fill_color(34, 139, 34) 
        self.rect(0, 0, 210, 40, 'F')
        
        # Firm Name
        self.set_font('Arial', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, 'BABA BHAI BHAWA SINGH JI BIOMASS PELLET PLANT', 0, 1, 'C')
        
        # Address & GSTIN
        self.set_font('Arial', '', 10)
        self.cell(0, 6, 'Building No./Flat No.: 5, Kot Dharam Chand Kalan Road, Tarn Taran, Punjab, 143301', 0, 1, 'C')
        self.set_font('Arial', 'B', 10)
        self.cell(0, 6, 'GSTIN: 03ABGFB5093F1ZO', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_quotation_pdf(client_name, date, qty, rate, transport, tax_type, total):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Body
    pdf.cell(200, 10, txt=f"Date: {date}", ln=True, align='R')
    pdf.cell(200, 10, txt=f"Quotation For: {client_name}", ln=True, align='L')
    pdf.ln(10)
    
    # Table Header
    pdf.set_fill_color(200, 220, 200)
    pdf.cell(90, 10, 'Description', 1, 0, 'C', 1)
    pdf.cell(30, 10, 'Qty (MT)', 1, 0, 'C', 1)
    pdf.cell(35, 10, 'Rate (Rs)', 1, 0, 'C', 1)
    pdf.cell(35, 10, 'Amount (Rs)', 1, 1, 'C', 1)
    
    # Table Data
    base_amount = qty * rate
    pdf.cell(90, 10, 'Eco-Friendly Biomass Pellets', 1, 0, 'L')
    pdf.cell(30, 10, str(qty), 1, 0, 'C')
    pdf.cell(35, 10, str(rate), 1, 0, 'C')
    pdf.cell(35, 10, str(base_amount), 1, 1, 'R')
    
    pdf.cell(155, 10, 'Transportation Cost', 1, 0, 'R')
    pdf.cell(35, 10, str(transport), 1, 1, 'R')
    
    tax_amount = (base_amount + transport) * 0.05 # Assuming 5% GST for pellets
    pdf.cell(155, 10, f'GST ({tax_type} - 5%)', 1, 0, 'R')
    pdf.cell(35, 10, str(tax_amount), 1, 1, 'R')
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(155, 10, 'TOTAL AMOUNT', 1, 0, 'R', 1)
    pdf.cell(35, 10, str(total), 1, 1, 'R', 1)
    
    pdf.ln(20)
    pdf.cell(200, 10, txt="Authorized Signatory", ln=True, align='R')
    
    return pdf.output(dest='S').encode('latin1')

# --- AUTHENTICATION (BASIC) ---
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None

if st.session_state['user_role'] is None:
    st.title("Login")
    role = st.selectbox("Select Role", ["Staff", "Admin"])
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # Replace with secure passwords in production
        if role == "Admin" and password == "admin123":
            st.session_state['user_role'] = "Admin"
            st.rerun()
        elif role == "Staff" and password == "staff123":
            st.session_state['user_role'] = "Staff"
            st.rerun()
        else:
            st.error("Invalid Password")
else:
    # --- MAIN APPLICATION DASHBOARD ---
    st.sidebar.title(f"Welcome, {st.session_state['user_role']}")
    menu = st.sidebar.radio("Navigation", ["Issue Quotation", "Quotation Records"])
    
    if st.sidebar.button("Logout"):
        st.session_state['user_role'] = None
        st.rerun()

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
                # Calculations (Assuming 5% GST on Biomass Pellets)
                base = (qty * rate) + transport
                tax = base * 0.05
                total = base + tax
                
                # Save to Supabase
                data, count = supabase.table("quotations").insert({
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
                
                # Generate PDF
                pdf_bytes = create_quotation_pdf(client_name, datetime.date.today(), qty, rate, transport, tax_type, total)
                
                # Provide Print/Download Button
                st.download_button(
                    label="📄 Download / Print A4 Quotation",
                    data=pdf_bytes,
                    file_name=f"Quotation_{client_name}.pdf",
                    mime="application/pdf"
                )
                
                # Provide WhatsApp Link
                if client_mobile:
                    msg = urllib.parse.quote(f"Hello {client_name}, your quotation for {qty}MT of Biomass Pellets is Rs. {total}. Please find the document attached.")
                    wa_link = f"https://wa.me/{client_mobile}?text={msg}"
                    st.markdown(f"[📱 Send WhatsApp Message to Client]({wa_link})")

    elif menu == "Quotation Records":
        st.title("Quotation History")
        
        # Fetch records
        response = supabase.table("quotations").select("*").order("created_at", desc=True).execute()
        records = response.data
        
        for record in records:
            with st.expander(f"{record['created_at'][:10]} - {record['client_name']} - Rs.{record['total_amount']}"):
                st.write(f"**Quantity:** {record['quantity_mt']} MT | **Rate:** Rs.{record['rate_per_mt']}/MT")
                st.write(f"**Issued By:** {record['issued_by']}")
                
                col_a, col_b = st.columns(2)
                
                # Reprint Option
                pdf_bytes = create_quotation_pdf(
                    record['client_name'], 
                    record['created_at'][:10], 
                    record['quantity_mt'], 
                    record['rate_per_mt'], 
                    record['transportation_cost'], 
                    record['tax_type'], 
                    record['total_amount']
                )
                col_a.download_button(
                    label="📄 Reprint PDF",
                    data=pdf_bytes,
                    file_name=f"Quotation_{record['client_name']}_Reprint.pdf",
                    mime="application/pdf",
                    key=f"dl_{record['id']}"
                )
                
                # Delete Option (Admin Only)
                if st.session_state['user_role'] == "Admin":
                    if col_b.button("🗑️ Delete Record", key=f"del_{record['id']}"):
                        supabase.table("quotations").delete().eq("id", record['id']).execute()
                        st.success("Record deleted. Please refresh the page.")
                        st.rerun()
