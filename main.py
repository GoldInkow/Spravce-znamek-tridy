import tkinter as tk
import json
database = {}
otazka = None
extra_okno = None
extra_okno2 = None

# ---------------------------------------------------------------------------------------------------------------------------

def vycentruj_okno(okno, sirka, vyska):
    sirka_obrazovky = okno.winfo_screenwidth()
    vyska_obrazovky = okno.winfo_screenheight()
    x = (sirka_obrazovky - sirka) // 2
    y = (vyska_obrazovky - vyska) // 2
    okno.geometry(f"{sirka}x{vyska}+{x}+{y}")

# ---------------------------------------------------------------------------------------------------------------------------

def save():
    database = {'Učitel': ucitel,'Třida': trida,'Předměty': data_predmety, 'Studenty': data_studenty}
    with open('Database_files/Database_Třidy.json','w',encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=4)

def start_button():
    global ucitel
    global trida
    if vstup_jmeno and vstup_trida:
        jmeno = vstup_jmeno.get()
        if not jmeno:
            upozorneni.config(text='Zadejte jmeno!')
            return
        trida_jmeno = vstup_trida.get()
        if not trida_jmeno:
            upozorneni.config(text='Zadejte jmeno třidy!')
            return
        ucitel = jmeno.title()
        trida = trida_jmeno.title()
        save()
    start_okno.destroy()
    hlavni_okno()

def radek_button(Data, Okno, SizeX, SizeY, posX, posY):
    if Data == []:
        tk.Label(Okno,text='Není data! Přidej je.',font=('Arial',16)).place(x=posX,y=posY,anchor='center')
    else:
        Buttons = []
        for i in range(len(Data)):
            if i > 8:
                break
            button = tk.Button(Okno,text=Data[i],font=('Arial',16))
            button.place(x=posX, y=posY+(i*50),anchor='center',width=SizeX,height=SizeY)
            Buttons.append(button)
        return Buttons

def radek_label(Data, Okno, posX, posY):
    if Data == []:
        tk.Label(Okno,text='Není data! Přidej je.',font=('Arial',16)).place(x=posX,y=posY,anchor='center')
    else:
        Labels = []
        for i in range(len(Data)):
            if i > 8:
                break
            label = tk.Label(Okno,text='-',font=('Arial',16),justify='center')
            label.place(x=posX, y=posY+(i*40),anchor='center')
            Labels.append(label)
        return Labels  

def seznam_zaplneni(seznam,data):
    try:
        for info in data:
            seznam.insert(tk.END, info)
    except FileNotFoundError:
        print("Soubor neexistuje, začínám s prázdným seznamem.")

def close_extra_okno(okno):
    try:
        okno.destroy()
    except (AttributeError, NameError, tk.TclError):
        return

def open_new_extra_okno(Text, x, y):
    Okno = tk.Tk()
    Okno.title(Text)
    vycentruj_okno(Okno, x, y)
    return Okno

def hlv_close():
    close_extra_okno(otazka)
    close_extra_okno(extra_okno)
    close_extra_okno(extra_okno2)
    hlv_okno.destroy()

def okno_otazka(i,com):
    global otazka
    def if_ne():
        otazka.destroy() 
    otazka = open_new_extra_okno('Otazka',600,100)
    tk.Label(otazka,text=i,font=('Arial',16)).place(x=300, y=25, anchor='center')
    ano = tk.Button(otazka, text='Ano',font=('Arial',16),command=com)
    ano.place(x=200,y=75,anchor='center',height=40,width=160)
    ne = tk.Button(otazka, text='Ne',font=('Arial',16),command=if_ne)
    ne.place(x=400,y=75,anchor='center',height=40,width=160)

def prumer(list):
    try:
        return float(f'{sum(list)/len(list):.2f}')
    except ZeroDivisionError:
        return '-'

# ---------------------------  Save Load  -----------------------------------------------------------------------------------

try:
    with open('Database_files/Database_Třidy.json','r',encoding='utf-8') as f:
        database = json.load(f)
        try:
            ucitel = database['Učitel']
            trida = database['Třida']
        except KeyError:
            ucitel, trida = '', ''
        try:
            data_studenty = database['Studenty']
            data_predmety = database['Předměty']
        except KeyError:
            data_studenty = {}
            data_predmety = []
except FileNotFoundError:
    ucitel = ''
    trida = ''
    data_studenty = {}
    data_predmety = []

# ---------------------------  Start Okno  ----------------------------------------------------------------------------------

start_okno = tk.Tk()
start_okno.title('Spravce znamek třidy')
vycentruj_okno(start_okno, 800, 800)

tk.Label(start_okno,text='Vytejte v Programu',font=('Arial',25)).place(x=400,y=100,anchor="center")
tk.Label(start_okno,text='Spravce třidnich znamek',font=('Arial',36)).place(x=400,y=160,anchor="center")

if not ucitel or not trida:
    tk.Label(start_okno,text='Zadejte jmeno třidniho učitele:',font=('Arial',25)).place(x=400,y=280,anchor="center")
    vstup_jmeno = tk.Entry(start_okno,justify='center',font=('Arial',17))
    vstup_jmeno.place(x=400,y=350,width=500,height=50,anchor="center")
    tk.Label(start_okno,text='Zadejte nazev třidy:',font=('Arial',25)).place(x=400,y=420,anchor="center")
    vstup_trida = tk.Entry(start_okno,justify='center',font=('Arial',17))
    vstup_trida.place(x=400,y=480,width=500,height=50,anchor="center")
else:
    vstup_jmeno, vstup_trida = False, False
    tk.Label(start_okno,text=f'Vytejte zpatky {ucitel}',font=('Arial',28)).place(x=400,y=400,anchor="center")

upozorneni = tk.Label(start_okno, text='', font=('Arial',16))
upozorneni.place(x=400,y=600,anchor='center')

start = tk.Button(start_okno,text='Start',font=('Arial',24),command=start_button)
start.place(x=400,y=700,width=600,height=60,anchor="center")

# -------------------------------  Hlavni Okno  ------------------------------------------------------------------------------

def hlavni_okno():
    def button_pridat_studenta():
        global otazka
        global extra_okno
        global extra_okno2
        close_extra_okno(otazka)
        close_extra_okno(extra_okno)
        close_extra_okno(extra_okno2)
        extra_okno = open_new_extra_okno('Přidat studenta', 400, 400)
        def pridat():
            data_studenty[Text.title()] = {'Věk': Cislo,}
            save()
            seznam.insert(tk.END, Text.title())
            extra_okno.destroy()
            otazka.destroy()
        def pridat_studenta():
            global seznam
            global Text
            global Cislo
            Text = jmeno_prijmeni.get()
            Cislo = rok.get() 
            if len(Text.split(' ')) < 2:
                upozorneni.config(text='Špatně zadane jmeno a přijmení!')
                return
            elif not Cislo.isdigit() or int(Cislo) > 50:
                upozorneni.config(text='Špatně zadani věk!')
                return
            elif Text.title() in data_studenty:
                upozorneni.config(text=f'{Text.title()} už existuje!')
                return
            okno_otazka(f'Opravdu chcete přidat {Text.title()} do seznamu?',pridat)

        tk.Label(extra_okno,text='Zadejte jmeno a přijmeni:',font=('Arial',16)).place(x=200,y=60,anchor="center")
        jmeno_prijmeni = tk.Entry(extra_okno,font=('Arial',16),justify='center')
        jmeno_prijmeni.place(x=200,y=110,width=378,height=40,anchor="center")

        tk.Label(extra_okno,text='Zadejte kolik mu/ji je let:',font=('Arial',16),).place(x=200,y=190,anchor="center")
        rok = tk.Entry(extra_okno,font=('Arial',16),justify='center')
        rok.place(x=200,y=240,width=378,height=40,anchor="center")

        upozorneni = tk.Label(extra_okno,text='',font=('Arial',16))
        upozorneni.place(x=200,y=320,anchor="center")
        ulozit = tk.Button(extra_okno,text='Uložit',font=('Arial',16),height=1,width=31,command=pridat_studenta)
        ulozit.place(x=200,y=360,anchor="center")

    def button_smazat_studenta():
        global otazka
        global extra_okno
        global extra_okno2
        close_extra_okno(otazka)
        close_extra_okno(extra_okno)
        close_extra_okno(extra_okno2)
        def smazat():
            del data_studenty[seznam.get(student)]
            seznam.delete(student[0])
            save()
            otazka.destroy()
        try:
            student = seznam.curselection()
            jmeno_studenta = seznam.get(student)
            if not jmeno_studenta == '':
                okno_otazka(f'Opravdu chcete smazat studenta {jmeno_studenta}',smazat)
            else:
                return
        except IndexError:
            return
     
    def button_nastavit_znamky():
        global vybrani_predmět
        global extra_okno
        global extra_okno2
        global otazka
        close_extra_okno(extra_okno)
        close_extra_okno(extra_okno2)
        close_extra_okno(otazka)
        def if_zero_or_keyerror(predmet):
            try:
                prumer_label.config(text=f'Pruměr: {prumer(data_studenty[student][predmet])}')
            except (KeyError, ZeroDivisionError):
                prumer_label.config(text='Pruměr: -')
        def predmet_button(button,index,posX,posY):
            def nacist_znamky_a_label_change():
                global vybrani_predmět
                znamky_seznam.delete(0, tk.END)
                znamky_seznam.config(font=('Arial',16))
                try:
                    for znamky in data_studenty[student][data_predmety[index]]:
                        znamky_seznam.insert(tk.END,znamky)
                    if znamky_seznam.size() == 0:
                        znamky_seznam.insert(tk.END,'Prazdne')
                        znamky_seznam.config(font=('Arial',10))
                except KeyError:
                    znamky_seznam.insert(tk.END,'Prazdne')
                    znamky_seznam.config(font=('Arial',10))
                vybrani_predmět = data_predmety[index]
                if_zero_or_keyerror(vybrani_predmět)
                ukazovac1.place(x=(posX-175),y=(posY+(50*index)),anchor='center')
                ukazovac2.place(x=(posX+175),y=(posY+(50*index)),anchor='center')
            button.config(command=nacist_znamky_a_label_change)
        def hotovo_button():
            save()
            close_extra_okno(extra_okno)
        def pridat_znamku():
            global znamky_seznam
            global extra_okno2
            def pridani_a_save_znamky():
                znamka = vstup_znamky.get()
                if znamka.isdigit():
                    if 0 < int(znamka) < 6:
                        try:
                            list_znamek = list(data_studenty[student][vybrani_predmět])
                        except KeyError:
                            list_znamek = []
                        list_znamek.append(int(znamka))
                        data_studenty[student][vybrani_predmět] = list_znamek
                        if_zero_or_keyerror(vybrani_predmět)
                        try:
                            if znamky_seznam.get(0)=='Prazdne':
                                znamky_seznam.delete(0,tk.END)
                                znamky_seznam.config(font=('Arial',16))
                        except ValueError:
                            print('Chyba')
                        znamky_seznam.insert(tk.END,znamka)
                        save()
                        extra_okno2.destroy()
                    else:
                        upozorneni.config(text='Zadejte znamku od 1 do 5')
                else:
                    upozorneni.config(text='Zadejte čislo!')
            if not vybrani_predmět == '':
                extra_okno2 = open_new_extra_okno('Přidat znamku',300,300)
                tk.Label(extra_okno2,text=f'Student: {student}',font=('Arial',16)).place(x=150,y=20,anchor="center")
                tk.Label(extra_okno2,text=f'Předmět: {vybrani_predmět}',font=('Arial',16)).place(x=150,y=60,anchor="center")
                tk.Label(extra_okno2,text='Zadejte znamku:',font=('Arial',16)).place(x=150,y=120,anchor="center")
                vstup_znamky = tk.Entry(extra_okno2,font=('Arial',16),justify='center')
                vstup_znamky.place(x=150,y=160,anchor="center",width=200,height=40)
                upozorneni = tk.Label(extra_okno2,text='',font=('Arial',14))
                upozorneni.place(x=150,y=210,anchor="center")
                pridat_znamku_tlacitko = tk.Button(extra_okno2,text='Přidat',font=('Arial',16),command=pridani_a_save_znamky)
                pridat_znamku_tlacitko.place(x=150,y=260,anchor="center",width=250,height=40)
        def smazani_a_save_znamky():
            global znamky_seznam
            global data_studenty
            def smazat():
                znamky_seznam.delete(znamka)
                list_znamek.remove(list_znamek[znamky_seznam.index(znamka)])
                data_studenty[student][vybrani_predmět] = list_znamek
                if_zero_or_keyerror(vybrani_predmět)
                save()
                otazka.destroy()
            znamka = znamky_seznam.curselection()
            try:
                list_znamek = list(data_studenty[student][vybrani_predmět])
            except KeyError:
                return
            if znamka:
                okno_otazka(f'Chcete smazat znamku: {list_znamek[znamky_seznam.index(znamka)]}',smazat)
        try:
            global znamky_seznam
            student = seznam.curselection()
            student = seznam.get(student)
            vybrani_predmět = ''
            if not student == '':
                extra_okno = open_new_extra_okno('Nastavit znamky',600,600)
                tk.Label(extra_okno,text=f'Znamky studenta {student}',font=('Arial',20)).place(x=300,y=30,anchor="center")
                znamky_seznam = tk.Listbox(extra_okno,font=('Arial',10),justify='center')
                znamky_seznam.place(x=470,y=270,anchor="center",width=100,height=400)
                znamky_seznam.insert(tk.END,'Vyberte předmět')
                Predmety_tlacitka = radek_button(data_predmety, extra_okno, 300, 40, 200, 80)
                ukazovac1 = tk.Label(extra_okno,text='>>',font=('Arial',20))
                ukazovac1.place(x=-400,y=0,anchor='center')
                ukazovac2 = tk.Label(extra_okno,text='<<',font=('Arial',20))
                ukazovac2.place(x=-100,y=0,anchor='center')
                prumer_label = tk.Label(extra_okno,text=f'Pruměr: -',font=('Arial',14))
                prumer_label.place(x=470,y=500,anchor='center')

                pridat = tk.Button(extra_okno,text='Přidat',font=('Arial',18),command=pridat_znamku)
                pridat.place(x=100,y=550,anchor="center",height=40,width=150)

                smazat = tk.Button(extra_okno,text='Smazat',font=('Arial',18),command=smazani_a_save_znamky)
                smazat.place(x=300,y=550,anchor="center",height=40,width=150)

                hotovo = tk.Button(extra_okno,text='Hotovo',font=('Arial',18),command=hotovo_button)
                hotovo.place(x=500,y=550,anchor="center",height=40,width=150)

                try:
                    for button in Predmety_tlacitka:
                        predmet_button(button,Predmety_tlacitka.index(button),200, 80)
                except TypeError:
                    return
            else:
                # label pro chybu
                return
        except NameError:
            print('Chyba')
            extra_okno.destroy()
            return

    def button_nastavit_predmety():
        global otazka
        global extra_okno
        global extra_okno2
        close_extra_okno(otazka)
        close_extra_okno(extra_okno)
        close_extra_okno(extra_okno2)
        def button_hotovo():
            extra_okno.destroy()

        def pridani_a_save_předmětu():
            def pridani_a_save():
                def pridat():
                    data_predmety.append(text.capitalize())
                    predmety_seznam.insert(tk.END,text.capitalize())
                    save()
                    close_extra_okno(extra_okno2)
                    close_extra_okno(otazka)
                text = vstup_predmet.get()
                if text:
                    okno_otazka(f'Chcete přidat předmět {text}',pridat)
            if len(data_predmety) > 8:
                return
            else:
                global extra_okno2
                extra_okno2 = open_new_extra_okno('Přidat',400,400)
                tk.Label(extra_okno2,text='Zadejte nazvu předmětu:',font=('Arial',18)).place(x=200,y=120,anchor='center')
                vstup_predmet = tk.Entry(extra_okno2,font=('Arial',16),justify='center')
                vstup_predmet.place(x=200,y=180,anchor='center',width=300,height=50)
                button = tk.Button(extra_okno2,text='Přidat',font=('Arial',16),command=pridani_a_save)
                button.place(x=200,y=350,anchor='center',width=300,height=50)

        def smazani_a_save_předmětu():
            global data_predmety
            def smazat():
                data_predmety.remove(info)
                predmety_seznam.delete(predmet)
                for student in data_studenty:
                    try:
                        del data_studenty[student][info]
                    except KeyError:
                        continue
                save()
                otazka.destroy()
            predmet = predmety_seznam.curselection()
            info = predmety_seznam.get(predmet)
            if predmet:
                okno_otazka(f'Chcete smazat předmět: {info}',smazat)
        extra_okno = open_new_extra_okno('Nastavit předměty',500,500)
        tk.Label(extra_okno,text='Nastavení předmětu',font=('Arial',20)).place(x=250,y=30,anchor='center')
        tk.Label(extra_okno,text='Max 9 předmětu',font=('Arial',14)).place(x=250,y=60,anchor='center')
        predmety_seznam = tk.Listbox(extra_okno,justify='center',font=('Arial',16))
        predmety_seznam.place(x=250,y=250,anchor='center',width=400,height=330)
        pridat = tk.Button(extra_okno,text='Přidat',font=('Arial',16),command=pridani_a_save_předmětu)
        pridat.place(x=90,y=460,width=150,height=45,anchor='center')
        smazat = tk.Button(extra_okno,text='Smazat',font=('Arial',16),command=smazani_a_save_předmětu)
        smazat.place(x=250,y=460,width=150,height=45,anchor='center')
        hotovo = tk.Button(extra_okno,text='Hotovo',font=('Arial',16),command=button_hotovo)
        hotovo.place(x=410,y=460,width=150,height=45,anchor='center')
        for predmet in data_predmety:
            if data_predmety.index(predmet) > 8:
                break
            predmety_seznam.insert(tk.END,predmet)

    def button_zobrazit_info():
        global otazka
        global extra_okno
        global extra_okno2
        close_extra_okno(otazka)
        close_extra_okno(extra_okno)
        close_extra_okno(extra_okno2)
        def button_hotovo():
            extra_okno.destroy()

        def button_zmenit_vek():
            global extra_okno2
            def zmenit_vek():
                def zmenit():
                    data_studenty[student]['Věk'] = vek
                    save()
                    close_extra_okno(extra_okno2)
                global data_studenty
                vek = vstup_vek.get()
                if vek:
                    if not vek.isdigit() or int(vek) > 50:
                        upozorneni.config(text='Špatně zadani věk!')
                    elif vek == data_studenty[student]['Věk']:
                        upozorneni.config(text='Věk je stejni!')
                    else:
                        data_studenty[student]['Věk'] = vek
                        vek_label.config(text=f'Let: {vek}')
                        save()
                        close_extra_okno(extra_okno2)

            extra_okno2 = open_new_extra_okno('Změnit věk',400,400)
            tk.Label(extra_okno2,text='Zadejte věk',font=('Arial',20)).place(x=200,y=100,anchor='center')
            vstup_vek = tk.Entry(extra_okno2,justify='center',font=('Arial',20))
            vstup_vek.place(x=200,y=160,anchor='center',width=300,height=50)
            upozorneni = tk.Label(extra_okno2, text='', font=('Arial',16))
            upozorneni.place(x=200,y=310,anchor='center')
            button = tk.Button(extra_okno2,text='Změnit',font=('Arial',18),command=zmenit_vek)
            button.place(x=200,y=360,anchor='center',width=300,height=50)

        i = seznam.curselection()
        student = seznam.get(i)
        if student:
            extra_okno = open_new_extra_okno('Informace žaka',400,560)
            tk.Label(extra_okno,text=f'Student/ka: {student}',font=('Arial',15)).place(x=200,y=25,anchor='center')
            vek_label = tk.Label(extra_okno,text=f'Let: {data_studenty[student]['Věk']}',font=('Arial',15))
            vek_label.place(x=200,y=50,anchor='center')
            labels = radek_label(data_predmety, extra_okno,200,100)
            hotovo = tk.Button(extra_okno,text='Hotovo',font=('Arial',18),command=button_hotovo)
            hotovo.place(x=300,y=500,anchor='center',width=150,height=50)
            zmenit_vek = tk.Button(extra_okno,text='Změňit věk',font=('Arial',18),command=button_zmenit_vek)
            zmenit_vek.place(x=100,y=500,anchor='center',width=150,height=50)
            try:
                for label in labels:
                    try:
                        prumer_znamky = prumer(data_studenty[student][data_predmety[labels.index(label)]])
                    except KeyError:
                        prumer_znamky = '-'
                    label.config(text=f'{data_predmety[labels.index(label)]}: {prumer_znamky}')
            except TypeError:
                return

    def button_zobrazit_prumer_tridy():
        global otazka
        global extra_okno
        global extra_okno2
        close_extra_okno(otazka)
        close_extra_okno(extra_okno)
        close_extra_okno(extra_okno2)
        def hotovo():
            close_extra_okno(extra_okno)
        extra_okno = open_new_extra_okno('Pruměr třidy',400,600)
        tk.Label(extra_okno,text='Pruměr třidy',font=('Arial',22)).place(x=200,y=40,anchor='center')
        labels = radek_label(data_predmety,extra_okno,200,100)
        pole_pro_celi_prumer = []
        tk.Label(extra_okno,text=f'Pruměr celkem: {prumer(pole_pro_celi_prumer)}',font=('Arial',22)).place(anchor='center',x=200,y=475)
        button = tk.Button(extra_okno,text='Hotovo',font=('Arial',16),command=hotovo)
        button.place(x=200,y=550,anchor='center',width=300,height=50)
        try:
            for label in labels:
                predmet_index = labels.index(label)
                predmet = data_predmety[predmet_index]
                pole_pro_prumer = []
                for student in data_studenty:
                    try:
                        pole_pro_prumer += data_studenty[student][predmet]
                        pole_pro_celi_prumer += data_studenty[student][predmet]
                    except KeyError:
                        continue
                label.config(text=f'{predmet}: {prumer(pole_pro_prumer)}')
        except TypeError:
            return

    global hlv_okno
    global seznam
    hlv_okno = tk.Tk()
    hlv_okno.title('Spravce znamek třidy')
    vycentruj_okno(hlv_okno, 800, 800)

    seznam = tk.Listbox(hlv_okno,font=('Arial',17),height=28,width=31,justify='center')
    seznam.place(x=10,y=10)
    seznam_zaplneni(seznam, data_studenty)

    ukoncit = tk.Button(hlv_okno,text='Ukončit',font=('Arial',16),height=1,width=26,command=hlv_close)
    ukoncit.place(x=440, y=20)

    pridat_studenta = tk.Button(hlv_okno,text='Přidat studenta',font=('Arial',16),height=1,width=26,command=button_pridat_studenta)
    pridat_studenta.place(x=440,y=130)
    smazat_studenta = tk.Button(hlv_okno,text='Smazat studenta',font=('Arial',16),height=1,width=26,command=button_smazat_studenta)
    smazat_studenta.place(x=440, y=190)
    nastavit_znamku = tk.Button(hlv_okno,text='Nastavit znamky',font=('Arial',16),height=1,width=26,command=button_nastavit_znamky)
    nastavit_znamku.place(x=440, y=250)
    nastavit_predmety = tk.Button(hlv_okno,text='Nastavit předměty',font=('Arial',16),height=1,width=26,command=button_nastavit_predmety)
    nastavit_predmety.place(x=440, y=310)
    zobrazit_info = tk.Button(hlv_okno,text='Zobrazit info',font=('Arial',16),height=1,width=26,command=button_zobrazit_info)
    zobrazit_info.place(x=440, y=370)
    zobrazit_prumer_tridy = tk.Button(hlv_okno,text='Zobrazit pruměr třidy',font=('Arial',16),height=1,width=26,command=button_zobrazit_prumer_tridy)
    zobrazit_prumer_tridy.place(x=440, y=430)
    
    tk.Label(hlv_okno, text='Info třídy:',font=('Arial',20)).place(x=600, y=520,anchor='center')
    tk.Label(hlv_okno, text='Jmeno třidniho učitele:',font=('Arial',16)).place(x=600, y=570, anchor='center')
    jmeno = tk.Label(hlv_okno, text=ucitel, font=('Arial',16))
    jmeno.place(x=600, y=600, anchor='center')
    jmeno_trida = tk.Label(hlv_okno, text=f'Třida: {trida}', font=('Arial',16))
    jmeno_trida.place(x=600, y=640, anchor='center')
    pocet_zaku = tk.Label(hlv_okno, text=f'Počet žaku: {seznam.size()}', font=('Arial',16))
    pocet_zaku.place(x=600, y=680, anchor='center')
    pocet_predmetu = tk.Label(hlv_okno, text=f'Počet předmětu: {len(data_predmety)}', font=('Arial',16))
    pocet_predmetu.place(x=600, y=720, anchor='center')

    hlv_okno.mainloop()

start_okno.mainloop()