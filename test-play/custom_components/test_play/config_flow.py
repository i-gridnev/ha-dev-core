"""sdfsdfsd."""
import logging
from typing import Any, Optional

from homeassistant import config_entries
from homeassistant.const import CONF_COUNT, CONF_NAME
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

MY_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_COUNT): int
    }
)


async def validate_startval(startval: int) -> None:
    """Validate startval."""
    if startval > 50:
        raise ValueError


class GithubCustomConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Custom config flow."""

    data: Optional[dict[str, Any]]

    async def async_step_user(self, user_input: Optional[dict[str, Any]] = None):
        """Invoke when a user initiates a flow via the user interface."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                await validate_startval(user_input[CONF_COUNT])
            except ValueError:
                errors["base"] = "auth"
            if not errors:
                # Input is valid, set data.
                self.data = user_input
                # Return the form of the next step.
                return self.async_create_entry(title=self.data[CONF_NAME], data=self.data)

        return self.async_show_form(
            step_id="user", data_schema=MY_SCHEMA, errors=errors
        )

    # async def async_step_repo(self, user_input: Optional[Dict[str, Any]] = None):
    #     """Second step in config flow to add a repo to watch."""
    #     errors: Dict[str, str] = {}
    #     if user_input is not None:
    #         # Validate the path.
    #         try:
    #             validate_path(user_input[CONF_PATH])
    #         except ValueError:
    #             errors["base"] = "invalid_path"

    #         if not errors:
    #             # Input is valid, set data.
    #             self.data[CONF_REPOS].append(
    #                 {
    #                     "path": user_input[CONF_PATH],
    #                     "name": user_input.get(CONF_NAME, user_input[CONF_PATH]),
    #                 }
    #             )
    #             # If user ticked the box show this form again so they can add an
    #             # additional repo.
    #             if user_input.get("add_another", False):
    #                 return await self.async_step_repo()

    #             # User is done adding repos, create the config entry.
    #             return self.async_create_entry(title="GitHub Custom", data=self.data)

    #     return self.async_show_form(
    #         step_id="repo", data_schema=REPO_SCHEMA, errors=errors
    #     )
