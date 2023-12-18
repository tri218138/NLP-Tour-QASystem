# Hệ thống hỏi đáp các tour du lịch

Hệ thống hỏi đáp các tour du lịch là đề tài hấp dẫn ứng dụng Xử lý ngôn ngữ tự nhiên để truy vấn dữ liệu và trả lời câu hỏi. Gửi lời cảm ơn đến anh Hoàng Lê Hải Thanh đã hỗ trợ em phần baseline của hệ thống bằng ngôn ngữ tiếng Anh và truy vấn với _WHICH_. Ở phần này, em sẽ cải tiến với ngôn ngữ tiếng Việt và hỗ trợ cho 4 loại câu hỏi _WHICH_, _HOWLONG_, _WHEN_, _YESNO_.

-   Co-Author: Doan Tran Cao Tri
-   University: Ho Chi Minh University of Technology
-   Id: 2010733
-   Contact: tri.doan218138@hcmut.edu.vn

## 1. Demo

```
đi từ Hồ Chí Minh tới Nha Trang hết bao lâu?
```

```
-------------Parsed structure-------------
(S[GAP=?np, SEM=<WHQUERY(?np,(SOURCE(TOUR(NAME('HoChiMinh'))) & DEST(TOUR(NAME('NhaTrang'))) & IN(\n.HOWLONG(t3,n))))>]
  (VP[SEM=<(SOURCE(TOUR(NAME('HoChiMinh'))) & DEST(TOUR(NAME('NhaTrang'))) & IN(\n.HOWLONG(t2,n)))>]
    (VP[SEM=<(SOURCE(TOUR(NAME('HoChiMinh'))) & DEST(TOUR(NAME('NhaTrang'))))>]
      (VP[SEM=<SOURCE(TOUR(NAME('HoChiMinh')))>, VAR=?v]
        (V[] đi)
        (PP[SEM=<SOURCE(TOUR(NAME('HoChiMinh')))>]
          (P-LEAVE[SEM=<LEAVE>] từ)
          (TOUR-CNP[SEM=<TOUR(NAME('HoChiMinh'))>]
            (TOUR-NAME[SEM=<NAME('HoChiMinh')>] Hồ_Chí_Minh))))
      (PP[SEM=<DEST(TOUR(NAME('NhaTrang')))>]
        (P-ARRIVE[SEM=<ARRIVE>] tới)
        (TOUR-CNP[SEM=<TOUR(NAME('NhaTrang'))>]
          (TOUR-NAME[SEM=<NAME('NhaTrang')>] Nha_Trang))))
    (PP[SEM=<IN(\n.HOWLONG(t3,n))>]
      (P[SEM=<IN>] hết)
      (NP[SEM=<\n.HOWLONG(t2,n)>]
        (HOWLONG-QDET[SEM=<\t.HOWLONG(t)>, VAR=<t1>] bao_lâu)))))
```

```
-------------Parsed logical form-------------
WHQUERY(?np (SOURCE(TOUR(NAME('HoChiMinh'))) & DEST(TOUR(NAME('NhaTrang'))) & IN(\n.HOWLONG(t3 n))))
```

```
-------------Procedure semantics-------------
(PRINT-ALL ?t3 (TOUR ?tr) (ATIME ?tr NT ?at) (DTIME ?tr HCM ?dt) (RUN-TIME ?tr HCM NT t3) (BY ?tr ?ve))
```

```
-------------Retrieved result-------------
5:00HR
```

## 2. Cấu trúc hệ thống

Cài đặt thư viện

```
pip install -r requirements.txt
```

Gồm 4 files chính

-   [main.py](main.py) : File chạy chương trình.
-   [nlp_parser.py](nlp_parser.py) : Parser.
-   [nlp_data.py](nlp_data.py) : Load data.
-   [nlp_file.py](nlp_file.py) : Xử lý file.

files khác:

-   [grammar.fcfg](grammar.fcfg) : The free context grammar file.

## 3. Chạy mẫu

Run by Docker

```sh
docker build --network=host -t nlp222 .
docker run --rm -v $S_OUT:/nlp/output -v $S_IN:/nlp/input nlp222
```

Use default arguments:

```sh
$python3 main.py # for all sample
```

Use custom arguments:

```sh
$python3 main.py --input --question [question] --rule_file_name [rule_file_name]
```

Usage:

-   `--question` : The input question in English. Default: "_Máy bay nào đến thành phố Huế lúc 13:30HR ?_"
-   `--rule_file_name` : The context free grammar file (.fcfg). Default: _grammar.fcfg_

Ví dụ

```sh
$python3 main.py
$python3 main.py --input --rule_file_name=grammar.fcfg --question=1
$python3 main.py --input --rule_file_name=grammar.fcfg --question="đi từ Hồ Chí Minh tới Nha Trang hết bao lâu?"
```

## 4. Database

```
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
```
