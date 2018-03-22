from cars_web.models import CarsDetails
from django.core.mail import EmailMultiAlternatives
from cars_web.settings import EMAIL_HOST_USER


cars_years_list = [{'year': '2019', 'value': '36362520'}, {'year': '2018', 'value': '35797618'},
                   {'year': '2017', 'value': '30031936'}, {'year': '2016', 'value': '58487'},
                   {'year': '2015', 'value': '56007'}, {'year': '2014', 'value': '51683'},
                   {'year': '2013', 'value': '47272'}, {'year': '2012', 'value': '39723'},
                   {'year': '2011', 'value': '34923'}, {'year': '2010', 'value': '27381'},
                   {'year': '2009', 'value': '20201'}, {'year': '2008', 'value': '20145'},
                   {'year': '2007', 'value': '20200'}, {'year': '2006', 'value': '20144'},
                   {'year': '2005', 'value': '20199'}, {'year': '2004', 'value': '20143'},
                   {'year': '2003', 'value': '20198'}, {'year': '2002', 'value': '20142'},
                   {'year': '2001', 'value': '20197'}, {'year': '2000', 'value': '20141'},
                   {'year': '1999', 'value': '20196'}, {'year': '1998', 'value': '20140'},
                   {'year': '1997', 'value': '20195'}, {'year': '1996', 'value': '20139'},
                   {'year': '1995', 'value': '20194'}, {'year': '1994', 'value': '20138'},
                   {'year': '1993', 'value': '20193'}, {'year': '1992', 'value': '20137'},
                   {'year': '1991', 'value': '20192'}, {'year': '1990', 'value': '20136'},
                   {'year': '1989', 'value': '20191'}, {'year': '1988', 'value': '20135'},
                   {'year': '1987', 'value': '20190'}, {'year': '1986', 'value': '20134'},
                   {'year': '1985', 'value': '20189'}, {'year': '1984', 'value': '20133'},
                   {'year': '1983', 'value': '20188'}, {'year': '1982', 'value': '20132'},
                   {'year': '1981', 'value': '20187'}, {'year': '1980', 'value': '20131'},
                   {'year': '1979', 'value': '20186'}, {'year': '1978', 'value': '20130'},
                   {'year': '1977', 'value': '20185'}, {'year': '1976', 'value': '20129'},
                   {'year': '1975', 'value': '20184'}, {'year': '1974', 'value': '20128'},
                   {'year': '1973', 'value': '20183'}, {'year': '1972', 'value': '20127'},
                   {'year': '1971', 'value': '20182'}, {'year': '1970', 'value': '20126'},
                   {'year': '1969', 'value': '20181'}, {'year': '1968', 'value': '20125'},
                   {'year': '1967', 'value': '20180'}, {'year': '1966', 'value': '20124'},
                   {'year': '1965', 'value': '20179'}, {'year': '1964', 'value': '20123'},
                   {'year': '1963', 'value': '20178'}, {'year': '1962', 'value': '20122'},
                   {'year': '1961', 'value': '20177'}, {'year': '1960', 'value': '20121'},
                   {'year': '1959', 'value': '20176'}, {'year': '1958', 'value': '20120'},
                   {'year': '1957', 'value': '20175'}, {'year': '1956', 'value': '20119'},
                   {'year': '1955', 'value': '20174'}, {'year': '1954', 'value': '20118'},
                   {'year': '1953', 'value': '20173'}, {'year': '1952', 'value': '20117'},
                   {'year': '1951', 'value': '20172'}, {'year': '1950', 'value': '20116'},
                   {'year': '1949', 'value': '20171'}, {'year': '1948', 'value': '20115'},
                   {'year': '1947', 'value': '20170'}, {'year': '1946', 'value': '20114'},
                   {'year': '1942', 'value': '20112'}, {'year': '1941', 'value': '20167'},
                   {'year': '1940', 'value': '20111'}, {'year': '1939', 'value': '20166'},
                   {'year': '1938', 'value': '20110'}, {'year': '1937', 'value': '20165'},
                   {'year': '1936', 'value': '20109'}, {'year': '1935', 'value': '20164'},
                   {'year': '1934', 'value': '20108'}, {'year': '1933', 'value': '20163'},
                   {'year': '1932', 'value': '20107'}, {'year': '1931', 'value': '20162'},
                   {'year': '1930', 'value': '20106'}, {'year': '1929', 'value': '20161'},
                   {'year': '1928', 'value': '20105'}, {'year': '1927', 'value': '20160'},
                   {'year': '1926', 'value': '20104'}, {'year': '1925', 'value': '20159'},
                   {'year': '1924', 'value': '20103'}, {'year': '1923', 'value': '20158'},
                   {'year': '1922', 'value': '20102'}, {'year': '1921', 'value': '20157'},
                   {'year': '1918', 'value': '20100'}]


def save_data(website, make, model, title, link):
    CarsDetails.objects.create(website=website, make=make, model=model, title=title, link=link)


def delete_previous_results(website, make, model):
    if CarsDetails.objects.filter(website=website, make=make, model=model).count() > 0:
        CarsDetails.objects.filter(website=website, make=make, model=model).all().delete()


def send_email(items, email):
    text_content = ""
    for i in items:
        text_content += "Title: %s\n Make: %s\n Model: %s\n Link: %s" % (i[0], i[1], i[2], i[3])
    if len(items) == 1:
        msg = EmailMultiAlternatives("%s %s %s" % (items[0][0], items[0][1], items[0][2]),
                                    text_content, EMAIL_HOST_USER, [email])
    else:
        msg = EmailMultiAlternatives("%s %s" % (items[0][0], items[0][1]), text_content, EMAIL_HOST_USER, [email])
    msg.send()
