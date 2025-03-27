"""HELLOMED website REST API."""

from server.api.chat import chat_test
from server.api.check_in import post_check_in
from server.api.check_in import get_check_ins
from server.api.check_in import get_check_in
from server.api.auth import get_admin
from server.api.auth import get_admins
from server.api.auth import post_admin
from server.api.auth import delete_admin
from server.api.locations import get_locations_info
from server.api.locations import put_locations_info
from server.api.images import presigned_url_for_post
from server.api.images import presigned_url_for_get