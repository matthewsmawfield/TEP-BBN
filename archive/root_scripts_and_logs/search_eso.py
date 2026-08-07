from astroquery.eso import Eso
eso = Eso()
table = eso.query_surveys(target='Q0913+072', radius=10)
print(table)
