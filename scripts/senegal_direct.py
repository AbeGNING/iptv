#!/usr/bin/env python3
"""Fabrique une playlist personnelle des grandes chaînes sénégalaises.

Ces chaînes (SenTV, Walf TV, 7TV, Leral TV...) sont servies par ACAN Group
derrière un jeton valable dix minutes ; RTS 1 et RTS 2 passent par Dailymotion,
dont l'URL HLS est elle aussi éphémère. Une playlist statique ne peut donc pas
les contenir : ce script demande des jetons frais et écrit un fichier M3U à
ouvrir immédiatement (dans les dix minutes) dans VLC ou un autre lecteur.

Usage :
    python scripts/senegal_direct.py            # écrit senegal-direct.m3u
    python scripts/senegal_direct.py sortie.m3u # autre nom de fichier

Prérequis : Python 3.8+, aucune bibliothèque tierce.
Remarque : Dailymotion refuse les adresses IP de centres de données ; à lancer
depuis une connexion résidentielle ou mobile.
"""
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
TIMEOUT_S = 15

# API publique d'ACAN Group : l'identifiant 2 (SenTV) suffit, le jeton obtenu
# ouvre toutes les applications publiclive/, acanabr/ et acas/ du même serveur.
ACAN_API = "https://tveapi.acan.group/myapiv2/directplayback/2/json?platform=web"
ACAN_HOST = "https://live1.acangroup.org:1929/"
ACAN_CHAINES = [
    ("SenTV", "acanabr/sentv.stream_all/playlist.m3u8"),
    ("Walf TV", "publiclive/walftv.stream/playlist.m3u8"),
    ("7TV", "publiclive/septtv.stream/playlist.m3u8"),
    ("Leral TV", "acanabr/leraltv_all/playlist.m3u8"),
    ("Télé École", "acanabr/teleecole_all/playlist.m3u8"),
    ("Asfiyahi TV", "acas/asfiyahitv/playlist.m3u8"),
    ("Malikia TV", "publiclive/malikiatv.stream/playlist.m3u8"),
    ("Global TV HD", "publiclive/globaltvhd/playlist.m3u8"),
    ("CIS Media TV", "publiclive/cismediatv/playlist.m3u8"),
    ("RTJ TV (Gambie)", "acas/rtjtv/playlist.m3u8"),
]

# Identifiants permanents des directs Dailymotion (compte officiel de chaque chaîne).
DAILYMOTION_CHAINES = [
    ("RTS 1", "x9kctc2"),
    ("RTS 2", "xab8sx4"),
    ("RSI (radio filmée)", "xab6b7y"),
    ("RFM (radio filmée)", "x7wi5y1"),
    ("TFM", "x7wcr45"),
]


def lire_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT_S) as rep:
        return json.load(rep)


def jeton_acan():
    """Retourne le paramètre wmsAuthSign courant, ou None si l'API refuse."""
    try:
        web_url = lire_json(ACAN_API).get("web_url", "")
    except (urllib.error.URLError, ValueError) as exc:
        print(f"ACAN : jeton indisponible ({exc})", file=sys.stderr)
        return None
    jeton = urllib.parse.parse_qs(urllib.parse.urlparse(web_url).query).get("wmsAuthSign")
    return jeton[0] if jeton else None


def flux_dailymotion(video_id):
    """Retourne l'URL HLS du direct, ou None si la chaîne est hors antenne."""
    try:
        meta = lire_json(f"https://www.dailymotion.com/player/metadata/video/{video_id}")
    except (urllib.error.URLError, ValueError) as exc:
        print(f"Dailymotion {video_id} : {exc}", file=sys.stderr)
        return None
    if meta.get("error"):
        print(f"Dailymotion {video_id} : {meta['error'].get('title', 'hors antenne')}", file=sys.stderr)
        return None
    qualites = meta.get("qualities", {}).get("auto", [])
    return qualites[0]["url"] if qualites else None


def construire():
    lignes = ["#EXTM3U", "# Playlist éphémère (jetons de 10 minutes), régénérée par scripts/senegal_direct.py"]
    jeton = jeton_acan()
    if jeton:
        for nom, chemin in ACAN_CHAINES:
            lignes.append(f'#EXTINF:-1 group-title="Sénégal (ACAN)",{nom}')
            lignes.append(f"{ACAN_HOST}{chemin}?wmsAuthSign={jeton}")
    for nom, video_id in DAILYMOTION_CHAINES:
        url = flux_dailymotion(video_id)
        if not url:
            continue
        lignes.append(f'#EXTINF:-1 group-title="Sénégal (Dailymotion)",{nom}')
        lignes.append(f"#EXTVLCOPT:http-user-agent={UA}")
        lignes.append(url)
    return lignes


def main():
    sortie = sys.argv[1] if len(sys.argv) > 1 else "senegal-direct.m3u"
    lignes = construire()
    nb = sum(1 for l in lignes if l.startswith("#EXTINF"))
    if nb == 0:
        print("Aucun flux obtenu : vérifier la connexion.", file=sys.stderr)
        sys.exit(1)
    with open(sortie, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")
    print(f"{nb} flux écrits dans {sortie} ; à ouvrir dans les dix minutes.")


if __name__ == "__main__":
    main()
