"""Choice lists for the admin portal.

Kept in one module so the client can revise a dropdown without touching models,
views or templates. Several of these are marked TENTATIVE -- the handwritten
spec named the field but not its options; see docs/requests/UI-002-admin-dashboard.md.
"""

# Page 1 of the spec: "KG - 12th"
STD_CHOICES = [
    ('KG', 'KG'), ('LKG', 'LKG'), ('UKG', 'UKG'),
    ('I', 'I'), ('II', 'II'), ('III', 'III'), ('IV', 'IV'), ('V', 'V'), ('VI', 'VI'),
    ('VII', 'VII'), ('VIII', 'VIII'), ('IX', 'IX'), ('X', 'X'), ('XI', 'XI'), ('XII', 'XII'),
]

# Spec: "STATE / CBSE / IGCSE". ICSE added because the public course page advertises it.
CURRICULUM_CHOICES = [
    ('state', 'State Board'), ('cbse', 'CBSE'), ('icse', 'ICSE'), ('igcse', 'IGCSE'),
]

# Spec: "WCC R / WCC G / WCC A". What A stands for is unconfirmed (open question 2).
BRANCH_CHOICES = [
    ('wcc_r', 'WCC R'), ('wcc_g', 'WCC G'), ('wcc_a', 'WCC A'),
]

# Spec: "Active / Discontinued / Re-Joining"
ACTIVE_STATUS_CHOICES = [
    ('active', 'Active'), ('discontinued', 'Discontinued'), ('rejoining', 'Re-Joining'),
]

# Spec: "Ripplers / Planners"
TEAM_CHOICES = [('ripplers', 'Ripplers'), ('planners', 'Planners')]

# Spec page 2: "MARK (INTERNAL / EXTERNAL)"
EXAM_TYPE_CHOICES = [('internal', 'Internal'), ('external', 'External')]

# Spec page 3: Present / Absent / "No Class (Holiday)"
ATTENDANCE_STATUS_CHOICES = [
    ('present', 'Present'), ('absent', 'Absent'), ('no_class', 'No Class'),
]

# TENTATIVE -- the spec shows a "Category" dropdown with no options listed (open question 1).
CATEGORY_CHOICES = [
    ('regular', 'Regular Tuition'), ('neet', 'NEET'), ('vac', 'Value-Added Course'),
    ('daycare', 'Day Care'), ('spoken', 'Spoken English'),
]
