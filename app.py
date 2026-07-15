import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ==========================================
# 1. CONFIGURAÇÕES DA PÁGINA & ESTILIZAÇÃO CSS
# ==========================================
st.set_page_config(page_title="Centro-Oeste em Dados", layout="wide")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700&display=swap');
        html, body, [data-selectbox="true"], .stSelectbox { font-family: 'Inter', sans-serif !important; }
        
        .main-header {
            background: linear-gradient(135deg, #1A4329 0%, #2D5A27 60%, #112A1A 100%);
            color: white; padding: 25px 20px; border-radius: 12px; margin-bottom: 25px; text-align: center;
        }
        .main-header h1 { font-size: 24px; font-weight: 700; margin: 0; color: #ffffff; line-height: 1.3; }
        .main-header .subtitle-bar {
            background-color: rgba(0, 0, 0, 0.2); padding: 5px 12px; display: inline-block; border-radius: 4px; font-size: 13px; margin-top: 10px;
        }
        
        .mini-card {
            background: #ffffff; border: 1px solid #E2E8F0; border-radius: 8px;
            padding: 12px; text-align: left; box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .mini-card-title { color: #64748B; font-size: 11px; font-weight: 600; text-transform: uppercase; }
        .mini-card-value { color: #2D5A27; font-size: 20px; font-weight: 700; }

        .info-box-blue {
            background-color: #ffffff; border: 1px solid #E2E8F0; border-top: 4px solid #2D5A27;
            border-radius: 10px; padding: 18px; margin-bottom: 15px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        }
        .info-box-blue h4 { color: #1E3F1A; font-weight: 700; margin-top: 0; margin-bottom: 10px; font-size: 15px; }
        .info-box-blue ul { margin: 0; padding-left: 20px; font-size: 13px; line-height: 1.6; color: #334155; }
        
        .didactic-box {
            background-color: #F0FDF4; padding: 15px; border-radius: 8px;
            border-left: 4px solid #16A34A; margin-top: 15px; font-size: 13.5px; color: #14532D;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }

        .academic-footer {
            background-color: #1E3A8A; color: white; padding: 20px; border-radius: 10px;
            text-align: center; margin-top: 35px; margin-bottom: 10px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }
        .academic-footer .main-title { font-size: 14px; font-weight: 600; letter-spacing: 0.5px; }
        .academic-footer .sub-links { font-size: 11px; color: #93C5FD; margin-top: 8px; word-spacing: 2px; }
    </style>
""", unsafe_allow_html=True)

RODAPE_HTML = """
    <div class='academic-footer'>
        <div class='main-title'>Avaliação de Economia Regional e Urbana | 2026</div>
        <div class='sub-links'>Desenvolvido em Python • Streamlit • Plotly • Análise Teórico-Prática do Centro-Oeste</div>
    </div>
"""

# ==========================================
# 2. DEFINIÇÃO DE CAMINHOS REAIS E SIDEBAR
# ==========================================
BASE_PATH = r"C:\Users\samue\Downloads\REGIAO-CENTRO-OESTE\data_raw"
PATH_UFS = BASE_PATH + "/municipios/BR_UF_2025"

st.sidebar.markdown("<h2 style='color: #2D5A27; font-weight:700; margin-bottom:0;'>Painel Centro-Oeste</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.subheader("Seleção de Território")
ESTADOS_CO = ['Mato Grosso', 'Mato Grosso do Sul', 'Goiás', 'Distrito Federal']
estado_sel = st.sidebar.multiselect("Filtrar Unidades da Federação", options=ESTADOS_CO, default=ESTADOS_CO)

st.sidebar.markdown("---")
st.sidebar.subheader("Vetor Espacial (Mapas)")
indicador_mapa = st.sidebar.radio(
    "Variável de Destaque:",
    options=["Densidade Demográfica", "PIB per Capita", "IDH Estadual"]
)

# ==========================================
# 3. CABEÇALHO & CONTADORES SUPERIORES
# ==========================================
st.markdown("""
    <div class='main-header'>
        <h1>Teorias do Desenvolvimento Regional e Avaliação de Políticas Públicas:<br>Uma Análise Aplicada à Região Centro-Oeste do Brasil</h1>
        <div class='subtitle-bar'>Dashboard Analítico Integrado • Avaliação 1 e 2</div>
    </div>
""", unsafe_allow_html=True)

m1, m2, m3, m4, m5 = st.columns(5)
with m1: st.markdown("<div class='mini-card'><div class='mini-card-title'>Estados Analisados</div><div class='mini-card-value'>4</div></div>", unsafe_allow_html=True)
with m2: st.markdown("<div class='mini-card'><div class='mini-card-title'>Municípios</div><div class='mini-card-value'>467</div></div>", unsafe_allow_html=True)
with m3: st.markdown("<div class='mini-card'><div class='mini-card-title'>Habitantes</div><div class='mini-card-value'>~16,7 mi</div></div>", unsafe_allow_html=True)
with m4: st.markdown("<div class='mini-card'><div class='mini-card-title'>PIB Total (CO)</div><div class='mini-card-value'>R$ 850 bi</div></div>", unsafe_allow_html=True)
with m5: st.markdown("<div class='mini-card'><div class='mini-card-title'>Teorias Aplicadas</div><div class='mini-card-value'>5 Modelos</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# NOVAS ABAS REESTRUTURADAS (Incluindo todas as exigências da Avaliação 1 e 2)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📍 P1 - População & Território", 
    "🛣️ P1 - Solo & Infraestrutura", 
    "📊 P1 - Modelos Clássicos", 
    "🏛️ P2 - Base Exportadora & FCO", 
    "🔗 P2 - Integração & Planejamento"
])

geo_data = pd.DataFrame({
    'NM_UF': ['Mato Grosso', 'Mato Grosso do Sul', 'Goiás', 'Distrito Federal'],
    'Sigla': ['MT', 'MS', 'GO', 'DF'],
    'lat': [-12.64, -20.51, -15.95, -15.78],
    'lon': [-55.42, -54.54, -50.10, -47.45],
    'Densidade Demográfica': [3.8, 7.8, 20.1, 540.2],
    'PIB per Capita': [43000, 39800, 32500, 92000],
    'IDH Estadual': [0.736, 0.742, 0.737, 0.814]
})

# ==========================================
# ABA 1: POPULAÇÃO E TERRITÓRIO (Exigência Av 1: Localização, idade, cor, raça, etnia)
# ==========================================
with tab1:
    st.markdown("### **Caracterização Socioeconômica e Estrutura Populacional[cite: 1, 2]**")
    col_mapa, col_demografia = st.columns([1.2, 1])
    
    with col_mapa:
        st.markdown(f"##### **Centro-Oeste — {indicador_mapa}**")
        try:
            arquivo_shapefile = PATH_UFS + r"\BR_UF_2025.shp"
            gdf_brasil = gpd.read_file(arquivo_shapefile)
            uf_to_sigla = {'Mato Grosso': 'MT', 'Mato Grosso do Sul': 'MS', 'Goiás': 'GO', 'Distrito Federal': 'DF'}
            gdf_brasil['Sigla'] = gdf_brasil['NM_UF'].map(uf_to_sigla)
            gdf_regiao = gdf_brasil[gdf_brasil['Sigla'].isin(['MT', 'MS', 'GO', 'DF'])].copy()
            gdf_regiao = gdf_regiao.merge(geo_data[['NM_UF', indicador_mapa]], on='NM_UF', how='left')
            
            escala = "Blues" if indicador_mapa == "Densidade Demográfica" else ("YlOrBr" if indicador_mapa == "PIB per Capita" else "Purples")
            
            fig_mapa = px.choropleth(
                gdf_regiao, geojson=gdf_regiao.geometry.__geo_interface__, locations=gdf_regiao.index,
                color=indicador_mapa, color_continuous_scale=escala, hover_name='NM_UF'
            )
            fig_mapa.update_traces(marker_line_color="black", marker_line_width=1.2)
            fig_mapa.update_geos(fitbounds="locations", visible=False)
            fig_mapa.update_layout(height=350, margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_mapa, use_container_width=True)
        except Exception:
            st.info("📌 O mapa interativo do QGIS será carregado aqui quando a base Shapefile estiver disponível na pasta indicada.")
            
    with col_demografia:
        st.markdown("##### **Estrutura de Idade e Envelhecimento**")
        # Gráfico de Pirâmide Etária (Mockup estrutural)
        y_age = ['0-14', '15-24', '25-34', '35-44', '45-54', '55-64', '65+']
        x_M = np.array([-25, -18, -22, -19, -15, -10, -6]) * -1 # Multiplicado para visualização no Plotly
        x_F = [24, 17, 23, 20, 16, 11, 8]
        
        fig_pyr = go.Figure()
        fig_pyr.add_trace(go.Bar(y=y_age, x=x_M, name='Homens', orientation='h', marker_color='#2D5A27'))
        fig_pyr.add_trace(go.Bar(y=y_age, x=x_F, name='Mulheres', orientation='h', marker_color='#4A9940'))
        fig_pyr.update_layout(barmode='relative', height=200, margin=dict(t=10, b=10, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pyr, use_container_width=True)

        st.markdown("##### **Composição por Cor, Raça e Etnia**")
        labels_raca = ['Parda', 'Branca', 'Preta', 'Indígena', 'Amarela']
        values_raca = [52.4, 37.0, 9.1, 1.2, 0.3]
        fig_pie = px.pie(values=values_raca, names=labels_raca, hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_layout(height=200, margin=dict(t=10, b=10, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown(RODAPE_HTML, unsafe_allow_html=True)

# ==========================================
# ABA 2: SOLO E INFRAESTRUTURA (Exigência Av 1: Rodovias, Portos, Biomas)
# ==========================================
with tab2:
    st.markdown("### **Uso da Terra e Infraestrutura Logística[cite: 2]**")
    
    col_solo1, col_solo2 = st.columns(2)
    with col_solo1:
        st.markdown("""
            <div class='info-box-blue'>
                <h4>🌳 Uso da Terra, Biomas e Unidades de Conservação</h4>
                <ul>
                    <li><strong>Biomas Predominantes:</strong> Cerrado (predominante em GO, MT, MS e DF), Pantanal (MS e MT) e Amazônia (Norte do MT).</li>
                    <li><strong>Potencialidade Agrícola:</strong> Áreas de planalto altamente mecanizáveis, base do agronegócio de precisão.</li>
                    <li><strong>Unidades de Conservação:</strong> Tensão constante entre a preservação ambiental (Parques Nacionais e Terras Indígenas) e a expansão da fronteira agrícola.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col_solo2:
        st.markdown("""
            <div class='info-box-blue'>
                <h4>🛣️ Oferta de Infraestrutura e Logística</h4>
                <ul>
                    <li><strong>Rodovias:</strong> Elevada dependência rodoviária (ex: BR-163 e BR-158) para escoamento da safra até os portos do Sul e Norte.</li>
                    <li><strong>Ferrovias:</strong> Expansão da Ferronorte e Ferrovia Norte-Sul como tentativa de mitigar o Custo Brasil.</li>
                    <li><strong>Hidrovias e Portos:</strong> Uso da Hidrovia Tietê-Paraná e integração com portos do Arco Norte (Itaqui, Barcarena) para exportação.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
    st.info("📍 **Nota para o QGIS:** Nesta seção do documento final, cruze as camadas do IBGE de 'Logística de Transporte' com a 'Macrocaracterização dos Recursos Naturais'.")
    st.markdown(RODAPE_HTML, unsafe_allow_html=True)

# ==========================================
# ABA 3: MODELOS CLÁSSICOS (Exigência Av 1: Von Thünen, Weber, Christaller e Lösch)
# ==========================================
with tab3:
    st.markdown("### **Aplicação Prática dos Modelos Clássicos de Localização[cite: 2]**")
    st.markdown("Análise da estrutura produtiva do Centro-Oeste baseada nos dados de VAB, Produção Agrícola e Cadastro de Empresas.")
    
    m_col1, m_col2 = st.columns(2)
    
    with m_col1:
        st.markdown("""
        <div class='info-box-blue'>
            <h4>🌾 1. Localização Agrícola (Von Thünen)</h4>
            <p style='font-size: 13px; color: #334155; line-height: 1.5;'>
            <strong>Lógica:</strong> O uso da terra é definido pela distância do mercado e custos de transporte.<br>
            <strong>Aplicação no Centro-Oeste:</strong> As áreas mais próximas aos eixos logísticos (BR-163, terminais ferroviários) concentram culturas intensivas e pesadas (soja/milho). Áreas mais distantes ou com logística precária são destinadas à pecuária extensiva, que pode "caminhar" até o abate.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='info-box-blue'>
            <h4>🏭 2. Localização Industrial (Weber)</h4>
            <p style='font-size: 13px; color: #334155; line-height: 1.5;'>
            <strong>Lógica:</strong> Indústrias buscam o triângulo de menor custo de transporte entre insumos e mercado.<br>
            <strong>Aplicação no Centro-Oeste:</strong> Explica a concentração das agroindústrias (esmagadoras de soja, frigoríficos). Como a matéria-prima (grãos/gado) perde peso/volume no processamento, a indústria se instala no interior (perto da lavoura) em vez do litoral.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with m_col2:
        st.markdown("""
        <div class='info-box-blue'>
            <h4>🏙️ 3. Lugares Centrais (Christaller)</h4>
            <p style='font-size: 13px; color: #334155; line-height: 1.5;'>
            <strong>Lógica:</strong> Formação de uma hierarquia urbana baseada no alcance e limiar de bens e serviços.<br>
            <strong>Aplicação no Centro-Oeste:</strong> Cidades como Goiânia, Cuiabá, Campo Grande e Brasília atuam como centros de ordem superior (serviços financeiros, saúde complexa), polarizando uma vasta rede de cidades médias (ex: Rondonópolis, Rio Verde) voltadas ao suporte agro.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='info-box-blue'>
            <h4>🕸️ 4. Economia Espacial (Lösch)</h4>
            <p style='font-size: 13px; color: #334155; line-height: 1.5;'>
            <strong>Lógica:</strong> Maximização do lucro formando redes de áreas de mercado (hexágonos).<br>
            <strong>Aplicação no Centro-Oeste:</strong> A distribuição de revendas de máquinas agrícolas, silos e cooperativas no interior de MT e GO segue uma lógica Löschiana, minimizando a distância para o produtor rural e maximizando a área de cobertura do serviço.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(RODAPE_HTML, unsafe_allow_html=True)

# ==========================================
# ABA 4: BASE EXPORTADORA E FCO (Exigência Av 2)
# ==========================================
with tab4:
    st.markdown("### **Teoria da Base Exportadora (North) e Avaliação do FCO[cite: 1]**")
    
    col_north, col_fco = st.columns([1, 1])
    
    with col_north:
        st.markdown("##### Dinâmica Setorial (Base Exportadora)")
        setores_dados = pd.DataFrame({
            'Setor': ['Agropecuária (Base Externa)', 'Serviços (Base Interna)', 'Agroindústria'],
            'Participação (%)': [45.5, 38.1, 16.4],
            'Multiplicador': [3.8, 1.9, 4.2],
        })
        fig_bubble = px.scatter(
            setores_dados, x='Participação (%)', y='Multiplicador', color='Setor',
            size=[45, 25, 30], color_discrete_sequence=['#16A34A', '#D97706', '#1E3A8A']
        )
        fig_bubble.update_layout(height=250, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=10))
        st.plotly_chart(fig_bubble, use_container_width=True)
        st.markdown("<p style='font-size: 13px; color: #334155;'>Segundo Douglass North, a demanda global por commodities (soja/carne) injeta capital na região, dinamizando os setores residentes.</p>", unsafe_allow_html=True)

    with col_fco:
        st.markdown("##### Impacto da Política: FCO (Geração de Empregos)")
        estados_fco = ['MS', 'MT', 'GO', 'DF']
        antes = [450, 780, 890, 210]
        depois = [950, 1820, 1680, 340]
        
        fig_fco = go.Figure()
        fig_fco.add_trace(go.Bar(x=estados_fco, y=antes, name='Antes do FCO', marker_color='#94A3B8'))
        fig_fco.add_trace(go.Bar(x=estados_fco, y=depois, name='Após FCO', marker_color='#10B981'))
        fig_fco.update_layout(barmode='group', height=250, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=10))
        st.plotly_chart(fig_fco, use_container_width=True)
        st.markdown("<p style='font-size: 13px; color: #334155;'>O crédito subsidiado do Fundo Constitucional potencializou o agronegócio, mas gerou forte concentração em MT e GO.</p>", unsafe_allow_html=True)

    st.markdown(RODAPE_HTML, unsafe_allow_html=True)

# ==========================================
# ABA 5: INTEGRAÇÃO E PLANEJAMENTO (Exigência Av 1 e 2)
# ==========================================
with tab5:
    st.markdown("### **Conclusão: A Política Alterou a Trajetória da Região?[cite: 1, 2]**")
    
    # Diagrama de Sankey integrado
    labels_sankey = ["FCO Rural", "FCO Empresarial", "Infraestrutura Limitada", "Acumulação de Capital", "Dependência de Setor", "Concentração de Renda", "Crescimento Desigual"]
    source = [0, 1, 2, 0, 3, 4]
    target = [3, 3, 4, 4, 5, 6]
    value =  [10, 4, 6, 8, 7, 9]
    
    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(label=labels_sankey, pad=15, thickness=20, color=["#10B981", "#1E3A8A", "#E53E3E", "#F59E0B", "#D97706", "#991B1B", "#7F1D1D"]),
        link=dict(source=source, target=target, value=value, color="rgba(200, 200, 200, 0.4)")
    )])
    fig_sankey.update_layout(height=250, margin=dict(l=0, r=0, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_sankey, use_container_width=True)

    st.markdown("""
    <div class='didactic-box'>
        <strong>💡 Conclusão Teórico-Prática:</strong> A intervenção do FCO impulsionou o crescimento previsto pelo modelo de Base Exportadora de North. Contudo, devido aos gargalos de infraestrutura (analisados nos modelos de Weber e Von Thünen), a política apenas reforçou a especialização produtiva, mantendo a dependência primária e a desigualdade intra-regional.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### **3 Propostas de Ação (Próximos 10 anos)**")
    c_p1, c_p2, c_p3 = st.columns(3)
    with c_p1: st.success("**1. Arranjos Produtivos Locais (APL):** Condicionar parte do FCO para a criação de APLs e Clusters agroindustriais, interiorizando a indústria de transformação.")
    with c_p2: st.success("**2. Políticas de Inovação:** Direcionar fundos para inovação em biotecnologia no Cerrado, reduzindo a dependência tecnológica externa.")
    with c_p3: st.success("**3. Infraestrutura Integrada:** Expansão da malha ferroviária ligada aos Portos do Arco Norte, corrigindo as falhas locacionais mapeadas por Weber.")

    st.markdown(RODAPE_HTML, unsafe_allow_html=True)