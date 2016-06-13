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

import testutils
if __name__ == "__main__":
    testutils.run_using_pytest(globals())

import suds

import pytest
from six import itervalues, next, u, text_type
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
    #assert _isOutputWrapped(client, "f")

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
    assert isinstance(response.result1, text_type)
    assert isinstance(response.result2, text_type)
    assert isinstance(response.result3, text_type)
    