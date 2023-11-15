import glob
import json
import re
import statistics
import xml.etree.ElementTree as ET
import re

COMMENTS = ""


def extract_text(element):
    text = element.text.strip() if element.text else ""
    text = f"{text}\n" if text else text
    for child in element:
        text += extract_text(child)
    return text


if __name__ == "__main__":
    files = glob.glob("data/items/**/*.xml")
    paragraphs = []
    for f in files:
        date = None
        # ignore the attachments for now
        if not re.match(r"data\/items\/_.+", f):
            tree = ET.parse(f)
            root = tree.getroot()
            for doc in root.iter("norm"):
                date = doc.findtext("metadaten/ausfertigung-datum", date)
                jurabk = doc.findtext("metadaten/jurabk", default="")
                titel = doc.findtext("metadaten/titel", default="")
                enbez = doc.findtext("metadaten/enbez", default="")
                doknr = doc.get("doknr")
                complete_title = f"{jurabk} {enbez} - {titel}"

                if (
                    "Inhalt" in enbez
                    or "Eingangsformel" in enbez
                    or "Schlussformel" in enbez
                    or "Schlußformel" in enbez
                ):
                    continue

                for text in doc.findall("textdaten/text/Content"):
                    t = extract_text(text)
                    # filter (gegenstandslos) or (weggefallen) or -
                    if t and len(t.strip()) > 20:
                        p = {
                            "snippet": f"{complete_title}\n{t}",
                            "tags": [],
                            "id": doknr,
                            "properties": {
                                "snippet": t,
                                "title": complete_title,
                            },
                        }
                        if date and date.strip() != "0000-00-00":
                            p["properties"]["publication_date"] = f"{date}T00:00:00Z"
                        if jurabk:
                            p["properties"]["jurabk"] = jurabk
                            p["tags"].append(jurabk)
                        if titel:
                            p["properties"]["original_title"] = titel
                        if enbez:
                            p["properties"]["enbez"] = enbez
                            p["tags"].append(enbez)

                        paragraphs.append(p)
    # print(len(paragraphs))
    # list_len = list(map(lambda x: len(x['snippet']), paragraphs))
    # average = sum( list_len )/ len(paragraphs)
    # print(average)
    # print(f"median: {statistics.variance(list_len)}")
    # for i in range(1, 10):
    #     print(paragraphs[i])
    #     print('-------------------------')
    print(json.dumps(paragraphs))
