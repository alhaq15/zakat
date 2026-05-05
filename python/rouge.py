from rouge_score import rouge_scorer
import pandas as pd

# =========================
# 1. CONTOH DATA
# =========================
data = [
    {
        "id": 1,
        "reference": "Penerimaan zakat fitrah berupa beras 100 kg dan uang Rp 2.000.000 dari 50 muzaki.",
        "generated": "Zakat fitrah yang diterima adalah 100 kg beras dan Rp 2.000.000 dari 50 orang muzaki."
    },
    {
        "id": 2,
        "reference": "Infak yang terkumpul berupa 20 kg beras dan Rp 500.000 dari 10 donatur.",
        "generated": "Infak terkumpul sebesar 20 kg beras dan uang Rp 500.000 yang berasal dari 10 donatur."
    },
    {
        "id": 3,
        "reference": "Penyaluran zakat diberikan kepada 30 mustahiq berupa 90 kg beras dan Rp 1.800.000.",
        "generated": "Zakat telah disalurkan kepada 30 mustahiq dengan total 90 kg beras dan Rp 1.800.000."
    }
]

# =========================
# 2. INIT ROUGE SCORER
# =========================
scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

results = []

# =========================
# 3. HITUNG ROUGE PER DATA
# =========================
for item in data:
    scores = scorer.score(item["reference"], item["generated"])

    results.append({
        "ID": item["id"],

        # ROUGE-1
        "R1_P": scores["rouge1"].precision,
        "R1_R": scores["rouge1"].recall,
        "R1_F": scores["rouge1"].fmeasure,

        # ROUGE-2
        "R2_P": scores["rouge2"].precision,
        "R2_R": scores["rouge2"].recall,
        "R2_F": scores["rouge2"].fmeasure,

        # ROUGE-L
        "RL_P": scores["rougeL"].precision,
        "RL_R": scores["rougeL"].recall,
        "RL_F": scores["rougeL"].fmeasure,
    })

# =========================
# 4. BUAT DATAFRAME
# =========================
df = pd.DataFrame(results)

# =========================
# 5. RATA-RATA (MEAN SCORE)
# =========================
mean_scores = df.mean(numeric_only=True)

# =========================
# 6. OUTPUT
# =========================
print("\n===== HASIL ROUGE PER DATA =====\n")
print(df)

print("\n===== RATA-RATA SCORE =====\n")
print(mean_scores)