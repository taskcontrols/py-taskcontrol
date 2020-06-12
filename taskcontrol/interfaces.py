
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

    # Testing passing functions to get closure with self-implementation
    def auth_closure(
            self,
            get_dbconn=None,
            set_dbconn=None,
            db_execute=None,
            db_close=None,
            get_pconn=None,
            set_pconn=None,
            p_dump=None,
            p_close=None
        ):
        db_connections = {}
        pickle_connections = {}

        if get_dbconn != None and type(get_dbconn) == callable:
            raise TypeError("AuthenticationBase: get_dbconn not set error")

        if set_dbconn != None and type(set_dbconn) == callable:
            raise TypeError("AuthenticationBase: set_dbconn not set error")

        if db_execute != None and type(db_execute) == callable:
            raise TypeError("AuthenticationBase: db_execute not set error")

        if db_close != None and type(db_close) == callable:
            raise TypeError("AuthenticationBase: db_close not set error")

        if get_pconn != None and type(get_pconn) == callable:
            raise TypeError("AuthenticationBase: get_pconn not set error")

        if set_pconn != None and type(set_pconn) == callable:
            raise TypeError("AuthenticationBase: set_pconn not set error")

        if p_dump != None and type(p_dump) == callable:
            raise TypeError("AuthenticationBase: p_dump not set error")

        if p_close != None and type(p_close) == callable:
            raise TypeError("AuthenticationBase: p_close not set error")

        return (
            get_dbconn, set_dbconn, db_execute, db_close,
            get_pconn, set_pconn, p_dump, p_close
        )

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
class LoggerBase(metaclass=abc.ABCMeta):

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

