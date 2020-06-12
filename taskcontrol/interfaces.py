
from dataclasses import dataclass
import abc


@dataclass(frozen=True)
class AuthenticationBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def init_db(self, path, name):
        raise NotImplementedError

    @abc.abstractmethod
    def init_tables(self, conn):
        raise NotImplementedError

    @abc.abstractmethod
    def init_superuser(self, conn):
        raise NotImplementedError

    @abc.abstractmethod
    def create_user(self):
        raise NotImplementedError

    @abc.abstractmethod
    def update_user(self):
        raise NotImplementedError

    @abc.abstractmethod
    def delete_user(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self):
        raise NotImplementedError

    @abc.abstractmethod
    def change_password(self):
        raise NotImplementedError

    @abc.abstractmethod
    def create_permissions(self, options):
        # user/role, action, permissions
        raise NotImplementedError

    @abc.abstractmethod
    def update_permissions(self, options):
        raise NotImplementedError

    @abc.abstractmethod
    def delete_permissions(self, options):
        raise NotImplementedError

    @abc.abstractmethod
    def get_permissions(self, options):
        raise NotImplementedError

    @abc.abstractmethod
    def create_role(self, options):
        # role
        raise NotImplementedError

    @abc.abstractmethod
    def update_role(self, options):
        raise NotImplementedError

    @abc.abstractmethod
    def delete_role(self, options):
        raise NotImplementedError

    @abc.abstractmethod
    def get_role(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_permissions(self, user):
        # user, role, action, permissions
        raise NotImplementedError

    @abc.abstractmethod
    def is_authenticated(self):
        # true/false
        raise NotImplementedError


@dataclass(frozen=True)
class SocketsBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, **kwargs):
        raise NotImplementedError
        
    @abc.abstractmethod
    def socket_create(self):
        raise NotImplementedError

    @abc.abstractmethod
    def socket_delete(self):
        raise NotImplementedError

    @abc.abstractmethod
    def socket_listen(self):
        raise NotImplementedError

    @abc.abstractmethod
    def socket_message(self):
        raise NotImplementedError

    @abc.abstractmethod
    def socket_receive(self):
        raise NotImplementedError


@dataclass(frozen=True)
class HooksBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def hook_state(self):
        raise NotImplementedError

    @abc.abstractmethod
    def service_run(self):
        raise NotImplementedError

    @abc.abstractmethod
    def service_stop(self):
        raise NotImplementedError

    @abc.abstractmethod
    def register_hook(self):
        raise NotImplementedError

    @abc.abstractmethod
    def register_receiver(self):
        raise NotImplementedError

    @abc.abstractmethod
    def send(self):
        raise NotImplementedError

    @abc.abstractmethod
    def receive(self):
        raise NotImplementedError


@dataclass(frozen=True)
class SQLBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, conn, options):
        raise NotImplementedError
    
    @abc.abstractmethod
    def find(self, conn, options):
        raise NotImplementedError
    
    @abc.abstractmethod
    def update(self, conn, options):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, conn, options):
        raise NotImplementedError


@dataclass(frozen=True)
class LogBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, config):
        raise NotImplementedError

    @abc.abstractmethod
    def log(self, logger_options):
        raise NotImplementedError


@dataclass(frozen=True)
class PluginBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def plugin_create(self, name, task_instance):
        raise NotImplementedError


@dataclass(frozen=True)
class TimeBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def time(self, name, task_instance):
        raise NotImplementedError

