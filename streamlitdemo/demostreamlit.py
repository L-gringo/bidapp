import streamlit_authenticator as stauth
import streamlit as st
from bidapp.user.user import user
#from CalculEnchere.getexchangerate.getexchangerate import get_exchange_rate
from bidapp.Connector.connector import connect
import datetime
from streamlit_option_menu import option_menu
from bidapp.Menus import Menu_CalculEnchere, Menu_AjoutNouvelAchat, Menu_RecapEncheres, Menu_MajStatutParc, Menu_Generermarge, Menu_Recapdesmarges, Menu_Stockparc
import pandas as pd


def main():
     
     #Mes variables globales

    ct=datetime.datetime.now()
    ctkeystr=ct.strftime("%Y-%m-%d-%H-%M-%S")
    ctstr=ct.strftime("%d %B  %Y") 
    credentials= connect()
    stockcsvpath="C:\\Users\\ma79caen\\Documents\\vscodetest\\.venv\\streamlitdemo\\Stock.csv"
    historiccsvpath="C:\\Users\\ma79caen\\Documents\\vscodetest\\.venv\\streamlitdemo\\Historicdataset.csv"
    margescsvpath="C:\\Users\\ma79caen\\Documents\\vscodetest\\.venv\\streamlitdemo\\Marges.csv"
    field_Names1=["key",
                "Fabricant",
                 "Modele", 
                 "date sortie",
                 "date achat",
                 "frais transport",
                 "fret",
                 "prix achat",
                 "prix de vente previsionnel",
                 "prix de vente final",
                 "reparations",
                 "marge",
                 "statut"]
    
    exchangerate=0.932


    #authenticator= stauth.Authenticate(names,usernames,hashed_passwords, "cookies", "abcdef", cookie_expiry_days=7)
    #Authentification à l'appli
    authenticator= stauth.Authenticate(credentials, "cookies", "abcdef", cookie_expiry_days=7)

    name, authentication_status, username = authenticator.login("login","main")

    if authentication_status==False:
         st.error("Username/password is incorrect")

    if authentication_status==None:
         st.warning("Please enter your username and password")
    
    if authentication_status:

        
        authenticator.logout("Logout", "sidebar")

        #Logging
        user1=user(username)
        
        #Menu
        
            #Informations sur le prix de vente final, le fret, la marge visée, le nom du modèle, la date de sortie 
        #st.title(":green[RECAP DES ENCHERES]")
        
        #barre latérale avec le menu
        with st.sidebar:
            st.header (f"Bienvenue {name}")

            Options_Menu= option_menu(menu_title=None, 
                         options=["Calcul Enchere", "Ajout Nouvel Achat","Recap Encheres","MAJ Statut Parc", "Generer Marge","Recap Des Marges","Stock Parc"],
                         icons=["calculator","cart-plus","table","check-all","coin","currency-dollar","database-fill"],
                         default_index=0,
                         orientation="vertical")
        
        #Option de calcul Enchere qui propose le formulaire de calcul des enchères
        
        Menu_CalculEnchere.menu_calcul_enchere(Options_Menu,user1,exchangerate,ctkeystr,ctstr)

        #Option qui affiche le récap des enchères calculées
    
        Menu_RecapEncheres.menu_recap_encheres(Options_Menu,historiccsvpath,"History2","Historicdataset.csv", user1,ctkeystr)
           
        # Option qui permet de rajouter chaque nouvelle achat au stock. Il génère une base de données Stock qui sera ensuite remplie
        #avec les infos du véhicule et des montants prévisionnels pour la vente le fret, etc.

        Menu_AjoutNouvelAchat.menu_ajout_nouvel_achat(Options_Menu,user1,ctkeystr)        
    
        # Option pour mettre à jour les informations des véhicules en stock, notamment suite à une vente ou une arrivée de véhicule

        Menu_MajStatutParc.menu_maj_statut_parc(Options_Menu,"Stock",field_Names1,"Stock.csv",stockcsvpath,user1) 

       #Option pour calculer la marge générée par véhicule 

        Menu_Generermarge.menu_generer_marge(Options_Menu,"Stock",field_Names1,"Stock.csv",stockcsvpath,exchangerate)
           
            # Actions pour afficher le récap des marges calculées et effectuer des sommes de marges

        Menu_Recapdesmarges.menu_recap_marges(Options_Menu,"Marges","Marges.csv",margescsvpath)
        
        #Option pour afficher le contenu du stock ainsi que le statut de disponibilité des véhicules

        Menu_Stockparc.menu_stock_parc(Options_Menu,"Stock",field_Names1,"Stock.csv",stockcsvpath)    
       
        
if __name__=="__main__":
        main()