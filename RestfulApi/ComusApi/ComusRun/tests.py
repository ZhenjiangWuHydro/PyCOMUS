import pandas as pd

data = {
    "1": {"multr": 1, "num_step": 1, "period_len": 1},
    "2": {"multr": 1, "num_step": 1, "period_len": 1}
}

df = pd.DataFrame(data.values(), index=data.keys())
df.index.name = 'IPER'
df = df[['period_len', 'num_step', 'multr']].rename(columns={'period_len': 'PERLEN', 'num_step': 'NSTEP', 'multr': 'MULTR'})

print(df)
