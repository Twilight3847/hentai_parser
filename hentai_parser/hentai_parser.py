import json
import re
from pathlib import Path


class Hentai_parser:
    def __init__(self) -> None:
        json_file = Path(__file__).parent / "data/tags.json"
        with json_file.open("r", encoding="utf-8") as f:
            self.tags_dict = json.loads(f.read())

    def parse(self, filename: str = "") -> str:
        if not filename:
            return

        normalized_name: str = self._filename_parser(filename)

        return normalized_name

    def _filename_parser(self, input: str) -> str:
        filename = Path(input).stem
        suffix = Path(input).suffix

        manga_name = re.sub(
            r"\s+", " ", re.sub(r"\[.*?\]|\(.*?\)|\【.*?\】", "", filename)
        ).strip()

        original_tags = re.findall(r"\[.*?\]|\(.*?\)|\【.*?\】", filename)
        matches = {"bad_tags": [], "uncensored": [], "normal": []}

        for tag in original_tags:
            lower_tag = tag.lower()
            add = False
            for category in self.tags_dict:
                for word in self.tags_dict[category]:
                    if word in lower_tag:
                        matches[category].append(word)
                        add = True
            if not add:
                matches["normal"].append(tag)

        normalized_name = f"{' '.join(matches['normal'])} {manga_name}{' [無修正]' if matches['uncensored'] else ''}{suffix}"
        return normalized_name


if __name__ == "__main__":
    new_name = Hentai_parser().parse("[真白しらこ] 彼女フェイス [DL版]")
    print(new_name)
