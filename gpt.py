import os
from pathlib import Path

# Définir les extensions de fichiers à lire
EXTENSIONS = {'.ts', '.css', '.html', '.py', '.json'}

def get_file_content(file_path):
    """Lit le contenu d'un fichier et le renvoie sous forme de chaîne."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_markdown_file(file_name, content):
    """Écrit le contenu dans un fichier Markdown."""
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)

def generate_markdown_for_directory(root_dir):
    """Génère un fichier Markdown avec le contenu de tous les fichiers spécifiés."""
    markdown_content = "# Contenu des fichiers\n\n"
    
    print(f"Démarrage de l'analyse du répertoire : {root_dir}")
    
    # Parcourir les répertoires et fichiers
    for root, dirs, files in os.walk(root_dir):
        print(f"Analyse du répertoire : {root}")
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix in EXTENSIONS:
                print(f"Lecture du fichier : {file_path}")
                # Ajouter le nom du fichier dans le Markdown
                markdown_content += f"## {file_path.relative_to(root_dir)}\n\n"
                # Ajouter le contenu du fichier dans le Markdown
                try:
                    file_content = get_file_content(file_path)
                    markdown_content += f"```\n{file_content}\n```\n\n"
                except Exception as e:
                    markdown_content += f"Erreur lors de la lecture du fichier {file_path}: {e}\n\n"
                    print(f"Erreur lors de la lecture du fichier {file_path}: {e}")

    return markdown_content

if __name__ == "__main__":
    root_directory = Path(__file__).parent  # Le répertoire contenant ce script
    print(f"Répertoire racine : {root_directory}")
    markdown_file_path = root_directory / 'contenu_fichiers.md'
    print(f"Fichier Markdown sera généré ici : {markdown_file_path}")
    markdown_content = generate_markdown_for_directory(root_directory)
    write_markdown_file(markdown_file_path, markdown_content)
    print("Le fichier Markdown a été généré avec succès.")
