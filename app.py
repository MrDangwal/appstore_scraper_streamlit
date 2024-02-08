import streamlit as st
from app_store_scraper import AppStore
import pandas as pd
from datetime import datetime
import base64


def getAppStoreReviews(link):
    app_name = link.split("/")[-2]
    revolut = AppStore(country="US", app_name=app_name)
    revolut.review(after=datetime(2000, 1, 1))
    revolut.review()
    df = pd.DataFrame(revolut.reviews)
    df['Brand'] = app_name
    df['root'] = link
    df.rename(columns={'userName': 'Author', 'review': 'Review'}, inplace=True)
    st.write(f"Scraping done for {app_name}")
    return df

#Streamlit UI
def main():
    st.title("App Store Reviews Scraper")

    #Input for app links
    app_links_text = st.text_area("Enter app links (one link per line)")

    if st.button("Scrape Reviews"):
        app_links = app_links_text.split("\n")
        dataframes = []

        for link in app_links:
            if link:
                dataframes.append(getAppStoreReviews(link))

        st.write("All scraping done!")

        for idx, df in enumerate(dataframes):  
            csv = df.to_csv(index=False).encode('utf-8')
            b64 = base64.b64encode(csv).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="{df["Brand"].iloc[0]}.csv">Download CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
