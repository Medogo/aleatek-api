import sys

def find_duplicates(lines):
    seen = {}
    result = []
    for line in lines:
        if line in seen:
            seen[line] += 1
            result.append(f"{line} ({seen[line]})")
        else:
            seen[line] = 1
            result.append(line)
    return result

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py input_file output_file")
        return

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    try:
        with open(input_file_path, 'r') as file:
            lines = file.read().splitlines()

        modified_lines = find_duplicates(lines)

        with open(output_file_path, 'w') as file:
            file.write('\n'.join(modified_lines))

        print("Opération terminée avec succès.")

    except FileNotFoundError:
        print("Le fichier spécifié est introuvable.")
    except Exception as e:
        print("Une erreur s'est produite :", e)

if __name__ == "__main__":
    main()
