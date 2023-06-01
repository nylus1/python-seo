#---------------------------------------------------------------#
#  Script para agilizar la creación de prompts SEO              #
#  Autor: Ignacio Sánchez Gómez                                 #
#  DPTO: BirdCom                                                #
#  Fecha Inicio: 30/05/2023                                     #
#  Versión 1.0                                                  #
#---------------------------------------------------------------#


input_file = "ChangeCharacters/input.txt"
output_file = "ChangeCharacters/output.txt"

with open(input_file, "r") as f:
    content = f.readlines()

# Sustituye tabulaciones con "|"
content = [line.replace("\t", "|") for line in content]

# Añade "|" al principio y final de cada línea
content = ["|" + line.strip() + "|" for line in content]

with open(output_file, "w") as f:
    f.write("\n".join(content))

print("Documento guardado como", output_file)
