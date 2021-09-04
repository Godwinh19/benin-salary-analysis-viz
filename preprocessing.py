
GROUP = {

    "dev_frontend": ["Développeur Front-end", "Développeur Angular", "Développeur front end", "Frontend dev",
                     "Développeur Web Frontend"],
    "dev_backend": ["Developeur Backend", "Developer back-end", "Développeur Web Backend", "Développeur JEE"],
    "fullstack": ["Full stack web developer", "Développeur Web Full Stack", "Full Stack Dev",
                  "Développeur Web FullStack et Mobile ", "Développeur Web (Back end et front end) "],
    "dev_web": ['Développeur web', "Développeur Web"],
    "mobile": ["Développeur web et mobile ", "Développeur web et mobile", "Développeur Android et python"],
    "data_analyst": ["Data Analyst ", "Data Analyst", "IT & Data Analyste"],
    "manager": ["IT Project Manager ", "Lead developer", "Project Manager Junior", "Big Data Manager",
                "Chef Division Applications et Base de Données", "Manager", "Chef de projet web et mobile"],
    "reseau_sécurite": ["Ingénieur réseau, système et securité"],
    "devops": ['DevOps', "Devops"],
    "autres": ['Assistant technique '],
    "designer": ['UX/UI DESIGNER ']

}


def clean_salary(salary):
    salary = str(salary).lower()  # transformer tout FCFA en fcfa
    to_remove = ['fcfa', '.', 'mille']

    for chaine in to_remove:
        if chaine == 'mille':
            salary = salary.replace(chaine, '000')
        salary = salary.replace(chaine, '')
    return salary


class DataCleaning:
    def __init__(self, df):
        self.data = df

    @property
    def run(self):
        data = self.data

        columns = ['date', 'poste', 'experience', 'salaire_debut', 'salaire_actuel', 'satisfaction']
        data.columns = columns

        # data['salaire_debut'] = data['salaire_debut'].apply(clean_salary)
        # data['salaire_actuel'] = data['salaire_actuel'].apply(clean_salary)

        data[['salaire_debut', 'salaire_actuel']] = data[['salaire_debut', 'salaire_actuel']].astype('int')

        metiers = []

        for i, row in data.iterrows():
            is_in = True
            for metier in GROUP:
                if row.poste in GROUP[metier]:
                    metiers.append(metier)
                    is_in = False

            if is_in:
                metiers.append(row.poste)

        data['metiers'] = metiers

        return data
