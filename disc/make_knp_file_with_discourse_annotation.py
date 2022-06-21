import os
import sys
import re
from pyknp import KNP
from collections import defaultdict
from argparse import ArgumentParser

knp = KNP()

EXPERT_ANN_FILE = "./disc_expert.txt"
CROWD_ANN_FILE = "./disc_crowdsourcing.txt"
EXPERT_KNP = "./disc_expert.knp2"
CROWD_KNP = "./disc_crowdsourcing.knp2"

GOLD_KNP_DIR = "../knp"
GOLD_ORG_DIR = "../org"

END_MARKERS = re.compile(r'(。|？|！|．．．)$')


def organize_knp_features(knp_result):
    sid = knp_result.sid
    clause_tids = []
    # remove bnst's features
    for i, bnst in enumerate(knp_result.bnst_list()):
        knp_result.bnst_list()[i].fstring = ""
    # remove mrph's features
    for i, mrph in enumerate(knp_result.mrph_list()):
        knp_result.mrph_list()[i].fstring = ""
    # Organize tag's features
    for i, tag in enumerate(knp_result.tag_list()):
        new_feature = ""
        # Check <節-区切>, <節-機能>, <節-前向き機能>
        for f_tag in re.findall("<節-[^>]+>", tag.fstring):
            new_feature += f_tag
            if f_tag == "<節-区切>":
                clause_tids.append(f'{sid}/{tag.tag_id}')
        # Update tag's feature
        knp_result.tag_list()[i].fstring = \
            re.sub("<節-区切:連体修飾>|<節-主辞>", "", new_feature)\
            if "<節-区切:連体修飾>" in new_feature\
               else new_feature
    return knp_result, clause_tids


def add_discourse_info_to_gold_knp(ann_data):
    output_text = ""
    for doc in ann_data:
        # Search KNP file
        knp_path = \
            os.path.join(GOLD_KNP_DIR, doc["A-ID"][:13], f'{doc["A-ID"]}.knp')
        if not os.path.exists(knp_path):
            print(f'KNP FILE IS NOT EXIST: {knp_path}', file=sys.stderr)
        else:
            knp_results = []
            clause_tids = []
            # Load knp file
            with open(knp_path, "r") as f:
                data = ""
                for line in f:
                    data += line
                    if line.strip() == "EOS":
                        # Load knp data
                        result = knp.result(data)
                        if "括弧始" in result.comment:
                            data = ""
                            continue
                        result, _ = organize_knp_features(result)
                        # Pick discourse features
                        parse = knp.parse(
                            "".join(
                                [mrph.midasi for mrph in result.mrph_list()]
                            )
                        )
                        parse, _ = organize_knp_features(parse)
                        discourse_features = {}
                        char_idx = 0
                        for tag in parse.tag_list():
                            char_idx += len(
                                "".join(mrph.midasi
                                        for mrph in tag.mrph_list())
                            )
                            if tag.fstring:
                                discourse_features[char_idx] = tag.fstring
                        # Add discourse features to gold knp
                        char_idx = 0
                        for i, tag in enumerate(result.tag_list()):
                            char_idx += len(
                                "".join(mrph.midasi
                                        for mrph in tag.mrph_list())
                            )
                            if char_idx in discourse_features:
                                result.tag_list()[i].fstring =\
                                    discourse_features[char_idx]
                                if "<節-区切>" in discourse_features[char_idx]:
                                    clause_tids.append(
                                        f'{result.sid}/{tag.tag_id}'
                                    )
                        knp_results.append(result)
                        data = ""
            # Add discourse tags
            if len(clause_tids) != len(doc["clause"]):
                print(f'Warning: Differ clause split: {doc["A-ID"]}',
                      file=sys.stderr)
                # print(clause_tids, doc["clause"]), file=sys.stderr)
                continue
            clause_id = 1
            if len(knp_results) != 3:
                print(doc["A-ID"])
                for i in range(0, len(knp_results)):
                    result = knp_results[i]
                    print("".join(
                        [mrph.midasi for mrph in result.mrph_list()]
                    ))
                sys.exit(1)
            for sent_id in range(0, 3):
                result = knp_results[sent_id]
                for i, tag in enumerate(result.tag_list()):
                    if '<節-区切>' in tag.fstring:
                        dc_label = ''
                        is_print = False
                        for target_id in range(clause_id+1,
                                               len(clause_tids)+1):
                            for dc_tag in \
                                  doc['rel'][str(clause_id)][str(target_id)]:
                                dc_label +=\
                                    f'{clause_tids[target_id-1]}/{dc_tag};'
                                if dc_tag != "談話関係なし":
                                    is_print = True
                        if dc_label and is_print:
                            result.tag_list()[i].fstring +=\
                                f'<談話関係:{re.sub(";$", ">", dc_label)}'
                        clause_id += 1
                knp_results[sent_id] = result.all().strip()
            output_text += "\n".join(knp_results)+"\n"
    return output_text


def parse_knp(sent, sid):
    result = knp.parse(sent)
    result.sid = sid
    result.comment = f'# S-ID:{sid}'
    result, tids = organize_knp_features(result)
    return result, tids


def make_knp_from_textfile(disc_ann):
    output_text = ""
    for doc in disc_ann:
        knp_results = []
        clause_tids = []
        sid = 1
        # Check org directory
        org_path = os.path.join(GOLD_ORG_DIR, doc["A-ID"][:13],
                                f'{doc["A-ID"]}.org')
        if os.path.exists(org_path):
            # Found -> read org file
            with open(org_path, "r") as f:
                sents = []
                insert_point = -1
                for line in f.readlines():
                    if re.match("#", line.strip()):
                        if paren_cidx :=\
                           re.search(r"括弧位置:(\d+)", line.strip()):
                            insert_point = paren_cidx.group(1)
                    else:
                        if insert_point != -1:
                            # insert paren
                            sents[-1] =\
                                f'{sents[-1][:int(insert_point)]}'\
                                + f'（{line.strip()}）'\
                                + f'{sents[-1][int(insert_point):]}'
                            insert_point = -1
                        else:
                            sents.append(line.strip())
            # parse
            for sent in sents:
                result, tids = parse_knp(sent, f'{doc["A-ID"]}-{sid}')
                knp_results.append(result)
                clause_tids.extend(tids)
                sid += 1
        else:
            # Not found -> read text file with discourse annotations and parse
            sent = ""
            for clause in doc["clause"]:
                sent += clause
                if END_MARKERS.search(sent):
                    result, tids = parse_knp(sent, f'{doc["A-ID"]}-{sid}')
                    knp_results.append(result)
                    clause_tids.extend(tids)
                    sent = ""
                    sid += 1
            if sent != "":
                # Last 1 sentences
                result, tids = parse_knp(sent, f'{doc["A-ID"]}-{sid}')
                knp_results.append(result)
                clause_tids.extend(tids)
        # Add discourse tags
        clause_id = 1
        if len(knp_results) != 3:
            print(f'Warning: Failed to restore text: {doc["A-ID"]}',
                  file=sys.stderr)
            # print(doc["A-ID"])
            # for i in range(0, len(knp_results)):
            #     result = knp_results[i]
            #     print("".join([mrph.midasi for mrph in result.mrph_list()]))
            continue
        for sent_id in range(0, 3):
            try:
                result = knp_results[sent_id]
            except:
                print(doc["A-ID"])
                print(knp_results)
                sys.exit(1)
            for i, tag in enumerate(result.tag_list()):
                if '<節-区切>' in tag.fstring:
                    dc_label = ''
                    is_print = False
                    for target_id in range(clause_id+1, len(clause_tids)+1):
                        for dc_tag \
                              in doc['rel'][str(clause_id)][str(target_id)]:
                            dc_label += f'{clause_tids[target_id-1]}/{dc_tag};'
                            if dc_tag != "談話関係なし":
                                is_print = True
                    if dc_label and is_print:
                        result.tag_list()[i].fstring +=\
                            f'<談話関係:{re.sub(";$", ">", dc_label)}'
                    clause_id += 1
            knp_results[sent_id] = result.all().strip()
        output_text += "\n".join(knp_results)+"\n"
    return output_text


def remove_duplicate_data(expert_ann, crowd_ann,
                          remove_duplicate_from_expert=False,
                          remove_duplicate_from_crowd=False):
    new_expert = expert_ann
    new_crowd = crowd_ann
    if remove_duplicate_from_expert:
        new_expert = []
        aids = [doc["A-ID"] for doc in crowd_ann]
        for doc in expert_ann:
            if doc["A-ID"] in aids:
                print(
                    f'Remove duplicate text from expert corpus: {doc["A-ID"]}',
                    file=sys.stderr
                )
            else:
                new_expert.append(doc)
    if remove_duplicate_from_crowd:
        new_crowd = []
        aids = [doc["A-ID"] for doc in expert_ann]
        for doc in crowd_ann:
            if doc["A-ID"] in aids:
                print(
                    f'Remove duplicate text from crowd corpus: {doc["A-ID"]}',
                    file=sys.stderr
                )
            else:
                new_crowd.append(doc)
    return new_expert, new_crowd


def read_disc_ann_file(filepath):
    result = []
    with open(filepath, "r") as f:
        doc = {
            'A-ID': "", 'clause': [],
            'rel': defaultdict(lambda: defaultdict(list))
        }
        for line in f.readlines():
            if line.strip() == "":
                continue
            if "# A-ID" in line and doc['A-ID']:
                # Parse & output data
                result.append(doc)
                doc = {
                    'A-ID': "", 'clause': [],
                    'rel': defaultdict(lambda: defaultdict(str))
                }
            # Store a line
            split_line = re.split(r"\s+", line.strip())
            if "A-ID" in line:
                doc['A-ID'] = re.sub("A-ID:", "", split_line[1])
            elif "-" not in split_line[0]:
                doc['clause'].append(split_line[1])
            else:
                if ":" in split_line[1]:
                    tag, vote = split_line[1].strip().split(":", 1)
                    disc_tag = [tag]
                    for temp in split_line[2:]:
                        new_tag, new_vote = temp.strip().split(":", 1)
                        if vote == new_vote:
                            disc_tag.append(new_tag)
                        else:
                            break
                    if disc_tag == ["談話関係なし"]:
                        disc_tag = []
                else:
                    disc_tag = [split_line[1]]
                split_cid = split_line[0].strip().split("-")
                doc['rel'][split_cid[0]][split_cid[1]] = disc_tag
    if doc['A-ID']:
        # Last 1 data
        result.append(doc)
    return result


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-g", "--gold_knp", default=False, action='store_true')
    parser.add_argument("--remove_duplicate_from_expert",
                        default=False, action='store_true')
    parser.add_argument("--remove_duplicate_from_crowd",
                        default=False, action='store_true')
    args = parser.parse_args()

    # Read Disc_annotation files
    expert_ann = read_disc_ann_file(EXPERT_ANN_FILE)
    crowd_ann = read_disc_ann_file(CROWD_ANN_FILE)

    # Remove duplicate data
    expert_ann, crowd_ann = remove_duplicate_data(
        expert_ann, crowd_ann,
        args.remove_duplicate_from_expert, args.remove_duplicate_from_crowd,
    )

    # Make knp files
    if args.gold_knp:
        expert = add_discourse_info_to_gold_knp(expert_ann)
        crowd = add_discourse_info_to_gold_knp(crowd_ann)
    else:
        expert = make_knp_from_textfile(expert_ann)
        crowd = make_knp_from_textfile(crowd_ann)

    # Output files
    with open(EXPERT_KNP, "w") as f:
        print(expert, file=f)
    with open(CROWD_KNP, "w") as f:
        print(crowd, file=f)
