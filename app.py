import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

from google import genai
from google.genai import types

from config import SYSTEM_INSTRUCTION

# =========================================
# CONFIGURAÇÃO
# =========================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": "*"}}
)

# =========================================
# FUNÇÃO GEMINI
# =========================================

def ask_gemini(prompt):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=2
        )
    )

    try:
        return response.text
    except:
        return "Erro ao gerar resposta."

# =========================================
# ROTA PRINCIPAL
# =========================================

@app.route("/")
def home():

    return jsonify({
        "status": "online",
        "message": "LoveAI funcionando ❤️"
    })

# =========================================
# RF01 - CANTADAS
# =========================================

@app.route("/cantada", methods=["POST"])
def gerar_cantada():

    data = request.get_json()

    personalidade = data.get("personalidade")
    estilo = data.get("estilo")

    if not personalidade or not estilo:
        return jsonify({
            "erro": "Envie personalidade e estilo"
        }), 400

    prompt = f"""
    Crie 5 cantadas para uma pessoa com personalidade:
    {personalidade}

    O estilo da cantada deve ser:
    {estilo}

    Seja criativo, divertido e natural.
    """

    resposta = ask_gemini(prompt)

    return jsonify({
        "status": "success",
        "cantadas": resposta
    })

# =========================================
# RF02 - PRESENTES
# =========================================

@app.route("/presente", methods=["POST"])
def gerar_presente():

    data = request.get_json()

    renda = data.get("renda")
    gostos = data.get("gostos")

    if not renda or not gostos:
        return jsonify({
            "erro": "Envie renda e gostos"
        }), 400

    prompt = f"""
    Sugira presentes criativos para uma pessoa
    que gosta de:

    {gostos}

    O orçamento é:
    {renda}

    Inclua:
    - presentes baratos
    - presentes criativos
    - experiências românticas
    """

    resposta = ask_gemini(prompt)

    return jsonify({
        "status": "success",
        "presentes": resposta
    })

# =========================================
# RF03 - CONSELHOS
# =========================================

@app.route("/conselho", methods=["POST"])
def conselho():

    data = request.get_json()

    problema = data.get("problema")

    if not problema:
        return jsonify({
            "erro": "Envie o problema"
        }), 400

    prompt = f"""
    Um usuário precisa de um conselho amoroso.

    Situação:
    {problema}

    Responda de forma empática,
    inteligente e útil.
    """

    resposta = ask_gemini(prompt)

    return jsonify({
        "status": "success",
        "conselho": resposta
    })

# =========================================
# START
# =========================================

if __name__ == "__main__":
    app.run(debug=True)