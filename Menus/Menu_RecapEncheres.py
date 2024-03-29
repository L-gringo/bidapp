import streamlit as st
#from CalculEnchere.getexchangerate.getexchangerate import get_exchange_rate
from streamlitdemo.pandastest import  select_affichage_func
from streamlitdemo.database import delete_items, insert_datastock
from streamlitdemo.pandastest import list_towns


def menu_recap_encheres(Options_Menu,basename,user1,ctkeystr):

    if Options_Menu=="Recap Encheres":
           
           
            
            #st.title("Recapitulatif des encheres")
            st.markdown("<h1 style='text-align: center; color: grey;'>Recapitulatif des encheres</h1>",unsafe_allow_html=True)
            # génère un fichier csv en guise de dataset pour l'affichage du tableau
            #field_Names=["key","Fabricant","Date Enchere", "Date sortie", "Modele", "Montant Enchere"]

            if "MAJ1" not in st.session_state:
                st.session_state.MAJ1=False

            #st.write(st.session_state.MAJ1)

            def callback():
                st.session_state.MAJ1=True


            dataframe_edit=select_affichage_func(basename)
            col1,col2=st.columns([1,1])
            with col1:
                 supp_button= st.button("Supprimer")
            
            with col2:
                add_stock_button=st.button("Ajouter au Stock", on_click=callback)

            if supp_button:
                
                frame=dataframe_edit[0]
                indice=dataframe_edit[1][0]
                value=frame.iloc[indice]["key"]
                delete_items(basename,value)
                st.write("Entrée supprimée")
            
            #if add_stock_button or st.session_state.MAJ1:
            if add_stock_button or st.session_state.MAJ1:    
                frame2=dataframe_edit[0]
                indice2=dataframe_edit[1]
                
                st.write(len(indice2)) 
                for i in indice2:
                        #st.write(st.session_state.MAJ1)
                        line=frame2.iloc[i]
                        modele=str(line["Modele"])
                        annee=int(line["Date sortie"])
                        exchangerate=float(line["Taux de Change"])
                        st.write(f"Merci de completer le formulaire pour l'insertion dans le stock du modele {modele} {annee}")
                        
                        with st.form(key=f"form{i}"):
                              manufacturer_input= st.text_input("Fabricant", str(line["Fabricant"]))
                              model_input= st.text_input("Modele",str(line["Modele"]))
                              model_year_input=st.number_input("Date sortie",int(line["Date sortie"]))
                              sell_date_input=st.date_input("Date de vente")
                              buy_date=st.date_input("Entrer la date d'achat")
                              town=st.selectbox("Selectionner la ville d'origine du véhicule :",list_towns("Transports"),index=0)
                              transpfees=user1.transportfees(town)
                              buy_price_input=st.number_input("Entrer le prix d'achat")
                              sale_price_prev_input=st.number_input("Entrer le prix de vente prévisionnel")
                              exchange_input=st.number_input("Taux de change", value=exchangerate)
                              marge_input=st.number_input("marge", min_value=0)
                              fret_input=st.number_input("Entrer le prix du fret")
                              statuts_input=st.selectbox("Satut",["En stock","Vendu","Concessionnaire","Port de depart","Bateau","Port arrivee","En location"], index=0) 
                              sale_price_final_input=st.number_input("Entrer le prix de vente final")
                              reparations=st.number_input("Montant estimé de réparations",min_value=0)
                              submit_button=st.form_submit_button("Valider")
                              
                        if submit_button:
                             
                            insert_datastock("Stock",
                                             ctkeystr,
                                             manufacturer_input,
                                             model_input,
                                             model_year_input,
                                             buy_date.strftime("%d %B  %Y"),
                                             sell_date_input.strftime("%d %B %Y"),
                                             buy_price_input,
                                             transpfees,
                                             sale_price_prev_input,
                                             sale_price_final_input,
                                             fret_input,reparations,
                                             marge_input,
                                             exchange_input,
                                            statuts_input

                                            )
                            
                            st.write("Entrée ajoutée")
                            

                #st.session_state.MAJ1=False
                #st.write(st.session_state.MAJ1)