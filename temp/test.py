import wikipediaapi

wiki = wikipediaapi.Wikipedia("ru")

page = wiki.page("Пайтон")

if page.exists():
    print(page.summary)
