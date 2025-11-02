import streamlit as st

import sqlite3


# --- consts ---
OPTIONS_BUSCA = [
    'Nome 🔤',
    'Lugar 🗺️',
    'Endereço 📍️',
    'Cozinha 🧑‍🍳',
    'Serviços 🥤'
]

OPTIONS_TO_SQL = {
    'Nome 🔤': 'Name',
    'Lugar 🗺️': 'Location',
    'Endereço 📍️': 'Address',
    'Cozinha 🧑‍🍳': 'Cuisine',
    'Serviços 🥤': 'FacilitiesAndServices',
}

AWARDS = {
    '3 Stars': '⭐⭐⭐',
    'Selected Restaurants': 'Selected Restaurants',
    '1 Star': '⭐',
    '2 Stars': '⭐⭐',
    'Bib Gourmand': 'Bib Gourmand (value-for-money award)',
}


# --- header ---
st.set_page_config(page_title='Guia não oficial Michelin', layout="wide")
st.image('indian-food.jpg', use_container_width=True)
st.title('Guia não oficial Michelin')

# --- sql connection ---
# @st.cache_resource  # não pode compartilhar conexão entre threads
def connect(ref):
    conn = sqlite3.connect(ref)
    return conn.cursor(), conn

sql_conn, sql_cursor = connect('michelin.db')


# --- search bar ---
with st.form('form_busca'):
    with st.container(horizontal=True, vertical_alignment='bottom'):
        input_string = st.text_input(label='Pesquise restaurantes:', width=500, placeholder='Buscar...')
        st.form_submit_button(label='', help='Submeter', icon='🔍')

    with st.container(horizontal=True, vertical_alignment='bottom'):
        search_type = st.segmented_control(
            label='Busca por... ', options=OPTIONS_BUSCA, selection_mode='single', default=OPTIONS_BUSCA[0]
        )
        if search_type is None:
            search_type = OPTIONS_BUSCA[0]

        st.write('filtros...') # green star; award; pais (like)
        # st.multiselect('Filtros', OPTIONS_BUSCA, default=OPTIONS_BUSCA)


# --- page size bar ---
LIST_LIMITS = [5, 10, 20, 50, 100]
with st.container(horizontal=True, vertical_alignment='bottom'):
    list_limit = st.segmented_control(
        label='Número de resultados',
        options=LIST_LIMITS,
        selection_mode='single',
        default=LIST_LIMITS[0],
        key='list_limit_selector',
    )
    if list_limit is None:
        list_limit = LIST_LIMITS[0]

    list_page_offset = st.number_input(f'Página atual:', min_value=0, step=1, width=100)
    if list_page_offset is None:
        list_page_offset = 0

# --- actual query ---
# README: SQLite3 safe string interpolation (with `?`) automatically adds quotes.
# this is a problem when you need to interpolate a column (or table) name.
# In this case, we will be using python unsafe interpolation (the names are preselected,
# so it is safe).
selection_list = sql_cursor.execute(
    f"""SELECT * FROM restaurants WHERE
    {OPTIONS_TO_SQL[search_type]} LIKE ?
    COLLATE NOCASE
    LIMIT ? OFFSET ?;""",
    (
        f"%{input_string}%",
        list_limit,
        list_page_offset*list_limit
    )
).fetchall()

st.write(OPTIONS_TO_SQL[search_type])


# --- display results ---
def display_restaurant(restaurants_row: tuple):
    values = {
        'Name': restaurants_row[0],
        'Address': restaurants_row[1],
        'Location': restaurants_row[2],
        'Price': restaurants_row[3],
        'Cuisine': restaurants_row[4],
        'Longitude': restaurants_row[5],
        'Latitude': restaurants_row[6],
        'PhoneNumber': restaurants_row[7],
        'Url': restaurants_row[8],
        'WebsiteUrl': restaurants_row[9],
        'Award': restaurants_row[10],
        'GreenStar': restaurants_row[11],
        'FacilitiesAndServices': restaurants_row[12],
        'Description': restaurants_row[13],
    }
    
    with st.container(border=True):
        if values['GreenStar'] == 1:
            col_title, col_green1, col_green2 = st.columns([70, 15, 15])
            with col_green1:
                st.image(
                    'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fd3h1lg3ksw6i6b.cloudfront.net%2Fmedia%2Fimage%2F2022%2F10%2F11%2F31d3d763e68745dca54c19db6978db5f_Green-Star-hero-image.jpg&f=1&nofb=1&ipt=66daaf4f1091fad80a0a78cc8b22d1cf309baf2c8dfb3b89a9ce9bba8f147aeb',
                )
            with col_green2:
                st.text('Este restaurante recebeu a Estrela Verde Michelin por sua sustentabilidade na gastronomia.')

        else:
            col_title, = st.columns(1)

        with col_title:
            st.subheader(values['Name'])
            st.text(values['Location'])

        col_award, col_price, col_details = st.columns([30, 20, 50])
        with col_award:
            st.metric('Premiação:', AWARDS[values['Award']], border=True)
        with col_price:
            st.metric('Preço:', values['Price'], border=True)
        with col_details:
            st.markdown(f'''
**Cozinha 🧑‍🍳:** {values['Cuisine']}\n
**Serviços 🥤:** {values['FacilitiesAndServices']}\n
''')

        with st.expander('Descrição'):
            st.text(values['Description'])
        with st.expander('Contato '):
            st.markdown(f'''
**Website:** [{values['WebsiteUrl']}]({values['WebsiteUrl']})\n
**Telefone:** [{values['PhoneNumber']}]({values['PhoneNumber']})\n
''')
        st.link_button('Ver no Guia Michelin', values['Url'])

st.header('Restaurantes encontrados:')
if selection_list:
    for row in selection_list:
        display_restaurant(row)
else:
    st.header('Nenhum restaurante encontrado com as características desejadas :('
              '\nTente remover alguns filtros ou voltar para a página 0.')
