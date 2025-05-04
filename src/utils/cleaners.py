import pandas as pd

def clean_emergency_services_column(df, source_col='EmergencyServices', target_col='EmergencyServices'):
    """
    Safely transforms TRUE/FALSE emergency service values into 1/0 (int8) and avoids SettingWithCopyWarning.
    """
    # Step 0: Make a safe copy to avoid chained assignment warnings
    df = df.copy()

    # Step 1: Transform TRUE/FALSE -> 1/0
    temp_col = f"__{target_col}_temp__"
    df[temp_col] = df[source_col].apply(
        lambda x: 1 if str(x).strip().upper() == 'TRUE' else 0
    ).astype('int8')

    # Step 2: Drop original and rename
    df.drop(columns=[source_col], inplace=True)
    df.rename(columns={temp_col: target_col}, inplace=True)

    return df

