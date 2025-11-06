import streamlit as st
from portfolio import Portfolio
from uitls import clean_text
from chains import Chain
from langchain_community.document_loaders import WebBaseLoader



def create_streamlit_app(llm,portfolio,clean_text):
    st.title("📧 Cold Email Generator")
    url_input=st.text_input("Enter a URL:",value="https://nexusitgroup.com/job-descriptions/data-science/ml-ai-engineer/")
    submit=st.button("Submit")
    
    if submit:
        try:
            loader=WebBaseLoader([url_input])
            data=clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs=llm.extract_jobs(data)
            for job in jobs:
                skills=job.get('skills',[])
                links=portfolio.query_links(skills)
                email=llm.write_mail(jobs,links)
                st.code(email,language='markdown')
        except Exception as e:
            st.error(f"An error occured: {e}")
            
if __name__=="__main__":
    chain=Chain()              
    portfolio=Portfolio()
    st.set_page_config(layout="wide",page_title="Cold Email Generator",page_icon="📧")
    create_streamlit_app(chain,portfolio,clean_text)