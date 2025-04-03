import pandas as pd
from datetime import datetime
from pathlib import Path

def salvar_excel(df):
    data_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"imoveis_{data_str}.xlsx"
    path = Path("data")
    path.mkdir(exist_ok=True)
    full_path = path / filename
    df.to_excel(full_path, index=False)
    print(f"Excel salvo como: {full_path}")
