from pydantic import BaseModel


class NewsList(BaseModel):
    news: list[str]


class NewsValidation(BaseModel):
    is_wrong_date: bool
    is_informational: bool
    is_duplicate: bool


class NewsValidationList(BaseModel):
    validations: list[NewsValidation]


class NewsScore(BaseModel):
    score: int  # -5 to 5
    reasoning: str


class NewsScoreList(BaseModel):
    scores: list[NewsScore]