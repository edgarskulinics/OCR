# 📄 PDF Vision Pro: Uzlabots OCR un PDF apstrādes rīks


**PDF Vision Pro** ir jaudīga un daudzfunkcionāla darbvirsmas lietojumprogramma, kas izstrādāta ar Python, izmantojot `tkinter` un `ttkbootstrap` bibliotēkas, lai nodrošinātu intuitīvu un modernu lietotāja saskarni. Tā piedāvā plašu attēlu apstrādes, optiskās rakstzīmju atpazīšanas (OCR) un PDF pārvaldības rīku klāstu, padarot to par ideālu risinājumu dokumentu digitalizēšanai un organizēšanai.

Šī lietojumprogramma ir paredzēta gan individuāliem lietotājiem, gan maziem uzņēmumiem, kuriem nepieciešams efektīvi apstrādāt skenētus dokumentus, attēlus un PDF failus, izvilkt tekstu, uzlabot attēlu kvalitāti un pārvaldīt dokumentu arhīvu.

## ✨ Galvenās Iespējas

*   **Uzlabota OCR funkcionalitāte:** Izmanto Tesseract OCR dzinēju ar pielāgojamiem parametriem (DPI, PSM, OEM, valodas) precīzai teksta atpazīšanai no attēliem un PDF.
*   **Daudzvalodu atbalsts:** Atbalsta vairākas OCR valodas, tostarp latviešu, angļu, krievu, vācu, franču, spāņu, itāļu, lietuviešu un igauņu.
*   **Visaptveroša attēlu apstrāde:**
    *   Spilgtuma, kontrasta, asuma, gamma korekcija.
    *   Pelēktoņu, binārizācijas, malu noteikšanas, trokšņu samazināšanas filtri.
    *   Attēla rotācija, spoguļošana, apgriešana un izmēru maiņa.
    *   **AI-darbināta dokumentu detekcija:** Automātiska dokumentu robežu noteikšana un perspektīvas korekcija no attēliem vai kameras plūsmas.
    *   **Krāsu balstīta detekcija:** Uzlabota dokumentu atpazīšana, izmantojot mērķa krāsu un toleranci.
    *   **Automātiska attēla uzlabošana:** Optimizē attēla iestatījumus (spilgtums, kontrasts, gamma), lai iegūtu labākos OCR rezultātus.
    *   **QR koda/Svītrkoda rāmja rediģēšana:** Iespēja definēt apgabalu, kurā atrodas QR kods vai svītrkods, lai uzlabotu atpazīšanu.
*   **Kameras skenēšana:** Tieša dokumentu skenēšana, izmantojot pievienotu kameru, ar reāllaika priekšskatījumu un automātisku dokumentu robežu detekciju.
*   **PDF pārvaldība:**
    *   PDF failu ielāde un priekšskatīšana lapu pa lapai.
    *   PDF sadalīšana atsevišķās lapās.
    *   PDF šifrēšana/atšifrēšana ar paroli.
    *   PDF paroles maiņa.
    *   Meklējama teksta iekļaušana PDF izvades failos.
    *   Pielāgojami PDF izvades iestatījumi (kvalitāte, lapas izmērs, fonts).
    *   **ID koda pievienošana:** Iespēja pievienot QR kodus vai svītrkodus (Code 128, Code 39, EAN-13) PDF dokumentiem ar pielāgojamu pozīciju.
*   **Iekšējā failu sistēma:** Hierarhiska mapju struktūra dokumentu organizēšanai lietotnes iekšienē.
*   **Integrācija ar Google Drive un Sheets:** Automātiska PDF augšupielāde Google Drive un metadatu sinhronizācija ar Google Sheets.
*   **E-pasta sūtīšana:** Iespēja nosūtīt apstrādātos PDF failus pa e-pastu tieši no lietotnes.
*   **Automatizēta mapju uzraudzība:** Automātiska jaunu failu apstrāde no uzraudzītām mapēm.
*   **Lietotāja saskarne:**
    *   Intuitīva un responsīva GUI, izmantojot `ttkbootstrap` tēmas.
    *   Pilnekrāna attēlu skatītājs ar tālummaiņu un pārvietošanu.
    *   Ielādes ekrāns ar modernu dizainu.
    *   Pielāgojami vispārīgie un skenēšanas iestatījumi.
    *   Iestatījumu vēsture automātiskai un manuālai attēlu uzlabošanai.
    *   Failu asociācija ar `.pdf` failiem Windows sistēmās.

## 🚀 Pilnīga Funkcionalitāte: Visas Iespējas un Sadaļas

Šī sadaļa sniedz pilnīgu pārskatu par visām pieejamajām funkcijām, sadalītu pa galvenajām cilnēm un apakšsadaļām. Katra funkcija ir aprakstīta ar tās mērķi, kā to izmantot un saistītajiem parametriem vai ierobežojumiem.

### 1. **Attēlu Apstrādes Cilne** (Galvenā darbības zona attēlu un OCR apstrādei)

Šī cilne ir veltīta attēlu ielādei, uzlabošanai, OCR apstrādei un PDF ģenerēšanai. Tā ir sadalīta trīs galvenajās zonās: augšējā rīkjosla, kreisā puse (failu saraksts un OCR kontroles) un labā puse (attēla priekšskatījums un apstrādes rīki).

#### **Augšējā Rīkjosla (Toolbar)**
- **Atvērt attēlus/PDF**: Atver failu dialogu, lai ielādētu attēlus (JPG, PNG, TIFF, BMP) vai PDF failus. Atbalsta vairāku failu atlasi. Ielādētie faili parādās failu sarakstā pa kreisi. PDF faili tiek apstrādāti lapu pa lapai.
- **Skenēt ar kameru**: Inicializē kameru (izmantojot OpenCV) un atver reāllaika skenēšanas logu. Atbalsta kameras indeksa maiņu (0, 1, 2 utt.), automātisku dokumentu detekciju, attēla uzlabojumus (spilgtums, kontrasts, gamma) un saglabāšanu kā jaunu attēlu sarakstā. Iespējama krāsu balstīta detekcija (mērķa krāsa un tolerance). Automātiska saglabāšana ar laika zīmi (piem., "Skenēts_dokuments_20231201_143022").
- **Atlasīt dokumentu no attēla**: Atver pilnekrāna logu ar atlasīto attēlu, kur var manuāli vai automātiski (izmantojot Canny malu detekciju, adaptīvo sliekšņošanu un kontūru analīzi) noteikt dokumenta robežas. Atbalsta perspektīvas korekciju (four_point_transform), stūru vilkšanu ar peli, tālummaiņu (pelē rullītis), pārvietošanu (vidējā peles poga) un saglabāšanu kā apstrādātu attēlu.
- **Vispārīgie Iestatījumi**: Atver konfigurācijas logu ar cilnēm (Vispārīgi, OCR, PDF, E-pasts). Skatīt sadaļu "Iestatījumi" zemāk.
- **Skenēšanas Iestatījumi**: Atver specializētu logu kameras un detekcijas parametriem (kamera indekss, izšķirtspēja, kontūra minimālais laukums, aspekta attiecība, Gausa kodols, adaptīvā sliekšņošana, Canny sliekšņi, morfoloģija, malu dilatācija).
- **Pārbaudīt valodas**: Pārbauda Tesseract valodu pakotnes un parāda pieejamās valodas. Brīdinājums, ja valoda nav instalēta.

#### **OCR Parametri (Toolbar beigās)**
- **DPI**: Spinbox (70-600), ietekmē attēla izšķirtspēju OCR procesā (augstāks DPI = precīzāks, bet lēnāks).
- **Fonts**: Spinbox (5-20), fonta izmērs meklējamam tekstam PDF izvadē.
- **Konfidence**: Spinbox (0-100), minimālā OCR konfidences līmenis tekstam.
- **PSM**: Spinbox (0-13), Page Segmentation Mode (piem., 3 = pilnīgi automātisks, 6 = vienskaitļa bloks).
- **OEM**: Spinbox (0-3), OCR Engine Mode (0 = tikai LSTM, 1 = tikai legacy, 3 = abas).
- **Orientācija**: Combobox (Auto, Portrets, Ainava, A4 Portrets utt.), PDF lapas orientācija.
- **Iekļaut meklējamu tekstu**: Checkbutton, pievieno OCR tekstu kā slāni PDF failā.

#### **Kreisā Puse: Failu Saraksts un OCR Kontroles**
- **Failu saraksts (Listbox)**: Rāda ielādētos failus ar vairāku atlasi (EXTENDED). Bindings: atlase parāda priekšskatījumu, dubultklikšķis atver pilnekrāna skatītāju, labais klikšķis parāda konteksta izvēlni (dzēst, pārdēvēt utt.).
- **Kārtošanas pogas**: "↑ Uz augšu" un "↓ Uz leju" pārvieto atlasīto failu sarakstā.
- **OCR Progresu Josla**: Rāda OCR apstrādes progresu (0-100%).
- **Sākt OCR**: Apstrādā atlasītos failus ar Tesseract, izmantojot atlasītās valodas un parametrus. Rezultāts parādās teksta laukā pa labi. Atbalsta daudzvalodu OCR (piem., "lav+eng+rus").
- **Apturēt**: Aptur OCR procesu, ja tas ir aktīvs.
- **Dzēst atlasīto**: Dzēš atlasītos failus no saraksta (ne dzēš fiziski no diska).

#### **Labā Puse: Attēla Priekšskatījums un Apstrādes Rīki**
- **Priekšskatījuma Kanvas**: Rāda atlasītā faila priekšskatījumu ar tālummaiņu (pelē rullītis), pārvietošanu (vidējā poga), atlasi (kreisā poga vilkšanai).
- **Attēlu Apstrādes Rīki (Scrollable Frame)**:
  - **Slīdņi**: Spilgtums (0.1-3.0), Kontrasts (0.1-3.0), Asums (2.0-3.5), Rotācija (-360 līdz 360, pa 90°).
  - **Checkbuttoni**: Pelēktoņi, Slīpuma korekcija (izmanto OpenCV deskew), Trokšņu samazināšana, Attēla negatīvs, Malu noteikšana, Binārizācija. Katrs maina priekšskatījumu reāllaikā.
  - **Pogas**:
    - **Apgriezt attēlu (vilkt)**: Ieslēdz režīmu, kur ar peli var atlasīt taisnstūri un apgriezt attēlu.
    - **Rediģēt koda rāmi**: Ieslēdz QR/svītrkoda rāmja rediģēšanu (vilkšana, izmēru maiņa).
    - **Pagriezt par 90°**: Rotē attēlu par 90° pulksteņrādītāja virzienā.
    - **Spoguļot (Horiz./Vert.)**: Spoguļo attēlu horizontāli vai vertikāli.
    - **Mainīt izmērus**: Atver dialogu, lai ievadītu jaunu izmēru (procentuāli vai pikseļos).
    - **Auto uzlabošana**: Automātiski optimizē attēlu, izmantojot histogramu un kontrastu.
    - **Rādīt histogrammu**: Atver logu ar RGB kanālu histogrammām.
    - **Rādīt metadatus**: Parāda EXIF metadatus (datums, kamera utt.).
    - **Rādīt krāsu paleti**: Izvelk dominējošās krāsas un parāda paleti.
    - **Atvērt pilnekrāna priekšskatījumu**: Atver pilnekrāna skatītāju ar tālummaiņu un atlasi.
- **OCR Rezultātu Lauks (Text Widget)**: Rediģējams teksta logs ar ritjoslu, kur parādās OCR izvilktais teksts. Var rediģēt manuāli pirms PDF saglabāšanas.

### 2. **Failu Pārvaldības Cilne** (Dokumentu arhīva organizēšana)

Šī cilne ļauj pārvaldīt saglabātos PDF un attēlus iekšējā hierarhiskā sistēmā. Tā ir sadalīta zonās: meklēšana/filtrēšana, PDF priekšskatījums, failu saraksts ar navigāciju un darbību pogas.

#### **Meklēšana un Filtrēšana (Augšdaļa)**
- **Meklēt**: Ievades lauks, meklē failus pēc nosaukuma (reāllaikā, KeyRelease binding).
- **No datuma/Līdz datumam**: Datuma diapazona filtrēšana (ievades lauki + kalendāra pogas). Filtrē failus pēc izveides datuma.
- **Filtrēt**: Lieto meklēšanu un datuma filtrus, atjaunina sarakstu.
- **Notīrīt filtrus**: Atiestata visus filtrus un rāda visu saturu.

#### **PDF Priekšskatījums (Kreisā Rūts)**
- **Kanvass**: Rāda atlasītā PDF lapu ar tālummaiņu (pelē rullītis), pārvietošanu (kreisā poga vilkšanai).
- **Navigācija**: "← Iepriekšējā" / "Nākamā →" pogas pārvietojas pa lapām. Etiķete rāda "Lapa X/Y". Atbalsta zoom (0.1-5.0) un pan.

#### **Failu Saraksts un Mapju Navigācija (Vidējā Rūts)**
- **Mapju Navigācija**: "Atpakaļ" poga atgriežas vecākā mapē. "Atsvaidzināt lapu" sinhronizē ar fizisko disku. Ceļa etiķete rāda pašreizējo ceļu (piem., "Sakne > Dokumenti > 2023").
- **Failu Saraksts (tk.Text Widget)**: Rāda failus un mapes hierarhiski (ar atkāpēm). Bindings:
  - **Viens klikšķis**: Atlasa rindu, parāda priekšskatījumu.
  - **Dubultklikšķis**: Atver failu (PDF - priekšskatījums, attēls - pilnekrāns) vai ieiet mapē.
  - **Labais klikšķis**: Konteksta izvēlne (dzēst, pārdēvēt, pārvietot, e-pasts, parole, sadalīt).
  - **Ritjoslas**: Vertikāla un horizontāla ritināšana.
- **Iekrāsošana**: Atlasītā rinda ir zila (selected_line tag). Meklēšanas rezultāti dzeltenā (highlight tag).

#### **Darbību Pogas (Labā Rūts, Grid Layout)**
- **📂 Atvērt**: Atver atlasīto failu ar noklusējuma programmu (os.startfile).
- **📁 Atvērt mapē**: Atver faila direktoriju sistēmas pārlūkā.
- **🗑️ Dzēst**: Dzēš atlasītos failus/mapes (ar apstiprinājumu, fiziski no diska un arhīva).
- **📧 Nosūtīt e-pastā**: Nosūta atlasītos PDF kā pielikumus, izmantojot konfigurētos SMTP iestatījumus (ar HTML/plain tekstu).
- **➕ Izveidot mapi**: Izveido jaunu mapi pašreizējā direktorijā (ar nosaukuma ievadi).
- **➡️ Pārvietot uz...**: Pārvieto atlasītos failus uz citu mapi (ar dialogu mapju izvēlei).
- **✏️ Pārdēvēt**: Pārdēvē atlasīto failu/mapi (ar ievades dialogu).
- **📄 Saglabāt kā Word**: Eksportē PDF kā .docx (izmanto docx bibliotēku, pašlaik pamata implementācija).
- **🔒 Pievienot paroli**: Pievieno paroli PDF (izmanto pypdf, ar paroles ievadi).
- **🔓 Noņemt paroli**: Noņem paroli no PDF (ar esošās paroles ievadi, ja nepieciešams).
- **🔑 Mainīt paroli**: Maina PDF paroli (esošā + jauna).
- **✂️ Sadalīt PDF**: Sadala PDF pa lapām, katru saglabājot kā atsevišķu PDF failu ar OCR tekstu. Automātiski izveido apakšmapi (piem., "dokumenta_nosaukums_pages"), pārvieto oriģinālo PDF tur un pievieno katru lapu kā jaunu failu ar nosaukumu "dokumenta_nosaukums_page_001.pdf". Atbalsta progresu joslu un saglabāšanu iekšējā arhīvā.
- **📱 Pievienot ID kodu**: Pievieno QR kodu vai svītrkodu (Code 128, Code 39, EAN-13) PDF beigās vai sākumā, izmantojot reportlab. Pozīcijas opcijas: augšā pa kreisi/labā, apakšā pa kreisi/labā. Koda saturs: unikāls ID vai datums.
- **🔍 Meklēt tekstu PDF**: Meklē tekstu atlasītajā PDF un izceļ to priekšskatījumā (izmanto PyMuPDF meklēšanas funkciju).
- **📊 Eksportēt metadatus**: Eksportē PDF metadatus (autors, datums, lapu skaits) kā JSON vai TXT failu.
- **🔄 Sinhronizēt ar Google Drive**: Augšupielādē atlasītos failus uz Google Drive (izmanto google-api-python-client) un atjaunina metadatus Sheets.
- **📈 Atjaunināt Google Sheet**: Sinhronizē failu metadatus (nosaukums, ID, ceļš, datums, Google Drive saite) ar Google Sheets (izmanto gspread).

### 3. **Papildu Rīku Cilne** (Uzlabota attēlu analīze un apstrāde)

Šī cilne piedāvā specializētus rīkus attēlu analīzei, uzlabošanai un ģenerēšanai. Tā ir sadalīta apakšsadaļās: attēlu analīze, papildu apstrāde, QR ģenerators un PDF priekšskatījums.

#### **Attēlu Analīzes Rīki**
- **Rādīt histogrammu**: Atver logu ar RGB kanālu histogrammām (izmanto matplotlib vai PIL), lai analizētu krāsu sadalījumu un kontrastu.
- **Rādīt metadatus**: Parāda EXIF metadatus (datums, kamera, GPS, orientācija) no attēla (izmanto PIL ExifTags).
- **Rādīt krāsu paleti**: Izvelk 10 dominējošās krāsas no attēla (izmanto k-means klasterizāciju ar OpenCV) un parāda kā krāsu kvadrātus ar hex vērtībām.
- **Salīdzināt attēlus**: Salīdzina divus attēlus (atbalsta SSIM indeksu vai pikseļu atšķirības), parāda atšķirību kā siltuma karti.
- **Novērtēt kvalitāti**: Aprēķina attēla kvalitātes rādītāju (izmanto BRISQUE vai Laplacian varianci), sniedz ieteikumus uzlabojumiem.
- **Izvilkt tekstu no apgabala**: Ļauj atlasīt taisnstūri attēlā un veikt OCR tikai tajā apgabalā (izmanto PIL crop + Tesseract).

#### **Papildu Attēlu Apstrādes Rīki**
- **Krāsu konvertēšana**: Konvertē attēlu uz HSV, LAB, YUV vai pelēktoņiem (izmanto OpenCV cvtColor), ar priekšskatījumu.
- **Ūdenszīmes**: Pievieno tekstu vai attēlu kā ūdenszīmi (pozīcija, caurspīdīgums, fonts pielāgojams).
- **Mozaīkas efekts**: Pielieto pikseļu mozaīku atlasītam apgabalam (izmanto OpenCV resize + overlay).
- **Attēlu salikšana**: Apvieno vairākus attēlus (horizontāli/vertikāli vai ar overlap, izmanto OpenCV stitching).
- **Atjaunošana (Inpainting)**: Noņem traucējumus vai objektus, aizpildot ar apkārtējo tekstūru (izmanto OpenCV inpaint).
- **Stilizācija**: Pielieto mākslinieciskus filtrus (piem., eļļas glezna, skices efekts, izmanto OpenCV stilizācijas funkcijas).
- **Ģeometriskās transformācijas**: Pielieto affine, perspective vai warp transformācijas (izmanto OpenCV warpAffine/warpPerspective).
- **Kanālu izvilkšana/apvienošana**: Izvelk RGB kanālus kā atsevišķus attēlus vai apvieno vairākus attēlus kanālos.
- **Sēpijas/Vinjetes efekti**: Pielieto sēpijas toni vai vinjetes ēnojumu (izmanto OpenCV un maskas).
- **Pikselizācija**: Samazina attēla izšķirtspēju blokos, lai izveidotu pikselizētu efektu.
- **Seju noteikšana**: Atrod sejas attēlā (izmanto OpenCV Haar cascades), zīmē taisnstūrus ap tām.

#### **QR Koda Ģenerators**
- **Ģenerēt QR kodu**: Ievades lauks tekstam/URL, ģenerē QR kodu (izmanto qrcode bibliotēku), saglabā kā PNG vai pievieno PDF.
- **Ģenerēt svītrkodu**: Atbalsta Code 128, Code 39, EAN-13 (izmanto reportlab barcode), pielāgojams izmērs un krāsa.
- **Atpazīt QR/svītrkodus**: Izmanto pyzbar, lai atpazītu un atšifrētu kodus no attēla, parāda rezultātus sarakstā.

#### **PDF Priekšskatījums un Navigācija**
- **Sinhronizēts priekšskatījums**: Rāda PDF lapas no "Failu pārvaldības" cilnes atlases, ar tālummaiņu un pārvietošanu.
- **Iepriekšējā/Nākamā lapa**: Pārvietojas pa PDF lapām (izmanto PyMuPDF).
- **Lapas etiķete**: Rāda pašreizējo lapu (X/Y).
- **Atbalsts attēliem**: Ja atlasīts attēls no "Attēlu apstrādes" cilnes, rāda to kā priekšskatījumu.

### 4. **Automatizācijas Cilne** (Fonā darbojošās funkcijas)

Šī cilne ļauj konfigurēt automātiskas darbības, lai samazinātu manuālo darbu.

#### **Mapju Uzraudzība (Watchdog Integrācija)**
- **Uzraudzīt mapi**: Norāda mapi, lai automātiski apstrādātu jaunus failus (attēlus/PDF). Iespējo/izslēdz ar checkbutton.
- **Apstrādes darbības**: Automātiski veic OCR, saglabā kā PDF, augšupielādē uz Drive/Sheets. Atbalsta filtru pēc faila tipa (tikai PDF/attēli).
- **Notikumu žurnāls**: Rāda žurnālu ar apstrādātiem failiem (datums, fails, statuss: veiksmīgi/kļūda).

#### **Attālinātā Glabāšana**
- **Glabāšanas tips**: Combobox (Local, FTP, SFTP, Google Drive). Konfigurē atsevišķus laukus katram.
- **FTP/SFTP iestatījumi**: Host, Ports (21/22), Lietotājs, Parole, Attālinātais ceļš. Atbalsta SFTP ar paramiko (pēc izvēles instalācija).
- **Google Drive iestatījumi**: Mapes ID, Credentials JSON ceļš, Token JSON ceļs. Automātiska autentifikācija ar OAuth.
- **Automātiska augšupielāde**: Checkbutton, lai augšupielādētu katru jaunu PDF. Mērķis: Local (tikai saglabā), FTP, Google Drive.

#### **Google Sheets Integrācija**
- **Sheet ID**: Ievades lauks Google Sheet ID (no URL).
- **Lapas nosaukums**: Noklusējums "OCR_Failu_Saraksts", definē kolonnas (Nosaukums, ID, Ceļš, Datums, Drive Saite).
- **Credentials ceļš**: JSON faila ceļš pakalpojuma kontam.
- **Sinhronizācija**: Poga, lai atjaunotu visus failus Sheets. Automātiska pie katras saglabāšanas, ja ieslēgta.

#### **E-pasta Automatizācija**
- **Automātiska sūtīšana**: Checkbutton, lai nosūtītu PDF pa e-pastu pēc apstrādes (izmanto konfigurētos SMTP iestatījumus).
- **Saņēmēji**: Vairāki e-pasta lauki (noklusējums no iestatījumiem).

### 5. **Iestatījumu Windows** (Konfigurācijas dialogi)

#### **Vispārīgie Iestatījumi (Notebook ar cilnēm)**
- **Vispārīgi**: Tēma (Combobox ar ttkbootstrap tēmām), Saglabāšanas mape (Entry + Browse), Autentifikācija (Checkbutton).
- **OCR**: Tesseract ceļš (Entry + Browse), Valodas (Checkbuttons: Latviešu, Angļu utt.), DPI (Spinbox 70-600), Konfidence (0-100).
- **PDF**: Kvalitāte (Combobox: Zema/Vidēja/Augsta), Lapas izmērs (Combobox), Fonta izmērs (5-20), Meklējams teksts (Checkbutton), ID kods (Checkbutton + tips: QR/Barcode/Code39/EAN13, pozīcija: top_left/top_right/bottom_left/bottom_right).
- **E-pasts**: SMTP serveris/ports, Lietotājs/parole, No/Uz adreses, SSL (Checkbutton), Tēma (Entry), Plain/HTML ķermeņi (Text widgets), Pārbaudīt savienojumu (poga, testē SMTP).
- **Saglabāt/Atcelt**: Saglabā JSON failā (~/.ocr_pdf_settings.json), atjaunina mainīgos.

#### **Skenēšanas Iestatījumi (Specializēts logs)**
- **Kamera**: Indekss (Spinbox 0-10), Platums/Augstums (Spinbox 640-1920/480-1080).
- **Detekcija**: Min. kontūra laukums (1000-10000), Aspekta attiecība (min 0.4, max 2.3), Gausa kodols (3-15, nepāra), Adaptīva sliekšņošana (bloks 3-51 nepāra, C -10 līdz 10), Canny sliekšņi (0-255), Morfoloģija (Checkbutton + kodols 1-5), Malu dilatācija (0-5).
- **Uzlabojumi**: Spilgtums/Kontrasts/Satura piesātinājums (-100 līdz 100), Gamma (0.1-3.0), Krāsu detekcija (Checkbutton + krāsa Entry #FFFFFF, tolerance 1-100).
- **Automātiskā pielāgošana**: Poga, lai automātiski meklētu labākos iestatījumus (brute-force brightness/contrast/gamma, progress 0-100%, saglabā vēsturē).
- **Vēsture**: Listbox ar saglabātiem iestatījumiem (timestamp, tips: auto/manual, parametri, score). Pogām: Ielādēt, Pārdēvēt, Dzēst, Saglabāt pašreizējos (ar nosaukumu).
- **Saglabāt**: Saglabā atsevišķā JSON failā (~/.ocr_scan_settings.json).

## 🚀 Instalācija

Lai palaistu PDF Vision Pro, jums būs nepieciešams Python 3.x un dažas papildu bibliotēkas.

### 1. Python instalācija

Ja jums vēl nav instalēts Python, lejupielādējiet to no oficiālās vietnes: [python.org](https://www.python.org/downloads/). Instalācijas laikā pārliecinieties, ka atzīmējat opciju "Add Python to PATH".

### 2. Tesseract OCR dzinējs

PDF Vision Pro izmanto Tesseract OCR dzinēju. Jums tas ir jāinstalē atsevišķi.

*   **Windows:** Lejupielādējiet instalētāju no [Tesseract GitHub lapas](https://tesseract-ocr.github.io/tessdoc/Downloads.html). Instalācijas laikā pārliecinieties, ka atzīmējat opciju "Add to PATH" un instalējat nepieciešamās valodu pakotnes (piemēram, `lat`, `eng`, `rus`).
*   **macOS:** `brew install tesseract`
*   **Linux (Ubuntu/Debian):** `sudo apt install tesseract-ocr`

Pēc instalēšanas, iespējams, būs jānorāda Tesseract izpildāmā faila ceļš lietotnes iestatījumos.
