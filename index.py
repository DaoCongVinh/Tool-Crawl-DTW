# spotify_scraper.py
import os
import time
import re
import requests
from bs4 import BeautifulSoup
from typing import Optional, List, Dict
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# ========== CONFIG ==========
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET", "YOUR_CLIENT_SECRET")
# ============================

def spotify_client():
    """Create and return a Spotipy client using Client Credentials flow."""
    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager, requests_timeout=10, retries=3)
    return sp

# ---------- Helpers ----------
def normalize_number_text(s: str) -> int:
    """Convert '1,234', '1.2M', '12K' into integer (approx)."""
    s = s.strip()
    if s == "":
        return 0
    s = s.replace(',', '').replace('.', '')
    # crude heuristics for K/M if spelled:
    if s.endswith('K') or s.endswith('k'):
        return int(float(s[:-1]) * 1_000)
    if s.endswith('M') or s.endswith('m'):
        return int(float(s[:-1]) * 1_000_000)
    try:
        return int(re.sub(r'\D', '', s))
    except:
        return 0

def try_parse_monthly_listeners_from_artist_page(artist_id: str) -> Optional[int]:
    """
    Attempt to scrape open.spotify.com/artist/{id}/about for 'Monthly listeners'.
    WARNING: scraping spotify.com may violate their terms. This is best-effort and may break.
    Returns integer monthly listeners or None if not found.
    """
    url = f"https://open.spotify.com/artist/{artist_id}/about"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; DataCollector/1.0; +https://example.com/bot)",
        # avoid sending cookies or auth
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None
        html = r.text

        # Strategy A: look for "Monthly listeners" visible string and a nearby number
        if "Monthly listeners" in html:
            # naive parse: find 'Monthly listeners' and grab following digits/strings
            idx = html.find("Monthly listeners")
            snippet = html[idx: idx + 300]
            m = re.search(r"Monthly listeners[^0-9A-Za-z]{1,20}([\d,\.KMkmb]+)", snippet)
            if m:
                return normalize_number_text(m.group(1))

        # Strategy B: the page includes JSON blobs; try to find "monthly_listeners" like tokens
        m2 = re.search(r'monthly_listeners[^:\"]*[:\"]\s*([0-9,\.KMk]+)', html, flags=re.IGNORECASE)
        if m2:
            return normalize_number_text(m2.group(1))

        # Strategy C: fallback - parse human visible number after the label in rendered HTML
        soup = BeautifulSoup(html, "html.parser")
        # find element that contains the label text
        label_tags = soup.find_all(string=re.compile(r"Monthly listeners", re.IGNORECASE))
        for label in label_tags:
            parent = label.parent
            # search siblings
            if parent:
                sibling_text = parent.get_text(separator=" ").strip()
                # try to find number inside sibling_text
                m3 = re.search(r'([\d,\.KMk]+)\s*(?:monthly listeners)?', sibling_text)
                if m3:
                    return normalize_number_text(m3.group(1))
        return None
    except Exception as e:
        # network/parsing errors -> return None (best-effort)
        return None

# ---------- Core functions ----------
def get_track_info(sp: spotipy.Spotify, track_id: str) -> Dict:
    """
    Returns metadata for a track id (id or URI or full url).
    Includes: name, artists, album, duration_ms, popularity (0-100), explicit, url.
    """
    t = sp.track(track_id)
    info = {
        "id": t["id"],
        "name": t["name"],
        "artists": [{"id": a["id"], "name": a["name"]} for a in t["artists"]],
        "album": {"id": t["album"]["id"], "name": t["album"]["name"]},
        "duration_ms": t["duration_ms"],
        "explicit": t["explicit"],
        "popularity": t.get("popularity"),  # 0-100 (proxy for plays)
        "external_url": t["external_urls"].get("spotify"),
    }
    return info

def get_tracks_from_playlist(sp: spotipy.Spotify, playlist_id: str, limit: int = 100) -> List[Dict]:
    """
    Get tracks metadata from a playlist. Returns list of track info dicts.
    playlist_id can be full URL or id.
    """
    results = sp.playlist_items(playlist_id, additional_types=["track"], limit=100)
    tracks = []
    while True:
        for item in results["items"]:
            if item["track"] is None:
                continue
            track = item["track"]
            tracks.append({
                "id": track["id"],
                "name": track["name"],
                "artists": [a["name"] for a in track["artists"]],
                "album": track["album"]["name"],
                "popularity": track.get("popularity"),
                "external_url": track["external_urls"].get("spotify")
            })
            if limit and len(tracks) >= limit:
                return tracks[:limit]
        if results.get("next"):
            results = sp.next(results)
        else:
            break
    return tracks

def get_artist_info(sp: spotipy.Spotify, artist_id: str) -> Dict:
    """
    Returns artist info: id, name, genres, followers, popularity, monthly_listeners (best-effort scraped)
    """
    a = sp.artist(artist_id)
    artist = {
        "id": a["id"],
        "name": a["name"],
        "genres": a.get("genres", []),
        "followers": a.get("followers", {}).get("total"),
        "popularity": a.get("popularity"),  # 0-100
        "monthly_listeners": None
    }
    # best-effort scrape
    try:
        ml = try_parse_monthly_listeners_from_artist_page(artist_id)
        artist["monthly_listeners"] = ml
    except Exception:
        artist["monthly_listeners"] = None
    return artist

# ---------- Example usage ----------
if __name__ == "__main__":
    if CLIENT_ID == "YOUR_CLIENT_ID" or CLIENT_SECRET == "YOUR_CLIENT_SECRET":
        print("Please set your CLIENT_ID and CLIENT_SECRET (env SPOTIPY_CLIENT_ID/SPOTIPY_CLIENT_SECRET or edit constants).")
        raise SystemExit(1)

    sp = spotify_client()
    # Example: get a track
    example_track = "3n3Ppam7vgaVa1iaRUc9Lp"  # use any track id or url
    track_info = get_track_info(sp, example_track)
    print("Track info (metadata + popularity):")
    print(track_info)

    # Example: get artist info (includes followers and best-effort monthly listeners)
    artist_id = track_info["artists"][0]["id"]
    artist_info = get_artist_info(sp, artist_id)
    print("\nArtist info (followers, popularity, monthly_listeners best-effort):")
    print(artist_info)

    # Example: get tracks from a playlist (first 50)
    # playlist_url_or_id = "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"
    # playlist_tracks = get_tracks_from_playlist(sp, playlist_url_or_id, limit=50)
    # print("\nPlaylist tracks (first 50):")
    # for t in playlist_tracks[:10]:
    #     print(t)
