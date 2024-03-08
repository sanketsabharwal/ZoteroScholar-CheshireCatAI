from pydantic import BaseModel, Field

from cat.mad_hatter.decorators import tool, plugin


class Settings(BaseModel):
    zotero_user_id: str = Field(
        title="Zotero User ID",
        description="Your Zotero User ID",
        default=""
    )
    zotero_api_key: str = Field(
        title="Zotero API Key",
        description="Your Zotero API Key",
        default=""
    )


@plugin
def settings_model():
    return Settings