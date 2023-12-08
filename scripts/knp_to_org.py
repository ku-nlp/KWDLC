from pathlib import Path

from rhoknp import Document

KNP_DIR = Path("knp")
ORG_DIR = Path("org")


def main():
    for path in KNP_DIR.glob("**/*.knp"):
        document = Document.from_knp(path.read_text())
        output_path: Path = ORG_DIR.joinpath(path.relative_to(KNP_DIR)).with_suffix(".org")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        org_text = ""
        for sentence in document.sentences:
            org_text += sentence.comment + "\n"
            org_text += sentence.text + "\n"
        output_path.write_text(org_text)


if __name__ == "__main__":
    main()
