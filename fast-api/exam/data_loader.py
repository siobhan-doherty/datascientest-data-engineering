import pandas as pd


def load_questions():
    df = pd.read_excel("questions_en.xlsx", engine = "openpyxl")
    df = df.rename(
        columns = {
            "responseA": "answerA",
            "responseB": "answerB",
            "responseC": "answerC",
            "responseD": "answerD",
        }
    )
    # convert any pandas NaN to None
    df = df.where(pd.notnull(df), None)
    return df.to_dict(orient = "records")

QUESTIONS = load_questions()
