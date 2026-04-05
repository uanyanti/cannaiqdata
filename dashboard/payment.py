import streamlit as st
import stripe
import os
from dotenv import load_dotenv

# Load .env from root folder
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base, ".env"))

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
PRICE_ID = os.getenv("STRIPE_PRICE_ID")
PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")

def show_payment_page():
    st.markdown("""
    <style>
    .pricing-card {
        background: linear-gradient(135deg, #1B5E20, #2E7D32);
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin: 20px 0;
    }
    .price-tag {
        font-size: 64px;
        font-weight: bold;
        color: white;
    }
    .feature-list {
        text-align: left;
        padding: 20px;
        background: #1E1E1E;
        border-radius: 12px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p style="font-size:36px; font-weight:bold; text-align:center">🌿 Join CannaIQ Beta</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#888">Get full access to Calgary cannabis market intelligence</p>', unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="pricing-card">
            <p style="font-size:22px; margin:0">CannaIQ Starter</p>
            <p class="price-tag">$199</p>
            <p style="font-size:16px; color:#90EE90">per month CAD</p>
            <p style="font-size:14px">Cancel anytime</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-list">
            <p style="color:#2E7D32; font-weight:bold">What You Get:</p>
            <p>Full Calgary market intelligence dashboard</p>
            <p>Neighbourhood saturation scores</p>
            <p>Opportunity scores by area</p>
            <p>196 store competitive landscape</p>
            <p>Updated daily</p>
            <p>New store alerts</p>
            <p>Edmonton data (coming soon)</p>
            <p>Vancouver data (coming soon)</p>
            <p>Predictive analytics (coming soon)</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        email = st.text_input("Your email address", placeholder="you@example.com")

        if st.button("Start Subscription — $199/month CAD", use_container_width=True):
            if not email:
                st.error("Please enter your email address")
            else:
                try:
                    session = stripe.checkout.Session.create(
                        payment_method_types=["card"],
                        line_items=[{
                            "price": PRICE_ID,
                            "quantity": 1
                        }],
                        mode="subscription",
                        customer_email=email,
                        success_url="https://cannaiqdata.streamlit.app?subscribed=true",
                        cancel_url="https://cannaiqdata.streamlit.app?cancelled=true",
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
                    ">
                        Click Here To Complete Payment
                    </a>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Payment error: {e}")

        st.markdown('<p style="text-align:center; color:#555; font-size:12px">Secured by Stripe · Cancel anytime · No hidden fees</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_payment_page()