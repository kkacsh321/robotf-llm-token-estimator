"""
RoboTF LLM Token Estimator - Streamlit Application

This Python script creates a Streamlit web application that allows users to estimate the number of tokens
for a given text input using a specified Hugging Face model's tokenizer. The tokenizer is loaded using
the `autotiktokenizer` library, which supports a wide range of models available on the Hugging Face Hub.

Features:
- User-friendly interface for entering the model name and text input.
- Displays the estimated token count, original text length, and cleaned text length.
- Supports any model with a `tokenizer.json` in the Hugging Face repository.
- Provides example model names and a link to browse models on the Hugging Face Hub.
- Includes detailed instructions on how the token estimation works.
- Caches the tokenizer for efficiency using Streamlit's `st.cache_resource`.

Dependencies:
- streamlit
- PIL (Python Imaging Library)
- autotiktokenizer

Usage:
1. Run the script using Streamlit: `streamlit run RoboTF_LLM_Token_Estimator.py`
2. Enter the Hugging Face model name and the text you want to analyze.
3. Click the 'Count Tokens' button to see the estimated token count and other details.

Example Model Names:
- mistralai/Mistral-7B-Instruct-v0.3
- deepseek-ai/DeepSeek-Coder-V2-Instruct-0724
- Qwen/Qwen2.5-Coder-32B-Instruct

Note:
- The application removes newline characters from the input text before tokenization.
- The tokenizer is loaded from the specified model repository on Hugging Face.
- For models that are quantized or re-trained, point to the original model repository containing `tokenizer.json`.

Author: Keith Kacsh
GitHub: https://github.com/kkacsh321/robotf-llm-token-estimator

"""

import streamlit as st
from PIL import Image
from autotiktokenizer import AutoTikTokenizer

def main():
    st.set_page_config(page_title="LLM Token Estimator", layout="wide", page_icon="images/favicon.ico")

    try:
        image = Image.open("images/robot_token.jpg")
        st.image(image, width=400)
    except FileNotFoundError as e:
        st.error(f"The image file 'robot_token.jpg' was not found: {e}")
    except Exception as e:
        st.error(f"Failed to load image: {e}")

    # Title and description
    st.title("RoboTF LLM Token Estimator")
    st.write("Enter text below to count the number of tokens for your specific LLM Model.")

    # Provide example model names and link to Hugging Face
    st.write("Example model names: `mistralai/Mistral-7B-Instruct-v0.3`, `deepseek-ai/DeepSeek-Coder-V2-Instruct-0724`, `Qwen/Qwen2.5-Coder-32B-Instruct`")
    st.markdown("[Browse models on Hugging Face Hub](https://huggingface.co/models) 🤗")
    st.markdown("Should support any model with a `tokenizer.json` in the HuggingFace repo")
    st.markdown("If using a quant, or re-train, point at original model repo with `tokenizer.json`")
    st.markdown("This is only an estimator based on [autotiktokenizer](https://github.com/bhavnicksm/autotiktokenizer) project - Go Support them")
    st.markdown("---")
    st.markdown("How this works:")
    st.markdown("You enter the user/model-repo-name that contains a `tokenizer.json` from huggingface")
    st.markdown("It removes any newline characters in the input")
    st.markdown("We use autotiktokenizer to take your prompt input and estimate the tokens for that model")
    st.markdown("Hope you find useful and can find the Github project here: [RoboTF LLM Token Estimator](https://github.com/kkacsh321/robotf-llm-token-estimator)")

    # Function to load tokenizer with caching
    @st.cache_resource
    def load_tokenizer(model_name):
        return AutoTikTokenizer.from_pretrained(model_name)

    # Create a form for the inputs and button
    with st.form(key='token_count_form'):
        # Text input for the model name
        model_name = st.text_area(
            "Enter the Hugging Face model name: (org/model_name)",
            placeholder="mistralai/Mistral-7B-Instruct-v0.3", height=68  # Default model name
        )

        # Text area for the user's input text
        user_input = st.text_area("Your text:", height=200)

        # Submit button
        submit_button = st.form_submit_button(label='Count Tokens')

    # When the form is submitted
    if submit_button:
        if model_name:
            # Initialize the tokenizer
            try:
                tokenizer = load_tokenizer(model_name)
            except Exception as e:
                st.error(f"Error loading tokenizer for model '{model_name}': {e}")
                st.stop()

            if user_input:
                # Replace newlines with spaces in the user input
                cleaned_input = user_input.replace('\n', ' ')

                # Tokenize the cleaned input text
                tokens = tokenizer.encode(cleaned_input)
                token_count = len(tokens)

                # Display results
                st.subheader("Results")
                st.write(f"**Model:** {model_name}")
                st.write(f"**Estimated Token count:** {token_count}")
                st.write(f"**Original Text Length:** {len(user_input)} characters")
                st.write(f"**Cleaned Text Length:** {len(cleaned_input)} characters")

            else:
                st.warning("Please enter some text to count tokens.")
        else:
            st.warning("Please enter a model name to proceed.")

if __name__ == "__main__":
    main()
