"""ABLE C-type visual system: deep teal sidebar + service-style cards."""
from html import escape
import streamlit as st

PAGES = ["🏠 홈", "✨ 회의록 원클릭", "🎙 AI 비서", "🎯 업무 우선순위", "📅 일정 관리", "✉️ 이메일", "🔗 Google Calendar"]


def apply_theme():
    st.markdown('''<style>
    :root{--able-deep:#153D42;--able-teal:#168B87;--able-cream:#F0EEE9;--able-mint:#DCEFEB;--able-ink:#193438}
    .stApp{background:#F7F7F3;color:var(--able-ink)}
    .block-container{max-width:1260px;padding-top:1.7rem;padding-bottom:4rem}
    [data-testid="stSidebar"]{background:#153D42!important;border-right:0}
    [data-testid="stSidebar"] *{color:#F3FAF8!important}
    [data-testid="stSidebar"] input{color:#153D42!important;background:#fff!important}
    [data-testid="stSidebar"] [role="radiogroup"] label{border-radius:12px;padding:5px 8px}
    [data-testid="stSidebar"] [role="radiogroup"] label:hover{background:#24545A}
    [data-testid="stSidebar"] [data-testid="stButton"] button{border-color:#638185;background:#214E53}
    .stButton button[kind="primary"],.stFormSubmitButton button[kind="primary"]{background:#168B87!important;border-color:#168B87!important;color:white!important;border-radius:11px;font-weight:700}
    .stButton button,.stDownloadButton button,.stFormSubmitButton button{border-radius:11px}
    [data-testid="stMetric"],.metric-shell{background:#fff;border:1px solid #E0E9E5;border-radius:16px;padding:15px;box-shadow:0 3px 14px rgba(21,61,66,.04)}
    .metric-shell .big{font-size:1.65rem;font-weight:800;line-height:1.4;color:#153D42}
    .metric-shell .small{font-size:.83rem;color:#687F7D}
    .hero{background:linear-gradient(115deg,#153D42,#168B87)!important;border-radius:22px;padding:27px 31px;color:white;margin-bottom:20px}
    .hero h1,.hero p{color:white!important}
    .qbox{background:white;border:1px solid #E0E9E5;border-radius:17px;padding:17px;min-height:195px}
    .qhead{font-weight:800;font-size:1.03rem;margin-bottom:5px}
    .qhint{font-size:.78rem;color:#687F7D;margin-bottom:12px}
    .qitem{background:#F8FBFA;border:1px solid #E4ECE8;border-radius:10px;padding:9px 11px;margin:7px 0;font-size:.87rem;line-height:1.5}
    .qitem small{color:#637976}
    .priority-card{border:1px solid #E0E9E5;border-radius:16px;padding:18px 20px;margin:9px 0;background:white}
    .priority-card.featured{border-left:5px solid #168B87}
    .priority-rank,.priority-score{color:#147F7B;font-weight:800}
    .priority-score{font-size:1.5rem;white-space:nowrap}
    .source-chip{font-size:.75rem;padding:2px 7px;border-radius:9px;background:#DCEFEB;color:#153D42}
    [data-testid="stDataFrame"]{border-radius:13px;overflow:hidden}
    .able-welcome{padding:26px 2px 16px}
    .able-welcome h1{font-size:2rem;letter-spacing:-.04em;color:#153D42;margin:0 0 7px}
    .able-welcome p{color:#66807C;margin:0}
    .able-kpi{background:white;border:1px solid #E0E9E5;border-radius:17px;padding:19px;min-height:110px}
    .able-kpi span{color:#66807C;font-size:.83rem}.able-kpi strong{display:block;font-size:1.85rem;color:#153D42;margin-top:7px}
    .able-panel{background:white;border:1px solid #E0E9E5;border-radius:18px;padding:19px;margin:12px 0}
    .able-panel h3{font-size:1.08rem;color:#153D42;margin:0 0 13px}
    .able-task{padding:12px 2px;border-bottom:1px solid #ECF0ED}
    .able-task:last-child{border-bottom:0}
    .able-task b{color:#193438}.able-task small{display:block;color:#68817D;margin-top:4px}
    .cal-week{background:#E6F0ED!important;color:#153D42!important}
    .cal-today{outline:2px solid #168B87!important}
    .cal-task{background:#FFF0E8!important;color:#9B4D2D!important;border-left-color:#E9A079!important}
    .cal-meeting{background:#DCEFEB!important;color:#153D42!important;border-left-color:#168B87!important}
    @media(max-width:700px){.block-container{padding-left:1rem;padding-right:1rem}.able-welcome h1{font-size:1.55rem}.priority-card{padding:12px}}
    </style>''', unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown('## ✦ ABLE')
        st.caption('AI 업무비서 · Smart Workspace')
        st.divider()
        if 'able_page' not in st.session_state or st.session_state.able_page not in PAGES:
            st.session_state.able_page = PAGES[0]
        # Radio widget owns its key; navigation is read from the widget on each rerun.
        selected = st.radio('메뉴', PAGES, index=PAGES.index(st.session_state.able_page),
                            label_visibility='collapsed')
        st.session_state.able_page = selected
        st.divider()
        st.markdown('**개인 설정**')
        user_name = st.text_input('사용자 이름', value='김 대리', key='able_user_name')
        if st.button('대화 기록 초기화', use_container_width=True):
            st.session_state.messages = []
            st.session_state.last_answer = ''
            st.session_state.last_audio = None
            st.rerun()
        st.caption('민감한 업무 정보는 업로드 전 확인해 주세요.')
    return selected, user_name


def render_home(tasks, events, mail_draft, document, ask_callback):
    st.markdown('<div class="able-welcome"><h1>오늘의 업무를 에이블과 함께 👋</h1><p>회의록 분석부터 업무·일정·이메일 승인까지 한눈에 관리하세요.</p></div>', unsafe_allow_html=True)
    from datetime import date
    due_soon = 0
    for task in tasks:
        try:
            delta = (date.fromisoformat(str(task.get('due', ''))) - date.today()).days
            if 0 <= delta <= 3: due_soon += 1
        except (ValueError, TypeError): pass
    kpis = [('전체 업무',len(tasks)),('3일 내 마감',due_soon),('확정 일정',len(events)),('이메일 초안',1 if mail_draft else 0)]
    cols = st.columns(4)
    for col,(label,num) in zip(cols,kpis):
        with col:
            st.markdown(f'<div class="able-kpi"><span>{escape(label)}</span><strong>{num}</strong></div>',unsafe_allow_html=True)
    st.markdown('### 빠른 실행')
    a,b,c,d=st.columns(4)
    shortcuts=[(a,'📄 회의록 분석',PAGES[1]),(b,'🎙 AI 비서',PAGES[2]),(c,'🎯 우선순위',PAGES[3]),(d,'✉️ 이메일 확인',PAGES[5])]
    for col,label,page in shortcuts:
        with col:
            if st.button(label,use_container_width=True,key='shortcut_'+str(PAGES.index(page))):
                st.session_state.able_page=page
                st.rerun()
    left,right=st.columns([1.5,1],gap='large')
    with left:
        st.markdown('### 🎯 먼저 확인할 업무')
        if not tasks: st.info('회의록을 분석하면 추천 업무가 여기에 표시됩니다.')
        else:
            for i,task in enumerate(tasks[:3],1):
                name=escape(str(task.get('task') or '업무'))
                owner=escape(str(task.get('owner') or '확인 필요'))
                due=escape(str(task.get('due') or '마감일 미확인'))
                st.markdown(f'<div class="able-panel able-task"><b>{i}. {name}</b><small>담당 {owner} · 마감 {due}</small></div>',unsafe_allow_html=True)
    with right:
        st.markdown('### 📌 현재 작업 상태')
        st.info('회의록 연결됨' if document else '회의록이 아직 업로드되지 않았습니다.')
        if mail_draft: st.success('검토할 이메일 초안이 있습니다.')
        st.caption('일정 등록과 이메일 발송은 반드시 최종 승인 후 실행됩니다.')
    st.markdown('### 💬 에이블에게 바로 질문하기')
    for msg in st.session_state.messages[-6:]:
        with st.chat_message(msg['role']): st.write(msg['content'])
    question=st.chat_input('에이블에게 메시지를 보내세요...')
    if question: ask_callback(question)
