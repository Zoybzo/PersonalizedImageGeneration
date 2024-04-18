import os
import gzip

import jsonlines
from tqdm import tqdm
from PIL import Image


def get_sub_paths(path):
    sub_paths = [os.path.join(path, sub_path) for sub_path in os.listdir(path)]
    results = [sub_path for sub_path in sub_paths if os.path.isdir(sub_path)]
    return results


def _parse_csv_line(line):
    data = line.strip().split(",")
    return {
        "user": str(data[0]),
        "item": str(data[1]),
        "rate": float(data[2]),
        "time": int(data[3]),
    }


def load_inter_file(inter_file):
    assert inter_file.endswith(".csv")

    inters = set()
    with open(inter_file, "r", encoding="utf-8") as fobj:
        for line in tqdm(fobj.readlines(), desc=f"load inter file {inter_file}"):
            data = _parse_csv_line(line)
            user = data["user"]
            item = data["item"]
            rate = data["rate"]
            time = data["time"]
            inters.add((user, item, rate, time))
    print("Total inters:", len(inters))
    return inters


def _parse_gz_line(line):
    return eval(line)


def _parse_vision(data):
    try:
        if "imUrl" in data:
            image_url = data["imUrl"]
            if image_url:
                return image_url
        return None
    except:
        return None


def _parse_text(data):
    try:
        text = ""
        if "title" in data:
            text += f"Title: {str(data['title'])} ; "
        if "description" in data:
            text += f"Description: {str(data['description'])} ; "

        if text:
            return text
        else:
            return f"Asin: {str(data['asin'])} ; "
    except:
        return None


def load_meta_file(meta_file):
    assert meta_file.endswith(".json.gz")

    metas = {}
    gzip_file = gzip.open(meta_file, "r")
    for line in tqdm(gzip_file, desc=f"load meta file {meta_file}"):
        data = _parse_gz_line(line)
        item = str(data["asin"])

        vision = _parse_vision(data)
        text = _parse_text(data)

        metas[item] = {"vision": vision, "audio": None, "text": text}
    return metas


def filter_inters_by_metas(inters, metas):
    new_inters = []
    for inter in tqdm(inters, desc="filter inters by metas"):
        if inter[1] in metas:
            new_inters.append(inter)
    return new_inters


def filter_metas_by_inters(metas, inters):
    items = set()
    for inter in tqdm(inters, desc="filter metas by inters"):
        items.add(inter[1])
    new_metas = {}
    for id, meta in metas.items():
        if id in items:
            new_metas[id] = meta
    return new_metas


def filter_k_core_inters(inters, user_inter_threshold=5, item_inter_threshold=5):
    print(f"Filter K core: user {user_inter_threshold}, item {item_inter_threshold}")
    while True:
        user_count = {}
        item_count = {}
        for inter in inters:
            if inter[0] not in user_count:
                user_count[inter[0]] = 1
            else:
                user_count[inter[0]] += 1

            if inter[1] not in item_count:
                item_count[inter[1]] = 1
            else:
                item_count[inter[1]] += 1

        new_inters = []
        for inter in inters:
            if (
                user_count[inter[0]] >= user_inter_threshold
                and item_count[inter[1]] >= item_inter_threshold
            ):
                new_inters.append(inter)

        print(f"\tFilter: {len(inters)} inters to {len(new_inters)} inters")
        if len(new_inters) == len(inters):
            return new_inters
        inters = new_inters


def group_inters_by_user(inters):
    users = {}
    for inter in tqdm(inters, desc="group inters by user"):
        if inter[0] not in users:
            users[inter[0]] = []
        users[inter[0]].append({"item": inter[1], "time": inter[3]})
    return users


def filter_metas_without_modality(metas, vision_filter=False, text_filter=False):
    desc = "filter metas"
    desc += " [without vision]" if vision_filter else ""
    desc += " [without text]" if text_filter else ""

    new_metas = {}
    for item, meta in tqdm(metas.items(), desc=desc):
        if vision_filter and meta["vision"] is None:
            continue
        if text_filter and meta["text"] is None:
            continue
        new_metas[item] = meta
    return new_metas
