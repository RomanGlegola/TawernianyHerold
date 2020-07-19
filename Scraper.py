import feedparser
from bs4 import BeautifulSoup
import requests


def forumTawernyRpgWatki():
    return (
        'https://tawerna.rpg.pl/forum/viewforum.php?f=1', 'https://tawerna.rpg.pl/forum/viewforum.php?f=2',
        'https://tawerna.rpg.pl/forum/viewforum.php?f=3', 'https://tawerna.rpg.pl/forum/viewforum.php?f=4',
        'https://tawerna.rpg.pl/forum/viewforum.php?f=5', 'https://tawerna.rpg.pl/forum/viewforum.php?f=6',
        'https://tawerna.rpg.pl/forum/viewforum.php?f=7', 'https://tawerna.rpg.pl/forum/viewforum.php?f=9',
        'https://tawerna.rpg.pl/forum/viewforum.php?f=10', 'https://tawerna.rpg.pl/forum/viewforum.php?f=11',
        'https://tawerna.rpg.pl/forum/viewforum.php?f=13', 'https://tawerna.rpg.pl/forum/viewforum.php?f=17',
        'https://tawerna.rpg.pl/forum/viewforum.php?f=21', 'https://tawerna.rpg.pl/forum/viewforum.php?f=27',
        'https://tawerna.rpg.pl/forum/viewforum.php?f=46', 'https://tawerna.rpg.pl/forum/viewforum.php?f=47',
        'https://tawerna.rpg.pl/forum/viewforum.php?f=48', 'https://tawerna.rpg.pl/forum/viewforum.php?f=53',
        'https://tawerna.rpg.pl/forum/viewforum.php?f=55', 'https://tawerna.rpg.pl/forum/viewforum.php?f=56',
        'https://tawerna.rpg.pl/forum/viewforum.php?f=57', 'https://tawerna.rpg.pl/forum/viewforum.php?f=58',
        'https://tawerna.rpg.pl/forum/viewforum.php?f=61', 'https://tawerna.rpg.pl/forum/viewforum.php?f=62',
        'https://tawerna.rpg.pl/forum/viewforum.php?f=63', 'https://tawerna.rpg.pl/forum/viewforum.php?f=64',
        'https://tawerna.rpg.pl/forum/viewforum.php?f=65', 'https://tawerna.rpg.pl/forum/viewforum.php?f=66',
        'https://tawerna.rpg.pl/forum/viewforum.php?f=68', 'https://tawerna.rpg.pl/forum/viewforum.php?f=100',
        'https://tawerna.rpg.pl/forum/viewforum.php?f=101', 'https://tawerna.rpg.pl/forum/viewforum.php?f=102',
        'https://tawerna.rpg.pl/forum/viewforum.php?f=103', 'https://tawerna.rpg.pl/forum/viewforum.php?f=104',
        'https://tawerna.rpg.pl/forum/viewforum.php?f=126')


def forumTawernyRpgPbf():
    return (
        'https://tawerna.rpg.pl/forum/viewforum.php?f=107', 'https://tawerna.rpg.pl/forum/viewforum.php?f=14',
        'https://tawerna.rpg.pl/forum/viewforum.php?f=15')


def kanalRssTawerny():
    return ('https://tawerna.rpg.pl/?feed=rss2')


def daneForum(dane):
    """
    funkcja wydobywa autora wątku, nazwę wątku, adres
    www wątku, datę publikacji wątku oraz surową datę do
    oznaczenia ostatniego opublikowanego wątku na kanale
    """

    autor_watku = dane.findAll(("a", "span"), class_=
    ["username", "username-coloured"])[1] \
        .text \
        .strip()
    nazwa_watku = dane.find("a", class_="topictitle") \
        .getText()
    adres_watku = dane.find("a", class_="topictitle") \
                      .attrs["href"][1:].split('&sid=')
    data_watku = dane.select("time", class_="datetime")[1] \
        .text \
        .strip() \
        .split(',')
    data_watku[1] = data_watku[1][1:]
    data_watku[2] = data_watku[2].replace(' ', '')
    sol_daty = data_surowa(data_watku)
    data_czytelna = data_przerobiona(sol_daty)
    return autor_watku, nazwa_watku, f'https://tawerna.rpg.pl/forum{adres_watku[0]}', \
           data_czytelna, sol_daty


def daneStrony(dane):
    """
    funkcja wydobywa autora artykułu, nazwę artykułu, adres
    www artykułu, datę publikacji artykułu oraz surową datę do
    oznaczenia ostatniego opublikowanego artykułu na kanale
    :param dane:
    :return:
    """
    author = dane.author
    title = dane.title
    link = dane.link
    data = dane.published[5:-9]
    published = [''] + data \
        .rsplit(sep=" ", maxsplit=1)
    sol_daty = data_surowa(published)
    data_czytelna = data_przerobiona(sol_daty)
    yield author, title, link, data_czytelna, sol_daty


def data_przerobiona(dane):
    rok = dane[0:4]
    miesiac = dane[4:6]
    dzien = dane[6:8]
    godzina = dane[8:10]
    minuta = dane[10:12]

    cyfra_z_zerem = ['00', '01', '02', '03', '04',
                     '05', '06', '07', '08', '09',
                     '10', '11', '12']
    cyfra_bez_zera = ['0', '1', '2', '3', '4',
                      '5', '6', '7', '8', '9']

    for x in range(10):
        if godzina == cyfra_z_zerem[x]:
            godzina = godzina.replace(cyfra_z_zerem[x], cyfra_bez_zera[x])

    for x in range(10):
        if dzien == cyfra_z_zerem[x]:
            dzien = dzien.replace(cyfra_z_zerem[x], cyfra_bez_zera[x])

    miesiac_czytelny = ['', 'stycznia', 'lutego', 'marca',
                        'kwietnia', 'maja', 'czerwca',
                        'lipca', 'sierpnia', 'września',
                        'października', 'listopada', 'grudnia']

    for x in range(len(miesiac_czytelny)):
        if miesiac == cyfra_z_zerem[x]:
            miesiac = miesiac.replace(cyfra_z_zerem[x], miesiac_czytelny[x])
    return f"{dzien} {miesiac} {rok}", f"{godzina}:{minuta}"


def data_surowa(dane):
    """
    funkcja wydobywa z daty do funkcji surowe
    cyfry celem późniejszej obróbki wiadomości
    :param dane:
    :return:
    """
    miesiace_stare = [
        ['stycznia', 'lutego', 'marca',
         'kwietnia', 'maja', 'czerwca',
         'lipca', 'sierpnia', 'września',
         'października', 'listopada', 'grudnia'],
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]
    miesiace_nowe = [
        '01', '02', '03', '04', '05', '06',
        '07', '08', '09', '10', '11', '12']
    for x in range(len(miesiace_nowe)):
        for i in range(len(miesiace_stare)):
            dane = [item.replace(miesiace_stare[i][x], miesiace_nowe[x]) for item in dane]
    lista = [int(x) for x in
             dane[1].split()[::-1] +
             dane[2].split(':')]
    return "".join(map(lambda x: "%02d" % x, lista[:6]))


def zupaForum(dane):
    """
    funkcja pobiera kod strony internetowej. Następnie
    wydobywa z działu na forum posty celem sprawdzenia
    które z nich są najstarsze i przekazuje dalej.
    :param dane:
    :return:
    """
    strona = requests \
        .get(dane) \
        .text
    for watek in BeautifulSoup(strona, 'lxml').findAll(class_=
                                                       ['row-item sticky_read_locked',
                                                        'row-item topic_read',
                                                        'row-item topic_read_hot',
                                                        'row-item topic_read_mine',
                                                        'row-item topic_unread',
                                                        'row-item topic_unread_mine']):
        yield watek


def zupaStrony(dane):
    """
    funkcja pobiera kod strony internetowej. Następnie
    wydobywa ARTYKUŁY celem sprawdzenia
    które z nich są najstarsze i przekazuje dalej.
    :param dane:
    :return:
    """
    dane = feedparser.parse(dane)
    for x in range(8):
        yield dane.entries[x]


def zrzutForum(dane):
    """
    funkcja zrzuca wszystkie wydobyte dane z Forum w formie listy i je drukuje.
    :return:
    """
    return tuple([daneForum(x) for x in (zupaForum(i))] for i in dane)


def zrzutStrony(dane):
    """
    funkcja zrzuca wszystkie wydobyte dane z RSS w formie listy i je drukuje.
    :return:
    """
    return tuple([*daneStrony(i)] for i in zupaStrony(dane))


def tekstPBF(dane=forumTawernyRpgPbf()):
    from OperacjeNaPlikach import DataSystemuWatkuWyswietl, DataSystemuWatkuNadpisz
    data_archiwum = DataSystemuWatkuWyswietl('forumTawernyRpgPbfData')
    data_temp = data_archiwum
    for strona in zrzutForum(dane):
        for watek in strona:
            if data_archiwum < watek[4]:
                if data_temp < watek[4]:
                    data_temp = watek[4]
                yield (f'Ogłaszam uroczyście, że dnia {watek[3][0]} o godzinie {watek[3][1]} '
                       f'na forum pojawiła się nowa gra PBF! "{watek[1]}".\n'
                       f'Autorstwa "{watek[0]}". Pełną wiadomość można poznać pod adresem: {watek[2]}/\n')
    DataSystemuWatkuNadpisz('forumTawernyRpgPbfData', data_temp)


def tekstForum(dane=forumTawernyRpgWatki()):
    from OperacjeNaPlikach import DataSystemuWatkuWyswietl, DataSystemuWatkuNadpisz
    data_archiwum = DataSystemuWatkuWyswietl('forumTawernyRpgWatkiData')
    data_temp = data_archiwum
    for strona in zrzutForum(dane):
        for watek in strona:
            if data_archiwum < watek[4]:
                if data_temp < watek[4]:
                    data_temp = watek[4]
                yield (f'Ogłaszam uroczyście, że dnia {watek[3][0]} o godzinie {watek[3][1]} '
                       f'na forum pojawił się wątek! "{watek[1]}".\n'
                       f'Autorstwa "{watek[0]}". Pełną wiadomość można poznać pod adresem: {watek[2]}/\n')
    DataSystemuWatkuNadpisz('forumTawernyRpgWatkiData', data_temp)


def tekstRSS(dane=kanalRssTawerny()):
    from OperacjeNaPlikach import DataSystemuWatkuWyswietl, DataSystemuWatkuNadpisz
    data_archiwum = DataSystemuWatkuWyswietl('kanalRssTawernyData')
    data_temp = data_archiwum
    for kanalRss in zrzutStrony(dane):
        for artykul in kanalRss:
            if data_archiwum < artykul[4]:
                if data_temp < artykul[4]:
                    data_temp = artykul[4]
                yield (f'Z nieukrywaną radością ogłaszam, że dnia {artykul[3][0]} o godzinie {artykul[3][1]} '
                       f'na stronie pojawił się nowy artykuł pod tytułem: "{artykul[1]}".\n'
                       f'Autorstwa "{artykul[0]}". Z pełną treścią można się zapoznać pod adresem: {artykul[2]}\n')
    DataSystemuWatkuNadpisz('kanalRssTawernyData', data_temp)


# print(*tekstPBF(forumTawernyRpgPbf()))
# print(*tekstForum(forumTawernyRpgWatki()))
# print(*tekstRSS(kanalRssTawerny()))
