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

from gencode_lib.identifier import IdentifierPart


def test__IdentifierPart__should_instanciate_regular_part_when_it_matches():
    assert IdentifierPart("wHaTeVer").isRegular
    assert IdentifierPart("1234").isRegular
    assert not IdentifierPart().isRegular
    assert not IdentifierPart("ku,pd-ù'").isRegular


def test__IdentifierPart__should_instanciate_separator_when_it_does_not_matches():
    assert not IdentifierPart("wHaTeVer").isSeparator
    assert not IdentifierPart("1234").isSeparator
    assert IdentifierPart().isSeparator
    assert IdentifierPart("ku,pd-ù'").isSeparator


def test__IdentifierPart_lowered__should_return_loweredd_values_for_regulars():
    assert IdentifierPart("wHaTeVer").lowered == "whatever"
    assert IdentifierPart("1234").lowered == "1234"


def test__IdentifierPart_capitalized__should_return_capitalized_values_for_regulars():
    assert IdentifierPart("wHaTeVer").capitalized == "Whatever"
    assert IdentifierPart("1234").capitalized == "1234"


def test__IdentifierPart_allcaps__should_return_uppercased_values_for_regulars():
    assert IdentifierPart("wHaTeVer").allcaps == "WHATEVER"
    assert IdentifierPart("1234").allcaps == "1234"


def test__IdentifierPart__should_return_underscore_for_any_form_of_values():
    part = IdentifierPart()
    assert part.lowered == "_"
    assert part.capitalized == "_"
    assert part.allcaps == "_"

    part = IdentifierPart("ku,pd-ù'")
    assert part.lowered == "_"
    assert part.capitalized == "_"
    assert part.allcaps == "_"
