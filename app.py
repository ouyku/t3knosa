import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="t3knosa", layout="wide")
st.title("t3knosa")
st.caption("find exact product images by name or model code")

col1, col2 = st.columns([3, 1])
with col1:
    product = st.text_input("product name", placeholder="Nothing Headphone 1")
with col2:
    product_code = st.text_input("model code (optional)", placeholder="B170")

if st.button("search", use_container_width=True):
    if not product:
        st.warning("enter a product name")
    else:
        with st.spinner("searching..."):
            params = {"product": product}
            if product_code:
                params["product_code"] = product_code
            response = requests.get(f"{API_URL}/find-images", params=params)
            if response.status_code == 200:
                data = response.json()
                st.session_state["results"] = data.get("results", [])
                st.session_state["product"] = product
                st.session_state["product_code"] = product_code
                st.session_state["satisfied"] = None  # reset on new search
            else:
                st.error(f"api error: {response.status_code}")

# satisfaction buttons — always visible after a search
if "results" in st.session_state:
    st.write("**satisfied with the results?**")
    sat_col1, sat_col2 = st.columns([1, 1])
    with sat_col1:
        if st.button("yes", use_container_width=True):
            st.session_state["satisfied"] = True
    with sat_col2:
        if st.button("no", use_container_width=True):
            st.session_state["satisfied"] = False

    # generate buttons only appear if user said no
    if st.session_state.get("satisfied") is False:
        gen_col1, gen_col2 = st.columns(2)
        with gen_col1:
            catalog_clicked = st.button("catalog photo", use_container_width=True)
        with gen_col2:
            lifestyle_clicked = st.button("lifestyle photo", use_container_width=True)

        style = None
        if catalog_clicked:
            style = "catalog"
        elif lifestyle_clicked:
            style = "lifestyle"

        if style:
            with st.spinner(f"generating {style} photo..."):
                params = {"product": st.session_state["product"], "style": style}
                if st.session_state.get("product_code"):
                    params["product_code"] = st.session_state["product_code"]

                # only use reference if score >= 0.9
                real_results = [r for r in st.session_state.get("results", []) if not r.get("is_generated")]
                if real_results and real_results[0]["confidence_score"] >= 0.9:
                    params["reference_image_url"] = real_results[0]["image_url"]

                response = requests.get(f"{API_URL}/generate-image", params=params)
                if response.status_code == 200:
                    data = response.json()
                    generated = data.get("results", [])
                    if generated:
                        st.caption(f"AI generated — {style}")
                        st.image(generated[0]["image_url"], width=500)
                else:
                    st.error(f"generation failed: {response.status_code}")


# show results below
if "results" in st.session_state and st.session_state["results"]:
    results = st.session_state["results"]
    st.divider()
    st.success(f"{len(results)} images found")

    cols = st.columns(4)
    for i, item in enumerate(results):
        with cols[i % 4]:
            if item.get("is_generated"):
                st.caption("AI generated")
            st.image(item["image_url"], use_container_width=True)
            st.caption(f"score: {item['confidence_score']:.2f} — {item['title'][:40]}")
