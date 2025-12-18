import streamlit as st
import requests
import time

# API for Facts
TRIVIA_API = "https://opentdb.com/api.php?amount=1&category=9&type=multiple"
# API for Quotes
ADVICE_API = "https://api.adviceslip.com/advice"
# API for Images
DOG_IMAGE_API = "https://dog.ceo/api/breeds/image/random"

# Set a reliable timeout
API_TIMEOUT = 10

def get_serendipity_data():
    """Fetches all required data from external APIs and handles errors."""
    
    data = {}
    
    # 1. Fetch Trivia Fact
    try:
        fact_response = requests.get(TRIVIA_API, timeout=API_TIMEOUT)
        fact_response.raise_for_status() 
        trivia_data = fact_response.json()
        
        if trivia_data['response_code'] == 0:
            result = trivia_data['results'][0]
            question = result['question'].replace("&quot;", '"').replace("&#039;", "'")
            answer = result['correct_answer'].replace("&quot;", '"').replace("&#039;", "'")
            
            fact_text = f"Q: {question}\nA: {answer}"
            data['fact'] = fact_text
        else:
            data['fact'] = "Trivia API returned no results."

    except Exception as e:
        print(f"Error fetching trivia fact: {e}")
        data['fact'] = "Trivia fact failed to load." # This is the fallback message

    # 2. Fetch Quote/Advice
    try:
        quote_response = requests.get(ADVICE_API, timeout=API_TIMEOUT)
        quote_response.raise_for_status() 
        quote_data = quote_response.json()
        data['quote'] = quote_data['slip']['advice']
    except Exception as e:
        print(f"Error fetching quote: {e}")
        data['quote'] = "Life is a journey, not a destination. (Quote API failed to load)"


    # 3. Fetch Dog Image URL 
    try:
        image_response = requests.get(DOG_IMAGE_API, timeout=API_TIMEOUT)
        image_response.raise_for_status()
        image_data = image_response.json()
        data['image_url'] = image_data['message']
    except Exception as e:
        print(f"Error fetching image: {e}")
        data['image_url'] = ""

    return data


# --- Streamlit Application Logic ---

st.set_page_config(page_title="Serendipity Generator", layout="wide")
st.title("🐍 Serendipity Generator")
st.markdown("---")

if 'data' not in st.session_state:
    st.session_state['data'] = get_serendipity_data()

if st.button('✨ Generate New Serendipity'):
    # Clear cache and fetch new data
    st.session_state['data'] = get_serendipity_data()
    # Forces Streamlit to re-run from the top to display new data
    st.rerun() 

# Display the data using columns
col1, col2, col3 = st.columns(3)
current_data = st.session_state['data']

with col1:
    st.subheader("Random Fact (Q/A)")
    st.info(current_data['fact'])

with col2:
    st.subheader("Wise-Advice")
    st.warning(f'"{current_data["quote"]}"')

with col3:
    st.subheader("Random Dog")
    image_url = current_data['image_url']
    if image_url:
        # Fixed the deprecated parameter to use_container_width=True
        st.image(image_url, caption="A good boy/girl!", use_container_width=True) 
    else:
        st.error("Image failed to load.")

st.markdown("---")

st.caption("Project built by a Ashraf k !")

