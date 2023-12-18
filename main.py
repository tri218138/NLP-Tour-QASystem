"""
Thanks Hoàng Lê Hải Thanh for baseline source
publish from https://github.com/hoanglehaithanh/NLP2017_Assignment in English
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
import re
from nltk import grammar, parse
import argparse

from Models.nlp_parser import parse_to_procedure
from Models.nlp_data import retrieve_result
from Models.nlp_file import write_file, write_file2
from Input.database import post_process_results
from Input.query import customer_queries


def main(args):
    """
    Main entry point for the program
    """
    # Load grammar from .fcfg file
    print("-------------Loading grammar---------------------")
    nlp_grammar = parse.load_parser(args.rule_file_name, trace=0)
    print("Grammar loaded at {}".format(args.rule_file_name))
    write_file(1, str(nlp_grammar.grammar()))

    question = args.question
    print(question)

    # Get parse tree
    print("-------------Parsed structure-------------")
    tree = nlp_grammar.parse_one(question.replace("?", "").split())
    print(tree)
    write_file(2, str(tree))
    write_file(3, str(tree))

    # Parse to logical form
    print("-------------Parsed logical form-------------")
    # print(question)
    logical_form = str(tree.label()["SEM"]).replace(",", " ")
    print(logical_form)
    write_file(4, str(logical_form))

    # Get procedure semantics
    print("-------------Procedure semantics-------------")
    procedure_semantics = parse_to_procedure(tree)
    for index, procedure_semantic in enumerate(procedure_semantics):
        print(procedure_semantic["procedure"])
        write_file(5, procedure_semantic["procedure"], index)

    # Retrive result:
    print("-------------Retrieved result-------------")
    for index, procedure_semantic in enumerate(procedure_semantics):
        results = retrieve_result(procedure_semantic)
        results = post_process_results(results)
        if len(results) == 0:
            print("No result found!")
        else:
            for result in results:
                print(result, end=" ", flush=True)
            print("")
            write_file(6, " ".join(results) + "\n", index)

            if not args.input:
                write_file2(
                    f"output/p2-q-{args.id}.txt", " ".join(results) + "\n", index
                )


FIX_WORDS = [
    "có thể",
    "nhắc lại",
    "tất cả",
    "được không",
    "Phú Quốc",
    "Hồ Chí Minh",
    "Đà Nẵng",
    "Nha Trang",
    "bao lâu",
    "bao nhiêu",
    "phương tiện",
    "lịch trình",
    "bao gồm",
    "xuất phát",
    "thời gian",
    "sử dụng",
    "phương tiện",
    "tàu hỏa",
    "máy bay",
]
STOP_WORDS = ["em", "có thể", "được không", "vậy", "bạn", "nhỉ"]


def preprocess_query(query: str):
    query = query[0].lower() + query[1:]
    query = re.sub(r"T[P|p]\.", "TP. ", query)
    query = re.sub(r",", " và ", query)
    query = re.sub(r"\?", " ? ", query)
    query = re.sub(r" HR", "HR", query)

    for word in STOP_WORDS:
        query = re.sub(word, "", query)
    for word in FIX_WORDS:
        query = re.sub(word, word.replace(" ", "_"), query)
    return query


def get_query(index: str = "1"):
    try:
        return customer_queries[int(index) - 1]
    except:
        return {
            "0": "",
            # "1": "em có thể nhắc lại tất cả các tour được không?",  # Phú_Quốc Đà_Nẵng Nha_Trang
            # "2": "đi từ Hồ Chí Minh tới Nha Trang hết bao lâu?",  # 5:00HR
            # "3": "đi từ Hồ Chí Minh tới Đà Nẵng hết bao lâu?",  # 2:00HR
            # "4": "có bao nhiêu tour đi Phú Quốc vậy bạn?",  # 1
            # "5": "tour Nha Trang đi bằng phương tiện gì vậy?",  # train
            # "6": "đi Nha Trang có những ngày nào nhỉ?",  # 1/7 5/7
            "7": "Lịch trình tour Phú Quốc bao gồm những ngày nào?",
            "8": "Địa điểm xuất phát và đến của tour Đà Nẵng là gì?",
            "9": "Thời gian đi và đến của tour Nha Trang như thế nào?",
            "10": "Có bao nhiêu tour sử dụng phương tiện đi lại bằng máy bay?",  # 2
            "11": "Tour nào có thời gian đi sớm nhất?",
            "12": "Có bao nhiêu tour sử dụng phương tiện đi lại bằng tàu hỏa?",  # 1
            "13": "Tour nào xuất phát từ Phú Quốc?",  # No result found!
            "14": "Thời gian đi và đến của tour Hồ Chí Minh - Phú Quốc là bao lâu?",
            "15": "Tour nào có thời gian đi trễ nhất?",
            "16": "Có tour nào xuất phát từ Đà Nẵng không?",  # False # No result found!
        }.get(index, "0")


def run(**kwargs):
    parser = argparse.ArgumentParser(description="NLP Assignment Command Line")

    parser.add_argument(
        "--input",
        action="store_true",
        help="Run all customer queries instead per one",
    )

    parser.add_argument(
        "--id",
        default=-1,
        help="Question to be parsed. Default = 'em có thể nhắc lại tất cả các tour được không?'",
    )

    parser.add_argument(
        "--question",
        default=get_query("1"),
        help="Question to be parsed. Default = 'em có thể nhắc lại tất cả các tour được không?'",
    )

    parser.add_argument(
        "--rule_file_name",
        default="grammar.fcfg",
        help="Context Free Grammar file to be parsed. Default = 'grammar.fcfg'",
    )

    args = parser.parse_args()

    if not args.input:
        for idx, ques in enumerate(customer_queries):
            args.id = idx + 1
            args.question = preprocess_query(ques)
            main(args)
    else:
        try:
            args.question = get_query(args.question)
        except:
            pass
        args.question = preprocess_query(args.question)
        # print(args.question)
        main(args)


if __name__ == "__main__":
    run()
