"""
© 2017 Hoàng Lê Hải Thanh (Thanh Hoang Le Hai) aka GhostBB
If there are any problems, contact me at mail@hoanglehaithanh.com or 1413492@hcmut.edu.vn 
This project is under [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) (Inherit from NLTK)

# Author: Doan Tran Cao Tri
# University: Ho Chi Minh University of Technology
# Id: 2010733
# Contact: tri.doan218138@hcmut.edu.vn
########################################################################
# Simple Grammar without SEM
########################################################################
"""

file_name = [
    "output_a.txt",
    "output_b.txt",
    "output_c.txt",
    "output_d.txt",
    "output_e.txt",
    "output_f.txt",
]


def write_file(question_number, content, append=False):
    file = open(
        "Output/" + file_name[question_number - 1],
        "a" if append else "w",
        encoding="utf-8",
    )
    file.write(content)
    file.close()


def write_file2(file_name_path, content, append=False):
    file = open(
        file_name_path,
        "a" if append else "w",
        encoding="utf-8",
    )
    file.write(content)
    file.close()
