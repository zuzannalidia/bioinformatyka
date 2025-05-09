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
    return ''.join(random.choices('ACGT', k=length))


def insert_name(sequence, name):
    """Wstawia imię użytkownika w losowe miejsce sekwencji DNA."""
    insert_pos = random.randint(0, len(sequence))
    return sequence[:insert_pos] + name + sequence[insert_pos:]


def calculate_statistics(sequence):
    """Oblicza procentowy udział A, C, G, T oraz stosunek %CG."""
    counts = {nuc: sequence.count(nuc) for nuc in 'ACGT'}
    total = sum(counts.values())
    percentages = {nuc: round((counts[nuc] / total) * 100, 1) for nuc in 'ACGT'}
    cg_content = round(((counts['C'] + counts['G']) / total) * 100, 1)
    return percentages, cg_content


def save_fasta(filename, header, sequence):
    """Zapisuje sekwencję do pliku w formacie FASTA."""

    # ORIGINAL:
    # with open(filename, 'w') as f:
    #     f.write(f">{header}\n")
    #     f.write(sequence + "\n")

    # MODIFIED (dodano podział długich sekwencji na linie po 60 znaków – zgodnie ze specyfikacją FASTA):
    with open(filename, 'w') as f:
        f.write(f">{header}\n")
        for i in range(0, len(sequence), 60):
            f.write(sequence[i:i + 60] + '\n')


def validate_sequence_length(length_str):
    """Sprawdza, czy użytkownik podał poprawną długość."""
    if not length_str.isdigit() or int(length_str) <= 0:
        raise ValueError("Długość sekwencji musi być dodatnią liczbą całkowitą.")
    return int(length_str)


def main():
    # ORIGINAL:
    # length = int(input("Podaj długość sekwencji: "))

    # MODIFIED (dodano walidację wejścia, aby uniknąć błędów – lepsze UX):
    while True:
        try:
            length = validate_sequence_length(input("Podaj długość sekwencji: "))
            break
        except ValueError as e:
            print("Błąd:", e)

    seq_id = input("Podaj ID sekwencji: ")
    description = input("Podaj opis sekwencji: ")
    name = input("Podaj imię: ")

    # ORIGINAL:
    # filename = f"{seq_id}.fasta"

    # MODIFIED (dodano sprawdzenie, czy plik już istnieje – bezpieczeństwo danych):
    filename = f"{seq_id}.fasta"
    if os.path.exists(filename):
        print(f"Ostrzeżenie: Plik '{filename}' już istnieje i zostanie nadpisany.")

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
    print(f"\nSekwencja została zapisana do pliku {filename}")
    print("Statystyki sekwencji:")
    for nuc in 'ACGT':
        print(f"{nuc}: {stats[nuc]}%")
    print(f"%CG: {cg_ratio}")


if __name__ == "__main__":
    main()
