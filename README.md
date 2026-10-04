# IPTV Afrique francophone

Playlist M3U de chaînes de télévision africaines francophones, avec un accent sur le Sénégal.
Chaque flux HLS a été vérifié en deux passes (réponse HTTP 200/206 et manifeste `#EXTM3U` lu) le 4 octobre 2026.

## Utilisation

URL courte à coller dans VLC, Kodi, TiviMate, IPTV Smarters ou tout lecteur compatible M3U :

```
https://abegning.github.io/iptv/afrique.m3u
```

Adresse de secours (même fichier, servi par GitHub directement) :

```
https://raw.githubusercontent.com/AbeGNING/iptv/main/afrique.m3u
```

## Contenu

| Groupe | Flux | Exemples |
|---|---|---|
| Sénégal | 8 | A2i TV, A2i Religion, Asfiyahi TV, GMS TV, Louga TV, SenJeunes TV, Seneweb TV, Diaspora 24 |
| Sénégal (directs YouTube) | 8 | RTS, TFM, 2STV, Walf TV, SenTV, iTV, Leral TV, Dakaractu |
| Panafricain | 7 | Africa 24, Africanews FR, Business 24 Africa |
| Côte d'Ivoire | 15 | RTI 1, NTV, 7 Info, Ivoire Channel |
| Cameroun | 9 | CRTV News, Allo Ciné, CAM 10 TV |
| Maroc | 9 | 2M, Al Maghribia, Medi1TV Afrique |
| Rwanda | 6 | TV1, TV10, Rwanda TV |
| Algérie | 5 | AL24 News, El-Heddaf TV |
| Burkina Faso | 4 | RTB, RTB 3, Savane TV, Filinfo TV |
| Bénin | 4 | TVC Bénin, ADO TV, Eden TV |
| RD Congo | 4 | EVI TV, LBFD RTV |
| Guinée, Togo, Congo, Tunisie | 3 chacun | Espace TV, Kalac TV, Mosaïque FM |
| Niger, Mali, Mauritanie, Tchad | 1 à 2 | Télé Sahel, D3 TV, Sahara 24, Télé Tchad |

Marqueurs dans les noms : `[Pas 24/7]` (émission par tranches), `[Géo-bloqué]` (réservé à certains pays).

## Pourquoi RTS, TFM, 2STV, Walf TV et SenTV ne sont qu'en YouTube

Ces chaînes sont hébergées par ACAN Group sur un serveur Wowza dont le manifeste HLS exige un jeton signé
(`wmsAuthSign`, lié à la session et valable dix minutes). Aucun flux ouvert n'existe ; toutes les URL qui circulent
pour ces chaînes (69.64.57.208, live3.acangroup.org, uvotv, push2stream) sont mortes ou renvoient 403.
Les entrées YouTube pointent vers la page `/live` de chaque chaîne : elles se lisent avec `yt-dlp -g <url>` ou
un lecteur qui sait résoudre YouTube (VLC récent, extension YouTube de Kodi). Ces chaînes ne diffusent pas en
continu sur YouTube ; hors direct, l'entrée reste vide.

Attention : les « RTS 1 » et « RTS 2 » hébergées sur `webtvstream.bhtelecom.ba`, présentes dans beaucoup de
listes « Sénégal », sont la télévision serbe. Elles ne figurent pas ici.

## Revérifier les flux

```
python scripts/verifier.py afrique.m3u
```

Le script teste chaque flux en parallèle et sort en erreur si un flux est en panne.

## Sources

Seuls des flux publics diffusés librement par les chaînes ou leurs hébergeurs sont retenus.
Agrégats consultés : [iptv-org/iptv](https://github.com/iptv-org/iptv), [Free-TV/IPTV](https://github.com/Free-TV/IPTV),
dépôts communautaires (spookyhost1/yarr-stremio, drsof1968/iptv, bermufine/senegal, Lams94/afr), ainsi que les
serveurs sen-gt.com et acangroup.org. Les détenteurs de droits qui souhaitent le retrait d'un flux peuvent ouvrir une issue.
