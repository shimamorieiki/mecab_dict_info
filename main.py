"""_summary_
"""

import csv
import os
from pathlib import Path
from typing import Dict, List, Set


def read_csv(file_path: str) -> List[List[str]]:
    """[summary]
        csvファイルの中身を読み取りリストとして取得する
    Args:
        file_path ([type]): [description]
    Returns:
        [type]: [description]
    """

    return_list: List[List[str]] = []
    with open(file=file_path, mode="r", encoding="utf-8") as read:
        reader = csv.reader(read)
        for row in reader:
            return_list.append(row)
        return return_list


def search_files(path: str, recursive: bool = False) -> List[str]:
    """[summary]
        path以下のファイルを返す
        recursive=Trueのときは以下のフォルダのファイルも再帰的に取得する。
    Args:
        path ([type]): フォルダパス
        recursive (bool, optional): 以下のフォルダの中身を再帰的に取得するか. Defaults to False.
    Returns:
        [type]: [description]
    """
    files: List[str] = []
    for file_path in list(Path(path).glob("*")):
        if os.path.isfile(file_path):
            files.append(str(file_path))
        if recursive:
            files.extend(search_files(str(file_path), recursive=True))
    return sorted(files)


def get_hinsis_list(path: str) -> Set[str]:
    """_summary_
        品詞の一覧を取得する
    Returns:
        _type_: _description_
    """
    files: List[str] = search_files(path=path)
    hinsis_set: Set[str] = set()
    for file in files:
        rows: List[List[str]] = read_csv(file_path=file)
        for row in rows:
            hinsis_set.add(row[4])

    return hinsis_set


def get_hinsis_katuyou(path: str):
    """_summary_
        品詞の活用一覧を取得する
    Args:
        path (str): _description_
    """
    files: List[str] = search_files(path=path)
    hinsis_list: List[str] = list(get_hinsis_list(path=path))

    hinsi_katuyou_dict: Dict[str, List[Set[str]]] = dict()
    for hinsi in hinsis_list:
        hinsi_katuyou_dict.setdefault(hinsi, [])
        hinsi_katuyou_dict[hinsi] = [set() for _ in range(2)]

    # 1ファイルずつ読み込み品詞の一覧を取得する
    for file in files:
        rows: List[List[str]] = read_csv(file_path=file)
        for row in rows:
            (
                _,
                _,
                _,
                _,
                hinsi,
                _,
                _,
                _,
                katuyou_type,
                katuyou_form,
                _,
                _,
                _,
            ) = row
            hinsi_katuyou_dict[hinsi][0].add(katuyou_type)
            hinsi_katuyou_dict[hinsi][1].add(katuyou_form)

    return hinsi_katuyou_dict


def main():
    """_summary_
    main
    """
    path: str = "mecab/ipadic"

    # # 品詞一覧を取得する
    # hinsis_set: Set[str] = get_hinsis_list(path=path)
    # print(hinsis_set)

    # 品詞の活用一覧を取得する
    hinsi_katuyou_dict: Dict[str, Set[str]] = get_hinsis_katuyou(path=path)
    for hinsi in hinsi_katuyou_dict:
        print(hinsi)
        print(hinsi_katuyou_dict[hinsi][0])
        print(hinsi_katuyou_dict[hinsi][1])
        print("\n")


if __name__ == "__main__":
    main()
