

# import streamlit as st
# import pandas as pd
# import plotly.express as px

# # Função para limpar e normalizar os dados
# def clean_data(df):
#     return df.applymap(lambda x: ' '.join(x.strip().lower().split()) if isinstance(x, str) else x)

# # Configuração do Streamlit
# st.set_page_config(page_title="Ferramentas do Mercado", layout="wide")
# st.title("📊 Monitoramento de Ferramentas do Mercado")

# # Upload do CSV
# uploaded_file = st.file_uploader("Carregue o arquivo CSV com as vagas de emprego", type=["csv"])

# if uploaded_file is not None:
#     # Carregar os dados
#     data = pd.read_csv(uploaded_file)
#     st.sidebar.header("Configurações de Filtros")
    
#     # Limpar os dados
#     data = clean_data(data)

#     # Filtros laterais
#     posicao_options = ["Todas"] + sorted(data['posicao'].dropna().unique().tolist())
#     titulo_vaga_options = ["Todas"] + sorted(data['titulo_vaga'].dropna().unique().tolist())

#     posicao_selecionada = st.sidebar.selectbox("Selecione a posição:", options=posicao_options)
#     titulo_vaga = st.sidebar.text_input("Digite o título da vaga (ou deixe em branco):", "")

#     # Aplicar os filtros
#     filtered_data = data.copy()
#     if posicao_selecionada != "Todas":
#         filtered_data = filtered_data[filtered_data['posicao'] == posicao_selecionada]
#     if titulo_vaga:
#         filtered_data = filtered_data[filtered_data['titulo_vaga'].str.contains(titulo_vaga, case=False, na=False)]

#     # Mostrar estatísticas gerais
#     st.header("Estatísticas Gerais")
#     total_vagas = len(filtered_data)
#     st.metric(label="Total de Vagas Filtradas", value=total_vagas)
#     st.write("Distribuição de Ferramentas Requisitadas:")

#     # Contar as ferramentas
#     tool_counts = (
#         filtered_data['requisitos']
#         .str.split(', ')
#         .explode()
#         .value_counts()
#     )

    
#     # Preparar os dados para o gráfico
#     tool_counts_df = tool_counts.head(20).reset_index()  # Resetar o índice para torná-lo uma coluna
#     tool_counts_df.columns = ['Ferramenta', 'Quantidade']  # Renomear as colunas

#     # Criar o gráfico interativo com Plotly
#     fig = px.bar(
#     tool_counts_df,
#     x='Quantidade',
#     y='Ferramenta',
#     orientation='h',
#     labels={'Quantidade': 'Quantidade de Ocorrências', 'Ferramenta': 'Ferramentas'},
#     title="Top 20 Ferramentas Mais Requisitadas"
#     )

#     #    Adicionar os valores à frente das barras
#     fig.update_traces(
#     text=tool_counts_df['Quantidade'],
#     textposition='outside'  # Exibir os valores fora das barras
#     )

#     # Ajustar layout
#     fig.update_layout(
#     yaxis=dict(autorange="reversed"),  # Inverter o eixo Y para a barra maior ficar no topo
#     margin=dict(l=150, r=50, t=50, b=50)  # Ajustar margens para melhor visualização
#     )

#     # Exibir o gráfico no Streamlit
#     st.plotly_chart(fig, use_container_width=True)
    

#     # Botão para baixar os dados filtrados
#     st.header("Download de Dados Filtrados")
#     csv = filtered_data.to_csv(index=False).encode('utf-8')
#     st.download_button(
#         label="Baixar Dados Filtrados",
#         data=csv,
#         file_name="dados_filtrados.csv",
#         mime="text/csv"
#     )
# else:
#     st.write("Carregue um arquivo CSV para começar a análise.")




# import streamlit as st
# import pandas as pd
# import plotly.express as px

# # Função para limpar e normalizar os dados
# def clean_data(df):
#     return df.applymap(lambda x: ' '.join(x.strip().lower().split()) if isinstance(x, str) else x)

# # Configuração do Streamlit
# st.set_page_config(page_title="Ferramentas do Mercado", layout="wide")
# st.title("📊 Monitoramento de Ferramentas do Mercado")

# # Upload do CSV
# uploaded_file = st.file_uploader("Carregue o arquivo CSV com as vagas de emprego", type=["csv"])

# if uploaded_file is not None:
#     # Carregar os dados
#     data = pd.read_csv(uploaded_file)
#     st.sidebar.header("Configurações de Filtros")
    
#     # Limpar os dados
#     data = clean_data(data)

#     # Filtros laterais
#     posicao_options = ["Todas"] + sorted(data['posicao'].dropna().unique().tolist())
#     posicao_selecionada = st.sidebar.selectbox("Selecione a posição:", options=posicao_options)

#     # Filtro avançado para título da vaga
#     titulo_vaga_input = st.sidebar.text_area(
#         "Digite os termos de busca para o título da vaga (separados por vírgula):",
#         placeholder="Exemplo: analista de BI, analista de dados"
#     )

#     # Aplicar os filtros
#     filtered_data = data.copy()

#     # Filtro por posição
#     if posicao_selecionada != "Todas":
#         filtered_data = filtered_data[filtered_data['posicao'] == posicao_selecionada]

#     # Filtro por múltiplos termos no título da vaga
#     if titulo_vaga_input:
#         termos_busca = [termo.strip() for termo in titulo_vaga_input.split(',')]
#         regex_pattern = '|'.join(termos_busca)  # Cria um padrão regex para "OU"
#         filtered_data = filtered_data[
#             filtered_data['titulo_vaga'].str.contains(regex_pattern, case=False, na=False)
#         ]

#     # Mostrar estatísticas gerais
#     st.header("Estatísticas Gerais")
#     total_vagas = len(filtered_data)
#     st.metric(label="Total de Vagas Filtradas", value=total_vagas)
#     st.write("Distribuição de Ferramentas Requisitadas:")

#     # Contar as ferramentas
#     tool_counts = (
#         filtered_data['requisitos']
#         .str.split(', ')
#         .explode()
#         .value_counts()
#     )

#     # Mostrar tabela com as ferramentas mais requisitadas
#     # st.dataframe(tool_counts.reset_index().rename(columns={'index': 'Ferramenta', 'requisitos': 'Quantidade'}))

#     # Preparar os dados para o gráfico
#     tool_counts_df = tool_counts.head(20).reset_index()  # Resetar o índice para torná-lo uma coluna
#     tool_counts_df.columns = ['Ferramenta', 'Quantidade']  # Renomear as colunas

#     # Criar o gráfico interativo com Plotly
#     fig = px.bar(
#     tool_counts_df,
#     x='Quantidade',
#     y='Ferramenta',
#     orientation='h',
#     text='Quantidade',  # Adicionar os valores diretamente nas barras
#     labels={'Quantidade': 'Quantidade de Ocorrências', 'Ferramenta': 'Ferramentas'},
#     title="Top 20 Ferramentas Mais Requisitadas"
#     )

#     # Ajustar layout para mostrar os valores à frente das barras
#     fig.update_traces(textposition='outside')

#     # Ajustar layout geral
#     fig.update_layout(
#     yaxis=dict(autorange="reversed"),  # Inverter o eixo Y para a barra maior ficar no topo
#     margin=dict(l=150, r=50, t=50, b=50)  # Ajustar margens para melhor visualização
#     )

#     # Exibir o gráfico no Streamlit
    
#     st.plotly_chart(fig, use_container_width=True)


#     # Botão para baixar os dados filtrados
#     st.header("Download de Dados Filtrados")
#     csv = filtered_data.to_csv(index=False).encode('utf-8')
#     st.download_button(
#         label="Baixar Dados Filtrados",
#         data=csv,
#         file_name="dados_filtrados.csv",
#         mime="text/csv"
#     )
# else:
#     st.write("Carregue um arquivo CSV para começar a análise.")





import streamlit as st
import pandas as pd
import plotly.express as px

# Função para limpar e normalizar os dados
def clean_data(df):
    return df.applymap(lambda x: ' '.join(x.strip().lower().split()) if isinstance(x, str) else x)

# Configuração do Streamlit
st.set_page_config(page_title="Ferramentas do Mercado", layout="wide")
st.title("📊 Monitoramento de Ferramentas do Mercado")

# Upload do CSV
uploaded_file = st.file_uploader("Carregue o arquivo CSV com as vagas de emprego", type=["csv"])

if uploaded_file is not None:
    # Carregar os dados
    data = pd.read_csv(uploaded_file)

    # Exibir as colunas disponíveis para debug
    st.write("Colunas disponíveis no arquivo:")
    st.write(data.columns.tolist())

    # Limpar os dados e normalizar os nomes das colunas
    data.columns = [col.strip().lower().replace(" ", "_") for col in data.columns]
    data = clean_data(data)

    # Verificar se as colunas esperadas existem
    if 'posicao' in data.columns and 'titulo_vaga' in data.columns and 'requisitos' in data.columns:
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
            regex_pattern = '|'.join(termos_busca)  # Cria um padrão regex para "OU"
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
        tool_counts_df = tool_counts.head(20).reset_index()  # Resetar o índice para torná-lo uma coluna
        tool_counts_df.columns = ['Ferramenta', 'Quantidade']  # Renomear as colunas

        # Criar o gráfico interativo com Plotly
        fig = px.bar(
            tool_counts_df,
            x='Quantidade',
            y='Ferramenta',
            orientation='h',
            text='Quantidade',  # Adicionar os valores diretamente nas barras
            labels={'Quantidade': 'Quantidade de Ocorrências', 'Ferramenta': 'Ferramentas'},
            title="Top 20 Ferramentas Mais Requisitadas"
        )

        # Ajustar layout para mostrar os valores à frente das barras
        fig.update_traces(textposition='outside')

        # Ajustar layout geral
        fig.update_layout(
            yaxis=dict(autorange="reversed"),  # Inverter o eixo Y para a barra maior ficar no topo
            margin=dict(l=150, r=50, t=50, b=50)  # Ajustar margens para melhor visualização
        )

        # Exibir o gráfico no Streamlit
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
    else:
        # Exibir aviso de erro se as colunas esperadas não existirem
        st.error("O arquivo CSV carregado não contém as colunas esperadas: 'posicao', 'titulo_vaga' ou 'requisitos'. Verifique o arquivo.")
else:
    st.write("Carregue um arquivo CSV para começar a análise.")

