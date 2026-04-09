import streamlit as st
import stripe
import os
from dotenv import load_dotenv

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base, ".env"))

def show_payment_page():
    st.markdown("""
    <style>
    .pricing-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 16px;
        margin: 20px 0;
    }
    .pricing-card {
        background: #0f1a0f;
        border: 1px solid #1a2e1a;
        border-radius: 20px;
        padding: 28px 20px;
        text-align: center;
        color: white;
    }
    .pricing-card.featured {
        border: 2px solid #2E7D32;
        transform: scale(1.02);
    }
    .pricing-card.investor {
        border: 1px solid #FFD700;
    }
    .price-badge {
        display: inline-block;
        background: #2E7D32;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .price-badge.gold {
        background: #B8860B;
    }
    .plan-name {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 8px;
        color: white;
    }
    .plan-price {
        font-size: 48px;
        font-weight: 800;
        color: #4CAF50;
        line-height: 1;
    }
    .plan-price.gold {
        color: #FFD700;
    }
    .plan-period {
        font-size: 13px;
        color: #888;
        margin-bottom: 20px;
    }
    .plan-features {
        list-style: none;
        padding: 0;
        text-align: left;
        margin-bottom: 20px;
        font-size: 13px;
        color: #ccc;
    }
    .plan-features li {
        padding: 6px 0;
        border-bottom: 1px solid #1a2e1a;
    }
    .plan-features li:last-child {
        border-bottom: none;
    }
    @media (max-width: 640px) {
        .pricing-grid { grid-template-columns: 1fr; }
        .pricing-card.featured { transform: none; }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p style="font-size:32px; font-weight:800; text-align:center; color:#f0f0f0">🌿 Join CannaIQ</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#888; margin-bottom:24px">Choose the plan that fits your needs</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="pricing-grid">
        <div class="pricing-card">
            <div class="price-badge">BASIC</div>
            <div class="plan-name">Starter</div>
            <div class="plan-price">$99</div>
            <div class="plan-period">per month CAD</div>
            <ul class="plan-features">
                <li>✅ Calgary dashboard</li>
                <li>✅ Saturation scores</li>
                <li>✅ Opportunity scores</li>
                <li>✅ Updated daily</li>
                <li>❌ Store map</li>
                <li>❌ Postal code analysis</li>
                <li>❌ Edmonton data</li>
            </ul>
        </div>
        <div class="pricing-card featured">
            <div class="price-badge">MOST POPULAR</div>
            <div class="plan-name">Pro</div>
            <div class="plan-price">$199</div>
            <div class="plan-period">per month CAD</div>
            <ul class="plan-features">
                <li>✅ Calgary + Edmonton</li>
                <li>✅ Interactive store map</li>
                <li>✅ Postal code analysis</li>
                <li>✅ Saturation + opportunity scores</li>
                <li>✅ Full store intelligence</li>
                <li>✅ New store alerts</li>
                <li>✅ Updated daily</li>
            </ul>
        </div>
        <div class="pricing-card investor">
            <div class="price-badge gold">INVESTOR</div>
            <div class="plan-name">Investor</div>
            <div class="plan-price gold">$499</div>
            <div class="plan-period">per month CAD</div>
            <ul class="plan-features">
                <li>✅ Everything in Pro</li>
                <li>✅ Market growth signals</li>
                <li>✅ Distress indicators</li>
                <li>✅ National expansion data</li>
                <li>✅ Priority support</li>
                <li>🔜 API access</li>
                <li>🔜 Custom reports</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Plan selector
    plan = st.radio(
        "Select your plan",
        ["Starter — $99/month", "Pro — $199/month", "Investor — $499/month"],
        index=1,
        horizontal=True
    )

    email = st.text_input("Your email address", placeholder="you@example.com")

    if st.button("Start Subscription", use_container_width=True):
        if not email:
            st.error("Please enter your email address")
        else:
            secret_key = os.environ.get("STRIPE_SECRET_KEY", "")
            if not secret_key:
                st.error("Configuration error — please contact hello@cannaiqdata.ca")
            else:
                try:
                    stripe.api_key = secret_key

                    if "Starter" in plan:
                        price_id = os.environ.get("STRIPE_BASIC_PRICE_ID", "")
                    elif "Investor" in plan:
                        price_id = os.environ.get("STRIPE_INVESTOR_PRICE_ID", "")
                    else:
                        price_id = os.environ.get("STRIPE_PRICE_ID", "")

                    session = stripe.checkout.Session.create(
                        payment_method_types=["card"],
                        line_items=[{"price": price_id, "quantity": 1}],
                        mode="subscription",
                        customer_email=email,
                        success_url="https://dashboard.cannaiqdata.ca?subscribed=true",
                        cancel_url="https://dashboard.cannaiqdata.ca?cancelled=true",
                    )
                    st.success("Your secure checkout is ready!")
                    st.markdown(f"""
                    <a href="{session.url}" target="_blank" style="
                        display:block;
                        background:#2E7D32;
                        color:white;
                        padding:15px;
                        text-align:center;
                        border-radius:10px;
                        font-size:18px;
                        font-weight:bold;
                        text-decoration:none;
                        margin-top:10px;
                    ">Click Here To Complete Payment</a>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Payment error: {e}")

    st.markdown('<p style="text-align:center; color:#555; font-size:12px; margin-top:16px">Secured by Stripe · Cancel anytime · No hidden fees</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_payment_page()