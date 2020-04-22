import logging

logger = logging.getLogger(__name__)


def first_match_after_anchor(string, anchor, regex, disallowed_in_between=None):
    if disallowed_in_between is None:
        disallowed_in_between = []

    anchor_match = anchor.search(string)

    if anchor_match is None:
        return None

    remaining_string = string[anchor_match.end():]

    if anchor.search(remaining_string) is not None:
        logger.warning(f"Multiple anchors found")

    final_match = regex.search(remaining_string)
    if final_match is None:
        return None

    in_between_text = string[anchor_match.end():final_match.start()]

    for disallowed_reg in disallowed_in_between:
        match = disallowed_reg.search(in_between_text)
        if match is not None:
            logger.warning(f"Found disallowed in between regex in between matching '{match.group()}'")

            return None

    return final_match
