import streamlit as st
import re
from pymongo import MongoClient, errors
from datetime import datetime
from config import MONGO_URI, DB_NAME, COLLECTION_NAME


# -----------------------------
# MongoDB Connection Function
# -----------------------------
@st.cache_resource
def init_connection():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        # Trigger server selection to verify connection
        client.server_info()
        return client
    except errors.ServerSelectionTimeoutError:
        st.error("❌ Unable to connect to MongoDB. Please check your connection string.")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected MongoDB Error: {e}")
        return None


def app():
    st.set_page_config(page_title="Simple Number Analyzer", layout="centered")
    st.title("Smart Number Checker")
    st.markdown("---")

    # Initialize MongoDB
    client = init_connection()
    if client is None:
        st.stop()

    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    nums = st.text_input(
        "Enter a list of integers separated by commas:",
        placeholder="e.g., 18, -5, 4, 0, -20",
        key="num_input_field"
    )

    if st.button("Analyze Numbers", type="primary"):

        if not nums.strip():
            st.warning("⚠️ Please enter at least one number before analyzing.")
            return

        st.subheader("Analysis Results:")

        raw_num_strings = [x.strip() for x in re.split(r',', nums) if x.strip()]

        if not raw_num_strings:
            st.error("❌ No valid input found after splitting by comma.")
            return

        try:
            num_list = [int(x) for x in raw_num_strings]
        except ValueError:
            st.error("❌ Please enter valid integers only.")
            return

        results = []

        for num in num_list:
            num_str = str(num)

            if num > 0:
                if num % 2 == 0:
                    result = "Positive and Even"
                    st.markdown(f":green[**{num_str}**] is {result}")
                else:
                    result = "Positive and Odd"
                    st.markdown(f":green[**{num_str}**] is {result}")
            elif num < 0:
                if num % 2 == 0:
                    result = "Negative and Even"
                    st.markdown(f":red[**{num_str}**] is {result}")
                else:
                    result = "Negative and Odd"
                    st.markdown(f":red[**{num_str}**] is {result}")
            else:
                result = "Zero"
                st.markdown(f":orange[**{num_str}**] is Zero")

            results.append({
                "number": num,
                "analysis": result
            })

        # -----------------------------
        # Save Data to MongoDB
        # -----------------------------
        document = {
            "input_numbers": num_list,
            "results": results,
            "created_at": datetime.utcnow()
        }

        try:
            collection.insert_one(document)
            st.success("✅ Data saved to MongoDB successfully!")
        except Exception as e:
            st.error(f"❌ Failed to save data: {e}")

        st.markdown("---")


if __name__ == '__main__':
    app()