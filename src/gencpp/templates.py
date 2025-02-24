"""
---
(c) 2024 David SPORN
---
This is part of Gencode -- whatever.

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

TEMPLATE_SOURCES = {
    ########
    # General data
    ########
    # ---
    "copyright": """Copyright (C) {{YEARS_COPYRIGHT}} {{NAMES_COPYRIGHT}}""",
    # ---
    "no_licence_no_description": """ALL RIGHT RESERVED -- project **{{LABEL_PROJECT}}**.""",
    "no_licence_with_description": """ALL RIGHT RESERVED -- project **{{LABEL_PROJECT}}**.\n{{DESCRIPTION_PROJECT}}.""",
    "with_licence_no_description": """This is part of **{{LABEL_PROJECT}}**.""",
    "with_licence_with_description": """This is part of **{{LABEL_PROJECT}}**.\n{{DESCRIPTION_PROJECT}}.""",
    # ---
    "licence_spdx_id": """/* SPDX-License-Identifier: {{SPDX_CLAUSE}} */

""",
    ########
    # Header files
    ########
    # Main template
    # ---
    "source_header": """{{LICENCE_SPDX}}/****************************************

---
{{COPYRIGHT}}
---
{{LICENCE}}
****************************************/
#ifndef {{CODE_GUARD}}
#define {{CODE_GUARD}}
// ================[ CODE BEGINS ]================

{{HEADER_BODY}}

// ================[ END OF CODE ]================
#endif""",
    # ---
    # Header file bodies
    # ---
    "header_body_blank": """// ...your code...""",
    ########
    # CPP Source files
    ########
    # Main template
    # ---
    "source_main": """{{LICENCE_SPDX}}/****************************************

---
{{COPYRIGHT}}
---
{{LICENCE}}
****************************************/
#include "{{NAME_HEADER}}.hpp"

{{SOURCE_BODY}}

""",
    # ---
    # Source file bodies
    # ---
    "source_body_blank": """// ...your code...""",
}
