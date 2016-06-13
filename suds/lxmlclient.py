import logging
import time

from lxml import objectify
from lxml.etree import XMLParser
from suds import WebFault, TypeNotFound
from suds.client import Client as sudsClient
from suds.plugin import MessagePlugin
from suds.xsd.query import TypeQuery, ElementQuery

parser = XMLParser(remove_blank_text=True, huge_tree=True)
parser.set_element_class_lookup(objectify.ObjectifyElementClassLookup())
objectify.set_default_parser(parser)

logger = logging.getLogger('suds.client.lxml')
logging.getLogger('suds.client').setLevel(logging.CRITICAL)  # Don't show suds messages!


class SoapObject:
    def __init__(self, name):
        self.__name__ = name
    
    def __len__(self):
        return len(self.__dict__.items()) - 1 # ignore the __name__ property
    
    def __repr__(self):
        return self.__str__()
        
    def __str__(self):
        return self.__name__

    def as_dict(self):
        return {k: v for k, v in self.__dict__.items() if '__name__' not in k}


# This is a wrapper for all our soap calls
def lxml_wrapper(f, schema):
    def bodypart_types(method, schema, input=True):
        """
        This returns the types of a soap body.
        This is basically copied from the suds source code (suds.bindings.binding)
        """
        result = []
        if input:
            parts = method.soap.input.body.parts
        else:
            parts = method.soap.output.body.parts
        for p in parts:
            if p.element is not None:
                query = ElementQuery(p.element)
            else:
                query = TypeQuery(p.type)
            pt = query.execute(schema)
            if pt is None:
                raise TypeNotFound(query.ref)
            if p.type is not None:
                pt = TypeNotFound(p.name, pt)
            if input:
                if pt.name is None:
                    result.append((p.name, pt))
                else:
                    result.append((pt.name, pt))
            else:
                result.append(pt)
        return result

    def get_return_types(method, schema):
        """
        This gives us a list of return types.
        This is basically copied from the suds source code (suds.bindings.binding)
        """
        result = []
        for rt in bodypart_types(method, schema, input=False):
            result.append(rt)
        return result

    def lxml_to_python(obj, resolved):
        """
        Convert lxml object into a SoapObject
        """
        python_obj = SoapObject(resolved.name)
        # The component of the tuple in the dict resolved_children is the child itself and the 2nd
        # is the resolved form of the child. We need this because the unresolved child contains
        # some info that the resolved child does not, like the proper unbounded info.
        resolved_children = {c[0].name: (c[0], c[0].resolve(nobuiltin=True)) for c in resolved.children()}

        for child in obj.iterchildren():
            i = child.tag.find('}')
            if i >= 0:
                key = child.tag[i+1:]
            else:
                key = child.tag
            resolved_child = resolved_children[key][1]
            # Enums aren't basic types technically and thus have children, but they effectively are
            if resolved_child.enum() or len(resolved_child.children()) == 0:
                cval = child.pyval
                if resolved_children[key][0].type is not None and resolved_children[key][0].type[0] == 'string':
                    # lxml's type inference fails sometimes with stuff like 0 being interpreted as an int
                    cval = child.text
            else:
                cval = lxml_to_python(child, resolved_child)
            v = getattr(python_obj, key, None)
            if v is not None:
                if isinstance(v, list):
                    v.append(cval)
                else:
                    setattr(python_obj, key, [v, cval])
                continue
            # The resolving deletes the unbounded info, so use the original info
            if resolved_children[key][0].multi_occurrence():
                if cval is None:
                    setattr(python_obj, key, [])
                else:
                    setattr(python_obj, key, [cval, ])
            else:
                setattr(python_obj, key, cval)

        for child, resolved_child in resolved_children.values():
            if getattr(python_obj, child.name, None) is None:
                setattr(python_obj, child.name, None)

        return python_obj

    def call_server(*args, **kwargs):
        """
        Call the server and return the response, the start time, and the end time
        """
        server_start_time = time.clock()
        retxml = f(*args, **kwargs)
        server_response_time = time.clock() - server_start_time
        return retxml, server_start_time, server_response_time

    def lxml_deserialize(retxml):
        """
        Deserialize using lxml objectify
        """
        deserialize_start_time = time.clock()
        lxml_obj = objectify.fromstring(retxml)
        lxml_deserialize_time = time.clock() - deserialize_start_time
        return lxml_obj, lxml_deserialize_time

    def resolve_return_type():
        """
        Use suds to resolve return types
        """
        method_type = f.method
        rtypes = get_return_types(method_type, schema)

        # Resolve the type.
        # We assume there is 1 return type and that it is not nothing
        resolved = rtypes[0].resolve(nobuiltin=True)
        return resolved

    def to_python(lxml_obj):
        to_python_start_time = time.clock()
        return_obj = lxml_obj.Body.getchildren()[0]

        resolved = resolve_return_type()

        response = lxml_to_python(return_obj, resolved)
        to_python_time = time.clock() - to_python_start_time
        return response, to_python_time

    def call(*args, **kwargs):
        """
        This is a decorator method to use lxml to parse the soap response.
        """
        retxml, server_start_time, server_response_time = call_server(*args, **kwargs)

        lxml_obj, lxml_deserialize_time = lxml_deserialize(retxml)
        response, to_python_time = to_python(lxml_obj)

        total_time = time.clock() - server_start_time
        logger.info(
            ("The request took {0:.4f} seconds. "
             "({1:.4f} serialize/server, "
             "{2:.4f} lxml deserialize, "
             "{3:.4f}s to_python)").format(total_time,
                                           server_response_time,
                                           lxml_deserialize_time,
                                           to_python_time))
        return response

    return call


class Client(object):
    def __set_methods__(self, client):
        self.service = client.service
        if len(client.service._ServiceSelector__services) > 0:
            self.suds_methods = client.service._ServiceSelector__services[0].ports[0].methods.keys()
            for method in self.suds_methods:
                suds_method = getattr(client.service, method)
                setattr(self.service, method, lxml_wrapper(suds_method, client.wsdl.schema))

    def __set_soap_types__(self, client):
        setattr(self, 'factory', client.factory)

    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.suds_client = sudsClient(self.url, retxml=True, *args, **kwargs) #maybe clean for retxml in kwargs

        self.__set_methods__(self.suds_client)
        self.__set_soap_types__(self.suds_client)
    
    def __str__(self):
        return str(self.suds_client)