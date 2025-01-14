from logging import getLogger

from sqlalchemy.exc import NoResultFound

from membership.membership import get_membership_summary
from membership.models import Member
from multiaccessy.accessy import ACCESSY_LABACCESS_GROUP, ACCESSY_SPECIAL_LABACCESS_GROUP, \
    AccessyError, accessy_session
from service.db import db_session


logger = getLogger("makeradmin")


class AccessyInvitePreconditionFailed(AccessyError):
    pass


def ensure_accessy_labaccess(member_id):
    """ If all preconditions are met, send an accessy invite (including auto add to labaccess gropup). Returns human
    readable message of what happened. """
    try:
        member = db_session.query(Member).get(member_id)
    except NoResultFound as e:
        raise AccessyInvitePreconditionFailed("hittade inte medlem") from e

    if not member.phone:
        raise AccessyInvitePreconditionFailed("inget telefonnummer")

    if not member.labaccess_agreement_at:
        raise AccessyInvitePreconditionFailed("inget labbavtal")

    summary = get_membership_summary(member_id)
    if not summary.labaccess_active and not summary.special_labaccess_active:
        raise AccessyInvitePreconditionFailed("ingen aktiv labaccess")

    groups = []
    if summary.labaccess_active:
        groups.append(ACCESSY_LABACCESS_GROUP)
    if summary.special_labaccess_active:
        groups.append(ACCESSY_SPECIAL_LABACCESS_GROUP)

    try:
        if accessy_session.is_in_org(member.phone):
            for group in groups:
                logger.info(f"accessy, addding to group: {member=} {group=}")
                accessy_session.add_to_group(member.phone, group)
        else:
            logger.info(f"accessy, sending invite: {member=} {groups=}")
            accessy_session.invite_phone_to_org_and_groups([member.phone], groups)
    except Exception as e:
        raise AccessyError("failed to interact with accessy") from e
