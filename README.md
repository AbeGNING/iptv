# IPTV Afrique francophone

Playlist M3U de chaînes de télévision africaines francophones, avec un accent sur le Sénégal.
117 flux HLS vérifiés en deux passes (réponse HTTP 200/206, manifeste HLS avec variantes ou segments) le 4 octobre 2026, plus un script pour les grandes chaînes sénégalaises à jeton.

## Utilisation

URL courte à coller dans VLC, Kodi, TiviMate, IPTV Smarters ou tout lecteur compatible M3U :

```
https://abegning.github.io/iptv/afrique.m3u
```

Adresse de secours (même fichier, servi par GitHub directement) :

```
https://raw.githubusercontent.com/AbeGNING/iptv/main/afrique.m3u
```

## Contenu de la playlist

| Groupe | Flux | Exemples |
|---|---|---|
| Sénégal | 9 | iTV Sénégal, A2i TV, A2i Religion, Asfiyahi TV, GMS TV, Louga TV, SenJeunes TV, Seneweb TV, Diaspora 24 |
| Côte d'Ivoire | 26 | RTI 1, RTI 2, RTI La 3 (1080p via Kaltura), NCI (1080p), Life TV, 7 Info, NTV, Fitini TV, L'Intelligent TV, Novela Channel |
| Cameroun | 15 | CRTV (1080p), CRTV News, Afrique Media, Allo Ciné, CAM 10 TV, Kemet TV, Heaven TV, TR24 |
| Panafricain et international | 17 | France 24, TV5MONDE Info, Africa 24, Africanews FR, Business 24, Trace Africa, Trace Urban FR, Trace Gospel FR |
| Maroc | 9 | 2M, Al Maghribia, Medi1TV Afrique |
| Rwanda | 6 | TV1, TV10, Rwanda TV |
| RD Congo | 5 | EVI TV, LBFD RTV, RL PRO TV |
| Burkina Faso, Bénin, Algérie | 4 chacun | RTB, RTB 3, RTB Guiriko, ORTB 1, TVC Bénin, AL24 News |
| Guinée, Togo, Congo, Tunisie | 3 chacun | Espace TV, Kalac TV, Mosaïque FM |
| Mali, Niger, Mauritanie, Tchad | 1 à 2 | D3 TV, Télé Sahel, Sahara 24, Télé Tchad |
| Sénégal (YouTube, dernier recours) | 4 | 2STV, TFM, RTS, Dakaractu |

Marqueurs : `[Pas 24/7]` (émission par tranches), `[Géo-bloqué]` (réservé à certains pays), `(miroir)` (second hébergeur de la même chaîne).
Afrique Media exige l'en-tête `Referer: https://odysee.com` : l'entrée porte un `#EXTVLCOPT` pour VLC et le suffixe `|Referer=` pour Kodi/TiviMate.

## Grandes chaînes sénégalaises : SenTV, Walf TV, 7TV, Leral TV, RTS 1 et 2

Elles ne sont pas dans la playlist statique, et aucune liste publique ne peut les contenir durablement :

- **SenTV, Walf TV, 7TV, Leral TV, Télé École, Asfiyahi TV, Malikia TV, Global TV HD, CIS Media TV, RTJ TV** sont servies par ACAN Group (`live1.acangroup.org:1929`) derrière un jeton `wmsAuthSign` valable dix minutes. Le jeton s'obtient sans navigateur sur l'API publique `tveapi.acan.group` et ouvre toutes ces chaînes à la fois.
- **RTS 1, RTS 2, RSI, RFM** diffusent sur Dailymotion (identifiants de direct permanents) ; l'URL HLS, elle, expire après un quart d'heure et le CDN refuse les adresses IP de centres de données ou de VPN.

Le script `scripts/senegal_direct.py` fabrique à la demande une playlist personnelle avec des jetons frais :

```
python scripts/senegal_direct.py
vlc senegal-direct.m3u      # à ouvrir dans les dix minutes
```

Testé le 4 octobre 2026 : les dix chaînes ACAN se décodent (ffprobe, H.264 ; SenTV et Walf TV en 1920x1080), et une lecture engagée se poursuit au-delà des dix minutes (13 minutes continues mesurées avec ffmpeg) : le jeton ne conditionne que l'ouverture du flux, pas sa durée. Dailymotion n'a pu être validé que depuis une adresse africaine ; depuis un VPN il renvoie 403.

Sans flux ouvert d'aucune sorte : **TFM** (Dailymotion hors antenne, serveur bozztv fermé), **2STV** (serveur MediaMTX sans flux publié), **DTV**, **Touba TV**, **Lamp Fall TV**, **Al Mouridiyyah TV**, **Mouride TV**. Leurs directs YouTube restent la seule voie (`yt-dlp -g <url>`).

Attention : les « RTS 1 » et « RTS 2 » hébergées sur `webtvstream.bhtelecom.ba`, présentes dans beaucoup de listes « Sénégal », sont la télévision serbe. Elles ne figurent pas ici.

## Chaînes recherchées sans résultat

Côte d'Ivoire : A+ Ivoire (bouquet Canal+, payant). Cameroun : Canal 2 International, Equinoxe TV, Vision 4, STV, Info TV, DBS TV, Vox Africa (sites injoignables ou sans lecteur, aucun flux dans les sources publiques). Afrique de l'Ouest : ORTM, Africable, RTG Guinée, TVT Togo, Gabon 1ère, Télé Congo, RTNC (anciens serveurs éteints).

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
