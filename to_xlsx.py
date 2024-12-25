import json
import pandas as pd

def to_xlsx(all_data, output_json, output_xlxs):
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    # Đọc file JSON
    with open(output_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Chuyển dữ liệu sang DataFrame
    df = pd.DataFrame(data)

    # Xuất DataFrame thành file Excel
    output_file = output_xlxs
    df.to_excel(output_file, index=False, engine='openpyxl')

    print(f"Dữ liệu đã được lưu vào file {output_file}")

    print("Scraping completed for all URLs.")