#!/usr/bin/env python3

# copyright 2020 Bill Dry
# This module provides a user object that is logged in/out & tracked by flask_login

# Import UserMixin to provide common user states
from flask_login import UserMixin

class user(UserMixin):
    def __init__(self, user_id):
        self.id = user_id