"""
Jeanine Palicte

A set of classes that represent functionality for storing information about
countries and the languages they speak, as well as comparing them.
LanguageFile allows for summarizing the data and writing it to a user chosen
file. LanguageUI gives an interactive method for selecting countries and 
comparing the languages spoken in each one. Language class is a super class
that opens DEFAULT_FILE and reads and stores the data.
"""



class Language:
    DEFAULT_FILE = "lab3.txt"
    languageToNumSpoken = {}
    countryToLanguages = {}
    languageLen = None
    created = False

    def __init__(self):
        """
        Read the default file and store its data in some dictionaries
        """
        if self.created:
            return

        f = open(self.DEFAULT_FILE, "r")

        for line in f.readlines():
            line = line.split(",")
            country = line[0].strip().lower()
            self.countryToLanguages[country] = [
                lang.strip().lower() for lang in line[1:]
            ]

            for language in line[1:]:
                language = language.strip().lower()
                if self.languageLen == None:
                    self.languageLen = len(language)
                if len(language) > self.languageLen:
                    self.languageLen = len(language)

                self.languageToNumSpoken[language] = (
                    self.languageToNumSpoken.get(language, 0) + 1
                )

        f.close()
        self.created = True



class LanguageFile(Language):
    def mostCommonLanguages(self, filename):
        """
        Write to file filename a list languages that are spoken in more than 10 countries
        """
        f = open(filename, "w")
        f.write("The most common languages\n")
        badLanguages = ["other", "dialect", "regional", "languages"]
        rows = [("Language", "Num of countries")]
        rows.extend(
            filter(
                lambda item: item[1] > 10
                and not any(bad in item[0] for bad in badLanguages),
                reversed(
                    sorted(self.languageToNumSpoken.items(), key=lambda item: item[1])
                ),
            )
        )

        for row in rows:
            f.write(
                "".join(
                    row[0].capitalize().ljust(self.languageLen) + str(row[1]).ljust(3)
                )
                + "\n"
            )
        f.close()

    def writeDict(self, fhandle, data, label):
        """
        Write the keys of dict to a provided file in alphabetical order separated by starting character
        """
        fhandle.write(f"List of {len(data.keys())} {label}:\n")

        data = sorted(data.keys())
        lines = ""
        for letter in "abcdefghijklmnopqrstuvwxyz":
            line = filter(lambda lang: lang.startswith(letter), data)

            if line == []:
                continue
            line = ", ".join([lang.strip().capitalize() for lang in line]) + "\n\n"
            lines += line
        fhandle.write(lines)

    def totalCountriesAndLanguages(self, filename, choice=None):
        """
        Write either all countries, languages, or both to a file in a structured format
        """
        if choice not in ["country", "language", None]:
            print("Not a valid option for choice!")
            exit()
        f = open(filename, "w")
        if choice == "country":
            self.writeDict(f, self.countryToLanguages, "countries")
        elif choice == "language":
            self.writeDict(f, self.languageToNumSpoken, "languages")
        elif choice == None:
            self.writeDict(f, self.countryToLanguages, "countries")
            self.writeDict(f, self.languageToNumSpoken, "languages")
        f.close()



class LanguageUI(Language):
    def _getLetter(self):
        """
        Get the starting letter for the country the user wants
        """
        done = False
        while not done:
            letter = input("Enter first letter of country name: ").strip().lower()
            if letter == "":
                return "Done"
            if letter not in [char for char in "abcedefghijklmnopqrstuvwxyz"]:
                print("Input must be a letter")
                continue
            done = True
        return letter

    def _getIndex(self, validCountries):
        """
        Get the index of the country the user wants
        """
        done = False
        while not done:
            num = input("Enter a number corresponding to a country name: ").strip()
            try:
                num = int(num)
            except ValueError:
                print("Input is not a number")
                continue
            if num < 1 or num > len(validCountries):
                print("number is not within range")
                continue
            done = True
        return num

    def _getCountries(self):
        """
        Get list of countries whose languages should be compared
        """
        print("Need at least 2 countries")

        countries = set()
        done = False
        while not done:
            letter = self._getLetter()
            if letter == "Done" and len(countries) < 2:
                print("Need at least 2 countries")
                continue
            if letter == "Done":
                done = True
                continue

            print(f"Country names starting with {letter.upper()}")
            validCountries = list(
                filter(
                    lambda lang: lang.startswith(letter),
                    sorted(self.countryToLanguages.keys()),
                )
            )
            for idx, country in enumerate(validCountries):
                print(f"{idx + 1} {country.capitalize()}")

            num = self._getIndex(validCountries)
            print(f"{validCountries[num - 1].capitalize()} chosen")
            countries.add(validCountries[num - 1])

        return countries

    def compareLanguages(self):
        print("Compare Languages")
        countries = self._getCountries()
        languageForCountries = [
            set(self.countryToLanguages[country]) for country in countries
        ]

        languagesInCommon = languageForCountries[0]
        allLanguages = languageForCountries[0]
        for languageSet in languageForCountries[1:]:
            languagesInCommon = languagesInCommon.intersection(languageSet)
            allLanguages = allLanguages.union(languageSet)

        if len(languagesInCommon) == 0:
            print("No common language")
        else:
            sentence = "Common languages: "
            for language in languagesInCommon:
                sentence += language.capitalize() + " "
            print(sentence.strip())

        allLanguages = sorted(list(allLanguages))
        sentence = "All languages: "
        for language in allLanguages:
            sentence += language.capitalize() + " "
        print(sentence.strip())
        print()
