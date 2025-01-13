import streamlit as st
import pandas as pd
import plotly.express as px

# Função para limpar e normalizar os dados
def clean_data(df):
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    return df.applymap(lambda x: ' '.join(x.strip().lower().split()) if isinstance(x, str) else x)

# Configuração do Streamlit
st.set_page_config(page_title="Ferramentas do Mercado", layout="wide")
st.title("📊 Monitoramento de Ferramentas do Mercado")

# Upload do CSV
uploaded_file = st.file_uploader("Carregue o arquivo CSV com as vagas de emprego", type=["csv"])

if uploaded_file is not None:
    # Carregar os dados
    data = pd.read_csv(uploaded_file)

    # Normalizar os nomes das colunas
    data = clean_data(data)

    # Verificar se as colunas essenciais existem
    required_columns = {'posicao', 'titulo_vaga', 'requisitos'}
    if required_columns.issubset(set(data.columns)):
        # Criar abas para o app
        tab1, tab2 = st.tabs(["📊 Análise", "🗂 Dados Completos"])

        with tab1:
            st.sidebar.header("Configurações de Filtros")

            # Filtros laterais
            posicao_options = ["Todas"] + sorted(data['posicao'].dropna().unique().tolist())
            posicao_selecionada = st.sidebar.selectbox("Selecione a posição:", options=posicao_options)

            # Filtro avançado para título da vaga
            titulo_vaga_input = st.sidebar.text_area(
                "Digite os termos de busca para o título da vaga (separados por vírgula):",
                placeholder="Exemplo: analista de BI, analista de dados"
            )

            # Aplicar os filtros
            filtered_data = data.copy()

            # Filtro por posição
            if posicao_selecionada != "Todas":
                filtered_data = filtered_data[filtered_data['posicao'] == posicao_selecionada]

            # Filtro por múltiplos termos no título da vaga
            if titulo_vaga_input:
                termos_busca = [termo.strip() for termo in titulo_vaga_input.split(',')]
                regex_pattern = '|'.join(termos_busca)
                filtered_data = filtered_data[
                    filtered_data['titulo_vaga'].str.contains(regex_pattern, case=False, na=False)
                ]

            # Mostrar estatísticas gerais
            st.header("Estatísticas Gerais")
            total_vagas = len(filtered_data)
            st.metric(label="Total de Vagas Filtradas", value=total_vagas)
            st.write("Distribuição de Ferramentas Requisitadas:")

            # Contar as ferramentas
            tool_counts = (
                filtered_data['requisitos']
                .str.split(', ')
                .explode()
                .value_counts()
            )

            # Preparar os dados para o gráfico
            tool_counts_df = tool_counts.head(20).reset_index()
            tool_counts_df.columns = ['Ferramenta', 'Quantidade']

            # Criar o gráfico interativo com Plotly
            fig = px.bar(
                tool_counts_df,
                x='Quantidade',
                y='Ferramenta',
                orientation='h',
                text='Quantidade',
                labels={'Quantidade': 'Quantidade de Ocorrências', 'Ferramenta': 'Ferramentas'},
                title="Top 20 Ferramentas Mais Requisitadas"
            )
            fig.update_traces(textposition='outside')
            fig.update_layout(
                yaxis=dict(autorange="reversed"),
                margin=dict(l=150, r=50, t=50, b=50)
            )
            st.plotly_chart(fig, use_container_width=True)

            # Botão para baixar os dados filtrados
            st.header("Download de Dados Filtrados")
            csv = filtered_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Baixar Dados Filtrados",
                data=csv,
                file_name="dados_filtrados.csv",
                mime="text/csv"
            )

        with tab2:
            st.header("🗂 Dados Completos")
            st.write("Aqui estão os dados carregados do arquivo CSV:")
            st.dataframe(data, use_container_width=True)  # Exibir o DataFrame completo com ajuste ao layout

    else:
        missing_columns = required_columns - set(data.columns)
        st.error(f"O arquivo CSV não contém as colunas necessárias: {', '.join(missing_columns)}.")
else:
    st.write("Carregue um arquivo CSV para começar a análise.")
