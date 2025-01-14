# Versao 01

# import streamlit as st
# import pandas as pd
# import plotly.express as px

# # Função para limpar e normalizar os dados
# def clean_data(df):
#     df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
#     return df.applymap(lambda x: ' '.join(x.strip().lower().split()) if isinstance(x, str) else x)

# # Configuração do Streamlit
# st.set_page_config(page_title="Ferramentas do Mercado", layout="wide")
# st.title("📊 Monitoramento de Vagas e Ferramentas do Mercado")

# # Upload do CSV
# uploaded_file = st.file_uploader("Carregue o arquivo CSV com as vagas de emprego", type=["csv"])

# if uploaded_file is not None:
#     # Carregar os dados
#     data = pd.read_csv(uploaded_file)

#     # Normalizar os nomes das colunas
#     data = clean_data(data)

#     # Verificar se as colunas essenciais existem
#     required_columns = {'posicao', 'titulo_vaga', 'requisitos'}
#     if required_columns.issubset(set(data.columns)):
#         # Criar abas para o app
#         tab1, tab2 = st.tabs(["📊 Análise", "🗂 Dados Completos"])

#         with tab1:
#             st.sidebar.header("Pesquise pelo Título da Vaga")

#             # Filtros laterais
#             posicao_options = ["Todas"] + sorted(data['posicao'].dropna().unique().tolist())
#             posicao_selecionada = st.sidebar.selectbox("Selecione a posição:", options=posicao_options)

#             # Filtro avançado para título da vaga
#             titulo_vaga_input = st.sidebar.text_area(
#                 "Digite os termos de busca para o título da vaga (separados por vírgula):",
#                 placeholder="Exemplo: analista de BI, analista de dados"
#             )

#             # Aplicar os filtros
#             filtered_data = data.copy()

#             # Filtro por posição
#             if posicao_selecionada != "Todas":
#                 filtered_data = filtered_data[filtered_data['posicao'] == posicao_selecionada]

#             # Filtro por múltiplos termos no título da vaga
#             if titulo_vaga_input:
#                 termos_busca = [termo.strip() for termo in titulo_vaga_input.split(',')]
#                 regex_pattern = '|'.join(termos_busca)
#                 filtered_data = filtered_data[
#                     filtered_data['titulo_vaga'].str.contains(regex_pattern, case=False, na=False)
#                 ]

#             # Mostrar estatísticas gerais
#             st.header("Estatísticas Gerais")
#             total_vagas = len(filtered_data)
#             st.metric(label="Total de Vagas Filtradas", value=total_vagas)
#             st.write("Distribuição de Ferramentas Requisitadas:")

#             # Contar as ferramentas
#             tool_counts = (
#                 filtered_data['requisitos']
#                 .str.split(', ')
#                 .explode()
#                 .value_counts()
#             )

#             # Preparar os dados para o gráfico
#             tool_counts_df = tool_counts.head(20).reset_index()
#             tool_counts_df.columns = ['Ferramenta', 'Quantidade']

#             # Criar o gráfico interativo com Plotly
#             fig = px.bar(
#                 tool_counts_df,
#                 x='Quantidade',
#                 y='Ferramenta',
#                 orientation='h',
#                 text='Quantidade',
#                 labels={'Quantidade': 'Quantidade de Ocorrências', 'Ferramenta': 'Ferramentas'},
#                 title="Top 20 Ferramentas Mais Requisitadas"
#             )
#             fig.update_traces(textposition='outside')
#             fig.update_layout(
#                 yaxis=dict(autorange="reversed"),
#                 margin=dict(l=150, r=50, t=50, b=50)
#             )
#             st.plotly_chart(fig, use_container_width=True)

#             # Botão para baixar os dados filtrados
#             st.header("Download de Dados Filtrados")
#             csv = filtered_data.to_csv(index=False).encode('utf-8')
#             st.download_button(
#                 label="Baixar Dados Filtrados",
#                 data=csv,
#                 file_name="dados_filtrados.csv",
#                 mime="text/csv"
#             )

#         with tab2:
#             st.header("🗂 Visualização dos Completos das Vagas")
#             st.write("Aqui estão os dados carregados do arquivo CSV:")
#             st.dataframe(data, use_container_width=True)  # Exibir o DataFrame completo com ajuste ao layout

#     else:
#         missing_columns = required_columns - set(data.columns)
#         st.error(f"O arquivo CSV não contém as colunas necessárias: {', '.join(missing_columns)}.")
# else:
#     st.write("Carregue um arquivo CSV para começar a análise.")

# Versao 02

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import re

# # Função para limpar e normalizar os dados
# def clean_data(df):
#     df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
#     return df.applymap(lambda x: ' '.join(x.strip().lower().split()) if isinstance(x, str) else x)

# # Função para substituir espaços por _ dentro de aspas simples
# def replace_spaces_inside_quotes(column):
#     if isinstance(column, str):
#         # Substituir espaços dentro de termos compostos por _
#         return re.sub(r"'(.*?)'", lambda m: f"'{m.group(1).replace(' ', '_')}'", column)
#     return column

# # Função para limpar e padronizar as colunas de requisitos e competências
# def clean_list_column(column):
#     if isinstance(column, str):
#         # Aplicar substituição de espaços por _
#         column = replace_spaces_inside_quotes(column)
#         # Remover colchetes e aspas
#         column = column.replace("'", "").replace('[', '').replace(']', '').strip()
#         # Criar lista de termos limpos
#         terms = [term.strip() for term in column.split()]
#         return ', '.join(terms)
#     return ''

# # Configuração do Streamlit
# st.set_page_config(page_title="Monitoramento de Ferramentas e Competências", layout="wide")
# st.title("📊 Monitoramento de Ferramentas e Competências do Mercado")

# # Upload dos dois arquivos CSV
# uploaded_file1 = st.file_uploader("Carregue a Parte 1 do arquivo CSV", type=["csv"])
# uploaded_file2 = st.file_uploader("Carregue a Parte 2 do arquivo CSV", type=["csv"])

# if uploaded_file1 is not None and uploaded_file2 is not None:
#     try:
#         # Carregar os dois arquivos
#         data1 = pd.read_csv(uploaded_file1)
#         data2 = pd.read_csv(uploaded_file2)

#         # Concatenar os DataFrames
#         combined_data = pd.concat([data1, data2], ignore_index=True)

#         # Normalizar os dados
#         combined_data = clean_data(combined_data)

#         # Verificar se as colunas essenciais existem
#         required_columns = {'posicao', 'titulo_vaga', 'requisitos', 'competencias', 'senioridade', 'modalidade'}
#         if required_columns.issubset(set(combined_data.columns)):
#             # Limpar e padronizar as colunas de requisitos e competências
#             combined_data['requisitos'] = combined_data['requisitos'].apply(clean_list_column)
#             combined_data['competencias'] = combined_data['competencias'].apply(clean_list_column)

#             # Criar abas para o app
#             tab1, tab2, tab3 = st.tabs(["📊 Gráfico de Requisitos", "📊 Gráfico de Competências", "🗂 Dados Completos"])

#             # Filtros na barra lateral
#             st.sidebar.header("Filtros")
#             posicao_selecionada = st.sidebar.selectbox(
#                 "Selecione a posição:", 
#                 options=["Todas"] + sorted(combined_data['posicao'].dropna().unique().tolist())
#             )
#             senioridade_selecionada = st.sidebar.selectbox(
#                 "Selecione a senioridade:", 
#                 options=["Todas"] + sorted(combined_data['senioridade'].dropna().unique().tolist())
#             )
#             modalidade_selecionada = st.sidebar.selectbox(
#                 "Selecione a modalidade:", 
#                 options=["Todas"] + sorted(combined_data['modalidade'].dropna().unique().tolist())
#             )
#             competencias_input = st.sidebar.text_area(
#                 "Digite as competências (separadas por vírgula):",
#                 placeholder="Exemplo: python, sql, machine_learning"
#             )

#             # Aplicar os filtros
#             filtered_data = combined_data.copy()

#             if posicao_selecionada != "Todas":
#                 filtered_data = filtered_data[filtered_data['posicao'] == posicao_selecionada]

#             if senioridade_selecionada != "Todas":
#                 filtered_data = filtered_data[filtered_data['senioridade'] == senioridade_selecionada]

#             if modalidade_selecionada != "Todas":
#                 filtered_data = filtered_data[filtered_data['modalidade'] == modalidade_selecionada]

#             if competencias_input:
#                 competencias_busca = [term.strip() for term in competencias_input.split(',')]
#                 regex_pattern = '|'.join(competencias_busca)
#                 filtered_data = filtered_data[
#                     filtered_data['competencias'].str.contains(regex_pattern, case=False, na=False)
#                 ]

#             # Estatísticas Gerais
#             with tab1:
#                 total_vagas = len(filtered_data)
#                 st.metric(label="Total de Vagas Filtradas", value=total_vagas)

#                 # Gráfico de Requisitos
#                 requisitos_counts = (
#                     filtered_data['requisitos']
#                     .str.split(', ')
#                     .explode()
#                     .value_counts()
#                 )
#                 requisitos_df = requisitos_counts.reset_index()
#                 requisitos_df.columns = ['Requisito', 'Quantidade']

#                 fig_requisitos = px.bar(
#                     requisitos_df.head(20),  # Mostra apenas os 20 primeiros para destaque
#                     x='Quantidade',
#                     y='Requisito',
#                     orientation='h',
#                     text='Quantidade',
#                     title="Top 20 Requisitos Mais Requisitados",
#                     labels={'Quantidade': 'Ocorrências', 'Requisito': 'Requisitos'}
#                 )

#                 # Ajustar o layout do gráfico
#                 fig_requisitos.update_traces(textposition='outside', marker=dict(line=dict(width=1)))
#                 fig_requisitos.update_layout(
#                     yaxis=dict(autorange="reversed"),
#                     margin=dict(l=200, r=50, t=100, b=50),
#                     height=800
#                 )
#                 st.plotly_chart(fig_requisitos, use_container_width=True)

#             # Gráfico de Competências
#             with tab2:
#                 competencias_counts = (
#                     filtered_data['competencias']
#                     .str.split(', ')
#                     .explode()
#                     .value_counts()
#                 )
#                 competencias_df = competencias_counts.reset_index()
#                 competencias_df.columns = ['Competência', 'Quantidade']

#                 fig_competencias = px.bar(
#                     competencias_df.head(20),  # Mostra apenas os 20 primeiros para destaque
#                     x='Quantidade',
#                     y='Competência',
#                     orientation='h',
#                     text='Quantidade',
#                     title="Top 20 Competências Mais Requisitadas",
#                     labels={'Quantidade': 'Ocorrências', 'Competência': 'Competências'}
#                 )

#                 # Ajustar o layout do gráfico
#                 fig_competencias.update_traces(textposition='outside', marker=dict(line=dict(width=1)))
#                 fig_competencias.update_layout(
#                     yaxis=dict(autorange="reversed"),
#                     margin=dict(l=200, r=50, t=100, b=50),
#                     height=800
#                 )
#                 st.plotly_chart(fig_competencias, use_container_width=True)

#             # Dados Completos
#             with tab3:
#                 st.header("🗂 Dados Completos")
#                 st.write("Aqui estão os dados carregados do arquivo CSV:")
#                 st.dataframe(data1, use_container_width=True)

#         else:
#             missing_columns = required_columns - set(data2.columns)
#             st.error(f"O arquivo CSV não contém as colunas necessárias: {', '.join(missing_columns)}.")

#     except Exception as e:
#         st.error(f"Erro ao carregar ou processar os arquivos: {e}")
# else:
#     st.write("Carregue ambos os arquivos CSV para começar.")



# Versao 03

import streamlit as st
import pandas as pd
import plotly.express as px
import re

# Função para limpar e normalizar os dados
def clean_data(df):
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    return df.applymap(lambda x: ' '.join(x.strip().lower().split()) if isinstance(x, str) else x)

# Função para substituir espaços por _ dentro de aspas simples
def replace_spaces_inside_quotes(column):
    if isinstance(column, str):
        # Substituir espaços dentro de termos compostos por _
        return re.sub(r"'(.*?)'", lambda m: f"'{m.group(1).replace(' ', '_')}'", column)
    return column

# Função para limpar e padronizar as colunas de requisitos e competências
def clean_list_column(column):
    if isinstance(column, str):
        # Aplicar substituição de espaços por _
        column = replace_spaces_inside_quotes(column)
        # Remover colchetes e aspas
        column = column.replace("'", "").replace('[', '').replace(']', '').strip()
        # Criar lista de termos limpos
        terms = [term.strip() for term in column.split()]
        return ', '.join(terms)
    return ''

# Configuração do Streamlit
st.set_page_config(page_title="Monitoramento de Ferramentas e Competências", layout="wide")
st.header("📊 Monitoramento de Ferramentas e Competências do Mercado", divider='rainbow')

# Upload dos dois arquivos CSV
uploaded_file1 = st.file_uploader("Carregue a Parte 1 do arquivo CSV", type=["csv"])
uploaded_file2 = st.file_uploader("Carregue a Parte 2 do arquivo CSV", type=["csv"])

if uploaded_file1 is not None and uploaded_file2 is not None:
    try:
        # Carregar os dois arquivos
        data1 = pd.read_csv(uploaded_file1)
        data2 = pd.read_csv(uploaded_file2)

        # Concatenar os DataFrames
        combined_data = pd.concat([data1, data2], ignore_index=True)

        # Normalizar os dados
        combined_data = clean_data(combined_data)

        # Verificar se as colunas essenciais existem
        required_columns = {'posicao', 'titulo_vaga', 'requisitos', 'competencias', 'senioridade', 'modalidade', 'estado', 'cidade'}
        if required_columns.issubset(set(combined_data.columns)):
            # Limpar e padronizar as colunas de requisitos e competências
            combined_data['requisitos'] = combined_data['requisitos'].apply(clean_list_column)
            combined_data['competencias'] = combined_data['competencias'].apply(clean_list_column)

            # Criar abas para o app
            tab1, tab2, tab3 = st.tabs(["📊 Gráfico de Requisitos", "📊 Gráfico de Competências", "🗂 Todos os Dados"])

            # Filtros na barra lateral
            st.sidebar.header("Filtros")
            posicao_selecionada = st.sidebar.selectbox(
                "Posição:", 
                options=["Todas"] + sorted(combined_data['posicao'].dropna().unique().tolist())
            )
            senioridade_selecionada = st.sidebar.selectbox(
                "Senioridade:", 
                options=["Todas"] + sorted(combined_data['senioridade'].dropna().unique().tolist())
            )
            estado_selecionado = st.sidebar.selectbox(
                "Estado:", 
                options=["Todos"] + sorted(combined_data['estado'].dropna().unique().tolist())
            )
            cidade_selecionada = st.sidebar.selectbox(
                "Cidade:", 
                options=["Todas"] + sorted(combined_data['cidade'].dropna().unique().tolist())
            )
            modalidade_selecionada = st.sidebar.selectbox(
                "Modalidade:", 
                options=["Todas"] + sorted(combined_data['modalidade'].dropna().unique().tolist())
            )
            competencias_input = st.sidebar.text_area(
                "Digite as competências (separadas por vírgula):",
                placeholder="Exemplo: python, sql, machine_learning"
            )

            # Alternar entre porcentagem e valor absoluto
            show_percentage = st.sidebar.checkbox("Mostrar porcentagem (%)")

            # Aplicar os filtros
            filtered_data = combined_data.copy()

            if posicao_selecionada != "Todas":
                filtered_data = filtered_data[filtered_data['posicao'] == posicao_selecionada]

            if senioridade_selecionada != "Todas":
                filtered_data = filtered_data[filtered_data['senioridade'] == senioridade_selecionada]

            if estado_selecionado != "Todos":
                filtered_data = filtered_data[filtered_data['estado'] == estado_selecionado]

            if cidade_selecionada != "Todas":
                filtered_data = filtered_data[filtered_data['cidade'] == cidade_selecionada]

            if modalidade_selecionada != "Todas":
                filtered_data = filtered_data[filtered_data['modalidade'] == modalidade_selecionada]

            if competencias_input:
                competencias_busca = [term.strip() for term in competencias_input.split(',')]
                regex_pattern = '|'.join(competencias_busca)
                filtered_data = filtered_data[
                    filtered_data['competencias'].str.contains(regex_pattern, case=False, na=False)
                ]

            # Estatísticas Gerais
            total_vagas = len(filtered_data)

            with tab1:
                # Gráfico de Requisitos
                requisitos_counts = (
                    filtered_data['requisitos']
                    .str.split(', ')
                    .explode()
                    .value_counts(normalize=show_percentage)
                )
                requisitos_counts = requisitos_counts * 100 if show_percentage else requisitos_counts
                requisitos_df = requisitos_counts.reset_index()
                requisitos_df.columns = ['Requisito', 'Quantidade']

                # Adicionar estatística acima do gráfico
                st.metric(label="Total de Vagas Filtradas", value=total_vagas)

                fig_requisitos = px.bar(
                    requisitos_df.head(20),  # Mostra apenas os 20 primeiros para destaque
                    x='Quantidade',
                    y='Requisito',
                    orientation='h',
                    text='Quantidade',
                    title="Top 20 Requisitos Mais Requisitados",
                    color='Quantidade',
                    color_continuous_scale=[[0, '#0D133B'], [1, '#FF6F00']],  # Degradê Azul Escuro -> Laranja
                )

                # Ajustar o layout do gráfico
                fig_requisitos.update_traces(textposition='outside', marker=dict(line=dict(width=1)))
                fig_requisitos.update_layout(
                    yaxis=dict(autorange="reversed"),
                    margin=dict(l=200, r=50, t=100, b=50),
                    height=800,
                    coloraxis_showscale=False,  # Remove a escala de cor
                )
                st.plotly_chart(fig_requisitos, use_container_width=True)

            with tab2:
                # Gráfico de Competências
                competencias_counts = (
                    filtered_data['competencias']
                    .str.split(', ')
                    .explode()
                    .value_counts(normalize=show_percentage)
                )
                competencias_counts = competencias_counts * 100 if show_percentage else competencias_counts
                competencias_df = competencias_counts.reset_index()
                competencias_df.columns = ['Competência', 'Quantidade']

                # Adicionar estatística acima do gráfico
                st.metric(label="Total de Vagas Filtradas", value=total_vagas)

                fig_competencias = px.bar(
                    competencias_df.head(20),  # Mostra apenas os 20 primeiros para destaque
                    x='Quantidade',
                    y='Competência',
                    orientation='h',
                    text='Quantidade',
                    title="Top 20 Competências Mais Requisitadas",
                    color='Quantidade',
                    color_continuous_scale=[[0, '#0D133B'], [1, '#FF6F00']],  # Degradê Azul Escuro -> Laranja
                )

                # Ajustar o layout do gráfico
                fig_competencias.update_traces(textposition='outside', marker=dict(line=dict(width=1)))
                fig_competencias.update_layout(
                    yaxis=dict(autorange="reversed"),
                    margin=dict(l=200, r=50, t=100, b=50),
                    height=800,
                    coloraxis_showscale=False,  # Remove a escala de cor
                )
                st.plotly_chart(fig_competencias, use_container_width=True)

            with tab3:
                # Exibir todos os dados filtrados
                st.header("🗂 Todos os Dados")
                st.dataframe(filtered_data, use_container_width=True)

        else:
            missing_columns = required_columns - set(combined_data.columns)
            st.error(f"O arquivo CSV não contém as colunas necessárias: {', '.join(missing_columns)}.")

    except Exception as e:
        st.error(f"Erro ao carregar ou processar os arquivos: {e}")
else:
    st.write("Carregue ambos os arquivos CSV para começar.")

