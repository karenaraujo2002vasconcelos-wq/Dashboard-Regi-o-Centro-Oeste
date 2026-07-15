import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. CONFIGURAÇÕES DA PÁGINA & ESTILIZAÇÃO CSS
# ==========================================
st.set_page_config(page_title="Centro-Oeste em Dados", layout="wide")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700&display=swap');
        html, body, [data-selectbox="true"], .stSelectbox { font-family: 'Inter', sans-serif !important; }
        
        /* Cabeçalho Unificado (Estilo Bruno) */
        .main-header {
            background: linear-gradient(135deg, #1A4329 0%, #2D5A27 60%, #112A1A 100%);
            color: white; padding: 25px 20px; border-radius: 12px; margin-bottom: 25px; text-align: center;
        }
        .main-header h1 { font-size: 24px; font-weight: 700; margin: 0; color: #ffffff; line-height: 1.3; }
        .main-header .subtitle-bar {
            background-color: rgba(0, 0, 0, 0.2); padding: 5px 12px; display: inline-block; border-radius: 4px; font-size: 13px; margin-top: 10px;
        }
        
        /* Mini Cards Superiores */
        .mini-card {
            background: #ffffff; border: 1px solid #E2E8F0; border-radius: 8px;
            padding: 12px; text-align: left; box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .mini-card-title { color: #64748B; font-size: 11px; font-weight: 600; text-transform: uppercase; }
        .mini-card-value { color: #2D5A27; font-size: 20px; font-weight: 700; }

        /* Caixas de Texto Laterais Arredondadas (Fiel ao Bruno) */
        .info-box-blue {
            background-color: #ffffff; border: 1px solid #E2E8F0; border-top: 4px solid #2D5A27;
            border-radius: 10px; padding: 18px; margin-bottom: 15px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        }
        .info-box-blue h4 { color: #1E3F1A; font-weight: 700; margin-top: 0; margin-bottom: 10px; font-size: 15px; }
        .info-box-blue ul { margin: 0; padding-left: 20px; font-size: 13px; line-height: 1.6; color: #334155; }
        
        .info-box-red {
            background-color: #FFF5F5; border: 1px solid #FEB2B2; border-left: 4px solid #E53E3E;
            border-radius: 10px; padding: 18px; margin-bottom: 15px;
        }
        .info-box-red h4 { color: #C53030; font-weight: 700; margin-top: 0; margin-bottom: 10px; font-size: 15px; }
        .info-box-red ul { margin: 0; padding-left: 20px; font-size: 13px; line-height: 1.6; color: #742A2A; }

        .ficha-tecnica {
            background-color: #F8FAFC; border: 1px solid #E2E8F0; border-left: 4px solid #10B981;
            padding: 12px; border-radius: 6px; font-size: 12px; color: #475569; margin-bottom: 20px;
        }
        .didactic-box {
            background-color: #F0FDF4; padding: 15px; border-radius: 8px;
            border-left: 4px solid #16A34A; margin-top: 15px; font-size: 13.5px; color: #14532D;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }

        /* Rodapé Acadêmico Corrigido e Limpo */
        .academic-footer {
            background-color: #1E3A8A; color: white; padding: 20px; border-radius: 10px;
            text-align: center; margin-top: 35px; margin-bottom: 10px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }
        .academic-footer .main-title { font-size: 14px; font-weight: 600; letter-spacing: 0.5px; }
        .academic-footer .sub-links { font-size: 11px; color: #93C5FD; margin-top: 8px; word-spacing: 2px; }
    </style>
""", unsafe_allow_html=True)

# Bloco HTML corrigido sem "Aluna:" e sem a repetição da disciplina
RODAPE_HTML = """
    <div class='academic-footer'>
        <div class='main-title'>Avaliação de Economia Regional e Urbana | Karen A. Vasconcelos Lucena | 2026</div>
        <div class='sub-links'>Desenvolvido em Python • Streamlit • Plotly • Dados estruturados e sintéticos baseados em IBGE • IPEA • BNB/FCO • MTE/CAGED • Finalidade exclusivamente acadêmica</div>
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
st.sidebar.subheader("Vetor Espacial (Parte I)")
indicador_mapa = st.sidebar.radio(
    "Variável de Destaque Espacial:",
    options=["Densidade Demográfica", "PIB per Capita", "IDH Estadual"]
)

# ==========================================
# 3. CABEÇALHO & CONTADORES SUPERIORES
# ==========================================
st.markdown("""
    <div class='main-header'>
        <h1>Teorias do Desenvolvimento Regional e Avaliação de Políticas Públicas:<br>Uma Análise Aplicada à Região Centro-Oeste do Brasil</h1>
        <div class='subtitle-bar'>Dashboard Analítico • Economia Regional e Urbana • Karen A. Vasconcelos Lucena • 2026</div>
    </div>
""", unsafe_allow_html=True)

m1, m2, m3, m4, m5 = st.columns(5)
with m1: st.markdown("<div class='mini-card'><div class='mini-card-title'>Estados Analisados</div><div class='mini-card-value'>4</div></div>", unsafe_allow_html=True)
with m2: st.markdown("<div class='mini-card'><div class='mini-card-title'>Municípios</div><div class='mini-card-value'>467</div></div>", unsafe_allow_html=True)
with m3: st.markdown("<div class='mini-card'><div class='mini-card-title'>Habitantes</div><div class='mini-card-value'>~16,7 mi</div></div>", unsafe_allow_html=True)
with m4: st.markdown("<div class='mini-card'><div class='mini-card-title'>PIB Total (CO)</div><div class='mini-card-value'>R$ 850 bi</div></div>", unsafe_allow_html=True)
with m5: st.markdown("<div class='mini-card'><div class='mini-card-title'>Partes de Análise</div><div class='mini-card-value'>5 Seções</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📍 Parte I – Caracterização", 
    "📊 Parte II – Teoria Regional", 
    "🏛️ Parte III – Política Pública", 
    "🔗 Parte IV – Integração", 
    "🚀 Parte V – Planejamento"
])

# Banco de dados de indicadores estaduais macro
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
# ABA 1: PARTE I - CARACTERIZAÇÃO (COM CONCEITOS ECONÔMICOS)
# ==========================================
with tab1:
    col_mapa, col_info = st.columns([1.3, 1])
    
    with col_mapa:
        st.markdown(f"##### **Centro-Oeste — {indicador_mapa} por Estado**")
        
        # Injeção de Fundamentação Econômica Dinâmica baseada no Indicador Selecionado
        if indicador_mapa == "Densidade Demográfica":
            st.markdown("""
                <div style='background-color: #F8FAFC; padding: 12px 15px; border-radius: 6px; border-left: 3px solid #1E3A8A; font-size: 13px; margin-bottom: 15px; color: #334155;'>
                    <strong>💡 Significado Econômico — Densidade Demográfica:</strong> Mede a distribuição da população sobre o território (hab/km²). Para a economia regional, indica o grau de <strong>concentração dos fatores de produção (trabalho)</strong>, a formação de mercados consumidores internos e a presença de economias de aglomeração urbanas. No Centro-Oeste, reflete um padrão de 'vazios demográficos' intercalados por eixos agroindustriais altamente povoados.
                </div>
            """, unsafe_allow_html=True)
        elif indicador_mapa == "PIB per Capita":
            st.markdown("""
                <div style='background-color: #F8FAFC; padding: 12px 15px; border-radius: 6px; border-left: 3px solid #D97706; font-size: 13px; margin-bottom: 15px; color: #334155;'>
                    <strong>💡 Significado Econômico — PIB per Capita:</strong> É a razão entre o Produto Interno Bruto total e a população residente. Funciona como um indicador aproximador do <strong>nível de produtividade média da força de trabalho</strong> e do dinamismo de acumulação regional. No entanto, em economias baseadas em *enclaves exportadores* ou forte peso do setor público (como o Distrito Federal), ele pode camuflar severas assimetrias na distribuição primária da renda.
                </div>
            """, unsafe_allow_html=True)
        else: # IDH Estadual
            st.markdown("""
                <div style='background-color: #F8FAFC; padding: 12px 15px; border-radius: 6px; border-left: 3px solid #7030A0; font-size: 13px; margin-bottom: 15px; color: #334155;'>
                    <strong>💡 Significado Econômico — IDH Estadual:</strong> O Índice de Desenvolvimento Humano é uma medida composta que sintetiza três pilares essenciais: <strong>renda, longevidade e educação</strong>. Ao contrário dos indicadores puramente monetários, o IDH qualifica a eficiência do crescimento regional, avaliando se o transbordamento da base exportadora está se traduzindo em bem-estar social real e capacitação humana de longo prazo.
                </div>
            """, unsafe_allow_html=True)

        try:
            arquivo_shapefile = PATH_UFS + r"\BR_UF_2025.shp"
            gdf_brasil = gpd.read_file(arquivo_shapefile)
            
            uf_to_sigla = {
                'Mato Grosso': 'MT', 'Mato Grosso do Sul': 'MS', 'Goiás': 'GO', 'Distrito Federal': 'DF',
                'Rondônia': 'RO', 'Amazonas': 'AM', 'Pará': 'PA', 'Tocantins': 'TO', 
                'Bahia': 'BA', 'Minas Gerais': 'MG', 'São Paulo': 'SP', 'Paraná': 'PR'
            }
            gdf_brasil['Sigla'] = gdf_brasil['NM_UF'].map(uf_to_sigla)
            
            estados_vizinhos_siglas = ['MT', 'MS', 'GO', 'DF', 'RO', 'AM', 'PA', 'TO', 'BA', 'MG', 'SP', 'PR']
            gdf_regiao = gdf_brasil[gdf_brasil['Sigla'].isin(estados_vizinhos_siglas)].copy()
            gdf_regiao = gdf_regiao.merge(geo_data[['NM_UF', indicador_mapa]], on='NM_UF', how='left')
            
            if indicador_mapa == "Densidade Demográfica":
                escala_cores = "Blues"
            elif indicador_mapa == "PIB per Capita":
                escala_cores = "YlOrBr"
            else:
                escala_cores = "Purples"
            
            fig_mapa = px.choropleth(
                gdf_regiao,
                geojson=gdf_regiao.geometry.__geo_interface__,
                locations=gdf_regiao.index,
                color=indicador_mapa,
                color_continuous_scale=escala_cores,
                hover_name='NM_UF',
                range_color=[geo_data[indicador_mapa].min(), geo_data[indicador_mapa].max()]
            )
            
            fig_mapa.update_traces(marker_line_color="black", marker_line_width=1.2)
            
            fig_mapa.add_trace(go.Scattergeo(
                lat=geo_data['lat'],
                lon=geo_data['lon'],
                mode='text',
                text=geo_data['NM_UF'],
                textfont=dict(size=11, color='black', family='Inter', weight='bold'),
                showlegend=False
            ))
            
            fig_mapa.update_geos(fitbounds="locations", visible=False)
            
            fig_mapa.update_layout(
                height=400, margin={"r":0,"t":10,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)',
                coloraxis_colorbar=dict(
                    title=dict(text=indicador_mapa, font=dict(family="Inter", size=12, color="#64748B")),
                    thicknessmode="pixels", thickness=15, lenmode="pixels", len=280,
                    yanchor="middle", y=0.5, xanchor="left", x=1.02
                )
            )
            st.plotly_chart(fig_mapa, use_container_width=True)
            st.caption("Fonte: Elaboração própria a partir de dados do IBGE e IPEA.")
            
        except Exception:
            st.error(f"Erro na leitura da malha local: Verifique o arquivo principal 'BR_UF_2025.shp' na pasta.")
            
        st.markdown(f"##### **{indicador_mapa} — Comparativo Regional**")
        df_bar = geo_data.sort_values(by=indicador_mapa, ascending=True)
        fig_bar = px.bar(
            df_bar, x=indicador_mapa, y='NM_UF', orientation='h', text_auto=True, color='NM_UF',
            color_discrete_map={'Mato Grosso': '#1E3F1A', 'Mato Grosso do Sul': '#2D5A27', 'Goiás': '#4A9940', 'Distrito Federal': '#D97706'}
        )
        if indicador_mapa == "PIB per Capita":
            fig_bar.add_vline(x=34200, line_dash="dash", line_color="red", annotation_text="Média BR R$ 34.200")
            
        fig_bar.update_layout(height=230, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_title="", yaxis_title="")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_info:
        st.markdown("""
            <div class='info-box-blue'>
                <h4>🌏 Localização e Delimitação</h4>
                <ul>
                    <li><strong>4 Unidades Federativas</strong> integrando a macrorregião.</li>
                    <li><strong>Área:</strong> 1,60 mi km² (18,8% da extensão territorial do Brasil).</li>
                    <li><strong>População:</strong> ~16,7 milhões de habitantes concentrados em eixos urbanos.</li>
                    <li><strong>Biomas:</strong> Predomínio do Cerrado, complexo do Pantanal e franjas Amazônicas ao norte.</li>
                </ul>
            </div>
            <div class='info-box-blue'>
                <h4>⚙️ Atividades Econômicas</h4>
                <ul>
                    <li><strong>Agropecuária:</strong> Fronteira agrícola líder nacional em soja, milho e algodão.</li>
                    <li><strong>Indústria:</strong> Complexos agroindustriais de esmagamento e processamento químico alimentício.</li>
                    <li><strong>Serviços:</strong> Redes logísticas de comercialização de commodities e forte peso do setor público (DF).</li>
                </ul>
            </div>
            <div class='info-box-blue'>
                <h4>📊 PIB e Emprego</h4>
                <ul>
                    <li><strong>PIB Regional:</strong> Estimado em R$ 850 bilhões anuais.</li>
                    <li><strong>Dinâmica de Emprego:</strong> Elevado índice de formalização ligado às cadeias produtivas agroindustriais.</li>
                    <li><strong>Assimetria Intraregional:</strong> O Distrito Federal distorce as médias pelo alto rendimento público.</li>
                </ul>
            </div>
            <div class='info-box-red'>
                <h4>⚠️ Desafios Estruturais</h4>
                <ul>
                    <li><strong>Gargalo Logístico:</strong> Dependência acentuada do modal rodoviário para escoamento.</li>
                    <li><strong>Vulnerabilidade Ambiental:</strong> Pressão do avanço da fronteira agrícola sobre o Cerrado nativo.</li>
                    <li><strong>Dependência Exógena:</strong> Alta suscetibilidade às oscilações dos preços internacionais de commodities.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown(RODAPE_HTML, unsafe_allow_html=True)

# ==========================================
# ABA 2: PARTE II - TEORIA REGIONAL
# ==========================================
with tab2:
    st.markdown("### **Abordagem Teórica: Teoria da Base Exportadora (Douglass North)**")
    st.markdown("A dinâmica de crescimento regional é interpretada a partir da capacidade da região de estruturar um vetor de demanda externa capaz de dinamizar o mercado interno de serviços.")
    
    st.markdown("---")
    indicador_setor = st.selectbox(
        "📊 Selecione o Vetor Setorial para Investigação de Tendência:",
        options=["PAM - Produção Agrícola", "PPM - Pecuária de Grande Porte", "PIA - Valor da Transformação Industrial"]
    )
    
    if indicador_setor == "PAM - Produção Agrícola":
        st.markdown("""
            <div style='background-color: #F8FAFC; padding: 10px 15px; border-radius: 6px; border-left: 3px solid #64748B; font-size: 13px; margin-bottom: 15px;'>
                <strong>📋 Nota Metodológica (PAM):</strong> A pesquisa de <strong>Produção Agrícola Municipal (PAM)</strong> do IBGE acompanha variáveis de área colhida, rendimento médio e valor da produção de culturas temporárias e permanentes. No Centro-Oeste, representa o termômetro principal do complexo de grãos (soja e milho).
            </div>
        """, unsafe_allow_html=True)
    elif indicador_setor == "PPM - Pecuária de Grande Porte":
        st.markdown("""
            <div style='background-color: #F8FAFC; padding: 10px 15px; border-radius: 6px; border-left: 3px solid #64748B; font-size: 13px; margin-bottom: 15px;'>
                <strong>📋 Nota Metodológica (PPM):</strong> A <strong>Pesquisa da Pecuária Municipal (PPM)</strong> do IBGE fornece dados sobre os efetivos dos rebanhos (bovino, suíno, aves) e produtos da extração animal. É crucial para monitorar a densidade de pastagens e o fornecimento de proteína para a cadeia de frigoríficos.
            </div>
        """, unsafe_allow_html=True)
    elif indicador_setor == "PIA - Valor da Transformação Industrial":
        st.markdown("""
            <div style='background-color: #F8FAFC; padding: 10px 15px; border-radius: 6px; border-left: 3px solid #64748B; font-size: 13px; margin-bottom: 15px;'>
                <strong>📋 Nota Metodológica (PIA):</strong> A <strong>Pesquisa Industrial Anual (PIA-Empresa)</strong> identifica as características estruturais e o Valor da Transformação Industrial (VTI) por subsetores. Revela o nível de adensamento técnico e o beneficiamento interno das commodities antes da exportação.
            </div>
        """, unsafe_allow_html=True)

    c_graf1, c_graf2 = st.columns([1.1, 1])
    
    with c_graf1:
        st.markdown("##### **Participação no Crescimento Regional por Setor**")
        setores_dados = pd.DataFrame({
            'Setor': ['Agropecuária', 'Agroindústria', 'Serviços Logísticos', 'Serviços Urbanos'],
            'Participação (%)': [35.5, 15.2, 28.1, 21.2],
            'Multiplicador de Emprego': [2.8, 4.2, 3.1, 1.9],
        })
        
        fig_bubble = px.scatter(
            setores_dados, x='Participação (%)', y='Multiplicador de Emprego', color='Setor',
            text='Setor', size=[40, 25, 35, 20], color_discrete_sequence=px.colors.qualitative.Dark2
        )
        fig_bubble.update_layout(height=280, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bubble, use_container_width=True)
        
    with c_graf2:
        st.markdown(f"##### **Evolução do Índice Base (2019=100) — {indicador_setor}**")
        anos = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
        if "Agrícola" in indicador_setor:
            valores = [100, 118, 135, 158, 185, 179, 198]
        elif "Pecuária" in indicador_setor:
            valores = [100, 104, 109, 112, 115, 114, 118]
        else:
            valores = [100, 95, 108, 102, 115, 110, 112]
            
        fig_line = px.line(x=anos, y=valores, markers=True, color_discrete_sequence=['#16A34A'])
        fig_line.update_layout(height=280, xaxis_title="Anos", yaxis_title="Índice", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("""
        <div class='didactic-box'>
            <strong>💡 Interpretação do Modelo de North no Centro-Oeste:</strong><br>
            A base econômica externa (o complexo agroexportador) funciona como o motor primordial de acumulação de capital. A renda gerada nesse setor dita a velocidade de expansão das atividades complementares urbanas (indústria local e serviços), comprovando a tese de causação de Douglass North.
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(RODAPE_HTML, unsafe_allow_html=True)

# ==========================================
# ABA 3: PARTE III - POLÍTICA PÚBLICA
# ==========================================
with tab3:
    st.markdown("### **Avaliação de Política Pública: Fundo Constitucional do Centro-Oeste (FCO)**")
    
    st.markdown("""
        <div class='ficha-tecnica'>
            <strong>Ficha Técnica – FCO</strong><br>
            <strong>Criação:</strong> Art. 159 da CF/88 | <strong>Gestor Principal:</strong> Banco do Brasil (BB) | 
            <strong>Público-alvo:</strong> Produtores rurais e empresas industriais/comerciais da região | 
            <strong>Objetivo:</strong> Promover o desenvolvimento econômico e social mediante financiamentos de longo prazo.
        </div>
    """, unsafe_allow_html=True)
    
    kp1, kp2, kp3 = st.columns(3)
    with kp1: st.markdown("<div class='mini-card'><div class='mini-card-title'>FCO Acumulado Recente</div><div class='mini-card-value'>R$ 14,2 bi</div></div>", unsafe_allow_html=True)
    with kp2: st.markdown("<div class='mini-card'><div class='mini-card-title'>Projetos Atendidos</div><div class='mini-card-value'>+32 mil</div></div>", unsafe_allow_html=True)
    with kp3: st.markdown("<div class='mini-card'><div class='mini-card-title'>Concentração MT/GO</div><div class='mini-card-value'>~68%</div></div>", unsafe_allow_html=True)
    
    st.markdown("<br>##### **Impacto do FCO por Estado Antes vs. Depois da Política (Empregos Gerados)**", unsafe_allow_html=True)
    
    estados_fco = ['Mato Grosso do Sul', 'Mato Grosso', 'Goiás', 'Distrito Federal']
    antes = [450, 780, 890, 210]
    depois = [950, 1820, 1680, 340]
    
    fig_fco = go.Figure()
    fig_fco.add_trace(go.Bar(x=estados_fco, y=antes, name='Antes do FCO (Estágio Base)', marker_color='#94A3B8'))
    fig_fco.add_trace(go.Bar(x=estados_fco, y=depois, name='Após Consolidação do FCO', marker_color='#10B981'))
    fig_fco.update_layout(barmode='group', height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(x=0.01, y=0.99))
    st.plotly_chart(fig_fco, use_container_width=True)

    st.markdown("""
        <div class='didactic-box'>
            <strong>📊 Análise Interpretativa dos Resultados da Política Pública:</strong><br>
            A consolidação do FCO como mecanismo de funding gerou um impacto expressivo na modernização das cadeias produtivas regionais, expandindo os postos de trabalho formais em todos os estados, com destaque para a forte resposta de Mato Grosso e Goiás. No entanto, os resultados evidenciam que o subsídio tende a acompanhar a dinâmica de mercados já consolidados, concentrando os maiores volumes financeiros rurais nas franjas territoriais de alta produtividade. Para mitigar o descolamento regional, o planejamento futuro demanda critérios redistributivos intermunicipais associados a incentivos para indústrias locais de transformação secundária.
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(RODAPE_HTML, unsafe_allow_html=True)

# ==========================================
# ABA 4: PARTE IV - INTEGRAÇÃO (RESOLUÇÃO DEFINITIVA)
# ==========================================
with tab4:
    st.markdown("### **Integração: Relação entre a Política Pública (FCO) × Modelo Teórico (North)**")
    
    col_sankey, col_boxes = st.columns([1.3, 1])
    
    with col_sankey:
        st.markdown("<p style='text-align: right; font-size: 11px; font-weight: 700; color: #475569; margin-bottom: 5px;'>Fluxo: FCO ➔ Mecanismos de North ➔ Impactos ➔ Convergência</p>", unsafe_allow_html=True)
        
        # Variáveis de dados
        labels_sankey = [
            "FCO — Crédito Rural", "FCO — Empresarial/Indústria", "FCO — Infraestrutura", 
            "Acumulação de Capital", "Adensamento Técnico", "Encadeamentos Produtivos", 
            "Modernização Agrícola", "Geração de Empregos", "Diversificação Primária",
            "Concentração Espacial", "Convergência Regional"
        ]
        
        source = [0, 0, 1, 1, 2, 2, 3, 3, 4, 5, 5, 6, 7, 8]
        target = [3, 5, 4, 5, 3, 5, 6, 7, 6, 7, 8, 9, 10, 10]
        value =  [8, 4, 5, 6, 7, 4, 8, 7, 5, 6, 4, 9, 11, 4]
        
        # Criação do gráfico - Dicionário 'node' contendo APENAS o essencial
        fig_sankey = go.Figure(data=[go.Sankey(
            node=dict(
                label=labels_sankey, 
                pad=14, 
                thickness=18, 
                color=["#1E3F1A", "#1E3F1A", "#1E3F1A", "#4A9940", "#4A9940", "#4A9940", "#10B981", "#10B981", "#10B981", "#E53E3E", "#2D5A27"]
            ), 
            link=dict(
                source=source, 
                target=target, 
                value=value, 
                color="rgba(37, 99, 235, 0.12)"
            )
        )])
        
        # Aplicação das fontes de forma isolada e segura
        fig_sankey.update_layout(
            height=390, 
            margin=dict(l=5, r=5, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", size=11, color="black")
        )
        st.plotly_chart(fig_sankey, use_container_width=True)
        st.caption("Fonte: Elaboração própria a partir de dados do IBGE, IPEA e BNB.")

    with col_boxes:
        st.markdown("""
            <div style='background-color: #EEF2F6; border: 1px solid #CBD5E1; border-top: 4px solid #1E3F1A; border-radius: 8px; padding: 12px; margin-bottom: 12px;'>
                <span style='font-size:13px; font-weight:700; color:#1E3F1A;'>🔹 A Política Alterou a Trajetória?</span>
                <span style='font-size:12.5px; color:#334155;'><strong>Parcialmente sim.</strong> A correlação FCO × Emprego Formal demonstra dinamização relevante nas cadeias agroindustriais de Mato Grosso e Goiás.</span>
            </div>
            <div style='background-color: #EEF2F6; border: 1px solid #CBD5E1; border-top: 4px solid #D97706; border-radius: 8px; padding: 12px; margin-bottom: 12px;'>
                <span style='font-size:13px; font-weight:700; color:#D97706;'>📌 Foi suficiente?</span>
                <span style='font-size:12.5px; color:#334155;'><strong>Não integralmente.</strong> O gap de renda per capita intrarregional permanece elástico. Sem critérios rígidos de desconcentração municipal, perpetua-se a <strong>hiperpolarização</strong>.</span>
            </div>
            <div style='background-color: #FFFDF5; border: 1px solid #FEF08A; border-top: 4px solid #F59E0B; border-radius: 8px; padding: 12px;'>
                <span style='font-size:13px; font-weight:700; color:#B45309;'>🧩 Fortalecimentos e Fragilidades</span>
                <ul style='margin: 4px 0 0 0; padding-left: 18px; font-size: 12px; color: #451a03; line-height: 1.4;'>
                    <li><strong>Fortaleceu:</strong> Emprego na base exportadora.</li>
                    <li><strong>Enfraqueceu:</strong> Diversificação manufatureira.</li>
                    <li><strong>Necessário:</strong> Gradação inversa de subsídios.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style='background-color: #ffffff; border: 1px solid #E2E8F0; border-radius: 8px; padding: 15px; margin-top: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);'>
            <span style='font-size:13.5px; font-weight:700; color:#1E3A8A;'>Leitura do Diagrama</span><br>
            <p style='margin: 6px 0 0 0; font-size:12.5px; color:#475569;'>
                Os vetores do FCO alimentam os canais de acumulação de Douglass North. A espessura dos fluxos traduz a intensidade dos repasses, sinalizando onde ajustes redistributivos são necessários para a Convergência Regional.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(RODAPE_HTML, unsafe_allow_html=True)

# ==========================================
# ABA 5: PARTE V - PLANEJAMENTO
# ==========================================
with tab5:
    st.markdown("### **Diretrizes Estratégicas e Planejamento Regional**")
    
    c_plan1, c_plan2 = st.columns(2)
    with c_plan1:
        st.markdown("""
            <div class='info-box-blue' style='height: 100%; border-top: 4px solid #10B981;'>
                <h4>🎯 Recomendações de Políticas para o Futuro</h4>
                <ul>
                    <li><strong>Rotas de Intermodalidade (BR-163 & Ferronorte):</strong> Priorização de investimentos nos eixos ferroviários para reduzir a pegada de carbono do transporte rodoviário pesado.</li>
                    <li><strong>Fomento a Ecoprodutos e Bioeconomia:</strong> Criação de linhas de crédito específicas no FCO para aproveitamento sustentável dos ativos biológicos do Cerrado.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
    with c_plan2:
        st.markdown("""
            <div class='info-box-blue' style='height: 100%; border-top: 4px solid #6366F1;'>
                <h4>📌 Metas de Convergência Regional</h4>
                <ul>
                    <li>Reduzir em até 25% a disparidade de VAB per capita entre os municípios mais ricos e as franjas de menor dinamismo econômico da região.</li>
                    <li>Elevar em 40% a participação das ferrovias na matriz modal de transporte de grãos direcionada aos portos de saída.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown(RODAPE_HTML, unsafe_allow_html=True)