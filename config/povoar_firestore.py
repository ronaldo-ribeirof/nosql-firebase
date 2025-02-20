import firebase_admin
from firebase_admin import credentials, firestore
import os

# Inicializa o Firebase
cred_path = os.path.join(os.path.dirname(__file__), 'nosql-iaad-firebase-adminsdk-fbsvc-fb35983bd7.json')
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

def popular_banco_de_dados():
    dados_programadores = [
        {
            "id": "30001",
            "nome": "João Pedro",
            "genero": "M",
            "data_nasc": "23/06/1993",
            "dependentes": [{"nome": "André Sousa", "parentesco": "Filho", "data_nasc": "15/05/2020"}],
            "linguagens": ["Python", "PHP"],
            "startup_id": "10001"
        },
        {
            "id": "30002",
            "nome": "Ana Cristina",
            "genero": "F",
            "data_nasc": "19/02/1968",
            "dependentes": [],
            "linguagens": [],
            "startup_id": "10001"
        },
        {
            "id": "30003",
            "nome": "Paula Silva",
            "genero": "F",
            "data_nasc": "10/01/1986",
            "dependentes": [
                {"nome": "Luciana Silva", "parentesco": "Filha", "data_nasc": "26/07/2018"},
                {"nome": "Elisa Silva", "parentesco": "Filha", "data_nasc": "06/01/2020"},
                {"nome": "Breno Silva", "parentesco": "Esposo", "data_nasc": "21/05/1984"}
            ],
            "linguagens": ["Java"],
            "startup_id": "10002"
        },
        {
            "id": "30007",
            "nome": "Laura Marques",
            "genero": "F",
            "data_nasc": "04/10/1987",
            "dependentes": [{"nome": "Daniel Marques", "parentesco": "Filho", "data_nasc": "06/06/2014"}],
            "linguagens": ["Python", "PHP"],
            "startup_id": "10002"
        },
        {
            "id": "30003",
            "nome": "Renata Vieira",
            "genero": "F",
            "data_nasc": "05/07/1991",
            "dependentes": [],
            "linguagens": ["C", "JavaScript"],
            "startup_id": "10003"
        },
        {
            "id": "30004",
            "nome": "Felipe Santos",
            "genero": "M",
            "data_nasc": "25/11/1976",
            "dependentes": [
                {"nome": "Rafaela Santos", "parentesco": "Esposa", "data_nasc": "12/02/1980"},
                {"nome": "Marcos Martines", "parentesco": "Filho", "data_nasc": "26/03/2008"}
            ],
            "linguagens": ["JavaScript"],
            "startup_id": "10004"
        },
        {
            "id": "30006",
            "nome": "Fernando Alves",
            "genero": "M",
            "data_nasc": "07/07/1988",
            "dependentes": [{"nome": "Lais Meneses", "parentesco": "Esposa", "data_nasc": "09/11/1990"}],
            "linguagens": [],
            "startup_id": "10004"
        },
        {
            "id": "30008",
            "nome": "Lucas Lima",
            "genero": "M",
            "data_nasc": "09/10/2000",
            "dependentes": [],
            "linguagens": [],
            "startup_id": None
        },
        {
            "id": "30011",
            "nome": "Alice Lins",
            "genero": "F",
            "data_nasc": "09/10/2000",
            "dependentes": [],
            "linguagens": [],
            "startup_id": "10007"
        },
        {
            "id": "30009",
            "nome": "Camila Macedo",
            "genero": "F",
            "data_nasc": "03/07/1995",
            "dependentes": [{"nome": "Lidiane Macedo", "parentesco": "Filha", "data_nasc": "14/04/2015"}],
            "linguagens": ["C", "SQL"],
            "startup_id": None
        },
        {
            "id": "30010",
            "nome": "Leonardo Ramos",
            "genero": "M",
            "data_nasc": "05/07/2005",
            "dependentes": [],
            "linguagens": ["SQL"],
            "startup_id": None
        }
    ]

    dados_startups = [
        {"id": "10001", "nome": "Tech4Toy", "cidade_sede": "Porto Alegre"},
        {"id": "10002", "nome": "Smart123", "cidade_sede": "Belo Horizonte"},
        {"id": "10003", "nome": "knowledgeUp", "cidade_sede": "Rio de Janeiro"},
        {"id": "10004", "nome": "BSI Next Level", "cidade_sede": "Recife"},
        {"id": "10005", "nome": "QualiHealth", "cidade_sede": "São Paulo"},
        {"id": "10006", "nome": "ProEdu", "cidade_sede": "Florianópolis"},
        {"id": "10007", "nome": "CommerceIA", "cidade_sede": "Manaus"}
    ]

    dados_linguagens = [
        {"id": "20001", "nome": "Python"},
        {"id": "20002", "nome": "PHP"},
        {"id": "20003", "nome": "Java"},
        {"id": "20004", "nome": "C"},
        {"id": "20005", "nome": "JavaScript"},
        {"id": "20006", "nome": "Dart"},
        {"id": "20007", "nome": "SQL"}
    ]

    # Adiciona os dados ao Firestore
    for programador in dados_programadores:
        db.collection("programadores").document(programador["id"]).set(programador)

    for startup in dados_startups:
        db.collection("startups").document(startup["id"]).set(startup)

    for linguagem in dados_linguagens:
        db.collection("linguagens").document(linguagem["id"]).set(linguagem)

# Chama a função para popular o banco de dados
popular_banco_de_dados()
print("Banco de Dados populado com sucesso.")