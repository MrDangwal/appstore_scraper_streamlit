import streamlit as st
from app_store_scraper import AppStore
import pandas as pd
from datetime import datetime

def getAppStoreReviews(link, after_date, country):
    app_name = link.split("/")[-2]

    try:
        revolut = AppStore(country=country, app_name=app_name)
        revolut.review(after=after_date)
        revolut.review()
        reviews = revolut.reviews

        if not reviews:
            st.write(f"No reviews found for {app_name}")
            return None

        df = pd.DataFrame(reviews)
        df['Brand'] = app_name
        df['root'] = link
        df.rename(columns={'userName': 'Author', 'review': 'Review'}, inplace=True)
        df.to_csv(f"{app_name}.csv", index=False)
        st.write(f"Scraping done for {app_name}")
        return df

    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def main():
    st.title("App Store Reviews Scraper")

    after_date = st.date_input("Select after date")
    country = st.text_input("Enter country code (e.g., US)")
    app_links_text = st.text_area("Enter app links (one link per line)")

    if st.button("Scrape Reviews"):
        dataframes = []
        app_links = app_links_text.split("\n")

        for link in app_links:
            if link:
                df = getAppStoreReviews(link, after_date, country)
                if df is not None:
                    dataframes.append(df)

        st.write("All scraping done!")

        for df in dataframes:
            csv = df.to_csv(index=False).encode('utf-8')
            href = f'<a href="data:file/csv;base64,{b64encode(csv).decode()}" download="{df["Brand"].iloc[0]}.csv">Download CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
