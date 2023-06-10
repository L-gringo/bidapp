from deta import Deta
import datetime
import streamlit_authenticator as stauth
from bidapp.streamlitdemo.generatecsv import gencsv

DETA_KEY="a0awy5axjcn_kq6uEzReYznKn68FiTRJWfnFEJWPKk95"

deta=Deta(DETA_KEY)

def insert_dataenchere(basename,key, manufacturer, model, modeldate,enchere,currday):

    db = deta.Base(basename)
    db.put({"key":key, "Fabricant":manufacturer, "Modele":model, "Date sortie":modeldate, "Montant Enchere":enchere, "Date Enchere":currday})

def insert_datastock(basename,key, manufacturer, model, modeldate,buydate,buyprice,transp,salepriceprev,salepriceend,fret,repair,marge,statut):

    db = deta.Base(basename)
    
    db.put(
        {"key":key, 
            "Fabricant":manufacturer, 
            "Modele":model, 
            "date sortie":modeldate,
              "date achat":buydate,
              "frais transport":transp,
              "fret":fret,
              "marge":marge,
              "prix achat":buyprice, 
              "prix de vente previsionnel":salepriceprev, 
              "prix de vente final":salepriceend,
              "reparations":repair,
                "statut":statut}
         )


#def insert_marge_base(basename,key, manufacturer, model, modeldate,buydate,buyprice,salepriceend,marge):
def insert_marge_base(basename,key, manufacturer, model, modeldate, buydate, buyprice, salepriceend, marge):

    db = deta.Base(basename)
    
    db.put(
        {"key":key, 
            "Fabricant":manufacturer, 
            "Modele":model, 
            "date sortie":modeldate,
              "date achat":buydate,
              "prix achat":buyprice,
              "prix de vente final":salepriceend,
              "marge":marge,
               
              }
         )

def insert_cred(basename,username, name, password):

    hashed_pass= stauth.Hasher(password).generate() 
    db=deta.Base(basename)
    db.put({"Key":username,"Name":name,"password":hashed_pass})

def fetch_data(basename):
    db=deta.Base(basename)
    data=db.fetch()
    return data.items

def update_db(basename, keyval, fab, mod, ds, da, tf, ft, pa, pvf, pvp, rp, mg,stt):

    db=deta.Base(basename)
    updates={"Fabricant":fab,
            "Modele":mod, 
            "date sortie":ds,
            "date achat":da,
            "frais transport":tf,
            "fret":ft,
            "prix achat":pa,
            "prix de vente previsionnel":pvp,
            "prix de vente final":pvf,  
            "reparations":rp, 
            "marge":mg,         
            "statut":stt,
            }
    db.update(updates=updates, key=keyval)


def update_marge(basename, keyval,mg):

    db=deta.Base(basename)
    updates={"marge":mg}
    db.update(updates=updates,key=keyval)


def delete_items(basename, keyval):

    db=deta.Base(basename)
    db.delete(key=keyval)
    
#value="2023-06-07-00-27-09"
#update_db("Stock",value,"MAZDA","Aoura","07 June  2023","2008","15470","78548997","108900000","78459","vendu")

#datas= fetch_data("History1")
#gencsv("Historicenchere.csv", datas,["key","Date Enchere", "Date sortie", "Modele", "Montant Enchere"])

#print(ct)
#insert_data("History1","Honda","CRV",2008,10000,ctstr)
#insert_cred("Credbase","Mannou","Freaky1","sato")