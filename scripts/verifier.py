#!/usr/bin/env python3
"""Revérifie chaque flux de la playlist et écrit un rapport.

Usage : python scripts/verifier.py afrique-francophone.m3u
Un flux est valide si le serveur répond 200/206 et que le corps commence par #EXTM3U.
Les entrées YouTube ne sont pas testées (elles passent par yt-dlp).
"""
import concurrent.futures as cf
import re
import subprocess
import sys

TIMEOUT_S = 15
THREADS = 24


def lire(chemin):
    lignes = open(chemin, encoding="utf-8").read().splitlines()
    for i, l in enumerate(lignes):
        if l.startswith("#EXTINF") and i + 1 < len(lignes):
            yield l.rsplit(",", 1)[-1].strip(), lignes[i + 1].strip()


def tester(entree):
    nom, url = entree
    if "youtube.com" in url:
        return nom, url, "youtube"
    try:
        r = subprocess.run(
            ["curl", "-sL", "--max-time", str(TIMEOUT_S), "-A", "Mozilla/5.0",
             "-w", "\n@@%{http_code}", url],
            capture_output=True, text=True, errors="ignore", timeout=TIMEOUT_S + 10)
        corps, _, code = r.stdout.rpartition("@@")
        ok = code.strip() in ("200", "206") and "#EXTM3U" in corps[:800]
        return nom, url, "ok" if ok else f"ko ({code.strip() or 'timeout'})"
    except Exception as exc:  # réseau coupé, curl absent...
        return nom, url, f"ko ({exc.__class__.__name__})"


def main():
    chemin = sys.argv[1] if len(sys.argv) > 1 else "afrique-francophone.m3u"
    entrees = list(lire(chemin))
    with cf.ThreadPoolExecutor(THREADS) as ex:
        resultats = list(ex.map(tester, entrees))
    ok = [r for r in resultats if r[2] == "ok"]
    ko = [r for r in resultats if r[2].startswith("ko")]
    for nom, url, etat in resultats:
        print(f"{etat:14} {nom[:40]:40} {url}")
    print(f"\n{len(ok)} valides, {len(ko)} en panne, "
          f"{len(resultats) - len(ok) - len(ko)} YouTube non testés")
    sys.exit(1 if ko else 0)


if __name__ == "__main__":
    main()
