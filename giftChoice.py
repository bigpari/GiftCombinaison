from urllib.request import urlopen
from bs4 import BeautifulSoup
from itertools import combinations

url = "https://www.amazon.ca/hz/wishlist/printview/31VIE6A08078B?target=_blank&ref_=lv_pv&filter=persistent_all&sort=default"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

products=[]
prices=[]
max_amount = 350
max_combinaison = 4
price_difference_from_max = 20

for item_row in  soup.find_all("tr")[1:]:
    spans = item_row.find_all("span")
    price = float(spans[2].get_text().replace('$', ''))
    if price == 0 :
        continue
    products.append(spans[0].get_text())
    prices.append(price)

res = {}
for combinaisonIndex in range(1, max_combinaison):
    for gift in combinations(products, combinaisonIndex):
        ele_sum = sum([prices[products.index(x)] for x in gift])
        try:
            res[ele_sum].append(str(gift) + " total => " + str(ele_sum))
        except KeyError:
            res[ele_sum] = [str(gift) + " total => " + str(ele_sum)]

f = open("giftCombinaison.txt", "a")

for key, value in res.items():
    if key > max_amount:
        continue
    if max_amount - key <= price_difference_from_max:
        for giftCombinaison in value:
            print(giftCombinaison)
            f.write(giftCombinaison)
            f.write("\n")

f.close()