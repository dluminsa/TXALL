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

#st.header('CODE UNDER MAINTENANCE, TRY AGAIN TOMORROW')
#st.stop()
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
            if df['TI'].str.contains('YES').any():
                st.write("The transfer in column you are using doesn't have dates but words, like YES, kindly use the right transfer in colum")
                st.stop()
            
            df['AS'] = df['AS'].astype(str)
            df['RD'] = df['RD'].astype(str)
            df['TI'] = df['TI'].astype(str)
            df['TO'] = df['TO'].astype(str)
            df['VD'] = df['VD'].astype(str)
            
            y = pd.DataFrame({'A' :['2','3','4'], 'TI':['1-1-1',1,'1/1/1'], 'RD':['1-1-1',1,'1/1/1'], 
                              'TO':['1-1-1',1,'1/1/1'], 'AS':['1-1-1',1,'1/1/1'], 'VD':['1-1-1',1,'1/1/1']})  
            

            df['AS'] = df['AS'].str.replace('00:00:00', '', regex=True)
            df['RD'] = df['RD'].str.replace('00:00:00', '', regex=True)
            df['VD'] = df['VD'].str.replace('00:00:00', '', regex=True)
            df['TO'] = df['TO'].str.replace('00:00:00', '', regex=True)
            df['TI'] = df['TI'].str.replace('00:00:00', '',regex=True)
            df = pd.concat([df,y])


            df['AS'] = df['AS'].astype(str)
            df['RD'] = df['RD'].astype(str)
            df['TI'] = df['TI'].astype(str)
            df['TO'] = df['TO'].astype(str)
            df['VD'] = df['VD'].astype(str)


            # SPLITTING ART START DATE
            A = df[df['AS'].str.contains('-')]
            a = df[~df['AS'].str.contains('-')]
            B = a[a['AS'].str.contains('/')]
            C = a[~a['AS'].str.contains('/')]

            A[['Ayear', 'Amonth', 'Aday']] = A['AS'].str.split('-', expand = True)
            B[['Ayear', 'Amonth', 'Aday']] = B['AS'].str.split('/', expand = True)
                        
            C['AS'] = pd.to_numeric(C['AS'], errors='coerce')
            C['AS'] = pd.to_datetime(C['AS'], origin='1899-12-30', unit='D', errors='coerce')
            C['AS'] =  C['AS'].astype(str)
            C[['Ayear', 'Amonth', 'Aday']] = C['AS'].str.split('-', expand = True)
            df = pd.concat([A,B,C])
          
            # SORTING THE RETURN VISIT DATE
            A = df[df['RD'].str.contains('-')]
            a = df[~df['RD'].str.contains('-')]
            B = a[a['RD'].str.contains('/')]
            C = a[~a['RD'].str.contains('/')]
      
            A[['Ryear', 'Rmonth', 'Rday']] = A['RD'].str.split('-', expand = True)
            B[['Ryear', 'Rmonth', 'Rday']] = B['RD'].str.split('/', expand = True)
                        
            C['RD'] = pd.to_numeric(C['RD'], errors='coerce')
            C['RD'] = pd.to_datetime(C['RD'], origin='1899-12-30', unit='D', errors='coerce')
            C['RD'] =  C['RD'].astype(str)
            C[['Ryear', 'Rmonth', 'Rday']] = C['RD'].str.split('-', expand = True)
            df = pd.concat([A,B,C]) 
          
            #SORTING THE VD DATE
            A = df[df['VD'].str.contains('-')]
            a = df[~df['VD'].str.contains('-')]
            B = a[a['VD'].str.contains('/')]
            C = a[~a['VD'].str.contains('/')]

            A[['Vyear', 'Vmonth', 'Vday']] = A['VD'].str.split('-', expand = True)
            B[['Vyear', 'Vmonth', 'Vday']] = B['VD'].str.split('/', expand = True)
                        
            C['VD'] = pd.to_numeric(C['VD'], errors='coerce')
            C['VD'] = pd.to_datetime(C['VD'], origin='1899-12-30', unit='D', errors='coerce')
            C['VD'] =  C['VD'].astype(str)
            C[['Vyear', 'Vmonth', 'Vday']] = C['VD'].str.split('-', expand = True)
            df = pd.concat([A,B,C])

            #SORTING THE TO DATE
            A = df[df['TO'].str.contains('-')]
            a = df[~df['TO'].str.contains('-')]
            B = a[a['TO'].str.contains('/')]
            C = a[~a['TO'].str.contains('/')]

            A[['Tyear', 'Tmonth', 'Tday']] = A['TO'].str.split('-', expand = True)
            B[['Tyear', 'Tmonth', 'Tday']] = B['TO'].str.split('/', expand = True)
                        
            C['TO'] = pd.to_numeric(C['TO'], errors='coerce')
            C['TO'] = pd.to_datetime(C['TO'], origin='1899-12-30', unit='D', errors='coerce')
            C['TO'] =  C['TO'].astype(str)
            C[['Tyear', 'Tmonth', 'Tday']] = C['TO'].str.split('-', expand = True)
            df = pd.concat([A,B,C])
        

           #SORTING THE TI DATE
            A = df[df['TI'].str.contains('-')]
            a = df[~df['TI'].str.contains('-')]
            B = a[a['TI'].str.contains('/')]
            C = a[~a['TI'].str.contains('/')]

            A[['Tiyear', 'Timonth', 'Tiday']] = A['TI'].str.split('-', expand = True)
            B[['Tiyear', 'Timonth', 'Tiday']] = B['TI'].str.split('/', expand = True)
                        
            C['TI'] = pd.to_numeric(C['TI'], errors='coerce')
            C['TI'] = pd.to_datetime(C['TI'], origin='1899-12-30', unit='D', errors='coerce')
            C['TI'] =  C['TI'].astype(str)
            C[['Tiyear', 'Timonth', 'Tiday']] = C['TI'].str.split('-', expand = True)
            df = pd.concat([A,B,C])

               #BRINGING BACK THE / IN DATES
            #df[['AS', 'RD', 'VD','TO','TI']] = df[['AS', 'RD', 'VD','TO','TI']].astype(str)
            df['AS'] = df['AS'].astype(str)
            df['RD'] = df['RD'].astype(str)
            df['TI'] = df['TI'].astype(str)
            df['TO'] = df['TO'].astype(str)
            df['VD'] = df['VD'].astype(str)

            #Clearing NaT from te dates
            df['AS'] = df['AS'].str.replace('NaT', '',regex=True)
            df['RD'] = df['RD'].str.replace('NaT', '',regex=True)
            df['VD'] = df['VD'].str.replace('NaT', '',regex=True)
            df['TO'] = df['TO'].str.replace('NaT', '',regex=True)
            df['TI'] = df['TI'].str.replace('NaT', '',regex=True)

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
            #df['Tiyear'] = df['Tiyear'].fillna(2022)
            #df['Timonth'] = df['Timonth'].fillna(2)
            #df['Tiday'] = df['Tiday'].fillna(2)
            try:
               df[['Tiyear', 'Tiday']] =df[['Tiyear','Tiday']].apply(pd.to_numeric, errors = 'coerce')
            except:
                st.write('**There are no dates in the transfer in column**')
                #st. markdown('##')
                st.write('Copy one date from the Return Visit date and paste it in the Transfer in date, and try again')
                st.write('But this will mean the number of Transfer in is wrong but other paarameters will be correct')
                st.markdown('##')
                st.write('**Another option is to extract a new extract with Transfer in Obs date**')
                st.stop()
            df['Tiyear'] = df['Tiyear'].fillna(2022)
            a = df[df['Tiyear']>31].copy()
            b = df[df['Tiyear']<32].copy()
            b = b.rename(columns={'Tiyear': 'Tiday1', 'Tiday': 'Tiyear'})
            b = b.rename(columns={'Tiday1': 'Tiday'})
            df = pd.concat([a,b])
            dfb = df.shape[0]

            # #SORTING THE RETURN VISIT DATE YEARS
            #st.write(df['RD'])
            #st.stop()
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
            dfw = df[df['Ryear'] ==2025].copy()
            dfy = df[df['Ryear'] ==2024].copy()
            dfy[['Rmonth', 'Rday']] = dfy[['Rmonth', 'Rday']].apply(pd.to_numeric, errors = 'coerce')
            dfy = dfy[((dfy['Rmonth']>3) | ((dfy['Rmonth']==3) & (dfy['Rday'] >3)))].copy()
            df = pd.concat([dfw,dfy])
            
            df['Rday1'] = df['Rday'].astype(str).str.split('.').str[0]
            df['Rmonth1'] = df['Rmonth'].astype(str).str.split('.').str[0]
            df['Ryear1'] = df['Ryear'].astype(str).str.split('.').str[0]

            df['Vday1'] = df['Vday'].astype(str).str.split('.').str[0]
            df['Vmonth1'] = df['Vmonth'].astype(str).str.split('.').str[0]
            df['Vyear1'] = df['Vyear'].astype(str).str.split('.').str[0]

            #df['Tiday'] = df['Tiday'].astype(str).str.split('.').str[0]
            #df['Timonth'] = df['Timonth'].astype(str).str.split('.').str[0]
            #df['Tiyear'] = df['Tiyear'].astype(str).str.split('.').str[0]

            df['Aday1'] = df['Aday'].astype(str).str.split('.').str[0]
            df['Amonth1'] = df['Amonth'].astype(str).str.split('.').str[0]
            df['Ayear1'] = df['Ayear'].astype(str).str.split('.').str[0]
            
            df['Tday1'] = df['Tday'].astype(str).str.split('.').str[0]
            df['Tmonth1'] = df['Tmonth'].astype(str).str.split('.').str[0]
            df['Tyear1'] = df['Tyear'].astype(str).str.split('.').str[0]

            df['ART START DATE'] = df['Aday1'] + '/' + df['Amonth1'] + '/' + df['Ayear1']
            df['RETURN DATE'] = df['Rday1'] + '/' + df['Rmonth1'] + '/' + df['Ryear1']
            df['VL DATE'] = df['Vday1'] + '/' + df['Vmonth1'] + '/' + df['Vyear1']
            df['T OUT DATE'] = df['Tday1'] + '/' + df['Tmonth1'] + '/' + df['Tyear1']
            #df['T IN DATE'] = df['Rday1'] + '/' + df['Rmonth1'] + '/' + df['Ryear1']

            df['RETURN DATE'] = pd.to_datetime(df['RETURN DATE'], format='%d/%m/%Y', errors='coerce')
            df['VL DATE'] = pd.to_datetime(df['VL DATE'], format='%d/%m/%Y', errors='coerce')
            df['T OUT DATE'] = pd.to_datetime(df['T OUT DATE'], format='%d/%m/%Y', errors='coerce')
            df['ART START DATE'] = pd.to_datetime(df['ART START DATE'], format='%d/%m/%Y', errors='coerce')

            df['RETURN DATE'] = df['RETURN DATE'].dt.strftime('%d/%m/%Y')
            df['VL DATE'] = df['VL DATE'].dt.strftime('%d/%m/%Y')
            df['T OUT DATE'] = df['T OUT DATE'].dt.strftime('%d/%m/%Y')
            df['ART START DATE'] = df['ART START DATE'].dt.strftime('%d/%m/%Y')
            
            df = df.rename(columns={'A': 'ART NO'})#, 'AS': 'ART START DATE', 'RD': 'RETURN DATE', 'VD': 'VL DATE', 'TO': 'T OUT DATE'})
            potential = df.shape[0]
            df[['Tyear', 'Ryear', 'Rmonth', 'Rday', 'Vyear', 'Vmonth', 'Ayear']] = df[['Tyear', 'Ryear', 'Rmonth', 'Rday', 'Vyear', 'Vmonth', 'Ayear']].apply(pd.to_numeric, errors='coerce')
         
            TXML = df[df['Ryear']==2024].copy()
            TXML[['Rmonth', 'Rday']] = TXML[['Rmonth', 'Rday']].apply(pd.to_numeric, errors='coerce')
            TXML = TXML[((TXML['Rmonth']>3) | ((TXML['Rmonth']==3) & (TXML['Rday']>3)))].copy()
            TXML[['Rmonth', 'Rday']] = TXML[['Rmonth', 'Rday']].apply(pd.to_numeric, errors='coerce')
            TXML = TXML[((TXML['Rmonth']<6) | ((TXML['Rmonth']==6) & (TXML['Rday']<3)))].copy()
            TXML['Tyear'] = pd.to_numeric(TXML['Tyear'], errors='coerce')
            TXML = TXML[TXML['Tyear']==1994].copy()
            
            #TX CURR
            a = df[df['Ryear']==2025].copy()
            b = df[df['Ryear']==2024].copy()
            b[['Rmonth', 'Rday']] = b[['Rmonth', 'Rday']].apply(pd.to_numeric, errors='coerce')
            b = b[((b['Rmonth']>6) | ((b['Rmonth']==6) & (b['Rday']>2)))].copy()
            b['Tyear'] = pd.to_numeric(b['Tyear'], errors='coerce')
            b = b[b['Tyear']==1994].copy()
            TXCURR = pd.concat([a,b])
            #TX NEW
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
            #TOa[['Tmonth', 'Tyear']] = TOa[['Tmonth','Tyear']].apply(pd.to_numeric, errors='coerce')
            #TOa = TOa[((TOa['Tyear']==2024) & (TOa['Tmonth'].isin([4,5,6])))].copy()
            
            FALSE = TO[((TO['Ryear']>2024) | ((TO['Ryear']==2024) & (TO['Rmonth']>6)))].copy()
            TXCUR = pd.concat([TXCURR,FALSE])

            #VL COV
            TXCUR['Ayear'] = pd.to_numeric(TXCUR['Ayear'], errors='coerce')
            c = TXCUR[ TXCUR['Ayear']==2024].copy()
            d = TXCUR[ TXCUR['Ayear']<2024].copy()
            d[['Vyear', 'Vmonth']] = d[['Vyear', 'Vmonth']].apply(pd.to_numeric, errors='coerce')
            e = d[((d['Vyear'] ==2024) | ((d['Vyear'] ==2023) & (d['Vmonth'] >6)))].copy()
            f = d[((d['Vyear'] < 2023) | ((d['Vyear'] ==2023) & (d['Vmonth'] <7)))].copy()
            WVL = pd.concat([c,e])
            NOVL = f.copy()

            POTENTIAL = potential
            new = TXNEW.shape[0]
            out = TOa.shape[0]
            inn = TI.shape[0]
            curr = TXCUR.shape[0]
            false = FALSE.shape[0]
            lost = TXML.shape[0]
            vl = WVL.shape[0]
            perc = round((vl/curr)*100)
            exp = round(curr*0.95)
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
                    UK = potential- prev - inn - new

                    ba = prev - curr
                    if ba > 0:
                        bal == ba
                    elif ba == 0:
                        bal = 'EVEN'
                    elif ba < 0:
                        bal == 'EXCEEDED'
                    grow = curr-prev
                    if grow ==0:
                        st.success(f'WEBALE {name},😐 this TXCURR has broken even (Q2 CURR is equal to Q3 CURR), but you need to add more clients to grow it even further 👏👏👏')
                        if perc > 94:
                            st.success(f'Even the VL COVERAGE is good, at {perc}%  👏👏👏')
                        else:
                            st.warning(f'**However the VL COVERAGE is poor, at {perc}%** 🥲')

                    elif grow>0:
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
                                'UNKNOWN GAIN': UK,
                                'POTENTIAL': potential,
                                'Q3 CURR': curr,
                                'TXML' : lost,
                                 'BALANCE': bal,
                                'TX NEW' : new,
                                'TO' : out,
                                'FALSE TO': false,
                                'TI': inn,
                                'HAS VL' : vl,
                                'VL COV (%)': perc,
                                'EXPECTED': exp,
                                'NO VL' : novl,
                                'WEEK': week           
                                 }])
                    #data = data.set_index('DISTRICT')
                    st.dataframe(data)
                    #SUBMISSION
                    # conn = st.connection('gsheets', type=GSheetsConnection)
                    # exist = conn.read(worksheet ='TXML', usecols = list(range(15)), ttl=5)
                    # existing = exist.dropna(how='all')
                    col1,col2,col3 = st.columns([1,2,1])
                    with col3:
                        submit = st.button('Submit') 
                    if submit:
                        try:
                            conn = st.connection('gsheets', type=GSheetsConnection)
                            exist = conn.read(worksheet ='TXML', usecols = list(range(16)), ttl=5)
                            existing = exist.dropna(how='all')
                            updated = pd.concat([existing, data], ignore_index =True)
                            conn.update(worksheet = 'TXML', data = updated)
                            st.success('Your data above has been submitted')
                        except:
                            st.write("Couldn't submit, poor network")
                    st.write(f"<h6>DOWNLOAD LINELISTS FROM HERE</h6>", unsafe_allow_html=True)
                    cola, colb, colc = st.columns(3)
                    with cola:
                         dat = TXML.copy()
                         dat = dat[['ART NO', 'ART START DATE', 'RETURN DATE', 'VL DATE']]
                         csv_data = dat.to_csv(index=False)
                         st.download_button(
                                     label=" DOWNLOAD TXML",
                                     data=csv_data,
                                     file_name=f"{facility} TXML.csv",
                                     mime="text/csv")
                    with colb:
                         dat = NOVL.copy()
                         dat = dat[['ART NO', 'ART START DATE', 'RETURN DATE', 'VL DATE']]
                         csv_data = dat.to_csv(index=False)
                         st.download_button(
                                         label=" DOWNLOAD WITH NO VL",
                                         data=csv_data,
                                         file_name=f" {facility} NO VL.csv",
                                         mime="text/csv")
                    with colc:
                         dat = TOa.copy()
                         dat = dat[['ART NO', 'ART START DATE', 'RETURN DATE', 'VL DATE', 'T OUT DATE']]
                        
                         csv_data = dat.to_csv(index=False)
                         st.download_button(
                                     label=" DOWNLOAD TRANSFER OUTS",
                                     data=csv_data,
                                     file_name=f" {facility} T OUTS.csv",
                                     mime="text/csv")
