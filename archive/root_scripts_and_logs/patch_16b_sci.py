with open("scripts/steps/step_16b_build_feature_vector_J1419.py", "r") as f:
    code = f.read()

replacement = """
      "source": "extracted from Pettini & Cooke 2012 (arXiv:1205.3785)",
      "reference_redshift": 3.049840,
      "is_proxy": False,
      "scientific_use": True,
      "D_window_used": False,
"""
code = code.replace("""
      "source": "extracted from Pettini & Cooke 2012 (arXiv:1205.3785)",
      "D_window_used": False,
""", replacement)

with open("scripts/steps/step_16b_build_feature_vector_J1419.py", "w") as f:
    f.write(code)
