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

from enum import Enum
import re

Whatever = "whatever"

IdentifierPartType = Enum("IdentifierPartType", ["SEPARATOR", "REGULAR"])

RegularPartPattern = re.compile("^[0-9A-Za-z]+$")


class IdentifierPart:
    def __init__(self, value: str = None):
        match = RegularPartPattern.match("" if value is None else value)
        if match:
            self._type = IdentifierPartType.REGULAR
            self._value = value
        else:
            self._type = IdentifierPartType.SEPARATOR
            self._value = "_"

    @property
    def isSeparator(self):
        return self._type is IdentifierPartType.SEPARATOR

    @property
    def isRegular(self):
        return self._type is IdentifierPartType.REGULAR

    @property
    def lowered(self):
        return self._value if self.isSeparator else self._value.lower()

    @property
    def capitalized(self):
        return self._value if self.isSeparator else self._value.capitalize()

    @property
    def allcaps(self):
        return self._value if self.isSeparator else self._value.upper()


IdentifierParsingState = Enum(
    "IdentifierParsingState",
    [
        "ACCUMULATE",
        "ACCUMULATE_CAPITALIZED",
        "ACCUMULATE_ALLCAPS",
        "ACCUMULATE_SEPARATOR",
    ],
)
IdentifierCharClass = Enum(
    "IdentifierCharClass", ["LOWER", "CAPITAL", "DIGIT", "SEPARATOR"]
)
lowercaseMatcher = re.compile(r"[a-z]")
uppercaseMatcher = re.compile(r"[A-Z]")
digitMatcher = re.compile(r"[0-9]")


class Identifier:

    @staticmethod
    def evalCharType(c: str) -> IdentifierCharClass:
        return (
            IdentifierCharClass.LOWER
            if lowercaseMatcher.match(c)
            else (
                IdentifierCharClass.CAPITAL
                if uppercaseMatcher.match(c)
                else (
                    IdentifierCharClass.DIGIT
                    if digitMatcher.match(c)
                    else IdentifierCharClass.SEPARATOR
                )
            )
        )

    @staticmethod
    def evalAccumulationType(chartype: IdentifierCharClass) -> IdentifierParsingState:
        return (
            IdentifierParsingState.ACCUMULATE_SEPARATOR
            if chartype is IdentifierCharClass.SEPARATOR
            else (
                IdentifierParsingState.ACCUMULATE_CAPITALIZED
                if chartype is IdentifierCharClass.CAPITAL
                else IdentifierParsingState.ACCUMULATE
            )
        )

    @staticmethod
    def canAccumulate(
        sizeOfAccumulator: int,
        state: IdentifierParsingState,
        chartype: IdentifierCharClass,
    ):
        return (
            sizeOfAccumulator == 0
            or (
                state is IdentifierParsingState.ACCUMULATE_ALLCAPS
                and chartype in [IdentifierCharClass.CAPITAL, IdentifierCharClass.DIGIT]
            )
            or (
                state is IdentifierParsingState.ACCUMULATE_CAPITALIZED
                and chartype in [IdentifierCharClass.LOWER, IdentifierCharClass.DIGIT]
            )
            or (
                state is IdentifierParsingState.ACCUMULATE
                and chartype in [IdentifierCharClass.LOWER, IdentifierCharClass.DIGIT]
            )
            or (
                state is IdentifierParsingState.ACCUMULATE_SEPARATOR
                and chartype in [IdentifierCharClass.SEPARATOR]
            )
        )

    def __init__(self, value: str):
        if value is None or len(value) == 0:
            raise ValueError("invalid.value.blank")
        # TODO breakdown into parts

        self._parts = []

        accumulator = ""
        state = IdentifierParsingState.ACCUMULATE
        for i, c in enumerate(value):
            chartype = Identifier.evalCharType(c)
            sizeOfAccumulator = len(accumulator)
            # 1 -- set or update state (type of accumulation) if appliable
            if sizeOfAccumulator == 0:
                state = Identifier.evalAccumulationType(chartype)
            elif (
                sizeOfAccumulator == 1
                and state == IdentifierParsingState.ACCUMULATE_CAPITALIZED
                and chartype is IdentifierCharClass.CAPITAL
            ):
                state = IdentifierParsingState.ACCUMULATE_ALLCAPS

            # 2 -- accumulate if possible
            if Identifier.canAccumulate(sizeOfAccumulator, state, chartype):
                accumulator = accumulator + c
                continue

            # 3 -- manage end of accumulation
            if state is IdentifierParsingState.ACCUMULATE_SEPARATOR:
                self._parts += [IdentifierPart()]
                accumulator = c
                state = Identifier.evalAccumulationType(chartype)
            elif state is IdentifierParsingState.ACCUMULATE_ALLCAPS:
                if chartype is IdentifierCharClass.LOWER:
                    # Accronyme or one letter word followed by capitalized word
                    self._parts += [IdentifierPart(accumulator[:-1])]
                    accumulator = accumulator[-1:] + c
                    state = IdentifierParsingState.ACCUMULATE_CAPITALIZED
                elif chartype is IdentifierCharClass.SEPARATOR:
                    # Regular part of all caps identifier, ditch the found separator
                    self._parts += [IdentifierPart(accumulator)]
                    accumulator = ""
            else:
                # state is ACCUMULATE or ACCUMULATE_CAPITALIZED
                if chartype is IdentifierCharClass.CAPITAL:
                    # Capitalized word followed by capitalized word
                    self._parts += [IdentifierPart(accumulator)]
                    accumulator = c
                    state = IdentifierParsingState.ACCUMULATE_CAPITALIZED
                elif chartype is IdentifierCharClass.SEPARATOR:
                    self._parts += [IdentifierPart(accumulator)]
                    accumulator = c
                    state = IdentifierParsingState.ACCUMULATE_SEPARATOR

            # DONE

        if len(accumulator):
            self._parts += [
                (
                    IdentifierPart()
                    if state == IdentifierParsingState.ACCUMULATE_SEPARATOR
                    else IdentifierPart(accumulator)
                )
            ]

    @property
    def parts(self):
        # return a clone to prevent modification
        return [p for p in self._parts]

    @property
    def allcaps(self):
        render = [p.allcaps for p in self._parts]
        return "_".join(render).replace("___", "__")

    @property
    def sluggified(self):
        render = [p.lowered for p in self._parts]
        lowered = "_".join(render).replace("___", "_")
        return re.sub(r"^_+|_+$", "", lowered)
