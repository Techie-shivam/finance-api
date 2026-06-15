def save_dataframe(df, output_path):

    df.to_csv(
        output_path,
        index=False
    )

    print(f"CSV saved at {output_path}")