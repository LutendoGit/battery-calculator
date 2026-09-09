import modules.lithium_education as education


def test_module_5_assessment_matches_updated_content():
    questions = education.MODULE_5_ASSESSMENT["questions"]

    assert len(questions) == 25
    assert questions[0]["question"] == (
        "What should determine the design of an energy system before equipment is selected?"
    )
    assert questions[0]["answer"] == "B"
    assert questions[10]["question"] == (
        "Why should the calculated energy requirement not simply be treated as the final\n"
        "battery size?"
    )
    assert questions[10]["answer"] == "A"
    assert questions[11]["question"] == (
        "A customer wants longer backup time without increasing the essential load.\n"
        "Which part of the system will generally need more capacity?"
    )
    assert questions[11]["answer"] == "A"
    assert questions[24]["answer"] == "C"
