#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © Nekoka.tt 2019-2020
#
# This file is part of Hikari.
#
# Hikari is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hikari is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Hikari. If not, see <https://www.gnu.org/licenses/>.
"""Components and entities that are used to describe guilds on Discord.
"""
__all__ = [
    "ActivityFlag",
    "ActivityType",
    "GuildChannel",
    "GuildTextChannel",
    "GuildNewsChannel",
    "GuildStoreChannel",
    "GuildVoiceChannel",
    "GuildCategory",
    "GuildRole",
    "GuildFeature",
    "GuildSystemChannelFlag",
    "GuildMessageNotificationsLevel",
    "GuildExplicitContentFilterLevel",
    "GuildMFALevel",
    "GuildVerificationLevel",
    "GuildPremiumTier",
    "Guild",
    "GuildMember",
    "GuildMemberPresence",
    "GuildIntegration",
    "GuildMemberBan",
    "PartialGuild",
    "PresenceStatus",
]

import datetime
import enum
import typing

from hikari.core import channels
from hikari.core import emojis as _emojis
from hikari.core import entities
from hikari.core import permissions
from hikari.core import snowflakes
from hikari.core import users
from hikari.internal_utilities import cdn
from hikari.internal_utilities import dates
from hikari.internal_utilities import marshaller
from hikari.internal_utilities import transformations


@marshaller.attrs(slots=True)
class GuildChannel(channels.Channel, entities.Deserializable):
    """The base for anything that is a guild channel."""


@marshaller.attrs(slots=True)
class GuildTextChannel(GuildChannel):
    ...


@marshaller.attrs(slots=True)
class GuildVoiceChannel(GuildChannel):
    ...


@marshaller.attrs(slots=True)
class GuildCategory(GuildChannel):
    ...


@marshaller.attrs(slots=True)
class GuildStoreChannel(GuildChannel):
    ...


@marshaller.attrs(slots=True)
class GuildNewsChannel(GuildChannel):
    ...


def parse_guild_channel(payload) -> GuildChannel:
    class Duff:
        id = snowflakes.Snowflake(123)

    # FIXME: implement properly
    return Duff()


@enum.unique
class GuildExplicitContentFilterLevel(enum.IntEnum):
    """Represents the explicit content filter setting for a guild."""

    #: No explicit content filter.
    DISABLED = 0

    #: Filter posts from anyone without a role.
    MEMBERS_WITHOUT_ROLES = 1

    #: Filter all posts.
    ALL_MEMBERS = 2


@enum.unique
class GuildFeature(str, enum.Enum):
    """Features that a guild can provide."""

    #: Guild has access to set an animated guild icon.
    ANIMATED_ICON = "ANIMATED_ICON"
    #: Guild has access to set a guild banner image.
    BANNER = "BANNER"
    #: Guild has access to use commerce features (i.e. create store channels).
    COMMERCE = "COMMERCE"
    #: Guild is able to be discovered in the directory.
    DISCOVERABLE = "DISCOVERABLE"
    #: Guild is able to be featured in the directory.
    FEATURABLE = "FEATURABLE"
    #: Guild has access to set an invite splash background.
    INVITE_SPLASH = "INVITE_SPLASH"
    #: More emojis can be hosted in this guild than normal.
    MORE_EMOJI = "MORE_EMOJI"
    #: Guild has access to create news channels.
    NEWS = "NEWS"
    #: People can view channels in this guild without joining.
    LURKABLE = "LURKABLE"
    #: Guild is partnered.
    PARTNERED = "PARTNERED"
    #: Guild is public, go figure.
    PUBLIC = "PUBLIC"
    #: Guild cannot be public. Who would have guessed?
    PUBLIC_DISABLED = "PUBLIC_DISABLED"
    #: Guild has access to set a vanity URL.
    VANITY_URL = "VANITY_URL"
    #: Guild is verified.
    VERIFIED = "VERIFIED"
    #: Guild has access to set 384kbps bitrate in voice (previously
    #: VIP voice servers).
    VIP_REGIONS = "VIP_REGIONS"


@enum.unique
class GuildMessageNotificationsLevel(enum.IntEnum):
    """Represents the default notification level for new messages in a guild."""

    #: Notify users when any message is sent.
    ALL_MESSAGES = 0

    #: Only notify users when they are @mentioned.
    ONLY_MENTIONS = 1


@enum.unique
class GuildMFALevel(enum.IntEnum):
    """Represents the multi-factor authorization requirement for a guild."""

    #: No MFA requirement.
    NONE = 0

    #: MFA requirement.
    ELEVATED = 1


@enum.unique
class GuildPremiumTier(enum.IntEnum):
    """Tier for Discord Nitro boosting in a guild."""

    #: No Nitro boosts.
    NONE = 0

    #: Level 1 Nitro boost.
    TIER_1 = 1

    #: Level 2 Nitro boost.
    TIER_2 = 2

    #: Level 3 Nitro boost.
    TIER_3 = 3


class GuildSystemChannelFlag(enum.IntFlag):
    """Defines which features are suppressed in the system channel."""

    #: Display a message about new users joining.
    SUPPRESS_USER_JOIN = 1
    #: Display a message when the guild is Nitro boosted.
    SUPPRESS_PREMIUM_SUBSCRIPTION = 2


@enum.unique
class GuildVerificationLevel(enum.IntEnum):
    """Represents the level of verification a user needs to provide for their
    account before being allowed to participate in a guild."""

    #: Unrestricted
    NONE = 0

    #: Must have a verified email on their account.
    LOW = 1

    #: Must have been registered on Discord for more than 5 minutes.
    MEDIUM = 2

    #: (╯°□°）╯︵ ┻━┻ - must be a member of the guild for longer than 10 minutes.
    HIGH = 3

    #: ┻━┻ミヽ(ಠ益ಠ)ﾉ彡┻━┻ - must have a verified phone number.
    VERY_HIGH = 4


@marshaller.attrs(slots=True)
class GuildMember(entities.HikariEntity, entities.Deserializable):
    """Used to represent a guild bound member."""

    #: This member's user object.
    #:
    #: :type: :obj:`users.User`
    user: users.User = marshaller.attrib(deserializer=users.User.deserialize)

    #: This member's nickname, if set.
    #:
    #: :type: :obj:`str`, optional
    nickname: typing.Optional[str] = marshaller.attrib(raw_name="nick", deserializer=str, if_none=None)

    #: A sequence of the IDs of the member's current roles.
    #:
    #: :type: :obj:`typing.Sequence` [ :obj:`snowflakes.Snowflake` ]
    role_ids: typing.Sequence[snowflakes.Snowflake] = marshaller.attrib(
        raw_name="roles", deserializer=lambda role_ids: [snowflakes.Snowflake.deserialize(rid) for rid in role_ids],
    )

    #: The datetime of when this member joined the guild they belong to.
    #:
    #: :type: :obj:`datetime.datetime`
    joined_at: datetime.datetime = marshaller.attrib(deserializer=dates.parse_iso_8601_ts)

    #: The datetime of when this member started "boosting" this guild.
    #: Will be ``None`` if they aren't boosting.
    #:
    #: :type: :obj:`datetime.datetime`, optional
    premium_since: typing.Optional[datetime.datetime] = marshaller.attrib(
        deserializer=dates.parse_iso_8601_ts, if_none=None, if_undefined=None,
    )

    #: Whether this member is deafened by this guild in it's voice channels.
    #:
    #: :type: :obj:`bool`
    is_deaf: bool = marshaller.attrib(raw_name="deaf", deserializer=bool)

    #: Whether this member is muted by this guild in it's voice channels.
    #:
    #: :type: :obj:`bool`
    is_mute: bool = marshaller.attrib(raw_name="mute", deserializer=bool)


@marshaller.attrs(slots=True)
class GuildRole(snowflakes.UniqueEntity, entities.Deserializable):
    ...


@enum.unique
class ActivityType(enum.IntEnum):
    """
    The activity state.
    """

    #: Shows up as ``Playing <name>``
    PLAYING = 0
    #: Shows up as ``Streaming <name>``.
    #:
    #: Warnings
    #: --------
    #: Corresponding presences must be associated with VALID Twitch or YouTube
    #: stream URLS!
    STREAMING = 1
    #: Shows up as ``Listening to <name>``.
    LISTENING = 2
    #: Shows up as ``Watching <name>``. Note that this is not officially
    #: documented, so will be likely removed in the near future.
    WATCHING = 3
    #: A custom status.
    #:
    #: To set an emoji with the status, place a unicode emoji or Discord emoji
    #: (``:smiley:``) as the first part of the status activity name.
    CUSTOM = 4


@marshaller.attrs(slots=True)
class ActivityTimestamps(entities.HikariEntity, entities.Deserializable):
    """The datetimes for the start and/or end of an activity session."""

    #: When this activity's session was started, if applicable.
    #:
    #: :type: :obj:`datetime.datetime`, optional
    start: typing.Optional[datetime.datetime] = marshaller.attrib(
        deserializer=dates.unix_epoch_to_ts, if_undefined=None
    )

    #: When this activity's session will end, if applicable.
    #:
    #: :type: :obj:`datetime.datetime`, optional
    end: typing.Optional[datetime.datetime] = marshaller.attrib(deserializer=dates.unix_epoch_to_ts, if_undefined=None)


@marshaller.attrs(slots=True)
class ActivityParty(entities.HikariEntity, entities.Deserializable):
    """Used to represent activity groups of users."""

    #: The string id of this party instance, if set.
    #:
    #: :type: :obj:`str`, optional
    id: typing.Optional[str] = marshaller.attrib(deserializer=str, if_undefined=None)

    #: The size metadata of this party, if applicable.
    #:
    #: :type: :obj:`typing.Tuple` [ :obj:`int`, :obj:`int` ], optional
    _size_information: typing.Optional[typing.Tuple[int, int]] = marshaller.attrib(
        raw_name="size", deserializer=tuple, if_undefined=None,
    )

    @property
    def current_size(self) -> typing.Optional[int]:
        """The current size of this party, if applicable."""
        return self._size_information and self._size_information[0] or None

    @property
    def max_size(self) -> typing.Optional[int]:
        """The maximum size of this party, if applicable"""
        return self._size_information and self._size_information[1] or None


@marshaller.attrs(slots=True)
class ActivityAssets(entities.HikariEntity, entities.Deserializable):
    """Used to represent possible assets for an activity."""

    #: The ID of the asset's large image, if set.
    #:
    #: :type: :obj:`str`, optional
    large_image: typing.Optional[str] = marshaller.attrib(deserializer=str, if_undefined=None)

    #: The text that'll appear when hovering over the large image, if set.
    #:
    #: :type: :obj:`str`, optional
    large_text: typing.Optional[str] = marshaller.attrib(deserializer=str, if_undefined=None)

    #: The ID of the asset's small image, if set.
    #:
    #: :type: :obj:`str`, optional
    small_image: typing.Optional[str] = marshaller.attrib(deserializer=str, if_undefined=None)

    #: The text that'll appear when hovering over the small image, if set.
    #:
    #: :type: :obj:`str`, optional
    small_text: typing.Optional[str] = marshaller.attrib(deserializer=str, if_undefined=None)


@marshaller.attrs(slots=True)
class ActivitySecret(entities.HikariEntity, entities.Deserializable):
    """The secrets used for interacting with an activity party."""

    #: The secret used for joining a party, if applicable.
    #:
    #: :type: :obj:`str`, optional
    join: typing.Optional[str] = marshaller.attrib(deserializer=str, if_undefined=None)

    #: The secret used for spectating a party, if applicable.
    #:
    #: :type: :obj:`str`, optional
    spectate: typing.Optional[str] = marshaller.attrib(deserializer=str, if_undefined=None)

    #: The secret used for joining a party, if applicable.
    #:
    #: :type: :obj:`str`, optional
    match: typing.Optional[str] = marshaller.attrib(deserializer=str, if_undefined=None)


class ActivityFlag(enum.IntFlag):
    """
    Flags that describe what an activity includes,
    can be more than one using bitwise-combinations.
    """

    INSTANCE = 1 << 0
    JOIN = 1 << 1
    SPECTATE = 1 << 2
    JOIN_REQUEST = 1 << 3
    SYNC = 1 << 4
    PLAY = 1 << 5


@marshaller.attrs(slots=True)
class PresenceActivity(entities.HikariEntity, entities.Deserializable):
    """Represents an activity that'll be attached to a member's presence."""

    #: The activity's name.
    #:
    #: :type: :obj:`str`
    name: str = marshaller.attrib(deserializer=str)

    #: The activity's type.
    #:
    #: :type: :obj:`ActivityType`
    type: ActivityType = marshaller.attrib(deserializer=ActivityType)

    #: The url for a ``STREAM` type activity, if applicable
    #:
    #: :type: :obj:`url`, optional
    url: typing.Optional[str] = marshaller.attrib(deserializer=str, if_undefined=None, if_none=None)

    #: When this activity was added to the user's session.
    #:
    #: :type: :obj:`datetime.datetime`
    created_at: datetime.datetime = marshaller.attrib(deserializer=dates.unix_epoch_to_ts)

    #: The timestamps for when this activity's current state will start and
    #: end, if applicable.
    #:
    #: :type: :obj:`ActivityTimestamps`, optional
    timestamps: ActivityTimestamps = marshaller.attrib(deserializer=ActivityTimestamps.deserialize)

    #: The ID of the application this activity is for, if applicable.
    #:
    #: :type: :obj:`snowflakes.Snowflake`, optional
    application_id: typing.Optional[snowflakes.Snowflake] = marshaller.attrib(
        deserializer=snowflakes.Snowflake.deserialize, if_undefined=None
    )

    #: The text that describes what the activity's target is doing, if set.
    #:
    #: :type: :obj:`str`, optional
    details: typing.Optional[str] = marshaller.attrib(deserializer=str, if_undefined=None, if_none=None)

    #: The current status of this activity's target, if set.
    #:
    #: :type: :obj:`str`, optional
    state: typing.Optional[str] = marshaller.attrib(deserializer=str, if_undefined=None, if_none=None)

    #: The emoji of this activity, if it is a custom status and set.
    #:
    #: :type: :obj:`typing.Union` [ :obj:`_emojis.UnicodeEmoji`, :obj:`_emojis.UnknownEmoji` ], optional
    emoji: typing.Union[None, _emojis.UnicodeEmoji, _emojis.UnknownEmoji] = marshaller.attrib(
        deserializer=_emojis.deserialize_reaction_emoji, if_undefined=None
    )

    #: Information about the party associated with this activity, if set.
    #:
    #: :type: :obj:`ActivityParty`, optional
    party: typing.Optional[ActivityParty] = marshaller.attrib(deserializer=ActivityParty.deserialize, if_undefined=None)

    #: Images and their hover over text for the activity.
    #:
    #: :type: :obj:`ActivityAssets`, optional
    assets: typing.Optional[ActivityAssets] = marshaller.attrib(
        deserializer=ActivityAssets.deserialize, if_undefined=None
    )

    #: Secrets for Rich Presence joining and spectating.
    #:
    #: :type: :obj:`ActivitySecret`, optional
    secrets: typing.Optional[ActivitySecret] = marshaller.attrib(
        deserializer=ActivitySecret.deserialize, if_undefined=None
    )

    #: Whether this activity is an instanced game session.
    #:
    #: :type: :obj:`bool`, optional
    is_instance: typing.Optional[bool] = marshaller.attrib(raw_name="instance", deserializer=bool, if_undefined=None)

    #: Flags that describe what the activity includes.
    #:
    #: :type: :obj:`ActivityFlag`
    flags: ActivityFlag = marshaller.attrib(deserializer=ActivityFlag, if_undefined=None)


class PresenceStatus(enum.Enum):
    """
    The status of a member.
    """

    #: Online/green.
    ONLINE = "online"
    #: Idle/yellow.
    IDLE = "idle"
    #: Do not disturb/red.
    DND = "dnd"
    #: An alias for :attr:`DND`
    DO_NOT_DISTURB = DND
    #: Offline or invisible/grey.
    OFFLINE = "offline"


@marshaller.attrs(slots=True)
class ClientStatus(entities.HikariEntity, entities.Deserializable):
    """The client statuses for this member."""

    #: The status of the target user's desktop session.
    #:
    #: :type: :obj:`PresenceStatus`
    desktop: PresenceStatus = marshaller.attrib(
        deserializer=PresenceStatus, if_undefined=lambda: PresenceStatus.OFFLINE,
    )

    #: The status of the target user's mobile session.
    #:
    #: :type: :obj:`PresenceStatus`
    mobile: PresenceStatus = marshaller.attrib(deserializer=PresenceStatus, if_undefined=lambda: PresenceStatus.OFFLINE)

    #: The status of the target user's web session.
    #:
    #: :type: :obj:`PresenceStatus`
    web: PresenceStatus = marshaller.attrib(deserializer=PresenceStatus, if_undefined=lambda: PresenceStatus.OFFLINE)


@marshaller.attrs(slots=True)
class PresenceUser(users.User):
    """A user representation specifically used for presence updates.

    Warnings
    --------
    Every attribute except :attr:`id` may be received as :obj:`entities.UNSET`
    unless it is specifically being modified for this update.
    """

    #: This user's discriminator.
    #:
    #: :type: :obj:`typing.Union` [ :obj:`str`, `entities.UNSET` ]
    discriminator: typing.Union[str, entities.Unset] = marshaller.attrib(deserializer=str, if_undefined=entities.Unset)

    #: This user's username.
    #:
    #: :type: :obj:`typing.Union` [ :obj:`str`, `entities.UNSET` ]
    username: typing.Union[str, entities.Unset] = marshaller.attrib(deserializer=str, if_undefined=entities.Unset)

    #: This user's avatar hash, if set.
    #:
    #: :type: :obj:`typing.Union` [ :obj:`str`, `entities.UNSET` ], optional
    avatar_hash: typing.Union[None, str, entities.Unset] = marshaller.attrib(
        raw_name="avatar", deserializer=str, if_none=None, if_undefined=entities.Unset
    )

    #: Whether this user is a bot account.
    #:
    #: :type:  :obj:`typing.Union` [ :obj:`bool`, `entities.UNSET` ]
    is_bot: typing.Union[bool, entities.Unset] = marshaller.attrib(
        raw_name="bot", deserializer=bool, if_undefined=entities.Unset
    )

    #: Whether this user is a system account.
    #:
    #: :type:  :obj:`typing.Union` [ :obj:`bool`, `entities.UNSET` ]
    is_system: typing.Union[bool, entities.Unset] = marshaller.attrib(
        raw_name="system", deserializer=bool, if_undefined=entities.Unset,
    )


@marshaller.attrs(slots=True)
class GuildMemberPresence(entities.HikariEntity, entities.Deserializable):
    """Used to represent a guild member's presence."""

    #: The object of the user who this presence is for, only `id` is guaranteed
    #: for this partial object, with other attributes only being included when
    #: when they are being changed in an event.
    #:
    #: :type: :obj:`PresenceUser`
    user: PresenceUser = marshaller.attrib(deserializer=PresenceUser.deserialize)

    #: A sequence of the ids of the user's current roles in the guild this
    #: presence belongs to.
    #:
    #: :type: :obj:`typing.Sequence` [ :obj:`snowflakes.Snowflake` ]
    role_ids: typing.Sequence[snowflakes.Snowflake] = marshaller.attrib(
        raw_name="roles", deserializer=lambda roles: [snowflakes.Snowflake.deserialize(rid) for rid in roles],
    )

    #: The ID of the guild this presence belongs to.
    #:
    #: :type: :obj:`snowflakes.Snowflake`
    guild_id: snowflakes.Snowflake = marshaller.attrib(deserializer=snowflakes.Snowflake.deserialize)

    #: This user's current status being displayed by the client.
    #:
    #: :type: :obj:`PresenceStatus`
    visible_status: PresenceStatus = marshaller.attrib(raw_name="status", deserializer=PresenceStatus)

    #: An array of the user's activities, with the top one will being
    #: prioritised by the client.
    #:
    #: :type: :obj:`typing.Sequence` [ :obj:`PresenceActivity` ]
    activities: typing.Sequence[PresenceActivity] = marshaller.attrib(
        deserializer=lambda activities: [PresenceActivity.deserialize(a) for a in activities]
    )

    #: An object of the target user's client statuses.
    #:
    #: :type: :obj:`ClientStatus`
    client_status: ClientStatus = marshaller.attrib(deserializer=ClientStatus.deserialize)

    #: The datetime of when this member started "boosting" this guild.
    #: Will be ``None`` if they aren't boosting.
    #:
    #: :type: :obj:`datetime.datetime`, optional
    premium_since: typing.Optional[datetime.datetime] = marshaller.attrib(
        deserializer=dates.parse_iso_8601_ts, if_none=None, if_undefined=None,
    )

    #: This member's nickname, if set.
    #:
    #: :type: :obj:`str`, optional
    nick: typing.Optional[str] = marshaller.attrib(raw_name="nick", deserializer=str, if_undefined=None, if_none=None)


@marshaller.attrs(slots=True)
class GuildIntegration(snowflakes.UniqueEntity):
    ...


@marshaller.attrs(slots=True)
class GuildMemberBan(entities.HikariEntity):
    ...


@marshaller.attrs(slots=True)
class UnavailableGuild(snowflakes.UniqueEntity, entities.Deserializable):
    """An unavailable guild object, received during gateway events such as
    the "Ready".
    An unavailable guild cannot be interacted with, and most information may
    be outdated if that is the case.
    """

    @property
    def is_unavailable(self) -> bool:
        """
        Whether this guild is unavailable or not, should always be :obj:`True`.
        """
        return True


@marshaller.attrs(slots=True)
class PartialGuild(snowflakes.UniqueEntity, entities.Deserializable):
    """This is a base object for any partial guild objects returned by the api
    where we are only given limited information."""

    #: The name of the guild.
    #:
    #: :type: :obj:`str`
    name: str = marshaller.attrib(deserializer=str)

    #: The hash for the guild icon, if there is one.
    #:
    #: :type: :obj:`str`, optional
    icon_hash: typing.Optional[str] = marshaller.attrib(raw_name="icon", deserializer=str, if_none=None)

    #: A set of the features in this guild.
    #:
    #: :type: :obj:`typing.Set` [ :obj:`GuildFeature` ]
    features: typing.Set[GuildFeature] = marshaller.attrib(
        deserializer=lambda features: {transformations.try_cast(f, GuildFeature, f) for f in features},
    )

    def format_icon_url(self, fmt: typing.Optional[str] = None, size: int = 2048) -> typing.Optional[str]:
        """Generate the url for this guild's custom icon, if set.

        Parameters
        ----------
        fmt : :obj:`str`
            The format to use for this url, defaults to ``png`` or ``gif``.
            Supports ``png``, ``jpeg``, `jpg`, ``webp`` and ``gif`` (when
            animated).
        size : :obj:`int`
            The size to set for the url, defaults to ``2048``.
            Can be any power of two between 16 and 2048.

        Returns
        -------
        :obj:`str`, optional
            The string url.
        """
        if self.icon_hash:
            # pylint: disable=E1101:
            if fmt is None and self.icon_hash.startswith("a_"):
                fmt = "gif"
            elif fmt is None:
                fmt = "png"
            return cdn.generate_cdn_url("icons", str(self.id), self.icon_hash, fmt=fmt, size=size)
        return None

    @property
    def icon_url(self) -> typing.Optional[str]:
        """The url for this guild's icon, if set."""
        return self.format_icon_url()


@marshaller.attrs(slots=True)
class Guild(PartialGuild):
    """A representation of a guild on Discord.

    Note
    ----
    If a guild object is considered to be unavailable, then the state of any
    other fields other than the :attr:`is_unavailable` and :attr:`id` members
    outdated, or incorrect. If a guild is unavailable, then the contents of any
    other fields should be ignored.
    """

    #: The hash of the splash for the guild, if there is one.
    #:
    #: :type: :obj:`str`, optional
    splash_hash: typing.Optional[str] = marshaller.attrib(raw_name="splash", deserializer=str, if_none=None)

    #: The hash of the discovery splash for the guild, if there is one.
    #:
    #: :type: :obj:`str`, optional
    discovery_splash_hash: typing.Optional[str] = marshaller.attrib(
        raw_name="discovery_splash", deserializer=str, if_none=None
    )

    #: The ID of the owner of this guild.
    #:
    #: :type: :obj:`snowflakes.Snowflake`
    owner_id: snowflakes.Snowflake = marshaller.attrib(deserializer=snowflakes.Snowflake)

    #: The guild level permissions that apply to the bot user.
    #:
    #: :type: :obj:`permissions.Permission`
    my_permissions: permissions.Permission = marshaller.attrib(
        raw_name="permissions", deserializer=permissions.Permission
    )

    #: The voice region for the guild.
    #:
    #: :type: :obj:`str`
    region: str = marshaller.attrib(deserializer=str)

    #: The ID for the channel that AFK voice users get sent to, if set for the
    #: guild.
    #:
    #: :type: :obj:`snowflakes.Snowflake`, optional
    afk_channel_id: typing.Optional[snowflakes.Snowflake] = marshaller.attrib(
        deserializer=snowflakes.Snowflake, if_none=None
    )

    #: How long a voice user has to be AFK for before they are classed as being
    #: AFK and are moved to the AFK channel (:attr:`afk_channel_id`).
    #:
    #: :type: :obj:`datetime.timedelta`
    afk_timeout: datetime.timedelta = marshaller.attrib(
        deserializer=lambda seconds: datetime.timedelta(seconds=seconds)
    )

    # TODO: document when this is not specified.
    # FIXME: do we need a field for this, or can we infer it from the `embed_channel_id`?
    #: Defines if the guild embed is enabled or not. This information may not
    #: be present, in which case, it will be ``None`` instead.
    #:
    #: :type: :obj:`bool`, optional
    is_embed_enabled: typing.Optional[bool] = marshaller.attrib(
        raw_name="embed_enabled", if_undefined=False, deserializer=bool
    )

    #: The channel ID that the guild embed will generate an invite to, if
    #: enabled for this guild. If not enabled, it will be ``None``.
    #:
    #: :type: :obj:`snowflakes.Snowflake`, optional
    embed_channel_id: typing.Optional[snowflakes.Snowflake] = marshaller.attrib(
        deserializer=snowflakes.Snowflake, if_none=None, if_undefined=None
    )

    #: The verification level required for a user to participate in this guild.
    #:
    #: :type: :obj:`GuildVerificationLevel`
    verification_level: GuildVerificationLevel = marshaller.attrib(deserializer=GuildVerificationLevel)

    #: The default setting for message notifications in this guild.
    #:
    #: :type: :obj:`GuildMessageNotificationsLevel`
    default_message_notifications: GuildMessageNotificationsLevel = marshaller.attrib(
        deserializer=GuildMessageNotificationsLevel
    )

    #: The setting for the explicit content filter in this guild.
    #:
    #: :type: :obj:`GuildExplicitContentFilterLevel`
    explicit_content_filter: GuildExplicitContentFilterLevel = marshaller.attrib(
        deserializer=GuildExplicitContentFilterLevel
    )

    #: The roles in this guild, represented as a mapping of ID to role object.
    #:
    #: :type: :obj:`typing.Mapping` [ :obj:`snowflakes.Snowflake`, :obj:`GuildRole` ]
    roles: typing.Mapping[snowflakes.Snowflake, GuildRole] = marshaller.attrib(
        deserializer=lambda roles: {r.id: r for r in map(GuildRole.deserialize, roles)},
    )

    #: The emojis that this guild provides, represented as a mapping of ID to
    #: emoji object.
    #:
    #: :type: :obj:`typing.Mapping` [ :obj:`snowflakes.Snowflake`, :obj:`_emojis.GuildEmoji` ]
    emojis: typing.Mapping[snowflakes.Snowflake, _emojis.GuildEmoji] = marshaller.attrib(
        deserializer=lambda emojis: {e.id: e for e in map(_emojis.GuildEmoji.deserialize, emojis)},
    )

    #: The required MFA level for users wishing to participate in this guild.
    #:
    #: :type: :obj:`GuildMFALevel`
    mfa_level: GuildMFALevel = marshaller.attrib(deserializer=GuildMFALevel)

    #: The ID of the application that created this guild, if it was created by
    #: a bot. If not, this is always ``None``.
    #:
    #: :type: :obj:`snowflakes.Snowflake`, optional
    application_id: typing.Optional[snowflakes.Snowflake] = marshaller.attrib(
        deserializer=snowflakes.Snowflake, if_none=None
    )

    #: Whether the guild is unavailable or not.
    #:
    #: This information is only available if the guild was sent via a
    #: ``GUILD_CREATE`` event. If the guild is received from any other place,
    #: this will always be ``None``.
    #:
    #: An unavailable guild cannot be interacted with, and most information may
    #: be outdated if that is the case.
    is_unavailable: typing.Optional[bool] = marshaller.attrib(
        raw_name="unavailable", if_undefined=None, deserializer=bool
    )

    # TODO: document in which cases this information is not available.
    #: Describes whether the guild widget is enabled or not. If this information
    #: is not present, this will be ``None``.
    #:
    #: :type: :obj:`bool`, optional
    is_widget_enabled: typing.Optional[bool] = marshaller.attrib(
        raw_name="widget_enabled", if_undefined=None, deserializer=bool
    )

    #: The channel ID that the widget's generated invite will send the user to,
    #: if enabled. If this information is unavailable, this will be ``None``.
    #:
    #: :type: :obj:`snowflakes.Snowflake`, optional
    widget_channel_id: typing.Optional[snowflakes.Snowflake] = marshaller.attrib(
        if_undefined=None, if_none=None, deserializer=snowflakes.Snowflake
    )

    #: The ID of the system channel (where welcome messages and Nitro boost
    #: messages are sent), or ``None`` if it is not enabled.
    #:
    #: :type: :obj:`snowflakes.Snowflake`, optional
    system_channel_id: typing.Optional[snowflakes.Snowflake] = marshaller.attrib(
        if_none=None, deserializer=snowflakes.Snowflake
    )

    #: Flags for the guild system channel to describe which notification
    #: features are suppressed.
    #:
    #: :type: :obj:`GuildSystemChannelFlag`
    system_channel_flags: GuildSystemChannelFlag = marshaller.attrib(deserializer=GuildSystemChannelFlag)

    #: The ID of the channel where guilds with the :obj:`GuildFeature.PUBLIC`
    #: :attr:`features` display rules and guidelines. If the
    #: :obj:`GuildFeature.PUBLIC` feature is not defined, then this is ``None``.
    #:
    #: :type: :obj:`snowflakes.Snowflake`, optional
    rules_channel_id: typing.Optional[snowflakes.Snowflake] = marshaller.attrib(
        if_none=None, deserializer=snowflakes.Snowflake
    )

    #: The date and time that the bot user joined this guild.
    #:
    #: This information is only available if the guild was sent via a
    #: ``GUILD_CREATE`` event. If the guild is received from any other place,
    #: this will always be ``None``.
    #:
    #: :type: :obj`datetime.datetime`, optional
    joined_at: typing.Optional[datetime.datetime] = marshaller.attrib(deserializer=dates.parse_iso_8601_ts)

    #: Whether the guild is considered to be large or not.
    #:
    #: This information is only available if the guild was sent via a
    #: ``GUILD_CREATE`` event. If the guild is received from any other place,
    #: this will always be ``None``.
    #:
    #: The implications of a large guild are that presence information will
    #: not be sent about members who are offline or invisible.
    #:
    #: :type: :obj:`bool`, optional
    is_large: typing.Optional[bool] = marshaller.attrib(raw_name="large", if_undefined=None, deserializer=bool)

    #: The number of members in this guild.
    #:
    #: This information is only available if the guild was sent via a
    #: ``GUILD_CREATE`` event. If the guild is received from any other place,
    #: this will always be ``None``.
    #:
    #: :type: :obj:`int`, optional
    member_count: typing.Optional[int] = marshaller.attrib(if_undefined=None, deserializer=int)

    #: A mapping of ID to the corresponding guild members in this guild.
    #:
    #: This information is only available if the guild was sent via a
    #: ``GUILD_CREATE`` event. If the guild is received from any other place,
    #: this will always be ``None``.
    #:
    #: Additionally, any offline members may not be included here, especially
    #: if there are more members than the large threshold set for the gateway
    #: this object was send with.
    #:
    #: This information will only be updated if your shards have the correct
    #: intents set for any update events.
    #:
    #: Essentially, you should not trust the information here to be a full
    #: representation. If you need complete accurate information, you should
    #: query the members using the appropriate API call instead.
    #:
    #: :type: :obj:`typing.Mapping` [ :obj:`snowflakes.Snowflake`, :obj:`GuildMember` ], optional
    members: typing.Optional[typing.Mapping[snowflakes.Snowflake, GuildMember]] = marshaller.attrib(
        deserializer=lambda members: {m.user.id: m for m in map(GuildMember.deserialize, members)}, if_undefined=None,
    )

    #: A mapping of ID to the corresponding guild channels in this guild.
    #:
    #: This information is only available if the guild was sent via a
    #: ``GUILD_CREATE`` event. If the guild is received from any other place,
    #: this will always be ``None``.
    #:
    #: Additionally, any channels that you lack permissions to see will not be
    #: defined here.
    #:
    #: This information will only be updated if your shards have the correct
    #: intents set for any update events.
    #:
    #: To retrieve a list of channels in any other case, you should make an
    #: appropriate API call to retrieve this information.
    #:
    #: :type: :obj:`typing.Mapping` [ :obj:`snowflakes.Snowflake`, :obj:`GuildChannel` ], optional
    channels: typing.Optional[typing.Mapping[snowflakes.Snowflake, GuildChannel]] = marshaller.attrib(
        deserializer=lambda guild_channels: {c.id: c for c in map(parse_guild_channel, guild_channels)},
        if_undefined=None,
    )

    #: A mapping of member ID to the corresponding presence information for
    #: the given member, if available.
    #:
    #: This information is only available if the guild was sent via a
    #: ``GUILD_CREATE`` event. If the guild is received from any other place,
    #: this will always be ``None``.
    #:
    #: Additionally, any channels that you lack permissions to see will not be
    #: defined here.
    #:
    #: This information will only be updated if your shards have the correct
    #: intents set for any update events.
    #:
    #: To retrieve a list of presences in any other case, you should make an
    #: appropriate API call to retrieve this information.
    #:
    #: :type: :obj:`typing.Mapping` [ :obj:`snowflakes.Snowflake`, :obj:`GuildMemberPresence` ], optional
    presences: typing.Optional[typing.Mapping[snowflakes.Snowflake, GuildMemberPresence]] = marshaller.attrib(
        deserializer=lambda presences: {p.user.id: p for p in map(GuildMemberPresence.deserialize, presences)},
        if_undefined=None,
    )

    #: The maximum number of presences for the guild. If this is ``None``, then
    #: the default value is used (currently 5000).
    #:
    #: :type: :obj:`int`, optional
    max_presences: typing.Optional[int] = marshaller.attrib(if_none=None, if_undefined=None, deserializer=int)

    #: The maximum number of members allowed in this guild.
    #:
    #: This information may not be present, in which case, it will be ``None``.
    #:
    #: :type: :obj:`int`, optional
    max_members: typing.Optional[int] = marshaller.attrib(if_undefined=None, deserializer=int)

    #: The vanity URL code for the guild's vanity URL.
    #: This is only present if :obj:`GuildFeatures.VANITY_URL` is in the
    #: :attr:`features` for this guild. If not, this will always be ``None``.
    #:
    #: :type: :obj:`str`, optional
    vanity_url_code: typing.Optional[str] = marshaller.attrib(if_none=None, deserializer=str)

    #: The guild's description.
    #:
    #: This is only present if certain :attr:`features` are set in this guild.
    #: Otherwise, this will always be ``None``. For all other purposes, it is
    #: ``None``.
    #:
    #: :type: :obj:`str`, optional
    description: typing.Optional[str] = marshaller.attrib(if_none=None, deserializer=str)

    #: The hash for the guild's banner.
    #: This is only present if the guild has :obj:`GuildFeatures.BANNER` in the
    #: :attr:`features` for this guild. For all other purposes, it is ``None``.
    #:
    #: :type: :obj:`str`, optional
    banner_hash: typing.Optional[str] = marshaller.attrib(raw_name="banner", if_none=None, deserializer=str)

    #: The premium tier for this guild.
    #:
    #: :type: :obj:`GuildPremiumTier`
    premium_tier: GuildPremiumTier = marshaller.attrib(deserializer=GuildPremiumTier)

    #: The number of nitro boosts that the server currently has. This
    #: information may not be present, in which case, it will be ``None``.
    #:
    #: :type: :obj:`int`, optional
    premium_subscription_count: typing.Optional[int] = marshaller.attrib(if_undefined=None, deserializer=int)

    #: The preferred locale to use for this guild.
    #:
    #: This can only be change if :obj:`GuildFeatures.PUBLIC` is in the
    #: :attr:`features` for this guild and will otherwise default to ``en-US```.
    #:
    #: :type: :obj:`str`
    preferred_locale: str = marshaller.attrib(deserializer=str)

    #: The channel ID of the channel where admins and moderators receive notices
    #: from Discord.
    #:
    #: This is only present if :obj:`GuildFeatures.PUBLIC` is in the
    #: :attr:`features` for this guild. For all other purposes, it should be
    #: considered to be ``None``.
    #:
    #: :type: :obj:`snowflakes.Snowflake`, optional
    public_updates_channel_id: typing.Optional[snowflakes.Snowflake] = marshaller.attrib(
        if_none=None, deserializer=snowflakes.Snowflake
    )
