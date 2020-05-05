
all:

%:
	@echo Executing \"make $@\" on all LUFA library elements.
	@echo
	$(MAKE) -C LUFA $@
	$(MAKE) -C Demos $@
	$(MAKE) -C Projects $@
	$(MAKE) -C Bootloaders $@
	@echo
	@echo LUFA \"make $@\" operation complete.
