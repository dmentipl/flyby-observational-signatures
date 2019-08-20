#
# Makefile for flyby observational paper
#

.PHONY: help
help:
	@echo "What do you want to make?"
	@echo ""
	@echo "    - radiative-transfer: run MCFOST on Phantom data"
	@echo "    - figures: use pymcfost to make figures from MCFOST data"
	@echo ""
	@echo "Note: figures require radiative-transfer to have been run"

.PHONY: figures
figures:
	./flyby_make_figures_for_paper.py

.PHONY: radiative-transfer
radiative-transfer:
	./flyby_run_mcfost.py
