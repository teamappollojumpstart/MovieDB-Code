from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

# <membership/>
membership = Element( 'membership' )


for i in range(1,10):
	# <membership><users/>
	users = SubElement( membership, 'users' )
	# <membership><users><user/>
	SubElement( users, 'user', name='john' ).text = "cool"
	SubElement( users, 'user', name='charles' )
	SubElement( users, 'user', name='john' ).text = "coolk"
	SubElement( users, 'user', name='peter' )

users = SubElement( membership, 'users')

SubElement( users,'users',name="dakalti")

# <membership><groups/>
groups = SubElement( membership, 'groups' )

# <membership><groups><group/>
group = SubElement( groups, 'group', name='users' )

# <membership><groups><group><user/>
SubElement( group, 'user', name='john' )
SubElement( group, 'user', name='charles' )

# <membership><groups><group/>
group = SubElement( groups, 'group', name='administrators' )

# <membership><groups><group><user/>
SubElement( group, 'user', name='peter' )

output_file = open( 'membership.xml', 'w' )
output_file.write( '<?xml version="1.0"?>' )
output_file.write( ElementTree.tostring( membership ) )
output_file.close()


