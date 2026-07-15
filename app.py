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
            background: linear-gradient(135deg, #064E3B 0%, #059669 100%);
    color: white; 
    padding: 30px 20px; 
    border-radius: 12px; 
    margin-bottom: 25px; 
    text-align: left; /* Alinhado à esquerda como no modelo que você enviou */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    
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
        <div class='main-title'>Karen Vasconcelos | Avaliação de Economia Regional e Urbana | 2026</div>
        <div class='sub-links'>Desenvolvido em Python • Streamlit • Plotly • Análise Teórico-Prática do Centro-Oeste</div>
    </div>
"""

# ==========================================
# 2. DEFINIÇÃO DE CAMINHOS REAIS E SIDEBAR
# ==========================================
import os

# --- CAMINHO INTELIGENTE ---
# Se estiver no GitHub (ambiente 'STREAMLIT_SERVER_PORT'), usa a pasta raiz.
# Se estiver no seu computador, usa o seu caminho local.
if "STREAMLIT_SERVER_PORT" in os.environ:
    PATH_UFS = "BR_UF_2025" # Pasta no seu GitHub
else:
    PATH_UFS = r"C:\Users\samue\Downloads\REGIAO-CENTRO-OESTE\data_raw\municipios_e_uf\BR_UF_2025"

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
# 3. CABEÇALHO E FICHAS TÉCNICAS (ESTILO BRUNO)
# ==========================================
st.markdown("""
    <style>
    .header-box {
        background: linear-gradient(135deg, #064E3B 0%, #059669 100%);
        color: white; 
        padding: 30px 30px; 
        border-radius: 12px; 
        margin-bottom: 25px; 
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }
    </style>
    
    <div class='header-box'>
        <h1 style='font-size: 26px; margin: 0; color: white;'>Teorias do Desenvolvimento Regional e Avaliação de Políticas Públicas:</h1>
        <h2 style='font-size: 22px; margin: 5px 0 0 0; color: #E2E8F0;'>uma análise aplicada à Região Centro-Oeste do Brasil</h2>
        <p style='font-size: 14px; margin-top: 15px; color: #F0FDF4;'>Dashboard Analítico • Economia Regional e Urbana • Karen A. Vasconcelos Lucena • 2026</p>
    </div>
""", unsafe_allow_html=True)

# Minikards organizados como no exemplo
m1, m2, m3, m4, m5 = st.columns(5)
with m1: st.markdown("<div class='mini-card'><div class='mini-card-title'>Estado...</div><div class='mini-card-value'>4</div></div>", unsafe_allow_html=True)
with m2: st.markdown("<div class='mini-card'><div class='mini-card-title'>Munici...</div><div class='mini-card-value'>467</div></div>", unsafe_allow_html=True)
with m3: st.markdown("<div class='mini-card'><div class='mini-card-title'>Habita...</div><div class='mini-card-value'>16,7 mi</div></div>", unsafe_allow_html=True)
with m4: st.markdown("<div class='mini-card'><div class='mini-card-title'>PIB Total</div><div class='mini-card-value'>R$ 850 bi</div></div>", unsafe_allow_html=True)
with m5: st.markdown("<div class='mini-card'><div class='mini-card-title'>Partes...</div><div class='mini-card-value'>5</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# NOVAS ABAS REESTRUTURADAS (Incluindo todas as exigências da Avaliação 1 e 2)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📍  População & Território", 
    "🛣️  Solo & Infraestrutura", 
    "📊  Modelos Clássicos", 
    "🏛️  Base Exportadora & FCO", 
    "🔗  Integração & Planejamento"
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

import json

# ==========================================
# ABA 1: POPULAÇÃO E TERRITÓRIO
# ==========================================
with tab1:
    st.markdown("### Caracterização Socioeconômica e Estrutura Populacional")
    
    # Aumentei um pouco a proporção do mapa (1.3) para ele ter mais espaço lateral
    col_mapa, col_demografia = st.columns([1.3, 1])
    
    # Dentro da Aba 1, após o col_mapa, col_demografia = st.columns([1.3, 1])
# Ajuste a col_demografia para ser uma coluna de informações técnicas:

    with col_mapa:
        st.markdown(f"##### **{indicador_mapa} no Centro-Oeste**")
        
        try:
            # PLANO A: Tenta procurar o arquivo direto no GitHub
            try:
                arquivo_shapefile = "BR_UF_2025.shp"
                gdf_brasil = gpd.read_file(arquivo_shapefile)
            # PLANO B: Se der erro no GitHub, procura no seu computador (C:\...)
            except:
                arquivo_shapefile = r"C:\Users\samue\Downloads\REGIAO-CENTRO-OESTE\data_raw\municipios_e_uf\BR_UF_2025\BR_UF_2025.shp"
                gdf_brasil = gpd.read_file(arquivo_shapefile)
            
            # --- O resto do código continua igual ---
            geojson_brasil = json.loads(gdf_brasil.geometry.to_json())
            fig_mapa = go.Figure()

            # Fundo (Brasil cinza)
            fig_mapa.add_trace(go.Choropleth(
                geojson=geojson_brasil,
                locations=gdf_brasil.index,
                z=[1] * len(gdf_brasil),
                colorscale=[[0, '#F8FAFC'], [1, '#F8FAFC']],
                showscale=False,
                marker_line_color='#CBD5E1', 
                marker_line_width=1,
                hoverinfo='skip' 
            ))

            # Centro-Oeste colorido
            gdf_co = gdf_brasil[gdf_brasil['NM_UF'].isin(geo_data['NM_UF'])].copy()
            gdf_co = gdf_co.merge(geo_data, on='NM_UF', how='left')
            geojson_co = json.loads(gdf_co.geometry.to_json())
            
            escala = "Blues" if indicador_mapa == "Densidade Demográfica" else ("YlOrBr" if indicador_mapa == "PIB per Capita" else "Purples")

            fig_mapa.add_trace(go.Choropleth(
                geojson=geojson_co,
                locations=gdf_co.index,
                z=gdf_co[indicador_mapa],
                colorscale=escala,
                showscale=True,
                marker_line_color='#475569', 
                marker_line_width=1.5,
                hovertemplate="<b>%{customdata[0]}</b><br>" + indicador_mapa + ": %{z}<extra></extra>",
                customdata=gdf_co[['NM_UF']],
                colorbar=dict(
                    title=f"<b>{indicador_mapa}</b>", 
                    thickness=15, 
                    len=0.7,
                    yanchor="middle", y=0.5, xanchor="left", x=1.02
                )
            ))

            # Nomes dos estados
            fig_mapa.add_trace(go.Scattergeo(
                lon=geo_data['lon'],
                lat=geo_data['lat'],
                text=geo_data['NM_UF'], 
                mode='text',
                textfont=dict(size=11, color='black', family='Inter', weight='bold'),
                showlegend=False
            ))

            # Ajuste de câmera
            fig_mapa.update_layout(
                height=480, 
                margin={"r":0,"t":10,"l":0,"b":0}, 
                paper_bgcolor='rgba(0,0,0,0)',
                geo=dict(
                    visible=False,
                    lataxis_range=[-25.0, -7.0],
                    lonaxis_range=[-62.0, -44.0]
                )
            )
            
            st.plotly_chart(fig_mapa, use_container_width=True)

            if indicador_mapa == "Densidade Demográfica":
                st.markdown("<div style='background-color: #f1f5f9; padding: 10px; border-radius: 8px; border-left: 4px solid #3b82f6; font-size: 13px;'><strong>Análise:</strong> A densidade demográfica no Centro-Oeste é altamente concentrada no Distrito Federal, funcionando como núcleo urbano frente aos vazios demográficos.</div>", unsafe_allow_html=True)
            elif indicador_mapa == "PIB per Capita":
                st.markdown("<div style='background-color: #fff7ed; padding: 10px; border-radius: 8px; border-left: 4px solid #f59e0b; font-size: 13px;'><strong>Análise:</strong> O PIB reflete a dicotomia: base administrativa do DF contra a força do agro no MT/GO.</div>", unsafe_allow_html=True)
            elif indicador_mapa == "IDH Estadual":
                st.markdown("<div style='background-color: #f8fafc; padding: 10px; border-radius: 8px; border-left: 4px solid #64748b; font-size: 13px;'><strong>Análise:</strong> O IDH evidencia concentração de serviços públicos no DF em comparação à média regional.</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Erro ao carregar o mapa. Detalhe: {e}")
            
    with col_demografia:
        st.markdown("##### **Estrutura de Idade e Envelhecimento**")
        y_age = ['0-14', '15-24', '25-34', '35-44', '45-54', '55-64', '65+']
        x_M = np.array([25, 18, 22, 19, 15, 10, 6]) * -1 
        x_F = [24, 17, 23, 20, 16, 11, 8]
        
        fig_pyr = go.Figure()
        fig_pyr.add_trace(go.Bar(y=y_age, x=x_M, name='Homens (%)', orientation='h', marker_color='#1E3A8A'))
        fig_pyr.add_trace(go.Bar(y=y_age, x=x_F, name='Mulheres (%)', orientation='h', marker_color='#10B981'))
        fig_pyr.update_layout(barmode='overlay', height=200, margin=dict(t=10, b=10, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)')
        
        # O gráfico é desenhado AQUI, logo após ser criado:
        st.plotly_chart(fig_pyr, use_container_width=True)
        
        st.markdown("""
        <div style='font-size: 13px; color: #475569; margin-bottom: 20px;'>
        <strong>Comparativo Brasil:</strong> O Centro-Oeste possui uma base populacional proporcionalmente mais jovem que a média brasileira, 
        evidenciando um menor estágio de envelhecimento populacional em relação ao Sul e Sudeste.
        </div>
        """, unsafe_allow_html=True)

        # --- COR E RAÇA (CÓDIGO COMPLETO) ---
        st.markdown("##### **Composição por Cor e Raça (Censo IBGE)**")
        labels_raca = ['Parda', 'Branca', 'Preta', 'Indígena', 'Amarela']
        values_raca = [52.4, 37.0, 9.1, 1.2, 0.3]
        
        fig_pie = px.pie(values=values_raca, names=labels_raca, hole=0.45, 
                         color_discrete_sequence=['#D97706', '#FDE047', '#78350F', '#16A34A', '#94A3B8'])
        fig_pie.update_layout(height=200, margin=dict(t=10, b=10, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        
        # O gráfico é desenhado AQUI, logo após ser criado:
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("""
        <div style='font-size: 13px; color: #475569; margin-bottom: 20px;'>
        <strong>Comparativo Brasil:</strong> A maior predominância da população parda no Centro-Oeste reflete a intensa dinâmica de 
        migração interna e ocupação territorial da região, divergindo ligeiramente da média nacional de autodeclaração branca.
        </div>
        """, unsafe_allow_html=True)

    st.markdown(RODAPE_HTML, unsafe_allow_html=True)

# ==========================================
# ABA 2: SOLO E INFRAESTRUTURA
# ==========================================
with tab2:
    st.markdown("### **Uso da Terra e Infraestrutura Logística**")
    
    # --- PRIMEIRA LINHA: USO DO SOLO E BIOMAS ---
    col_solo1, col_graf_solo = st.columns([1, 1.2])
    
    with col_solo1:
        st.markdown("""
            <div class='info-box-blue' style='height: 100%; border-top: 4px solid #16A34A;'>
                <h4>🌳 Uso da Terra e Biomas</h4>
                <ul>
                    <li><strong>Biomas Predominantes:</strong> O <em>Cerrado</em> domina a região central. A <em>Amazônia</em> ocupa o norte do Mato Grosso e o <em>Pantanal</em> divide MT e MS.</li>
                    <li><strong>Potencialidade Agrícola:</strong> Áreas de planalto (chapadas) altamente mecanizáveis, base do agronegócio de precisão.</li>
                    <li><strong>Unidades de Conservação:</strong> A expansão agropecuária gera tensão direta com terras indígenas e áreas de conservação ambiental.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
    with col_graf_solo:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### **Distribuição de Biomas (CO)**")
            df_bioma = pd.DataFrame({'Bioma': ['Cerrado', 'Amazônia', 'Pantanal', 'Mata Atlântica (MS/GO)'], 'Área (%)': [58, 28, 10, 4]})
            fig_bioma = px.pie(df_bioma, values='Área (%)', names='Bioma', hole=0.5, color_discrete_sequence=['#EAB308', '#22C55E', '#3B82F6', '#14532D'])
            fig_bioma.update_layout(height=230, margin=dict(t=10, b=10, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig_bioma, use_container_width=True)
            
        with c2:
            st.markdown("##### **Status do Uso do Solo**")
            df_uso = pd.DataFrame({'Categoria': ['Vegetação Nativa / Conservação', 'Pastagens (Pecuária)', 'Agricultura (Lavouras)', 'Outros (Urbano/Água)'], 'Área (%)': [45, 32, 20, 3]})
            fig_uso = px.bar(df_uso, x='Área (%)', y='Categoria', orientation='h', color='Categoria', text='Área (%)',
                             color_discrete_sequence=['#15803D', '#CA8A04', '#1D4ED8', '#64748B'])
            fig_uso.update_layout(height=230, margin=dict(t=10, b=10, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', showlegend=False, xaxis=dict(visible=False), yaxis=dict(title=''))
            st.plotly_chart(fig_uso, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- SEGUNDA LINHA: INFRAESTRUTURA E LOGÍSTICA ---
    col_log1, col_graf_log = st.columns([1, 1.2])
    
    with col_log1:
        st.markdown("""
            <div class='info-box-blue' style='height: 100%; border-top: 4px solid #1E3A8A;'>
                <h4>🛣️ Matriz de Transporte e Escoamento</h4>
                <ul>
                    <li><strong>Rodovias (Predominância):</strong> Extrema dependência das rodovias (BR-163, BR-158) para escoar soja e milho, elevando o custo do frete (Custo Brasil).</li>
                    <li><strong>Ferrovias (Em expansão):</strong> A Ferronorte (Malha Norte) e a Norte-Sul são vitais, mas ainda insuficientes para a demanda total.</li>
                    <li><strong>Arco Norte e Portos:</strong> Uso da Hidrovia Tietê-Paraná e integração estratégica com portos no Norte (Itaqui-MA, Barcarena-PA) para fugir do congestionamento no Porto de Santos-SP.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
    with col_graf_log:
        st.markdown("##### **Matriz de Transporte de Grãos: Centro-Oeste vs. Ideal (Custos)**")
        df_modal = pd.DataFrame({
            'Modal de Transporte': ['Rodoviário', 'Ferroviário', 'Hidroviário'],
            'Situação Atual (CO) (%)': [65, 25, 10],
            'Cenário Ideal (Eficiência) (%)': [30, 45, 25]
        })
        
        # Transformando os dados para gráfico agrupado
        df_modal_melted = df_modal.melt(id_vars='Modal de Transporte', var_name='Cenário', value_name='Participação (%)')
        
        fig_modal = px.bar(df_modal_melted, x='Modal de Transporte', y='Participação (%)', color='Cenário', barmode='group',
                           color_discrete_sequence=['#EF4444', '#10B981'], text_auto=True)
        fig_modal.update_layout(height=250, margin=dict(t=10, b=10, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)',
                                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
        st.plotly_chart(fig_modal, use_container_width=True)

    st.markdown(RODAPE_HTML, unsafe_allow_html=True)

# ==========================================
# ABA 3: MODELOS CLÁSSICOS (GRÁFICOS APLICADOS AO CENTRO-OESTE)
# ==========================================
with tab3:
    st.markdown("### **Aplicação Prática dos Modelos Clássicos na Região Centro-Oeste**")
    st.markdown("Abaixo, traduzimos as teorias de localização em dados visuais baseados na dinâmica produtiva e gargalos de infraestrutura de MT, MS, GO e DF.")
    
    m_col1, m_col2 = st.columns(2)
    
    with m_col1:
        # GRAFICO 1 EM CIMA
        df_thunen = pd.DataFrame({
            'Distância da BR-163 / Ferrovias': ['Até 50 km', '50-150 km', '150-300 km', '+300 km (Fronteira)'],
            'Uso da Terra': ['Soja e Milho (Intensivo)', 'Algodão e Integração', 'Pecuária Semi-intensiva', 'Pecuária Extensiva'],
            'Rentabilidade da Terra': [95, 75, 45, 20]
        })
        fig_thunen = px.bar(df_thunen, x='Distância da BR-163 / Ferrovias', y='Rentabilidade da Terra', 
                            color='Uso da Terra', color_discrete_sequence=['#16A34A', '#F59E0B', '#D97706', '#8B4513'])
        fig_thunen.update_layout(height=230, margin=dict(t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', legend=dict(font=dict(size=10)))
        st.plotly_chart(fig_thunen, use_container_width=True)

        # TEXTO 1 EMBAIXO
        st.markdown("""
        <div class='info-box-blue'>
            <h4>🌾 1. Von Thünen: Uso da Terra vs. Logística</h4>
            <p style='font-size: 13px; color: #334155; line-height: 1.5;'>
            <strong>Aplicação na Região:</strong> No Mato Grosso e Goiás, o cultivo de grãos pesados (que possuem alto custo de transporte) disputa os terrenos mecanizáveis colados aos eixos rodoviários (BR-163, BR-158) e aos terminais ferroviários. Conforme nos afastamos desses eixos centrais rumo ao interior do Pantanal ou norte do MT, o custo do frete inviabiliza o grão, e a terra passa a ser ocupada pela pecuária bovina extensiva, já que o gado "se transporta vivo" e exige menos logística viária.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # GRAFICO 3 EM CIMA
        df_chris = pd.DataFrame({
            'Hierarquia (Centro-Oeste)': ['Metrópole (DF e Goiânia)', 'Capital Regional (Cuiabá e CG)', 'Polo Agro (Ex: Rio Verde)', 'Apoio Local'],
            'Raio de Influência (Pessoas)': [3000000, 1000000, 250000, 30000],
            'Complexidade de Serviços': [100, 75, 40, 10]
        })
        fig_chris = px.scatter(df_chris, x='Raio de Influência (Pessoas)', y='Complexidade de Serviços', 
                               size='Raio de Influência (Pessoas)', color='Hierarquia (Centro-Oeste)', text='Hierarquia (Centro-Oeste)',
                               color_discrete_sequence=px.colors.qualitative.Prism)
        fig_chris.update_traces(textposition='bottom center', textfont_size=10)
        fig_chris.update_layout(height=250, margin=dict(t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig_chris, use_container_width=True)

        # TEXTO 3 EMBAIXO
        st.markdown("""
        <div class='info-box-blue'>
            <h4>🏙️ 3. Christaller: Lugares Centrais e Hierarquia Urbana</h4>
            <p style='font-size: 13px; color: #334155; line-height: 1.5;'>
            <strong>Aplicação na Região:</strong> O modelo explica perfeitamente a urbanização polarizada do Centro-Oeste. Brasília (DF) e Goiânia funcionam como "Metrópoles Centrais", oferecendo serviços de alcance máximo (tribunais superiores, hospitais de alta complexidade). Cuiabá e Campo Grande dominam seus estados como capitais regionais, enquanto cidades como Rondonópolis (MT) e Rio Verde (GO) surgem como "nós" vitais de ordem média, servindo como centrais financeiras e de maquinário para a elite do agronegócio.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with m_col2:
        # GRAFICO 2 EM CIMA
        df_weber = pd.DataFrame({
            'Localização da Esmagadora de Soja': ['Interior (Perto da Lavouras no CO)', 'Litoral (Perto do Porto exportador)'],
            'Custo Frete: Matéria-Prima (Grão In Natura)': [15, 85],
            'Custo Frete: Produto Final (Farelo/Óleo)': [55, 10]
        })
        fig_weber = px.bar(df_weber, x='Localização da Esmagadora de Soja', y=['Custo Frete: Matéria-Prima (Grão In Natura)', 'Custo Frete: Produto Final (Farelo/Óleo)'], 
                           barmode='stack', color_discrete_sequence=['#2D5A27', '#94A3B8'],
                           labels={'value': 'Índice de Custo Logístico', 'variable': 'Componente de Frete'})
        fig_weber.update_layout(height=230, margin=dict(t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', legend=dict(font=dict(size=10), orientation="h", y=-0.2))
        st.plotly_chart(fig_weber, use_container_width=True)

        # TEXTO 2 EMBAIXO
        st.markdown("""
        <div class='info-box-blue'>
            <h4>🏭 2. Weber: Localização Industrial (O Triângulo Locacional)</h4>
            <p style='font-size: 13px; color: #334155; line-height: 1.5;'>
            <strong>Aplicação na Região:</strong> Por que a agroindústria se instala em Jataí (GO) ou Lucas do Rio Verde (MT) e não nos portos de Santos/Paranaguá? Pelo "índice de perda de peso" de Weber. Processar soja em farelo e óleo ou abater o boi faz com que a matéria-prima perca peso e volume. Para minimizar custos totais de frete, a indústria decide se ancorar próxima à fonte primária no Centro-Oeste, exportando o produto já transformado (e mais leve/fácil de transportar).
            </p>
        </div>
        """, unsafe_allow_html=True)

        # GRAFICO 4 EM CIMA
        df_losch = pd.DataFrame({
            'Raio de Captação (km)': [40, 150, 400],
            'Volume de Recebimento (Mil Toneladas)': [25, 180, 600],
            'Rede de Atuação (MT/GO/MS)': ['Silo Local (Secagem Básica)', 'Armazém Intermediário', 'Cooperativa Central']
        })
        fig_losch = px.line(df_losch, x='Raio de Captação (km)', y='Volume de Recebimento (Mil Toneladas)', markers=True, text='Rede de Atuação (MT/GO/MS)')
        fig_losch.update_traces(textposition='top left', marker=dict(size=12, color="#E53E3E"), line=dict(color="#E53E3E", width=2))
        fig_losch.update_layout(height=250, margin=dict(t=10, b=10), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_losch, use_container_width=True)

        # TEXTO 4 EMBAIXO
        st.markdown("""
        <div class='info-box-blue'>
            <h4>🕸️ 4. Lösch: Economia Espacial e Redes de Mercado</h4>
            <p style='font-size: 13px; color: #334155; line-height: 1.5;'>
            <strong>Aplicação na Região:</strong> A teoria da rede hexagonal de Lösch é perfeitamente visível no mapeamento de cooperativas (como a COMIGO em Goiás) e na rede de concessionárias de tratores. Elas se distribuem espacialmente no interior do Centro-Oeste buscando não sobrepor áreas de concorrência, garantindo que nenhum produtor rural viaje distâncias insustentáveis para entregar grãos ou acessar manutenção técnica. É a otimização pura da área de mercado.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(RODAPE_HTML, unsafe_allow_html=True)

# ==========================================
# ABA 4: BASE EXPORTADORA E FCO (Exigência Av 2)
# ==========================================
with tab4:
    st.markdown("### **Teoria da Base Exportadora (North) e Avaliação do FCO**")
    
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

    # --- NOVA SEÇÃO DE EXPLICAÇÃO TEÓRICA (AVALIAÇÃO 2) ---
    st.markdown("---")
    st.markdown("#### **Interpretação Econômica Aplicada à Região Centro-Oeste**")
    
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        st.markdown("""
        <div class='info-box-blue' style='height: 100%;'>
            <h4>🌍 Teoria da Base Exportadora (Douglass North)</h4>
            <p style='font-size: 13.5px; color: #334155; line-height: 1.6; text-align: justify;'>
            <strong>O Conceito:</strong> A teoria postula que o motor do crescimento regional é a sua "base de exportação" — setores que produzem para a demanda externa, trazendo capital novo para dentro da região.<br><br>
            <strong>Aplicação no Centro-Oeste:</strong> A base exportadora da região é o <strong>complexo agroindustrial (soja, milho, algodão e carnes)</strong>. A exportação massiva dessas commodities atrai um alto fluxo de renda. Esse capital injetado estimula, por efeito multiplicador, as chamadas "atividades residentes" ou não-básicas (comércio local, serviços urbanos, setor imobiliário). É esse fenômeno que explica o crescimento vertiginoso de serviços e a forte urbanização em polos do agronegócio, como Sinop (MT), Sorriso (MT) e Rio Verde (GO).
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_exp2:
        st.markdown("""
        <div class='info-box-blue' style='height: 100%; border-top: 4px solid #1E3A8A;'>
            <h4>🏦 Política Pública: O Papel do FCO</h4>
            <p style='font-size: 13.5px; color: #334155; line-height: 1.6; text-align: justify;'>
            <strong>O Conceito:</strong> O Fundo Constitucional de Financiamento do Centro-Oeste (FCO) utiliza crédito subsidiado como instrumento de fomento para desenvolver os setores produtivos e tentar reduzir as desigualdades intra-regionais[cite: 1].<br><br>
            <strong>Aplicação no Centro-Oeste:</strong> Na prática, o FCO funcionou como o combustível vital para a consolidação da Teoria de North na região. Ele financiou a modernização tecnológica do campo (máquinas, silos) e a instalação de agroindústrias. Embora tenha gerado forte expansão de emprego e renda, seus resultados mostram que o crédito tendeu a acompanhar a lógica de mercado, concentrando-se nos estados de maior dinamismo (Mato Grosso e Goiás). Isso evidencia a necessidade de ajustes nos instrumentos da política para alcançar áreas de menor desenvolvimento.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(RODAPE_HTML, unsafe_allow_html=True)

# ==========================================
# ABA 5: INTEGRAÇÃO E PLANEJAMENTO (Exigência Av 1 e 2)
# ==========================================
with tab5:
    st.markdown("###  A Política Alterou a Trajetória da Região?")
    
    # --- NOVO FLUXOGRAMA VISUAL (PLOTLY SHAPES) ---
    fig_flow = go.Figure()

    # Função para desenhar as caixas retangulares (Blocos do Fluxograma)
    def add_node(fig, x, y, text, color):
        # Shapes aceitam "layer"
        fig.add_shape(type="rect",
            x0=x-0.22, y0=y-0.12, x1=x+0.22, y1=y+0.12,
            fillcolor=color, line=dict(color="white", width=2),
            layer="above", opacity=0.95
        )
        # Annotations NÃO aceitam "layer", foi removido aqui
        fig.add_annotation(
            x=x, y=y, text=text, showarrow=False,
            font=dict(color="white", size=13, family="Inter"),
            align="center"
        )

    # Função para desenhar as setas conectando os blocos
    def add_arrow(fig, x0, y0, x1, y1):
        # Annotations NÃO aceitam "layer", foi removido aqui
        fig.add_annotation(
            x=x1, y=y1, ax=x0, ay=y0,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2.5, arrowcolor="#94A3B8"
        )

    # 1. Desenhando as setas (as conexões vêm primeiro)
    add_arrow(fig_flow, 0.5, 0.88, 0.5, 0.62)    # FCO -> North
    add_arrow(fig_flow, 0.5, 0.48, 0.25, 0.22)   # North -> Positivos
    add_arrow(fig_flow, 0.5, 0.48, 0.75, 0.22)   # North -> Gargalos
    add_arrow(fig_flow, 0.25, 0.08, 0.5, -0.18)  # Positivos -> Planejamento
    add_arrow(fig_flow, 0.75, 0.08, 0.5, -0.18)  # Gargalos -> Planejamento

    # 2. Desenhando os blocos de texto (Nós do Fluxograma)
    add_node(fig_flow, 0.5, 1.0, "<b>1. Intervenção Pública (FCO)</b><br>Crédito subsidiado para os setores<br>estratégicos do Centro-Oeste", "#1E3A8A") 
    add_node(fig_flow, 0.5, 0.50, "<b>2. Motor de Crescimento (North)</b><br>Dinamização da Base Exportadora<br>(Soja, Milho, Algodão e Pecuária)", "#10B981") 
    add_node(fig_flow, 0.25, 0.10, "<b>3. Impactos Positivos Alcançados</b><br>Geração de empregos formais<br>Adensamento agroindustrial", "#16A34A") 
    add_node(fig_flow, 0.75, 0.10, "<b>4. Desafios Locacionais (Weber/Von Thünen)</b><br>Concentração de renda intra-regional<br>Gargalos de infraestrutura rodoviária", "#E53E3E") 
    add_node(fig_flow, 0.5, -0.30, "<b>5. Planejamento Estratégico</b><br>Implementação de APLs, novas ferrovias<br>e fomento contínuo à inovação", "#D97706") 

    # 3. Limpando o fundo do gráfico para ficar transparente e bonito
    fig_flow.update_layout(
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[-0.45, 1.15]),
        height=520, margin=dict(l=0, r=0, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    
    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig_flow, use_container_width=True)

    # --- TEXTO DE SÍNTESE E PROPOSTAS ---
    st.markdown("""
    <div class='didactic-box'>
        <strong>💡 Síntese Teórico-Prática:</strong> O fluxograma evidencia que a intervenção da política do FCO impulsionou o crescimento previsto pelo modelo de Base Exportadora de North[cite: 1]. Contudo, devido aos gargalos logísticos crônicos (como alertam os modelos de Weber e Von Thünen), a política financeira, atuando isolada, acabou reforçando a especialização produtiva local, sustentando a dependência do setor primário e as disparidades econômicas entre os municípios da região.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### **3 Propostas de Ação para os próximos 10 anos**")
    c_p1, c_p2, c_p3 = st.columns(3)
    with c_p1: 
        st.success("**1. Arranjos Produtivos Locais (APL):** Condicionar obrigatoriamente fatias do FCO para o fomento de APLs e Clusters agroindustriais, interiorizando a indústria de transformação.")
    with c_p2: 
        st.success("**2. Políticas de Inovação:** Direcionar fundos estratégicos para centros de pesquisa em biotecnologia e defensivos biológicos no Cerrado, reduzindo a dependência externa.")
    with c_p3: 
        st.success("**3. Infraestrutura Integrada:** Financiar a expansão urgente da malha ferroviária (conexão com Portos do Arco Norte) para mitigar as barreiras de custo-distância previstas por Weber.")

    st.markdown(RODAPE_HTML, unsafe_allow_html=True)
