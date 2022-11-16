# %%
import pandas as pd

# %%
path = "/src/data/WhiskyDatabase.csv"
df = pd.read_csv(path)
# %%
df = df.dropna()
df = df.reset_index(drop=True)
# write not nan df to csv file
path = "/src/data/WhiskyDatabase_not_nan.csv"
df.to_csv(path, index=False)

# %%
def create_primary_score(df):
    # get columns
    def _create_dict(column: str) -> dict:
        # create a dictionary of the column
        column_dict = df[column].value_counts().to_dict()
        column_dict = {
            k: v
            for k, v in sorted(
                column_dict.items(), key=lambda item: item[1], reverse=True
            )
        }
        column_dict = {k: i for i, k in enumerate(column_dict.keys())}
        return column_dict

    primary_score = "Primary Score"
    columns = df.columns
    drop_columns = ["Whisky", "Meta Critic", "STDEV", "#", "Primary Score"]
    columns = [column for column in columns if column not in drop_columns]
    df[primary_score] = [0] * len(df)
    for column in columns:
        column_dict = _create_dict(column)
        score_list = []
        print(column)
        print(column_dict)
        for key, value in df[column].items():
            score_list.append(column_dict[value])
        df[primary_score] += score_list
        # break

    return df


# %%
df = create_primary_score(df)
# %%
df
# %%
df = df.sort_values(by=["Primary Score"], ascending=False)
df = df.reset_index(drop=True)
# %%
df_200 = df[:200]

# %%
df_200.groupby("Country").count()

# %%
# write 100 random rows to csv file
path = "/src/data/WhiskyDatabase_200.csv"
df.to_csv(path, index=False)

# %%
