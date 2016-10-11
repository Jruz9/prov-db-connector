from abc import ABC, abstractmethod
from collections import namedtuple
from enum import Enum

import logging
log = logging.getLogger(__name__).addHandler(logging.NullHandler())


class AdapterException(Exception):
    pass


class InvalidOptionsException(AdapterException):
    pass


class AuthException(AdapterException):
    pass


class DatabaseException(AdapterException):
    pass


class CreateRecordException(DatabaseException):
    pass


class CreateRelationException(DatabaseException):
    pass


class NotFoundException(DatabaseException):
    pass

class MergeException(DatabaseException):
    pass

METADATA_PARENT_ID = "parent_id"
METADATA_KEY_PROV_TYPE = "prov_type"
METADATA_KEY_IDENTIFIER = "identifier"
METADATA_KEY_NAMESPACES = "namespaces"
METADATA_KEY_TYPE_MAP = "type_map"

#Return types for adapter classes
DbDocument = namedtuple("DbDocument", "document, bundles")
DbBundle = namedtuple("DbBundle",  "records, bundle_record")

DbRecord = namedtuple("DbRecord", "attributes, metadata")
DbRelation = namedtuple("DbRelation", "attributes, metadata")

class MergeBehaviour(Enum):
    NO_MERGE = 0
    SOFT = 1
    OVERRIDE = 2

class BaseAdapter(ABC):

    """
    :type MergeBehaviour
    """
    merge_behaviour = MergeBehaviour.NO_MERGE

    """
    Interface class for a prov database adapter
    """
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def connect(self, authentication_info):
        """
        Establish the database connection / login into the database
        :param authentication_info: a custom dict with credentials
        :return: bool
        """
        pass


    @abstractmethod
    def save_record(self, attributes, metadata):
        """
        Creates a database node
        :param attributes: Attributes as dict for the record. Be careful you have to encode the dict
        :param metadata: Metadata as dict for the record. Be careful you have to encode the dict but you can be sure that all meta keys are always there
        :return: Record id as string
        """
        pass

    @abstractmethod
    def save_relation(self,  from_node,  to_node, attributes, metadata):
        """
        Create a relation between 2 nodes
        :param from_node: The identifier
        :param to_node: The identifier for the destionation node
        :param attributes:  Attributes as dict for the record. Be careful you have to encode the dict
        :param metadata: Metadata as dict for the record. Be careful you have to encode the dict but you can be sure that all meta keys are always there
        :return:
        """
        pass


    @abstractmethod
    def get_records_by_filter(self, properties_dict=dict(), metadata_dict=dict()):

        pass

    @abstractmethod
    def get_records_tail(self,properties_dict=dict(), metadata_dict=dict(), depth=None):
        pass

    @abstractmethod
    def get_record(self, record_id):
        """
        Return a single record
        :param record_id:
        :return: DbRecord
        """
        pass

    @abstractmethod
    def get_relation(self, relation_id):
        """
        Returns a single relation
        :param relation_id:
        :return:DbRelation
        """
        pass

    @abstractmethod
    def delete_records_by_filter(self, properties_dict, metadata_dict):
        pass

    @abstractmethod
    def delete_record(self, record_id):
        """
        Delete a single record
        :param record_id:
        :return:bool
        :raise NotFoundException
        """
        pass

    @abstractmethod
    def delete_relation(self, relation_id):
        """
        Delete a single relation
        :param relation_id:
        :return:bool
        :raise NotFoundException
        """
        pass

    def setMergeBehaviour(self, new_behaviour):
        if type(new_behaviour) is MergeBehaviour:
            self.merge_behaviour = new_behaviour
        else:
            raise InvalidOptionsException("new_behaviour must be typeof {} but was {}".format(type(MergeBehaviour), type(new_behaviour)))