import streamlit as st
import requests

# Render Backend URL
be_url = "https://be-ai-interview-chat-bot-1.onrender.com"

st.title("AI Interview Preparation Helper Bot")

with st.form("Details"):

    topic = st.text_input("Enter Lang/Topic:")

    level = st.selectbox(
        "Choose Level",
        ["Easy", "Medium", "Advanced"]
    )

    ways = st.multiselect(
        "Choose Question Types",
        ["MCQS", "Theory questions", "Coding question"]
    )

    submit = st.form_submit_button("Generate Questions")

    if submit:

        if not topic:
            st.warning("Please enter a topic.")
            st.stop()

        if not ways:
            st.warning("Please select at least one question type.")
            st.stop()

        prompt = f"""
Generate interview questions.

Topic: {topic}
Difficulty Level: {level}
Question Types: {', '.join(ways)}

IMPORTANT RULES:
1. Return ONLY a valid JSON array.
2. Do NOT return explanations.
3. Do NOT return answers.
4. Do NOT return markdown.
5. Do NOT return any text before or after the JSON.
6. Generate exactly 10 questions for each selected question type.

Expected format:

[
    {{
        "question_type": "Theory questions",
        "question": "What is Python?"
    }}
]
"""

        with st.spinner("Generating Questions..."):

            try:

                response = requests.post(
                    f"{be_url}/generate",
                    json={"prompt": prompt},
                    timeout=120
                )

                st.write("Status Code:", response.status_code)

                if response.status_code == 200:

                    result = response.json()

                    if "object" in result:

                        questions = result["object"]

                        st.success(
                            f"Generated {len(questions)} Questions"
                        )

                        for i, q in enumerate(questions, start=1):

                            st.write(
                                f"### {i}. [{q['question_type']}]"
                            )

                            st.write(q["question"])

                            st.divider()

                    else:

                        st.error(
                            result.get(
                                "error",
                                "Unknown backend error"
                            )
                        )

                        if "raw_output" in result:
                            st.code(result["raw_output"])

                else:

                    st.error(
                        f"Backend Error: {response.status_code}"
                    )

                    st.write(response.text)

            except Exception as e:

                st.error(
                    f"Connection Error: {str(e)}"
                )