#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ferien- und Feiertags-Checker für Deutschland und Dänemark 2026
Überprüft, ob ein Datum auf Schulferien oder Feiertage fällt
Mit Tkinter-GUI für einfache Bedienung
"""

import pandas as pd
from datetime import datetime

def get_available_years():
    """
    Gibt die Liste der verfügbaren Jahre zurück (2026-2036)
    
    Returns:
        list: Liste von Jahren (z.B. [2026, 2027, ..., 2036])
    """
    return list(range(2026, 2037))


DEUTSCHE_FEIERTAGE_2026 = {
    'Neujahr': '01.01.2026',
    'Heilige Drei Könige': '06.01.2026',  # BW, BY, ST
    'Karfreitag': '03.04.2026',
    'Ostersonntag': '05.04.2026',
    'Ostermontag': '06.04.2026',
    'Tag der Arbeit': '01.05.2026',
    'Christi Himmelfahrt': '14.05.2026',
    'Pfingstsonntag': '24.05.2026',
    'Pfingstmontag': '25.05.2026',
    'Fronleichnam': '04.06.2026',  # BW, BY, HE, NW, RP, SL
    'Mariä Himmelfahrt': '15.08.2026',  # BY (regional), SL
    'Tag der Deutschen Einheit': '03.10.2026',
    'Reformationstag': '31.10.2026',  # BB, MV, SN, ST, TH
    'Allerheiligen': '01.11.2026',  # BW, BY, NW, RP, SL
    'Buß- und Bettag': '18.11.2026',  # SN
    '1. Weihnachtstag': '25.12.2026',
    '2. Weihnachtstag': '26.12.2026',
}

FEIERTAGE_BUNDESLAENDER = {
    'BW': ['Neujahr', 'Heilige Drei Könige', 'Karfreitag', 'Ostermontag', 'Tag der Arbeit', 
           'Christi Himmelfahrt', 'Pfingstmontag', 'Fronleichnam', 'Tag der Deutschen Einheit', 
           'Allerheiligen', '1. Weihnachtstag', '2. Weihnachtstag'],
    'BY': ['Neujahr', 'Heilige Drei Könige', 'Karfreitag', 'Ostermontag', 'Tag der Arbeit', 
           'Christi Himmelfahrt', 'Pfingstmontag', 'Fronleichnam', 'Mariä Himmelfahrt', 
           'Tag der Deutschen Einheit', 'Allerheiligen', '1. Weihnachtstag', '2. Weihnachtstag'],
    'BE': ['Neujahr', 'Karfreitag', 'Ostermontag', 'Tag der Arbeit', 'Christi Himmelfahrt', 
           'Pfingstmontag', 'Tag der Deutschen Einheit', '1. Weihnachtstag', '2. Weihnachtstag'],
    'BB': ['Neujahr', 'Karfreitag', 'Ostermontag', 'Tag der Arbeit', 'Christi Himmelfahrt', 
           'Pfingstmontag', 'Tag der Deutschen Einheit', 'Reformationstag', '1. Weihnachtstag', '2. Weihnachtstag'],
    'HB': ['Neujahr', 'Karfreitag', 'Ostermontag', 'Tag der Arbeit', 'Christi Himmelfahrt', 
           'Pfingstmontag', 'Tag der Deutschen Einheit', '1. Weihnachtstag', '2. Weihnachtstag'],
    'HH': ['Neujahr', 'Karfreitag', 'Ostermontag', 'Tag der Arbeit', 'Christi Himmelfahrt', 
           'Pfingstmontag', 'Tag der Deutschen Einheit', '1. Weihnachtstag', '2. Weihnachtstag'],
    'HE': ['Neujahr', 'Karfreitag', 'Ostermontag', 'Tag der Arbeit', 'Christi Himmelfahrt', 
           'Pfingstmontag', 'Fronleichnam', 'Tag der Deutschen Einheit', '1. Weihnachtstag', '2. Weihnachtstag'],
    'MV': ['Neujahr', 'Karfreitag', 'Ostermontag', 'Tag der Arbeit', 'Christi Himmelfahrt', 
           'Pfingstmontag', 'Tag der Deutschen Einheit', 'Reformationstag', '1. Weihnahtstag', '2. Weihnachtstag'],
    'NI': ['Neujahr', 'Karfreitag', 'Ostermontag', 'Tag der Arbeit', 'Christi Himmelfahrt', 
           'Pfingstmontag', 'Tag der Deutschen Einheit', '1. Weihnachtstag', '2. Weihnachtstag'],
    'NRW': ['Neujahr', 'Karfreitag', 'Ostermontag', 'Tag der Arbeit', 'Christi Himmelfahrt', 
            'Pfingstmontag', 'Fronleichnam', 'Tag der Deutschen Einheit', 'Allerheiligen', 
            '1. Weihnachtstag', '2. Weihnachtstag'],
    'RP': ['Neujahr', 'Karfreitag', 'Ostermontag', 'Tag der Arbeit', 'Christi Himmelfahrt', 
           'Pfingstmontag', 'Fronleichnam', 'Tag der Deutschen Einheit', 'Allerheiligen', 
           '1. Weihnachtstag', '2. Weihnachtstag'],
    'SL': ['Neujahr', 'Karfreitag', 'Ostermontag', 'Tag der Arbeit', 'Christi Himmelfahrt', 
           'Pfingstmontag', 'Fronleichnam', 'Mariä Himmelfahrt', 'Tag der Deutschen Einheit', 
           'Allerheiligen', '1. Weihnachtstag', '2. Weihnachtstag'],
    'SN': ['Neujahr', 'Karfreitag', 'Ostermontag', 'Tag der Arbeit', 'Christi Himmelfahrt', 
           'Pfingstmontag', 'Tag der Deutschen Einheit', 'Reformationstag', 'Buß- und Bettag', 
           '1. Weihnachtstag', '2. Weihnachtstag'],
    'ST': ['Neujahr', 'Heilige Drei Könige', 'Karfreitag', 'Ostermontag', 'Tag der Arbeit', 
           'Christi Himmelfahrt', 'Pfingstmontag', 'Tag der Deutschen Einheit', 'Reformationstag', 
           '1. Weihnachtstag', '2. Weihnachtstag'],
    'SH': ['Neujahr', 'Karfreitag', 'Ostermontag', 'Tag der Arbeit', 'Christi Himmelfahrt', 
           'Pfingstmontag', 'Tag der Deutschen Einheit', '1. Weihnachtstag', '2. Weihnachtstag'],
    'TH': ['Neujahr', 'Karfreitag', 'Ostermontag', 'Tag der Arbeit', 'Christi Himmelfahrt', 
           'Pfingstmontag', 'Tag der Deutschen Einheit', 'Reformationstag', '1. Weihnachtstag', '2. Weihnachtstag'],
}

SCHULFERIEN_2026 = {
    'BW': [
        ('Winterferien', '09.02.2026', '13.02.2026'),
        ('Osterferien', '30.03.2026', '10.04.2026'),
        ('Pfingstferien', '02.06.2026', '12.06.2026'),
        ('Sommerferien', '30.07.2026', '12.09.2026'),
        ('Herbstferien', '26.10.2026', '30.10.2026'),
        ('Weihnachtsferien', '23.12.2026', '09.01.2027'),
    ],
    'BY': [
        ('Winterferien', '16.02.2026', '20.02.2026'),
        ('Osterferien', '30.03.2026', '10.04.2026'),
        ('Pfingstferien', '26.05.2026', '05.06.2026'),
        ('Sommerferien', '27.07.2026', '10.09.2026'),
        ('Herbstferien', '02.11.2026', '06.11.2026'),
        ('Weihnachtsferien', '23.12.2026', '09.01.2027'),
    ],
    'BE': [
        ('Winterferien', '02.02.2026', '07.02.2026'),
        ('Osterferien', '30.03.2026', '10.04.2026'),
        ('Sommerferien', '09.07.2026', '22.08.2026'),
        ('Herbstferien', '19.10.2026', '31.10.2026'),
        ('Weihnachtsferien', '23.12.2026', '02.01.2027'),
    ],
    'BB': [
        ('Winterferien', '02.02.2026', '07.02.2026'),
        ('Osterferien', '30.03.2026', '10.04.2026'),
        ('Sommerferien', '09.07.2026', '22.08.2026'),
        ('Herbstferien', '19.10.2026', '31.10.2026'),
        ('Weihnachtsferien', '23.12.2026', '02.01.2027'),
    ],
    'HB': [
        ('Winterferien', '02.02.2026', '03.02.2026'),
        ('Osterferien', '27.03.2026', '11.04.2026'),
        ('Pfingstferien', '15.05.2026', '15.05.2026'),
        ('Sommerferien', '23.07.2026', '02.09.2026'),
        ('Herbstferien', '12.10.2026', '24.10.2026'),
        ('Weihnachtsferien', '23.12.2026', '08.01.2027'),
    ],
    'HH': [
        ('Winterferien', '02.02.2026', '02.02.2026'),
        ('Osterferien', '06.03.2026', '18.03.2026'),
        ('Pfingstferien', '15.05.2026', '19.05.2026'),
        ('Sommerferien', '25.06.2026', '05.08.2026'),
        ('Herbstferien', '12.10.2026', '23.10.2026'),
        ('Weihnachtsferien', '21.12.2026', '04.01.2027'),
    ],
    'HE': [
        ('Osterferien', '06.04.2026', '18.04.2026'),
        ('Sommerferien', '06.07.2026', '14.08.2026'),
        ('Herbstferien', '05.10.2026', '17.10.2026'),
        ('Weihnachtsferien', '23.12.2026', '09.01.2027'),
    ],
    'MV': [
        ('Winterferien', '09.02.2026', '21.02.2026'),
        ('Osterferien', '30.03.2026', '08.04.2026'),
        ('Pfingstferien', '22.05.2026', '26.05.2026'),
        ('Sommerferien', '22.06.2026', '01.08.2026'),
        ('Herbstferien', '05.10.2026', '10.10.2026'),
        ('Weihnachtsferien', '21.12.2026', '02.01.2027'),
    ],
    'NI': [
        ('Winterferien', '02.02.2026', '03.02.2026'),
        ('Osterferien', '23.03.2026', '10.04.2026'),
        ('Pfingstferien', '15.05.2026', '15.05.2026'),
        ('Sommerferien', '23.07.2026', '02.09.2026'),
        ('Herbstferien', '12.10.2026', '24.10.2026'),
        ('Weihnachtsferien', '23.12.2026', '08.01.2027'),
    ],
    'NRW': [
        ('Osterferien', '30.03.2026', '11.04.2026'),
        ('Pfingstferien', '26.05.2026', '26.05.2026'),
        ('Sommerferien', '15.07.2026', '26.08.2026'),
        ('Herbstferien', '12.10.2026', '24.10.2026'),
        ('Weihnachtsferien', '23.12.2026', '06.01.2027'),
    ],
    'RP': [
        ('Winterferien', '16.02.2026', '16.02.2026'),
        ('Osterferien', '27.03.2026', '10.04.2026'),
        ('Sommerferien', '06.07.2026', '14.08.2026'),
        ('Herbstferien', '12.10.2026', '23.10.2026'),
        ('Weihnachtsferien', '23.12.2026', '08.01.2027'),
    ],
    'SL': [
        ('Winterferien', '16.02.2026', '21.02.2026'),
        ('Osterferien', '30.03.2026', '10.04.2026'),
        ('Pfingstferien', '09.06.2026', '09.06.2026'),
        ('Sommerferien', '06.07.2026', '14.08.2026'),
        ('Herbstferien', '12.10.2026', '23.10.2026'),
        ('Weihnachtsferien', '23.12.2026', '04.01.2027'),
    ],
    'SN': [
        ('Winterferien', '09.02.2026', '21.02.2026'),
        ('Osterferien', '02.04.2026', '10.04.2026'),
        ('Pfingstferien', '15.05.2026', '15.05.2026'),
        ('Sommerferien', '22.06.2026', '31.07.2026'),
        ('Herbstferien', '19.10.2026', '31.10.2026'),
        ('Weihnachtsferien', '23.12.2026', '02.01.2027'),
    ],
    'ST': [
        ('Winterferien', '02.02.2026', '07.02.2026'),
        ('Osterferien', '30.03.2026', '04.04.2026'),
        ('Pfingstferien', '15.05.2026', '15.05.2026'),
        ('Sommerferien', '29.06.2026', '08.08.2026'),
        ('Herbstferien', '26.10.2026', '30.10.2026'),
        ('Weihnachtsferien', '21.12.2026', '05.01.2027'),
    ],
    'SH': [
        ('Osterferien', '02.04.2026', '18.04.2026'),
        ('Pfingstferien', '15.05.2026', '16.05.2026'),
        ('Sommerferien', '20.07.2026', '29.08.2026'),
        ('Herbstferien', '12.10.2026', '24.10.2026'),
        ('Weihnachtsferien', '21.12.2026', '06.01.2027'),
    ],
    'TH': [
        ('Winterferien', '02.02.2026', '07.02.2026'),
        ('Osterferien', '30.03.2026', '11.04.2026'),
        ('Pfingstferien', '22.05.2026', '22.05.2026'),
        ('Sommerferien', '20.07.2026', '29.08.2026'),
        ('Herbstferien', '05.10.2026', '17.10.2026'),
        ('Weihnachtsferien', '23.12.2026', '02.01.2027'),
    ],
}

DAENISCHE_FEIERTAGE_2026 = {
    'Nytårsdag': '01.01.2026',
    'Skærtorsdag': '02.04.2026',
    'Langfredag': '03.04.2026',
    'Påskedag': '05.04.2026',
    '2. påskedag': '06.04.2026',
    'Store bededag': '01.05.2026',
    'Kristi himmelfartsdag': '14.05.2026',
    'Pinsedag': '24.05.2026',
    '2. pinsedag': '25.05.2026',
    'Grundlovsdag': '05.06.2026',
    'Juleaftensdag': '24.12.2026',
    'Juledag': '25.12.2026',
    '2. juledag': '26.12.2026',
}

DAENISCHE_SCHULFERIEN_2026 = [
    ('Vinterferien', '09.02.2026', '15.02.2026'),
    ('Påskeferien', '02.04.2026', '06.04.2026'),
    ('Sommerferien', '27.06.2026', '04.08.2026'),
    ('Efterårsferie', '12.10.2026', '18.10.2026'),
    ('Juleferie', '23.12.2026', '03.01.2027'),
]


def parse_date(datum_str):
    """Konvertiert Datum-String (TT.MM.JJJJ) in datetime-Objekt"""
    return datetime.strptime(datum_str, '%d.%m.%Y')


def is_date_in_range(datum, start_str, end_str):
    """Prüft, ob ein Datum in einem bestimmten Zeitraum liegt"""
    start = parse_date(start_str)
    end = parse_date(end_str)
    return start <= datum <= end


def check_date(datum_str, bundesland='NRW'):
    """
    Überprüft, ob ein Datum auf Ferien oder Feiertage fällt
    
    Args:
        datum_str: Datum im Format TT.MM.JJJJ
        bundesland: Bundesland-Kürzel (z.B. 'BY', 'NRW', 'BW') oder 'DK' für Dänemark
    
    Returns:
        Liste von Strings mit den Ergebnissen
    """
    try:
        datum = parse_date(datum_str)
    except ValueError:
        return [f"Fehler: Ungültiges Datumsformat. Bitte TT.MM.JJJJ verwenden."]
    
    ergebnisse = []
    
    if bundesland == 'DK':
        for feiertag, feiertag_datum in DAENISCHE_FEIERTAGE_2026.items():
            if datum_str == feiertag_datum:
                ergebnisse.append(f"Feiertag: {feiertag} (DK)")
        
        for ferien_name, start, end in DAENISCHE_SCHULFERIEN_2026:
            if is_date_in_range(datum, start, end):
                ergebnisse.append(f"DK: Ferien: {ferien_name}")
    
    else:
        if bundesland not in SCHULFERIEN_2026:
            return [f"Fehler: Bundesland '{bundesland}' nicht bekannt. Verfügbare: {', '.join(SCHULFERIEN_2026.keys())}, DK"]
        
        feiertage_bundesland = FEIERTAGE_BUNDESLAENDER.get(bundesland, [])
        for feiertag in feiertage_bundesland:
            feiertag_datum = DEUTSCHE_FEIERTAGE_2026.get(feiertag)
            if feiertag_datum and datum_str == feiertag_datum:
                ergebnisse.append(f"Feiertag: {feiertag} (DE)")
        
        for ferien_name, start, end in SCHULFERIEN_2026[bundesland]:
            if is_date_in_range(datum, start, end):
                ergebnisse.append(f"DE ({bundesland}): Ferien: {ferien_name}")
    
    if not ergebnisse:
        if bundesland == 'DK':
            ergebnisse.append(f"DK: Kein Feiertag oder Ferien am {datum_str}")
        else:
            ergebnisse.append(f"DE ({bundesland}): Kein Feiertag oder Ferien am {datum_str}")
    
    return ergebnisse


def print_beispiele():
    """Zeigt Beispiel-Aufrufe der check_date Funktion"""
    print("=" * 70)
    print("FERIEN- UND FEIERTAGS-CHECKER 2026 - BEISPIELE")
    print("=" * 70)
    print()
    
    beispiele = [
        ('15.07.2026', 'NRW'),
        ('01.01.2026', 'BY'),
        ('03.04.2026', 'BW'),
        ('27.07.2026', 'BY'),
        ('05.06.2026', 'DK'),
        ('27.06.2026', 'DK'),
        ('15.05.2026', 'HE'),
        ('01.11.2026', 'NRW'),
        ('31.10.2026', 'TH'),
        ('12.03.2026', 'HH'),
    ]
    
    for datum, bl in beispiele:
        print(f"check_date('{datum}', '{bl}'):")
        ergebnisse = check_date(datum, bl)
        for ergebnis in ergebnisse:
            print(f"  → {ergebnis}")
        print()


def show_bundeslaender_info():
    """Zeigt alle verfügbaren Bundesländer"""
    print("=" * 70)
    print("VERFÜGBARE BUNDESLÄNDER")
    print("=" * 70)
    
    bundeslaender_namen = {
        'BW': 'Baden-Württemberg',
        'BY': 'Bayern',
        'BE': 'Berlin',
        'BB': 'Brandenburg',
        'HB': 'Bremen',
        'HH': 'Hamburg',
        'HE': 'Hessen',
        'MV': 'Mecklenburg-Vorpommern',
        'NI': 'Niedersachsen',
        'NRW': 'Nordrhein-Westfalen',
        'RP': 'Rheinland-Pfalz',
        'SL': 'Saarland',
        'SN': 'Sachsen',
        'ST': 'Sachsen-Anhalt',
        'SH': 'Schleswig-Holstein',
        'TH': 'Thüringen',
        'DK': 'Dänemark',
    }
    
    for kuerzel, name in sorted(bundeslaender_namen.items()):
        print(f"  {kuerzel:4s} - {name}")
    print()


class FerienCheckerGUI:
    """
    Tkinter-GUI für den Ferien- und Feiertags-Checker
    """
    
    def __init__(self, root):
        """Initialisiert die GUI"""
        self.root = root
        self.root.title("Ferien- und Feiertags-Checker 2026")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Bundesländer-Namen für Dropdown (mit vollständigen Namen)
        self.bundeslaender = {
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
            'Dänemark': 'DK',
        }
        
        self.create_widgets()
    
    def create_widgets(self):
        """Erstellt alle GUI-Elemente"""
        
        # Hauptrahmen mit Padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titel
        title_label = ttk.Label(
            main_frame, 
            text="Ferien- und Feiertags-Checker 2026",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Datum-Eingabefeld
        datum_label = ttk.Label(main_frame, text="Datum (TT.MM.JJJJ):", font=('Arial', 10))
        datum_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.datum_entry = ttk.Entry(main_frame, width=25, font=('Arial', 10))
        self.datum_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        self.datum_entry.insert(0, "15.07.2026")  # Beispiel-Datum
        
        # Bundesland-Dropdown
        bundesland_label = ttk.Label(main_frame, text="Bundesland:", font=('Arial', 10))
        bundesland_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.bundesland_var = tk.StringVar(value='Nordrhein-Westfalen')
        bundesland_dropdown = ttk.Combobox(
            main_frame, 
            textvariable=self.bundesland_var,
            values=list(self.bundeslaender.keys()),
            state='readonly',
            width=23,
            font=('Arial', 10)
        )
        bundesland_dropdown.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Prüfen-Button
        pruefen_button = ttk.Button(
            main_frame,
            text="Prüfen",
            command=self.pruefen_datum,
            width=20
        )
        pruefen_button.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Ergebnis-Label
        ergebnis_label = ttk.Label(main_frame, text="Ergebnis:", font=('Arial', 10, 'bold'))
        ergebnis_label.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        # Ergebnis-Textfeld mit Scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Textfeld für Ergebnisse
        self.ergebnis_text = tk.Text(
            text_frame,
            height=12,
            width=50,
            wrap=tk.WORD,
            font=('Arial', 10),
            yscrollcommand=scrollbar.set
        )
        self.ergebnis_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.ergebnis_text.yview)
        
        # Info-Text am unteren Rand
        info_label = ttk.Label(
            main_frame,
            text="Überprüft Ferien und Feiertage für Deutschland und Dänemark",
            font=('Arial', 8),
            foreground='gray'
        )
        info_label.grid(row=6, column=0, columnspan=2, pady=(10, 0))
        
        # Grid-Gewichtung für responsive Layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
    
    def pruefen_datum(self):
        """
        Wird beim Klick auf 'Prüfen'-Button aufgerufen
        Ruft check_date() auf und zeigt Ergebnisse an
        """
        # Eingaben holen
        datum_str = self.datum_entry.get().strip()
        bundesland_name = self.bundesland_var.get()
        bundesland_kuerzel = self.bundeslaender[bundesland_name]
        
        # Validierung: Datum darf nicht leer sein
        if not datum_str:
            messagebox.showwarning("Warnung", "Bitte geben Sie ein Datum ein!")
            return
        
        # Check-Funktion aufrufen
        ergebnisse = check_date(datum_str, bundesland_kuerzel)
        
        # Ergebnis-Textfeld leeren
        self.ergebnis_text.delete('1.0', tk.END)
        
        # Ergebnisse anzeigen
        self.ergebnis_text.insert('1.0', f"Datum: {datum_str}\n")
        self.ergebnis_text.insert(tk.END, f"Region: {bundesland_name}\n")
        self.ergebnis_text.insert(tk.END, "=" * 50 + "\n\n")
        
        # Jedes Ergebnis in eigener Zeile
        for ergebnis in ergebnisse:
            self.ergebnis_text.insert(tk.END, f"• {ergebnis}\n")
        
        # Farbliche Hervorhebung je nach Ergebnis
        if any("Ferien" in erg or "Feiertag" in erg for erg in ergebnisse):
            # Grüner Hintergrund für Ferien/Feiertage
            self.ergebnis_text.tag_add("highlight", "4.0", tk.END)
            self.ergebnis_text.tag_config("highlight", foreground="darkgreen", font=('Arial', 10, 'bold'))
        else:
            # Normale Anzeige wenn kein Feiertag/Ferien
            self.ergebnis_text.tag_add("normal", "4.0", tk.END)
            self.ergebnis_text.tag_config("normal", foreground="darkred")


def start_gui():
    """Startet die Tkinter-GUI-Anwendung"""
    root = tk.Tk()
    app = FerienCheckerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    # Starte GUI (kommentieren Sie die nächste Zeile aus für Konsolen-Modus)
    start_gui()
    
    # Alternativ: Konsolen-Modus (auskommentiert)
    # show_bundeslaender_info()
    # print_beispiele()
