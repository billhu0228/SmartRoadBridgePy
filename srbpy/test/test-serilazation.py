from srbpy.model import Model, Bridge, Span
from srbpy.alignment import Align

ali = Align(path="00-MainLine/M1K-0312", name="M1K")
ali.set_width(width=21.6)
bri = Bridge(name="BridgeA")
spa = Span(align=ali, bridge=bri, station=16500, ang_deg=90)

md = Model()
md.add_align(ali)
md.add_bridge(bri)
md.add_span(spa)

print(ali.serialize(step=50))
print(bri.serialize())
print(spa.serialize())
