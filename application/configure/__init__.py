# -*-coding: utf-8-*-
# time: 2015/09/23 08:33
# author: liukaizeng

import os

from . import development
from . import production
from . import testing

__all__ = ['setting']

current_env = os.environ.get('APPLICATION_ENV') or "development"

setting = {
    "development": development,
    "production": production,
    "testing": testing
}.get(current_env, "development")

print ("current_env = %s" % current_env)



