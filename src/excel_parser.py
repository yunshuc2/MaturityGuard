import pandas as pd
from datetime import datetime
import config

def parse_excel():
    data = []

    # --------------------------
    # 解析 CD 表
    # --------------------------
    try:
        cd_df = pd.read_excel(
            config.EXCEL_PATH,
            sheet_name="CD",
            usecols="A:D",
            header=0,
            converters={
                "Maturity Date": lambda x: datetime.strptime(x, "%m/%d/%Y")  # 首字母大写，格式 MM/DD/YYYY
            }
        )

        # 清理无效行（确保列名正确）
        cd_df = cd_df[cd_df["Bank Name"].notna()]

        for _, row in cd_df.iterrows():
            data.append({
                "name": f"{row['Bank Name']} CD",
                "amount": float(row["Amount($)"]),
                "maturity": row["Maturity Date"],  # 列名首字母大写
                "rate": float(row["Interest rate"])
            })
    except Exception as e:
        print(f"解析CD表时出错: {str(e)}")
        raise  # 调试时抛出详细错误

    # --------------------------
    # 解析 Bonds 表
    # --------------------------
    try:
        bonds_df = pd.read_excel(
            config.EXCEL_PATH,
            sheet_name="Bonds",
            usecols="B:F",
            header=0,
            names=["Maturity Date", "Issue Date", "Type", "Interest Rate", "Amount"],
            converters={
                "Maturity Date": lambda x: datetime.strptime(x, "%m-%d-%Y"),  # 格式 MM-DD-YYYY
                "Issue Date": lambda x: datetime.strptime(x, "%m/%d/%Y")       # 格式 MM/DD/YYYY
            }
        )

        for _, row in bonds_df.iterrows():
            amount = float(str(row["Amount"]).replace("$", "").replace(",", ""))
            data.append({
                "name": f"{row['Type']} Bond",
                "amount": amount,
                "maturity": row["Maturity Date"],
                "rate": float(row["Interest Rate"])
            })
    except Exception as e:
        print(f"解析Bonds表时出错: {str(e)}")
        raise

    return data