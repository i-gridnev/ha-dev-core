"""My sensor platform."""
from datetime import timedelta
import logging
from typing import Optional

from homeassistant import config_entries, core
from homeassistant.const import CONF_COUNT, CONF_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
import voluptuous as vol

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=2)

MY_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_COUNT): int
    }
)

# REPO_SCHEMA = vol.Schema(
#     {vol.Required(CONF_PATH): cv.string, vol.Optional(CONF_NAME): cv.string}
# )

# PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
#     {
#         vol.Required(CONF_ACCESS_TOKEN): cv.string,
#         vol.Required(CONF_REPOS): vol.All(cv.ensure_list, [REPO_SCHEMA]),
#         vol.Optional(CONF_URL): cv.url,
#     }
# )


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Invoke a setup sensors from a config entry created in the integrations UI."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    sensor = [MySensor(config[CONF_NAME], config[CONF_COUNT])]
    async_add_entities(sensor, update_before_add=True)


# async def async_setup_platform(
#     hass: HomeAssistantType,
#     config: ConfigType,
#     async_add_entities: Callable,
#     discovery_info: Optional[DiscoveryInfoType] = None,
# ) -> None:
#     """Set up the sensor platform."""
#     session = async_get_clientsession(hass)
#     github = GitHubAPI(session, "requester", oauth_token=config[CONF_ACCESS_TOKEN])
#     sensors = [GitHubRepoSensor(github, repo) for repo in config[CONF_REPOS]]
#     async_add_entities(sensors, update_before_add=True)


class MySensor(Entity):
    """Representation of a GitHub Repo sensor."""

    def __init__(self, start_val: int, name: str) -> None:
        """Init my sensor."""
        super().__init__()
        self._name = name
        self._state = start_val
        self._available = True

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    # @property
    # def unique_id(self) -> str:
    #     """Return the unique ID of the sensor."""
    #     return self.repo

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def state(self) -> Optional[str]:
        """Get state."""
        return self._state

    # @property
    # def device_state_attributes(self) -> Dict[str, Any]:
    #     return self.attrs

    async def async_update(self):
        """Update state."""
        self._state = self._state + 1
        _LOGGER.info("Sensor %s inc to %s", self._name, self._state)
