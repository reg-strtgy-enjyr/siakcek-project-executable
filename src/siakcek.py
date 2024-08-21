from bs4 import BeautifulSoup
import kurikulum
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

def processData(soup, SKSTransfer, process_type):
    table = soup.find("table", {"class": "box"})
    studentData = soup.find("h3").text.split(' - ')
    studentName = studentData[1]
    NPM = studentData[0]
    prodi = soup.find("strong").text.split(' ')[-2]
    sks_t = 0
    if prodi == "Komputer":
        k16s = kurikulum.k16s_tekkom
        k20s = kurikulum.k20s_tekkom
        k24s = kurikulum.k24s_tekkom
        sks24 = kurikulum.sks24_tekkom
    elif prodi == "Elektro":
        k16s = kurikulum.k16s_tekkom
        k20s = kurikulum.k20s_elektro
        k24s = kurikulum.k24s_elektro
        sks24 = kurikulum.sks24_elektro
    elif prodi == "Biomedik":
        k16s = kurikulum.k16s_tekkom
        k20s = kurikulum.k20s_biomed
        k24s = kurikulum.k24s_biomed
        sks24 = kurikulum.sks24_biomed

    angkatan = int(NPM[:2])
    
    try:
        if (angkatan < 20):
            kw = kurikulum.k16w_tekkom
            # kp = kurikulum.k16p
            # ks = kurikulum.k16s
            # khapus = kurikulum.k16h
            kur = '2016'
        elif (angkatan < 24):
            if prodi == "Komputer":
                kw = kurikulum.k20w_tekkom
            elif prodi == "Elektro":
                kw = kurikulum.k20w_elektro
            elif prodi == "Biomedik":
                kw = kurikulum.k20w_biomed
            elektronika = kurikulum.k20m_elektronika
            listrik = kurikulum.k20m_listrik
            telkom = kurikulum.k20m_telkom
            kendali = kurikulum.k20m_kendali
            # kp = kurikulum.k20p
            # ks = kurikulum.k20s
            # khapus = kurikulum.k16h
            kur = '2020'
        else:
            if prodi == "Komputer":
                kw = kurikulum.k24w_tekkom
            elif prodi == "Elektro":
                kw = kurikulum.k24w_elektro
            elif prodi == "Biomedik":
                kw = kurikulum.k24w_biomed
            elektronika = kurikulum.k24m_elektronika
            listrik = kurikulum.k24m_listrik
            telkom = kurikulum.k24m_telkom
            kendali = kurikulum.k24m_kendali
            # kp = kurikulum.k24p
            # ks = kurikulum.k24s
            # khapus = kurikulum.k16h
            kur = '2024'
    except TypeError:
        pass
    matkul_taken = []
    i = 0
    j = 0
    skip_data = ["Tahun Ajaran", "Disetujui", "detail", "Menunggu persetujuan"]
    agama_list = ["Islam", "Kristen", "Katolik", "Buddha", "Hindu"]
    matkul_code = ''
    matkul_name = ''
    matkul_type = ''
    matkul_sks = 0
    matkul_done = []
    sks_done_w = []
    sks_done_p = []
    sks_available = []
    if SKSTransfer != None:
        sks_t = SKSTransfer[0]
        try:
            SKSTransfer[1] = k20s[SKSTransfer[1]]
        except KeyError:
            pass
        matkul_done.append(SKSTransfer[1])
    for row in table.findAll("td"):
        if any([x in row.text for x in skip_data]):
            # print(row.text + ("(removed)"))
            continue
        table_content = row.text
        i += 1
        j += 1
        if table_content == 'Empty':
            j += 1
        if j == 9:
            j -= 8
        # print(table_content + f"({j})")
        # match j:
        if j == 2:
            matkul_code = table_content
        elif j == 4:
            if any([x in table_content for x in agama_list]):
                table_content = "Agama"
            if "MPK Olahraga" in table_content:
                table_content = "MPK Olahraga/Seni"
            if "MPK Seni" in table_content:
                table_content = "MPK Olahraga/Seni"
            if angkatan < 20:
                try:
                    table_content = k16s[table_content]
                except KeyError:
                    pass
            elif angkatan < 24:
                try:
                    table_content = k20s[table_content]
                except KeyError:
                    pass
            matkul_name = table_content
            if any([x in table_content for x in kw]):
                matkul_type = 'wajib'
            else:
                matkul_type = 'pilihan'

        elif j == 6:
            try:
                table_content = int(row.text)
            except ValueError:
                pass
            matkul_sks = table_content
        elif j == 8:
            matkul_score = table_content
            # match matkul_score:
            if ((matkul_score == 'A') or (matkul_score == 'A-') or (matkul_score == 'B+') or(matkul_score == 'B')or(matkul_score == 'B-')or(matkul_score == 'C+')or(matkul_score == 'C')or(matkul_score == 'TK')):
            # if set(matkul_score).intersection(set(nilai_lulus)):
                # print(matkul_score)
                matkul_status = 'lulus'
                matkul_taken.insert(i, (
                    matkul_code, matkul_name, matkul_score, matkul_sks, matkul_type, matkul_status))

                matkul_done.append(matkul_name)                
                if matkul_type == 'wajib':
                    sks_done_w.append(matkul_sks)
                else:
                    sks_done_p.append(matkul_sks)
            else:
                # print("belum lulus")
                matkul_status = 'belum lulus'
                matkul_taken.insert(i, (
                    matkul_code, matkul_name, matkul_score, matkul_sks, matkul_type, matkul_status))
    matkul_needed = list(set(kw) - set(matkul_done))
    if(angkatan < 24):
        if prodi == 'Komputer':
            if "Probabilitas dan Proses Stokastik" in matkul_done:
                if not (("Praktikum Fisika Mekanika dan Panas" in matkul_done) or ("Prak. Fisika Mekanika dan Panas" in matkul_done)):
                    matkul_needed.append("Praktikum Fisika Mekanika dan Panas")
        elif prodi == 'Elektro':
            if "Fisika Semikonduktor" not in matkul_done:
                if "Matematika Diskrit" not in matkul_done:
                    matkul_needed.append("Matematika Diskrit")
            try:
                matkul_needed.remove("Praktikum Fisika Mekanika dan Panas")
            except ValueError:
                pass
            try:
                matkul_needed.remove("Praktikum Sistem Benam")
            except ValueError:
                pass
        elif prodi == 'Biomedik':
            if not(("Pengantar Instrumentasi Biomedik" in matkul_done) and ("Standar Regulasi Teknik Biomedik" in matkul_done)):
                if "Manajemen Alat Kesehatan" not in matkul_done:
                    matkul_needed.append("Manajemen Alat Kesehatan")
                try:
                    matkul_needed.remove("Pengantar Instrumentasi Biomedik")
                except ValueError:
                    pass
                try:
                    matkul_needed.remove("Standar Regulasi Teknik Biomedik")
                except ValueError:
                    pass
            if not(("Teori Medan Elektromagnetika" in matkul_done) and ("Divais Medis Sistem RF dan Microwave" in matkul_done)):
                if "Elektromagnetika dan Perancangan Divais RF Medis" not in matkul_done:
                    matkul_needed.append("Elektromagnetika dan Perancangan Divais RF Medis")
                try:
                    matkul_needed.remove("Teori Medan Elektromagnetika")
                except ValueError:
                    pass
                try:
                    matkul_needed.remove("Divais Medis Sistem RF dan Microwave")
                except ValueError:
                    pass
    if angkatan < 20:
        if not(("MPKT A" in matkul_done) and ("MPKT B" in matkul_done)):
            if "MPKT" not in matkul_done:
                matkul_needed.append("MPKT")
            try:
                matkul_needed.remove("MPKT A")
            except ValueError:
                pass
            try:
                matkul_needed.remove("MPKT B")
            except ValueError:
                pass
        if "Manajemen Proyek Teknologi Informasi" not in matkul_done:
            matkul_needed.append("Desain Proyek Teknik Komputer 1")
            matkul_needed.append("Desain Proyek Teknik Komputer 2")
            matkul_needed.remove("Manajemen Proyek Teknologi Informasi")
    # matkul_needed = list(set(kw) - set(khapus) - set(matkul_done) )
    # for x in matkul_done:
    #     print(x)
    try:
        penyetaraan = []
        for x in matkul_needed:
            try:
                x = k24s[x]
            except KeyError:
                pass
            # print(f"{x} - {sks24[x]}")
            sks_available.append(sks24[x])
            penyetaraan.append(x)
        matkul_needed = penyetaraan
    except:
        pass
    # print(f"total : {sum(sks_available)}")
    if prodi == 'Elektro':
        penyetaraan = []
        sks_elek = []
        elek_needed = list(set(elektronika) - set(matkul_done))
        for x in elek_needed:
            try:
                x = k24s[x]
            except KeyError:
                pass
            # print(f"{x} - {sks24[x]}")
            sks_elek.append(sks24[x])
            penyetaraan.append(x)
        elek_needed = penyetaraan
        penyetaraan = []
        sks_listrik = []
        listrik_needed = list(set(listrik) - set(matkul_done))
        for x in listrik_needed:
            try:
                x = k24s[x]
            except KeyError:
                pass
            # print(f"{x} - {sks24[x]}")
            sks_listrik.append(sks24[x])
            penyetaraan.append(x)
        listrik_needed = penyetaraan
        penyetaraan = []
        sks_telkom = []
        telkom_needed = list(set(telkom) - set(matkul_done))
        for x in telkom_needed:
            try:
                x = k24s[x]
            except KeyError:
                pass
            # print(f"{x} - {sks24[x]}")
            sks_telkom.append(sks24[x])
            penyetaraan.append(x)
        telkom_needed = penyetaraan
        penyetaraan = []
        sks_kendali = []
        kendali_needed = list(set(kendali) - set(matkul_done))
        for x in kendali_needed:
            try:
                x = k24s[x]
            except KeyError:
                pass
            # print(f"{x} - {sks24[x]}")
            sks_kendali.append(sks24[x])
            penyetaraan.append(x)
        kendali_needed = penyetaraan
    # matkul_pilihan = list(set(kp) - set(matkul_done))
    resultWindow = tk.Toplevel(root)
    resultWindow.geometry('600x400')
    resultWindow.title("Result Window")
    nameLabel = tk.Label(resultWindow, text=studentName, justify='center')
    nameLabel.pack(pady=5)
    infoLabel = tk.Label(resultWindow, text=f"Teknik {prodi} - Kurikulum {kur}", justify='center')
    infoLabel.pack(pady=10)
    processLabel = tk.Label(resultWindow, text=process_type, justify='left')
    processLabel.pack(pady=5)
    dataSKSFrame = tk.Frame(resultWindow)
    dataSKSFrame.pack(pady=10)
    totalDone = tk.Label(dataSKSFrame, text=f"Total SKS diperoleh: {sum(sks_done_w) + sum(sks_done_p) + sks_t}")
    totalDone.pack()
    wajibDone = tk.Label(dataSKSFrame, text=f"SKS wajib diperoleh: {sum(sks_done_w)}", anchor='w')
    wajibDone.pack()
    pilihanDone = tk.Label(dataSKSFrame, text=f"SKS pilihan diperoleh: {sum(sks_done_p)}", justify='left')
    pilihanDone.pack()
    transferSKS = tk.Label(dataSKSFrame, text=f"SKS transfer diperoleh: {sks_t}", justify='left')
    transferSKS.pack()
    neededFrame = tk.Frame(resultWindow)
    neededFrame.pack()
    neededLabel = tk.Label(neededFrame, text="Mata Kuliah Wajib yang dibutuhkan:", justify='left')
    neededLabel.pack()
    for x in matkul_needed:
        tk.Label(neededFrame, text=x, justify='left').pack()
    sisaSKS = tk.Label(neededFrame, 
                       text=f"Total SKS yang dibutuhkan: {sum(sks_available)} wajib + {144 - (sum(sks_done_w) + sum(sks_done_p) + sks_t) - sum(sks_available)} pilihan")
    sisaSKS.pack()
    if prodi == "Elektro":
        peminatanFrame = tk.Frame(resultWindow)
        peminatanFrame.pack()
        elektronikaFrame = tk.Frame(peminatanFrame)
        elektronikaFrame.pack()
        elektronikaLabel = tk.Label(elektronikaFrame, text="Mata Kuliah Peminatan Elektronika yang dibutuhkan:")
        elektronikaLabel.pack()
        for x in elek_needed:
            tk.Label(elektronikaFrame, text=x, justify='left').pack()
        elektronikaSKS = tk.Label(elektronikaFrame, text=f"Total SKS: {sum(sks_elek)}")
        elektronikaSKS.pack()
        listrikFrame = tk.Frame(peminatanFrame)
        listrikFrame.pack()
        listrikLabel = tk.Label(listrikFrame, text="Mata Kuliah Peminatan Tenaga Listrik yang dibutuhkan:")
        listrikLabel.pack()
        for x in listrik_needed:
            tk.Label(listrikFrame, text=x, justify='left').pack()
        listrikSKS = tk.Label(listrikFrame, text=f"Total SKS: {sum(sks_listrik)}")
        listrikSKS.pack()
        telkomFrame = tk.Frame(peminatanFrame)
        telkomFrame.pack()
        telkomLabel = tk.Label(telkomFrame, text="Mata Kuliah Peminatan Telekomunikasi yang dibutuhkan:")
        telkomLabel.pack()
        for x in telkom_needed:
            tk.Label(telkomFrame, text=x, justify='left').pack()
        telkomSKS = tk.Label(telkomFrame, text=f"Total SKS: {sum(sks_telkom)}")
        telkomSKS.pack()
        kendaliFrame = tk.Frame(peminatanFrame)
        kendaliFrame.pack()
        kendaliLabel = tk.Label(kendaliFrame, text="Mata Kuliah Peminatan Kendali yang dibutuhkan:")
        kendaliLabel.pack()
        for x in kendali_needed:
            tk.Label(kendaliFrame, text=x, justify='left').pack()
        kendaliSKS = tk.Label(kendaliFrame, text=f"Total SKS: {sum(sks_kendali)}")
        kendaliSKS.pack()

def submit(event):
    try:
        soup = BeautifulSoup(htmlFile, features="lxml")
        process_type = ("---data from uploaded source---")
        if transfer.get() == 1:
            transferSKS = [ transferPilihan.get(), transferMatkul.get() ]
            if transferSKS[0] == '':
                transferSKS[0] = 0
            else:
                try:
                    transferSKS[0] = int(transferSKS[0])
                except ValueError:
                    mb.showError(title="Error found", message="Nilai SKS Pilihan yang dimasukkan tidak tepat")
                    return
        else:
            transferSKS = None
        processData(soup,transferSKS,process_type)
    except (IndexError,AttributeError):
        mb.showerror(title="Error found", message="File HTML tidak valid")

def openFile(event):
    global htmlFile
    filePath = fd.askopenfilename(title="Select a HTML File", filetypes =[('HTML Files', '*.html *.htm')])
    selectedFile.config(text=filePath)
    if filePath:
        with open(filePath, 'r') as file:
            htmlFile = file.read()

def transferState():
    global transfer
    if transfer.get() == 0:
        transferFrame.pack_forget()
    else:
        transferFrame.pack()
    submitButton.pack_forget()
    submitButton.pack()

htmlFile = None
root = tk.Tk()
root.geometry('720x240')
root.title("SIAKCEK - Window Utama")
uploadframe = tk.Frame(root)
uploadframe.pack()

header1 = tk.Label(uploadframe, text="Cek via upload file riwayat berdasarkan term", justify='center')
header1.pack(side='top')
selectedFile = tk.Label(uploadframe, text="No file selected yet", justify='center')
selectedFile.pack(side='top')
fileButton = tk.Button(uploadframe, text='Browse')
fileButton.bind('<Button-1>', openFile)
fileButton.pack(side='top')

transfer = tk.IntVar()
checkTransfer = tk.Checkbutton(root, text="Transfer SKS", variable=transfer, onvalue=1, offvalue=0, command=transferState)
checkTransfer.pack()
transferFrame = tk.Frame(root)
header2 = tk.Label(transferFrame, text="Spesifikan transfer SKS jika ada", justify='center')
header2.grid(row=0, columnspan=2)
transferPilihan = tk.StringVar()
transferMatkul = tk.StringVar()
transferLabel1 = tk.Label(transferFrame, text="Transfer SKS Pilihan*", justify='left')
transferEntry1 = tk.Entry(transferFrame, textvariable=transferPilihan, justify='left')
transferLabel2 = tk.Label(transferFrame, text="Transfer Mata Kuliah**", justify='left')
transferEntry2 = tk.Entry(transferFrame, textvariable=transferMatkul, justify='left')
note1 = tk.Label(transferFrame, text="  * Isi dengan jumlah SKS yang dikonversi sebagai SKS pilihan", justify='left')
note2 = tk.Label(transferFrame, text=" ** Isi dengan nama mata kuliah yang dikonversi, sesuai dengan yang ditentukan pada sistem SIAK", justify='left')
transferLabel1.grid(row=1, column=0)
transferEntry1.grid(row=1, column=1)
transferLabel2.grid(row=2, column=0)
transferEntry2.grid(row=2, column=1)
note1.grid(row=3, columnspan=2)
note2.grid(row=4, columnspan=2)

submitButton = tk.Button(root, text="Submit")
submitButton.bind('<Button-1>', submit)
submitButton.pack()

root.mainloop()