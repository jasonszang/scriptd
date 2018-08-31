# -*- coding: UTF-8 -*-
"""Custom exceptions used by scriptd"""


class ScriptdError(RuntimeError):
    pass


class AuthenticationError(ScriptdError):
    pass


class NoSuchScriptError(ScriptdError):
    pass


class NotPermittedError(ScriptdError):
    pass
