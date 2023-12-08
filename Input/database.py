import re

raw_database = [
    'ATIME PQ PQ "9AM 1/7"',
    'ATIME PQ PQ "10AM 5/7"',
    'ATIME DN DN "9AM 1/7"',
    'ATIME DN DN "9AM 4/7"',
    'ATIME NT NT "12AM 1/7"',
    'ATIME NT NT "12AM 5/7"',
    'DTIME NT HCMC "7AM 5/7"',
    'DTIME NT HCMC "7AM 1/7"',
    'DTIME DN HCMC "7AM 4/7"',
    'DTIME PQ HCMC "8AM 5/7"',
    'DTIME DN HCMC "7AM 1/7"',
    'DTIME PQ HCMC "7AM 1/7"',
    "RUN-TIME PQ HCM PQ 2:00 HR",
    "RUN-TIME DN HCM DN 2:00 HR",  # sửa nhầm lẫn so với đề: đề là RUN-TIME DN HCM PQ 2:00 HR
    "RUN-TIME NT HCM NT 5:00 HR",  # sửa nhầm lẫn so với đề: đề là RUN-TIME NT HCM PQ 5:00 HR
    "TOUR PQ Phú_Quốc",
    "TOUR DN Đà_Nẵng",
    "TOUR NT Nha_Trang",
    "BY PQ airplane",
    "BY DN airplane",
    "BY NT train",
]


def preprocess_database(database):
    for idx, ds in enumerate(database):
        # Remove double quotes
        ds = re.sub(r'"', "", ds)
        # Replace space between time components with underscore
        ds = re.sub(r"(\d+)([APMapm]+) (\d+)/(\d+)", r"\1\2_\3/\4", ds)
        ds = re.sub(r"(\d+):(\d+) HR", r"\1:\2HR", ds)
        database[idx] = ds
    return database


def post_process_results(results: []):
    for idx, res in enumerate(results):
        res = re.sub(r"PQ", "Phú_Quốc", res)
        res = re.sub(r"DN", "Đà_Nẵng", res)
        res = re.sub(r"NT", "Nha_Trang", res)
        res = re.sub(r"HCM", "Hồ_Chí_Minh", res)
        res = re.sub(r"HCMC", "Hồ_Chí_Minh", res)

        results[idx] = res
    return results


if __name__ == "__main__":
    database = preprocess_database(raw_database)
