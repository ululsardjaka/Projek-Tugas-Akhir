from requests import get

# BMKG Indonesia (data.bmkg.go.id)
def bmkg():
    url = "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json"
    responseJson = get(url).json()
    gempa = responseJson["Infogempa"]["gempa"]

    tanggal = gempa["Tanggal"]
    jam = gempa["Jam"]
    lintang = gempa["Lintang"]
    bujur = gempa["Bujur"]
    magnitude = gempa["Magnitude"]
    kedalaman = gempa["Kedalaman"]
    dirasakan = gempa["Dirasakan"]
    potensi = gempa["Potensi"]
    lokasi = gempa["Wilayah"]
    
    text = f"Gempa terakhir dari BMKG menunjukan pada tanggal {tanggal}, pukul {jam} terjadi gempa bumi bermagnitudo {magnitude} pada kedalaman {kedalaman}. Di {lokasi} dan {dirasakan}, berpotensi \"{potensi}\""
    return {
        "text": text,
        "map": f"https://data.bmkg.go.id/DataMKG/TEWS/{gempa['Shakemap']}",
        "google_map": f"https://www.google.com/maps/search/?api=1&query={lintang},{bujur}"
    }