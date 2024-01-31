#################################################################################################################################
# Aquest document conté part del codi de la pràctica 1, on es defineixen les funcions quue ens serviran per alguns dels passos.
# Autor: Marc Nosàs Pomares
# Data: 23/11/2023
#################################################################################################################################

import numpy as np
import pandas as pd
import re

def open_csvs(path, names, encoding='latin-1'):
    """
    Funció que llegeix diversos fitxers CSV a partir d'un path i una llista de noms de fitxers, 
    i retorna un dataframe que és la combinació de tots els fitxers llegits.

    :param path: El path en el que es troben els fitxers CSV
    :param names: Una llista de noms de fitxers CSV
    :param encoding: L'encodatge dels fitxers CSV (per defecte latin-1)
    :returns: Un dataframe que és la combinació de tots els fitxers CSV llegits.
    """

    # Creem una llista de dataframes a partir dels fitxers CSV
    dfs =  [pd.read_csv(path + name, 
                        sep=',', 
                        encoding=encoding,
                        on_bad_lines='skip',
                        low_memory=False) for name in names]

    # Ara fem un merge de tots els dataframes
    return pd.concat(dfs, ignore_index=True)

def remove_private_columns(df): 
    """
    Aquesta funció elimina les columnes privades del DataFrame df que es passa com a paràmetre. 
    
    Les columnes a eliminar són: 'Nombre', 'Email', 'Teléfono', 'Afiliado', 'Tarifa', 'Comentarios', 'Nombre Organización', 'Id. Tienda Online','Notas internas' i 'Metodo de pago'.
    
    Si alguna de les columnes a eliminar no es troba al DataFrame, la funció llença una excepció KeyError.
    
    :param df: DataFrame d'entrada del que es volen eliminar les columnes privades
    :return: DataFrame amb les columnes privades eliminades
    """
    # Llista de columnes a eliminar
    remove = ['Nombre', 'Email', 'Teléfono', 'Afiliado', 'Tarifa', 'Comentarios', 
              'Nombre Organización', 'Id. Tienda Online','Notas internas', 
              'Metodo de pago']

    # Comprova que totes les columnes a eliminar estan al DataFrame
    for col in remove:
        if col not in df.columns:
            raise KeyError(f'La columna "{col}" no es troba al DataFrame')

    # Elimina les columnes de la llista del DataFrame usant pandas
    df = df.drop(remove, axis=1)

    return df

def generate_motor_dict(df):
    """
    Aquesta funció genera un diccionari on cada clau és un valor únic de la columna 'Motor' del DataFrame df i el valor corresponent és una cadena de text 'hotel_{index}', on {index} és la posició de la clau dins la llista de valors únics.
    
    A continuació, la funció reemplaça els valors de la columna 'Motor' del DataFrame df pels valors corresponents del diccionari generat.
    
    :param df: DataFrame d'entrada que conté la columna 'Motor' a modificar
    :return: DataFrame amb els valors de la columna 'Motor' reemplaçats pels valors del diccionari generat
    """
    # Creem una llista amb els valors únics de la columna 'Motor'
    list_motor = list(df.Motor.unique())
    
    # Creem un diccionari buit
    motor_dic = {}
    
    # Iterem sobre la llista de valors únics i omplim el diccionari
    for index, motor_title in enumerate(list_motor):
        motor_dic[motor_title] = "hotel_{index}".format(index=index)
    
    # Ara ho canviem a la columna Motor
    df['Motor'] = df['Motor'].map(motor_dic)
    
    return df

def generate_bookings_dict(df):
    """
    Aquesta funció genera un diccionari de reserves a partir d'un dataframe.

    Primer, per cada T Booking ID, assigna un id format per 7 dígits que comença en 0000001. 
    A continuació, per cada booking id associat a aquest T Booking ID, assigna un id format per 7 dígits seguit d'un punt i un número de 2 dígits que comença en 01.

    Finalment, substitueix les columnes 'T Booking ID' i 'Booking ID' del dataframe original pel corresponent valor dels diccionaris generats.

    :param df: DataFrame original que conté les columnes 'T Booking ID' i 'Booking ID'
    :return: DataFrame amb les columnes 'T Booking ID' i 'Booking ID' substituïdes pels nous ids generats.
    """
    # Creem un diccionari amb els diferents Booking IDs que té assignats cada motor ID
    grouped = df.groupby('T Booking ID')['Booking ID'].unique()
    dict_T_booking_id = grouped.to_dict()

    # Ara recorrem el diccionari, a cada T Booking ID li assignem un id tipus 0000000 amb un numero de 7 digits que inciciarà en 0000001
    T_booking_id_dic = {}
    booking_id_dic = {}
    counter = 1
    for key, value in dict_T_booking_id.items():
        T_booking_id_dic[key] = f'{counter:07}'
        for index, booking_id in enumerate(list(value)):
            booking_id_dic[booking_id] = f'{counter:07}.{index+1:02}'
            
        counter += 1
    # Ara ja podem substituir els valors a les columnes
    df['T Booking ID'] = df['T Booking ID'].map(T_booking_id_dic)
    df['Booking ID'] = df['Booking ID'].map(booking_id_dic)
    return df

def covid_regex(string):
    """
    Aquesta funció rep un string i retorna una categoria en funció del contingut del string.
    Si el string conté alguna de les paraules 'covid', 'confinad' o 'confin', retorna 'COVID-19'.
    Si el string conté alguna de les paraules 'enfermedad', 'hospital', 'illness', 'disease' o 'sick', retorna 'ENFERMEDAD'.
    Si el string conté alguna de les paraules 'fechas' o 'dates', retorna 'CAMBIO FECHAS'.
    Si el string conté alguna de les paraules 'anula' o 'cancelacion', retorna 'ANULACIÓN'.
    En qualsevol altre cas, retorna 'OTROS'.
    
    :param string: string a categoritzar
    :return: categoria del string
    """
    if type(string) != str:
        return np.nan
    elif re.match(r'.*(covid|confinad|confin).*', string, re.IGNORECASE):
        return 'COVID-19'
    elif re.match(r'.*(enfermedad|hospital|illness|disease|sick).*', string, re.IGNORECASE):
        return 'ENFERMEDAD'
    elif re.match(r'.*(fechas|dates).*', string, re.IGNORECASE):
        return 'CAMBIO FECHAS'
    elif re.match(r'.*(anula|cancelacion).*', string, re.IGNORECASE):
        return 'ANULACIÓN'
    else:
        return 'OTROS'

def change_motivo_cancelacion(df):
    """
    Aquesta funció aplica la funció covid_regex a cada valor de la columna 'Motivo cancelación' del DataFrame df.
    
    :param df: DataFrame d'entrada que conté la columna 'Motivo cancelación' a modificar
    :return: DataFrame amb els valors de la columna 'Motivo cancelación' modificats segons la funció covid_regex
    """
    df['Motivo cancelación'] = df['Motivo cancelación'].apply(covid_regex)
    return df

def columns_to_boolean(df):
    """
    Aquesta funció converteix les columnes "Promociones", "Codigos Promocionales", "Reserva Combinada" i "Fidelizada" del DataFrame df a valors booleans.
    
    Les columnes "Promociones" i "Codigos Promocionales" es convertiran en True si tenen algun valor i False si són NaN.
    Les columnes "Reserva Combinada" i "Fidelizada" es convertiran directament a booleans (True o False) ja que estan en format string.
    
    :param df: DataFrame d'entrada que conté les columnes a convertir
    :return: DataFrame amb les columnes convertides a booleans
    """
    # A les columnes de "Promociones" i "Codigos Promocionales" només farem valors True si hi ha alguna promoció i False si el valor es NaN
    df['Promociones'] = df['Promociones'].notnull()
    df['Codigos Promocionales'] = df['Codigos Promocionales'].notnull()
    
    # Les columnes "Reserva Combinada" i "Fidelizada" contenen valors True i False, però en format string. Les convertim a booleans
    df['Reserva Combinada'] = df['Reserva Combinada'].astype('bool')
    df['Fidelizada'] = df['Fidelizada'].astype('bool')
    
    return df

def make_private(df):
    df = remove_private_columns(df)
    df = generate_motor_dict(df)
    df = generate_bookings_dict(df)
    df = change_motivo_cancelacion(df)
    df = columns_to_boolean(df)
    # També el guardarem en un fitxer CSV
    df.to_csv('Data/hotel_bookings.csv', index=False)
    
    return df


