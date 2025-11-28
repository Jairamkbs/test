# %%


# %%
#move files old
import os
import shutil
from datetime import datetime

# --- Folder paths ---
holidays_folder = r"C:\Users\bomma\Desktop\Daily Reports\News\News dates\Holidays"
news_folder = r"C:\Users\bomma\Desktop\Daily Reports\News\News dates\news"
old_data_folder = r"C:\Users\bomma\Desktop\Daily Reports\News\News dates\Old data"

# --- Create today's folder name (e.g., 16-10-2025) ---
today_folder = datetime.now().strftime("%d-%m-%Y")
destination_folder = os.path.join(old_data_folder, today_folder)

# --- Create folder if not exists ---
os.makedirs(destination_folder, exist_ok=True)

# --- Function to move all files from one folder ---
def move_files(src_folder, dst_folder):
    for file_name in os.listdir(src_folder):
        src_path = os.path.join(src_folder, file_name)
        dst_path = os.path.join(dst_folder, file_name)
        if os.path.isfile(src_path):
            shutil.move(src_path, dst_path)
            print(f"Moved: {file_name}")

# --- Move files from both folders ---
move_files(holidays_folder, destination_folder)
move_files(news_folder, destination_folder)

print(f"\n✅ All files moved successfully to: {destination_folder}")


# %%


# %%
# ✅ Create a <current_year>.csv with Date, Day, and Working day columns
import os
import pandas as pd
from datetime import date

# --- 1) SET YOUR FOLDER PATH HERE ---
FOLDER = r"C:\Users\bomma\Desktop\Daily Reports\News\News dates\news"   # <- change if needed

# --- 2) Build date range for the current year ---
year = date.today().year
start = f"{year}-01-01"
end   = f"{year}-12-31"

# --- 3) Create the dataframe with Date and Day name ---
dates = pd.date_range(start, end, freq="D")
df = pd.DataFrame({
    "Date": dates.strftime("%d-%m-%Y"),   # dd-mm-yyyy format
    "Day": dates.day_name()               # Monday, Tuesday, ...
})

# --- 4) Working day flag: "No" for Sat/Sun, else "Yes" ---
df["Working day"] = df["Day"].isin(["Saturday", "Sunday"]).map({True: "No", False: "Yes"})

# --- 5) Save as <year>.csv in the folder ---
os.makedirs(FOLDER, exist_ok=True)
out_path = os.path.join(FOLDER, f"{year}.csv")
df.to_csv(out_path, index=False)

print(f"✅ Saved: {out_path}")


# %%
#Next go to download nse holidays list in that it is no csv file download  so i copy that table and save in excel in excel folder holidays folder

# %%
import pandas as pd

# --- File paths ---
excel_file = r"C:\Users\bomma\Desktop\Daily Reports\News\News dates\Holidays\Book1.xlsx"
csv_file = r"C:\Users\bomma\Desktop\Daily Reports\News\News dates\Holidays\Holidays.csv"

# --- Read Excel file ---
df = pd.read_excel(excel_file)

# --- Save as CSV file (new name: Holidays.csv) ---
df.to_csv(csv_file, index=False)

print("✅ Excel file converted successfully as 'Holidays.csv'")


# %%
import pandas as pd

# 📁 Your CSV file path
file_path = r"C:\Users\bomma\Desktop\Daily Reports\News\News dates\Holidays\Holidays.csv"

# 🧩 Read the CSV file
df = pd.read_csv(file_path)

# 🗓️ Convert 'Date' column from yyyy-mm-dd → dd-mm-yyyy
df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%d-%m-%Y')

# 💾 Save the updated data back to the same CSV file
df.to_csv(file_path, index=False)

print("✅ Date column updated to 'dd-mm-yyyy' format successfully!")


# %%
print("holydays is there that date add in news csv file")

# %%
#https://chatgpt.com/share/68f0eb63-0b0c-800a-9de5-0becd5b12217
import pandas as pd
import os

# --- File paths ---
news_folder = r"C:\Users\bomma\Desktop\Daily Reports\News\News dates\news"
holiday_file = r"C:\Users\bomma\Desktop\Daily Reports\News\News dates\Holidays\Holidays.csv"

# --- Step 1: Find the CSV file inside the 'news' folder ---
for file in os.listdir(news_folder):
    if file.endswith(".csv"):
        news_file = os.path.join(news_folder, file)
        break

# --- Step 2: Read both CSV files ---
news_df = pd.read_csv(news_file)
holiday_df = pd.read_csv(holiday_file)

# --- Step 3: Compare dates and mark Holiday_day ---
news_df['Holiday_day'] = news_df['Date'].apply(
    lambda x: 'Yes' if x in holiday_df['Date'].values else 'No'
)

# --- Step 4: Save the updated CSV file ---
news_df.to_csv(news_file, index=False)
print(f"✅ Updated file saved successfully: {news_file}")


# %%
#hi this is my folder path "C:\Users\bomma\Desktop\Daily Reports\News\News dates\news"  in this one csv file is there take that in that file column name "Working day"  and "Holiday_day"   both are Yes in  mention "No" and both are No  mention "No"   if  "Working day"  is  data is "Yes"  then "Holiday_day"   data is "No"   then mention "Yes"   in column name "Working_status"  w rite a python code for this

import pandas as pd
import os

# 📂 Folder path where your CSV file is present
folder_path = r"C:\Users\bomma\Desktop\Daily Reports\News\News dates\news"

# 🔍 Find the CSV file in that folder
for file in os.listdir(folder_path):
    if file.endswith(".csv"):
        file_path = os.path.join(folder_path, file)
        break

# 📘 Read the CSV file
df = pd.read_csv(file_path)

# ✅ Create a new column "Working_status" based on conditions
def check_status(row):
    if row['Working day'] == 'Yes' and row['Holiday_day'] == 'No':
        return 'Yes'
    else:
        return 'No'

df['Working_status'] = df.apply(check_status, axis=1)

# 💾 Save updated file back
df.to_csv(file_path, index=False)

print("✅ 'Working_status' column added successfully.")


# %%
print("dates range pickup")

# %%
#chat gpt conversation  https://chatgpt.com/share/68f0f480-6414-800a-92df-3a75e95d84cc
# ✅ Build "From" and "To" with your latest rule
# - First two rows: "Manualy enter sir"
# - If current "Yes" and previous "Yes": From=prev Yes Date, To=prev Yes Date
# - If current "Yes" after No-block:    From=nearest earlier Yes Date, To=immediately previous row's Date (last No)
# - Other rows: leave From/To blank

import os, glob
import pandas as pd

FOLDER = r"C:\Users\bomma\Desktop\Daily Reports\News\News dates\news"

# --- Load the single CSV in folder ---
csvs = glob.glob(os.path.join(FOLDER, "*.csv"))
if not csvs:
    raise FileNotFoundError("No CSV in folder.")
fp = csvs[0]

df = pd.read_csv(fp, dtype=str).fillna("")

# --- Checks ---
for col in ["Date", "Working_status"]:
    if col not in df.columns:
        raise KeyError(f'Missing column: {col}')

# --- First two rows set to manual text ---
if len(df) >= 1: df.loc[0, "Working_status"] = "Manualy enter sir"
if len(df) >= 2: df.loc[1, "Working_status"] = "Manualy enter sir"

# --- Prepare outputs ---
df["From"] = ""
df["To"] = ""

ws = df["Working_status"].tolist()
dates = df["Date"].tolist()
n = len(df)

for i in range(2, n):
    if ws[i] != "Yes":
        continue

    # Case 1: current Yes and previous is also Yes
    if ws[i-1] == "Yes":
        # 👉 Use the previous Yes row's Date for both
        df.at[i, "From"] = dates[i-1]
        df.at[i, "To"]   = dates[i-1]
        continue

    # Case 2: current Yes after a block of No's
    # Walk back over No's to find nearest earlier Yes
    j = i - 1
    while j >= 0 and ws[j] == "No":
        j -= 1

    if j >= 0 and ws[j] == "Yes":
        df.at[i, "From"] = dates[j]      # nearest earlier Yes date
        df.at[i, "To"]   = dates[i-1]    # last No date (row just before current)
    else:
        # No earlier Yes found → leave blank (or set to current date if you prefer)
        df.at[i, "From"] = ""
        df.at[i, "To"]   = ""

# --- Save back ---
df.to_csv(fp, index=False)
print(f"✅ Updated file saved: {fp}")


# %%
import pandas as pd

# --- Paths ---
csv_path = r"C:\Users\bomma\Desktop\Daily Reports\News\News dates\news\2025.csv"

# --- Read CSV as strings (keeps your dd-mm-yyyy as-is) ---
df = pd.read_csv(csv_path, dtype=str).fillna("")

# --- Clean spaces just in case ---
df["From"] = df["From"].str.strip()
df["To"]   = df["To"].str.strip()

# --- Build URL only when both dates are present ---
valid = (df["From"] != "") & (df["To"] != "")

url_prefix = "https://www.nseindia.com/api/corporate-announcements?index=equities&from_date="
url_mid    = "&to_date="
url_suffix = "&reqXbrl=false&csv=true"

# Create/overwrite the URL column; leave empty where dates are missing
df["URL"] = ""
df.loc[valid, "URL"] = (
    url_prefix + df.loc[valid, "From"] + url_mid + df.loc[valid, "To"] + url_suffix
)

# --- Save back to the same file (or change path if you want a new file) ---
df.to_csv(csv_path, index=False)

print(f"✅ URLs created for {valid.sum()} rows; skipped {len(df) - valid.sum()} rows with empty dates.")


# %%
import os
import shutil

# --- Folder paths ---
source_folder = r"C:\Users\bomma\Desktop\Daily Reports\News\News dates\news"
destination_folder = r"C:\Users\bomma\Desktop\Daily Reports\News\News dates\New Year News"

# --- Create destination folder if not exists ---
os.makedirs(destination_folder, exist_ok=True)

# --- Copy and rename each file ---
for file_name in os.listdir(source_folder):
    source_path = os.path.join(source_folder, file_name)
    
    # Copy only if it's a file
    if os.path.isfile(source_path):
        # Get the file extension (.csv, .txt, .xlsx, etc.)
        extension = os.path.splitext(file_name)[1]
        
        # New file name
        new_name = f"My news{extension}"
        destination_path = os.path.join(destination_folder, new_name)
        
        # Copy file
        shutil.copy2(source_path, destination_path)
        print(f"✅ Copied and renamed: {file_name} → {new_name}")

print("🎉 All files copied and renamed successfully!")


# %%



