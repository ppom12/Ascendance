def assign_sosa(individual, sosa_number, sosa_dict, visited):
    """
    Remplit sosa_dict avec l'individu comme clé et son numéro SOSA comme valeur
    visited : pour éviter les cycles
    """
    if individual in visited:
        return
    visited.add(individual)
    sosa_dict[individual] = sosa_number
    
    parents = parser.get_parents(individual)
    if len(parents) > 0:
        father, mother = (parents[0], parents[1]) if len(parents) == 2 else (parents[0], None)
        if father:
            assign_sosa(father, sosa_number*2, sosa_dict, visited)
        if mother:
            assign_sosa(mother, sosa_number*2 + 1, sosa_dict, visited)

from gedcom.parser import Parser
from gedcom.element.individual import IndividualElement

parser = Parser()
parser.parse_file("Antoine_export.ged")
root_elements = parser.get_root_child_elements()

# Choisir l'individu racine pour SOSA
# Exemple: le premier individu du fichier
root_individual = next((el for el in root_elements if isinstance(el, IndividualElement)), None)

sosa_dict = {}
assign_sosa(root_individual, 1, sosa_dict, set())  # génère tous les SOSA

for element in root_elements:
    if isinstance(element, IndividualElement):

        # Nom
        first, last = element.get_name()
        nom = f"{last.upper()} {first}"

        # Naissance
        birth_data = element.get_birth_data()
        birth_date = birth_data[0] if len(birth_data) > 0 else ""
        birth_place = birth_data[1] if len(birth_data) > 1 else ""

        # Décès
        death_data = element.get_death_data()
        death_date = death_data[0] if len(death_data) > 0 else ""
        death_place = death_data[1] if len(death_data) > 1 else ""

        # Mariage
        marriage_date = ""
        marriage_place = ""
        for fam in parser.get_families(element):
            for child in fam.get_child_elements():
                if child.get_tag() == "MARR":
                    date_elem = next((e for e in child.get_child_elements() if e.get_tag() == "DATE"), None)
                    if date_elem:
                        marriage_date = date_elem.get_value()
                    place_elem = next((e for e in child.get_child_elements() if e.get_tag() == "PLAC"), None)
                    if place_elem:
                        marriage_place = place_elem.get_value()

        # SOSA
        sosa = sosa_dict.get(element, "")

        print(
            f"{nom}, {birth_date}, {birth_place}, "
            f"{marriage_date}, {marriage_place}, "
            f"{death_date}, {death_place}, {sosa}"
        )
