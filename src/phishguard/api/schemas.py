from pydantic import BaseModel, Field


class URLAnalysisRequest(BaseModel):
    url: str = Field(min_length=1)
    enable_whois: bool = False
