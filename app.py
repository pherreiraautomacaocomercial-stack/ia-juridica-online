import streamlit as st
import os
import json
from groq import Groq
from datetime import datetime

# Configurar página
st.set_page_config(
    page_title="IA Jurídica - Groq",
    page_icon="⚖️",
    layout="wide"
)

# Título principal
st.title("⚖️ IA Jurídica com Groq")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("🔑 Configuração")
    
    api_key = st.text_input(
        "Chave Groq API:",
        type="password",
        help="Obtenha em: https://console.groq.com"
    )
    
    st.markdown("---")
    st.info("""
    **Como obter chave:**
    1. Acesse console.groq.com
    2. Faça login/cadastro
    3. Clique em API Keys
    4. Crie nova chave
    5. Cole aqui
    """)

# Função principal da IA
def gerar_documento(tipo_documento, dados_caso, api_key):
    try:
        client = Groq(api_key=api_key)
        
        prompt = f"""
        Gere {tipo_documento} jurídico com base nestes dados:

        DADOS DO CASO:
        {json.dumps(dados_caso, indent=2, ensure_ascii=False)}

        INSTRUÇÕES:
        - Use linguagem jurídica formal brasileira
        - Fundamente com artigos de lei
        - Estruture corretamente o documento
        - Seja claro e persuasivo
        - Gere documento COMPLETO

        DOCUMENTO:
        """
        
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system", 
                    "content": "Você é um especialista jurídico brasileiro. Gere documentos precisos e tecnicamente corretos."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=4000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Erro: {str(e)}"

# Interface principal
def main():
    if not api_key:
        st.warning("⚠️ Insira sua Chave Groq API na sidebar")
        st.info("💡 Chave gratuita em: https://console.groq.com")
        return
    
    # Abas
    tab1, tab2, tab3 = st.tabs(["📝 Petição Inicial", "📄 Contrato", "⚖️ Parecer"])
    
    with tab1:
        st.header("Gerar Petição Inicial")
        
        with st.form("peticao_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Autor")
                autor_nome = st.text_input("Nome do Autor")
                autor_docs = st.text_input("CPF/CNPJ")
                
            with col2:
                st.subheader("Réu")
                reu_nome = st.text_input("Nome do Réu")
                reu_docs = st.text_input("CPF/CNPJ")
            
            fatos = st.text_area("Relato dos Fatos", height=100)
            pedidos = st.text_area("Pedidos", height=80)
            fundamentos = st.text_input("Fundamentos Legais")
            
            submitted = st.form_submit_button("🎯 Gerar Petição")
            
            if submitted:
                if not all([autor_nome, reu_nome, fatos]):
                    st.error("Preencha os campos obrigatórios!")
                    return
                
                dados = {
                    "autor": autor_nome,
                    "reu": reu_nome,
                    "fatos": fatos,
                    "pedidos": pedidos,
                    "fundamentos": fundamentos
                }
                
                with st.spinner("Gerando petição..."):
                    documento = gerar_documento("petição inicial", dados, api_key)
                
                st.success("Documento gerado!")
                st.text_area("Petição Gerada", documento, height=300)
                
                st.download_button(
                    "📥 Baixar Petição",
                    documento,
                    f"peticao_{datetime.now().strftime('%Y%m%d')}.txt"
                )
    
    with tab2:
        st.header("Gerar Contrato")
        st.info("Preencha os dados para gerar contrato personalizado")
        
        with st.form("contrato_form"):
            partes = st.text_input("Partes Contratantes")
            objeto = st.text_area("Objeto do Contrato")
            valor = st.number_input("Valor (R$)", value=1000.0)
            prazo = st.text_input("Prazo/Vigência")
            
            submitted_contrato = st.form_submit_button("📄 Gerar Contrato")
            
            if submitted_contrato:
                dados_contrato = {
                    "partes": partes,
                    "objeto": objeto,
                    "valor": valor,
                    "prazo": prazo
                }
                
                with st.spinner("Gerando contrato..."):
                    contrato = gerar_documento("contrato", dados_contrato, api_key)
                
                st.success("Contrato gerado!")
                st.text_area("Contrato Gerado", contrato, height=300)
    
    with tab3:
        st.header("Gerar Parecer Jurídico")
        st.info("Análise jurídica de situação específica")
        
        with st.form("parecer_form"):
            situacao = st.text_area("Situação para Análise", height=120)
            questionamento = st.text_input("Questão Jurídica")
            
            submitted_parecer = st.form_submit_button("⚖️ Gerar Parecer")
            
            if submitted_parecer:
                dados_parecer = {
                    "situacao": situacao,
                    "questao": questionamento
                }
                
                with st.spinner("Gerando parecer..."):
                    parecer = gerar_documento("parecer jurídico", dados_parecer, api_key)
                
                st.success("Parecer gerado!")
                st.text_area("Parecer Gerado", parecer, height=300)

if __name__ == "__main__":
    main()