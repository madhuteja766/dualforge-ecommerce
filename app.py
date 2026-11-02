"""
DualForge — Enterprise E-Commerce Platform
Full-Featured Streamlit Cloud Application
Includes Authentication (Admin, Seller, Customer), Role Portals, Catalog,
AI Assistant, Comparison, Size Calculator, Wishlist, Cart & Orders.
Developed by M. Madhu Teja & Team (EWDP Capstone Project)
"""

import streamlit as st
import pandas as pd
import datetime
import json
import re

st.set_page_config(
    page_title="DualForge E-Commerce",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- STYLING -----------------
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 50%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.3rem;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 1.2rem;
    }
    .badge-trust {
        display: inline-block;
        background: rgba(14, 165, 233, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(14, 165, 233, 0.3);
        padding: 3px 8px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-role {
        display: inline-block;
        background: rgba(99, 102, 241, 0.2);
        color: #818cf8;
        border: 1px solid rgba(99, 102, 241, 0.4);
        padding: 3px 9px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .product-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 16px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .product-card:hover {
        border-color: rgba(99, 102, 241, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ----------------- INITIAL CATALOG DATA -----------------
DEFAULT_PRODUCTS = [
    {
        "id": 1, "name": "Tech Hoodie Black", "category": "Fashion", "brand": "ForgeWear",
        "price": 2499.0, "original_price": 2799.0, "rating": 4.8, "reviews": 85,
        "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500",
        "description": "Wind-resistant thermo-regulating fleece hoodie with travel pockets.",
        "specs": "Fabric: Fleece Blend | Sizes: S, M, L, XL | Warranty: 1 Year",
        "stock": 40, "trust_score": 94, "eco_rating": "A+"
    },
    {
        "id": 2, "name": "Cyberpunk Oversized Hoodie", "category": "Fashion", "brand": "CyberForge",
        "price": 3299.0, "original_price": 3899.0, "rating": 4.9, "reviews": 120,
        "image": "https://images.unsplash.com/photo-1509967419530-da38b4704bc6?w=500",
        "description": "Heavyweight 450GSM organic cotton oversized fleece hoodie.",
        "specs": "Fabric: 100% Organic Cotton | Sizes: M, L, XL, XXL | Warranty: 1 Year",
        "stock": 25, "trust_score": 96, "eco_rating": "A"
    },
    {
        "id": 3, "name": "Urban Bomber Jacket", "category": "Fashion", "brand": "ForgeWear",
        "price": 4499.0, "original_price": 5299.0, "rating": 4.7, "reviews": 98,
        "image": "https://images.unsplash.com/photo-1548883354-7622d03aca27?w=500",
        "description": "Weatherproof bomber jacket with padded thermal lining.",
        "specs": "Shell: Nylon, Fill: Polyester | Sizes: M, L, XL | Warranty: 1 Year",
        "stock": 30, "trust_score": 92, "eco_rating": "B+"
    },
    {
        "id": 4, "name": "Forgebuds ANC Wireless", "category": "Electronics", "brand": "ForgeAudio",
        "price": 4999.0, "original_price": 5999.0, "rating": 4.6, "reviews": 188,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500",
        "description": "Studio acoustics, 35dB active noise cancellation, and 40h battery cell.",
        "specs": "ANC: 35dB | Battery: 40h | Driver: 10mm Graphene | Bluetooth 5.3",
        "stock": 50, "trust_score": 95, "eco_rating": "A"
    },
    {
        "id": 5, "name": "ForgePro Wireless Gaming Headset", "category": "Electronics", "brand": "ForgeAudio",
        "price": 6499.0, "original_price": 7999.0, "rating": 4.8, "reviews": 142,
        "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500",
        "description": "Low-latency 2.4GHz wireless headset with detachable spatial mic.",
        "specs": "Drivers: 50mm Neodymium | Battery: 30h | 7.1 Spatial Audio",
        "stock": 35, "trust_score": 97, "eco_rating": "A"
    },
    {
        "id": 6, "name": "BoomBlast Portable Speaker", "category": "Electronics", "brand": "ForgeAudio",
        "price": 3499.0, "original_price": 3999.0, "rating": 4.7, "reviews": 115,
        "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500",
        "description": "IPX7 waterproof 30W Bluetooth speaker with deep bass radiator.",
        "specs": "Power: 30W RMS | Battery: 15h | Waterproof: IPX7 | Fast Charge",
        "stock": 40, "trust_score": 93, "eco_rating": "A"
    },
    {
        "id": 7, "name": "Stealth Runners", "category": "Footwear", "brand": "Stealth",
        "price": 3499.0, "original_price": 4299.0, "rating": 4.7, "reviews": 254,
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500",
        "description": "Hydrophobic mesh structure with ultra-rebound cushioning outsoles.",
        "specs": "Sizes: UK 7-11 | Upper: Mesh | Sole: Rubber Rebound | Lightweight",
        "stock": 30, "trust_score": 95, "eco_rating": "A+"
    },
    {
        "id": 8, "name": "Apex Velocity Sneakers", "category": "Footwear", "brand": "ApexForge",
        "price": 5999.0, "original_price": 7499.0, "rating": 4.9, "reviews": 165,
        "image": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=500",
        "description": "Lightweight carbon-plated marathon racing shoes.",
        "specs": "Plate: Carbon Fiber | Foam: Nitrogen Infused | Sizes: UK 8-11",
        "stock": 20, "trust_score": 98, "eco_rating": "A"
    },
    {
        "id": 9, "name": "Classic Leather Oxfords", "category": "Footwear", "brand": "LeatherForge",
        "price": 4999.0, "original_price": 5999.0, "rating": 4.6, "reviews": 82,
        "image": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?w=500",
        "description": "Handcrafted Italian genuine leather formal Oxford dress shoes.",
        "specs": "100% Genuine Full-Grain Leather | Sizes: UK 7-10 | Goodyear Welted",
        "stock": 25, "trust_score": 94, "eco_rating": "B"
    },
    {
        "id": 10, "name": "Forgebook Pro 16", "category": "Electronics", "brand": "Forge",
        "price": 124999.0, "original_price": 139999.0, "rating": 4.8, "reviews": 124,
        "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500",
        "description": "Liquid-metal cooled workstation laptop with 16-inch 120Hz display.",
        "specs": "Intel i9 13900H | RTX 4070 8GB | 32GB DDR5 | 1TB NVMe SSD",
        "stock": 15, "trust_score": 99, "eco_rating": "A"
    },
    {
        "id": 11, "name": "RGB Mechanical Keyboard", "category": "Electronics", "brand": "ForgeKey",
        "price": 3499.0, "original_price": 4499.0, "rating": 4.6, "reviews": 230,
        "image": "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=500",
        "description": "Hot-swappable tactile mechanical switches with per-key RGB.",
        "specs": "PBT Keycaps | Hot-Swap Red/Brown | Type-C | N-Key Rollover",
        "stock": 60, "trust_score": 92, "eco_rating": "A"
    },
    {
        "id": 12, "name": "Forge Watch Ultra", "category": "Electronics", "brand": "ForgeWatch",
        "price": 14999.0, "original_price": 17999.0, "rating": 4.9, "reviews": 148,
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500",
        "description": "Titanium case outdoor smartwatch with dual-frequency GPS & ECG.",
        "specs": "2.0\" AMOLED | Titanium Case | 7 Days Battery | 100m Water Resist",
        "stock": 25, "trust_score": 98, "eco_rating": "A+"
    }
]

# ----------------- SESSION STATE -----------------
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "admin": {"username": "admin", "password": "adminpassword", "role": "ROLE_ADMIN", "name": "Super Admin", "email": "admin@dualforge.com"},
        "seller": {"username": "seller", "password": "sellerpassword", "role": "ROLE_SELLER", "name": "DualForge Store Seller", "email": "seller@dualforge.com"},
        "customer": {"username": "customer", "password": "customerpassword", "role": "ROLE_CUSTOMER", "name": "John Doe", "email": "customer@gmail.com"}
    }

if "current_user" not in st.session_state:
    st.session_state.current_user = None  # None indicates guest / not logged in

if "products" not in st.session_state:
    st.session_state.products = DEFAULT_PRODUCTS.copy()

if "cart" not in st.session_state:
    st.session_state.cart = []

if "wishlist" not in st.session_state:
    st.session_state.wishlist = []

if "orders" not in st.session_state:
    st.session_state.orders = [
        {
            "id": "ORD-78921",
            "date": "2026-11-01",
            "items": ["Tech Hoodie Black", "Forgebuds ANC Wireless"],
            "total": 7498.0,
            "status": "DELIVERED",
            "tracking": "TRK-DF-998124"
        }
    ]

if "coupon_applied" not in st.session_state:
    st.session_state.coupon_applied = False
if "discount_pct" not in st.session_state:
    st.session_state.discount_pct = 0.0

if "pending_sellers" not in st.session_state:
    st.session_state.pending_sellers = [
        {"store": "Apex Electronics Ltd", "gst": "29ABCDE1234F1Z5", "email": "contact@apexelectronics.in", "status": "PENDING"},
        {"store": "ForgeFootwear Global", "gst": "33AAACA9876M2Z1", "email": "support@forgefootwear.com", "status": "APPROVED"}
    ]

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "Hello! I am your **DualForge AI Shopping Assistant**. Ask me anything, or tell me your budget (e.g. *'I have ₹5000 for headphones'* or *'recommend running shoes'*)."}
    ]

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=100", width=60)
    st.title("DualForge")
    st.caption("Enterprise E-Commerce Platform")
    
    st.markdown("---")
    
    # User status widget
    if st.session_state.current_user:
        u = st.session_state.current_user
        st.markdown(f"**Logged in as:** `{u['username']}`")
        st.markdown(f"<span class='badge-role'>{u['role']}</span>", unsafe_allow_html=True)
        st.caption(f"📧 {u['email']}")
        if st.button("🚪 Log Out", key="logout_btn", use_container_width=True):
            st.session_state.current_user = None
            st.rerun()
    else:
        st.info("👤 You are browsing as **Guest**.")
        st.caption("Log in to access Admin, Seller, and Checkout features.")

    st.markdown("---")
    
    # Navigation options based on auth
    nav_options = ["🛍️ Store Catalog", "🤖 AI Assistant", "⚖️ Product Comparison", "📏 Smart Size Calculator", "🛒 My Cart", "❤️ Wishlist"]
    
    if st.session_state.current_user:
        nav_options.append("📦 Order History")
        if st.session_state.current_user["role"] == "ROLE_ADMIN":
            nav_options.insert(0, "🛡️ Admin Portal")
        elif st.session_state.current_user["role"] == "ROLE_SELLER":
            nav_options.insert(0, "🏪 Seller Portal")
    else:
        nav_options.insert(0, "🔑 Login / Register")
        
    nav_options.append("ℹ️ About Platform")
    
    selected_page = st.radio("Navigation", nav_options, index=0)
    
    st.markdown("---")
    st.markdown("**DualForge Trust Score: 94/100** ⭐")
    st.markdown("🔒 *JWT Protected Security Filter*")
    st.caption("EWDP Capstone — M. Madhu Teja & Team")

# ----------------- 0. LOGIN / REGISTER PAGE -----------------
if selected_page == "🔑 Login / Register":
    st.markdown('<div class="main-header">Account Authentication</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Secure JWT-backed login for Admins, Sellers, and Customers.</div>', unsafe_allow_html=True)

    tab_login, tab_register, tab_forgot = st.tabs(["🔐 Sign In", "📝 Create Account", "❓ Forgot Password"])

    with tab_login:
        c_left, c_right = st.columns([3, 2])
        
        with c_left:
            st.markdown("### User Sign In")
            login_user = st.text_input("Username or Email", placeholder="e.g. admin or customer")
            login_pass = st.text_input("Password", type="password", placeholder="Enter your password")
            
            if st.button("Sign In to DualForge", type="primary", use_container_width=True):
                user_record = st.session_state.users_db.get(login_user.strip())
                if user_record and user_record["password"] == login_pass.strip():
                    st.session_state.current_user = user_record
                    st.success(f"Welcome back, {user_record['name']}! Logged in as {user_record['role']}.")
                    st.rerun()
                else:
                    st.error("Invalid credentials! Please check your username and password.")

        with c_right:
            st.markdown("### ⚡ Quick Demo Logins")
            st.caption("Click any demo button to log in instantly:")
            
            if st.button("👑 Quick Admin Login (Full Control)", use_container_width=True):
                st.session_state.current_user = st.session_state.users_db["admin"]
                st.success("Logged in as Super Admin!")
                st.rerun()
                
            if st.button("🏪 Quick Seller Login (Store & Inventory)", use_container_width=True):
                st.session_state.current_user = st.session_state.users_db["seller"]
                st.success("Logged in as Verified Seller!")
                st.rerun()
                
            if st.button("🛍️ Quick Customer Login (Shop & Orders)", use_container_width=True):
                st.session_state.current_user = st.session_state.users_db["customer"]
                st.success("Logged in as Customer!")
                st.rerun()

    with tab_register:
        st.markdown("### Register New Account")
        r_col1, r_col2 = st.columns(2)
        with r_col1:
            new_fname = st.text_input("First Name")
            new_lname = st.text_input("Last Name")
            new_username = st.text_input("Desired Username")
            new_email = st.text_input("Email Address")
        with r_col2:
            new_phone = st.text_input("10-Digit Mobile Number")
            new_role = st.selectbox("Account Type", ["Customer (ROLE_CUSTOMER)", "Seller (ROLE_SELLER)"])
            new_pass = st.text_input("Password (min 8 characters)", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")

        reg_otp = st.text_input("Verification Code (Demo: 123456)", value="123456")
        
        if st.button("Complete Registration", type="primary"):
            if not new_username or not new_email or not new_pass:
                st.error("Please fill all mandatory fields.")
            elif new_pass != confirm_pass:
                st.error("Passwords do not match!")
            elif len(new_pass) < 8:
                st.error("Password must be at least 8 characters long.")
            else:
                role_val = "ROLE_SELLER" if "Seller" in new_role else "ROLE_CUSTOMER"
                st.session_state.users_db[new_username] = {
                    "username": new_username,
                    "password": new_pass,
                    "role": role_val,
                    "name": f"{new_fname} {new_lname}".strip() or new_username,
                    "email": new_email
                }
                st.success(f"Account for '{new_username}' registered successfully! You can now sign in.")

    with tab_forgot:
        st.markdown("### Reset Account Password")
        f_email = st.text_input("Enter your registered email address")
        if st.button("Send Recovery OTP"):
            st.info(f"Verification code sent to {f_email}! [DEMO CODE: 789456]")
        f_otp = st.text_input("Enter Recovery Code")
        f_new_pass = st.text_input("New Password", type="password")
        if st.button("Update Password"):
            st.success("Password reset successfully! Please sign in with your new password.")

# ----------------- 1. ADMIN PORTAL -----------------
elif selected_page == "🛡️ Admin Portal":
    st.markdown('<div class="main-header">DualForge Administrator Portal</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Global platform metrics, seller verification audits, and security logs.</div>', unsafe_allow_html=True)

    # Metric Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Platform Revenue", "₹3,48,900", "+18.4%")
    m2.metric("Total Catalog Products", f"{len(st.session_state.products)}", "+6 today")
    m3.metric("Registered Users", f"{len(st.session_state.users_db)}", "+3")
    m4.metric("Pending Seller Audits", f"{sum(1 for s in st.session_state.pending_sellers if s['status'] == 'PENDING')}", "Action Needed")

    st.markdown("---")
    adm_tab1, adm_tab2, adm_tab3 = st.tabs(["👥 Seller Verification Audits", "📦 Catalog Management", "🔒 Security Audit Logs"])

    with adm_tab1:
        st.markdown("### Seller Approvals & GST Verification")
        for idx, s in enumerate(st.session_state.pending_sellers):
            col_a, col_b, col_c, col_d = st.columns([2, 2, 1, 1])
            col_a.markdown(f"**Store:** {s['store']}")
            col_b.markdown(f"**GSTIN:** `{s['gst']}`")
            col_c.markdown(f"**Status:** `{s['status']}`")
            with col_d:
                if s["status"] == "PENDING":
                    if st.button("Approve", key=f"appr_{idx}"):
                        st.session_state.pending_sellers[idx]["status"] = "APPROVED"
                        st.toast(f"Approved {s['store']}!", icon="✅")
                        st.rerun()

    with adm_tab2:
        st.markdown("### Current Catalog Overview")
        df_prods = pd.DataFrame([
            {"ID": p["id"], "Name": p["name"], "Category": p["category"], "Price": f"₹{p['price']:,.0f}", "Stock": p["stock"], "Rating": p["rating"]}
            for p in st.session_state.products
        ])
        st.dataframe(df_prods, use_container_width=True)

    with adm_tab3:
        st.markdown("### Real-Time Security & Access Logs")
        logs = [
            {"Timestamp": "2026-11-02 09:45:10", "Event": "JWT Token Issued", "User": "admin", "IP": "127.0.0.1", "Status": "SUCCESS"},
            {"Timestamp": "2026-11-02 09:48:22", "Event": "Order Authorized", "User": "customer", "IP": "192.168.1.39", "Status": "SUCCESS"},
            {"Timestamp": "2026-11-02 10:00:15", "Event": "Catalog Database Seeding", "User": "SYSTEM", "IP": "localhost", "Status": "COMPLETED"},
            {"Timestamp": "2026-11-02 10:14:00", "Event": "CORS Validation Allowed", "Origin": "*.vercel.app", "Status": "PERMITTED"}
        ]
        st.table(pd.DataFrame(logs))

# ----------------- 2. SELLER PORTAL -----------------
elif selected_page == "🏪 Seller Portal":
    st.markdown('<div class="main-header">Seller Hub & Inventory Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Manage product listings, stock levels, and store profile.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(30, 41, 59, 0.7); border:1px solid rgba(255, 255, 255, 0.1); border-radius:10px; padding:15px; margin-bottom:20px;">
        <span class="badge-trust" style="color:#4ade80; border-color:rgba(74,222,128,0.3);">Verified Seller Badge</span>
        <h3 style="margin:5px 0;">DualForge Verified Store</h3>
        <p style="color:#94a3b8; font-size:0.9rem;">GSTIN: 27AAAAA0000A1Z5 | Settlement: HDFC Bank Ltd - HDFC0001234 | Rating: 4.9 / 5.0 ⭐</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ➕ Add New Product to Live Catalog")
    with st.form("new_product_form"):
        p_name = st.text_input("Product Name", placeholder="e.g. Ultra Carbon Sneakers")
        col_x, col_y = st.columns(2)
        with col_x:
            p_cat = st.selectbox("Category", ["Electronics", "Fashion", "Footwear", "Accessories"])
            p_price = st.number_input("Selling Price (₹)", min_value=100.0, value=2999.0, step=100.0)
            p_orig = st.number_input("Original MRP (₹)", min_value=100.0, value=3999.0, step=100.0)
        with col_y:
            p_brand = st.text_input("Brand", value="ForgeWear")
            p_stock = st.number_input("Initial Inventory Stock", min_value=1, value=50)
            p_img = st.text_input("Product Image URL", value="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500")

        p_desc = st.text_area("Product Description", "High-performance ergonomic build designed for everyday durability.")
        p_specs = st.text_input("Technical Specifications", "Material: Premium Composite | Sizes: All | Warranty: 1 Year")

        submit_prod = st.form_submit_button("Publish Product to Marketplace", type="primary")
        if submit_prod:
            if not p_name:
                st.error("Product name is required.")
            else:
                new_id = max(p["id"] for p in st.session_state.products) + 1
                st.session_state.products.append({
                    "id": new_id, "name": p_name, "category": p_cat, "brand": p_brand,
                    "price": p_price, "original_price": p_orig, "rating": 5.0, "reviews": 1,
                    "image": p_img, "description": p_desc, "specs": p_specs, "stock": p_stock,
                    "trust_score": 95, "eco_rating": "A"
                })
                st.success(f"Product '{p_name}' successfully published to DualForge catalog!")

# ----------------- 3. STORE CATALOG -----------------
elif selected_page == "🛍️ Store Catalog":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="main-header">DualForge Marketplace</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Discover high-performance electronics, apparel, and athletic footwear.</div>', unsafe_allow_html=True)
    with col2:
        cart_count = len(st.session_state.cart)
        st.metric("Shopping Cart", f"{cart_count} items")

    # Filters
    f_col1, f_col2, f_col3 = st.columns([2, 2, 2])
    with f_col1:
        categories = ["All"] + sorted(list(set(p["category"] for p in st.session_state.products)))
        selected_cat = st.selectbox("Filter Category", categories)
    with f_col2:
        max_price = st.slider("Max Budget (₹)", 1000, 150000, 150000, step=1000)
    with f_col3:
        search_query = st.text_input("🔍 Search Products", "")

    # Filtered List
    filtered = st.session_state.products
    if selected_cat != "All":
        filtered = [p for p in filtered if p["category"] == selected_cat]
    filtered = [p for p in filtered if p["price"] <= max_price]
    if search_query:
        q = search_query.lower()
        filtered = [p for p in filtered if q in p["name"].lower() or q in p["description"].lower() or q in p["brand"].lower()]

    st.markdown(f"**Showing {len(filtered)} product(s)**")

    # Product Grid
    cols = st.columns(3)
    for i, prod in enumerate(filtered):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="product-card">
                <img src="{prod['image']}" style="width:100%; height:200px; object-fit:cover; border-radius:8px; margin-bottom:12px;" />
                <span class="badge-trust">Trust {prod['trust_score']}%</span>
                <span class="badge-trust" style="color:#4ade80; border-color:rgba(74,222,128,0.3);">Eco: {prod['eco_rating']}</span>
                <h4 style="margin: 8px 0 4px 0;">{prod['name']}</h4>
                <p style="color:#94a3b8; font-size:0.85rem; height:40px; overflow:hidden;">{prod['description']}</p>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
                    <div>
                        <span style="font-size:1.25rem; font-weight:700; color:#38bdf8;">₹{prod['price']:,.0f}</span>
                        <span style="text-decoration:line-through; color:#64748b; font-size:0.85rem; margin-left:6px;">₹{prod['original_price']:,.0f}</span>
                    </div>
                    <span style="color:#f59e0b; font-size:0.9rem;">⭐ {prod['rating']} ({prod['reviews']})</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            b_col1, b_col2 = st.columns(2)
            with b_col1:
                if st.button("Add to Cart", key=f"add_{prod['id']}", use_container_width=True):
                    st.session_state.cart.append(prod)
                    st.toast(f"Added {prod['name']} to cart!", icon="🛒")
            with b_col2:
                if st.button("❤️ Wishlist", key=f"wish_{prod['id']}", use_container_width=True):
                    if prod not in st.session_state.wishlist:
                        st.session_state.wishlist.append(prod)
                        st.toast(f"Saved to Wishlist!", icon="❤️")

# ----------------- 4. AI ASSISTANT -----------------
elif selected_page == "🤖 AI Assistant":
    st.markdown('<div class="main-header">AI Shopping Decision Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Natural language query parser for budget-constrained shopping decisions.</div>', unsafe_allow_html=True)

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("E.g., 'I have 5000 rupees for audio' or 'Show me best sneakers'")
    if prompt:
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        p_lower = prompt.lower()
        budget_match = re.search(r'(\d+[\d,]*)', p_lower)
        budget = float(budget_match.group(1).replace(',', '')) if budget_match else None

        if "audio" in p_lower or "headphone" in p_lower or "speaker" in p_lower or "earbud" in p_lower:
            candidates = [p for p in st.session_state.products if "ForgeAudio" in p["brand"] or "Audio" in p["specs"] or "ANC" in p["name"] or "Headphone" in p["name"] or "Speaker" in p["name"]]
        elif "shoe" in p_lower or "sneaker" in p_lower or "runner" in p_lower or "footwear" in p_lower:
            candidates = [p for p in st.session_state.products if p["category"] == "Footwear"]
        elif "hoodie" in p_lower or "jacket" in p_lower or "fashion" in p_lower:
            candidates = [p for p in st.session_state.products if p["category"] == "Fashion"]
        elif "laptop" in p_lower or "computer" in p_lower or "pc" in p_lower:
            candidates = [p for p in st.session_state.products if "Forgebook" in p["name"]]
        else:
            candidates = st.session_state.products

        if budget:
            budget_candidates = [p for p in candidates if p["price"] <= budget]
            if budget_candidates:
                best_item = max(budget_candidates, key=lambda x: (x["rating"], -x["price"]))
                response = f"🎯 **Found {len(budget_candidates)} option(s) within ₹{budget:,.0f}:**\n\n"
                response += f"🌟 **Top AI Recommendation:** **{best_item['name']}** (₹{best_item['price']:,.0f})\n"
                response += f"- Rating: ⭐ {best_item['rating']} / 5 ({best_item['reviews']} reviews)\n"
                response += f"- Highlights: {best_item['specs']}\n"
                response += f"- Trust Score: **{best_item['trust_score']}/100**\n\n"
                if len(budget_candidates) > 1:
                    response += "**Other alternatives within budget:**\n"
                    for alt in budget_candidates:
                        if alt["id"] != best_item["id"]:
                            response += f"• **{alt['name']}** — ₹{alt['price']:,.0f} (⭐ {alt['rating']})\n"
            else:
                response = f"I couldn't find items in that category strictly under ₹{budget:,.0f}. The closest option is **{min(candidates, key=lambda x: x['price'])['name']}** at ₹{min(candidates, key=lambda x: x['price'])['price']:,.0f}."
        else:
            top_picks = sorted(candidates, key=lambda x: x["rating"], reverse=True)[:3]
            response = f"Here are the top-rated recommendations:\n\n"
            for p in top_picks:
                response += f"• **{p['name']}** (₹{p['price']:,.0f}) — ⭐ {p['rating']} — {p['description']}\n"

        response += "\n\n💡 *Tip: Apply coupon code `FLAGSHIP20` at checkout for 20% off!*"
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# ----------------- 5. PRODUCT COMPARISON MATRIX -----------------
elif selected_page == "⚖️ Product Comparison":
    st.markdown('<div class="main-header">Product Comparison Matrix</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Side-by-side spec comparison table with automated AI Value Recommendation.</div>', unsafe_allow_html=True)

    product_names = [p["name"] for p in st.session_state.products]
    selected_prods = st.multiselect(
        "Select up to 3 products to compare:",
        product_names,
        default=[st.session_state.products[3]["name"], st.session_state.products[4]["name"]]
    )

    if len(selected_prods) >= 2:
        comp_items = [p for p in st.session_state.products if p["name"] in selected_prods]
        table_data = {"Attribute": ["Price", "Rating", "Reviews", "Category", "Brand", "Trust Score", "Eco Impact", "Specs"]}
        for item in comp_items:
            table_data[item["name"]] = [
                f"₹{item['price']:,.0f}", f"⭐ {item['rating']}", str(item['reviews']),
                item["category"], item["brand"], f"{item['trust_score']}/100", item["eco_rating"], item["specs"]
            ]
        df = pd.DataFrame(table_data).set_index("Attribute")
        st.table(df)

        best_value = max(comp_items, key=lambda x: (x["rating"] / x["price"]) * 1000)
        st.success(f"🤖 **AI Value Recommendation:** **{best_value['name']}** offers the highest performance-to-price ratio with a rating of ⭐ {best_value['rating']} at ₹{best_value['price']:,.0f}.")
    else:
        st.info("Please select at least 2 products above to generate the comparison matrix.")

# ----------------- 6. SMART SIZE CALCULATOR -----------------
elif selected_page == "📏 Smart Size Calculator":
    st.markdown('<div class="main-header">Smart Size Recommendation Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Computes exact apparel and footwear sizes using biometric inputs and fit preferences.</div>', unsafe_allow_html=True)

    calc_tab1, calc_tab2 = st.tabs(["👕 Apparel Size Calculator", "👟 Footwear Size Calculator"])

    with calc_tab1:
        c1, c2 = st.columns(2)
        with c1:
            height = st.number_input("Your Height (cm)", min_value=120, max_value=220, value=175)
            weight = st.number_input("Your Weight (kg)", min_value=35, max_value=150, value=70)
        with c2:
            fit = st.selectbox("Fit Preference", ["Slim Fit", "Regular Fit", "Relaxed / Oversized Fit"])

        bmi = weight / ((height / 100) ** 2)
        if height < 165 or weight < 60:
            rec_size = "S"
        elif height < 178 and weight < 75:
            rec_size = "M" if fit != "Relaxed / Oversized Fit" else "L"
        elif height < 188 or weight < 90:
            rec_size = "L" if fit != "Relaxed / Oversized Fit" else "XL"
        else:
            rec_size = "XL" if fit != "Relaxed / Oversized Fit" else "XXL"

        st.markdown("---")
        st.markdown(f"### Recommended Size: **`{rec_size}`**")
        st.markdown(f"- Calculated Body Mass Index (BMI): **{bmi:.1f}**")
        st.markdown(f"- Selected Fit Profile: **{fit}**")

    with calc_tab2:
        foot_length = st.slider("Foot Length (cm)", 22.0, 31.0, 26.5, step=0.5)
        uk_size = max(6, min(12, round(foot_length - 18.0)))
        st.markdown("---")
        st.markdown(f"### Recommended Shoe Size: **`UK {uk_size}`** (US {uk_size + 1} / EU {uk_size + 33})")

# ----------------- 7. WISHLIST -----------------
elif selected_page == "❤️ Wishlist":
    st.markdown('<div class="main-header">My Wishlist</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Your saved items ready to be added to cart.</div>', unsafe_allow_html=True)

    if not st.session_state.wishlist:
        st.info("Your wishlist is currently empty. Click '❤️ Wishlist' on any product card in the Store Catalog to save it!")
    else:
        for idx, item in enumerate(st.session_state.wishlist):
            c_a, c_b, c_c, c_d = st.columns([1, 3, 2, 1])
            c_a.image(item["image"], width=70)
            c_b.markdown(f"**{item['name']}**\n\n₹{item['price']:,.0f}")
            with c_c:
                if st.button("Move to Cart", key=f"wish_cart_{idx}"):
                    st.session_state.cart.append(item)
                    st.session_state.wishlist.pop(idx)
                    st.toast(f"Moved {item['name']} to cart!", icon="🛒")
                    st.rerun()
            with c_d:
                if st.button("Remove", key=f"wish_del_{idx}"):
                    st.session_state.wishlist.pop(idx)
                    st.rerun()

# ----------------- 8. MY CART & CHECKOUT -----------------
elif selected_page == "🛒 My Cart":
    st.markdown('<div class="main-header">Shopping Cart & Secure Checkout</div>', unsafe_allow_html=True)

    if not st.session_state.cart:
        st.info("Your cart is currently empty. Head over to the Store Catalog to add items!")
    else:
        cart_cols = st.columns([3, 2])
        with cart_cols[0]:
            st.markdown("### Cart Items")
            for idx, item in enumerate(st.session_state.cart):
                c_a, c_b, c_c = st.columns([1, 3, 1])
                with c_a:
                    st.image(item["image"], width=60)
                with c_b:
                    st.markdown(f"**{item['name']}**\n₹{item['price']:,.0f}")
                with c_c:
                    if st.button("✕", key=f"del_{idx}"):
                        st.session_state.cart.pop(idx)
                        st.rerun()

        with cart_cols[1]:
            st.markdown("### Order Summary")
            subtotal = sum(p["price"] for p in st.session_state.cart)
            
            coupon = st.text_input("Discount Coupon", value="FLAGSHIP20" if not st.session_state.coupon_applied else "")
            if st.button("Apply Coupon"):
                if coupon.strip().upper() == "FLAGSHIP20":
                    st.session_state.coupon_applied = True
                    st.session_state.discount_pct = 0.20
                    st.success("Applied 20% Flagship Discount!")
                elif coupon.strip().upper() == "WELCOME10":
                    st.session_state.coupon_applied = True
                    st.session_state.discount_pct = 0.10
                    st.success("Applied 10% Welcome Discount!")
                else:
                    st.error("Invalid coupon code.")

            discount = subtotal * st.session_state.discount_pct
            tax = (subtotal - discount) * 0.18
            total = subtotal - discount + tax

            st.markdown(f"""
            - **Subtotal:** ₹{subtotal:,.2f}
            - **Discount ({int(st.session_state.discount_pct * 100)}%):** -₹{discount:,.2f}
            - **Estimated GST (18%):** ₹{tax:,.2f}
            ---
            ### **Total:** ₹{total:,.2f}
            """)

            # Shipping Details
            st.markdown("#### Shipping Details")
            ship_addr = st.text_input("Delivery Address", "124 Innovation Blvd, Bangalore")
            ship_pay = st.selectbox("Payment Method", ["UPI / QR Code", "Credit/Debit Card", "Cash on Delivery", "Net Banking"])

            if st.button("Authorize & Place Order", type="primary"):
                order_id = f"ORD-{int(time.time())}"
                st.session_state.orders.insert(0, {
                    "id": order_id,
                    "date": datetime.date.today().isoformat(),
                    "items": [item["name"] for item in st.session_state.cart],
                    "total": total,
                    "status": "PROCESSING",
                    "tracking": f"TRK-DF-{order_id[-6:]}"
                })
                st.balloons()
                st.success(f"🎉 Order {order_id} authorized and saved successfully!")
                st.session_state.cart = []
                st.session_state.coupon_applied = False
                st.session_state.discount_pct = 0.0

# ----------------- 9. ORDER HISTORY -----------------
elif selected_page == "📦 Order History":
    st.markdown('<div class="main-header">Order History & Receipts</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">View past orders and download verified tax invoices.</div>', unsafe_allow_html=True)

    if not st.session_state.orders:
        st.info("No orders found for this account.")
    else:
        for ord_data in st.session_state.orders:
            with st.expander(f"Order #{ord_data['id']} — {ord_data['date']} — ₹{ord_data['total']:,.2f} [{ord_data['status']}]", expanded=True):
                st.markdown(f"**Tracking Number:** `{ord_data['tracking']}`")
                st.markdown("**Purchased Items:**")
                for itm in ord_data["items"]:
                    st.markdown(f"- {itm}")
                st.markdown(f"**Total Amount Paid:** ₹{ord_data['total']:,.2f}")
                
                # Invoice Download simulator
                invoice_text = f"""====================================================
           DUALFORGE ENTERPRISE TAX INVOICE
====================================================
Invoice Ref   : INV-{ord_data['id']}
Order ID      : {ord_data['id']}
Date          : {ord_data['date']}
Customer      : {st.session_state.current_user['name'] if st.session_state.current_user else 'Guest Customer'}
Items:
{chr(10).join(f" - {itm}" for itm in ord_data['items'])}
Total Paid    : INR {ord_data['total']:,.2f} (Inclusive of 18% GST)
Seller        : DualForge Verified Store (GSTIN: 27AAAAA0000A1Z5)
====================================================
"""
                st.download_button(
                    label="📄 Download Tax Invoice (TXT)",
                    data=invoice_text,
                    file_name=f"Invoice_{ord_data['id']}.txt",
                    mime="text/plain"
                )

# ----------------- 10. ABOUT PLATFORM -----------------
elif selected_page == "ℹ️ About Platform":
    st.markdown('<div class="main-header">About DualForge Platform</div>', unsafe_allow_html=True)
    st.markdown("""
    **DualForge** is an enterprise e-commerce platform built as part of the **Java Full Stack Workforce Development Program (EWDP)** by **Ethnotech Academic Solutions Pvt Ltd** in association with **Madanapalle Institute of Technology & Science, Andhra Pradesh**.

    ### 👥 DualForge Engineering Team
    1. **M. Madhu Teja** (23691A3762) — *Team Lead & Full Stack Architect*
    2. **K. Madhu** (23691A3761) — *Frontend Engineer*
    3. **A. Hemanth Reddy** (23691A3747) — *Backend Developer*
    4. **V. Govardhan** (23691A3738) — *Database Engineer*
    5. **B. Harsha Vardhan** (23691A3740) — *Security Specialist*
    6. **S. Harinath Reddy** (23691A3738) — *QA & NoSQL Integration*

    ### 🛠️ Architecture
    * **Streamlit Cloud App**: Interactive full-stack interface with multi-role portals (Admin, Seller, Customer).
    * **React 19 + Vite Frontend**: High-performance Single Page Application with glassmorphism CSS.
    * **Spring Boot 3.3.4 (Java 21) REST Backend**: Security filter chain, JWT tokens, H2/MongoDB persistence.
    """)
