from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas as pd
import collections


def get_writed(age):
    last_number = age % 10
    pre_last_number = age // 10 % 10
    if 2 <= last_number <= 4:
        if pre_last_number == 1:
            writed = "лет"
        else:
            writed = "года"
    elif last_number == 1:
        if pre_last_number == 1:
            writed = "лет"
        else:
            writed = "год"
    else:
        writed = "лет"
    return writed


def main():
    products = pd.read_excel(
        "cakes3.xlsx",
        na_values=['N/A', 'NA'], keep_default_na=False
    ).to_dict("records")
    grouped_products = collections.defaultdict(list)
    for product in products:
        grouped_products[product["Категория"]].append(product)
    now = datetime.datetime.now()
    age = now.year - 2010
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template("template.html")
    rendered_page = template.render(
        age=age,
        writed=get_writed(age),
        grouped_products=grouped_products
    )
    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()