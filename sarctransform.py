import argparse
from collections import Mapping, OrderedDict
import csv
from dbfread import DBF  # type: ignore
import json
import os
import re
from typing import Any, Dict, List, Union
import xlrd  # type: ignore

SCHOOL_NAME_TO_CDS = OrderedDict(
    [
        ("lowell", "38684783833407"),
        ("lincoln", "38684783833241"),
        ("washington", "38684783839081"),
    ]
)

UNNECESSARY_FIELDS = [
    # discard race count fields that existed in 2006-07, 2007-08, 2008-09 but not later
    "WH",
    "SD",
    "PI",
    "MULTI",
    "MUULTI",  # misspelling in 2008-09
    "HI",
    "FI",
    "EL",
    "DI",
    "AS",
    "AI",
    "AA",
    # TOTAL doesn't exist in 2009-10, 2018-19, 2019-20
    "TOTAL",
]


def normalize_dict(
    row: Mapping[str, Any], assumed_year: str
) -> Dict[str, Union[str, int, float, None]]:
    d: Dict[str, Union[str, int, float, None]] = {}
    for k, v in row.items():
        if (
            isinstance(v, str)
            or isinstance(v, int)
            or isinstance(v, float)
            or v is None
        ):
            d[k] = v
    if "SARCYear" not in d:
        d["SARCYear"] = assumed_year
    if "CDSCode" in d:
        # 2019-10 used camel case but 2011-12 and later use all caps
        d["CDSCODE"] = d["CDSCode"]
        del d["CDSCode"]
    for field in UNNECESSARY_FIELDS:
        if field in d:
            del d[field]
    percentage_fields = [key for key in d.keys() if key.startswith("PER")]
    for key in percentage_fields:
        try:
            d[key] = float(d[key]) if d[key] is not None and d[key] != "" else None  # type: ignore
        except Exception as e:
            raise ValueError("{} key:{}, value:{}".format(d, key, d[key]))
    return d


def parsefile(assumed_year: str, filename: str, cdscode: str):
    filteredrows: List[Mapping[str, Union[str, int, float, None]]] = []
    if filename.endswith(".txt"):
        with open(filename) as f:
            reader = csv.DictReader(f)
            for d in reader:
                e = normalize_dict(d, assumed_year=assumed_year)
                if e["CDSCODE"] == cdscode:
                    filteredrows.append(e)
    elif filename.endswith(".xls"):
        workbook = xlrd.open_workbook(filename)
        sheet = workbook.sheet_by_index(0)
        print(
            "Sheet 0: name:{name}, nrows:{nrows}, ncols:{ncols}".format(
                name=sheet.name, nrows=sheet.nrows, ncols=sheet.ncols
            )
        )
        header: List[str] = [str(cell.value) for cell in sheet.row(0)]
        for rx in range(1, sheet.nrows):
            values = sheet.row_values(rx)
            d = dict(zip(header, values))
            e = normalize_dict(d, assumed_year=assumed_year)
            if e["CDSCODE"] == cdscode:
                # print(d)
                filteredrows.append(e)
    elif filename.lower().endswith(".dbf"):
        # table = dbf.Table(filename)
        # with table.open(mode=dbf.READ_ONLY):
        #     for record in table:
        #         for item in record.items():
        #             print(item)
        for d in DBF(filename, ignore_missing_memofile=True):
            e = normalize_dict(d, assumed_year=assumed_year)
            if e["CDSCODE"] == cdscode:
                filteredrows.append(e)
    return filteredrows


def scan_sarcs(school: str):
    if re.fullmatch(r"\d+", school):
        cdscode = school
    elif school in SCHOOL_NAME_TO_CDS:
        cdscode = SCHOOL_NAME_TO_CDS[school]
    else:
        raise ValueError(
            "Unknown school: {school}; must add it to SCHOOL_NAME_TO_CDS".format(
                school=school
            )
        )
    filteredrows = []
    for assumed_year, filename in [
        # downloaded and extracted from
        # https://web.archive.org/web/20110124001555/http://www.cde.ca.gov/ta/ac/sa/sarc0607.asp
        ("2006-07", "sarc07/SCHENRET.DBF"),
        # https://web.archive.org/web/20110124001554/http://www.cde.ca.gov/ta/ac/sa/sarc0708.asp
        ("2007-08", "sarc08/SCHENRETH.DBF"),
        # https://web.archive.org/web/20110124001553/http://www.cde.ca.gov/ta/ac/sa/sarc0809.asp
        ("2008-09", "sarc09/SCHENRET.dbf"),
        # wget --recursive --no-parent --no-clobber http://www3.cde.ca.gov/researchfiles/sarc/
        ("2009-10", "www3.cde.ca.gov/researchfiles/sarc/sarc0910/schenret.xls"),
        # ("2009-10", "schenret-2009-2010.xls"),
        ("2010-11", "www3.cde.ca.gov/researchfiles/sarc/sarc1011/SCHENRSG.xls"),
        ("2011-12", "www3.cde.ca.gov/researchfiles/sarc/sarc1112/SCHENRSG.xls"),
        # ("2012-13", "csteth1213.xls"), wrong table; this is test scores
        ("2012-13", "www3.cde.ca.gov/researchfiles/sarc/sarc1213/schenrsg.xls"),
        # "schenrsg1213.xls",
        # ("2013-14", "schenrsg1314.xls"),
        ("2013-14", "www3.cde.ca.gov/researchfiles/sarc/sarc1314/schenrsg.xls"),
        # ("2015-16", "schenrsg1516.txt"),
        ("2015-16", "www3.cde.ca.gov/researchfiles/sarc/sarc1516/schengr.txt "),
        ("2016-17", "www3.cde.ca.gov/researchfiles/sarc/sarc1617/enrbysubgrp.txt"),
        ("2017-18", "www3.cde.ca.gov/researchfiles/sarc/sarc1718/enrbysubgrp.txt"),
        ("2018-19", "www3.cde.ca.gov/researchfiles/sarc/sarc1819/enrbystgrp.txt"),
        ("2019-20", "www3.cde.ca.gov/researchfiles/sarc/sarc1920/enrbysubgrp.txt"),
    ]:
        path = os.path.join(os.path.dirname(__file__), filename)
        filteredrows.extend(parsefile(assumed_year, path, cdscode=cdscode))
    allkeys = sorted(list(set(key for row in filteredrows for key in row.keys())))
    transposed = OrderedDict(
        (key, OrderedDict((row.get("SARCYear"), row.get(key)) for row in filteredrows))
        for key in allkeys
    )
    return transposed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--school",
        help="school name or CDSCode to filter (one of {names}, or a CDSCode)".format(
            names=", ".join(SCHOOL_NAME_TO_CDS.keys())
        ),
        default=next(SCHOOL_NAME_TO_CDS.keys().__iter__()),
    )
    args = parser.parse_args()
    transposed = scan_sarcs(args.school)
    print(json.dumps(transposed, indent=2))


if __name__ == "__main__":
    main()
