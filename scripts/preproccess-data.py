import pandas as pd

df = pd.read_csv("data/raw/manufacturing-quality-control-dataset.csv")

# Даты
df['inspection_date'] = pd.to_datetime(df['inspection_date'], errors='coerce')
df['production_date'] = pd.to_datetime(df['production_date'], errors='coerce')

# Дефекты
df['defect_type'] = df['defect_type'].fillna('NO_DEFECT')

df['defect_severity'] = (
    df['defect_severity']
    .fillna(0)
    .astype(int)
)

df['defect_count'] = (
    df['defect_count']
    .fillna(0)
    .astype(int)
)

# Логическое поле
df['rework_required'] = df['rework_required'].astype(bool)

print(df.dtypes)

df.to_csv("data/processed/manufacturing_quality_clean.csv", index=False)
print("✓ Preprocessing completed successfully")
