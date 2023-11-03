# from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.callbacks.base import BaseCallbackHandler
import streamlit as st

# load_dotenv()

template = """
1. 당신은 기업 ESG 보고서 작성하는 전문가 입니다.
2. {DS} 공시기준에 해당하는 실제 외부에 공시할 수 있는 ESG 보고서를 {lang} 언어로 이어 작성해줘.
3. {DS} 공시기준에 해당하는 테이블도 포함해줘.
4. {DS}라는 공시기준에 맞게 다음 주어지는 Text에 이어질 ESG 보고서의 일부분을 작성해줘: {text}
"""

davinch3 = OpenAI(
    model_name='text-davinci-003',
    max_tokens = 1000,
    temperature=1, 
    streaming=True,
)

system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

# answer = chatgpt(chat_prompt.format_prompt(DS = 'GRI 2021 > GRI 2: General Disclosures 2021 > 거버넌스 > 2-9 지배구조 및 구성', lang='Korean', text='우리가 지금까지').to_messages())
# print(answer.content)


DS_list = [
    {
		'DS': 'GRI 2021 > GRI 2: General Disclosures 2021 > 거버넌스 > 2-9 지배구조 및 구성',
        'label': '2-9 지배구조 및 구성',
        'lang': 'Korean',
        'text': '우리가 생각하는'
	}, 
    {
		'DS': 'GRI 2021 > GRI 2: General Disclosures 2021 > 거버넌스 > 2-10 최고의사결정기구의 추천 및 선정',
        'label': '2-10 최고의사결정기구의 추천 및 선정',
        'lang': 'Korean',
		'text': '안녕하세요',
	},
    {
		'DS': 'GRI 2021 > GRI 2: General Disclosures 2021 > 거버넌스 > 2-11 최고의사결정기구의 의장',
        'label': '2-11 최고의사결정기구의 의장',
        'lang': 'Korean',
        'text': '적어도',
	},
]



class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text=initial_text
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text+=token
        self.container.markdown(self.text)

def gen_ai_service(service):
    return {
        'service_name': 'Report AI Service',
        'DS': DS_list
    }

def generate_report(index):
    current_text = st.session_state.get(f'textarea-{index}', '')
    chat_box = st.empty()
    stream_handler = StreamHandler(chat_box)
    llm = ChatOpenAI(model_name="gpt-4", temperature=1, streaming=True, callbacks=[stream_handler], max_tokens=600)
    chat_prompt_instance = chat_prompt.format_prompt(DS=DS_list[index]['DS'], lang=DS_list[index]['lang'], text=current_text)
    answer = llm(chat_prompt_instance.to_messages())
    st.session_state[f'result-{index}'] = answer
    
def add_to_text_area(index):
    if f'result-{index}' in st.session_state:
        st.session_state[f'textarea-{index}'] = st.session_state[f'result-{index}']

service = st.sidebar.selectbox("Pick a Service", ("Report AI", "PDF AI", "Chatting AI"))
response = gen_ai_service(service)
container = st.container()
response = gen_ai_service(service)
DS = response['DS']
col1, col2= st.columns(2)
result_container = st.empty()

st.title("섬섬 Report AI")

with st.container():
	st.text_area(DS_list[0]['label'], value=st.session_state.get(f'textarea-{0}', ''), placeholder='리포트 내용을 입력해주세요.', key=f'textarea-{0}', height=650)

	st.write("**리포트 결과**")
	if st.button('자동 생성', key=f'button-{0}'):
			generate_report(0)

st.header('')
st.header('')

with st.container():                  
		st.text_area(DS_list[1]['label'], value=st.session_state.get(f'textarea-{1}', ''), placeholder='리포트 내용을 입력해주세요.', key=f'textarea-{1}', height=650)
		st.write("**리포트 결과**")
		if st.button('자동 생성', key=f'button-{1}'):
				generate_report(1)

st.header('')
st.header('')

with st.container():                      
		st.text_area(DS_list[2]['label'], value=st.session_state.get(f'textarea-{2}', ''), placeholder='리포트 내용을 입력해주세요.', key=f'textarea-{2}', height=650)
		st.write("**리포트 결과**")
		if st.button('자동 생성', key=f'button-{2}'):
				generate_report(2)