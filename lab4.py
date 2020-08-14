"""
Jeanine Palicte

Read country and spoken language data from a file and store it.
Then write a summary of that data to several files.
Then allow the user to select multiple countries from a list to compare
the languages spoken in those countries.
"""



from language import LanguageFile, LanguageUI

l_file = LanguageFile()
l_file.totalCountriesAndLanguages("countries.txt", choice="country")
l_file.totalCountriesAndLanguages("languages.txt", choice="language")
l_file.totalCountriesAndLanguages("both.txt")
l_file.mostCommonLanguages("mostCommonLanguages.txt")

l_ui = LanguageUI()

done = False
while not done:
    l_ui.compareLanguages()

    cont = input("Continue to compare? y/n: ").strip().lower() == "y"
    if not cont:
        done = True