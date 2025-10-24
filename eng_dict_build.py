import json
import os
import sys

default_path = "open_eng_dict"
json_path = sys.argv[1] if len(sys.argv) > 1 else default_path
json_path = os.path.join(json_path, "dictionary")
output_path = "eng_dict_dist"

if not os.path.exists(json_path):
    print(f"❌ 错误：路径不存在 → {json_path}")
    print(f"用法：python build.py [可选JSON路径] （默认路径：{default_path}）")
    exit()

os.makedirs(output_path, exist_ok=True)
concise_file_path = os.path.join(output_path, "concise_definition.txt")
parasynonyms_file_path = os.path.join(output_path, "parasynonyms.txt")

concise_f = open(concise_file_path, "w", encoding="utf-8")
para_f = open(parasynonyms_file_path, "w", encoding="utf-8")

total = max(1, len(os.listdir(json_path)))
sep = max(1, total // 100)
count = 0
for filename in os.listdir(json_path):
    count += 1
    if count % sep == 0:
        print(f"{count}/{total} {count / total:.1%}")

    # 只处理 *.json
    if not filename.endswith(".json"):
        continue
    json_file_path = os.path.join(json_path, filename)

    try:
        with open(json_file_path, "r", encoding="utf-8") as json_f:
            data = json.load(json_f)

        if "word" not in data:
            continue
        word = data["word"].strip()

        # definition
        if "concise_definition" in data:
            concise_def = data["concise_definition"].strip()
            concise_line = f"{word} : {concise_def}\n"
            concise_f.write(concise_line)

        # parasynonyms
        if "comparison" in data and isinstance(data["comparison"], list):
            # 收集
            near_words = []
            for item in data["comparison"]:
                if "word_to_compare" in item:
                    near_word = item["word_to_compare"].strip()
                    if near_word and near_word not in near_words:
                        near_words.append(near_word)

            if near_words:
                parasynonyms_line = f"{word} {' '.join(near_words)}\n"
                para_f.write(parasynonyms_line)

    except Exception as e:
        print(f"处理文件 {filename} 时出错：{str(e)}")
        continue

print(
    f"处理完成！\n1. concise_definition.txt 路径：{concise_file_path}\n2. parasynonyms.txt 路径：{parasynonyms_file_path}"
)
