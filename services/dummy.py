from models import SpeciesMatchResult
from services.species import species_matcher
import json

def get_dummy_response() -> SpeciesMatchResult:
  try:
    with open("dummy.json") as file:
      data = json.load(file)
      print('loaded')
      species_names = data["matching_species"]
      print(species_names)
      matching_trees = species_matcher.get_tree_details(species_names)
      print(matching_trees)
      return SpeciesMatchResult(
        altitude=data["altitude"],
        climate=data["climate"],
        soil=data["soil"],
        matching_species=matching_trees
      )
  except Exception as e:
    raise ValueError(f"Dummy response error: {str(e)}")