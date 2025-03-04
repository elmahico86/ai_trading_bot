# **AI Trading Bot**
Un bot di trading avanzato basato su intelligenza artificiale per lo scalping di criptovalute su KuCoin.
## **Indice**
- Descrizione
- Caratteristiche
- Requisiti di Sistema
- Installazione
- Utilizzo
  - Interfaccia a Riga di Comando
  - Interfaccia Grafica (GUI)
- Guida per Principianti
- Cronologia delle Versioni
- Conclusione
- Note
- Licenza
  ## **Descrizione**
**AI Trading Bot** è un bot di trading automatizzato basato su intelligenza artificiale, progettato per lo scalping di criptovalute sull'exchange **KuCoin**. Sfruttando intelligenza artificiale avanzata, indicatori tecnici e strategie di gestione del rischio dinamiche, il bot esegue operazioni sia in modalità **live** che in **paper trading**. Ottimizzato per le coppie denominate in USDT, analizza dati a breve termine per capitalizzare le opportunità di mercato.
## **Caratteristiche**
- **Selezione Automatica delle Migliori Coppie USDT**
  - Analizza e seleziona le migliori coppie USDT per lo scalping basandosi su criteri come volatilità, volume e spread.
  - Le coppie e i parametri di trading vengono rivalutati ogni 60 minuti per adattarsi alle condizioni di mercato in tempo reale.
- **Integrazione con KuCoin**
  - Utilizza le API ufficiali di KuCoin per operazioni di trading sicure ed efficienti.
- **Modalità Paper Trading**
  - Testa le strategie senza rischiare capitale reale, ideale per l'apprendimento e la sperimentazione.
- **Modello AI Ottimizzato**
  - Impiega un modello AI basato su Transformer per previsioni di mercato accurate.
- **Gestione del Rischio Dinamica**
  - Calcola automaticamente le dimensioni delle posizioni e i livelli di stop-loss per proteggere il capitale.
- **Interfaccia Grafica Intuitiva (GUI)**
  - Interfaccia facile da usare per controllare il bot e monitorare le attività in tempo reale.
    ## **Requisiti di Sistema**
- **Versione Python**: 3.7 o superiore
- **Ambiente Virtuale**: Consigliato per isolare le dipendenze del progetto
- **Dipendenze Python**: Elencate in requirements.txt
- **GPU con CUDA**: Per prestazioni ottimali del modello AI (es. RTX 4060)
- **Sistema Operativo**: Compatibile con Windows, macOS e Linux
  ## **Installazione**
  ### **1. Clona il Repository**
bash

git clone https://github.com/tuo-utente/ai\_trading\_bot.git

cd ai\_trading\_bot
### **2. Crea un Ambiente Virtuale**
bash

python -m venv venv
### **3. Attiva l'Ambiente Virtuale**
- **Windows:**

  bash

  venv\Scripts\activate

- **macOS/Linux:**

  bash

  source venv/bin/activate
  ### **4. Installa le Dipendenze**
bash

pip install -r requirements.txt
### **5. Configura le Chiavi API di KuCoin**
- Ottieni le tue chiavi API da KuCoin assicurandoti di abilitare le autorizzazioni necessarie per **Trade** e **Market Data**.
- Crea un file .env nella directory principale del progetto e aggiungi le tue chiavi:

  bash

  KUCOIN\_API\_KEY=la\_tua\_api\_key

  KUCOIN\_API\_SECRET=il\_tuo\_api\_secret

  KUCOIN\_API\_PASSPHRASE=la\_tua\_api\_passphrase
  ## **Utilizzo**
  ### **Interfaccia a Riga di Comando**
Esegui il bot utilizzando la riga di comando:

bash

python src/main.py

- Il bot inizierà a eseguire operazioni in base alle impostazioni configurate.
  ### **Interfaccia Grafica (GUI)**
Avvia il bot con l'interfaccia grafica:

bash

python src/gui.py

- **Switch Modalità Paper Trading**: Passa facilmente tra modalità paper trading e live trading.
- **Barra di Progresso & ETA**: Monitora le operazioni a lungo termine con aggiornamenti in tempo reale.
- **Log in Tempo Reale**: Visualizza le attività del bot direttamente nell'interfaccia.

