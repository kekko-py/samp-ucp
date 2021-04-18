################################################################################################################################
#
#                                                        Roleplay WEB Panel
#                                                   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#-------------------------------------------------------------------------------------------------------------------------------
#
#                                                 [|]_______________________________ 
#                                                |                                |] 
#                                               |  Developed by kekko.py [100%]  |
#                                              |        ________________________|
#                                             |        |_]   |   
#                                            |        |_____/
#                                           |        |
#                                          |________| 
#
#-------------------------------------------------------------------------------------------------------------------------------
#
#                                                   |---- COFFEE TO CODE ----|  
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
################################################################################################################################
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#                                             CREDITS: Francesco De Rosa [@kekko.py] 
#                              27/10/2020   Prima scrittura del codice [Francesco De Rosa (kekko.py)]

# 
# {UCP V0.9.8}
#-------------------------------------------------------------
#SEZIONI:

#	• SEZIONE REGOLAMENTI
#	• SEZIONE VIP
#   • SEZIONE NEWS
#	• SEZIONE FAZIONE
#	• SEZIONE PERSONAGGIO (Lettura sms, fedina, cartella clinica)
#	• SEZIONE RINGRAZIAMENTI
#	• SEZIONE (LINK) Fake-Book.it

#FUNZIONALITÀ FAZIONI:

#        POLIZIA
#	•	Aggiungi Reato
#	•	Visualizza reati
#	•	Avviso news
#	•	Messaggio privato
#	•	Verifica arruolamento 
#	•	Pulisci fedina
#	•	Veicoli sequestrati 

#        MEDICI
#	•	Aggiungi Referto clinico
#	•	Visualizza referti
#	•	Messaggio privato
#	•	Avviso news
                
#        SAN NEWS
#	•	Aggiungi news
#	•	Messaggio privato 
#-------------------------------------------------------------

# {UCP V0.9.9} Primo sviluppo 18/04/2021 [Francesco De Rosa (kekko.py)]

#   • Aggiunta La funzionalità Statistiche nella sezione Personaggio.
#   • Aggiunta la possibiltà di cambiare il personaggio senza logout.
#   • Modificato il corpo della sezione ringraziamenti.
#   • Fixato il bug che faceva bloccare l'ucp a tutti a causa del timeout del Mysql.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
################################################################################################################################

#_______________CREDITI__________________
def credts_spam():
    return Fore.LIGHTMAGENTA_EX +'''
    ###################################################### 
                       ROLEPLAY WEB PANEL
                 ______________________________
                /                              \\                     
              \\|     Project SF - web panel    |/
              <|  Developed by kekko.py [100%]  |>
              /|   |---- COFFEE TO CODE ----|   |\\ 
                \\______________________________/

                          v0.9.9 [BETA]
    ######################################################
    '''+ Fore.RESET

# _______________INCLUSIONE LIBRERIE__________________
# pip install flask colorama configparser pymysql telepot
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from colorama import Fore, Back, Style, init
#from werkzeug.utils import secure_filename
from configparser import ConfigParser
import pymysql
import hashlib
import telepot
import random
import time
import os


init()
# _______________LETTURA DATI CONFIG.CFG__________________
config = ConfigParser()
config.read("config.cfg")

query = ConfigParser()
query.read("query.cfg")

funzionalita = ConfigParser()
funzionalita.read("funzioni.cfg")

rank_funzionalita = ConfigParser()
rank_funzionalita.read("gradi_fazioni.cfg")
# _______________VARIABILI GLOBALI ACCOUNT_______________
__key__ = config.get("ACCOUNT", 'license_key')
# _______________VARIABILI GLOBALI DATABASE_______________
__host__ = config.get("MYSQL", 'host')
__port__ = config.get("MYSQL", 'port')
__dbname__ = config.get("MYSQL", 'database_name')
__dbuser__ = config.get("MYSQL", 'username')
__dbpass__ = config.get("MYSQL", 'password')

try:
   connection = pymysql.connect(host=__host__,user=__dbuser__,password=__dbpass__,database=__dbname__,autocommit=True)    
   connection.close()
   __cursor__ = True
except:
    __cursor__ = False

# _______________VARIABILI GLOBALI QUERY_______________
query1 = query.get("IBAN", 'query1')
query2 = query.get("IBAN", 'query2')
query3 = query.get("IBAN", 'query3')

query4 = query.get("LOGIN", 'query4')
query5 = query.get("LOGIN", 'query5')

query6 = query.get("BANK", 'query6')
query7 = query.get("BANK", 'query7')
query8 = query.get("BANK", 'query8')
query19 = query.get("BANK", 'query19')

query11 = query.get("DIGIT", 'query11')
query12 = query.get("DIGIT", 'query12')
query13 = query.get("DIGIT", 'query13')

query21 = query.get("FAZIONE", 'query21')

query22 = query.get("POLIZIA", 'query22')
query23 = query.get("POLIZIA", 'query23')
query24 = query.get("POLIZIA", 'query24')
query25 = query.get("POLIZIA", 'query25')
query26 = query.get("POLIZIA", 'query26')

# _______________VARIABILI GLOBALI FAZIONE_______________
id_null = int(config.get("FAZIONI", 'null'))
id_pula = int(config.get("FAZIONI", 'polizia'))
id_ems = int(config.get("FAZIONI", 'medici'))
id_sfnn = int(config.get("FAZIONI", 'sfnn'))
# _______________VARIABILI GLOBALI WEB-APP_______________
__app__ = Flask(__name__)
__state__ = int(config.get("WEB-APP", 'state'))
porta_server = int(config.get("WEB-APP", 'porta'))
debug_server = int(config.get("WEB-APP", 'debug'))
#_____________VARIABILI GLOBALI FUNZIONALITA'____________
sez_reg = int(funzionalita.get("SEZIONI",'reg'))
sez_vip = int(funzionalita.get("SEZIONI",'vip'))
sez_news = int(funzionalita.get("SEZIONI",'news'))
sez_maze = int(funzionalita.get("SEZIONI",'maze'))
sez_digit = int(funzionalita.get("SEZIONI",'digit'))
sez_fazione = int(funzionalita.get("SEZIONI",'fazione'))
sez_concessionaria = int(funzionalita.get("SEZIONI",'concessionaria'))
sez_personaggio = int(funzionalita.get("SEZIONI",'personaggio'))
sez_ringraziamenti = int(funzionalita.get("SEZIONI",'ringraziamenti'))

registra_reato = int(funzionalita.get("POLIZIA",'registra_reato'))
visualizza_fedpen = int(funzionalita.get("POLIZIA",'visualizza_fedina'))
visualizza_trans = int(funzionalita.get("POLIZIA",'visualizza_trans'))
blocca_conto = int(funzionalita.get("POLIZIA",'blocca_conto'))
verifica_arruolamento =  int(funzionalita.get("POLIZIA",'verifica_arruolamento'))
avviso_comunale_pol =  int(funzionalita.get("POLIZIA",'avviso_comunale'))
mess_priv_pol = int(funzionalita.get("POLIZIA",'mess_priv'))
pulizia_fedina = int(funzionalita.get("POLIZIA",'pulizia_fedina'))
veicoli_seq = int(funzionalita.get("POLIZIA",'veicoli_seq'))

visualizza_cartella = int(funzionalita.get("MEDICI",'visualizza_cartella'))
agg_referto =  int(funzionalita.get("MEDICI",'agg_referto'))
avviso_comunale_med =  int(funzionalita.get("MEDICI",'avviso_comunale'))
mess_priv_med =  int(funzionalita.get("MEDICI",'mess_priv'))

crea_articolo = int(funzionalita.get("SFNN","articolo"))
avviso_comunale_sfnn = int(funzionalita.get("SFNN","avviso_comunale"))
mess_priv_sfnn = int(funzionalita.get("SFNN","mess_priv"))

#_____________VARIABILI RANK GLOBALI FUNZIONALITA'____________
rank_registra_reato = int(rank_funzionalita.get("POLIZIA",'registra_reato'))
rank_visualizza_fedpen = int(rank_funzionalita.get("POLIZIA",'visualizza_fedina'))
rank_visualizza_trans = int(rank_funzionalita.get("POLIZIA",'visualizza_trans'))
rank_blocca_conto = int(rank_funzionalita.get("POLIZIA",'blocca_conto'))
rank_verifica_arruolamento =  int(rank_funzionalita.get("POLIZIA",'verifica_arruolamento'))
rank_avviso_comunale_pol =  int(rank_funzionalita.get("POLIZIA",'avviso_comunale'))
rank_mess_priv_pol = int(rank_funzionalita.get("POLIZIA",'mess_priv'))
rank_pulizia_fedina = int(rank_funzionalita.get("POLIZIA",'pulizia_fedina'))
rank_veicoli_seq = int(rank_funzionalita.get("POLIZIA",'rank_veicoli_seq'))

rank_visualizza_cartella = int(rank_funzionalita.get("MEDICI",'visualizza_cartella'))
rank_agg_referto =  int(rank_funzionalita.get("MEDICI",'agg_referto'))
rank_avviso_comunale_med =  int(rank_funzionalita.get("MEDICI",'avviso_comunale'))
rank_mess_priv_med =  int(rank_funzionalita.get("MEDICI",'mess_priv'))

rank_crea_articolo = int(rank_funzionalita.get("SFNN","articolo"))
rank_avviso_comunale_sfnn = int(rank_funzionalita.get("SFNN","avviso_comunale"))
rank_mess_priv_sfnn = int(rank_funzionalita.get("SFNN","mess_priv"))

# _______________VARIABILI GLOBALI TEMPLATE_______________
template = "" 
credit = '<div class="small text-light">POWERED BY:</div>@kekko.py</div>'
#_____________VARIABILI GLOBALI FAZIONE____________
max_arrest = int(config.get("POLIZIA", 'max_arrest'))

#_____________________║QUERY MYSQL ESECUTORE║­­____________________
def dbrequest(query,fetch="none"):
    global connection
    connection = pymysql.connect(host=__host__,user=__dbuser__,password=__dbpass__,database=__dbname__,autocommit=True)
    cursor = connection.cursor()

    cursor.execute(query)
    if fetch=="fetchone": data = cursor.fetchone()
    elif fetch=="fetchall": data = cursor.fetchall()
    else: data=0

    cursor.close()
    connection.close()

    if data!=0: return data

#_____________________║CONTROLLO INPUT ESTERNO║­­____________________
#Per eventuali attacchi mysql injectiond
def controllo_input(string):
    if string.count("'")>0 or string.count('"')>0 :
        return 0
    
    else: return 1

#_____________________║SISTEMA SALVATAGGIO LOG║­­____________________
#BOT KEYS FOR LOGS
pd_chat_key = -520833055
ems_chat_key = -522143537
sfnn_chat_key = -487923137
admin_chat_key = -1001201314801
bot = telepot.Bot('1698925075:AAHNc8ITikXpcpQUi9N-VtdGlyV_Ow39oXY')
def save_log(fazione,name,azione,motivazione):
    data_ora = time.ctime()
    if fazione=="pd":
        dbrequest(f'INSERT INTO logs_polizia (name,azione,motivazione,data_ora) VALUES ("{name}","{azione}","{motivazione}","{data_ora}")')
        bot.sendMessage(pd_chat_key, f'<b>AGENTE:</b>\n<code>{name}</code>\n<b>AZIONE:</b>\n<code>{azione}</code>\n<b>MOTIVAZIONE:</b>\n<code>{motivazione}</code>', parse_mode= 'html')
        bot.sendMessage(admin_chat_key, f'<b>AGENTE:</b>\n<code>{name}</code>\n<b>AZIONE:</b>\n<code>{azione}</code>\n<b>MOTIVAZIONE:</b>\n<code>{motivazione}</code>', parse_mode= 'html')
    elif fazione=="ems":
        dbrequest(f'INSERT INTO logs_ems (name,azione,motivazione,data_ora) VALUES ("{name}","{azione}","{motivazione}","{data_ora}")')
        bot.sendMessage(ems_chat_key, f'<b>MEDICO:</b>\n<code>{name}</code>\n<b>AZIONE:</b>\n<code>{azione}</code>\n<b>MOTIVAZIONE:</b>\n<code>{motivazione}</code>', parse_mode= 'html')
        bot.sendMessage(admin_chat_key, f'<b>MEDICO:</b>\n<code>{name}</code>\n<b>AZIONE:</b>\n<code>{azione}</code>\n<b>MOTIVAZIONE:</b>\n<code>{motivazione}</code>', parse_mode= 'html')
    elif fazione=="sfnn":
        dbrequest(f'INSERT INTO logs_sfnn (name,azione,motivazione,data_ora) VALUES ("{name}","{azione}","{motivazione}","{data_ora}")')
        bot.sendMessage(sfnn_chat_key, f'<b>DIPENDENTE:</b>\n<code>{name}</code>\n<b>AZIONE:</b>\n<code>{azione}</code>\n<b>MOTIVAZIONE:</b>\n<code>{motivazione}</code>', parse_mode= 'html')
        bot.sendMessage(admin_chat_key, f'<b>DIPENDENTE:</b>\n<code>{name}</code>\n<b>AZIONE:</b>\n<code>{azione}</code>\n<b>MOTIVAZIONE:</b>\n<code>{motivazione}</code>', parse_mode= 'html')
#_____________________║GENERATORE E CONTROLLO IBAN║­­____________________
def generatore_iban():
    i = 1
    while i == 1:
        prefisso = "555"
        sufisso = str(random.randint(100, 999))
        iban = prefisso+sufisso
        data = dbrequest(query1+f'"{iban}"', 'fetchone')
        try:
            iban = data[0]
            i = 1
        except:
            i = 0
            dbrequest(query2+f'"{iban}" WHERE nome="{session["username"]}"')
            print(iban)
            return home()
#------------------------------------------------------
def controllo_iban():
    data = dbrequest(query3+f'"{session["username"]}"', "fetchone")
    iban = data[0]
    if not iban:
        return generatore_iban()
    else:
        return home()
#_____________________║BG SYSTEM║­­____________________  
def add_porz_bg(user,contenuto):
    try:
        data_ora = time.ctime()
        dbrequest(f'INSERT INTO bg (user,contenuto,data_ora) VALUES ("{user}","{contenuto}","{data_ora}")')
        return 1
    except:
        return 0
#----------
def get_bg(user):
    try:
        
        data = dbrequest('SELECT contenuto,data_ora FROM bg WHERE user="{user}" ORDER BY id DESC', "fetchall")
        return data
    except:
        return 0
#_____________________║SMS SYSTEM║­­____________________   
def sms_send(n_mittente,n_destinatario,contenuto):
    try:
        data_ora = time.ctime()
        dbrequest(f'INSERT INTO message (n_mittente,n_destinatario,contenuto,data_ora) VALUES ("{n_mittente}","{n_destinatario}","{contenuto}","{data_ora}")')
        return 1
    except:
        return 0

def visualizza_sms(user):
    try:
        sms = []
        data = dbrequest(f'SELECT * FROM message WHERE n_destinatario="{user}" ORDER BY id DESC', "fetchall") 
        for i in data:
            n_mittente = i[1]
            n_destinatario = i[2]
            contenuto = i[3]
            data_ora = i[4]

            if n_mittente=="911":
                n_mittente="San Fierro Police Department [911]"
            elif n_mittente=="118":
                n_mittente="San Fierro Medical [118]"
            elif n_mittente=="333":
                n_mittente="San Fierro News Network [333]"

            sms.append([n_mittente,n_destinatario,contenuto,data_ora])           
        return sms
    except:
        return 0
        
#--------
#_____________________║NEWS SYSTEM║­­____________________        
def nuova_news_text(id_faz,autore,news,fazione):
    try:
        tempo_attuale = time.ctime()
        dbrequest(f'INSERT INTO news (fazid, autore, text_news, data_ora, fazione, immagine, prezzo, numero) VALUES ({id_faz},"{autore}","{news}","{tempo_attuale}","{fazione}","N/A",0,0)')
        return 1
    except:
        return 0
#_____________________║REATI SYSTEM║­­____________________
def nuovo_reato(user,reato,multa,prigione,poliziotto):
    try:
        data_ora = time.ctime()
        dbrequest(f'INSERT INTO reati (user,reato,multa,prigione,poliziotto,data_ora) VALUES ("{user}","{reato}","{multa}","{prigione}","{poliziotto}","{data_ora}")')
        if bool(prigione):
            data = dbrequest(query23+f'"{user}"', "fetchone")
            dbrequest(f'UPDATE personaggi SET Arresti_ucp={int(data[0])+1} WHERE nome="{user}"')
            text_news = f"{user} è stato Arrestato da {poliziotto}, dopo aver pagato una multa di {multa}$, I reati sono: {reato}"
            save_log("pd",poliziotto,"Arresto di "+user,reato)
            #nuova_news_text(id_pula,poliziotto,text_news,"SF-Police Department")
            return 1
        save_log("pd",poliziotto,f"Multa a {user} di {multa}$",reato)
        return 1
    except:
        return 0
#--------
def pulisci_fedina(poliziotto,user,motivo=""):
    try:
        dbrequest(f'DELETE FROM reati WHERE user="{user}"')
        data_ora = time.ctime()
        save_log("pd",poliziotto,"Pulizia della fedina di "+ user ,motivo)
        return 1
    except:  
        return 0 
#--------
def visualizza_fedina(user):
    try:
        reati = []
        data = dbrequest(f'SELECT * FROM reati WHERE user="{user}" ORDER BY id DESC', "fetchall") 
        for i in data:
            reato = i[2]
            multa = i[3]
            prigione = i[4]
            poliziotto = i[5]
            data_ora = i[6]

            classe = "alert-primary"
            if multa > 0:    
                cont_multa = f"- Ha Pagato una multa di {multa}"
                if multa >= 2000:
                    classe = "alert-warning"
            else:
                cont_multa = ""

            if prigione == 1:
                classe = "alert-danger"
                contenuto2 = "- Ha scontato la sua pena in carcere!"
            else:
                contenuto2 = ""

            contenuto = f'{user} ha commesso: {reato}.'
            multato = f'È Stato Segnalato da: {poliziotto}.'

            reati.append([classe,contenuto,multato,cont_multa,contenuto2,data_ora])           
        return reati
    except:
        return 0
        
#--------
def transazione_bank_user(user,tabella):
    
    transazioni = []
    try:
        transazioni_data = dbrequest(f'SELECT * FROM {tabella} WHERE mittente="{user}" OR destinatario="{user}" ORDER BY id DESC', "fetchall")
        for i in transazioni_data:
            mittente = i[1]
            destinatario = i[2]
            importo = i[3]
            oggetto = i[4]
            data_ora = i[5]
        
            if mittente == user:
                classe = 'alert-danger'
                contenuto = f'Inviati {importo}$ a {destinatario}'
                causale = f'Causale: [{oggetto}]'
                data_ora = data_ora
                transazioni.append([classe,contenuto,causale,data_ora])

            if destinatario == user:
                classe = 'alert-success'
                contenuto = f'Ricevuti {importo}$ da {mittente}'
                causale = f'Causale: [{oggetto}]'
                data_ora = data_ora
                transazioni.append([classe,contenuto,causale,data_ora])
        return transazioni
    except:
        return []
#--------------
def pil_citta():
    try:
        pil = 0
        pil_data = dbrequest(query22, "fetchall")
        for i in pil_data:
            pil += i[0]
        return pil    
    except: return 0;
#--------------
def transazioni_citta(user=" "):
    try:
        if user==" ":
            que=" "
        else:
            que=f'WHERE mittente="{user}" or destinatario="{user}"'
        transazioni = []
        transazioni_data = dbrequest(f'SELECT * FROM transazioni {que} ORDER BY id DESC', "fetchall")
        for i in transazioni_data:
            mittente = i[1]
            destinatario = i[2]
            importo = i[3] 
            oggetto = i[4]
            data_ora = i[5]
            
            if importo >= 100000:
                classe = 'alert-danger'
            elif importo >= 50000:
                classe = 'alert-warning'
            elif importo >= 10000:
                classe = 'alert-warning'
            else:
                classe = 'alert-primary'

            contenuto = f'{mittente} ha inviato {importo}$ a {destinatario}'
            causale = f'Causale: [{oggetto}]'
            transazioni.append([classe,contenuto,causale,data_ora])

        return transazioni
    except:
        return 0
#-----------------
def validata_arruolamento(user):
    try:
        data = dbrequest(query23+f'"{user}"', "fetchone")
        if data[0] > max_arrest:
            return "no"
        else:
            return "si"
    except:
        return 0
#-------------------
def blocca_conto_funct(poliziotto,user,motivazione):
    try:
        data = dbrequest(query24+f'"{user}"', "fetchone")
        if data[0] == 1:
            dbrequest(query25+f'"{user}"')
            save_log("pd",poliziotto,"Bloccato il conto di "+user,motivazione)
            return "si"
        else:
            return "gia_bloccato"

    except:
        return 0
#-------------------
def sblocca_conto(poliziotto,user,motivazione):
    try:
        data = dbrequest(query24+f'"{user}"', "fetchone")
        if data[0] == 0:
            dbrequest(query26+f'"{user}"')
            save_log("pd",poliziotto,"Sbloccato il conto di "+user,motivazione)
            return "si"
        else:
            return "non_bloccato"

    except:
        return 0
#-------------------
def modelli_auto(id):
    if id==400: return "Landstalker"
    if id==401: return "Bravura"
    if id==402: return "Buffalo"
    if id==403: return "Linerunner"
    if id==404: return "Perenail"
    if id==405: return "Sentinel"
    if id==406: return "Dumper"
    if id==407: return "Firetruck"
    if id==408: return "Trashmaster"
    if id==409: return "Stretch"
    if id==410: return "Manana"
    if id==411: return "Infernus"
    if id==412: return "Voodoo"
    if id==413: return "Pony"
    if id==414: return "Mule"
    if id==415: return "Cheetah"
    if id==416: return "Ambulance"
    if id==417: return "Levetian"
    if id==418: return "Moonbeam"
    if id==419: return "Esperanto"
    if id==420: return "Taxi"
    if id==421: return "Washington"
    if id==422: return "Bobcat"
    if id==423: return "Mr Whoopee"
    if id==424: return "BF Injection"
    if id==425: return "Hunter"
    if id==426: return "Premier"
    if id==427: return "Enforcer"
    if id==428: return "Securicar"
    if id==429: return "Banshee"
    if id==430: return "Predator"
    if id==431: return "Bus"
    if id==432: return "Rhino"
    if id==433: return "Barracks"
    if id==434: return "Hotknife"
    if id==435: return "Artic Trailer 1"
    if id==436: return "Previon"
    if id==437: return "Coach"
    if id==438: return "Cabbie"
    if id==439: return "Stallion"
    if id==440: return "Rumpo"
    if id==441: return "RC Bandit"
    if id==442: return "Romero"
    if id==443: return "Packer"
    if id==444: return "Monster"
    if id==445: return "Admiral"
    if id==446: return "Squalo"
    if id==447: return "Seasparrow"
    if id==448: return "Pizza Boy"
    if id==449: return "Tram"
    if id==450: return "Artic Trailer 2"
    if id==451: return "Turismo"
    if id==452: return "Speeder"
    if id==453: return "Reefer"
    if id==454: return "Tropic"
    if id==455: return "Flatbed"
    if id==456: return "Yankee"
    if id==457: return "Caddy"
    if id==458: return "Solair"
    if id==459: return "Top Fun"
    if id==460: return "Skimmer"
    if id==461: return "PCJ-600"
    if id==462: return "Faggio"
    if id==463: return "Freeway"
    if id==464: return "RC Baron"
    if id==465: return "RC Raider"
    if id==466: return "Glendale"
    if id==467: return "Oceanic"
    if id==468: return "Sanchez"
    if id==469: return "Sparrow"
    if id==470: return "Patriot"
    if id==471: return "Quad"
    if id==472: return "Coastguard"
    if id==473: return "Dighy"
    if id==474: return "Hermes"
    if id==475: return "Sabre"
    if id==476: return "Rustler"
    if id==477: return "ZR-350"
    if id==478: return "Walton"
    if id==479: return "Regina"
    if id==480: return "Comet"
    if id==481: return "BMX"
    if id==482: return "Burrito"
    if id==483: return "Camper"
    if id==484: return "Marquis"
    if id==485: return "Baggage"
    if id==486: return "Dozer"
    if id==487: return "Maverick"
    if id==488: return "SAN Maverick"
    if id==489: return "Rancher"
    if id==490: return "FBI Rancher"
    if id==491: return "Virgo"
    if id==492: return "Greenwood"
    if id==493: return "Jetmax"
    if id==494: return "Hotring"
    if id==495: return "Sandking"
    if id==496: return "Blista Compact"
    if id==497: return "Police Maverick"
    if id==498: return "Boxville"
    if id==499: return "Benson"
    if id==500: return "Mesa"
    if id==501: return "RC Goblin"
    if id==502: return "Hotring A"
    if id==503: return "Hotring B"
    if id==504: return "Bloodring Banger"
    if id==505: return "Rancher (lure)"
    if id==506: return "Super GT"
    if id==507: return "Elegant"
    if id==508: return "Journey"
    if id==509: return "Bike"
    if id==510: return "Mountain bike"
    if id==511: return "Beagle"
    if id==512: return "Cropduster"
    if id==513: return "Stuntplane"
    if id==514: return "Petrol"
    if id==515: return "Roadtrain"
    if id==516: return "Nebula"
    if id==517: return "Majestic"
    if id==518: return "Buccaneer"
    if id==519: return "Shamal"
    if id==520: return "Hydra"
    if id==521: return "FCR-900"
    if id==522: return "NRG-500"
    if id==523: return "HPV-1000"
    if id==524: return "Cement Truck"
    if id==525: return "Tow Truck"
    if id==526: return "Fortune"
    if id==527: return "Cadrona"
    if id==528: return "FBI Truck"
    if id==529: return "Williard"
    if id==530: return "Forklift"
    if id==351: return "Tractor"
    if id==532: return "Combine"
    if id==533: return "Feltzer"
    if id==534: return "Remington"
    if id==535: return "Slamvan"
    if id==536: return "Blade"
    if id==537: return "Freight"
    if id==538: return "Streak"
    if id==539: return "Vortex"
    if id==540: return "Vincent"
    if id==541: return "Bullet"
    if id==542: return "Clover"
    if id==543: return "Sadler"
    if id==544: return "Firetruck LS"
    if id==545: return "Hustler"
    if id==546: return "Intruder"
    if id==547: return "Primo"
    if id==548: return "Cargobob"
    if id==549: return "Tampa"
    if id==550: return "Sunrise"
    if id==551: return "Merit"
    if id==552: return "Utility Van"
    if id==553: return "Nevada"
    if id==554: return "Yosemite"
    if id==555: return "Windsor"
    if id==556: return "Monster A"
    if id==557: return "Monster B"
    if id==558: return "Uranus"
    if id==559: return "Jester"
    if id==560: return "Sultan"
    if id==561: return "Stratum"
    if id==562: return "Elegy"
    if id==563: return "Raindance"
    if id==564: return "RC Tiger"
    if id==565: return "Flash"
    if id==566: return "Tahoma"
    if id==567: return "Savanna"
    if id==568: return "Bandito"
    if id==569: return "Freight Flat"
    if id==570: return "Streak"
    if id==571: return "Kart"
    if id==572: return "Mower"
    if id==573: return "Duneride"
    if id==574: return "Sweeper"
    if id==575: return "Broadway"
    if id==576: return "Tornado"
    if id==577: return "AT-400"
    if id==578: return "DFT-30"
    if id==579: return "Huntley"
    if id==580: return "Stafford"
    if id==581: return "BF-400"
    if id==582: return "News van"
    if id==583: return "Tug"
    if id==584: return "Petrol Tanker"
    if id==585: return "Emperor"
    if id==586: return "Wayfarer"
    if id==587: return "Euros"
    if id==588: return "Hotdog"
    if id==589: return "Club"
    if id==590: return "Freight box"
    if id==591: return "Artic Trailer"
    if id==592: return "Andromada"
    if id==593: return "Dodo"
    if id==594: return "RC Cam"
    if id==595: return "Launch"
    if id==596: return "Cop Car LS"
    if id==597: return "Cop Car SF"
    if id==598: return "Cop Car LV"
    if id==599: return "Ranger"
    if id==600: return "Picador"
    if id==601: return "Swat Tank"
    if id==602: return "Alpha"
    if id==603: return "Phoenix"
    if id==604: return "Glendale (damaged)"
    if id==605: return "Sadler (damaged)"
    if id==606: return "Bag Box A"
    if id==607: return "Bag Box B"
    if id==608: return "Stairs"
    if id==609: return "Boxville (black)"
    if id==610: return "Farm Trailer"
    if id==611: return "Utility Trailer"

def visualizza_sequestri():
    try:
        veicoli = []
        data = dbrequest("SELECT * FROM veicoli_sequestrati", "fetchall")
        for i in data:
            id_veh = i[1]
            poliziotto = i[2]
            data_ora = i[3]

            dativeicolo = dbrequest(f"SELECT Model,Owner,Assicurazione,Targa FROM vehicles WHERE ID={id_veh}", "fetchone")
            modello = modelli_auto(int(dativeicolo[0]))
            owner = dativeicolo[1]

            if int(dativeicolo[2]):
                assicurata = "Il veicolo è ASSICURATO"
            else:
                assicurata = "Il veicolo NON È ASSICURATO"

            targa = dativeicolo[3]

            intestazione = f"Il veicolo {modello} è stato sequestrato"
            contenuto1 = f"- Sequestrato da {poliziotto}"
            contenuto2 = f"- TARGA: ({targa})"
            contenuto3 = f"- PROPRIETARIO: ({owner})"
            contenuto4 = f"- {assicurata}"

            veicoli.append([intestazione,contenuto1,contenuto2,contenuto3,contenuto4,data_ora])

        return veicoli   
    except:
        return 0

#_____________________║CARTELLA CLINICA SYSTEM║­­____________________
def nuovo_rapporto_clinico(user,diagnosi,terapia,grado,medico):
    try:
        data_ora = time.ctime()
        dbrequest(f'INSERT INTO cartella_clinica (user,diagnosi,terapia,grado,medico,data_ora) VALUES ("{user}","{diagnosi}","{terapia}","{grado}","{medico}","{data_ora}")')
        save_log("ems",medico,f"Ha emesso un referto a {user}",diagnosi)
        return 1
    except:
        return 0
#--------------
def visualizza_cartella_clinica(user):
    try:
        rapporti = []
        if user=="":
            que=""
        else:
            que = f'WHERE user="{user}"'
        data = dbrequest(f'SELECT * FROM cartella_clinica {que} ORDER BY id DESC', "fetchall")
        for i in data:
            paziente = i[1]
            diagnosi = i[2]
            terapia = i[3]
            grado = i[4].upper()
            medico = i[5]
            data_ora = i[6]

            if grado == "VERDE":
                classe = 'alert-success'
            elif grado == "ARANCIO":
                classe = 'alert-warning'
            elif grado == "ROSSO":
                classe = 'alert-danger'
            else:
                classe = 'alert-success'
            
            riga0 = f'PAZIENTE: {paziente}'
            riga1 = f'DIAGNOSI: {diagnosi}'
            riga2 = f'TERAPIA: {terapia}'
            riga3 = f'MEDICO: {medico}'
            rapporti.append([classe,riga0,riga1,riga2,riga3,data_ora])
        
        return rapporti
    except:
        return 0

def load_stats(username):
#Return Array --> [SKIN, AGE, PHONENUMBER, PHONECREDIT, MONEY, BANKMONEY]
    try:
        data = dbrequest(f'SELECT Skin,Age,PhoneNumber,TrafficoCell,Money,Bank FROM personaggi WHERE nome="{username}"', "fetchone")
        return data
    except:
        return 0

def load_veh(username):
#Return Array --> [id_model,model,fuel,insurance,value]  
    try:
        veh = []
        data = dbrequest(f'SELECT Model,Benzina,Assicurazione,Valore FROM vehicles WHERE Owner="{username}"', "fetchall")
        for i in data:
            id_model = i[0]
            model = modelli_auto(i[0])
            fuel = i[1]
            insurance = ""
            if i[2]!=1:
                insurance = "VEICOLO NON ASSICURATO"
            value = i[3]/100*40

            veh.append([id_model,model,fuel,insurance,value])
        return veh
    except:
        return 0
# _______________VERIFICA VALIDITA' ACCOUNT______________
def verifica_account():
    return True

    #SISTEMA CHIAVE
    #host_central = config.get("CENTRAL-SERVER", 'host')
    #port_central = config.get("CENTRAL-SERVER", 'port')
    #dbname_central = 'central_db_sampweb'
    #dbuser_central = 'kekko.py'
    #dbpass_central = ''
    # HXc9g3TjjOd$vy*2#NTABpgtrRt*hzObvUuW*AlnIfrLs^!OxdHXc9g3TjjOd$vy*2#NTABpgtrRt*hzObvUuW*AlnIfrLs^!Oxd
    #dbpass_centra = hashlib.md5(dbpass_central.encode()).hexdigest()
    #print(dbpass_centra)
    '''    
    try:
        dbcentral = pymysql.connect(host_central,dbuser_central,dbpass_central,dbname_central,int(port_central),autocommit=True)
        with dbcentral.cursor() as cursor_central:
            cursor_central.execute(f'SELECT validate,banned,expired_days FROM account WHERE secret_key="{__key__}"')
            data = cursor_central.fetchone()
            if data[0] == 1:
                if data[1] == 1:
                    print(Fore.YELLOW +"Il tuo Account è valido, ma non potrai rinnovarlo alla scadenza poichè sei stato bannato!")
                    return True
                else:
                    print(Fore.GREEN +"Account Validato correttamente, Avvio in corso!")
                    return True

            elif data[1] == 1:
                print(Fore.RED +"Sei Stato bannato, il tuo account è scaduto, ma non potrai rinnovarlo!")
                return False
            else:
                print(Fore.YELLOW +"Account Scaduto rinnovalo su https://sampwebsuite.kekko-py.it")
                return False
    except:
        print(Fore.RED +"Connessione Rifiutata, Account non validato o impossibile connettersi al server centrale.")
        return False
    '''
# ______________AVVIO WEB APP______________________
def start_web_app():
    if verifica_account() and __cursor__ != False:
        global __state__
        if __state__ == 0:
            print(Fore.YELLOW +"Avvio Web-App in modalità MANUTENZIONE SITO WEB")
    elif __cursor__ == False:
        print(Fore.RED +"Database Cliente non trovato!, Controlla config.cfg")
        print(Fore.YELLOW +"Avvio Web-App in modalità MANUTENZIONE SITO WEB")
        __state__ = 0
    else:
        print(Fore.YELLOW +"Avvio Web-App in modalità MANUTENZIONE SITO WEB")
        __state__ = 0

    print(credts_spam())
    global debug_server
    if debug_server==1:
        debug_server=True
    else:
        debug_server=False
    __app__.run(debug=debug_server, host='0.0.0.0', port=porta_server)

# ___________________RENDER PAGES____________________
#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#________________________________║GESTORE PAGINA HOME║­­____________________________
@__app__.route('/',  methods=['GET','POST'])
def home(error=" "):
    if __state__ == 1:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            if request.method == 'GET':
                return login_get(error)
        else:
            if sez_reg:
                return reg()
            elif sez_vip:
                return vip()
            elif sez_news: 
                return news()
            elif sez_maze:
                return banca_get()
            elif sez_digit:
                return digit_coin_get()
            elif sez_fazione:
                return fazione()
            elif sez_personaggio:
                return personaggio()
            elif sez_ringraziamenti:
                return ringraziamenti()
            elif sez_concessionaria:
                return 0 
            else:
                return page_not_found(404)
    else:
        return render_template("state0.html")

#----------------------------------------------
#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#________________________________║GESTORE PAGINA ER404║­­____________________________
@__app__.errorhandler(404)
def page_not_found(e):
    page = render_template("404.html")
    global template
    global credit
    try:
        pagina = template % (credit, page)
        return pagina
    except:
        print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
        return quit()
    
#----------------------------------------------
#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#________________________________║GESTORE PAGINA LOGIN║­­____________________________
@__app__.route('/login', methods=['GET'])
def login_get(error=" "):
    if __state__ == 1:
        if not session.get('logged_in'):
            login = render_template("login.html")
            login = login % (error)
            global template
            template = render_template("template_panel.html", sez_reg=sez_reg, sez_vip=sez_vip, sez_news=sez_news, sez_maze=sez_maze, sez_digit=sez_digit, sez_fazione=sez_fazione, sez_concessionaria=sez_concessionaria, sez_personaggio=sez_personaggio, sez_ringraziamenti=sez_ringraziamenti)
            return login
        else:
            if sez_reg:
                return reg()
            elif sez_vip:
                return vip()
            elif sez_news: 
                return news()
            elif sez_maze:
                return banca_get()
            elif sez_digit:
                return digit_coin_get()
            elif sez_fazione:
                return fazione()
            elif sez_personaggio:
                return personaggio()
            elif sez_ringraziamenti:
                return ringraziamenti()
            elif sez_concessionaria:
                return 0 
            else:
                return page_not_found(404)
    else:
        return render_template("state0.html")

@__app__.route('/login', methods=['POST'])
def login():
    #session['logged_in'] = True
    #session['username'] = "Ciro_Esposito"
    #return home()

    username_login = request.form['username']
    password_login = request.form['password']

    if not (controllo_input(username_login) and controllo_input(password_login)):
        return login_get('Hai inserito un carattere Non consentito')

    session['account'] = username_login
    #session['username'] = username_login

    data = dbrequest(query4+f'"{username_login}"', "fetchone")
    try:

        #password_login = hashlib.md5(password_login.encode()).hexdigest()
        if password_login == data[1]:
            #session['logged_in'] = True
            return redirect(url_for('scelta_pg'))
        else:
            session['logged_in'] = False
            error = "Password Errata!"
            return login_get(error)
    except:
        error = "Account Inesistente"
        return login_get(error)
#----------------------------------------------
#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#________________________________║GESTORE SCELTA PG­­____________________________
@__app__.route('/scelta-pg', methods=['GET','POST'])
def scelta_pg():
    if __state__ == 1:
        if request.method == 'GET':

            data = dbrequest(f'SELECT PG1,PG2,PG3 FROM accounts WHERE nome="{session["account"]}"', "fetchone")
            try:
                session['pg'] = ["","",""]
                session['pg'][0] = data[0]
                session['pg'][1] = data[1]
                session['pg'][2] = data[2]
            except:
                return login_get("Devi prima eseguire l'autenticazione!")

            return render_template("scelta_pg.html",pg=session['pg'])
        else:
            pg = request.form['pg']

            if (pg==session['pg'][0] or pg==session['pg'][1] or pg==session['pg'][2]) and pg!="(nuovo personaggio)":
                session['username'] = pg
                session['logged_in'] = True
                return controllo_iban()
            else: 
                return login_get("EH VOLEVIIII")
    else:
        return render_template("state0.html")

#----------------------------------------------

@__app__.route('/regolamenti', methods=['GET','POST'])
def reg():
    if sez_reg:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            reg_page = render_template("sez_reg.html")
            global template
            global credit
            try:
                return template % (credit, reg_page)
            except :
                print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                return quit()

    else:
        return page_not_found(404)
#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#________________________________║GESTORE ACQUISTO VIP║­­____________________________
@__app__.route('/vip', methods=['GET','POST'])
def vip():
    if sez_vip:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            paypal = config.get("ACCOUNT", 'email_paypal')
            bronze = config.get("VIP", 'bronze')
            silver = config.get("VIP", 'silver')
            gold = config.get("VIP", 'gold')
            platinum = config.get("VIP", 'platinum')
            diamond = config.get("VIP", 'diamond')
            master = config.get("VIP", 'master')

            pnt_bronze = config.get("VIP", 'pnt_bronze')
            pnt_silver = config.get("VIP", 'pnt_silver')
            pnt_gold = config.get("VIP", 'pnt_gold')
            pnt_platinum = config.get("VIP", 'pnt_platinum')
            pnt_diamond = config.get("VIP", 'pnt_diamond')
            pnt_master = config.get("VIP", 'pnt_master')

            vip_page = render_template("vip.html", paypal=paypal, bronze=bronze, silver=silver, gold=gold, platinum=platinum, diamond=diamond, master=master, pnt_bronze=pnt_bronze, pnt_silver=pnt_silver, pnt_gold=pnt_gold, pnt_platinum=pnt_platinum, pnt_diamond=pnt_diamond, pnt_master=pnt_master)
            
            global template
            global credit
            try:
                return template % (credit, vip_page)
            except :
                print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                return quit()

    else:
        return page_not_found(404)
        
#----------------------------------------------
#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#________________________________║GESTORE SEZIONE NEWS║­­____________________________

@__app__.route('/news', methods=['GET','POST'])
def news():
    if sez_news:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            notizie=[]
            data = dbrequest('SELECT * FROM news ORDER BY id DESC', "fetchall")
            for row in data:
                fazid = row[1]
                autore = row[2]
                text_news = row[3]
                data_ora = row[4]
                fazione = row[5]
                immagine = row[6]
                prezzo = row[7]
                numero = row[8]

                if int(fazid) == int(id_pula):
                    fazione="SF Police Department"
                    classe="alert-primary"
                elif int(fazid) == int(id_ems):
                    fazione="Medical Department"
                    classe="alert-success"
                elif int(fazid) == int(id_sfnn):
                    fazione="San Fierro News Network"
                    classe="alert-warning"
                
                notizie.append([classe,fazione,autore,text_news,data_ora])

            news_page = render_template("news.html", notizie=notizie, len_notizie=len(notizie))
            global template
            global credit
            try:
                return template % (credit, news_page)
            except:
                    print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                    return quit()
    else:
        return page_not_found(404)
#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#________________________________║GESTORE BANCA, DIGITCOIN║­­____________________________
#*-*-*-*-*-*-*-*-*-*-*** POST ***-*-*-*-*-*-*-*-*-*
@__app__.route('/bank', methods=['POST'])
def banca_post():
    if sez_maze:
        try:
            in_banca_iban = request.form['in_banca_iban']
            in_banca_importo = int(request.form['in_banca_importo'])
            in_banca_oggetto = request.form['in_banca_oggetto']

            if not (controllo_input(str(in_banca_iban)) and controllo_input(str(in_banca_importo)) and controllo_input(in_banca_oggetto)):
                return banca_get('Hai inserito un carattere Non consentito')
            
            try:
                destinatario_data = dbrequest(query6+f'"{in_banca_iban}"', "fetchone")
                nome_destinatario = destinatario_data[0]
                saldo_banca_destinatario = destinatario_data[1]

                data = dbrequest(query7+f'"{session["username"]}"', "fetchone")
                iban = data[0]
                saldo_banca_mittente = data[1]

                if str(in_banca_iban) == str(iban): 
                    return banca_get('Non Puoi Inviare soldi a te stesso')

                if int(saldo_banca_mittente) >= int(in_banca_importo):
                    dbrequest(query8+f'{int(saldo_banca_mittente)-int(in_banca_importo)} WHERE iban="{iban}"')
                    dbrequest(query8+f'{int(saldo_banca_destinatario)+int(in_banca_importo)} WHERE iban="{in_banca_iban}"')
                    tempo_attuale = time.ctime()
                    dbrequest(f'INSERT INTO transazioni (mittente, destinatario, importo, oggetto, data_ora) VALUES ("{session["username"]}", "{nome_destinatario}", "{in_banca_importo}", "{in_banca_oggetto}", "{tempo_attuale}")')
                    return banca_get()
                else:
                    return banca_get()
            
            except:
                error="Iban Non Associato"
                return banca_get(error)

        except:
            error="Non Lasciare Campi Vuoti"
            return banca_get(error)
        
    else:
        return page_not_found(404)
#---------------------------------------------------
@__app__.route('/digit', methods=['POST'])
def digit_coin_post():
    if sez_digit:
        try:
            in_digit_iban = request.form['in_banca_iban']
            in_digit_importo = int(request.form['in_banca_importo'])
            in_digit_oggetto = request.form['in_banca_oggetto']
            if not (controllo_input(in_digit_iban) and controllo_input(str(in_digit_importo)) and controllo_input(in_digit_oggetto)):
                return digit_coin_get('Hai inserito un carattere Non consentito')

        except:
            error="Non Lasciare Campi Vuoti"
            return digit_coin_get(error)
        try:
            destinatario_data = dbrequest(query11+f'"{in_digit_iban}"', "fetchone")
            nome_destinatario = destinatario_data[0]
            saldo_digit_destinatario = destinatario_data[1]
            
        except:
            error="Iban Non Associato"
            return banca_get(error)
        
        data = dbrequest(query12+f'"{session["username"]}"', "fetchone")
        iban = data[0]
        saldo_digit_mittente = data[1]

        if str(in_digit_iban) == str(iban): 
            return digit_coin_get('Non Puoi Inviare soldi a te stesso')

        if int(saldo_digit_mittente) >= int(in_digit_importo):
            dbrequest(query13+f'{int(saldo_digit_mittente)-int(in_digit_importo)} WHERE iban="{iban}"')
            dbrequest(query13+f'{int(saldo_digit_destinatario)+int(in_digit_importo)} WHERE iban="{in_digit_iban}"')
            tempo_attuale = time.ctime()
            dbrequest(f'INSERT INTO transazioni_digit (mittente, destinatario, importo, oggetto, data_ora) VALUES ("{session["username"]}", "{nome_destinatario}", "{saldo_digit_destinatario}", "{in_digit_oggetto}", "{tempo_attuale}")')
            return digit_coin_get()
        else:
            return digit_coin_get()

    else:
        return page_not_found(404)

#*-*-*-*-*-*-*-*-*-*-*** GET ***-*-*-*-*-*-*-*-*-*

@__app__.route('/bank', methods=['GET','POST'])
def banca_get(error=""):
    if sez_maze:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            data = dbrequest(query19+f'"{session["username"]}"', "fetchone")
            iban = data[0]
            saldo_banca = str(data[1])

            transazioni = transazione_bank_user(session['username'], "transazioni")
            if transazioni == 0:
                error = "Impossibile Caricare le Transazioni!"
                transazioni = []
                         
            banca_page = render_template("new_maze.html",s1=iban, s2=saldo_banca+'$', s3=error, transazioni=transazioni, len_transazioni=len(transazioni))
            global template
            
            try:
                global credit
                pagina = template % (credit, banca_page)
                return pagina
            except :
                print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                
                return quit()
    else:
        return page_not_found(404)
#--------------------------------------
@__app__.route('/digit', methods=['GET','POST'])
def digit_coin_get(error=""):
    if sez_digit:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            data = dbrequest(query19+f'"{session["username"]}"', "fetchone")
            iban = data[0]
            saldo_digit = str(data[2])

            transazioni = transazione_bank_user(session['username'], "transazioni_digit")
            if transazioni == 0:
                error = "Impossibile Caricare le Transazioni!"
                transazioni = []
                     
            digit_page = render_template("digitcoin.html",s1=iban, s2=saldo_digit+'$', s3=error, transazioni=transazioni, len_transazioni=len(transazioni))
            global template
            global credit
            try:
                pagina = template % (credit, digit_page)
                return pagina
            except :
                print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                
                return quit()
    else:
        return page_not_found(404) 

@__app__.route('/ringraziamenti', methods=['GET','POST'])
def ringraziamenti():
    if sez_ringraziamenti:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            reg_page = render_template("sez_ringraziamenti.html")
            global template
            global credit
            try:
                return template % (credit, reg_page)
            except :
                print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                return quit()

    else:
        return page_not_found(404)
#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#________________________________║SEZIONI POLIZIA║­­____________________________

@__app__.route('/reg-reato', methods=['GET','POST'])
def page_reg_reato(m='null',error=""):
    try:
        data = dbrequest(f'SELECT Rank FROM personaggi WHERE nome="{session["username"]}"', "fetchone")
        rank=int(data[0])
    except:
        return home()
    if sez_fazione and registra_reato and rank <= rank_registra_reato:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            data = dbrequest(query21+f'"{session["username"]}"', "fetchone")
            if int(data[0]) == int(id_pula):
                if request.method == 'GET' or m=='get':
                    page = render_template("pd/reg_reato.html", error=error)

                    global template
                    global credit
                    try:
                        pagina = template % (credit, page)
                        return pagina
                    except:
                        print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                        return quit()
                else:
                    try:
                        sospetto = request.form['sospetto']
                        reato = request.form['reato']
                        multa = int(request.form['multa'])

                        if request.form.get('prigione'):
                            prigione=1
                        else:
                            prigione=0

                        if controllo_input(sospetto) and controllo_input(reato):
                            error=""
                            if not nuovo_reato(sospetto, reato, multa, prigione, session['username']):
                                error="Errore Registrazione"
                            else:
                                error="Registrazione Avvenuta con successo"

                        else:
                            error="Hai inserito dei Caratteri non consentiti"    
                    except:
                        error = "Compila tutti i Campi!"
                    return page_reg_reato("get",error)
            else:
                 return page_not_found(404)
    else:
        return page_not_found(404)     

#-----------------------------------------------------------------------------

@__app__.route('/fedina-pd', methods=['GET','POST'])
def page_fedina(m='null',error="",utente_cercato=""):
    try:
        data = dbrequest(f'SELECT Rank FROM personaggi WHERE nome="{session["username"]}"', "fetchone")
        rank=int(data[0])
    except:
        return home()
    if sez_fazione and visualizza_fedpen  and rank <= rank_visualizza_fedpen:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            data = dbrequest(query21+f'"{session["username"]}"', "fetchone")
            if int(data[0]) == int(id_pula):
                if request.method == 'GET' or m=='get':

                    reati = visualizza_fedina(utente_cercato)
                    len_reati = 0
                    if reati == 0:
                        error = "Errore Lettura fedina"
                        reati=[]
                    else:
                        len_reati = len(reati)
                        if len_reati == 0:
                            error = "Fedina Penale pulita"
                            reati = []
                        
                    page = render_template("pd/visualizza_fedina.html",error=error, reati=reati, len_reati=len_reati)

                    global template
                    global credit
                    try:
                        pagina = template % (credit, page)
                        return pagina
                    except:
                        print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                        return quit()
                else:
                    try:
                        user = request.form['user']
                        if controllo_input(user):
                            error=""
                        else:
                            user=""
                            error="Hai usato caratteri non consentiti"
                    except:
                        error="Compila il campo"
                    return page_fedina('get',error,user)
            else:
                return page_not_found(404)
    else:
        return page_not_found(404)       

#-----------------------------------------------------------------------------

@__app__.route('/transazioni-pd', methods=['GET','POST'])
def page_trans(m='null',error="",utente_cercato=" "):
    try:
        data = dbrequest(f'SELECT Rank FROM personaggi WHERE nome="{session["username"]}"', "fetchone")
        rank=int(data[0])
    except:
        return home()
    if sez_fazione and visualizza_trans and rank <= rank_visualizza_trans:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            data = dbrequest(query21+f'"{session["username"]}"',"fetchone")
            if int(data[0]) == int(id_pula):
                if request.method == 'GET' or m=='get':

                    trans = transazioni_citta(utente_cercato)
                    len_trans = 0
                    if trans == 0:
                        error = "Errore Lettura transazioni"
                        trans = []
                    else:
                        len_trans = len(trans)
                        if len_trans == 0:
                            error = "Nessuna Transazione"
                            trans = []
                        
                    page = render_template("pd/visualizza_transazioni.html",error=error, transazioni=trans, len_trans=len_trans)

                    global template
                    global credit
                    try:
                        pagina = template % (credit, page)
                        return pagina
                    except:
                        print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                        return quit()
                else:
                    try:
                        user = request.form['user']
                        if controllo_input(user):
                            error=""
                            if user=="":
                                user=" "
                        else:
                            user=" "
                            error="Hai usato caratteri non consentiti"
                    except:
                        error="Compila il campo"
                    return page_trans('get',error,user)
            else:
                return page_not_found(404)
    else:
        return page_not_found(404)   
    

@__app__.route('/send-sms-pd', methods=['GET','POST'])
def page_send_sms_pd(m='null',error=""):
    try:
        data = dbrequest(f'SELECT Rank FROM personaggi WHERE nome="{session["username"]}"', "fetchone")
        rank=int(data[0])
    except:
        return home()
    if sez_fazione and mess_priv_pol and rank <= rank_mess_priv_pol:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            data = dbrequest(query21+f'"{session["username"]}"', "fetchone")
            if int(data[0]) == int(id_pula):
                if request.method == 'GET' or m=='get':
                    page = render_template("pd/send_sms.html", error=error)

                    global template
                    global credit
                    try:
                        pagina = template % (credit, page)
                        return pagina
                    except:
                        print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                        return quit()
                else:
                    try:
                        user = request.form['user']
                        messaggio = request.form['messaggio']

                        if controllo_input(user) and controllo_input(messaggio):
                            error=""
                            if not sms_send(911,user,messaggio):
                                error="Errore Invio Messaggio"
                            else:
                                save_log("pd",session["username"],f"Ha inviato un messaggio a {user}",messaggio)
                                error="Messaggio spedito con successo"

                        else:
                            error="Hai inserito dei Caratteri non consentiti"    
                    except:
                        error = "Compila tutti i Campi!"
                    return page_send_sms_pd("get",error)
            else:
                 return page_not_found(404)
    else:
        return page_not_found(404)     
                                                                                                            
@__app__.route('/agg-avviso-pd', methods=['GET','POST'])
def page_avviso_pd(m='null',error=""):
    try:
        data = dbrequest(f'SELECT Rank FROM personaggi WHERE nome="{session["username"]}"', "fetchone")
        rank=int(data[0])
    except:
        return home()
    if sez_fazione and avviso_comunale_pol and rank <= rank_avviso_comunale_pol:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            data = dbrequest(query21+f'"{session["username"]}"', "fetchone")
            if int(data[0]) == int(id_pula):
                if request.method == 'GET' or m=='get':
                    page = render_template("pd/agg_avviso.html", error=error)

                    global template
                    global credit
                    try:
                        pagina = template % (credit, page)
                        return pagina
                    except:
                        print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                        return quit()
                else:
                    try:
                        messaggio = request.form['messaggio']

                        if controllo_input(messaggio):
                            error=""
                            if not nuova_news_text(id_pula,session["username"],messaggio, "Police Department"):
                                error="Errore Invio Messaggio"
                            else:
                                save_log("pd",session["username"],f"Ha aggiunto una news",messaggio)
                                error="Messaggio spedito con successo"

                        else:
                            error="Hai inserito dei Caratteri non consentiti"    
                    except:
                        error = "Compila tutti i Campi!"
                    return page_avviso_pd("get",error)
            else:
                 return page_not_found(404)
    else:
        return page_not_found(404)     



@__app__.route('/ver-arruolamento', methods=['GET','POST'])
def page_ver_arruolamento(m='null',error="",utente_cercato=""):
    try:
        data = dbrequest(f'SELECT Rank FROM personaggi WHERE nome="{session["username"]}"', "fetchone")
        rank=int(data[0])
    except:
        return home()
    if sez_fazione and verifica_arruolamento and rank <= rank_verifica_arruolamento:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            data = dbrequest(query21+f'"{session["username"]}"', "fetchone")
            if int(data[0]) == int(id_pula):
                if request.method == 'GET' or m=='get':
                    
                    classe="alert-primary"
                    msg="Cerca un cittadino per verificare la validità"
                    risultato = validata_arruolamento(utente_cercato)
                    if risultato == 0:
                        error = "Errore Lettura Validità"
                    else:
                        if risultato == "no":
                            error = ""
                            classe="alert-danger"
                            msg="L'utente cercato, non è idoneo per l'arruolamento, per maggiori informazioni controlla nella sezione fedine penali"
                        else:
                            error = ""
                            classe="alert-success"
                            msg="L'utente cercato, è idoneo per il servizio reclute e cadetti!"
  

                    page = render_template("pd/ver_arruolamento.html",error=error, classe=classe, msg=msg)

                    global template
                    global credit
                    try:
                        pagina = template % (credit, page)
                        return pagina
                    except:
                        print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                        return quit()
                else:
                    try:
                        user = request.form['user']
                        if controllo_input(user):
                            error=""
                        else:
                            user=""
                            error="Hai usato caratteri non consentiti"
                    except:
                        error="Compila il campo"
                    return page_ver_arruolamento('get',error,user)
            else:
                return page_not_found(404)
    else:
        return page_not_found(404)       


@__app__.route('/pulisci-fedina', methods=['GET','POST'])
def page_pulisci_fedina(m='null',error=""):
    try:
        data = dbrequest(f'SELECT Rank FROM personaggi WHERE nome="{session["username"]}"', "fetchone")
        rank=int(data[0])
    except:
        return home()
    if sez_fazione and pulizia_fedina and rank <= rank_pulizia_fedina:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            data = dbrequest(query21+f'"{session["username"]}"', "fetchone")
            if int(data[0]) == int(id_pula):
                if request.method == 'GET' or m=='get':
                    page = render_template("pd/pulisci_fedina.html", error=error)

                    global template
                    global credit
                    try:
                        pagina = template % (credit, page)
                        return pagina
                    except:
                        print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                        return quit()
                else:
                    try:
                        user = request.form['user']
                        motivo = request.form['motivo']

                        if controllo_input(user) and controllo_input(motivo):
                            error=""
                            if not pulisci_fedina(session['username'],user,motivo):
                                error="Errore Invio Messaggio"
                            else:
                                error="Fedina Pulita con successo"

                        else:
                            error="Hai inserito dei Caratteri non consentiti"    
                    except:
                        error = "Compila tutti i Campi!"
                    return page_pulisci_fedina("get",error)
            else:
                 return page_not_found(404)
    else:
        return page_not_found(404)     

@__app__.route('/veh-seq', methods=['GET','POST'])
def veh_seq(m='null',error=""):
    try:
        data = dbrequest(f'SELECT Rank FROM personaggi WHERE nome="{session["username"]}"', "fetchone")
        rank=int(data[0])
    except:
        return home()
    if sez_fazione and veicoli_seq and rank <= rank_veicoli_seq:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            data = dbrequest(query21+f'"{session["username"]}"', "fetchone")
            if int(data[0]) == int(id_pula):
                if request.method == 'GET' or m=='get':

                    veicoli = visualizza_sequestri()
                    if veicoli == 0:
                        error = "Errore Lettura veicoli"
                        veicoli=[]
                    elif len(veicoli) == 0:
                        error = "Nessun Veicolo Sequestrato"
                    else:
                        error=""

                    page = render_template("pd/veh_seq.html", error=error, veicoli=veicoli, len_veicoli=len(veicoli))

                    global template
                    global credit
                    try:
                        pagina = template % (credit, page)
                        return pagina
                    except:
                        print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                        return quit()
            else:
                 return page_not_found(404)
    else:
        return page_not_found(404)

#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#________________________________║SEZIONI MEDICI║­­____________________________

@__app__.route('/agg-referto', methods=['GET','POST'])
def page_agg_referto(m='null',error=""):
    try:
        data = dbrequest(f'SELECT Rank FROM personaggi WHERE nome="{session["username"]}"', "fetchone")
        rank=int(data[0])
    except:
        return home()
    if sez_fazione and agg_referto and rank <= rank_agg_referto:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            data = dbrequest(query21+f'"{session["username"]}"', "fetchone")
            if int(data[0]) == int(id_ems):
                if request.method == 'GET' or m=='get':
                    page = render_template("ems/aggiungi-referto.html", error=error)

                    global template
                    global credit
                    try:
                        pagina = template % (credit, page)
                        return pagina
                    except:
                        print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                        return quit()
                else:
                    try:
                        paziente = request.form['paziente']
                        diagnosi = request.form['diagnosi']
                        terapia = request.form['terapia']
                        grado = request.form['grado']

                        if controllo_input(paziente) and controllo_input(diagnosi) and controllo_input(terapia) and controllo_input(grado):
                            error=""
                            if not nuovo_rapporto_clinico(paziente,diagnosi,terapia,grado,session['username']):
                                error="Errore Registrazione"
                            else:
                                error="Registrazione Avvenuta con successo"

                        else:
                            error="Hai inserito dei Caratteri non consentiti"    
                    except:
                        error = "Compila tutti i Campi!"
                    return page_agg_referto("get",error)
            else:
                 return page_not_found(404)
    else:
        return page_not_found(404)     

@__app__.route('/cartella-clinica-ems', methods=['GET','POST'])
def page_cartella_clinica(m='null',error="",utente_cercato=""):
    try:
        data = dbrequest(f'SELECT Rank FROM personaggi WHERE nome="{session["username"]}"', "fetchone")
        rank=int(data[0])
    except:
        return home()
    if sez_fazione and visualizza_cartella and rank <= rank_visualizza_cartella:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            data = dbrequest(query21+f'"{session["username"]}"', "fetchone")
            if int(data[0]) == int(id_ems):
                if request.method == 'GET' or m=='get':

                    cartella = visualizza_cartella_clinica(utente_cercato)
                    len_cartella = 0
                    if cartella == 0:
                        error = "Errore Lettura Cartella Clinica"
                        cartella=[]
                    else:
                        len_cartella = len(cartella)
                        if len_cartella == 0:
                            error = "Cartella Clinica Vuota"
                            cartella = []
                        
                    page = render_template("ems/visualizza-cartella.html",error=error, cartella=cartella, len_cartella=len_cartella)

                    global template
                    global credit
                    try:
                        pagina = template % (credit, page)
                        return pagina
                    except:
                        print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                        return quit()
                else:
                    try:
                        user = request.form['user']
                        if controllo_input(user):
                            error=""
                        else:
                            user=""
                            error="Hai usato caratteri non consentiti"
                    except:
                        error="Compila il campo"
                    return page_cartella_clinica('get',error,user)
            else:
                return page_not_found(404)
    else:
        return page_not_found(404)   

@__app__.route('/agg-avviso-ems', methods=['GET','POST'])
def page_avviso_ems(m='null',error=""):
    try:
        data = dbrequest(f'SELECT Rank FROM personaggi WHERE nome="{session["username"]}"', "fetchone")
        rank=int(data[0])
    except:
        return home()
    if sez_fazione and avviso_comunale_med and rank <= rank_avviso_comunale_med:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            data = dbrequest(query21+f'"{session["username"]}"', "fetchone")
            if int(data[0]) == int(id_ems):
                if request.method == 'GET' or m=='get':
                    page = render_template("ems/agg_avviso.html", error=error)

                    global template
                    global credit
                    try:
                        pagina = template % (credit, page)
                        return pagina
                    except:
                        print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                        return quit()
                else:
                    try:
                        messaggio = request.form['messaggio']

                        if controllo_input(messaggio):
                            error=""
                            if not nuova_news_text(id_ems,session["username"],messaggio, "EMS Departement"):
                                error="Errore Invio Messaggio"
                            else:
                                save_log("ems",session["username"],f"Ha aggiunto una news",messaggio)
                                error="Messaggio spedito con successo"

                        else:
                            error="Hai inserito dei Caratteri non consentiti"    
                    except:
                        error = "Compila tutti i Campi!"
                    return page_avviso_ems("get",error)
            else:
                 return page_not_found(404)
    else:
        return page_not_found(404)     

@__app__.route('/send-sms-ems', methods=['GET','POST'])
def page_send_sms_ems(m='null',error=""):
    try:
        data = dbrequest(f'SELECT Rank FROM personaggi WHERE nome="{session["username"]}"', "fetchone")
        rank=int(data[0])
    except:
        return home()
    if sez_fazione and mess_priv_med and rank <= rank_mess_priv_med:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            data = dbrequest(query21+f'"{session["username"]}"', "fetchone")
            if int(data[0]) == int(id_ems):
                if request.method == 'GET' or m=='get':
                    page = render_template("ems/send_sms.html", error=error)

                    global template
                    global credit
                    try:
                        pagina = template % (credit, page)
                        return pagina
                    except:
                        print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                        return quit()
                else:
                    try:
                        user = request.form['user']
                        messaggio = request.form['messaggio']

                        if controllo_input(user) and controllo_input(messaggio):
                            error=""
                            if not sms_send(118,user,messaggio):
                                error="Errore Invio Messaggio"
                            else:
                                save_log("ems",session["username"],f"Ha inviato un messaggio a {user}",messaggio)
                                error="Messaggio spedito con successo"

                        else:
                            error="Hai inserito dei Caratteri non consentiti"    
                    except:
                        error = "Compila tutti i Campi!"
                    return page_send_sms_ems("get",error)
            else:
                 return page_not_found(404)
    else:
        return page_not_found(404)     

#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#________________________________║SEZIONI SFNN║­­____________________________

@__app__.route('/send-sms-sfnn', methods=['GET','POST'])
def page_send_sms_sfnn(m='null',error=""):
    try:
        data = dbrequest(f'SELECT Rank FROM personaggi WHERE nome="{session["username"]}"', "fetchone")
        rank=int(data[0])
    except:
        return home()
    if sez_fazione and mess_priv_sfnn and rank <= rank_mess_priv_sfnn:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            data = dbrequest(query21+f'"{session["username"]}"', "fetchone")
            if int(data[0]) == int(id_sfnn):
                if request.method == 'GET' or m=='get':
                    page = render_template("sfnn/send_sms.html", error=error)

                    global template
                    global credit
                    try:
                        pagina = template % (credit, page)
                        return pagina
                    except:
                        print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                        return quit()
                else:
                    try:
                        user = request.form['user']
                        messaggio = request.form['messaggio']

                        if controllo_input(user) and controllo_input(messaggio):
                            error=""
                            if not sms_send(333,user,messaggio):
                                error="Errore Invio Messaggio"
                            else:
                                save_log("sfnn",session["username"],f"Ha inviato un messaggio a {user}",messaggio)
                                error="Messaggio spedito con successo"

                        else:
                            error="Hai inserito dei Caratteri non consentiti"    
                    except:
                        error = "Compila tutti i Campi!"
                    return page_send_sms_sfnn("get",error)
            else:
                 return page_not_found(404)
    else:
        return page_not_found(404)     
                                                                                                            
@__app__.route('/agg-avviso-sfnn', methods=['GET','POST'])
def page_avviso_sfnn(m='null',error=""):
    try:
        data = dbrequest(f'SELECT Rank FROM personaggi WHERE nome="{session["username"]}"', "fetchone")
        rank=int(data[0])
    except:
        return home()
    if sez_fazione and avviso_comunale_sfnn and rank <= rank_avviso_comunale_sfnn:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            data = dbrequest(query21+f'"{session["username"]}"', "fetchone")
            if int(data[0]) == int(id_sfnn):
                if request.method == 'GET' or m=='get':
                    page = render_template("sfnn/agg_avviso.html", error=error)

                    global template
                    global credit
                    try:
                        pagina = template % (credit, page)
                        return pagina
                    except:
                        print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                        return quit()
                else:
                    try:
                        messaggio = request.form['messaggio']

                        if controllo_input(messaggio):
                            error=""
                            if not nuova_news_text(id_sfnn,session["username"],messaggio, "San Fierro News Network"):
                                error="Errore Invio Messaggio"
                            else:
                                save_log("sfnn",session["username"],f"Ha aggiunto una news",messaggio)
                                error="Messaggio spedito con successo"

                        else:
                            error="Hai inserito dei Caratteri non consentiti"    
                    except:
                        error = "Compila tutti i Campi!"
                    return page_avviso_sfnn("get",error)
            else:
                 return page_not_found(404)
    else:
        return page_not_found(404)     
'''
UPLOAD_FOLDER = '/articoli'
ALLOWED_EXTENSIONS = {'pdf'}
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@__app__.route('/articolo-sfnn', methods=['GET','POST'])
def page_articolo_sfnn(m='null',error=""):
    try:
        data = dbrequest(f'SELECT Rank FROM personaggi WHERE nome="{session["username"]}"', "fetchone")
        rank=int(data[0])
    except:
        return home()
    if sez_fazione and crea_articolo and rank <= rank_crea_articolo:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            data = dbrequest(query21+f'"{session["username"]}"', "fetchone")
            if int(data[0]) == int(id_sfnn):
                if request.method == 'GET' or m=='get':
                    page = render_template("sfnn/crea_articolo.html", error=error)

                    global template
                    global credit
                    try:
                        pagina = template % (credit, page)
                        return pagina
                    except:
                        print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                        return quit()
                else:
                    try:
                        __app__.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

                        titolo = request.form['titolo']
                        if 'file' not in request.files:
                            return page_articolo_sfnn("get", "Nessun File Selezionato")
                        
                        file = request.files['file']
                       
                        if file.filename == '':
                            return page_articolo_sfnn("get", "Nessun File Selezionato")

                        if controllo_input(titolo):
                            error=""
                            if not nuova_news_text(id_sfnn,session["username"],titolo, "San Fierro News Network"):
                                error="Errore Invio Messaggio"
                            else:
                                save_log("sfnn",session["username"],f"Ha aggiunto una news",titolo)
                                error="Messaggio spedito con successo"
                        else:
                            error="Hai inserito dei Caratteri non consentiti"

                        if file and allowed_file(file.filename):
                             filename = secure_filename(file.filename)
                             file.save(os.path.join(__app__.config['UPLOAD_FOLDER'], filename))


                    except:
                        error = "Compila tutti i Campi!"
                    return page_avviso_sfnn("get",error)
            else:
                 return page_not_found(404)
    else:
        return page_not_found(404)     
'''
#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#________________________________║GESTORE PAGINE FAZIONE║­­____________________________
# PAGINA FAZIONE NULL GET
def fazione_null():
    page = render_template("faz_null.html")
    global template
    global credit
    try:
        return template % (credit, page)
    except :
        print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
        return quit()

# PAGINA FAZIONE POLIZIA GET
def fazione_polizia_get():
    global registra_reato,visualizza_fedpen,visualizza_trans,blocca_conto,verifica_arruolamento,avviso_comunale_pol,mess_priv_pol,pulizia_fedina,veicoli_seq

    data = dbrequest(f'SELECT Rank FROM personaggi WHERE nome="{session["username"]}"', "fetchone")
    rank=int(data[0])

    loc_registra_reato = int(funzionalita.get("POLIZIA",'registra_reato'))
    loc_visualizza_fedpen = int(funzionalita.get("POLIZIA",'visualizza_fedina'))
    loc_visualizza_trans = int(funzionalita.get("POLIZIA",'visualizza_trans'))
    loc_blocca_conto = int(funzionalita.get("POLIZIA",'blocca_conto'))
    loc_verifica_arruolamento =  int(funzionalita.get("POLIZIA",'verifica_arruolamento'))
    loc_avviso_comunale_pol =  int(funzionalita.get("POLIZIA",'avviso_comunale'))
    loc_mess_priv_pol = int(funzionalita.get("POLIZIA",'mess_priv'))
    loc_pulizia_fedina = int(funzionalita.get("POLIZIA",'pulizia_fedina'))
    loc_veicoli_seq = int(funzionalita.get("POLIZIA",'veicoli_seq'))

    if loc_registra_reato:
        if not (rank <= rank_registra_reato):
            registra_reato=0
        else:
            registra_reato=1

    if loc_visualizza_fedpen:
        if not (rank <= rank_visualizza_fedpen): 
            visualizza_fedpen=0
        else:
            visualizza_fedpen=1

    if loc_visualizza_trans:
        if not (rank <= rank_visualizza_trans): 
            visualizza_trans=0
        else:
            visualizza_trans=1

    if loc_blocca_conto:       
        if not (rank <= rank_blocca_conto): 
            blocca_conto=0
        else:
            blocca_conto=1

    if loc_verifica_arruolamento:
        if not (rank <= rank_verifica_arruolamento): 
            verifica_arruolamento=0
        else:
            verifica_arruolamento=1

    if loc_avviso_comunale_pol: 
        if not (rank <= rank_avviso_comunale_pol): 
            avviso_comunale_pol=0
        else:
            avviso_comunale_pol=1

    if loc_mess_priv_pol:
        if not (rank <= rank_mess_priv_pol): 
            mess_priv_pol=0
        else:
            mess_priv_pol=1

    if loc_pulizia_fedina:
        if not (rank <= rank_pulizia_fedina): 
            pulizia_fedina=0
        else:
            pulizia_fedina=1

    if loc_veicoli_seq:
        if not (rank <= rank_veicoli_seq): 
            veicoli_seq=0
        else:
            veicoli_seq=1

    page = render_template("faz_pula.html", registra_reato=registra_reato, visualizza_fedina=visualizza_fedpen, visualizza_trans=visualizza_trans, blocca_conto=blocca_conto, verifica_arruolamento=verifica_arruolamento, avviso_comunale=avviso_comunale_pol, mess_priv=mess_priv_pol, pulizia_fedina=pulizia_fedina, veicoli_seq=veicoli_seq)
    global template
    global credit
    try:
        return template % (credit, page)
    except :
        print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
        return quit()

#PAGINA FAZIONE MEDICI GET
def fazione_ems_get():
    global visualizza_cartella,agg_referto,avviso_comunale_med,mess_priv_med

    data = dbrequest(f'SELECT Rank FROM personaggi WHERE nome="{session["username"]}"', "fetchone")
    rank=int(data[0])

    loc_visualizza_cartella = int(funzionalita.get("MEDICI",'visualizza_cartella'))
    loc_agg_referto =  int(funzionalita.get("MEDICI",'agg_referto'))
    loc_avviso_comunale_med =  int(funzionalita.get("MEDICI",'avviso_comunale'))
    loc_mess_priv_med =  int(funzionalita.get("MEDICI",'mess_priv'))

    if loc_visualizza_cartella:
        if not (rank <= rank_visualizza_cartella):
            visualizza_cartella=0
        else:
            visualizza_cartella=1 

    if loc_agg_referto:
        if not (rank <= rank_agg_referto): 
            agg_referto=0
        else:
            agg_referto=1

    if loc_avviso_comunale_med:
        if not (rank <= rank_avviso_comunale_med): 
            avviso_comunale_med=0
        else:
            avviso_comunale_med=1

    if loc_mess_priv_med:
        if not (rank <= rank_mess_priv_med): 
            mess_priv_med=0
        else:
            mess_priv_med=1

    page = render_template("faz_med.html", visualizza_cartella=visualizza_cartella,agg_referto=agg_referto,avviso_comunale_med=avviso_comunale_med,mess_priv_med=mess_priv_med)

    global template
    global credit
    try:
        return template % (credit, page)
    except :
        print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
        return quit()


#PAGINA FAZIONE SFNN
def fazione_sfnn_get():
    global crea_articolo,avviso_comunale_sfnn,mess_priv_sfnn

    data = dbrequest(f'SELECT Rank FROM personaggi WHERE nome="{session["username"]}"', "fetchone")
    rank=int(data[0])

    loc_crea_articolo = int(funzionalita.get("SFNN",'articolo'))
    loc_avviso_comunale_sfnn =  int(funzionalita.get("SFNN",'avviso_comunale'))
    loc_mess_priv_sfnn =  int(funzionalita.get("SFNN",'mess_priv'))

    if loc_crea_articolo:
        if not (rank <= rank_crea_articolo): 
            crea_articolo=0
        else:
            crea_articolo=1

    if loc_avviso_comunale_sfnn:
        if not (rank <= rank_avviso_comunale_sfnn): 
            avviso_comunale_sfnn=0
        else:
            avviso_comunale_sfnn=1

    if loc_mess_priv_sfnn:
        if not (rank <= rank_mess_priv_sfnn): 
            mess_priv_sfnn=0
        else:
            mess_priv_sfnn=1

    page = render_template("faz_sfnn.html", crea_articolo=crea_articolo,avviso_comunale_sfnn=avviso_comunale_med,mess_priv_sfnn=mess_priv_med)

    global template
    global credit
    try:
        return template % (credit, page)
    except :
        print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
        return quit()

#---------------------------------------------------------------------------------------------
@__app__.route('/fazione', methods=['GET','POST'])
def fazione(error=""):
    if sez_fazione:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            try:
                
                data = dbrequest(f'SELECT Faction FROM personaggi WHERE nome="{session["username"]}"', "fetchone")
                faction=int(data[0])

            except: 
                return fazione_null()

            if faction==id_pula:
                return fazione_polizia_get()
            if faction==id_ems:
                return fazione_ems_get()
            if faction==id_sfnn:
                return fazione_sfnn_get()
            else:
                return fazione_null()

    else:
        return page_not_found(404)

#---------------------------------------------------------------------------------------------
#[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
#________________________________║GESTORE PAGINE PERSONAGGIO║­­____________________________
@__app__.route('/mia-fedina', methods=['GET','POST'])
def mia_fedina(error=""):
    if sez_personaggio:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            reati=visualizza_fedina(session['username'])
            if reati == 0:
                error="Errore lettura fedina penale!"
                reati= []
            elif len(reati) == 0:
                error="Fedina Penale Pulita!"
            else:
                error=""
            
            page = render_template("sez_pers/mia_fedina.html",error=error, reati=reati, len_reati=len(reati))

            global template
            global credit
            try:
                pagina = template % (credit, page)
                return pagina
            except:
                print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                return quit()
    else:
        return page_not_found(404)

#---------------------------------------------------------------------------------------------
@__app__.route('/stats', methods=['GET','POST'])
def stats():
    if sez_personaggio:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            #[SKIN, AGE, PHONENUMBER, PHONECREDIT, MONEY, BANKMONEY]
            stats = load_stats(session['username'])
            
            #[id_model,model,fuel,insurance,value]  
            veh = load_veh(session['username'])

            page = render_template("sez_pers/stats.html",username=session["username"], stats=stats, veh=veh, len_veh=len(veh))

            global template
            global credit
            try:
                pagina = template % (credit, page)
                return pagina
            except:
                print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                return quit()
    else:
        return page_not_found(404) 
#---------------------------------------------------------------------------------------------
@__app__.route('/mia-cartella', methods=['GET','POST'])
def mia_cartella(m='null',error=""):
    if sez_personaggio:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            cartella = visualizza_cartella_clinica(session['username'])
            if cartella == 0:
                error = "Errore Lettura Cartella Clinica"
                cartella=[]
            elif len(cartella) == 0:
                error = "Cartella Clinica Vuota"
            else:
                error=""
                
            page = render_template("sez_pers/mia_cartella.html",error=error, cartella=cartella, len_cartella=len(cartella))
            global template
            global credit
            try:
                pagina = template % (credit, page)
                return pagina
            except:
                print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                return quit()
                   
    else:
        return page_not_found(404)   

#---------------------------------------------------------------------------------------------
# SEZIONE PERSONAGGIO
@__app__.route('/personaggio', methods=['GET','POST'])
def personaggio(error=""):
    if sez_personaggio:
        if not session.get('logged_in'):
            if request.method == 'POST':
                return login()
            return home()
        else:
            sms = visualizza_sms(session['username'])
            if sms == 0:
                error="Impossibile caricare i messaggi!"
                sms=[]
            elif len(sms)==0:
                error="Nessun Messaggio Trovato!"
            else:
                error=""
            page = render_template("sez_personaggio.html",error=error, sms=sms, len_sms=len(sms))
    
            global template
            global credit
            try:
                return template % (credit, page)
            except:
                print(Fore.RED +"Crediti Della Web-App RIMOSSI, Web-APP SPENTA, RIAVVIARE!")
                return quit()
    else:
        return page_not_found(404)
#---------------------------------------------------------------------------------------------
@__app__.route('/logout', methods=['GET','POST'])
def logout():
    if not session.get('logged_in'):
        if request.method == 'POST':
            return login()
        return home()
    else:
        session['logged_in'] = False
        session['username'] = ""
        return home()
        

# ______________FUNZIONE PRINCIPALE___________________
if __name__ == '__main__':
    __app__.secret_key = os.urandom(12)
    start_web_app()
