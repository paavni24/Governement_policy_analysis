import streamlit as st
import importlib.util
import os

# Path to the folder where your policy scripts are stored
POLICY_FOLDER = "lib/python3.11/site-packages/policies"

# Function to dynamically import a policy module
def load_policy_module(policy_name):
    policy_script_path = os.path.join(POLICY_FOLDER, f"{policy_name}.py")
    
    if os.path.exists(policy_script_path):
        spec = importlib.util.spec_from_file_location(policy_name, policy_script_path)
        policy_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(policy_module)
        return policy_module
    else:
        return None

# Streamlit app
st.title("Policy Query Engine")
st.subheader("Analyze and summarize policies effectively using AI.")

# Get available policy names dynamically from the folder
try:
    available_policies = [
        os.path.splitext(file)[0] for file in os.listdir(POLICY_FOLDER) if file.endswith(".py")
    ]
except FileNotFoundError:
    st.error(f"Policy folder `{POLICY_FOLDER}` not found!")
    st.stop()

if not available_policies:
    st.warning("No policy scripts found in the folder.")
    st.stop()

# Dropdown for selecting a policy
selected_policy = st.selectbox("Select a policy", available_policies)

# Load the module corresponding to the selected policy
policy_module = load_policy_module(selected_policy)

if policy_module:
    # User input for query
    query = st.text_input(
        f"Enter your query about the {selected_policy} policy",
        placeholder="e.g., Summarize the policy outcomes"
    )

    # Button to analyze the query
    if st.button("Get Analysis"):
        if query.strip():
            # Check if the required function exists in the module
            if hasattr(policy_module, "query_model"):
                with st.spinner("Generating response..."):
                    try:
                        response = policy_module.query_model(query)  # Query the model
                        st.success("Response generated successfully!")
                        st.write("**Response:**", response)
                    except Exception as e:
                        st.error(f"Error during analysis: {e}")
            else:
                st.error(f"The selected policy module does not have a `query_model` function.")
        else:
            st.warning("Please enter a query.")
else:
    st.error(f"Policy script `{selected_policy}.py` not found!")

# Footer
st.markdown(
    """
    ---
    **Developed by Paavni Singh**  
    Analyze government policies efficiently using advanced AI tools.
    """
)

