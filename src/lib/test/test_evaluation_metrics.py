# test_evaluation_metrics.py
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


from evaluation.evaluation_metrics import (
    evaluate_model_output,
    evaluate_model_output_entities,
    evaluate_model_output_start_positions,
    evaluate_model_output_end_positions,
)


def test_evaluate_model_output():
    reference = {
        "adverse_drug_reactions": [("Hunger pangs", 0, 12)],
        "diseases_or_medical_conditions": [],
        "medications": [],
        "clinical_findings": [],
        "symptoms_experienced_by_patients": [],
    }

    models = [
        {
            "adverse_drug_reactions": [
                {"name": "Hunger pangs", "start_position": 0, "end_position": 12}
            ],
            "diseases_or_medical_conditions": [],
            "medications": [],
            "clinical_findings": [],
            "symptoms_experienced_by_patients": [],
        },
        {
            "adverse_drug_reactions": [("Hunger pangs", 2, 14)],
            "diseases_or_medical_conditions": [],
            "medications": [],
            "clinical_findings": [],
            "symptoms_experienced_by_patients": [],
        },
        {
            "adverse_drug_reactions": [("Hunger pangs", 0, 15)],
            "diseases_or_medical_conditions": [],
            "medications": [],
            "clinical_findings": [],
            "symptoms_experienced_by_patients": [],
        },
        {
            "adverse_drug_reactions": [],
            "diseases_or_medical_conditions": [("Hunger pangs", 0, 12)],
            "medications": [],
            "clinical_findings": [],
            "symptoms_experienced_by_patients": [],
        },
        {
            "adverse_drug_reactions": [("Hunger  pangs", 0, 12)],
            "diseases_or_medical_conditions": [],
            "medications": [],
            "clinical_findings": [],
            "symptoms_experienced_by_patients": [],
        },
    ]

    expected_results = [
        (True, True, True, True),
        (False, True, True, True),
        (False, False, True, True),
        (False, False, False, True),
        (False, False, False, False),
    ]

    for model, expected in zip(models, expected_results):
        verif1, verif2, verif3, verif4 = evaluate_model_output(reference, model)
        assert (verif1, verif2, verif3, verif4) == expected


def test_evaluate_model_output_entities():
    expected_output_sample = {
        "adverse_drug_reactions": [
            ("anxious", 12, 19),
            ("words would not form", 50, 70),
            ("anxiety", 250, 257),
            ("fear", 258, 262),
            ("tingling", 349, 357),
            ("pains", 368, 373),
            ("muscle tingley thing", 621, 641),
        ],
        "diseases_or_medical_conditions": [],
        "medications": [("lipitor", 537, 544), ("Atorvastatin", 678, 690)],
        "clinical_findings": [],
        "symptoms_experienced_by_patients": [],
    }

    output_sample_format_1 = {
        "adverse_drug_reactions": [
            {
                "name": "more anxious about EVERYTHING",
                "start_position": 7,
                "end_position": 36,
            },
            {
                "name": "words would not form in my head",
                "start_position": 52,
                "end_position": 82,
            },
            {"name": "disturbing", "start_position": 88, "end_position": 98},
            {
                "name": "constant anxiety/fear",
                "start_position": 166,
                "end_position": 186,
            },
            {"name": "tingling", "start_position": 241, "end_position": 249},
            {"name": "weird pains", "start_position": 258, "end_position": 270},
            {
                "name": "muscle tingley thing",
                "start_position": 494,
                "end_position": 514,
            },
            {"name": "side affects", "start_position": 561, "end_position": 572},
        ],
        "diseases_or_medical_conditions": [],
        "medications": [
            {"name": "lipitor", "start_position": 379, "end_position": 386},
            {"name": "Atorvastatin", "start_position": 527, "end_position": 539},
        ],
        "clinical_findings": [],
        "symptoms_experienced_by_patients": [],
    }

    output_sample_format_2 = {
        "adverse_drug_reactions": [
            {
                "name": "more anxious about EVERYTHING",
                "start_position": 7,
                "end_position": 36,
            },
            {
                "name": "words would not form in my head",
                "start_position": 52,
                "end_position": 82,
            },
            {"name": "disturbing", "start_position": 88, "end_position": 98},
            {
                "name": "constant anxiety/fear",
                "start_position": 166,
                "end_position": 186,
            },
            {"name": "tingling", "start_position": 241, "end_position": 249},
            {"name": "weird pains", "start_position": 258, "end_position": 270},
            {
                "name": "muscle tingley thing",
                "start_position": 494,
                "end_position": 514,
            },
            {"name": "side affects", "start_position": 561, "end_position": 572},
        ],
        "diseases_or_medical_conditions": [],
        "medications": [
            {"name": "lipitor", "start_position": 379, "end_position": 386},
            {"name": "Atorvastatin", "start_position": 527, "end_position": 539},
        ],
        "clinical_findings": [],
        "symptoms_experienced_by_patients": [],
    }

    expected_output_sample_v2 = {
        "adverse_drug_reactions": [
            ("short term memory loss", 51, 73),
            ("extreme fatigue", 75, 90),
            ("reflux", 138, 144),
            ("fatigue", 655, 662),
        ],
        "diseases_or_medical_conditions": [],
        "medications": [
            ("Lipitor", 216, 223),
            ("Tricor", 248, 254),
            ("Lipitor", 276, 283),
            ("Tricor", 443, 449),
            ("Lipitor", 472, 479),
            ("Lipitor", 580, 587),
        ],
        "clinical_findings": [],
        "symptoms_experienced_by_patients": [],
    }
    output_sample_format_1_v2 = {
        "adverse_drug_reactions": [],
        "diseases_or_medical_conditions": [],
        "medications": [
            ("Lipitor", 216, 223),
            ("Tricor", 248, 254),
            ("Lipitor", 276, 283),
            ("Tricor", 443, 449),
            ("Lipitor", 472, 479),
            ("Lipitor", 580, 587),
        ],
        "clinical_findings": [],
        "symptoms_experienced_by_patients": [
            ("short term memory loss", 51, 73),
            ("extreme fatigue", 75, 90),
            ("joint pain", 91, 101),
            ("reflux", 138, 144),
        ],
    }
    output_sample_format_2_v2 = {
        "adverse_drug_reactions": [],
        "diseases_or_medical_conditions": [],
        "medications": [
            {"name": "Lipitor", "start_position": 216, "end_position": 223},
            {"name": "Tricor", "start_position": 248, "end_position": 254},
            {"name": "Lipitor", "start_position": 276, "end_position": 283},
            {"name": "Tricor", "start_position": 443, "end_position": 449},
            {"name": "Lipitor", "start_position": 472, "end_position": 479},
            {"name": "Lipitor", "start_position": 580, "end_position": 587},
        ],
        "clinical_findings": [],
        "symptoms_experienced_by_patients": [
            {
                "name": "short term memory loss",
                "start_position": 51,
                "end_position": 73,
            },
            {"name": "extreme fatigue", "start_position": 75, "end_position": 90},
            {"name": "joint pain", "start_position": 91, "end_position": 101},
            {"name": "reflux", "start_position": 138, "end_position": 144},
        ],
    }

    num_expected_1, num_correct_1, num_correct_classified_1 = (
        evaluate_model_output_entities(expected_output_sample, output_sample_format_1)
    )
    num_expected_2, num_correct_2, num_correct_classified_2 = (
        evaluate_model_output_entities(expected_output_sample, output_sample_format_2)
    )

    num_expected_1_v2, num_correct_1_v2, num_correct_classified_1_v2 = (
        evaluate_model_output_entities(
            expected_output_sample_v2, output_sample_format_1_v2
        )
    )
    num_expected_2_v2, num_correct_2_v2, num_correct_classified_2_v2 = (
        evaluate_model_output_entities(
            expected_output_sample_v2, output_sample_format_2_v2
        )
    )

    assert num_expected_1 == 9
    assert num_correct_1 == 4
    assert num_correct_classified_1 == 4
    assert num_expected_2 == 9
    assert num_correct_2 == 4
    assert num_correct_classified_2 == 4
    assert num_expected_1_v2 == 10
    assert num_correct_1_v2 == 9
    assert num_correct_classified_1_v2 == 6
    assert num_expected_2_v2 == 10
    assert num_correct_2_v2 == 9
    assert num_correct_classified_2_v2 == 6


def test_evaluate_model_output_start_positions():
    expected_output_sample = {
        "adverse_drug_reactions": [
            ("Muscle wasting", 0, 14),
            ("weakness", 16, 24),
            ("fatigue", 26, 33),
            ("diarrhea", 35, 43),
            ("anorexic", 45, 53),
            ("weight loss", 148, 159),
            ("muscles wasting", 181, 196),
            ("Kidney function became a problem", 198, 230),
            ("significan heart muscle weakness", 235, 267),
        ],
        "diseases_or_medical_conditions": [],
        "medications": [],
        "clinical_findings": [],
        "symptoms_experienced_by_patients": [],
    }
    output_sample_format_1 = {
        "adverse_drug_reactions": [
            ("Muscle wasting", 0, 14),
            ("weakness", 16, 24),
            ("fatigue", 26, 33),
            ("diarrhea", 35, 43),
            ("anorexic", 45, 53),
            ("weight loss", 151, 162),
            ("muscles wasting", 185, 200),
            ("Kidney function became a problem", 202, 235),
            ("heart muscle weakness", 252, 273),
        ],
        "diseases_or_medical_conditions": [],
        "medications": [],
        "clinical_findings": [],
        "symptoms_experienced_by_patients": [],
    }
    output_sample_format_2 = {
        "adverse_drug_reactions": [
            {"name": "Muscle wasting", "start_position": 0, "end_position": 14},
            {"name": "weakness", "start_position": 16, "end_position": 24},
            {"name": "fatigue", "start_position": 26, "end_position": 33},
            {"name": "diarrhea", "start_position": 35, "end_position": 43},
            {"name": "anorexic", "start_position": 45, "end_position": 53},
            {"name": "weight loss", "start_position": 151, "end_position": 162},
            {"name": "muscles wasting", "start_position": 185, "end_position": 200},
            {
                "name": "Kidney function became a problem",
                "start_position": 202,
                "end_position": 235,
            },
            {
                "name": "heart muscle weakness",
                "start_position": 252,
                "end_position": 273,
            },
        ],
        "diseases_or_medical_conditions": [],
        "medications": [],
        "clinical_findings": [],
        "symptoms_experienced_by_patients": [],
    }

    exact_matches_1, within_2_matches_1, within_5_matches_1, within_10_matches_1 = (
        evaluate_model_output_start_positions(
            expected_output_sample, output_sample_format_1
        )
    )
    exact_matches_2, within_2_matches_2, within_5_matches_2, within_10_matches_2 = (
        evaluate_model_output_start_positions(
            expected_output_sample, output_sample_format_2
        )
    )

    assert exact_matches_1 == 5
    assert within_2_matches_1 == 5
    assert within_5_matches_1 == 8
    assert within_10_matches_1 == 8
    assert exact_matches_2 == 5
    assert within_2_matches_2 == 5
    assert within_5_matches_2 == 8
    assert within_10_matches_2 == 8


def test_evaluate_model_output_end_positions():
    expected_output_sample = {
        "adverse_drug_reactions": [
            ("Muscle wasting", 0, 14),
            ("weakness", 16, 24),
            ("fatigue", 26, 33),
            ("diarrhea", 35, 43),
            ("anorexic", 45, 53),
            ("weight loss", 148, 159),
            ("muscles wasting", 181, 196),
            ("Kidney function became a problem", 198, 230),
            ("significan heart muscle weakness", 235, 267),
        ],
        "diseases_or_medical_conditions": [],
        "medications": [],
        "clinical_findings": [],
        "symptoms_experienced_by_patients": [],
    }
    output_sample_format_1 = {
        "adverse_drug_reactions": [
            ("Muscle wasting", 0, 14),
            ("weakness", 16, 24),
            ("fatigue", 26, 33),
            ("diarrhea", 35, 43),
            ("anorexic", 45, 53),
            ("weight loss", 151, 162),
            ("muscles wasting", 185, 200),
            ("Kidney function became a problem", 202, 235),
            ("heart muscle weakness", 252, 273),
        ],
        "diseases_or_medical_conditions": [],
        "medications": [],
        "clinical_findings": [],
        "symptoms_experienced_by_patients": [],
    }
    output_sample_format_2 = {
        "adverse_drug_reactions": [
            {"name": "Muscle wasting", "start_position": 0, "end_position": 14},
            {"name": "weakness", "start_position": 16, "end_position": 24},
            {"name": "fatigue", "start_position": 26, "end_position": 33},
            {"name": "diarrhea", "start_position": 35, "end_position": 43},
            {"name": "anorexic", "start_position": 45, "end_position": 53},
            {"name": "weight loss", "start_position": 151, "end_position": 162},
            {"name": "muscles wasting", "start_position": 185, "end_position": 200},
            {
                "name": "Kidney function became a problem",
                "start_position": 202,
                "end_position": 235,
            },
            {
                "name": "heart muscle weakness",
                "start_position": 252,
                "end_position": 273,
            },
        ],
        "diseases_or_medical_conditions": [],
        "medications": [],
        "clinical_findings": [],
        "symptoms_experienced_by_patients": [],
    }

    exact_matches_1, within_2_matches_1, within_5_matches_1, within_10_matches_1 = (
        evaluate_model_output_end_positions(
            expected_output_sample, output_sample_format_1
        )
    )
    exact_matches_2, within_2_matches_2, within_5_matches_2, within_10_matches_2 = (
        evaluate_model_output_end_positions(
            expected_output_sample, output_sample_format_2
        )
    )

    assert exact_matches_1 == 5
    assert within_2_matches_1 == 5
    assert within_5_matches_1 == 8
    assert within_10_matches_1 == 8
    assert exact_matches_2 == 5
    assert within_2_matches_2 == 5
    assert within_5_matches_2 == 8
    assert within_10_matches_2 == 8
