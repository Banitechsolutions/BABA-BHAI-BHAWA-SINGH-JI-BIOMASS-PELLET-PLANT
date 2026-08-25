import streamlit as st
from supabase import create_client, Client
import urllib.parse
import datetime
import os
import base64

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Baba Bhai Bhawa Singh Ji Biomass", layout="centered")

# --- DATABASE CONNECTION (HARDCODED) ---
SUPABASE_URL = "https://vnkykcvkaglvtciaxzaa.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZua3lrY3ZrYWdsdnRjaWF4emFhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODcyMzUyNTEsImV4cCI6MjEwMjgxMTI1MX0.1_0R39KMFJiZ7ouErrWnpHqXKhUxLO--uFe6TgMnEWI"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- IMAGE TO BASE64 CONVERTER (For Self-Contained HTML) ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# --- ADVANCED HTML/CSS QUOTATION GENERATOR ---
def create_html_quotation(client_name, client_mobile, client_address, date, qty, rate, transport, tax_type, total, ref_no):
    base_amount = qty * rate
    tax_amount = (base_amount + transport) * 0.05
    
    logo_b64 = get_base64_image("bani_logo.jpeg")
    logo_html = f'<img src="data:image/jpeg;base64,{logo_b64}" style="height: 40px; margin-left: 10px;">' if logo_b64 else ''
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Quotation - {client_name}</title>
        <style>
            body {{ font-family: 'Arial', sans-serif; background-color: #f4f6f4; margin: 0; padding: 20px; }}
            .container {{ max-width: 800px; margin: auto; background: white; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, #1e3c72, #2a5298); color: white; padding: 30px 40px; text-align: center; border-bottom: 6px solid #ff9a44; }}
            .header h1 {{ margin: 0; font-family: 'Times New Roman', serif; font-size: 24px; letter-spacing: 0.5px; white-space: nowrap; }}
            .header p {{ margin: 5px 0; font-size: 13px; color: #e0e6ed; }}
            .header .partner-info {{ margin-top: 15px; font-weight: bold; color: #ffdc73; font-size: 14px; }}
            .details-section {{ padding: 30px 40px 10px; display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #f0f0f0; }}
            .client-box {{ background: #f4f7fb; padding: 15px; border-left: 4px solid #1e3c72; width: 50%; border-radius: 0 4px 4px 0; }}
            .client-box h3 {{ margin: 0 0 5px 0; color: #333; font-size: 16px; }}
            .client-box text {{ display: block; font-size: 13px; color: #555; margin-top: 3px; }}
            .meta-info {{ text-align: right; }}
            .meta-info text {{ display: block; margin-bottom: 5px; font-size: 14px; color: #555; }}
            .table-container {{ padding: 20px 40px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th {{ background-color: #1e3c72; color: white; padding: 12px; text-align: left; font-size: 14px; border: 1px solid #152b52; }}
            td {{ padding: 12px; border: 1px solid #ddd; font-size: 14px; color: #444; }}
            .text-right {{ text-align: right; }}
            .text-center {{ text-align: center; }}
            .row-even {{ background-color: #f9fbfd; }}
            .total-row td {{ font-weight: bold; font-size: 15px; background-color: #eef2f7; color: #1e3c72; border-top: 2px solid #1e3c72; }}
            .bottom-section {{ padding: 20px 40px 40px; display: flex; justify-content: space-between; align-items: flex-end; }}
            .terms {{ font-size: 12px; color: #777; font-style: italic; max-width: 50%; }}
            .signatory {{ text-align: right; }}
            .signatory p {{ margin: 0; font-size: 14px; color: #555; }}
            .signatory h4 {{ margin: 0 0 40px 0; font-size: 16px; color: #333; }}
            .dev-branding {{ background: #222; color: #aaa; text-align: right; padding: 10px 40px; font-size: 12px; display: flex; justify-content: flex-end; align-items: center; }}
            .print-btn {{ display: block; width: 200px; margin: 0 auto 20px; padding: 12px; background: #ff9a44; color: #fff; text-align: center; font-weight: bold; border-radius: 5px; cursor: pointer; border: none; font-size: 16px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }}
            .print-btn:hover {{ background: #e88633; }}
            @media print {{
                body {{ background-color: white; padding: 0; }}
                .container {{ box-shadow: none; border: none; max-width: 100%; }}
                .print-btn {{ display: none; }}
                .header, th, .total-row td, .dev-branding {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
            }}
        </style>
    </head>
    <body>
        <button class="print-btn" onclick="window.print()">🖨️ Print / Save as PDF</button>
        <div class="container">
            <div class="header">
                <h1>BABA BHAI BHAWA SINGH JI BIOMASS PELLET PLANT</h1>
                <p>Kot Dharam Chand Kalan Road, Tarn Taran, Punjab, 143301 | GSTIN: 03ABGFB5093F1ZO</p>
                <div class="partner-info">Partner: Chamkaur Singh &nbsp;|&nbsp; Mob: +91 98722 73941</div>
            </div>
            <div class="details-section">
                <div class="client-box">
                    <h3>Quotation For:</h3>
                    <strong>{client_name}</strong>
                    <text><strong>Mobile:</strong> {client_mobile}</text>
                    <text><strong>Address:</strong><br>{client_address}</text>
                </div>
                <div class="meta-info">
                    <text><strong>Ref No:</strong> {ref_no}</text>
                    <text><strong>Date:</strong> {date}</text>
                </div>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Description</th>
                            <th class="text-center">Qty (MT)</th>
                            <th class="text-center">Rate (Rs)</th>
                            <th class="text-right">Amount (Rs)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Eco-Friendly Biomass Pellets</td>
                            <td class="text-center">{qty:,.2f}</td>
                            <td class="text-center">{rate:,.2f}</td>
                            <td class="text-right">{base_amount:,.2f}</td>
                        </tr>
                        <tr class="row-even">
                            <td colspan="3" class="text-right"><strong>Transportation Cost</strong></td>
                            <td class="text-right">{transport:,.2f}</td>
                        </tr>
                        <tr>
                            <td colspan="3" class="text-right"><strong>GST ({tax_type} - 5%)</strong></td>
                            <td class="text-right">{tax_amount:,.2f}</td>
                        </tr>
                        <tr class="total-row">
                            <td colspan="3" class="text-right">TOTAL AMOUNT</td>
                            <td class="text-right">Rs. {total:,.2f}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="bottom-section">
                <div class="terms">
                    * Terms and conditions apply.<br>
                    * This is a computer-generated document.
                </div>
                <div class="signatory">
                    <h4>Authorized Signatory</h4>
                    <p>For Baba Bhai Bhawa Singh Ji</p>
                    <p>Biomass Pellet Plant</p>
                </div>
            </div>
            <div class="dev-branding">
                Software designed by Bani Tech Solutions {logo_html}
            </div>
        </div>
    </body>
    </html>
    """
    return html_content.encode('utf-8')


# --- ADVANCED HTML/CSS PURCHASE ORDER GENERATOR (Matched to Quotation Style) ---
def create_html_purchase_order(supplier_name, supplier_mobile, supplier_gst, supplier_address, date, qty, rate, transport, tax_type, total, po_ref_no):
    base_amount = qty * rate
    tax_amount = (base_amount + transport) * 0.05
    
    logo_b64 = get_base64_image("bani_logo.jpeg")
    logo_html = f'<img src="data:image/jpeg;base64,{logo_b64}" style="height: 40px; margin-left: 10px;">' if logo_b64 else ''
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Purchase Order - {supplier_name}</title>
        <style>
            body {{ font-family: 'Arial', sans-serif; background-color: #f4f6f4; margin: 0; padding: 20px; }}
            .container {{ max-width: 800px; margin: auto; background: white; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, #1e3c72, #2a5298); color: white; padding: 30px 40px; text-align: center; border-bottom: 6px solid #ff9a44; }}
            .header h1 {{ margin: 0; font-family: 'Times New Roman', serif; font-size: 24px; letter-spacing: 0.5px; white-space: nowrap; }}
            .header p {{ margin: 5px 0; font-size: 13px; color: #e0e6ed; }}
            .header .partner-info {{ margin-top: 15px; font-weight: bold; color: #ffdc73; font-size: 14px; }}
            .details-section {{ padding: 30px 40px 10px; display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #f0f0f0; }}
            .supplier-box {{ background: #f4f7fb; padding: 15px; border-left: 4px solid #1e3c72; width: 50%; border-radius: 0 4px 4px 0; }}
            .supplier-box h3 {{ margin: 0 0 5px 0; color: #333; font-size: 16px; }}
            .supplier-box text {{ display: block; font-size: 13px; color: #555; margin-top: 3px; }}
            .meta-info {{ text-align: right; }}
            .meta-info text {{ display: block; margin-bottom: 5px; font-size: 14px; color: #555; }}
            .table-container {{ padding: 20px 40px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th {{ background-color: #1e3c72; color: white; padding: 12px; text-align: left; font-size: 14px; border: 1px solid #152b52; }}
            td {{ padding: 12px; border: 1px solid #ddd; font-size: 14px; color: #444; }}
            .text-right {{ text-align: right; }}
            .text-center {{ text-align: center; }}
            .row-even {{ background-color: #f9fbfd; }}
            .total-row td {{ font-weight: bold; font-size: 15px; background-color: #eef2f7; color: #1e3c72; border-top: 2px solid #1e3c72; }}
            .bottom-section {{ padding: 20px 40px 40px; display: flex; justify-content: space-between; align-items: flex-end; }}
            .terms {{ font-size: 12px; color: #777; font-style: italic; max-width: 50%; }}
            .signatory {{ text-align: right; }}
            .signatory p {{ margin: 0; font-size: 14px; color: #555; }}
            .signatory h4 {{ margin: 0 0 40px 0; font-size: 16px; color: #333; }}
            .dev-branding {{ background: #222; color: #aaa; text-align: right; padding: 10px 40px; font-size: 12px; display: flex; justify-content: flex-end; align-items: center; }}
            .print-btn {{ display: block; width: 200px; margin: 0 auto 20px; padding: 12px; background: #ff9a44; color: #fff; text-align: center; font-weight: bold; border-radius: 5px; cursor: pointer; border: none; font-size: 16px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }}
            .print-btn:hover {{ background: #e88633; }}
            @media print {{
                body {{ background-color: white; padding: 0; }}
                .container {{ box-shadow: none; border: none; max-width: 100%; }}
                .print-btn {{ display: none; }}
                .header, th, .total-row td, .dev-branding {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
            }}
        </style>
    </head>
    <body>
        <button class="print-btn" onclick="window.print()">🖨️ Print / Save PO as PDF</button>
        <div class="container">
            <div class="header">
                <h1>PURCHASE ORDER</h1>
                <p>Baba Bhai Bhawa Singh Ji Biomass Pellet Plant | GSTIN: 03ABGFB5093F1ZO</p>
                <div class="partner-info">Kot Dharam Chand Kalan Road, Tarn Taran, Punjab, 143301</div>
            </div>
            <div class="details-section">
                <div class="supplier-box">
                    <h3>Vendor / Supplier Details:</h3>
                    <strong>{supplier_name}</strong>
                    <text><strong>Mobile:</strong> {supplier_mobile}</text>
                    <text><strong>GSTIN:</strong> {supplier_gst}</text>
                    <text><strong>Address:</strong><br>{supplier_address}</text>
                </div>
                <div class="meta-info">
                    <text><strong>PO Ref No:</strong> {po_ref_no}</text>
                    <text><strong>Date:</strong> {date}</text>
                </div>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Item Description</th>
                            <th class="text-center">Qty (MT)</th>
                            <th class="text-center">Rate (Rs)</th>
                            <th class="text-right">Amount (Rs)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Raw Material / Biomass Feedstock</td>
                            <td class="text-center">{qty:,.2f}</td>
                            <td class="text-center">{rate:,.2f}</td>
                            <td class="text-right">{base_amount:,.2f}</td>
                        </tr>
                        <tr class="row-even">
                            <td colspan="3" class="text-right"><strong>Transportation Cost</strong></td>
                            <td class="text-right">{transport:,.2f}</td>
                        </tr>
                        <tr>
                            <td colspan="3" class="text-right"><strong>GST ({tax_type} - 5%)</strong></td>
                            <td class="text-right">{tax_amount:,.2f}</td>
                        </tr>
                        <tr class="total-row">
                            <td colspan="3" class="text-right">TOTAL PO AMOUNT</td>
                            <td class="text-right">Rs. {total:,.2f}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="bottom-section">
                <div class="terms">
                    * Please deliver materials as per schedule.<br>
                    * Mention PO reference on your tax invoice.
                </div>
                <div class="signatory">
                    <h4>Authorized Signatory</h4>
                    <p>For Baba Bhai Bhawa Singh Ji</p>
                    <p>Biomass Pellet Plant</p>
                </div>
            </div>
            <div class="dev-branding">
                Software designed by Bani Tech Solutions {logo_html}
            </div>
        </div>
    </body>
    </html>
    """
    return html_content.encode('utf-8')


# --- UI BRANDING HELPER FUNCS ---
def display_top_header():
    st.markdown("<h2 style='text-align: center; color: #1e3c72; font-family: serif; margin-top: -20px;'>BABA BHAI BHAWA SINGH JI<br>BIOMASS PELLET PLANT</h2>", unsafe_allow_html=True)
    st.markdown("<div style='background-color: #ff9a44; height: 3px; width: 100%; margin-bottom: 30px;'></div>", unsafe_allow_html=True)

def display_sidebar_branding():
    st.sidebar.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.markdown("<p style='text-align: left; color: gray; font-size: 13px; margin-bottom: 5px;'>Software designed by:</p>", unsafe_allow_html=True)
    if os.path.exists("bani_logo.jpeg"):
        st.sidebar.image("bani_logo.jpeg", width=160) 

def display_login_branding():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray; font-size: 14px; margin-bottom: 10px;'>Software designed by:</p>", unsafe_allow_html=True)
    if os.path.exists("bani_logo.jpeg"):
        col1, col2, col3 = st.columns([1.5, 1, 1.5])
        with col2:
            st.image("bani_logo.jpeg", use_container_width=True)


# --- TOP FIRM HEADER ---
display_top_header()

# --- AUTHENTICATION ---
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None

if st.session_state['user_role'] is None:
    st.title("System Login")
    role = st.selectbox("Select Role", ["Staff", "Admin"], key="login_role_select")
    password = st.text_input("Password", type="password", key="login_password_input")
    
    if st.button("Login", key="login_button"):
        if role == "Admin" and password == "admin123":
            st.session_state['user_role'] = "Admin"
            st.rerun()
        elif role == "Staff" and password == "staff123":
            st.session_state['user_role'] = "Staff"
            st.rerun()
        else:
            st.error("Invalid Password")
            
    display_login_branding()

else:
    # --- MAIN APPLICATION DASHBOARD ---
    st.sidebar.title(f"Welcome, {st.session_state['user_role']}")
    menu = st.sidebar.radio("Navigation", ["Issue Quotation", "Issue Purchase Order", "Quotation Records", "Purchase Order Records"])
    
    if st.sidebar.button("Logout"):
        st.session_state['user_role'] = None
        st.rerun()
        
    display_sidebar_branding()

    if menu == "Issue Quotation":
        st.title("Issue New Quotation")
        
        with st.form("quote_form"):
            col1, col2 = st.columns(2)
            client_name = col1.text_input("Client/Company Name")
            client_mobile = col2.text_input("Client WhatsApp Number (e.g., 919876543210)")
            
            client_address = st.text_area("Client Full Address")
            
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
                "client_address": client_address,
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
            
            html_bytes = create_html_quotation(
                client_name, client_mobile, client_address,
                datetime.date.today().strftime("%d-%b-%Y"), 
                qty, rate, transport, tax_type, total, 
                ref_no
            )
            
            wa_link = ""
            if client_mobile:
                msg = urllib.parse.quote(f"Hello {client_name}, your quotation ({ref_no}) for {qty}MT of Biomass Pellets is Rs. {total:,.2f}. Please find the document attached.")
                wa_link = f"https://wa.me/{client_mobile}?text={msg}"
            
            st.session_state['last_file'] = html_bytes
            st.session_state['last_filename'] = f"{ref_no}_{client_name}.html"
            st.session_state['last_wa'] = wa_link
            st.session_state['last_client'] = client_name

        if 'last_file' in st.session_state:
            st.markdown("---")
            st.write(f"**Actions for latest quotation: {st.session_state['last_client']}**")
            
            st.download_button(
                label="🌐 Download / Print HTML Quotation",
                data=st.session_state['last_file'],
                file_name=st.session_state['last_filename'],
                mime="text/html"
            )
            
            if st.session_state['last_wa']:
                st.markdown(f"[📱 Send WhatsApp Message to Client]({st.session_state['last_wa']})")

    elif menu == "Issue Purchase Order":
        st.title("Generate Purchase Order (PO)")
        
        try:
            parties_res = supabase.table("parties").select("*").execute()
            parties = parties_res.data if parties_res.data else []
        except Exception:
            parties = []
            
        if parties:
            party_names = [p.get('name', 'Unnamed Party') for p in parties]
            selected_party_name = st.selectbox("Select Vendor / Party", party_names)
            
            selected_party = next((p for p in parties if p.get('name') == selected_party_name), {})
            fetched_gst = selected_party.get('gst_no', 'N/A')
            fetched_address = selected_party.get('address', 'N/A')
            fetched_mobile = selected_party.get('phone', '')
        else:
            selected_party_name = st.text_input("Vendor / Party Name")
            fetched_mobile = st.text_input("Vendor WhatsApp Number (e.g., 919876543210)")
            fetched_gst = st.text_input("GSTIN Number")
            fetched_address = st.text_area("Full Address")
            
        with st.form("po_form"):
            col1, col2 = st.columns(2)
            po_qty = col1.number_input("Quantity (MT)", min_value=1.0, value=10.0)
            po_rate = col2.number_input("Rate per MT (Rs)", min_value=0.0, value=4000.0)
            
            po_transport = st.number_input("Transportation Cost (Rs)", min_value=0.0, value=500.0)
            po_tax_type = st.selectbox("Tax Type for PO", ["CGST/SGST", "IGST"])
            
            po_submit = st.form_submit_button("Generate Purchase Order")
            
        if po_submit and selected_party_name:
            base = (po_qty * po_rate) + po_transport
            tax = base * 0.05
            total = base + tax
            
            po_res = supabase.table("purchase_orders").insert({
                "supplier_name": selected_party_name,
                "supplier_gst": fetched_gst,
                "supplier_address": fetched_address,
                "supplier_mobile": fetched_mobile,
                "quantity_mt": po_qty,
                "rate_per_mt": po_rate,
                "transportation_cost": po_transport,
                "tax_type": po_tax_type,
                "total_amount": total,
                "issued_by": st.session_state['user_role']
            }).execute()
            
            st.success("Purchase Order Generated and Saved Successfully!")
            
            po_new_record = po_res.data[0]
            po_ref_no = f"BBSP-PO-{po_new_record['id'][:6].upper()}"
            
            html_po_bytes = create_html_purchase_order(
                selected_party_name, fetched_mobile, fetched_gst, fetched_address,
                datetime.date.today().strftime("%d-%b-%Y"),
                po_qty, po_rate, po_transport, po_tax_type, total, po_ref_no
            )
            
            wa_po_link = ""
            if fetched_mobile:
                msg_po = urllib.parse.quote(f"Hello {selected_party_name}, your Purchase Order ({po_ref_no}) for {po_qty}MT of Biomass Feedstock is Rs. {total:,.2f}. Please find the details attached.")
                wa_po_link = f"https://wa.me/{fetched_mobile}?text={msg_po}"
            
            st.session_state['po_last_file'] = html_po_bytes
            st.session_state['po_last_filename'] = f"{po_ref_no}_{selected_party_name}.html"
            st.session_state['po_last_wa'] = wa_po_link
            st.session_state['po_last_client'] = selected_party_name

        if 'po_last_file' in st.session_state:
            st.markdown("---")
            st.write(f"**Actions for latest PO: {st.session_state['po_last_client']}**")
            
            st.download_button(
                label="🌐 Download / Print HTML Purchase Order",
                data=st.session_state['po_last_file'],
                file_name=st.session_state['po_last_filename'],
                mime="text/html"
            )
            
            if st.session_state['po_last_wa']:
                st.markdown(f"[📱 Send WhatsApp Message to Vendor]({st.session_state['po_last_wa']})")

    elif menu == "Quotation Records":
        st.title("Quotation History")
        
        response = supabase.table("quotations").select("*").order("created_at", desc=True).execute()
        records = response.data
        
        if records:
            for record in records:
                record_date = record['created_at'][:10] if record.get('created_at') else "Unknown Date"
                ref_no = f"BBSP-{record['id'][:6].upper()}"
                
                with st.expander(f"{record_date} | {ref_no} | {record['client_name']} - Rs.{record['total_amount']:,.2f}"):
                    st.write(f"**Quantity:** {record['quantity_mt']} MT | **Rate:** Rs.{record['rate_per_mt']}/MT")
                    st.write(f"**Issued By:** {record['issued_by']}")
                    
                    col_a, col_b = st.columns(2)
                    
                    html_bytes = create_html_quotation(
                        record['client_name'], 
                        record.get('client_mobile', ''),
                        record.get('client_address', ''),
                        record_date, 
                        record['quantity_mt'], 
                        record['rate_per_mt'], 
                        record['transportation_cost'], 
                        record['tax_type'], 
                        record['total_amount'],
                        ref_no
                    )
                    col_a.download_button(
                        label="🌐 Reprint / Print HTML",
                        data=html_bytes,
                        file_name=f"{ref_no}_{record['client_name']}_Reprint.html",
                        mime="text/html",
                        key=f"dl_{record['id']}"
                    )
                    
                    if st.session_state['user_role'] == "Admin":
                        if col_b.button("🗑️ Delete Record", key=f"del_{record['id']}"):
                            supabase.table("quotations").delete().eq("id", record['id']).execute()
                            st.success("Record deleted. Please refresh the page.")
                            st.rerun()
        else:
            st.info("No quotation records found.")

    elif menu == "Purchase Order Records":
        st.title("Purchase Order History (Reprint & WhatsApp)")
        
        try:
            po_response = supabase.table("purchase_orders").select("*").order("created_at", desc=True).execute()
            po_records = po_response.data
        except Exception:
            po_records = []
            
        if po_records:
            for record in po_records:
                record_date = record['created_at'][:10] if record.get('created_at') else "Unknown Date"
                po_ref_no = f"BBSP-PO-{record['id'][:6].upper()}"
                
                with st.expander(f"{record_date} | {po_ref_no} | {record['supplier_name']} - Rs.{record['total_amount']:,.2f}"):
                    st.write(f"**Quantity:** {record['quantity_mt']} MT | **Rate:** Rs.{record['rate_per_mt']}/MT")
                    st.write(f"**GSTIN:** {record.get('supplier_gst', 'N/A')} | **Issued By:** {record.get('issued_by', 'Staff')}")
                    
                    col_a, col_b = st.columns(2)
                    
                    po_html_bytes = create_html_purchase_order(
                        record['supplier_name'],
                        record.get('supplier_mobile', ''),
                        record.get('supplier_gst', ''),
                        record.get('supplier_address', ''),
                        record_date,
                        record['quantity_mt'],
                        record['rate_per_mt'],
                        record['transportation_cost'],
                        record['tax_type'],
                        record['total_amount'],
                        po_ref_no
                    )
                    
                    col_a.download_button(
                        label="🌐 Reprint / Print PO",
                        data=po_html_bytes,
                        file_name=f"{po_ref_no}_{record['supplier_name']}_Reprint.html",
                        mime="text/html",
                        key=f"po_dl_{record['id']}"
                    )
                    
                    sup_mobile = record.get('supplier_mobile', '')
                    if sup_mobile:
                        hist_msg = urllib.parse.quote(f"Hello {record['supplier_name']}, regarding Purchase Order ({po_ref_no}) for {record['quantity_mt']}MT of Biomass Feedstock amounting to Rs. {record['total_amount']:,.2f}.")
                        hist_wa_link = f"https://wa.me/{sup_mobile}?text={hist_msg}"
                        st.markdown(f"[📱 Send WhatsApp Message to Vendor]({hist_wa_link})")
                    
                    if st.session_state['user_role'] == "Admin":
                        if col_b.button("🗑️ Delete PO Record", key=f"po_del_{record['id']}"):
                            supabase.table("purchase_orders").delete().eq("id", record['id']).execute()
                            st.success("Record deleted. Please refresh the page.")
                            st.rerun()
        else:
            st.info("No purchase order records found.")
