import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="AI Website Copy Generator Pro",
    page_icon="🍽️",
    layout="wide"
)

st.title("🍽️ AI Website Copy Generator Pro")

business_name = st.text_input(
    "Restaurant Name",
    placeholder="Spice Garden"
)

business_type = st.selectbox(
    "Business Type",
    ["Restaurant", "Cafe", "Bakery", "Food Truck"]
)

city = st.text_input(
    "City",
    placeholder="Visakhapatnam"
)

tone = st.selectbox(
    "Content Tone",
    ["Professional", "Friendly", "Luxury", "Modern"]
)

generate = st.button("Generate Website Copy")

if generate:

    if not business_name:
        st.warning("Please enter restaurant name")
        st.stop()

    try:

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )

        prompt = f"""
        Create website copy for:

        Business Name: {business_name}
        Type: {business_type}
        City: {city}
        Tone: {tone}

        Generate:

        1. Hero Section
        2. About Us
        3. Why Choose Us
        4. Services
        5. Call To Action
        """

        with st.spinner("Generating content..."):

            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

        content = response.choices[0].message.content

        st.success("Content Generated Successfully")

        st.markdown(content)

        # -----------------------
        # AI Evaluation Feature
        # -----------------------

        evaluation_prompt = f"""
        Evaluate the following website copy.

        Give:

        1. Quality Score (/10)
        2. Strengths
        3. Weaknesses
        4. Missing Sections
        5. Improvement Suggestions

        Content:
        {content}
        """

        eval_response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": evaluation_prompt
                }
            ]
        )

        evaluation = eval_response.choices[0].message.content

        st.subheader("📊 AI Evaluation Report")

        st.info(evaluation)

    except Exception as e:

        st.error("Error occurred while generating content")

        st.code(str(e))