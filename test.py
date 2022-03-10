import urllib.parse

query = {'spam': 1, 'eggs': True, 'bacon': 'foo'}
params = '&'.join([
            str(x) + "=" + urllib.parse.quote_plus(str(y))
            for x, y in query.items()
        ])
print(params)
