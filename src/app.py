import streamlit as st
from test_api import test_multiple_keys

st.set_page_config(page_title="API Key Tester", page_icon=":key:")
st.title(":key: Test Your API Keys")
# TODO make new line here

st.subheader("Base URL")
base_url = st.text_input(label="", placeholder="https://api.example.com/v1")
st.markdown("---")

st.subheader("API Keys")
keys_text = st.text_area(
    "Enter each key in new line",
    height=160,
    placeholder="sk-xxxxxxxx1\nsk-xxxxxxxx2\nsk-xxxxxxxx3",
)

if st.button("Start Testing :rocket:", type="primary"):
    if not base_url.strip():
        st.error("Enter Base URL.")
    elif not keys_text.strip():
        st.error("You should enter at least ")
    else:
        api_keys = [k for k in keys_text.strip().splitlines() if k.strip()]
        with st.spinner(f"Testing: {len(api_keys)}"):
            results = test_multiple_keys(base_url.strip(), api_keys)

        st.subheader("Results")
        for r in results:
            key = r["api_key"]
            masked = f"{key[:6]}...{key[-4:]}" if len(key) > 10 else key

            col1, col2, col3 = st.columns([1, 4, 5])
            with col1:
                st.markdown("### :white_check_mark:" if r["ok"] else "### :x:")
            with col2:
                st.code(masked)
            with col3:
                if r["ok"]:
                    st.caption(f"Status Code: {r['status_code']}")
                else:
                    st.caption(r['message'])

        ok_count = sum(1 for r in results if r["ok"])
        st.info(f"{ok_count} from {len(results)} api keys is active!")
