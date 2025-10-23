#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streamlit Webanwendung: Ferien- und Feiertags-Checker (2026-2036)
Vergleicht Schulferien und Feiertage zwischen deutschen Bundesländern und Dänemark
"""

import streamlit as st
from datetime import datetime, timedelta
from ferien_check_2026 import check_date, get_available_years

# Nur deutsche Bundesländer (ohne Dänemark)
BUNDESLAENDER = {
    'Baden-Württemberg': 'BW',
    'Bayern': 'BY',
    'Berlin': 'BE',
    'Brandenburg': 'BB',
    'Bremen': 'HB',
    'Hamburg': 'HH',
    'Hessen': 'HE',
    'Mecklenburg-Vorpommern': 'MV',
    'Niedersachsen': 'NI',
    'Nordrhein-Westfalen': 'NRW',
    'Rheinland-Pfalz': 'RP',
    'Saarland': 'SL',
    'Sachsen': 'SN',
    'Sachsen-Anhalt': 'ST',
    'Schleswig-Holstein': 'SH',
    'Thüringen': 'TH',
}


def parse_date(datum_str):
    """Konvertiert Datum-String (TT.MM.JJJJ) in datetime-Objekt"""
    try:
        return datetime.strptime(datum_str, '%d.%m.%Y')
    except ValueError:
        return None


def check_date_range(von_datum_str, bis_datum_str, bundesland_kuerzel, jahr):
    """
    Prüft einen Datumsbereich für ein Bundesland und Dänemark
    
    Args:
        von_datum_str: Start-Datum (TT.MM.JJJJ)
        bis_datum_str: End-Datum (TT.MM.JJJJ)
        bundesland_kuerzel: Kürzel des Bundeslandes (z.B. 'BY')
        jahr: Ausgewähltes Jahr (2026-2036)
    
    Returns:
        dict mit 'de' und 'dk' Listen von Ergebnissen
    """
    von_datum = parse_date(von_datum_str)
    bis_datum = parse_date(bis_datum_str)
    
    if not von_datum or not bis_datum:
        return {
            'error': True,
            'message': 'Ungültiges Datumsformat. Bitte TT.MM.JJJJ verwenden.'
        }
    
    if von_datum > bis_datum:
        return {
            'error': True,
            'message': 'Das Von-Datum muss vor dem Bis-Datum liegen.'
        }
    
    # Prüfe ob das Von-Datum mit dem ausgewählten Jahr übereinstimmt
    if von_datum.year != jahr:
        return {
            'error': True,
            'message': f'Das Von-Datum muss im Jahr {jahr} liegen.'
        }
    
    # Prüfe ob der Zeitraum maximal 366 Tage beträgt (1 Jahr inkl. Schaltjahr)
    # Dies erlaubt Jahreswechsel (z.B. 24.12.2026-06.01.2027) aber verhindert zu lange Zeiträume
    tage_differenz = (bis_datum - von_datum).days
    if tage_differenz > 366:
        return {
            'error': True,
            'message': f'Der Zeitraum darf maximal 366 Tage betragen (derzeit: {tage_differenz} Tage).'
        }
    
    # Sammel alle gefundenen Ferien/Feiertage
    de_ferien = set()
    de_feiertage = set()
    dk_ferien = set()
    dk_feiertage = set()
    
    # Durchlaufe jeden Tag im Zeitraum
    current_date = von_datum
    while current_date <= bis_datum:
        datum_str = current_date.strftime('%d.%m.%Y')
        
        # Prüfe deutsches Bundesland
        de_ergebnisse = check_date(datum_str, bundesland_kuerzel)
        for erg in de_ergebnisse:
            if "Feiertag:" in erg and "(DE)" in erg:
                feiertag_name = erg.split("Feiertag: ")[1].replace(" (DE)", "")
                de_feiertage.add(feiertag_name)
            elif "Ferien:" in erg and f"({bundesland_kuerzel})" in erg:
                ferien_name = erg.split("Ferien: ")[1]
                de_ferien.add(ferien_name)
        
        # Prüfe Dänemark
        dk_ergebnisse = check_date(datum_str, 'DK')
        for erg in dk_ergebnisse:
            if "Feiertag:" in erg and "(DK)" in erg:
                feiertag_name = erg.split("Feiertag: ")[1].replace(" (DK)", "")
                dk_feiertage.add(feiertag_name)
            elif "Ferien:" in erg and "DK:" in erg:
                ferien_name = erg.split("Ferien: ")[1]
                dk_ferien.add(ferien_name)
        
        current_date += timedelta(days=1)
    
    return {
        'error': False,
        'de_ferien': sorted(de_ferien),
        'de_feiertage': sorted(de_feiertage),
        'dk_ferien': sorted(dk_ferien),
        'dk_feiertage': sorted(dk_feiertage),
    }


def main():
    """Hauptfunktion der Streamlit-App"""
    
    # Seitenkonfiguration
    st.set_page_config(
        page_title="Ferien-Checker 2026-2036",
        page_icon="📅",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS für elegantes Header-Design
    st.markdown("""
        <style>
        /* Header mit Farbverlauf */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .main-title {
            font-family: 'Arial Black', 'Helvetica', sans-serif;
            font-size: 2.5rem;
            color: white;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        .sub-title {
            font-family: 'Arial', 'Helvetica', sans-serif;
            font-size: 1.1rem;
            color: #f0f0f0;
            margin-top: 0.5rem;
        }
        
        /* Verbesserte Boxen für Ergebnisse */
        .result-box {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        .country-header {
            font-size: 1.3rem;
            font-weight: bold;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid #667eea;
        }
        
        /* Info-Box Styling */
        .info-notice {
            background-color: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Eleganter Header mit Farbverlauf
    st.markdown("""
        <div class="main-header">
            <div class="main-title">📅 Ferien- & Feiertags-Checker</div>
            <div class="sub-title">Vergleichen Sie Schulferien und Feiertage (2026-2036)</div>
        </div>
    """, unsafe_allow_html=True)
    
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Eingabebereich in 4 Spalten (inkl. Jahr)
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1.5])
    
    with col1:
        # Von-Datum
        von_datum = st.text_input(
            "📅 Von Datum",
            value="15.07.2026",
            placeholder="TT.MM.JJJJ",
            help="Start-Datum im Format TT.MM.JJJJ"
        )
    
    with col2:
        # Bis-Datum
        bis_datum = st.text_input(
            "📅 Bis Datum",
            value="31.08.2026",
            placeholder="TT.MM.JJJJ",
            help="End-Datum im Format TT.MM.JJJJ"
        )
    
    with col3:
        # Bundesland-Dropdown (nur Deutschland)
        bundesland_name = st.selectbox(
            "🇩🇪 Bundesland",
            options=list(BUNDESLAENDER.keys()),
            index=list(BUNDESLAENDER.keys()).index('Nordrhein-Westfalen'),
            help="Wählen Sie ein deutsches Bundesland"
        )
    
    with col4:
        # Jahresauswahl (2026-2036)
        verfuegbare_jahre = get_available_years()
        jahr = st.selectbox(
            "📆 Jahr",
            options=verfuegbare_jahre,
            index=0,
            help="Wählen Sie das Jahr (2026 = vollständige Daten)"
        )
    
    # Prüfen-Button (zentriert)
    st.markdown("<br>", unsafe_allow_html=True)
    col_button1, col_button2, col_button3 = st.columns([1, 2, 1])
    with col_button2:
        pruefen_button = st.button("🔍 Vergleichen", use_container_width=True, type="primary")
    
    st.divider()
    
    # Ergebnisbereich
    if pruefen_button:
        # Validierung
        if not von_datum.strip() or not bis_datum.strip():
            st.error("⚠️ Bitte geben Sie beide Daten ein!")
            return
        
        # Bundesland-Kürzel ermitteln
        bundesland_kuerzel = BUNDESLAENDER[bundesland_name]
        
        # Datumsbereich prüfen
        ergebnis = check_date_range(von_datum.strip(), bis_datum.strip(), bundesland_kuerzel, jahr)
        
        # Fehlerbehandlung
        if ergebnis.get('error'):
            st.error(f"❌ {ergebnis['message']}")
            return
        
        # Ergebnisse anzeigen
        st.markdown("### 📋 Vergleichsergebnis")
        
        # Info-Box mit Zeitraum
        st.info(f"**Zeitraum:** {von_datum} bis {bis_datum} ({jahr})  \n**Bundesland:** {bundesland_name}")
        
        # Zwei Spalten für DE und DK mit verbessertem Design
        col_de, col_dk = st.columns(2)
        
        with col_de:
            # Container für Deutschland
            with st.container():
                st.markdown('<div class="country-header">🇩🇪 Deutschland</div>', unsafe_allow_html=True)
                st.markdown(f"**{bundesland_name}**")
                st.markdown("")
                
                # Deutsche Feiertage
                if ergebnis['de_feiertage']:
                    st.success("**Feiertage:**")
                    for feiertag in ergebnis['de_feiertage']:
                        st.markdown(f"🎊 {feiertag}")
                    st.markdown("")
                
                # Deutsche Ferien
                if ergebnis['de_ferien']:
                    st.success("**Ferien:**")
                    for ferien in ergebnis['de_ferien']:
                        st.markdown(f"🏖️ {ferien}")
                
                # Keine Ferien/Feiertage
                if not ergebnis['de_feiertage'] and not ergebnis['de_ferien']:
                    st.warning("📅 Keine Ferien oder Feiertage im ausgewählten Zeitraum")
        
        with col_dk:
            # Container für Dänemark
            with st.container():
                st.markdown('<div class="country-header">🇩🇰 Dänemark</div>', unsafe_allow_html=True)
                st.markdown("")
                
                # Dänische Feiertage
                if ergebnis['dk_feiertage']:
                    st.success("**Feiertage:**")
                    for feiertag in ergebnis['dk_feiertage']:
                        st.markdown(f"🎊 {feiertag}")
                    st.markdown("")
                
                # Dänische Ferien
                if ergebnis['dk_ferien']:
                    st.success("**Ferien:**")
                    for ferien in ergebnis['dk_ferien']:
                        st.markdown(f"🏖️ {ferien}")
                
                # Keine Ferien/Feiertage
                if not ergebnis['dk_feiertage'] and not ergebnis['dk_ferien']:
                    st.warning("📅 Keine Ferien oder Feiertage im ausgewählten Zeitraum")
    
    else:
        # Anleitung anzeigen, wenn noch nicht geprüft wurde
        st.info(
            "👆 Wählen Sie einen Datumsbereich, ein Bundesland und ein Jahr, "
            "dann klicken Sie auf **Vergleichen**."
        )
        
        # Beispiele in ansprechenden Boxen
        st.markdown("### 💡 Beispiele:")
        
        col_ex1, col_ex2, col_ex3 = st.columns(3)
        
        with col_ex1:
            st.markdown("""
            <div style='background-color: #f0f7ff; padding: 1rem; border-radius: 8px; border-left: 4px solid #2196F3;'>
                <strong>Sommerferien</strong><br>
                Von: 15.07.2026<br>
                Bis: 31.08.2026
            </div>
            """, unsafe_allow_html=True)
        
        with col_ex2:
            st.markdown("""
            <div style='background-color: #fff4e6; padding: 1rem; border-radius: 8px; border-left: 4px solid #ff9800;'>
                <strong>Weihnachten</strong><br>
                Von: 24.12.2026<br>
                Bis: 06.01.2027
            </div>
            """, unsafe_allow_html=True)
        
        with col_ex3:
            st.markdown("""
            <div style='background-color: #e8f5e9; padding: 1rem; border-radius: 8px; border-left: 4px solid #4caf50;'>
                <strong>Neujahr</strong><br>
                Von: 01.01.2026<br>
                Bis: 01.01.2026
            </div>
            """, unsafe_allow_html=True)
    
    # Footer mit modernem Design
    st.divider()
    st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.9em; padding: 1rem;'>
            <strong>Vergleich:</strong> Deutschland (16 Bundesländer) ⇄ Dänemark<br>
            <span style='font-size: 0.85em;'>Daten für 2026 vollständig | 2027-2036 anpassbar</span>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
