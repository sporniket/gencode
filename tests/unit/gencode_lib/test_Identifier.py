"""
---
(c) 2024 David SPORN
---
This is part of Gencode

Gencode is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

Gencode is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with Gencode.
If not, see <https://www.gnu.org/licenses/>. 
---
"""

from gencode_lib.identifier import Identifier


def test__Identifier__should_break_down_into_parts():
    # trivial cases
    p = Identifier("whatever").parts
    assert len(p) == 1
    assert p[0].isRegular and p[0].lowered == "whatever"

    p = Identifier("whatEver").parts
    assert len(p) == 2
    assert p[0].isRegular and p[0].lowered == "what"
    assert p[1].isRegular and p[1].lowered == "ever"

    p = Identifier("WhatEver").parts
    assert len(p) == 2
    assert p[0].isRegular and p[0].lowered == "what"
    assert p[1].isRegular and p[1].lowered == "ever"

    p = Identifier("WHAT_EVER").parts
    assert len(p) == 2
    assert p[0].isRegular and p[0].lowered == "what"
    assert p[1].isRegular and p[1].lowered == "ever"

    # tricky cases

    p = Identifier("ST7789").parts
    assert len(p) == 1
    assert p[0].isRegular and p[0].lowered == "st7789"

    p = Identifier("HTTPRequest").parts
    assert len(p) == 2
    assert p[0].isRegular and p[0].lowered == "http"
    assert p[1].isRegular and p[1].lowered == "request"

    p = Identifier("ASingleNode").parts
    assert len(p) == 3
    assert p[0].isRegular and p[0].lowered == "a"
    assert p[1].isRegular and p[1].lowered == "single"
    assert p[2].isRegular and p[2].lowered == "node"


def test__Identifier__should_spot_separators_when_breaking_down_into_parts():
    p = Identifier("what-ever").parts
    assert len(p) == 3
    assert p[0].isRegular and p[0].lowered == "what"
    assert p[1].isSeparator
    assert p[2].isRegular and p[2].lowered == "ever"

    p = Identifier("what_ever").parts
    assert len(p) == 3
    assert p[0].isRegular and p[0].lowered == "what"
    assert p[1].isSeparator
    assert p[2].isRegular and p[2].lowered == "ever"

    p = Identifier("what.ever").parts
    assert len(p) == 3
    assert p[0].isRegular and p[0].lowered == "what"
    assert p[1].isSeparator
    assert p[2].isRegular and p[2].lowered == "ever"

    p = Identifier("what___--_-_____ever").parts
    assert len(p) == 3
    assert p[0].isRegular and p[0].lowered == "what"
    assert p[1].isSeparator
    assert p[2].isRegular and p[2].lowered == "ever"

    p = Identifier("WHAT__EVER").parts
    assert len(p) == 3
    assert p[0].isRegular and p[0].lowered == "what"
    assert p[1].isSeparator
    assert p[2].isRegular and p[2].lowered == "ever"


def test__Identifier__should_consider_non_ascii_letters_as_separator():
    p = Identifier("é").parts
    assert len(p) == 1
    assert p[0].isSeparator


def test__Identifier_allcaps__should_render_all_caps_identifiers():
    assert Identifier("whatever").allcaps == "WHATEVER"

    for id in ["whatEver", "WhatEver", "WHAT_EVER"]:
        assert Identifier(id).allcaps == "WHAT_EVER"
        assert Identifier(f".{id}").allcaps == "__WHAT_EVER"

    for id in [
        "what-ever",
        "what_ever",
        "what.ever",
        "what___--_-_____ever",
        "WHAT__EVER",
    ]:
        assert Identifier(id).allcaps == "WHAT__EVER"


def test__Identifier_sluggified__should_strip_leading_and_trailing_separator():
    assert Identifier("---whatever---").sluggified == "whatever"


def test__Identifier_sluggified__should_have_no_sequences_of_separator():
    assert Identifier("what___--_-_____ever").sluggified == "what_ever"
