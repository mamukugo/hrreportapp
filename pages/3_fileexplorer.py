import streamlit as st

# Page title
st.title(" File Explorer")
st.write("Search for documents and files")

# Sample documents - simple list
documents = [
    {"name": "Office Tower Proposal", "type": "pdf", "keywords": "proposal office construction"},
    {"name": "Safety Protocol", "type": "docx", "keywords": "safety protocol guidelines"},
    {"name": "Budget Report Q1", "type": "xlsx", "keywords": "budget finance report"},
    {"name": "Client Contract", "type": "docx", "keywords": "contract agreement legal"},
    {"name": "Construction Schedule", "type": "xlsx", "keywords": "schedule timeline"},
    {"name": "Quality Standards", "type": "pdf", "keywords": "quality standards"}
]

# Search bar
search_term = st.text_input("Search documents", placeholder="Type keywords like 'proposal', 'safety', 'budget'...")

# Display results
if search_term:
    st.write(f"Search results for: **{search_term}**")
    
    found_docs = []
    for doc in documents:
        if search_term.lower() in doc["keywords"].lower() or search_term.lower() in doc["name"].lower():
            found_docs.append(doc)
    
    if found_docs:
        for doc in found_docs:
            # Display each document
            st.write("---")
            st.write(f"**{doc['name']}** ({doc['type'].upper()})")
            st.write(f"*Keywords: {doc['keywords']}*")
            
            # Simple download button
            if st.button(f"Download {doc['name']}", key=doc["name"]):
                st.success(f"Downloading {doc['name']}...")
    else:
        st.warning("No documents found. Try different keywords.")
        
        # Show all available documents
        st.write("### All available documents:")
        for doc in documents:
            st.write(f"- {doc['name']} ({doc['type']})")
else:
    # Show all documents when no search
    st.write("### All documents:")
    for doc in documents:
        st.write(f"- {doc['name']} ({doc['type']})")