import streamlit as st
from scrapers import ica, coop, willys, lidl
import urllib.request
from PIL import Image

st.set_page_config(page_title="Veckans Erbjudanden", page_icon="🛒", layout="wide")

st.title("🛒 Veckans Erbjudanden")
st.markdown("Här samlar vi de bästa erbjudandena från dina favoritbutiker den här veckan!")

# Sidebar för filtrering
st.sidebar.header("Filtrera på butik")
show_ica = st.sidebar.checkbox("ICA Torgkassen", value=True)
show_coop = st.sidebar.checkbox("Coop", value=True)
show_willys = st.sidebar.checkbox("Willys", value=True)
show_lidl = st.sidebar.checkbox("Lidl", value=True)

# Hämta data baserat på val
all_offers = []
if show_ica:
    all_offers.extend(ica.get_offers())
if show_coop:
    all_offers.extend(coop.get_offers())
if show_willys:
    all_offers.extend(willys.get_offers())
if show_lidl:
    all_offers.extend(lidl.get_offers())

if not all_offers:
    st.warning("Vänligen välj minst en butik i menyn till vänster.")
else:
    # Visa erbjudanden i ett grid
    cols = st.columns(4)
    
    for i, offer in enumerate(all_offers):
        col = cols[i % 4]
        with col:
            st.markdown(f"### {offer['product']}")
            st.markdown(f"**{offer['brand']}**")
            
            try:
                # Add headers to avoid 403 Forbidden for Unsplash
                req = urllib.request.Request(offer['image_url'], headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    img = Image.open(response)
                    st.image(img, width='stretch')
            except Exception as e:
                # Fallback if image fails to load
                st.info("Ingen bild tillgänglig")
                
            st.metric(label="Pris", value=offer['price'], delta=offer['discount'], delta_color="off")
            st.caption(f"Butik: {offer['store']}")
            st.markdown("---")
