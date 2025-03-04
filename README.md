AI Trading Bot
Versione: v1.2.0

Descrizione
AI Trading Bot è un bot di trading automatizzato che utilizza l'intelligenza artificiale e algoritmi avanzati per eseguire operazioni sul mercato delle criptovalute tramite l'exchange KuCoin. Il bot è progettato per analizzare i dati di mercato in tempo reale, calcolare indicatori tecnici e prendere decisioni di trading informate.

Caratteristiche Principali:

Integrazione con KuCoin: Utilizza le API ufficiali per operazioni di trading sicure.

Modalità Paper Trading: Simula operazioni per testare strategie senza rischi finanziari.

Interfaccia Grafica (GUI): Controlla comodamente il bot e le sue impostazioni.

Indicatori Tecnici: Calcola SMA, EMA, RSI e altri indicatori per analisi avanzate.

Modello di AI: Integra un modello di machine learning per previsioni di mercato.

Gestione dei Dati: Archivia le operazioni effettuate per analisi storiche.

Requisiti di Sistema
Python 3.7 o superiore

Ambiente Virtuale (consigliato)

Dipendenze Python (elencate in requirements.txt)

Installazione
1. Clona il Repository
bash
git clone https://github.com/tuo-utente/ai_trading_bot.git
cd ai_trading_bot
2. Crea un Ambiente Virtuale
bash
python -m venv venv
3. Attiva l'Ambiente Virtuale
Windows:

bash
venv\Scripts\activate
Mac/Linux:

bash
source venv/bin/activate
4. Installa le Dipendenze
bash
pip install -r requirements.txt
5. Configura le Chiavi API di KuCoin
Crea un account su KuCoin.

Accedi alla sezione API Management e crea delle API keys (consigliato utilizzare l'API Sandbox per il paper trading).

Rinomina il file .env.example in .env e inserisci le tue chiavi API:

KUCOIN_API_KEY=la_tua_api_key
KUCOIN_API_SECRET=il_tuo_api_secret
KUCOIN_API_PASSPHRASE=la_tua_api_passphrase
Utilizzo
Esegui il Bot da Linea di Comando
bash
python src/main.py
Avvia l'Interfaccia Grafica
bash
python src/gui.py
Utilizza lo switch nell'interfaccia per attivare o disattivare la modalità Paper Trading.

Premi "Avvia Bot" per iniziare le operazioni.
