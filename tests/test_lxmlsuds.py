# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify it under
# the terms of the (LGPL) GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Library Lesser General Public License
# for more details at ( http://www.gnu.org/licenses/lgpl.html ).
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# written by: Jurko Gospodnetić ( jurko.gospodnetic@pke.hr )

"""
General suds Python library unit tests.

Implemented using the 'pytest' testing framework.

This whole module should be refactored into more specialized modules as more
tests get added to it and it acquires more structure.

"""
import sys

import testutils
if __name__ == "__main__":
    testutils.run_using_pytest(globals())

import suds

import pytest
from six import itervalues, next, text_type, binary_type
from six.moves import http_client

import xml.sax

def test_converting_client_to_string_must_not_raise_an_exception():
    client = testutils.lxmlclient_from_wsdl(suds.byte_str(
        "<?xml version='1.0' encoding='UTF-8'?><root/>"))
    str(client)

def test_wrapped_sequence_output():
    client = testutils.lxmlclient_from_wsdl(testutils.wsdl("""\
      <xsd:element name="Wrapper">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="result1" type="xsd:string"/>
            <xsd:element name="result2" type="xsd:string"/>
            <xsd:element name="result3" type="xsd:string"/>
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>""", output="Wrapper"))

    response = client.service.f(__inject=dict(reply=suds.byte_str("""\
<?xml version="1.0"?>
<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
  <Body>
    <Wrapper xmlns="my-namespace">
        <result1>Uno</result1>
        <result2>Due</result2>
        <result3>Tre</result3>
    </Wrapper>
  </Body>
</Envelope>""")))

    # Check response content.
    assert len(response) == 3
    assert response.result1 == "Uno"
    assert response.result2 == "Due"
    assert response.result3 == "Tre"
    assert_lxml_string_value(response.result1)
    assert_lxml_string_value(response.result2)
    assert_lxml_string_value(response.result3)
    
    client = testutils.lxmlclient_from_wsdl(testutils.wsdl("""\
      <xsd:element name="Wrapper">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="result1" type="xsd:string"/>
            <xsd:element name="result2" type="xsd:string"/>
            <xsd:element name="result3" type="xsd:string"/>
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>""", output="Wrapper"))

    response = client.service.f(__inject=dict(reply=suds.byte_str("""\
<?xml version="1.0"?>
<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
  <Body>
    <Wrapper xmlns="my-namespace">
    </Wrapper>
  </Body>
</Envelope>""")))

    # Check response content.
    assert len(response) == 3
    assert response.result1 is None
    assert response.result2 is None
    assert response.result3 is None
        
#Todo fix
@pytest.mark.xfail
def test_enum():
    client = testutils.lxmlclient_from_wsdl(testutils.wsdl("""\
      <xsd:element name="Wrapper">
        <xsd:element name="Size">
          <xsd:simpleType name="DataSize">
            <xsd:restriction base="xsd:string">
              <xsd:enumeration value="1" />
              <xsd:enumeration value="2"/>
              <xsd:enumeration value="3"/>
            </xsd:restriction>
          </xsd:simpleType>
        </xsd:element>
      </xsd:element>""", output="Wrapper"))

    response = client.service.f(__inject=dict(reply=suds.byte_str("""\
<?xml version="1.0"?>
<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
  <Body>
    <Wrapper xmlns="my-namespace">
        <DataSize>1</DataSize>
    </Wrapper>
  </Body>
</Envelope>""")))

    # Check response content.
    assert len(response) == 1
    assert response.size == 1

def test_array():
    client = testutils.lxmlclient_from_wsdl(testutils.wsdl("""\
      <xsd:element name="Wrapper">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="value" type="xsd:string" maxOccurs="unbounded"/>
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>""", output="Wrapper"))

    response = client.service.f(__inject=dict(reply=suds.byte_str("""\
<?xml version="1.0"?>
<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
  <Body>
    <Wrapper xmlns="my-namespace">
        <value>9</value>
        <value>18</value>
        <value>5342</value>
    </Wrapper>
  </Body>
</Envelope>""")))

    # Check response content.
    assert len(response) == 1
    assert isinstance(response.value, list)
    assert len(response.value) == 3
    assert response.value[0] == "9"
    assert response.value[1] == "18"
    assert response.value[2] == "5342"
    assert_lxml_string_value(response.value[0])
    assert_lxml_string_value(response.value[1])
    assert_lxml_string_value(response.value[2])
    
    
    client = testutils.lxmlclient_from_wsdl(testutils.wsdl("""\
      <xsd:element name="Wrapper">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="value" type="xsd:int" maxOccurs="unbounded"/>
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>""", output="Wrapper"))

    response = client.service.f(__inject=dict(reply=suds.byte_str("""\
<?xml version="1.0"?>
<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
  <Body>
    <Wrapper xmlns="my-namespace">
        <value>19</value>
    </Wrapper>
  </Body>
</Envelope>""")))

    # Check response content.
    assert len(response) == 1
    assert isinstance(response.value, list)
    assert len(response.value) == 1
    assert response.value[0] == 19
    assert isinstance(response.value[0], int)
    
    client = testutils.lxmlclient_from_wsdl(testutils.wsdl("""\
      <xsd:element name="Wrapper">
        <xsd:complexType>
          <xsd:sequence>
            <xsd:element name="value" type="xsd:string" nillable="true" maxOccurs="unbounded"/>
          </xsd:sequence>
        </xsd:complexType>
      </xsd:element>""", output="Wrapper"))

    response = client.service.f(__inject=dict(reply=suds.byte_str("""\
<?xml version="1.0"?>
<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
  <Body>
    <Wrapper xmlns="my-namespace">
        <value />
    </Wrapper>
  </Body>
</Envelope>""")))

    # Check response content.
    assert len(response) == 1
    assert isinstance(response.value, list)
    assert len(response.value) == 0
    
def assert_lxml_string_value(test_obj):
    if sys.version_info >= (3,):
        assert isinstance(test_obj, text_type)
    else: #lxml uses ascii by default in python 2
        assert isinstance(test_obj, binary_type)
