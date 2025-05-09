# -----------------------------------------------
# CEL PROGRAMU:
# Generator losowych sekwencji DNA w formacie FASTA.
# Użytkownik podaje długość sekwencji, ID, opis i imię,
# które zostaje wstawione do sekwencji w losowym miejscu,
# ale nie wpływa na statystyki nukleotydów.
# Program zapisuje wynik do pliku *.fasta i prezentuje statystyki.
#
# KONTEKST ZASTOSOWANIA:
# Użyteczny jako narzędzie do nauki bioinformatyki, testowania algorytmów
# analizujących dane genetyczne, a także demonstracji podstaw pracy
# z formatem FASTA i manipulacji sekwencjami DNA.
# -----------------------------------------------

import random
import os  # Umożliwia sprawdzenie istnienia plików (ulepszenie 1)


def generate_random_dna(length):
    """Generuje losową sekwencję DNA złożoną z A, C, G i T."""
    return ''.join(random.choices('ACGT', k=length)) #z liter ACGT wybiera losowo litery tworząc ciąg o długości podanej przez użytkownika


def insert_name(sequence, name):
    """Wstawia imię użytkownika w losowe miejsce sekwencji DNA."""
    insert_pos = random.randint(0, len(sequence)) #losowo wybiera pozycję w sekwencji
    return sequence[:insert_pos] + name + sequence[insert_pos:] #wstawia imię w wylosowanie miejsce


def calculate_statistics(sequence):
    """Oblicza procentowy udział A, C, G, T oraz stosunek %CG."""
    counts = {nuc: sequence.count(nuc) for nuc in 'ACGT'} #liczy ile A,C,G i T jest w sekwencji
    total = sum(counts.values()) #sumuje
    percentages = {nuc: round((counts[nuc] / total) * 100, 1) for nuc in 'ACGT'} #oblicza procenty
    cg_content = round(((counts['C'] + counts['G']) / total) * 100, 1) #oblicza procenty konkretnie dla pary CG
    return percentages, cg_content


def save_fasta(filename, header, sequence):
    """Zapisuje sekwencję do pliku w formacie FASTA."""

    # ORIGINAL:
    # with open(filename, 'w') as f: #otwiera plik
    #     f.write(f">{header}\n")   #zapisuje w pliku
    #     f.write(sequence + "\n")

    # MODIFIED (dodano podział długich sekwencji na linie po 60 znaków – zgodnie ze specyfikacją FASTA):
    with open(filename, 'w') as f: #otwiera plik
        f.write(f">{header}\n")    #zapisuje w pliku
        for i in range(0, len(sequence), 60): #iteruje od 0 do 60 znaków by po 60 znakach przejść do nowej linii
            f.write(sequence[i:i + 60] + '\n')


def validate_sequence_length(length_str):
    """Sprawdza, czy użytkownik podał poprawną długość."""
    if not length_str.isdigit() or int(length_str) <= 0: #sprawdza czy liczba wpisana przez użytkownika jest mniejsza lub równa 0
        raise ValueError("Długość sekwencji musi być dodatnią liczbą całkowitą.") #wypisuje komunikat
    return int(length_str)


def main():
    # ORIGINAL:
    # length = int(input("Podaj długość sekwencji: ")) #wypisuje komunikat do użytkownika i przyjmuje długość

    # MODIFIED (dodano walidację wejścia, aby uniknąć błędów – lepsze UX):
    while True:
        try:
            length = validate_sequence_length(input("Podaj długość sekwencji: ")) #komunikat do użytkownika i przyjęcie długości
            break #gdy dlugość mniejsza od 0 błąd
        except ValueError as e:
            print("Błąd:", e)

    seq_id = input("Podaj ID sekwencji: ") #komunikat do użytkownika
    description = input("Podaj opis sekwencji: ") #komunikat do użytkownika
    name = input("Podaj imię: ") #komunikat do użytkownika

    # ORIGINAL:
    # filename = f"{seq_id}.fasta" #stworzenie nazwy pliku

    # MODIFIED (dodano sprawdzenie, czy plik już istnieje – bezpieczeństwo danych):
    filename = f"{seq_id}.fasta" #stworzenie nazwy pliku
    if os.path.exists(filename): #sprawdzenie czy ścieżka do pliku istnieje
        print(f"Ostrzeżenie: Plik '{filename}' już istnieje i zostanie nadpisany.") #komunikat do użytkownika

    # Generowanie sekwencji DNA
    dna_sequence = generate_random_dna(length)

    # Wstawienie imienia
    sequence_with_name = insert_name(dna_sequence, name)

    # Statystyki na czystej sekwencji (bez imienia)
    stats, cg_ratio = calculate_statistics(dna_sequence)

    # Zapis do pliku FASTA
    header = f"{seq_id} {description}"
    save_fasta(filename, header, sequence_with_name)

    # Wyświetlenie informacji końcowej
    print(f"\nSekwencja została zapisana do pliku {filename}") #komunikat do użytkownika
    print("Statystyki sekwencji:") #komunikat do użytkownika
    for nuc in 'ACGT': #wypisanie statystyk
        print(f"{nuc}: {stats[nuc]}%")
    print(f"%CG: {cg_ratio}")


if __name__ == "__main__":
    main()
