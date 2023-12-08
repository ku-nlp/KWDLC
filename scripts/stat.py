from collections import defaultdict
from pathlib import Path

from rhoknp import Document
from tabulate import tabulate

KNP_DIR = Path("knp")
ID_DIR = Path("id") / "split_for_pas"
HEADERS = (
    "split",
    "documents",
    "sentences",
    "morphemes",
    "named_entities",
    "predicates",
    "coreferring_mentions",
)


def calc_stats(documents: list[Document]) -> dict[str, int]:
    stats: dict[str, int] = defaultdict(int)
    for document in documents:
        stats["documents"] += 1
        stats["sentences"] += len([s for s in document.sentences if "括弧始" not in s.misc_comment])
        stats["named_entities"] += sum(len(sentence.named_entities) for sentence in document.sentences)
        for base_phrase in document.base_phrases:
            if any(len(arguments) > 0 for arguments in base_phrase.pas.get_all_arguments().values()):
                stats["predicates"] += 1
            coreferents = base_phrase.get_coreferents()
            if len(coreferents) > 0:
                stats["coreferring_mentions"] += 1
            stats["morphemes"] += len(base_phrase.morphemes)
    return stats


def main():
    data = []
    for split in ("train", "dev", "test"):
        row = [split]
        ids = [line.strip() for line in ID_DIR.joinpath(f"{split}.id").read_text().splitlines()]
        documents = [Document.from_knp(KNP_DIR.joinpath(f"{doc_id[:13]}/{doc_id}.knp").read_text()) for doc_id in ids]
        stats = calc_stats(documents)
        row.extend(stats[key] for key in HEADERS[1:])
        data.append(row)
    row = ["total"]
    row.extend(sum(row[i] for row in data) for i in range(1, len(HEADERS)))
    data.append(row)

    print(tabulate(data, headers=HEADERS, tablefmt="github", intfmt=","))


if __name__ == "__main__":
    main()
