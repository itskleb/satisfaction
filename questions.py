"""
Question metadata for the Scouting America Program Satisfaction Survey.

Each entry describes how a survey column should be treated by the dashboard:
  - "scale_10": numeric 1-10 rating (higher = better)
  - "likert_5": 1-5 rating with text labels (Extremely dissatisfied ... Extremely
    satisfied, or Strongly disagree ... Strongly agree)
  - "scale_5_num": numeric 1-5 rating with no exported text labels
  - "text": open-ended free text

`group` is used to organize the question picker in the UI.
"""

# Ordered 1-5 text scales as they appear in the raw data (both satisfaction and
# agreement wording share the same 5-point structure).
SATISFACTION_ORDER = [
    "Extremely dissatisfied",
    "Somewhat dissatisfied",
    "Neither satisfied nor dissatisfied",
    "Somewhat satisfied",
    "Extremely satisfied",
]

AGREEMENT_ORDER = [
    "Strongly disagree",
    "Somewhat disagree",
    "Neither agree nor disagree",
    "Somewhat agree",
    "Strongly agree",
]

QUESTIONS = {
    "Q7_1": {
        "label": "Overall Satisfaction",
        "text": "Overall, how satisfied are you with your Scouting America program experience?",
        "type": "scale_10",
        "group": "Headline Metrics",
    },
    "Q8_1": {
        "label": "Likelihood to Recommend",
        "text": "How likely are you to recommend this Scouting program to another family?",
        "type": "scale_10",
        "group": "Headline Metrics",
    },
    "Q9_1": {
        "label": "Expectations Met",
        "text": "How well has the program met your expectations?",
        "type": "scale_10",
        "group": "Headline Metrics",
    },
    "Q10_1": {
        "label": "Quality & Variety of Activities",
        "text": "How satisfied are you with each of the following aspects of the program? - Quality and variety of activities",
        "type": "likert_5",
        "scale_order": SATISFACTION_ORDER,
        "group": "Program Aspects",
    },
    "Q10_2": {
        "label": "Safety & Youth Protection",
        "text": "How satisfied are you with each of the following aspects of the program? - Safety and youth protection practices",
        "type": "likert_5",
        "scale_order": SATISFACTION_ORDER,
        "group": "Program Aspects",
    },
    "Q10_3": {
        "label": "Adult Leadership & Volunteers",
        "text": "How satisfied are you with each of the following aspects of the program? - Adult leadership and volunteers",
        "type": "likert_5",
        "scale_order": SATISFACTION_ORDER,
        "group": "Program Aspects",
    },
    "Q10_4": {
        "label": "Communication from Leaders/Unit",
        "text": "How satisfied are you with each of the following aspects of the program? - Communication from leaders / unit",
        "type": "likert_5",
        "scale_order": SATISFACTION_ORDER,
        "group": "Program Aspects",
    },
    "Q10_5": {
        "label": "Meeting Frequency & Scheduling",
        "text": "How satisfied are you with each of the following aspects of the program? - Meeting frequency and scheduling",
        "type": "likert_5",
        "scale_order": SATISFACTION_ORDER,
        "group": "Program Aspects",
    },
    "Q10_6": {
        "label": "Advancement & Skill Development",
        "text": "How satisfied are you with each of the following aspects of the program? - Advancement and skill development",
        "type": "likert_5",
        "scale_order": SATISFACTION_ORDER,
        "group": "Program Aspects",
    },
    "Q10_7": {
        "label": "Value for the Cost",
        "text": "How satisfied are you with each of the following aspects of the program? - Value for the cost (dues, fees, gear)",
        "type": "likert_5",
        "scale_order": SATISFACTION_ORDER,
        "group": "Program Aspects",
    },
    "Q10_8": {
        "label": "Inclusiveness & Welcoming Environment",
        "text": "How satisfied are you with each of the following aspects of the program? - Inclusiveness and welcoming environment",
        "type": "likert_5",
        "scale_order": SATISFACTION_ORDER,
        "group": "Program Aspects",
    },
    "Q11_1": {
        "label": "Scout Growing in Character & Confidence",
        "text": "Please rate your level of agreement with the following statements. - My Scout is growing in character and confidence.",
        "type": "likert_5",
        "scale_order": AGREEMENT_ORDER,
        "group": "Agreement Statements",
    },
    "Q11_2": {
        "label": "Leaders Well-Prepared & Organized",
        "text": "Please rate your level of agreement with the following statements. - Leaders are well-prepared and organized.",
        "type": "likert_5",
        "scale_order": AGREEMENT_ORDER,
        "group": "Agreement Statements",
    },
    "Q11_3": {
        "label": "Feel Informed About the Program",
        "text": "Please rate your level of agreement with the following statements. - I feel informed about what is happening in the program.",
        "type": "likert_5",
        "scale_order": AGREEMENT_ORDER,
        "group": "Agreement Statements",
    },
    "Q11_4": {
        "label": "Concerns Taken Seriously",
        "text": "Please rate your level of agreement with the following statements. - Concerns I raise are taken seriously and addressed.",
        "type": "likert_5",
        "scale_order": AGREEMENT_ORDER,
        "group": "Agreement Statements",
    },
    "Q11_5": {
        "label": "Worth the Time & Money",
        "text": "Please rate your level of agreement with the following statements. - The program is worth the time and money we invest.",
        "type": "likert_5",
        "scale_order": AGREEMENT_ORDER,
        "group": "Agreement Statements",
    },
    "Q11_6": {
        "label": "Scout Learned Useful Skills",
        "text": "Please rate your level of agreement with the following statements. - My Scout learned useful skills such as teamwork and communication that will help them succeed.",
        "type": "likert_5",
        "scale_order": AGREEMENT_ORDER,
        "group": "Agreement Statements",
    },
    "Q15_1": {
        "label": "Communication Satisfaction",
        "text": "How satisfied are you with how the program communicates with you?",
        "type": "scale_5_num",
        "group": "Other Ratings",
    },
    "Q17_1": {
        "label": "Safety Confidence",
        "text": "How confident are you in Scouting's commitment to youth safety?",
        "type": "scale_5_num",
        "group": "Other Ratings",
    },
    "Q18_1": {
        "label": "Likelihood to Re-register",
        "text": "How likely are you to continue with / re-register for the Scouting program next year?",
        "type": "scale_5_num",
        "group": "Other Ratings",
    },
}

# Open-ended text questions, shown in their own tab.
TEXT_QUESTIONS = {
    "Q13": "What do you value MOST about the program? What is working well?",
    "Q14": "What has been frustrating or disappointing? What would you most like to see improved?",
    "Q19": "What is the main reason for your answer above?",
    "Q20": "If you could change ONE thing about the Scouting program, what would it be?",
    "Q21": "Any other comments or suggestions you'd like to share?",
}

# Embedded-data / demographic filter dimensions (straight categorical columns).
CATEGORICAL_FILTERS = {
    "Boro": "Borough",
    "District": "District",
    "Program": "Program",
    "Unit": "Unit",
    "Gender": "Gender",
    "RegStatus": "Registration Status",
    "Demo": "Demographic Group",
    "Q5": "Relationship to Scouting",
}

# Tenure is ordinal - fixed display order regardless of alphabetical sort.
TENURE_COLUMN = "Q6"
TENURE_ORDER = ["Less than 1 year", "1-2 years", "3-5 years", "5+ years"]

# Which question drives the derived "Satisfaction Level" filter band.
SATISFACTION_SOURCE_COLUMN = "Q7_1"
SATISFACTION_BANDS = [
    (1, 4, "Low (1-4)"),
    (5, 7, "Medium (5-7)"),
    (8, 10, "High (8-10)"),
]
SATISFACTION_BAND_ORDER = [b[2] for b in SATISFACTION_BANDS]


def satisfaction_band(value):
    """Map a 1-10 overall satisfaction score to its band label."""
    if value is None:
        return None
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    for lo, hi, label in SATISFACTION_BANDS:
        if lo <= v <= hi:
            return label
    return None
