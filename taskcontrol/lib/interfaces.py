
from dataclasses import dataclass
import abc


@dataclass(frozen=True)
class ObjectModificationInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, config):
        raise NotImplementedError

    @abc.abstractmethod
    def fetch(self, config):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, config):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, config):
        raise NotImplementedError


@dataclass(frozen=True)
class FileReaderInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def exists(self, file_path):
        raise NotImplementedError

    @abc.abstractmethod
    def is_file(self, file_path):
        raise NotImplementedError

    @abc.abstractmethod
    def file_read(self, obj, way, index):
        raise NotImplementedError

    @abc.abstractmethod
    def file_write(self, obj, items, way):
        raise NotImplementedError

    @abc.abstractmethod
    def file_append(self, obj, items, way):
        raise NotImplementedError

    @abc.abstractmethod
    def row_insert(self, name, item, row):
        raise NotImplementedError

    @abc.abstractmethod
    def row_append(self, name, item):
        raise NotImplementedError

    @abc.abstractmethod
    def row_update(self, name, item, row):
        raise NotImplementedError

    @abc.abstractmethod
    def row_delete(self, name, row):
        raise NotImplementedError

    @abc.abstractmethod
    def row_search(self, name, params):
        raise NotImplementedError


@dataclass(frozen=True)
class CSVReaderInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def row_insert(self, name, head, params):
        raise NotImplementedError

    @abc.abstractmethod
    def row_fetch(self, name, head, params):
        raise NotImplementedError

    @abc.abstractmethod
    def row_update(self, name, params):
        raise NotImplementedError

    @abc.abstractmethod
    def row_delete(self, name, head):
        raise NotImplementedError


@dataclass(frozen=True)
class PicklesInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def row_insert(self, config):
        raise NotImplementedError

    @abc.abstractmethod
    def row_append(self, config):
        raise NotImplementedError

    @abc.abstractmethod
    def row_update(self, config):
        raise NotImplementedError

    @abc.abstractmethod
    def row_delete(self, config):
        raise NotImplementedError

    @abc.abstractmethod
    def search(self, config):
        raise NotImplementedError


@dataclass(frozen=True)
class AuthsInterface(metaclass=abc.ABCMeta):

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
class PubSubsInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def register_publisher(self):
        raise NotImplementedError

    @abc.abstractmethod
    def register_subscriber(self):
        raise NotImplementedError

    @abc.abstractmethod
    def register_event(self):
        raise NotImplementedError

    # @abc.abstractmethod
    # def __process(self):
    #     raise NotImplementedError

    @abc.abstractmethod
    def send(self, event_object):
        raise NotImplementedError

    @abc.abstractmethod
    def receive(self, event_object):
        raise NotImplementedError


@dataclass(frozen=True)
class QueuesInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def new(self, config):
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, name, item, index=0, nowait=True):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, name, index=0, nowait=True):
        raise NotImplementedError


@dataclass(frozen=True)
class EventsInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def event_register(self, event_object):
        raise NotImplementedError

    @abc.abstractmethod
    def event_unregister(self, event_name):
        raise NotImplementedError

    @abc.abstractmethod
    def listener_register(self, listener_object):
        raise NotImplementedError

    @abc.abstractmethod
    def on(self, event_name, name, handler):
        raise NotImplementedError

    @abc.abstractmethod
    def listener_unregister(self, listener_object):
        raise NotImplementedError

    @abc.abstractmethod
    def get_state(self, event_name):
        raise NotImplementedError

    @abc.abstractmethod
    def set_state(self, event_name, state):
        raise NotImplementedError

    @abc.abstractmethod
    def listen(self, event_name):
        raise NotImplementedError

    @abc.abstractmethod
    def stop(self, event_name):
        raise NotImplementedError

    @abc.abstractmethod
    def send(self, message_object):
        raise NotImplementedError

    @abc.abstractmethod
    def emit(self, event_name, message):
        raise NotImplementedError


@dataclass(frozen=True)
class SocketsInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def socket_create(self):
        raise NotImplementedError

    @abc.abstractmethod
    def socket_accept(self):
        raise NotImplementedError

    @abc.abstractmethod
    def socket_listen(self):
        raise NotImplementedError

    @abc.abstractmethod
    def socket_close(self):
        raise NotImplementedError

    @abc.abstractmethod
    def send(self):
        raise NotImplementedError

    @abc.abstractmethod
    def receive(self):
        raise NotImplementedError


@dataclass(frozen=True)
class HooksInterface(metaclass=abc.ABCMeta):

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
class SQLInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def row_insert(self, conn, options):
        raise NotImplementedError

    @abc.abstractmethod
    def row_find(self, conn, options):
        raise NotImplementedError

    @abc.abstractmethod
    def row_update(self, conn, options):
        raise NotImplementedError

    @abc.abstractmethod
    def row_delete(self, conn, options):
        raise NotImplementedError

    @abc.abstractmethod
    def db_create(self, conn, options):
        pass

    @abc.abstractmethod
    def db_alter(self, conn, options):
        pass

    @abc.abstractmethod
    def db_delete(self, conn, options):
        pass

    @abc.abstractmethod
    def db_find(self, conn, options):
        pass

    @abc.abstractmethod
    def table_create(self, conn, options):
        pass

    @abc.abstractmethod
    def table_alter(self, conn, options):
        pass

    @abc.abstractmethod
    def table_delete(self, conn, options):
        pass

    @abc.abstractmethod
    def table_find(self, conn, options):
        pass


@dataclass(frozen=True)
class LogsInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def logger_create(self, logger_options):
        raise NotImplementedError

    @abc.abstractmethod
    def log(self, logger_options):
        raise NotImplementedError


@dataclass(frozen=True)
class PluginsInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def plugin_create(self, name, task_instance):
        raise NotImplementedError


@dataclass(frozen=True)
class TimeInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def timer_create(self, config):
        raise NotImplementedError

    @abc.abstractmethod
    def elapsed_time(self, name):
        raise NotImplementedError

    @abc.abstractmethod
    def curent_elapsed_time(self, name):
        raise NotImplementedError

    @abc.abstractmethod
    def reset(self, name):
        raise NotImplementedError

    @abc.abstractmethod
    def start(self, name):
        raise NotImplementedError

    @abc.abstractmethod
    def stop(self, name):
        raise NotImplementedError

    @abc.abstractmethod
    def time(self, name, task_instance):
        raise NotImplementedError


@dataclass(frozen=True)
class CommandsInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def exists(self, options):
        raise NotImplementedError

    @abc.abstractmethod
    def path(self, command):
        raise NotImplementedError

    @abc.abstractmethod
    def execute(self, config):
        raise NotImplementedError


@dataclass(frozen=True)
class SSHInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def connect(self, options):
        raise NotImplementedError

    @abc.abstractmethod
    def execute(self, options):
        raise NotImplementedError
