from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from subprocess import call
from tkinter import filedialog
import tkinter as tk
from datetime import date


import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestion_absence",
        port=3308
    )
except mysql.connector.Error as error:
    print("Failed to connect to MySQL database: {}".format(error))


#Connect fonction
def connexion():
    utilisatuer = matriculeEntry.get()
    motDePasse = entryMdp.get()
    role = roleCombo.get().lower()
    curr = conn.cursor()
    sql = "SELECT role FROM utilisateur where matricule=%s and mot_de_passe=%s"
    curr.execute(sql, (utilisatuer, motDePasse))
    res = curr.fetchone()

    # controle de saisie
    if(utilisatuer == "" or motDePasse == ""):
        messagebox.showerror("", "Veuillez remplir tous les champs")
        matriculeEntry.delete(0, END)
        entryMdp.delete(0, END)
    elif not res:
        messagebox.showerror("", "Nom d'utilisateur ou mot de passe incorrect")
        matriculeEntry.delete(0, END)
        entryMdp.delete(0, END)
    else:
        db_role = res[0]
        if role != db_role:
            messagebox.showerror("", "Le rôle sélectionné ne correspond pas au rôle de l'utilisateur")
            return
        elif role == "professeur":
            messagebox.showinfo("", "Bienvenue")
            matriculeEntry.delete(0, END)
            entryMdp.delete(0, END)
            root.destroy()
            professeur()
        elif role == "etudiant":
            messagebox.showinfo("", "Bienvenue")
            matricule = utilisatuer
            matriculeEntry.delete(0, END)
            entryMdp.delete(0, END)
            root.destroy()
            etudiant(matricule)
            print(matricule)
             






#creation fenetre 
root = Tk()
root.title("Gestionnaire d'absences")
root.geometry("720x380+350+150")
root.config(background="#ECE8DD")


lbltitre = Label(root, borderwidth=3, text="Page de connexion", relief=SUNKEN, font=("Montserrat", 25), bg="#579BB1", fg="White")
lbltitre.pack(fill=X)

lblmatricule = Label(root, text="Matricule", font=("Ubuntu", 16), bg="#ECE8DD", fg="#222222")
lblmatricule.place(x=200, y=100)
matriculeEntry = Entry(root, bd=4, font=("Ubuntu", 14))
matriculeEntry.place(x=200, y=130, width=350)

lblMdp = Label(root, text="Mot de passe", font=("Ubuntu", 16), bg="#ECE8DD", fg="#222222")
lblMdp.place(x=200, y=180)
entryMdp = Entry(root, show="*", bd=4, font=("Ubuntu", 14))
entryMdp.place(x=200, y=210, width=350)

# création de la liste déroulante
lblRole = Label(root, text="Rôle", font=("Ubuntu", 16), bg="#ECE8DD", fg="#222222")
lblRole.place(x=200, y=260)

roleCombo = ttk.Combobox(root, values=["Etudiant", "Professeur"], font=("Ubuntu", 14))
roleCombo.current(0)
roleCombo.place(x=350, y=265)

btnConnexion = Button(root, text="Se connecter", font=("Montserrat", 18), bg="#579BB1", fg="#FFF", command=connexion)
btnConnexion.place(x=275, y=290, width=200)




def professeur():
    #create cursor
    def currentMat():
        conn = mysql.connector.connect( host="localhost", database="gestion_absence",user="root",password="",port=3308)
        curr = conn.cursor()
        curr.execute("SELECT MAX(id) FROM utilisateur")
        res = curr.fetchone()
        if(res):
            zero = ""
            for i in range(5-len(str(res[0]))):
                zero = zero+"0"
            matricule = "ETU"+zero+str(res[0]+1)
        else:
            matricule = "ETU00001"
        mat_entry.config(state=NORMAL)
        mat_entry.delete(0, END)
        mat_entry.insert(0, matricule)
        mat_entry.configure(state=DISABLED)

    def lire():
        conn = mysql.connector.connect( host="localhost", database="gestion_absence",user="root",password="",port=3308)
         #create cursor
        curr = conn.cursor()
        global count 
        count = 0
        curr.execute("SELECT matricule, nom, prenom, nombre_absence from utilisateur where role='etudiant'")
        res = curr.fetchall()
        curr.close()
        conn.close()

        for row in res:
            if count % 2 == 0:
                table.insert(parent='', index='end', iid=count, values=row, tags=('evenrow',))
            else:
                table.insert(parent='', index='end', iid=count, values=row, tags=('oddrow',))
            count +=1


    root = Tk()
    root.title("Gestionnaire d'absence")
    root.geometry("1000x500")

    #Add some style
    style = ttk.Style()

    #Pick A theme
    style.theme_use('default')

    #Configure the Treeview Colors
    style.configure("Treeview",
        background="#D3D3D3",
        forground="black",
        rowheight=25,
        fieldbackground="#D3D3D3")

    #Change Selected Colors
    style.map(['selected', '#347083'])

    #Create a Treeview Frame 
    treeview_frame = Frame(root)
    treeview_frame.pack(padx=10)

    #Create A Treeview Scrollbar
    treeview_scroll = Scrollbar(treeview_frame)
    treeview_scroll.pack(side=RIGHT, fill=Y)

    #Create The Treeview
    table = ttk.Treeview(treeview_frame, yscrollcommand=treeview_scroll.set, selectmode="extended")
    table.pack()

    #configure the scrollbar
    treeview_scroll.config(command=table.yview)
    #define columns
    table['columns'] = ("Matricule", "Nom", "Prenom", "Absence")

    #format columns
    table.column("#0", width=0, stretch=NO)
    table.column("Matricule", anchor=W, width=245)
    table.column("Nom", anchor=W, width=245)
    table.column("Prenom", anchor=W, width=245)
    table.column("Absence", anchor=W, width=245)
    #create headings
    table.heading("#0", text="")
    table.heading("Matricule", text="Matricule", anchor=W)
    table.heading("Nom", text="Nom", anchor=W)
    table.heading("Prenom", text="Prénom", anchor=W)
    table.heading("Absence", text="Nombre d'absence", anchor=W)

    #Create stripped row
    table.tag_configure('oddrow', background="#FFF")
    table.tag_configure('evenrow', background="lightblue")

    #Add data
    lire()

    #Add fields
    data_frame = LabelFrame(root, text="Enregistrement")
    data_frame.pack(fill="x", expand=YES, padx=20)

    mat_label = Label(data_frame, text="Matricule", font=("Montserrat",12))
    mat_label.grid(row=0, column=0, padx=10, pady=10)
    mat_entry = Entry(data_frame)
    currentMat()
    #mat_entry.insert(0, "ETU" + datetime.now().strftime("%d%m%Y%H%M%S"))
    mat_entry.config(state=DISABLED)
    mat_entry.grid(row=0, column=1 , padx=10, pady=10)

    role_label = Label(data_frame, text="Role", font=("Montserrat",12))
    role_label.grid(row=0, column=2, padx=10, pady=10)
    role_entry = Entry(data_frame)
    role_entry.insert(0,"etudiant")
    role_entry.config(state=DISABLED)
    role_entry.grid(row=0, column=3 , padx=10, pady=10)

    nom_label = Label(data_frame, text="Nom", font=("Montserrat",12))
    nom_label.grid(row=1, column=0, padx=10, pady=10)
    nom_entry = Entry(data_frame)
    nom_entry.grid(row=1, column=1 , padx=10, pady=10)

    pren_label = Label(data_frame, text="Prénom", font=("Montserrat",12))
    pren_label.grid(row=1, column=2, padx=10, pady=10)
    pren_entry = Entry(data_frame)
    pren_entry.grid(row=1, column=3 , padx=10, pady=10)

    mdp_label = Label(data_frame, text="Mot de passe", font=("Montserrat",12))
    mdp_label.grid(row=1, column=4, padx=10, pady=10)
    mdp_entry = Entry(data_frame)
    mdp_entry.insert(0, "1234")
    mdp_entry.config(state=DISABLED)
    mdp_entry.grid(row=1, column=5 , padx=10, pady=10)

    abs_label = Label(data_frame, text="Nombre d'absences", font=("Montserrat",12))
    abs_label.grid(row=2, column=0, padx=10, pady=10)
    abs_entry = Entry(data_frame)
    abs_entry.grid(row=2, column=1, padx=10, pady=10)


    


    #Methods for buttons
    #add record
    def ajouter():
        conn = mysql.connector.connect(host="localhost", database="gestion_absence", user="root", password="", port=3308)
        curr = conn.cursor()
        global count 
        count = 0
        matricule = mat_entry.get()
        role = role_entry.get()
        nom = nom_entry.get()
        prenom = pren_entry.get()
        mdp = mdp_entry.get()
        nombre_absence = int(abs_entry.get())

        # Retrieve raison from historique_absence table based on matricule
        curr.execute("SELECT raison FROM historique_absence WHERE matricule = %s", (matricule,))
        row = curr.fetchone()
        if row is not None:
            raison = row[0]
        else:
            raison = ""

        try:
            sql = "insert into utilisateur (matricule, nom, role, prenom, mot_de_passe, nombre_absence, raison) values (%s,%s,%s,%s,%s,%s,%s)"
            curr.execute(sql, (matricule, nom, role, prenom, mdp, nombre_absence, raison))

            conn.commit()
            messagebox.showinfo("Ajout", "Etudiant(e) ajouté(e) avec succèes !")
            curr.close()
            conn.close()
            mat_entry.delete(0, END)
            nom_entry.delete(0, END)
            pren_entry.delete(0, END)
            abs_entry.delete(0, END)
            currentMat()
            table.delete(*table.get_children())
            lire()
        except Exception as e:
            print(e)
            conn.rollback()
            conn.close()

        #update record
    def modifier():
        conn = mysql.connector.connect(host="localhost", database="gestion_absence", user="root", password="", port=3308)
        curr = conn.cursor()

        #get data
        matricule = mat_entry.get()
        role = role_entry.get()
        nom = nom_entry.get()
        prenom = pren_entry.get()
        mdp = mdp_entry.get()
        nombre_absence = abs_entry.get()

        #retrieve raison from historique_absence table based on matricule
        curr.execute("SELECT raison FROM historique_absence WHERE etudiant_id = %s", (matricule,))
        row = curr.fetchone()
        if row is not None:
            raison = row[0]
        else:
            raison = ""

        #update data
        try:
            sql = "UPDATE utilisateur SET matricule = %s, role = %s, nom = %s, prenom = %s, mot_de_passe = %s, nombre_absence = %s WHERE matricule = %s"
            curr.execute(sql, (matricule, role, nom, prenom, mdp, nombre_absence, matricule,))
            conn.commit()

            # add new entry to historique_absence table
            if int(nombre_absence) > int(abs_entry.previous_value):
                raison = "Absence injustifiée"
                sql = "INSERT INTO historique_absence (date_debut, date_fin, raison, etudiant_id) VALUES (%s, %s, %s, %s)"
                curr.execute(sql, (date.today(), date.today(), raison, matricule))
                conn.commit()

            messagebox.showinfo("Modification", "Etudiant(e) modifié(e) avec succès !")
            mat_entry.delete(0, END)
            nom_entry.delete(0, END)
            pren_entry.delete(0, END)
            abs_entry.delete(0, END)
            currentMat()
            table.delete(*table.get_children())
            lire()

        except Exception as e:
            print(e)
            conn.rollback()

        finally:
            curr.close()
            conn.close()




    #delete record
    def supprimer():
        conn = mysql.connector.connect( host="localhost", database="gestion_absence",user="root",password="",port=3308)
         #create cursor
        curr = conn.cursor()
        global count 
        count = 0
        matricule = mat_entry.get()
        curr = conn.cursor()
        sql = "delete from utilisateur where matricule=%s"
        curr.execute(sql, (matricule,))
        conn.commit()
        messagebox.showinfo("Suppression", "Etudiant(e) supprimé avec succès !")
        mat_entry.delete(0, END)
        nom_entry.delete(0, END)
        pren_entry.delete(0, END)
        currentMat()
        table.delete(*table.get_children())
        lire()
        curr.close()
        conn.close()



    def historique():
        global matricule
        matricule = mat_entry.get()

        def lire():
            global matricule
            conn = mysql.connector.connect(host="localhost", database="gestion_absence", user="root", password="", port=3308)
            # create cursor
            curr = conn.cursor()
            global count
            count = 0
            sql = "SELECT ha.id, date_debut, date_fin, raison from historique_absence as ha  join utilisateur as ut  on ha.etudiant_id=ut.id where ut.matricule=%s"
            curr.execute(sql, (matricule,))
            res = curr.fetchall()
            curr.close()
            conn.close()

            for row in res:
                if count % 2 == 0:
                    table.insert(parent='', index='end', iid=count, values=row, tags=('evenrow',))
                else:
                    table.insert(parent='', index='end', iid=count, values=row, tags=('oddrow',))
                count += 1

        historique = Toplevel(root)
        historique.title("Historique d'absences")
        historique.geometry("1000x500")


        #Add some style
        style = ttk.Style()

        #Pick A theme
        style.theme_use('default')

        #Configure the Treeview Colors
        style.configure("Treeview",
            background="#D3D3D3",
            forground="black",
            rowheight=25,
            fieldbackground="#D3D3D3")

        #Change Selected Colors
        style.map(['selected', '#347083'])

        #Create a Treeview Frame 
        treeview_frame = Frame(historique)
        treeview_frame.pack(padx=10)

        #Create A Treeview Scrollbar
        treeview_scroll = Scrollbar(treeview_frame)
        treeview_scroll.pack(side=RIGHT, fill=Y)

        #Create The Treeview
        table = ttk.Treeview(treeview_frame, yscrollcommand=treeview_scroll.set, selectmode="extended")
        table.pack()

        #configure the scrollbar
        treeview_scroll.config(command=table.yview)
        #define columns
        table['columns'] = ("ID", "Debut", "Fin", "Raison")

        #format columns
        table.column("#0", width=0, stretch=NO)
        table.column("ID", anchor=W, width=245)
        table.column("Debut", anchor=W, width=245)
        table.column("Fin", anchor=W, width=245)
        table.column("Raison", anchor=W, width=245)
        #create headings
        table.heading("#0", text="")
        table.heading("ID", text="ID Absence", anchor=W)
        table.heading("Debut", text="Date De Début", anchor=W)
        table.heading("Fin", text="Date De Fin", anchor=W)
        table.heading("Raison", text="Raison", anchor=W)

        #Create stripped row
        table.tag_configure('oddrow', background="#FFF")
        table.tag_configure('evenrow', background="lightblue")

        lire() 
    





















    #select record from the treeview
    def selectionner():
        mat_entry.config(state=NORMAL)
        #Clear the entry boxes
        mat_entry.delete(0, END)
        nom_entry.delete(0, END)
        pren_entry.delete(0, END)
        abs_entry.delete(0,END)
        #Grab record number
        selected = table.focus()
        #Grab record values
        values = table.item(selected, 'values')
        mat_entry.insert(0, values[0])
        mat_entry.config(state=DISABLED)
        nom_entry.insert(0, values[1])
        pren_entry.insert(0, values[2])
        abs_entry.insert(0,values[3])
    #Add  buttons
    button_frame = LabelFrame(root, text="Actions")
    button_frame.pack(fill="x", expand=YES, padx=20)

    btn_ajouter = Button(button_frame, text="Ajouter", command=ajouter)
    btn_ajouter.grid(row=0, column=0, padx=10, pady=10)

    

    btn_modifier = Button(button_frame, text="Modifier",command=modifier)
    btn_modifier.grid(row=0, column=1, padx=10, pady=10)

    btn_supprimer = Button(button_frame, text="Supprimer", command=supprimer)
    btn_supprimer.grid(row=0, column=2, padx=10, pady=10)

    btn_historique = Button(button_frame, text="Voir l'historique des absences", command=historique)
    btn_historique.grid(row=0, column=4, padx=10, pady=10)

    btn_select = Button(button_frame, text="Selectionner", command=selectionner)
    btn_select.grid(row=0, column=5, padx=10, pady=10)


    etudiant_id=None
    def ajouter_absence():
        # Récupérer les valeurs entrées par l'utilisateur
        matricule = mat_entry.get()
        debut = debut_entry.get()
        fin = fin_entry.get()
        raison = raison_entry.get()

        # Vérifier que toutes les valeurs ont été saisies
        if not matricule or not debut or not fin or not raison:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return

        # Se connecter à la base de données
        conn = mysql.connector.connect(host="localhost", database="gestion_absence", user="root", password="", port=3308)
        curr = conn.cursor()

        # Récupérer l'ID de l'étudiant correspondant au matricule entré
        sql_id = "SELECT id FROM utilisateur WHERE matricule = %s"
        curr.execute(sql_id, (matricule,))
        res_id = curr.fetchone()

        # Insérer l'absence dans la base de données avec l'ID de l'étudiant
        sql = "INSERT INTO historique_absence (etudiant_id, date_debut, date_fin, raison) VALUES (%s, %s, %s, %s)"
        values = (res_id[0], debut, fin, raison)
        conn.commit()

        # Afficher un message de confirmation
        messagebox.showinfo("Succès", "L'absence a été ajoutée avec succès")

        print(sql, values)  # Add this line
        curr.execute(sql, values)

        sql_count = "SELECT COUNT(*) FROM historique_absence WHERE etudiant_id = %s"
        curr.execute(sql_count, (res_id[0],))
        nombre_absences = curr.fetchone()[0]

        # Mettre à jour le nombre d'absences dans la table d'utilisateurs
        sql_update = "UPDATE utilisateur SET nombre_absence = %s WHERE id = %s"
        curr.execute(sql_update, (nombre_absences, res_id[0]))
        conn.commit()

        # Fermer la connexion à la base de données
        curr.close()
        conn.close()

        # Effacer les champs du formulaire
        mat_entry.delete(0, END)
        debut_entry.delete(0, END)
        fin_entry.delete(0, END)
        raison_entry.delete(0, END)


    # Créer les champs du formulaire
    mat_label = Label(root, text="Matricule")
    mat_entry = Entry(root)
    debut_label = Label(root, text="Date de début (AAAA-MM-JJ)")
    debut_entry = Entry(root)
    fin_label = Label(root, text="Date de fin (AAAA-MM-JJ)")
    fin_entry = Entry(root)
    raison_label = Label(root, text="Raison")
    raison_entry = Entry(root)

    # Positionner les champs dans la fenêtre
    mat_label.pack()
    mat_entry.pack()
    debut_label.pack()
    debut_entry.pack()
    fin_label.pack()
    fin_entry.pack()
    raison_label.pack()
    raison_entry.pack()

    btn_ajouter_absence = Button(button_frame, text="Ajouter une absence", command= ajouter_absence)
    btn_ajouter_absence.grid(row=0, column=3, padx=10, pady=10)


   

def etudiant(matricule):
    res_info = None

    def lire():
         conn = mysql.connector.connect( host="localhost", database="gestion_absence",user="root",password="",port=3308)
         curr = conn.cursor()
         global count 
         count = 0
         sql = "SELECT ha.id, date_debut, date_fin, raison from historique_absence as ha join utilisateur as ut on ha.etudiant_id=ut.id where ut.matricule=%s"
         curr.execute(sql, (matricule,))
         res = curr.fetchall()

         sql_info = "SELECT nom, prenom, matricule FROM utilisateur WHERE matricule=%s"
         curr.execute(sql_info, (matricule,))
         res_info = curr.fetchone()
         nom_label.config(text="Nom: "+res_info[0])
         prenom_label.config(text="Prenom: "+res_info[1])
         matricule_label.config(text="Matricule: "+res_info[2])
            
         curr.close()
         conn.close()

         for row in res:
             if count % 2 == 0:
                 table.insert(parent='', index='end', iid=count, values=row, tags=('evenrow',))
             else:
                 table.insert(parent='', index='end', iid=count, values=row, tags=('oddrow',))
             count +=1
            
             return res_info



    root = Tk()
    root.title("Historique d'absences")
    root.geometry("1000x500")

    #Add some style
    style = ttk.Style()

    #Pick A theme
    style.theme_use('default')

    #Configure the Treeview Colors
    style.configure("Treeview",
        background="#D3D3D3",
        forground="black",
        rowheight=25,
        fieldbackground="#D3D3D3")

    #Change Selected Colors
    style.map(['selected', '#347083'])

    #Create a Treeview Frame 
    treeview_frame = Frame(root)
    treeview_frame.pack(padx=10)

    #Create A Treeview Scrollbar
    treeview_scroll = Scrollbar(treeview_frame)
    treeview_scroll.pack(side=RIGHT, fill=Y)

    #Create The Treeview
    table = ttk.Treeview(treeview_frame, yscrollcommand=treeview_scroll.set, selectmode="extended")
    table.pack()

    #configure the scrollbar
    treeview_scroll.config(command=table.yview)
    #define columns
    table['columns'] = ("ID", "Debut", "Fin", "Raison")

    #format columns
    table.column("#0", width=0, stretch=NO)
    table.column("Debut", anchor=W, width=245)
    table.column("Fin", anchor=W, width=245)
    table.column("Raison", anchor=W, width=245)
    #create headings
    table.heading("#0", text="")
    table.heading("ID", text="ID", anchor=W)
    table.heading("Debut", text="Date De Début", anchor=W)
    table.heading("Fin", text="Date De Fin", anchor=W)
    table.heading("Raison", text="Raison", anchor=W)

    #Create stripped row
    table.tag_configure('oddrow', background="#FFF")
    table.tag_configure('evenrow', background="lightblue")

    #Add data
    # ...

    # Ajouter des widgets pour afficher les informations personnelles de l'étudiant
    info_frame = Frame(root)
    info_frame.pack(side=LEFT, padx=10)

    nom_label = Label(info_frame, text="Nom: ")
    nom_label.pack()
    prenom_label = Label(info_frame, text="Prénom: ")
    prenom_label.pack()
    matricule_label = Label(info_frame, text="Matricule: ")
    matricule_label.pack()

    lire()
    # Ajouter cette ligne à la fin de la fonction lire()
    table.insert(parent='', index='end', values=(res_info[0], res_info[1], res_info[2]), tags=('inforow',))
    table.tag_configure('inforow', background="#D3D3D3")
    # Call the lire() function and assign the return value to a variable
    res_info = lire()

mainloop()


