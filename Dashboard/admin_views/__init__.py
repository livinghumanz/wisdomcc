"""Admin portal views, one module per screen so the screens stay independent."""
from .students import student_list, student_form, student_delete          # noqa: F401
from .marks import marks_screen, growth_card                              # noqa: F401
from .attendance import attendance_register                               # noqa: F401
from .fees import fee_sheet, faculty_analysis                             # noqa: F401
