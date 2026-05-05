import pandas as pd
import requests

# =========================
# 1. BACA DATA EXCEL
# =========================
def read_excel(file_path):
    df = pd.read_excel(file_path)
    return df


# =========================
# 2. KONVERSI ANGKA -> TERBILANG INDONESIA
# =========================
def terbilang(n):
    angka = ["", "satu", "dua", "tiga", "empat", "lima", "enam",
             "tujuh", "delapan", "sembilan", "sepuluh", "sebelas"]

    n = int(n)

    if n < 12:
        return angka[n]
    elif n < 20:
        return terbilang(n - 10) + " belas"
    elif n < 100:
        return terbilang(n // 10) + " puluh " + terbilang(n % 10)
    elif n < 200:
        return "seratus " + terbilang(n - 100)
    elif n < 1000:
        return terbilang(n // 100) + " ratus " + terbilang(n % 100)
    elif n < 2000:
        return "seribu " + terbilang(n - 1000)
    elif n < 1000000:
        return terbilang(n // 1000) + " ribu " + terbilang(n % 1000)
    else:
        return str(n)


# =========================
# 3. TEMPLATE PARAGRAF
# =========================

def paragraf_pembuka(salam):
    return f"{salam}\n\nDengan memohon rahmat Allah SWT, kami menyampaikan laporan zakat fitrah."

def paragraf_judul(judul):
    return f"**{judul}**"

def paragraf_identitas(nama_masjid, alamat):
    return f"Masjid {nama_masjid}\nAlamat: {alamat}"

# =========================
# 4. PARAGRAF RINGKASAN (DARI EXCEL)
# =========================
def paragraf_ringkasan(data):
    """
    data = dict dari excel row
    """

    zakat_beras = data["zakat_beras"]
    zakat_uang = data["zakat_uang"]
    muzaki = data["jumlah_muzaki"]

    infak_beras = data["infak_beras"]
    infak_uang = data["infak_uang"]
    donatur = data["jumlah_donatur"]

    salur_beras = data["penyaluran_beras"]
    salur_uang = data["penyaluran_uang"]
    mustahiq = data["jumlah_mustahiq"]

    sisa_beras = zakat_beras + infak_beras - salur_beras
    sisa_uang = zakat_uang + infak_uang - salur_uang

    teks = f"""
1. Penerimaan Zakat:
Zakat fitrah yang diterima berupa beras sebanyak {zakat_beras} ({terbilang(zakat_beras)}) kg
dan uang sebesar Rp {zakat_uang} ({terbilang(zakat_uang)} rupiah) dari {muzaki} ({terbilang(muzaki)}) muzaki.

2. Penerimaan Infak:
Infak yang diterima berupa beras sebanyak {infak_beras} ({terbilang(infak_beras)}) kg
dan uang sebesar Rp {infak_uang} ({terbilang(infak_uang)} rupiah) dari {donatur} ({terbilang(donatur)}) donatur.

3. Penyaluran:
Penyaluran zakat dan infak berupa beras sebanyak {salur_beras} ({terbilang(salur_beras)}) kg
dan uang sebesar Rp {salur_uang} ({terbilang(salur_uang)} rupiah)
kepada {mustahiq} ({terbilang(mustahiq)}) mustahiq.

4. Saldo Akhir:
Sisa beras sebanyak {sisa_beras} ({terbilang(sisa_beras)}) kg
dan sisa uang sebesar Rp {sisa_uang} ({terbilang(sisa_uang)} rupiah).
"""
    return teks


# =========================
# 5. PARAGRAF PENUTUP
# =========================
def paragraf_penutup(pesan):
    return f"""
Demikian laporan ini kami sampaikan.

{pesan}

Wassalamu’alaikum warahmatullahi wabarakatuh.
"""


# =========================
# 6. GROC API (PARAGRAF 5 ENHANCEMENT)
# =========================
def refine_with_groq(paragraf, api_key):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert in formal Indonesian administrative reporting."
            },
            {
                "role": "user",
                "content": f"Perhalus dan rapikan paragraf laporan zakat berikut agar formal, jelas, dan enak dibaca:\n\n{paragraf}"
            }
        ],
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]


# =========================
# 7. MAIN PROGRAM
# =========================
def main():
    file_excel = "data_zakat.xlsx"
    api_key = "YOUR_GROQ_API_KEY"

    df = read_excel(file_excel)

    for _, row in df.iterrows():

        # input manual user
        salam = input("Masukkan salam pembuka: ")
        judul = input("Masukkan judul laporan: ")
        nama_masjid = input("Nama masjid: ")
        alamat = input("Alamat masjid: ")
        pesan_penutup = input("Pesan penutup: ")

        p1 = paragraf_pembuka(salam)
        p2 = paragraf_judul(judul)
        p3 = paragraf_identitas(nama_masjid, alamat)

        p4_raw = paragraf_ringkasan(row.to_dict())

        # refining paragraf 4 pakai LLM
        p4 = refine_with_groq(p4_raw, api_key)

        p5 = paragraf_penutup(pesan_penutup)

        laporan = f"""
{p1}

{p2}

{p3}

{p4}

{p5}
"""

        print("\n================ LAPORAN ================\n")
        print(laporan)


if __name__ == "__main__":
    main()