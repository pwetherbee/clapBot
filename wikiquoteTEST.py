import wikiquote
import random

#print(wikiquote.search("donald trump"))
print()

quotes = wikiquote.quotes("Bernie Sanders")

quote = random.choice(quotes)

print(quote)