#MenuTitle: Insert Glyph to Background
# encoding: utf-8

# by Tim Ahrens
# http://justanotherfoundry.com
# https://github.com/justanotherfoundry/glyphsapp-scripts

"""
1. Enter a glyph name.
2. Press the left align or right align button.
3. This script will clear the mask, then insert the specified glyph into the mask.

- With right align selected, the contours will be pasted as if the advance widths were aligned.
- The keyboard shortcuts for left and right aligned are Enter and Esc.
- It is sufficient to enter the beginning of the glyph name, e.g. "deg" for "degree".

"""

from GlyphsApp import *
from vanilla import *

LEFT = '<'
RIGHT = '>'

glyphs = Glyphs.font.glyphs

class GlyphnameDialog( object):

	def __init__( self, selected_glyphs ):
		self.selected_glyphs = selected_glyphs
		x = 10
		y = 10
		height = 20
		button_width = 30
		glyphname_width = 180
		gap = 6
		self.w = Window( ( x + button_width + gap + glyphname_width + gap + button_width + x, y + height + y ), "insert glyph" )
		self.w.center()
		self.w.glyphname = EditText( ( x, y, glyphname_width, height ), '')
		x += glyphname_width + gap
		self.w.alignleft = Button( ( x, y, button_width, height ), LEFT, callback = self.buttonCallback )
		x += button_width + gap
		self.w.alignright = Button( ( x, y, button_width, height ), RIGHT, callback = self.buttonCallback )
		self.w.setDefaultButton( self.w.alignleft )
		self.w.alignright.bind( "\x1b", [] )
		self.w.open()

	def buttonCallback( self, sender ):
		title = sender.getTitle()
		glyphname = self.w.glyphname.get()
		if not glyphname:
			self.w.close()
			return
		if len( glyphname ) == 1:
			pass
			# todo: get Unicode value and choose glyph accordingly
		other_glyph = glyphs[ glyphname ]
		if not other_glyph:
			for glyph in glyphs:
				if glyph.name.startswith( glyphname ):
					other_glyph = glyph
					print 'Using', glyph.name
					break
			else:
				print 'No matching glyph found.'
				self.w.close()
				return
		for glyph in self.selected_glyphs:
			glyph.beginUndo()
			for layer in glyph.layers:
				# clear mask
				for i in range( len ( layer.background.paths ) ):
					del layer.background.paths[0]
				# inert paths
				for other_layer in other_glyph.layers:
					if other_layer.associatedMasterId == layer.associatedMasterId:
						for path in other_layer.copyDecomposedLayer().paths:
							if title == RIGHT:
								shift = layer.width - other_layer.width # might not be used
								for node in path.nodes:
									node.x = node.x + shift
							layer.background.paths.append( path )
						break
			glyph.endUndo()
		self.w.close()

selected_glyphs = set( [ layer.parent for layer in Glyphs.font.selectedLayers ] )
GlyphnameDialog( selected_glyphs )