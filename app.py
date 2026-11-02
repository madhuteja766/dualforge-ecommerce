"""
DualForge — Enterprise E-Commerce Platform
Streamlit Cloud Application
Developed by M. Madhu Teja & Team (EWDP Capstone Project)
"""

import streamlit as st
import pandas as pd
import requests
import json
import time

st.set_page_config(
    page_title="DualForge E-Commerce",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for DualForge Glassmorphism & Modern Styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 50%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .badge-trust {
        display: inline-block;
        background: rgba(14, 165, 233, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(14, 165, 233, 0.3);
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .product-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 20px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .product-card:hover {
        border-color: rgba(99, 102, 241, 0.5);
    }
    .metric-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #38bdf8;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- PRODUCT DATA -----------------
CATALOG = [
    {
        "id": 1, "name": "Tech Hoodie Black", "category": "Fashion", "brand": "ForgeWear",
        "price": 2499.0, "original_price": 2799.0, "rating": 4.8, "reviews": 85,
        "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500",
        "description": "Wind-resistant thermo-regulating fleece hoodie with travel pockets.",
        "specs": "Fabric: Fleece Blend | Sizes: S, M, L, XL | Warranty: 1 Year",
        "trust_score": 94, "eco_rating": "A+"
    },
    {
        "id": 2, "name": "Cyberpunk Oversized Hoodie", "category": "Fashion", "brand": "CyberForge",
        "price": 3299.0, "original_price": 3899.0, "rating": 4.9, "reviews": 120,
        "image": "https://images.unsplash.com/photo-1509967419530-da38b4704bc6?w=500",
        "description": "Heavyweight 450GSM organic cotton oversized fleece hoodie.",
        "specs": "Fabric: 100% Organic Cotton | Sizes: M, L, XL, XXL | Warranty: 1 Year",
        "trust_score": 96, "eco_rating": "A"
    },
    {
        "id": 3, "name": "Urban Bomber Jacket", "category": "Fashion", "brand": "ForgeWear",
        "price": 4499.0, "original_price": 5299.0, "rating": 4.7, "reviews": 98,
        "image": "https://images.unsplash.com/photo-1548883354-7622d03aca27?w=500",
        "description": "Weatherproof bomber jacket with padded thermal lining.",
        "specs": "Shell: Nylon, Fill: Polyester | Sizes: M, L, XL | Warranty: 1 Year",
        "trust_score": 92, "eco_rating": "B+"
    },
    {
        "id": 4, "name": "Forgebuds ANC Wireless", "category": "Electronics", "brand": "ForgeAudio",
        "price": 4999.0, "original_price": 5999.0, "rating": 4.6, "reviews": 188,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500",
        "description": "Studio acoustics, 35dB active noise cancellation, and 40h battery cell.",
        "specs": "ANC: 35dB | Battery: 40h | Driver: 10mm Graphene | Bluetooth 5.3",
        "trust_score": 95, "eco_rating": "A"
    },
    {
        "id": 5, "name": "ForgePro Wireless Gaming Headset", "category": "Electronics", "brand": "ForgeAudio",
        "price": 6499.0, "original_price": 7999.0, "rating": 4.8, "reviews": 142,
        "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500",
        "description": "Low-latency 2.4GHz wireless headset with detachable spatial mic.",
        "specs": "Drivers: 50mm Neodymium | Battery: 30h | 7.1 Spatial Audio",
        "trust_score": 97, "eco_rating": "A"
    },
    {
        "id": 6, "name": "BoomBlast Portable Speaker", "category": "Electronics", "brand": "ForgeAudio",
        "price": 3499.0, "original_price": 3999.0, "rating": 4.7, "reviews": 115,
        "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500",
        "description": "IPX7 waterproof 30W Bluetooth speaker with deep bass radiator.",
        "specs": "Power: 30W RMS | Battery: 15h | Waterproof: IPX7 | Fast Charge",
        "trust_score": 93, "eco_rating": "A"
    },
    {
        "id": 7, "name": "Stealth Runners", "category": "Footwear", "brand": "Stealth",
        "price": 3499.0, "original_price": 4299.0, "rating": 4.7, "reviews": 254,
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500",
        "description": "Hydrophobic mesh structure with ultra-rebound cushioning outsoles.",
        "specs": "Sizes: UK 7-11 | Upper: Mesh | Sole: Rubber Rebound | Lightweight",
        "trust_score": 95, "eco_rating": "A+"
    },
    {
        "id": 8, "name": "Apex Velocity Sneakers", "category": "Footwear", "brand": "ApexForge",
        "price": 5999.0, "original_price": 7499.0, "rating": 4.9, "reviews": 165,
        "image": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=500",
        "description": "Lightweight carbon-plated marathon racing shoes.",
        "specs": "Plate: Carbon Fiber | Foam: Nitrogen Infused | Sizes: UK 8-11",
        "trust_score": 98, "eco_rating": "A"
    },
    {
        "id": 9, "name": "Classic Leather Oxfords", "category": "Footwear", "brand": "LeatherForge",
        "price": 4999.0, "original_price": 5999.0, "rating": 4.6, "reviews": 82,
        "image": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?w=500",
        "description": "Handcrafted Italian genuine leather formal Oxford dress shoes.",
        "specs": "100% Genuine Full-Grain Leather | Sizes: UK 7-10 | Goodyear Welted",
        "trust_score": 94, "eco_rating": "B"
    },
    {
        "id": 10, "name": "Forgebook Pro 16", "category": "Electronics", "brand": "Forge",
        "price": 124999.0, "original_price": 139999.0, "rating": 4.8, "reviews": 124,
        "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500",
        "description": "Liquid-metal cooled workstation laptop with 16-inch 120Hz display.",
        "specs": "Intel i9 13900H | RTX 4070 8GB | 32GB DDR5 | 1TB NVMe SSD",
        "trust_score": 99, "eco_rating": "A"
    },
    {
        "id": 11, "name": "RGB Mechanical Keyboard", "category": "Electronics", "brand": "ForgeKey",
        "price": 3499.0, "original_price": 4499.0, "rating": 4.6, "reviews": 230,
        "image": "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=500",
        "description": "Hot-swappable tactile mechanical switches with per-key RGB.",
        "specs": "PBT Keycaps | Hot-Swap Red/Brown | Type-C | N-Key Rollover",
        "trust_score": 92, "eco_rating": "A"
    },
    {
        "id": 12, "name": "Forge Watch Ultra", "category": "Electronics", "brand": "ForgeWatch",
        "price": 14999.0, "original_price": 17999.0, "rating": 4.9, "reviews": 148,
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500",
        "description": "Titanium case outdoor smartwatch with dual-frequency GPS & ECG.",
        "specs": "2.0\" AMOLED | Titanium Case | 7 Days Battery | 100m Water Resist",
        "trust_score": 98, "eco_rating": "A+"
    }
]

# ----------------- SESSION STATE -----------------
if "cart" not in st.session_state:
    st.session_state.cart = []
if "coupon_applied" not in st.session_state:
    st.session_state.coupon_applied = False
if "discount_pct" not in st.session_state:
    st.session_state.discount_pct = 0.0
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
    menu = st.radio(
        "Navigation",
        ["🛍️ Store Catalog", "🤖 AI Assistant", "⚖️ Product Comparison", "📏 Smart Size Calculator", "🛒 My Cart", "ℹ️ About Platform"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("**DualForge Trust Score: 94/100** ⭐")
    st.markdown("🔒 *100% Encrypted JWT Sessions*")
    st.caption("EWDP Capstone — M. Madhu Teja & Team")

# ----------------- 1. STORE CATALOG -----------------
if menu == "🛍️ Store Catalog":
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
        categories = ["All"] + sorted(list(set(p["category"] for p in CATALOG)))
        selected_cat = st.selectbox("Filter Category", categories)
    with f_col2:
        max_price = st.slider("Max Budget (₹)", 1000, 150000, 150000, step=1000)
    with f_col3:
        search_query = st.text_input("🔍 Search Products", "")

    # Filtered List
    filtered = CATALOG
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
            
            if st.button(f"Add to Cart", key=f"add_{prod['id']}"):
                st.session_state.cart.append(prod)
                st.toast(f"Added {prod['name']} to cart!", icon="🛒")

# ----------------- 2. AI ASSISTANT -----------------
elif menu == "🤖 AI Assistant":
    st.markdown('<div class="main-header">AI Shopping Decision Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Natural language query parser for budget-constrained shopping decisions.</div>', unsafe_allow_html=True)

    # Display chat history
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    prompt = st.chat_input("E.g., 'I have 5000 rupees for audio' or 'Show me best sneakers'")
    if prompt:
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Smart rule-based AI parser
        p_lower = prompt.lower()
        import re
        budget_match = re.search(r'(\d+[\d,]*)', p_lower)
        budget = float(budget_match.group(1).replace(',', '')) if budget_match else None

        response = ""
        # Category intent
        matched_category = None
        if "audio" in p_lower or "headphone" in p_lower or "speaker" in p_lower or "earbud" in p_lower:
            matched_category = "Electronics"
            candidates = [p for p in CATALOG if "ForgeAudio" in p["brand"] or "Audio" in p["specs"] or "ANC" in p["name"] or "Headphone" in p["name"] or "Speaker" in p["name"]]
        elif "shoe" in p_lower or "sneaker" in p_lower or "runner" in p_lower or "footwear" in p_lower:
            matched_category = "Footwear"
            candidates = [p for p in CATALOG if p["category"] == "Footwear"]
        elif "hoodie" in p_lower or "jacket" in p_lower or "cloth" in p_lower or "fashion" in p_lower or "wear" in p_lower:
            matched_category = "Fashion"
            candidates = [p for p in CATALOG if p["category"] == "Fashion"]
        elif "laptop" in p_lower or "computer" in p_lower or "pc" in p_lower:
            candidates = [p for p in CATALOG if "Forgebook" in p["name"]]
        else:
            candidates = CATALOG

        if budget:
            budget_candidates = [p for p in candidates if p["price"] <= budget]
            if budget_candidates:
                best_item = max(budget_candidates, key=lambda x: (x["rating"], -x["price"]))
                response = f"🎯 **Found {len(budget_candidates)} option(s) within ₹{budget:,.0f}:**\n\n"
                response += f"🌟 **Top AI Recommendation:** **{best_item['name']}** (₹{best_item['price']:,.0f})\n"
                response += f"- Rating: ⭐ {best_item['rating']} / 5 ({best_item['reviews']} verified reviews)\n"
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

# ----------------- 3. PRODUCT COMPARISON MATRIX -----------------
elif menu == "⚖️ Product Comparison":
    st.markdown('<div class="main-header">Product Comparison Matrix</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Side-by-side spec comparison table with automated AI Value Recommendation.</div>', unsafe_allow_html=True)

    product_names = [p["name"] for p in CATALOG]
    selected_prods = st.multiselect(
        "Select up to 3 products to compare:",
        product_names,
        default=[CATALOG[3]["name"], CATALOG[4]["name"]]
    )

    if len(selected_prods) >= 2:
        comp_items = [p for p in CATALOG if p["name"] in selected_prods]
        
        # Build comparison table
        table_data = {
            "Attribute": ["Price", "Rating", "Reviews", "Category", "Brand", "Trust Score", "Eco Impact", "Specs"],
        }
        for item in comp_items:
            table_data[item["name"]] = [
                f"₹{item['price']:,.0f}",
                f"⭐ {item['rating']}",
                str(item['reviews']),
                item["category"],
                item["brand"],
                f"{item['trust_score']}/100",
                item["eco_rating"],
                item["specs"]
            ]

        df = pd.DataFrame(table_data).set_index("Attribute")
        st.table(df)

        # AI Value Winner
        best_value = max(comp_items, key=lambda x: (x["rating"] / x["price"]) * 1000)
        st.success(f"🤖 **AI Value Recommendation:** **{best_value['name']}** offers the highest performance-to-price ratio with a rating of ⭐ {best_value['rating']} at ₹{best_value['price']:,.0f}.")
    else:
        st.info("Please select at least 2 products above to generate the comparison matrix.")

# ----------------- 4. SMART SIZE CALCULATOR -----------------
elif menu == "📏 Smart Size Calculator":
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
        # Standard conversion
        uk_size = round(foot_length - 18.0)
        uk_size = max(6, min(12, uk_size))
        
        st.markdown("---")
        st.markdown(f"### Recommended Shoe Size: **`UK {uk_size}`** (US {uk_size + 1} / EU {uk_size + 33})")

# ----------------- 5. MY CART & CHECKOUT -----------------
elif menu == "🛒 My Cart":
    st.markdown('<div class="main-header">Your Shopping Cart</div>', unsafe_allow_html=True)

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
            
            # Coupon section
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

            if st.button("Authorize & Place Order", type="primary"):
                st.balloons()
                st.success("🎉 Order successfully placed! Confirmation order receipt generated.")
                st.session_state.cart = []
                st.session_state.coupon_applied = False
                st.session_state.discount_pct = 0.0

# ----------------- 6. ABOUT PLATFORM -----------------
elif menu == "ℹ️ About Platform":
    st.markdown('<div class="main-header">About DualForge Platform</div>', unsafe_allow_html=True)
    st.markdown("""
    **DualForge** is an enterprise e-commerce platform built as part of the **Java Full Stack Workforce Development Program (EWDP)**.

    ### 👥 Engineering Team
    * **M. Madhu Teja** (23691A3762) — *Team Lead & Full Stack Architect*
    * **K. Madhu** (23691A3761) — *Frontend Engineer*
    * **A. Hemanth Reddy** (23691A3747) — *Backend Developer*
    * **V. Govardhan** (23691A3738) — *Database Engineer*
    * **B. Harsha Vardhan** (23691A3740) — *Security Specialist*
    * **S. Harinath Reddy** (23691A3738) — *QA & NoSQL Integration*

    ### 🛠️ Architecture
    * **Python Streamlit UI**: Real-time cloud interactive interface.
    * **React 19 + Vite Frontend**: High-performance glassmorphism Single Page Application.
    * **Spring Boot 3.3.4 (Java 21) REST Backend**: Robust security, JWT authorization, and H2/MongoDB persistence.
    """)
