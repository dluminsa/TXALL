import pandas as pd 
import streamlit as st 
import os
import numpy as np
import random
import time
from pathlib import Path
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

st.set_page_config(
    page_title = 'MOCK TX CURR',
    page_icon =":bar_chart"
    )

st.subheader('MOCK UP TX CURR AND VL COV')
st.success('WELCOME, this app was developed by Dr. Luminsa Desire, for any concern, reach out to him at desireluminsa@gmail.com')
today = datetime.now()
today = today.strftime("%Y-%m-%d %H:%M")
st.write(f"CURRENT DATE:    {today}")

st.markdown('**FIRST RENAME THESE COLUMNS BEFORE YOU PROCEED:**')
col1, col2, col3 = st.columns([1,1,1])
col1.markdown('Rename the **HIV CLINIC NO.** column to **A**')
col1.markdown('Rename the **ART START DATE** column to **AS**')
col2.markdown('Rename the **RETURN VISIT DATE** column to **RD**')
col2.markdown('Rename the **TRANSFER OUT DATE** column to **TO**')
col3.markdown('Rename the **TRANSFER IN DATE** column to **TI**')
col3.markdown('Rename the **HIV VIRAL LOAD DATE** column to **VD**')

file = st.file_uploader("Upload your EMR extract here", type=['csv', 'xlsx', 'txt'])


ext = None
if file is not None:
    # Get the file name
    fileN = file.name
    ext = os.path.basename(fileN).split('.')[1]
df = None
if file is not None:
    if ext !='xlsx':
        st.write('Unsupported file format, first save the excel as xlsx and try again')
        st.stop()
    else:
        df = pd.read_excel(file)
        st.write('Excel accepted')
    if df is not None:
        columns = ['A', 'AS', 'VD', 'RD','TO', 'TI']
        cols = df.columns.to_list()
        if not all(column in cols for column in columns):
            missing_columns = [column for column in columns if column not in cols]
            for column in missing_columns:
                st.markdown(f' **ERROR !!! {column} is not in the file uploaded**')
                st.markdown('**First rename all the columns as guided above**')
                st.stop()
        else:
              # Convert 'A' column to string and create 'ART' column with numeric part
            df['A'] = df['A'].astype(str)
            df['ART'] = df['A'].str.replace('[^0-9]', '', regex=True)
            df['ART'] = pd.to_numeric(df['ART'], errors= 'coerce')
            df = df[df['ART']>0]
            #df.dropna(subset='ART', inplace=True)
            df = df.copy()
            df[['AS', 'RD', 'VD','TO','TI']] = df[['AS', 'RD', 'VD','TO','TI']].astype(str)
            df['AS'] = df['AS'].str.replace('/', '*', regex=True)
            df['RD'] = df['RD'].str.replace('/', '*', regex=True)
            df['VD'] = df['VD'].str.replace('/', '*',regex=True)
            df['TO'] = df['TO'].str.replace('/', '*',regex=True)
            df['TI'] = df['TI'].str.replace('/', '*',regex=True)

            df['AS'] = df['AS'].str.replace('-', '*',regex=True)
            df['RD'] = df['RD'].str.replace('-', '*',regex=True)
            df['VD'] = df['VD'].str.replace('-', '*',regex=True)
            df['TO'] = df['TO'].str.replace('-', '*',regex=True)
            df['TI'] = df['TI'].str.replace('-', '*',regex=True)

            df['AS'] = df['AS'].str.replace('00:00:00', '', regex=True)
            df['RD'] = df['RD'].str.replace('00:00:00', '', regex=True)
            df['VD'] = df['VD'].str.replace('00:00:00', '', regex=True)
            df['TO'] = df['TO'].str.replace('00:00:00', '', regex=True)
            df['TI'] = df['TI'].str.replace('00:00:00', '',regex=True)
            try:
                df[['Ayear', 'Amonth', 'Aday']] = df['AS'].str.split('*', expand = True)
            except:
                pass
            try:
                df['AS'] = pd.to_numeric(df['AS'], errors='coerce')
                df['AS'] = pd.to_datetime(df['AS'], origin='1899-12-30', unit='D')
                df['AS'] =  df['AS'].astype(str)
                df['AS'] = df['AS'].str.replace('-', '*',regex=True)
                df[['Ayear', 'Amonth', 'Aday']] = df['AS'].str.split('*', expand = True)
            except:
                pass
            try:
                df[['Ryear', 'Rmonth', 'Rday']] = df['RD'].str.split('*', expand = True)
            except:
                pass
            try:
                df['RD'] = pd.to_numeric(df['RD'], errors='coerce')
                df['RD'] = pd.to_datetime(df['RD'], origin='1899-12-30', unit='D')
                df['RD'] =  df['RD'].astype(str)
                df['RD'] = df['RD'].str.replace('-', '*',regex=True)
                df[['Ryear', 'Rmonth', 'Rday']] = df['RD'].str.split('*', expand = True)
            except:
                pass
            try:
                df[['Vyear', 'Vmonth', 'Vday']] = df['VD'].str.split('*', expand = True)
            except:
                pass
            try:
                df['VD'] = pd.to_numeric(df['VD'], errors='coerce')
                df['VD'] = pd.to_datetime(df['VD'], origin='1899-12-30', unit='D')
                df['VD'] =  df['VD'].astype(str)
                df['VD'] = df['VD'].str.replace('-', '*',regex=True)
                df[['Vyear', 'Vmonth', 'Vday']] = df['VD'].str.split('*', expand = True)
            except:
                pass

            try:
                df[['Tyear', 'Tmonth', 'Tday']] = df['TO'].str.split('*', expand = True)
            except:
                pass

            try:
                df['TO'] = pd.to_numeric(df['TO'], errors='coerce')
                df['TO'] = pd.to_datetime(df['TO'], origin='1899-12-30', unit='D')
                df['TO'] =  df['TO'].astype(str)
                df['TO'] = df['TO'].str.replace('-', '*',regex=True)
                df[['Tyear', 'Tmonth', 'Tday']] = df['TO'].str.split('*', expand = True)
            except:
                pass

            try:
               df[['Tiyear', 'Timonth', 'Tiday']] = df['TI'].str.split('*', expand = True)
            except:
                pass
            try:
                df['TI'] = pd.to_numeric(df['TI'], errors='coerce')
                df['TI'] = pd.to_datetime(df['TI'], origin='1899-12-30', unit='D')
                df['TI'] =  df['TI'].astype(str)
                df['TI'] = df['TI'].str.replace('-', '*',regex=True)
                df[['Tiyear', 'Timonth', 'Tiday']] = df['TI'].str.split('*', expand = True)
            except:
                pass

               #BRINGING BACK THE / IN DATES
            df['AS'] = df['AS'].str.replace('*', '/',regex=True)
            df['RD'] = df['RD'].str.replace('*', '/',regex=True)
            df['VD'] = df['VD'].str.replace('*', '/',regex=True)
            #df['LD'] = df['LD'].str.replace('*', '/',regex=True)
            df['TO'] = df['TO'].str.replace('*', '/',regex=True)
            df['TI'] = df['TI'].str.replace('*', '/',regex=True)
            #             #SORTING THE VIRAL LOAD YEARS
            df[['Vyear', 'Vmonth', 'Vday']] =df[['Vyear', 'Vmonth', 'Vday']].apply(pd.to_numeric, errors = 'coerce') 
            df['Vyear'] = df['Vyear'].fillna(2022)
            a = df[df['Vyear']>31].copy()
            b = df[df['Vyear']<32].copy()
            b = b.rename(columns={'Vyear': 'Vday1', 'Vday': 'Vyear'})
            b = b.rename(columns={'Vday1': 'Vday'})
            df = pd.concat([a,b])
            dfa = df.shape[0]

            # #SORTING THE TRANSFER IN DATE YEARS
            df[['Tiyear', 'Tiday']] =df[['Tiyear','Tiday']].apply(pd.to_numeric, errors = 'coerce')
            df['Tiyear'] = df['Tiyear'].fillna(2022)
            a = df[df['Tiyear']>31].copy()
            b = df[df['Tiyear']<32].copy()
            b = b.rename(columns={'Tiyear': 'Tiday1', 'Tiday': 'Tiyear'})
            b = b.rename(columns={'Tiday1': 'Tiday'})
            df = pd.concat([a,b])
            dfb = df.shape[0]

            # #SORTING THE RETURN VISIT DATE YEARS
            df[['Rday', 'Ryear']] = df[['Rday', 'Ryear']].apply(pd.to_numeric, errors='coerce')
            df['Ryear'] = df['Ryear'].fillna(2022)
            a = df[df['Ryear']>31].copy()
            b = df[df['Ryear']<32].copy()
            b = b.rename(columns={'Ryear': 'Rday1', 'Rday': 'Ryear'})
            b = b.rename(columns={'Rday1': 'Rday'})

            df = pd.concat([a,b])
            dfc = df.shape[0]
            #SORTING THE TRANSFER OUT DATE YEAR
            df[['Tday', 'Tyear']] = df[['Tday', 'Tyear']].apply(pd.to_numeric, errors='coerce')
            df['Tyear'] = df['Tyear'].fillna(1994)
            a = df[df['Tyear']>31].copy()
            b = df[df['Tyear']<32].copy()
            b = b.rename(columns={'Tyear': 'Tday1', 'Tday': 'Tyear'})
            b = b.rename(columns={'Tday1': 'Tday'})
            df = pd.concat([a,b])

            # dfd = df.shape[0]
            #SORTING THE ART START YEARS
            df[['Ayear', 'Amonth', 'Aday']] =df[['Ayear', 'Amonth', 'Aday']].apply(pd.to_numeric, errors = 'coerce')
            df['Ayear'] = df['Ayear'].fillna(2022)
            a = df[df['Ayear']>31].copy()
            b = df[df['Ayear']<32].copy()
            b = b.rename(columns={'Ayear': 'Aday1', 'Aday': 'Ayear'})
            b = b.rename(columns={'Aday1': 'Aday'})
            df = pd.concat([a,b])
            dfe = df.shape[0]

            #file = r"C:\Users\Desire Lumisa\Desktop\TX CURR\MATEETE.xlsx"
            file2 = r'ALL.xlsx'
            dfx = pd.read_excel(file2)
            
            df[['Tyear', 'Ryear', 'Rmonth', 'Rday', 'Vyear', 'Vmonth', 'Ayear']] = df[['Tyear', 'Ryear', 'Rmonth', 'Rday', 'Vyear', 'Vmonth', 'Ayear']].apply(pd.to_numeric, errors='coerce')
            TXML = df[df['Ryear']==2024].copy()
            TXML[['Rmonth', 'Rday']] = TXML[['Rmonth', 'Rday']].apply(pd.to_numeric, errors='coerce')
            TXML = TXML[((TXML['Rmonth']>3) | ((TXML['Rmonth']==3) & (TXML['Rday']>3)))].copy()
            TXML[['Rmonth', 'Rday']] = TXML[['Rmonth', 'Rday']].apply(pd.to_numeric, errors='coerce')
            TXML = TXML[((TXML['Rmonth']<6) | ((TXML['Rmonth']==6) & (TXML['Rday']<3)))].copy()
            TXML['Tyear'] = pd.to_numeric(TXML['Tyear'], errors='coerce')
            TXML = TXML[TXML['Tyear']==1994].copy()
            a = df[df['Ryear']==2025].copy()
            b = df[df['Ryear']==2024].copy()
            b[['Rmonth', 'Rday']] = b[['Rmonth', 'Rday']].apply(pd.to_numeric, errors='coerce')
            b = b[((b['Rmonth']>6) | ((b['Rmonth']==6) & (b['Rday']>2)))].copy()
            b['Tyear'] = pd.to_numeric(b['Tyear'], errors='coerce')
            b = b[b['Tyear']==1994].copy()
            TXCURR = pd.concat([a,b])
            TXCURR['Ayear'] = pd.to_numeric(TXCURR['Ayear'], errors='coerce')
            c = TXCURR[ TXCURR['Ayear']==2024].copy()
            d = TXCURR[ TXCURR['Ayear']<2024].copy()
            d[['Vyear', 'Vmonth']] = d[['Vyear', 'Vmonth']].apply(pd.to_numeric, errors='coerce')
            e = d[((d['Vyear'] ==2024) | ((d['Vyear'] ==2023) & (d['Vmonth'] >6)))].copy()
            f = d[((d['Vyear'] < 2023) | ((d['Vyear'] ==2023) & (d['Vmonth'] <7)))].copy()
            WVL = pd.concat([c,e])
            NOVL = f.copy()
            df[['Ayear', 'Amonth']] = df[['Ayear', 'Amonth']].apply(pd.to_numeric, errors='coerce')
            TXNEW = df[((df['Ayear']==2024) & (df['Amonth'].isin([4,5,6])))].copy()
            df[['Tiyear', 'Timonth']] = df[['Tiyear', 'Timonth']].apply(pd.to_numeric, errors='coerce')
            TI = df[((df['Tiyear']==2024) & (df['Timonth'].isin([4,5,6])))].copy()
            df[['Tyear', 'Tmonth']] = df[['Tyear', 'Tmonth']].apply(pd.to_numeric, errors='coerce')
            TO = df[df['Tyear']!=1994].copy()
            TO[['Ryear', 'Rmonth', 'Rday']] = TO[['Ryear', 'Rmonth','Rday']].apply(pd.to_numeric, errors='coerce')
            TOa = TO[((TO['Ryear']==2024) & (TO['Rmonth']<7))].copy()
            TOa[['Rmonth', 'Rday']] = TOa[['Rmonth','Rday']].apply(pd.to_numeric, errors='coerce')
            TOa = TOa[((TOa['Rmonth'] >3) | ((TOa['Rmonth'] ==3) & (TOa['Rday'] >3)))].copy()
            TOa[['Tmonth', 'Tyear']] = TOa[['Tmonth','Tyear']].apply(pd.to_numeric, errors='coerce')
            TOa = TOa[((TOa['Tyear']==2024) & (TOa['Tmonth'].isin([4,5,6])))].copy()
            FALSE = TO[((TO['Ryear']>2024) | ((TO['Ryear']==2024) & (TO['Rmonth']>6)))].copy()
            st.write(FALSE.shape[0])
            st.write(TXCURR.shape[0])
            TXCUR = pd.concat([TXCURR,FALSE])
            st.write(TXCUR.shape[0])
            new = TXNEW.shape[0]
            out = TOa.shape[0]
            inn = TI.shape[0]
            curr = TXCUR.shape[0]
            false = FALSE.shape[0]
            lost = TXML.shape[0]
            vl = WVL.shape[0]
            perc = int((vl/curr)*100)
            novl = NOVL.shape[0]
            current_time = time.localtime()
            week = time.strftime("%V", current_time)
            # clusters = list(dfx['CLUSTER'].unique())
            # cluster = st.radio(label='**Choose a cluster**', options=clusters,index=None, horizontal=True)
            # if cluster:
            #     districts = dfx[dfx['CLUSTER']==cluster]
            #     districts = list(districts['DISTRICT'].unique())
            #     district = st.radio(label='**Choose a district**', options=districts,index=None, horizontal=True)
            districts = list(dfx['DISTRICT'].unique())
            district = st.radio(label='**Choose a district**', options=districts,index=None, horizontal=True)
            if district:
                facilities = dfx[dfx['DISTRICT']==district]
                facilities = facilities['FACILITY']
                facility = st.selectbox(label='**Choose a facility**', options=facilities,index=None)
                if facility:
                    preva = dfx[dfx['FACILITY'] == facility]
                    prev = int(preva.iloc[0,3])
                    name =str(preva.iloc[0,4])
                    grow = curr-prev
                    if grow>0:
                        st.success(f'WEBALE {name},😐 you have grown this TXCURR by {grow}, but you need to audit the TIs and TXNEWs, and watch out for RTT 👏👏👏')
                        if perc > 94:
                            st.success(f'Even the VL COVERAGE is good, at {perc}%  👏👏👏')
                        else:
                            st.warning(f'**However the VL COVERAGE is poor, at {perc}%** 🥲')
                    else:
                        st.warning(f'**BANANGE {name}, 😢 you have dropped this TXCURR by {grow}, you need to audit the TXMLs and TOs, and watch out for the dead** 😢😢😢')
                        if perc > 94:
                            st.success(f'BUT the VL COVERAGE is good, at {perc}% 👏')
                        else:
                            st.warning(f'**EVEN the VL COVERAGE is poor, at {perc}%** 😢😢😢')
                    data = pd.DataFrame([{
                                'DISTRICT': district,
                                'FACILITY' : facility,
                                'Q2 CURR':prev,
                                'Q3 CURR': curr,
                                'TXML' : lost,
                                'TX NEW' : new,
                                'TO' : out,
                                'FALSE TO': false,
                                'TI': inn,
                                'HAS VL' : vl,
                                'VL COV (%)': perc,
                                'NO VL' : novl,
                                'WEEK': week           
                                 }])
                    #data = data.set_index('DISTRICT')
                    st.dataframe(data)
                    #SUBMISSION
                    # conn = st.connection('gsheets', type=GSheetsConnection)
                    # exist = conn.read(worksheet ='TXML', usecols = list(range(13)), ttl=5)
                    # existing = exist.dropna(how='all')
                    col1,col2,col3 = st.columns([1,2,1])
                    with col3:
                        submit = st.button('Submit') 
                    if submit:
                        try:
                            conn = st.connection('gsheets', type=GSheetsConnection)
                            exist = conn.read(worksheet ='TXML', usecols = list(range(13)), ttl=5)
                            existing = exist.dropna(how='all')
                            updated = pd.concat([existing, data], ignore_index =True)
                            conn.update(worksheet = 'TXML', data = updated)
                            st.success('Your data above has been submitted')
                        except:
                            st.write("Couldn't submit, poor network")
