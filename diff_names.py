excel_names = [
    "GEETA KUMARI", "SIYA", "DIYA", "GARIMA SHARMA", "JIVESH KUMAR", "GAUTAM", 
    "YAGINI", "LUHANI", "YASHVI", "KHYATI", "GITESH", "DEVANSH", "ABHI", 
    "RISHABH", "MEENAKSHI", "GUNJAN", "DEEPIKA", "KAPIL", "MAYANK", "TANUJ", 
    "SAHIL KUMAR", "TANNU", "KAJAL", "NANCY", "KHUSHAL", "RIYA", "PURVI", 
    "YASH SHARMA", "SHIWANI", "TANISH", "DIYA", "MOHAMMAD ARBAJ KHAN", "HONEY"
]

portal_names = [
    "KAJAL", "KHUSHAL", "TANUJ", "SHIWANI", "NANCY", "SAHIL KUMAR", "TANNU",
    "MAYANK", "RISHABH", "PURVI", "YASH SHARMA", "KAPIL", "MEENAKSHI",
    "DEEPIKA", "RIYA", "ABHI", "GUNJAN", "GITESH", "LUHANI", "GARIMA SHARMA",
    "DIYA", "SIYA", "GEETA KUMARI", "SOURABH", "GAUTAM", "HONEY", "DIYA",
    "MOHAMMAD ARBAJ KHAN"
]

# Normalizing names
excel_names_norm = [n.strip().upper() for n in excel_names]
portal_names_norm = [n.strip().upper() for n in portal_names]

# Which are in excel but NOT in portal?
# Note: we need to handle duplicates like 'DIYA'. There are two 'DIYA's in both.
from collections import Counter
c_excel = Counter(excel_names_norm)
c_portal = Counter(portal_names_norm)

print("Missing from Portal (To be Added):")
for name, count in c_excel.items():
    if c_portal[name] < count:
        diff = count - c_portal[name]
        for _ in range(diff):
            print(f"- {name}")

print("\nExtra in Portal (Not in Excel):")
for name, count in c_portal.items():
    if c_excel[name] < count:
        diff = count - c_excel[name]
        for _ in range(diff):
            print(f"- {name}")

