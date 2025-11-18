# app.py - VERSÃO CORRIGIDA
import streamlit as st
import os
import json
import requests
from datetime import datetime
import time

# Configurar página
st.set_page_config(
    page_title="IA Jurídica Avançada - Groq",
    page_icon="⚖️",
    layout="wide"
)

# SUA CHAVE GROQ
GROQ_API_KEY = "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"

# Título principal
st.title("⚖️ IA Jurídica Avançada")
st.markdown("**Sistema profissional para geração de documentos jurídicos**")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("🎯 Status do Sistema")
    st.success("✅ Chave Groq configurada")
    st.success("✅ Sistema pronto para uso")
    
    st.markdown("---")
    st.header("📋 Documentos Disponíveis")
    st.info("""
    - 📝 Petição Inicial
    - 🛡️ Contestação
    - 📄 Contratos
    - ⚖️ Parecer Jurídico
    - 📢 Notificação Extrajudicial
    """)
    
    st.markdown("---")
    st.header("⚡ Velocidade Groq")
    st.info("""
    **Performance:**
    - ~500 tokens/segundo
    - Resposta em 2-5 segundos
    - Modelo: Llama3 70B
    - Máxima qualidade jurídica
    """)

# Classe da IA Jurídica usando requests direto
class IAJuridicaGroq:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def gerar_documento(self, tipo_documento, dados_caso):
        """Gera documento jurídico usando Groq API diretamente"""
        
        prompt = self._construir_prompt(tipo_documento, dados_caso)
        
        try:
            with st.spinner(f"🔄 Gerando {tipo_documento}..."):
                payload = {
                    "model": "llama3-70b-8192",
                    "messages": [
                        {
                            "role": "system", 
                            "content": self._construir_contexto_sistema(tipo_documento)
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.3,
                    "max_tokens": 4000,
                    "top_p": 0.9
                }
                
                response = requests.post(
                    self.base_url, 
                    headers=self.headers, 
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    return f"❌ Erro na API: {response.status_code} - {response.text}"
            
        except Exception as e:
            return f"❌ Erro na geração: {str(e)}"
    
    def _construir_contexto_sistema(self, tipo_documento):
        """Constrói contexto especializado"""
        return f"""
        Você é um especialista jurídico brasileiro com 20 anos de experiência.
        Domínio completo da legislação brasileira e jurisprudência.
        
        TAREFA: Gerar {tipo_documento.upper()} com excelência técnica.
        
        PRINCÍPIOS:
        - Linguagem jurídica formal e precisa
        - Fundamentação em artigos específicos
        - Citação de jurisprudência relevante
        - Estrutura canônica do documento
        - Análise estratégica de riscos
        - Persuasão técnica fundamentada
        
        FORMATO:
        - Documento COMPLETO e pronto para uso
        - Formatação jurídica correta
        - Divisões lógicas claras
        - Conclusão com pedidos específicos
        
        Gere o melhor documento possível para o caso concreto.
        """
    
    def _construir_prompt(self, tipo_documento, dados_caso):
        """Constrói prompt detalhado"""
        
        return f"""
        GERE {tipo_documento.upper()} JURÍDICO com máxima qualidade técnica.

        DADOS COMPLETOS DO CASO:
        {json.dumps(dados_caso, indent=2, ensure_ascii=False)}

        ESTRUTURA SOLICITADA:
        1. Cabeçalho formal com qualificação
        2. Relato detalhado dos fatos
        3. Fundamentação jurídica robusta
        4. Pedidos específicos e claros
        5. Conclusão formal

        FUNDAMENTAÇÃO EXIGIDA:
        - Cite artigos de lei aplicáveis
        - Menção a jurisprudência pertinente
        - Análise doutrinária quando cabível
        - Argumentação lógica e persuasiva

        Gere documento PRONTO PARA PROTOCOLO, com todos os elementos essenciais.
        """

# Inicializar IA
ia_juridica = IAJuridicaGroq(GROQ_API_KEY)

# Interface principal
def main():
    # Abas principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Petição Inicial", 
        "🛡️ Contestação", 
        "📄 Contratos", 
        "⚖️ Parecer Jurídico"
    ])
    
    # ABA 1: PETIÇÃO INICIAL
    with tab1:
        st.header("📝 Gerar Petição Inicial")
        st.info("Preencha os dados para gerar uma petição inicial completa")
        
        with st.form("peticao_inicial_form"):
            st.subheader("👥 Qualificação das Partes")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📋 Autor/Requerente**")
                autor_nome = st.text_input("Nome Completo:", placeholder="João Silva Santos", key="autor_nome")
                autor_cpf = st.text_input("CPF:", placeholder="123.456.789-00", key="autor_cpf")
                autor_endereco = st.text_area("Endereço Completo:", placeholder="Rua, número, bairro, cidade/UF, CEP", key="autor_end")
                autor_advogado = st.text_input("Advogado:", placeholder="Dr. Carlos Advogado - OAB/SP 123.456", key="autor_adv")
            
            with col2:
                st.markdown("**📋 Réu/Requerido**")
                reu_nome = st.text_input("Nome/Razão Social:", placeholder="Empresa XYZ Ltda", key="reu_nome")
                reu_cnpj = st.text_input("CPF/CNPJ:", placeholder="12.345.678/0001-90", key="reu_cnpj")
                reu_endereco = st.text_area("Endereço do Réu:", placeholder="Av. Comercial, 1000, Centro, São Paulo/SP", key="reu_end")
                reu_representante = st.text_input("Representante:", placeholder="Sr. Diretor Responsável", key="reu_rep")
            
            st.subheader("📖 Relato dos Fatos")
            fatos = st.text_area(
                "Descreva detalhadamente os fatos:",
                height=150,
                placeholder="Descreva cronologicamente os fatos que deram origem à ação. Inclua datas, valores, nomes de testemunhas, documentos importantes...",
                key="fatos"
            )
            
            st.subheader("🎯 Pedidos")
            pedidos = st.text_area(
                "Especifique os pedidos:",
                height=100,
                placeholder="EX: 1) Condenar o réu ao pagamento de R$ 50.000,00 por danos morais... 2) Custas processuais e honorários advocatícios...",
                key="pedidos"
            )
            
            st.subheader("⚖️ Fundamentação Jurídica")
            fundamentos = st.text_area(
                "Leis e fundamentos aplicáveis:",
                height=100,
                placeholder="EX: Art. 186 do Código Civil, Art. 927 do CC, Súmula 37 do STJ, Jurisprudência do STF...",
                key="fundamentos"
            )
            
            col_valor, col_urg = st.columns(2)
            with col_valor:
                valor_causa = st.number_input("Valor da Causa (R$):", min_value=0.0, value=10000.0, step=1000.0, key="valor")
            with col_urg:
                urgente = st.checkbox("Tutela de Urgência Necessária?", key="urgente")
            
            submitted = st.form_submit_button("🎯 GERAR PETIÇÃO INICIAL")
            
            if submitted:
                if not all([autor_nome, reu_nome, fatos, pedidos]):
                    st.error("❌ Preencha os campos obrigatórios: Autor, Réu, Fatos e Pedidos!")
                    return
                
                dados_caso = {
                    "tipo_documento": "Petição Inicial",
                    "partes": {
                        "autor": {
                            "nome": autor_nome,
                            "cpf": autor_cpf,
                            "endereco": autor_endereco,
                            "advogado": autor_advogado
                        },
                        "reu": {
                            "nome": reu_nome,
                            "cpf_cnpj": reu_cnpj,
                            "endereco": reu_endereco,
                            "representante": reu_representante
                        }
                    },
                    "fatos": fatos,
                    "pedidos": pedidos,
                    "fundamentacao": fundamentos,
                    "valor_causa": valor_causa,
                    "tutela_urgencia": urgente,
                    "data_geracao": datetime.now().strftime("%d/%m/%Y %H:%M")
                }
                
                documento = ia_juridica.gerar_documento("petição inicial", dados_caso)
                
                if not documento.startswith("❌"):
                    st.success("✅ Petição gerada com sucesso!")
                    
                    st.markdown("---")
                    st.subheader("📄 PETIÇÃO INICIAL GERADA")
                    
                    # Exibir documento
                    st.text_area("Conteúdo:", documento, height=400, key="peticao_content")
                    
                    # Botão de download
                    st.download_button(
                        label="📥 BAIXAR PETIÇÃO",
                        data=documento,
                        file_name=f"peticao_inicial_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain"
                    )
                
                else:
                    st.error(documento)
    
    # ABA 2: CONTESTAÇÃO
    with tab2:
        st.header("🛡️ Gerar Contestação")
        st.info("Resposta à petição inicial com defesa técnica")
        
        with st.form("contestacao_form"):
            st.subheader("📋 Dados do Processo")
            numero_processo = st.text_input("Número do Processo:", placeholder="0000000-00.0000.0.00.0000", key
