import gzip
import json

from pprint import pprint
from tqdm import tqdm

from data.amazon.process import _parse_gz_line


def get_metadata(meta_file, output_file):
    assert meta_file.endswith(".json.gz")
    metas = {}
    gzip_file = gzip.open(meta_file, "r")
    count = 1
    for line in tqdm(gzip_file, desc=f"load meta file {meta_file}"):
        data = _parse_gz_line(line)
        print(count)
        count = count + 1
        try:
            item = str(data["asin"])
            metas[item] = {"title": data["title"], "categories": data["categories"][0]}
        except:
            continue
    with open(output_file, "w") as f:
        json.dump(metas, f)

    return metas


def get_data_from_id(item_ID, meta_json):
    meta_data = meta_json[item_ID]
    item_image = "./processed/beauty/visions/" + item_ID + ".jpg"
    return meta_data, item_image
