import streamlit as st
from app_store_scraper import AppStore
import pandas as pd
from datetime import datetime

# Define the function to get App Store reviews
def getAppStoreReviews(link, after_date, country):
    app_name = link.split("/")[-2]
    revolut = AppStore(country=country, app_name=app_name)
    revolut.review(after=after_date)
    revolut.review()
    df = pd.DataFrame(revolut.reviews)
    df['Brand'] = app_name
    df['root'] = link
    df.rename(columns={'userName': 'Author', 'review': 'Review'}, inplace=True)
    df.to_csv(f"{app_name}.csv", index=False)
    st.write(f"Scraping done for {app_name}")
    return df

# Streamlit UI
def main():
    st.title("App Store Reviews Scraper")

    # Input for after date
    after_date = st.date_input("Select after date")

    # Input for country
    country = st.text_input("Enter country code (e.g., US)")

    # Input for app links
    app_links_text = st.text_area("Enter app links (one link per line)")
    app_links = app_links_text.split("\n")

    if st.button("Scrape Reviews"):
        for link in app_links:
            if link:
                getAppStoreReviews(link, after_date, country)

        st.write("All scraping done!")

if __name__ == "__main__":
    main()
