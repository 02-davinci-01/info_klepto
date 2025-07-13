import streamlit as st
import time
from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from parse import parse_with_ollama
import concurrent.futures

st.title("Info-Klepto")
st.markdown("<h2 style='font-size:22px; font-family:Courier New, monospace'>by vedant nagwanshi</h2>", unsafe_allow_html=True)
url = st.text_input("Enter a website as a url:")

# Track processing time
if "processing_metrics" not in st.session_state:
    st.session_state.processing_metrics = {}

if st.button("Klepto"):
    try:
        start_time = time.time()
        
        with st.spinner("Scraping the website..."):
            result = scrape_website(url)
            
            if not result:
                st.error("Failed to scrape the website. Please check the URL and try again.")
                st.stop()
                
            body_content = extract_body_content(result)
            cleaned_content = clean_body_content(body_content)
            
            if not cleaned_content:
                st.warning("No content found to parse. The page might be empty or requires JavaScript to load content.")
                st.stop()
                
            st.session_state.dom_content = cleaned_content
            
            scrape_time = time.time() - start_time
            st.session_state.processing_metrics["scrape_time"] = f"{scrape_time:.2f} seconds"
            
        with st.expander("View DOM Content"):
            st.text_area("DOM content", cleaned_content, height=300)
            
        st.success(f"Scraping completed in {scrape_time:.2f} seconds!")
        
    except Exception as e:
        st.error(f"An error occurred during scraping: {str(e)}")

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")
    
    col1, col2 = st.columns(2)
    with col1:
        use_parallel = st.checkbox("Use parallel processing", value=True, 
                                 help="Process content chunks in parallel for faster results")
    
    with col2:
        chunk_size = st.slider("Chunk size", min_value=1000, max_value=10000, value=6000, 
                             help="Smaller chunks may be processed faster but require more API calls")
    
    if st.button("Parse Content"):
        if not parse_description:
            st.warning("Please describe what you want to parse.")
            st.stop()
            
        try:
            start_time = time.time()
            
            with st.spinner("Parsing the content..."):
                dom_chunks = split_dom_content(st.session_state.dom_content, max_length=chunk_size)
                
                # Show progress indicator
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Either process in parallel or sequentially
                if use_parallel and len(dom_chunks) > 1:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        # Create a list of futures
                        futures = {
                            executor.submit(parse_with_ollama, chunk, parse_description): i 
                            for i, chunk in enumerate(dom_chunks)
                        }
                        
                        results = [""] * len(dom_chunks)  # Pre-allocate results list
                        
                        # Process as they complete
                        for i, future in enumerate(concurrent.futures.as_completed(futures)):
                            chunk_index = futures[future]
                            try:
                                results[chunk_index] = future.result()
                            except Exception as e:
                                results[chunk_index] = f"Error processing chunk {chunk_index+1}: {str(e)}"
                            
                            # Update progress
                            progress = (i + 1) / len(dom_chunks)
                            progress_bar.progress(progress)
                            status_text.text(f"Processed {i+1} of {len(dom_chunks)} chunks ({int(progress*100)}%)")
                            
                    parsed_result = "\n".join(filter(None, results))
                else:
                    # Sequential processing
                    results = []
                    for i, chunk in enumerate(dom_chunks):
                        result = parse_with_ollama(chunk, parse_description)
                        results.append(result)
                        
                        # Update progress
                        progress = (i + 1) / len(dom_chunks)
                        progress_bar.progress(progress)
                        status_text.text(f"Processed {i+1} of {len(dom_chunks)} chunks ({int(progress*100)}%)")
                    
                    parsed_result = "\n".join(filter(None, results))
                
                parse_time = time.time() - start_time
                st.session_state.processing_metrics["parse_time"] = f"{parse_time:.2f} seconds"
                
          
            progress_bar.empty()
            status_text.empty()
            
            if not parsed_result.strip():
                st.info("No matching content found based on your description.")
            else:
                st.subheader("Parsed Result")
                st.write(parsed_result)
                
            st.success(f"Parsing completed in {parse_time:.2f} seconds!")
            
            # Show metrics
            with st.expander("Processing Metrics"):
                for key, value in st.session_state.processing_metrics.items():
                    st.text(f"{key.replace('_', ' ').title()}: {value}")
                
        except Exception as e:
            st.error(f"An error occurred during parsing: {str(e)}")


st.markdown("""
    <div style="
        background-color: #f9f9f9;
        padding: 10px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    ">
    <h4 style='text-align:center; color:#333;'>Demo</h4>
""", unsafe_allow_html=True)

# Display the video
video_file = open('info_klepto.mp4', 'rb')
video_bytes = video_file.read()
st.video(video_bytes)

# Close the container
st.markdown("</div>", unsafe_allow_html=True)