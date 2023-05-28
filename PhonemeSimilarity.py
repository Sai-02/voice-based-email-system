from pyphonetics import Soundex
from pyphonetics import RefinedSoundex
rs = RefinedSoundex()
soundex = Soundex()
print(rs.distance('next mail','nxt ml', metric='levenshtein'))