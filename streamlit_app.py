import streamlit as st
import pandas as pd
import sys
import os
import certifi

from dotenv import load_dotenv
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.exception.exception import NetworkSecurityException

# Load environment variables
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL_KEY")
ca = certifi.where()

st.set_page_config(page_title="Network Security Prediction", layout="wide")

# Title
st.title("🛡️ Network Security Prediction Dashboard")

# TRAINING SECTION
if st.button("📊 Train Model"):
    try:
        st.info("Training in progress...")
        pipeline = TrainingPipeline()
        pipeline.run_pipeline()
        st.success("✅ Training Completed Successfully!")
    except Exception as e:
        st.error(f"❌ Training Failed: {e}")
        raise NetworkSecurityException(e, sys)

# PREDICTION SECTION
st.subheader("🔍 Upload CSV for Prediction")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("### 📄 Input Data")
        st.dataframe(df)

        # Load saved model and preprocessor
        preprocessor = load_object("final_model/preprocessor.pkl")
        model = load_object("final_model/model.pkl")

        network_model = NetworkModel(preprocessor=preprocessor, model=model)
        y_pred = network_model.predict(df)

        df["predicted_column"] = y_pred

        st.write("### 🧠 Prediction Results")
        st.dataframe(df)

        # Optional: Allow download of the result CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Result CSV", csv, file_name="predicted_output.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❌ Prediction Failed: {e}")
        raise NetworkSecurityException(e, sys)
