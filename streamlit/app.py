import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Verifica se o Firebase já foi inicializado
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate({
        "type": os.getenv("GOOGLE_TYPE"),
        "project_id": os.getenv("GOOGLE_PROJECT_ID"),
        "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
        "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace('\\n', '\n'),
        "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
        "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_X509_CERT_URL")
    })
    firebase_admin.initialize_app(cred)

db = firestore.client()
# Referências às coleções
programadores_ref = db.collection('programadores')
startups_ref = db.collection('startups')

# Funções CRUD para Programadores

def criar_programador(id, nome, genero, data_nasc, dependentes, linguagens, startup_id):
    doc_ref = programadores_ref.document(id)  # Cria um novo documento com ID fornecido
    doc_ref.set({
        'id': id,
        'nome': nome,
        'genero': genero,
        'data_nasc': data_nasc.strftime('%d/%m/%Y'),  # Formata a data para dd/mm/aaaa
        'dependentes': dependentes,
        'linguagens': linguagens,
        'startup_id': startup_id
    })
    return doc_ref.id  # Retorna o ID do documento criado

def ler_programadores():
    programadores = []
    docs = programadores_ref.stream()
    for doc in docs:
        programadores.append(doc.to_dict())
    return programadores

def atualizar_programador(id, nome, genero, data_nasc, dependentes, linguagens, startup_id):
    doc_ref = programadores_ref.document(id)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.update({
            'nome': nome,
            'genero': genero,
            'data_nasc': data_nasc.strftime('%d/%m/%Y'),  # Formata a data para dd/mm/aaaa
            'dependentes': dependentes,
            'linguagens': linguagens,
            'startup_id': startup_id
        })
        return True
    else:
        return False

def deletar_programador(id):
    doc_ref = programadores_ref.document(id)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.delete()
        return True
    else:
        return False

# Funções CRUD para Startups

def criar_startup(id, nome, cidade_sede):
    doc_ref = startups_ref.document(id)  # Cria um novo documento com ID fornecido
    doc_ref.set({
        'id': id,
        'nome': nome,
        'cidade_sede': cidade_sede
    })
    return doc_ref.id  # Retorna o ID do documento criado

def ler_startups():
    startups = []
    docs = startups_ref.stream()
    for doc in docs:
        startups.append(doc.to_dict())
    return startups

def atualizar_startup(id, nome, cidade_sede):
    doc_ref = startups_ref.document(id)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.update({
            'nome': nome,
            'cidade_sede': cidade_sede
        })
        return True
    else:
        return False

def deletar_startup(id):
    doc_ref = startups_ref.document(id)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.delete()
        print(f"Startup com ID {id} deletada com sucesso.")
        return True
    else:
        print(f"Startup com ID {id} não encontrada.")
        return False

# Interface Streamlit

st.title("CRUD de Programadores e Startups")

# Inicializa a lista de dependentes na sessão
if 'dependentes' not in st.session_state:
    st.session_state.dependentes = []

# Função para adicionar dependente
def adicionar_dependente(nome, parentesco, data_nasc):
    st.session_state.dependentes.append({"nome": nome, "parentesco": parentesco, "data_nasc": data_nasc.strftime('%d/%m/%Y')})

# Formulário para criar programador
st.subheader("Criar Programador")
with st.form(key='criar_programador_form'):
    id = st.text_input("ID do Programador")
    nome = st.text_input("Nome")
    genero = st.selectbox("Gênero", ["M", "F"])
    data_nasc = st.date_input("Data de Nascimento", min_value=datetime(1900, 1, 1), max_value=datetime.now(), format="DD/MM/YYYY")
    dependente_nome = st.text_input("Nome do Dependente")
    dependente_parentesco = st.text_input("Parentesco do Dependente")
    dependente_data_nasc = st.date_input("Data de Nascimento do Dependente", min_value=datetime(1900, 1, 1), max_value=datetime.now(), format="DD/MM/YYYY")
    if st.form_submit_button("Adicionar Dependente"):
        adicionar_dependente(dependente_nome, dependente_parentesco, dependente_data_nasc)
    linguagens_opcoes = ["Python", "Java", "JavaScript", "C", "C++", "PHP", "SQL"]
    linguagens = st.multiselect("Linguagens", linguagens_opcoes)
    outras_linguagens = st.text_input("Outras Linguagens (separadas por vírgula)")
    startup_id = st.text_input("ID da Startup")
    submit_button = st.form_submit_button(label='Criar Programador')

    if submit_button:
        linguagens += outras_linguagens.split(",") if outras_linguagens else []
        criar_programador(id, nome, genero, data_nasc, st.session_state.dependentes, linguagens, startup_id)
        st.success("Programador criado com sucesso!")
        st.session_state.dependentes.clear()  # Limpa a lista de dependentes após a criação

# Exibir dependentes adicionados
st.subheader("Dependentes Adicionados")
for dependente in st.session_state.dependentes:
    st.write(f"**Nome:** {dependente['nome']}")
    st.write(f"**Parentesco:** {dependente['parentesco']}")
    st.write(f"**Data de Nascimento:** {dependente['data_nasc']}")
    st.write("---")

# Formulário para atualizar programador
st.subheader("Atualizar Programador")
with st.form(key='atualizar_programador_form'):
    id = st.text_input("ID do Programador")
    nome = st.text_input("Nome")
    genero = st.selectbox("Gênero", ["M", "F"])
    data_nasc = st.date_input("Data de Nascimento", min_value=datetime(1900, 1, 1), max_value=datetime.now(), format="DD/MM/YYYY")
    dependente_nome = st.text_input("Nome do Dependente")
    dependente_parentesco = st.text_input("Parentesco do Dependente")
    dependente_data_nasc = st.date_input("Data de Nascimento do Dependente", min_value=datetime(1900, 1, 1), max_value=datetime.now(), format="DD/MM/YYYY")
    if st.form_submit_button("Adicionar Dependente"):
        adicionar_dependente(dependente_nome, dependente_parentesco, dependente_data_nasc)
    linguagens_opcoes = ["Python", "Java", "JavaScript", "C", "C++", "PHP", "SQL"]
    linguagens = st.multiselect("Linguagens", linguagens_opcoes)
    outras_linguagens = st.text_input("Outras Linguagens (separadas por vírgula)")
    startup_id = st.text_input("ID da Startup")
    submit_button = st.form_submit_button(label='Atualizar Programador')

    if submit_button:
        linguagens += outras_linguagens.split(",") if outras_linguagens else []
        if atualizar_programador(id, nome, genero, data_nasc, st.session_state.dependentes, linguagens, startup_id):
            st.success("Programador atualizado com sucesso!")
        else:
            st.error("ID do Programador não encontrado!")
        st.session_state.dependentes.clear()  # Limpa a lista de dependentes após a atualização

# Exibir dependentes adicionados
st.subheader("Dependentes Adicionados")
for dependente in st.session_state.dependentes:
    st.write(f"**Nome:** {dependente['nome']}")
    st.write(f"**Parentesco:** {dependente['parentesco']}")
    st.write(f"**Data de Nascimento:** {dependente['data_nasc']}")
    st.write("---")

# Formulário para deletar programador
st.subheader("Deletar Programador")
with st.form(key='deletar_programador_form'):
    id = st.text_input("ID do Programador")
    submit_button = st.form_submit_button(label='Deletar Programador')

    if submit_button:
        if deletar_programador(id):
            st.success("Programador deletado com sucesso!")
        else:
            st.error("ID do Programador não encontrado!")

# Formulário para criar startup
st.subheader("Criar Startup")
with st.form(key='criar_startup_form'):
    id = st.text_input("ID da Startup")
    nome = st.text_input("Nome da Startup")
    cidade_sede = st.text_input("Cidade Sede")
    submit_button = st.form_submit_button(label='Criar Startup')

    if submit_button:
        criar_startup(id, nome, cidade_sede)
        st.success("Startup criada com sucesso!")

# Formulário para atualizar startup
st.subheader("Atualizar Startup")
with st.form(key='atualizar_startup_form'):
    id = st.text_input("ID da Startup")
    nome = st.text_input("Nome da Startup")
    cidade_sede = st.text_input("Cidade Sede")
    submit_button = st.form_submit_button(label='Atualizar Startup')

    if submit_button:
        if atualizar_startup(id, nome, cidade_sede):
            st.success("Startup atualizada com sucesso!")
        else:
            st.error("ID da Startup não encontrado!")

# Formulário para deletar startup
st.subheader("Deletar Startup")
with st.form(key='deletar_startup_form'):
    id = st.text_input("ID da Startup")
    submit_button = st.form_submit_button(label='Deletar Startup')

    if submit_button:
        if deletar_startup(id):
            st.success("Startup deletada com sucesso!")
        else:
            st.error("ID da Startup não encontrado!")

# Exibição dos dados com filtros
st.subheader("Exibição dos Dados")

# Filtros para programadores
st.write("Filtros para Programadores")
filtro_genero = st.selectbox("Filtrar por Gênero", ["Todos", "M", "F"])
filtro_linguagens = st.text_input("Filtrar por Linguagens (separadas por vírgula)")

programadores = ler_programadores()
if filtro_genero != "Todos":
    programadores = [p for p in programadores if p['genero'] == filtro_genero]
if filtro_linguagens:
    linguagens = filtro_linguagens.split(",")
    programadores = [p for p in programadores if any(l in p['linguagens'] for l in linguagens)]

# Exibição dos programadores
expander_programadores = st.expander("Programadores", expanded=True)
with expander_programadores:
    for programador in programadores:
        st.write(f"**ID:** {programador['id']}")
        st.write(f"**Nome:** {programador['nome']}")
        st.write(f"**Gênero:** {programador['genero']}")
        st.write(f"**Data de Nascimento:** {programador['data_nasc']}")
        st.write(f"**Linguagens:** {', '.join(programador['linguagens'])}")
        st.write(f"**Startup ID:** {programador['startup_id']}")
        st.write("**Dependentes:**")
        for dependente in programador['dependentes']:
            st.write(f"  - {dependente['nome']} ({dependente['parentesco']}, {dependente['data_nasc']})")
        st.write("---")

# Filtros para startups
st.write("Filtros para Startups")
filtro_cidade = st.text_input("Filtrar por Cidade Sede")

startups = ler_startups()
if filtro_cidade:
    startups = [s for s in startups if s['cidade_sede'] == filtro_cidade]

# Exibição das startups
expander_startups = st.expander("Startups", expanded=True)
with expander_startups:
    for startup in startups:
        st.write(f"**ID:** {startup['id']}")
        st.write(f"**Nome:** {startup['nome']}")
        st.write(f"**Cidade Sede:** {startup['cidade_sede']}")
        st.write("---")

# Exemplo de consulta e exibição em tabela
st.subheader("Consulta de Programadores e Startups")
consulta = []
for programador in programadores:
    startup_nome = next((s['nome'] for s in startups if s['id'] == programador['startup_id']), " ")
    consulta.append({
        "Nome do Programador": programador['nome'],
        "Nome da Startup": startup_nome,
        "Linguagens": ', '.join(programador['linguagens']),
        "Quantidade de Linguagens": len(programador['linguagens'])
    })

st.write("### Tabela de Consulta")
st.table(consulta)

# Exibir o código da consulta
st.write("### Código da Consulta")
codigo_consulta = """
consulta = []
for programador in programadores:
    startup_nome = next((s['nome'] for s in startups if s['id'] == programador['startup_id']), " ")
    consulta.append({
        "Nome do Programador": programador['nome'],
        "Nome da Startup": startup_nome,
        "Linguagens": ', '.join(programador['linguagens']),
        "Quantidade de Linguagens": len(programador['linguagens'])
    })

st.table(consulta)
"""
st.code(codigo_consulta, language='python')